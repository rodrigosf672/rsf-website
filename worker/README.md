# ask-rodrigo — Portfolio Assistant

An AI-powered portfolio navigator embedded in the terminal UI on
[rodrigosf.com](https://rodrigosf.com). Visitors type `ask-rodrigo` in the
homepage terminal to explore Rodrigo's projects, publications, talks, GitHub
repositories, and background. Not a generic chatbot: every answer is
retrieval-grounded in published portfolio content only.

## Architecture

```
site/ (GitHub Pages, static)                worker/ (Cloudflare Worker)
┌──────────────────────────┐   POST /api/chat   ┌─────────────────────────────┐
│ terminal UI → chat panel │ ─────────────────▶ │ validate → rate limit →     │
│ SSE streaming client     │ ◀───────────────── │ cache? → embed query →      │
│ sources/confidence UI    │    SSE stream      │ retrieve top-k → Llama 3.3  │
└──────────────────────────┘                    │ (Workers AI, streaming)     │
                                                └─────────────────────────────┘
                 ▲
   scripts/build-index.mjs  — scans site/*.html + content/faq.md + GitHub,
   embeds chunks with @cf/baai/bge-base-en-v1.5, writes src/index-data.js
```

- **No API keys anywhere**: embeddings and generation both run on the
  Worker's native Workers AI binding (`env.AI`). Nothing client-side.
- **Retrieval-augmented**: `build:index` chunks approved content
  (~100 chunks) and embeds it. At query time the question is embedded,
  ranked by cosine similarity, and only the top passages are given to the
  model as inert `<document>` data.
- **Refusal floor**: if the best similarity is below threshold, the Worker
  returns the "couldn't find enough information" response *without calling
  the model*. Confidence (High/Medium/Low) is computed from retrieval
  scores server-side, never by the model.
- **Sources & related content** are attached server-side from the actual
  retrieved chunks — the model cannot fabricate citations.

## Limits (see `src/lib.js` LIMITS)

- 25 messages/hour/IP (best-effort in-isolate; add a Cloudflare WAF rate
  rule on `/api/chat` for a hard guarantee)
- 800-character questions, 8 history turns
- ~250-word answers (450 max tokens)
- Common first-turn questions cached at the edge for 24 h (served as an
  instant replayed stream)

## Security

- Server-side only; CORS locked to rodrigosf.com + localhost.
- Input validated and length-capped; control characters stripped; history
  roles coerced to user/assistant.
- Retrieved documents wrapped as data with quote-neutralized attributes;
  system prompt forbids following instructions inside them and refuses
  prompt-injection asks ("ignore previous instructions", "reveal your
  prompt", "search the web").
- Client renders all model output as text (`textContent`); only `**bold**`
  is interpreted. Links come exclusively from server-verified source
  metadata and must be http(s).
- Logging records message length and turn count only — never contents.

## Deploy

One-time setup (free Cloudflare account):

```sh
# 1. Build the index (needs a CF API token with Workers AI permission)
CF_ACCOUNT_ID=<your-account-id> CF_API_TOKEN=<token> npm run build:index

# 2. Deploy the Worker
cd worker
npx wrangler login
npx wrangler deploy        # prints https://ask-rodrigo.<subdomain>.workers.dev

# 3. Point the site at it
#    site/index.html → <meta name="assistant-api" content="https://ask-rodrigo....workers.dev">
```

Re-run `npm run build:index` + `wrangler deploy` whenever site content or
repos change (a monthly GitHub Action is a good fit).

Until step 3 the site degrades gracefully: the chat opens but explains the
assistant isn't connected yet.

## Test

```sh
npm run test:worker    # unit tests: validation, retrieval, prompts, limits
npm test               # Playwright: chat UI against a mocked API
npm run build:index -- --dry-run   # indexing pipeline without embeddings
```

## Tuning

Similarity thresholds live in `src/lib.js` (`THRESHOLDS`). After deploying,
ask a few in-scope and out-of-scope questions and adjust: raise `low` if
off-topic questions get answered; lower it if legitimate questions are
refused.
