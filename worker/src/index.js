// ask-rodrigo — Portfolio Assistant API (Cloudflare Worker).
//
// POST /api/chat  {message: string, history?: [{role, content}]}
//   -> text/event-stream of {type:"delta"|"meta"|"done"|"error", ...}
//
// Retrieval-augmented: every answer is grounded in worker/src/index-data.js
// (built by scripts/build-index.mjs). Generation runs on Workers AI.

import INDEX from "./index-data.js";
import {
  LIMITS, REFUSAL_TEXT, BLOG_REFUSAL_TEXT, validateRequest, retrieve, confidenceFor,
  splitSourcesAndRelated, scopeChunks, systemPrompt, blogSystemPrompt, wantsContact,
  cacheKeyFor, makeRateLimiter, sse,
} from "./lib.js";

const GEN_MODEL = "@cf/meta/llama-3.3-70b-instruct-fp8-fast";
const EMBED_MODEL = INDEX.model || "@cf/baai/bge-base-en-v1.5";
const ALLOWED_ORIGINS = [
  "https://rodrigosf.com", "https://www.rodrigosf.com",
  "http://localhost:4321", "http://127.0.0.1:4321",
];

const allow = makeRateLimiter();

function corsHeaders(origin) {
  const ok = ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];
  return {
    "Access-Control-Allow-Origin": ok,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Vary": "Origin",
  };
}

const json = (obj, status, extra = {}) =>
  new Response(JSON.stringify(obj), { status, headers: { "Content-Type": "application/json", ...extra } });

export default {
  async fetch(request, env, ctx) {
    const origin = request.headers.get("Origin") || "";
    const cors = corsHeaders(origin);

    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
    const url = new URL(request.url);
    if (url.pathname !== "/api/chat" || request.method !== "POST")
      return json({ error: "Not found" }, 404, cors);

    // rate limit (best-effort per isolate; add a Cloudflare WAF rule for hard limits)
    const ip = request.headers.get("CF-Connecting-IP") || "unknown";
    if (!allow(ip)) {
      return json({ error: "Rate limit reached — please try again in a little while." }, 429, cors);
    }

    let body;
    try { body = await request.json(); } catch { return json({ error: "Body must be JSON." }, 400, cors); }
    const v = validateRequest(body);
    if (!v.ok) return json({ error: v.error }, 400, cors);
    const { message, history, scope } = v;

    // Log volume only — never message contents.
    console.log(JSON.stringify({ evt: "chat", scope, len: message.length, turns: history.length }));

    // Cache common first-turn questions.
    const cacheable = history.length === 0;
    const cacheKey = cacheable ? cacheKeyFor(message, scope) : null;
    if (cacheKey) {
      const hit = await caches.default.match(new Request(cacheKey));
      if (hit) {
        const cached = await hit.json();
        return streamReplay(cached, cors);
      }
    }

    // Retrieval, restricted to the requested scope.
    const pool = scopeChunks(INDEX.chunks, scope);
    if (!pool.length || !pool[0].vec) {
      return json({ error: "The assistant index has not been built yet." }, 503, cors);
    }
    const qe = await env.AI.run(EMBED_MODEL, {
      text: ["Represent this sentence for searching relevant passages: " + message],
    });
    const ranked = retrieve(qe.data[0], pool);
    const confidence = confidenceFor(ranked[0]?.score ?? 0);
    const handoff = wantsContact(message);
    const refusal = scope === "blog" ? BLOG_REFUSAL_TEXT : REFUSAL_TEXT;

    if (!confidence) {
      const payload = { text: refusal, meta: { confidence: "Low", sources: [], related: relatedFallback(scope), handoff: true } };
      if (cacheKey) ctx.waitUntil(putCache(cacheKey, payload));
      return streamReplay(payload, cors);
    }

    const { used, sources, related } = splitSourcesAndRelated(ranked);
    const messages = [
      { role: "system", content: scope === "blog" ? blogSystemPrompt(used) : systemPrompt(used) },
      ...history,
      { role: "user", content: message },
    ];

    const ai = await env.AI.run(GEN_MODEL, {
      messages,
      stream: true,
      max_tokens: LIMITS.MAX_OUTPUT_TOKENS,
      temperature: 0.2,
    });

    // Transform Workers AI SSE -> our protocol; capture full text for caching.
    const meta = { confidence, sources, related, handoff };
    let full = "";
    const { readable, writable } = new TransformStream();
    const writer = writable.getWriter();
    const enc = new TextEncoder();

    ctx.waitUntil((async () => {
      try {
        const reader = ai.getReader();
        const dec = new TextDecoder();
        let buf = "";
        for (;;) {
          const { done, value } = await reader.read();
          if (done) break;
          buf += dec.decode(value, { stream: true });
          const lines = buf.split("\n");
          buf = lines.pop();
          for (const line of lines) {
            if (!line.startsWith("data: ")) continue;
            const data = line.slice(6).trim();
            if (data === "[DONE]") continue;
            try {
              const delta = String(JSON.parse(data).response ?? "");
              if (delta) {
                full += delta;
                await writer.write(enc.encode(sse({ type: "delta", text: delta })));
              }
            } catch { /* partial frame */ }
          }
        }
        await writer.write(enc.encode(sse({ type: "meta", ...meta })));
        await writer.write(enc.encode(sse({ type: "done" })));
        if (cacheKey && full) await putCache(cacheKey, { text: full, meta });
      } catch (e) {
        console.log(JSON.stringify({ evt: "error", msg: String(e).slice(0, 200) }));
        await writer.write(enc.encode(sse({ type: "error", error: "The assistant hit a temporary error. Please try again." })));
      } finally {
        await writer.close();
      }
    })());

    return new Response(readable, {
      headers: { "Content-Type": "text/event-stream", "Cache-Control": "no-store", ...cors },
    });
  },
};

function relatedFallback(scope) {
  // Stable pointers for the refusal path so visitors can keep exploring.
  if (scope === "blog") {
    const posts = [];
    const seen = new Set();
    for (const c of INDEX.chunks) {
      if (c.type !== "blog" || seen.has(c.url) || !c.title.startsWith("Blog post:")) continue;
      posts.push({ title: c.title.replace(/^Blog post: /, ""), url: c.url, type: "blog" });
      seen.add(c.url);
      if (posts.length >= 3) break;
    }
    return posts.length ? posts : [{ title: "Blog", url: "https://rodrigosf.com/blog/", type: "blog" }];
  }
  return [
    { title: "Projects", url: "https://rodrigosf.com/projects.html", type: "project" },
    { title: "Talks", url: "https://rodrigosf.com/talks.html", type: "talk" },
    { title: "Publications", url: "https://rodrigosf.com/publications.html", type: "publication" },
  ];
}

async function putCache(cacheKey, payload) {
  await caches.default.put(
    new Request(cacheKey),
    new Response(JSON.stringify(payload), {
      headers: { "Content-Type": "application/json", "Cache-Control": `max-age=${LIMITS.CACHE_TTL_SECONDS}` },
    }),
  );
}

/** Replay a cached/complete answer through the same SSE protocol. */
function streamReplay(payload, cors) {
  const enc = new TextEncoder();
  const stream = new ReadableStream({
    start(controller) {
      // chunk the text so the client still renders a typing effect
      const words = payload.text.split(/(?<=\s)/);
      for (let i = 0; i < words.length; i += 4)
        controller.enqueue(enc.encode(sse({ type: "delta", text: words.slice(i, i + 4).join("") })));
      controller.enqueue(enc.encode(sse({ type: "meta", ...payload.meta })));
      controller.enqueue(enc.encode(sse({ type: "done" })));
      controller.close();
    },
  });
  return new Response(stream, {
    headers: { "Content-Type": "text/event-stream", "Cache-Control": "no-store", ...cors },
  });
}
