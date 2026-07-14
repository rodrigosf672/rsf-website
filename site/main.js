// Theme toggle — the initial theme is set by an inline script in <head>
// (before first paint) from localStorage or prefers-color-scheme.
(function () {
  const root = document.documentElement;
  const btn = document.querySelector(".theme-toggle");
  if (!btn) return;

  function render() {
    const dark = root.getAttribute("data-theme") !== "light";
    btn.textContent = dark ? "--light" : "--dark";
    btn.setAttribute("aria-label", dark ? "Switch to light theme" : "Switch to dark theme");
  }

  btn.addEventListener("click", function () {
    const next = root.getAttribute("data-theme") === "light" ? "dark" : "light";
    root.setAttribute("data-theme", next);
    try { localStorage.setItem("theme", next); } catch (e) { /* private mode */ }
    render();
  });

  render();
})();

// Gallery: snap-scrolling strip with drag-to-swipe, event stepping, dots, and a lightbox.
(function () {
  const strip = document.querySelector(".gallery-strip");
  if (!strip) return;
  const events = Array.from(strip.querySelectorAll(".event"));
  const controls = document.querySelector(".gallery-controls");
  const dotsWrap = document.querySelector(".gallery-dots");

  const dots = events.map(function (ev, k) {
    const b = document.createElement("button");
    b.className = "g-dot";
    b.type = "button";
    b.setAttribute("aria-label", "Go to: " + (ev.querySelector("figcaption") || {}).textContent);
    b.addEventListener("click", function () { scrollToEvent(k); });
    dotsWrap.appendChild(b);
    return b;
  });

  function currentIndex() {
    const x = strip.scrollLeft + 12;
    let idx = 0;
    events.forEach(function (ev, k) { if (ev.offsetLeft - strip.offsetLeft <= x) idx = k; });
    return idx;
  }
  function scrollToEvent(k) {
    k = Math.max(0, Math.min(events.length - 1, k));
    strip.scrollTo({ left: events[k].offsetLeft - strip.offsetLeft, behavior: "smooth" });
  }
  document.querySelector(".g-prev").addEventListener("click", function () { scrollToEvent(currentIndex() - 1); });
  document.querySelector(".g-next").addEventListener("click", function () { scrollToEvent(currentIndex() + 1); });

  function sync() {
    const overflow = strip.scrollWidth > strip.clientWidth + 4;
    controls.style.display = overflow ? "" : "none";
    dotsWrap.style.display = overflow ? "" : "none";
    const idx = currentIndex();
    dots.forEach(function (d, k) { d.classList.toggle("is-active", k === idx); });
  }
  strip.addEventListener("scroll", function () { requestAnimationFrame(sync); }, { passive: true });
  window.addEventListener("resize", sync);
  sync();

  // Drag-to-swipe with a mouse (touch already swipes natively).
  let dragging = false, dragMoved = false, startX = 0, startLeft = 0;
  strip.addEventListener("pointerdown", function (e) {
    if (e.pointerType !== "mouse" || e.button !== 0) return;
    dragging = true; dragMoved = false; startX = e.clientX; startLeft = strip.scrollLeft;
  });
  window.addEventListener("pointermove", function (e) {
    if (!dragging) return;
    const dx = e.clientX - startX;
    if (!dragMoved && Math.abs(dx) > 10) {
      dragMoved = true;
      strip.classList.add("dragging");
    }
    if (dragMoved) strip.scrollLeft = startLeft - dx;
  });
  window.addEventListener("pointerup", function () {
    if (!dragging) return;
    dragging = false;
    strip.classList.remove("dragging");
    if (dragMoved) {
      scrollToEvent(currentIndex()); // settle on a snap point
      // swallow the click that follows a drag
      strip.addEventListener("click", function stop(e) { e.stopPropagation(); e.preventDefault(); }, { capture: true, once: true });
    }
  });

  // Lightbox (plain fixed overlay — no <dialog> dependency)
  const buttons = Array.from(strip.querySelectorAll(".photo-btn"));
  const photos = buttons.map(function (b) { return b.querySelector("img"); });
  const lb = document.createElement("div");
  lb.className = "lightbox";
  lb.hidden = true;
  lb.setAttribute("role", "dialog");
  lb.setAttribute("aria-modal", "true");
  lb.setAttribute("aria-label", "Photo viewer");
  lb.innerHTML = '<button class="lb-close" type="button" aria-label="Close photo viewer">&times;</button>' +
    '<button class="lb-prev" type="button" aria-label="Previous photo">&larr;</button>' +
    '<figure><img alt=""><figcaption></figcaption></figure>' +
    '<button class="lb-next" type="button" aria-label="Next photo">&rarr;</button>';
  document.body.appendChild(lb);
  const lbImg = lb.querySelector("img");
  const lbCap = lb.querySelector("figcaption");
  const lbClose = lb.querySelector(".lb-close");
  let cur = 0, lastFocus = null;

  function show(k) {
    cur = (k + photos.length) % photos.length;
    lbImg.src = photos[cur].src;
    lbImg.alt = photos[cur].alt;
    lbCap.textContent = photos[cur].closest(".event").querySelector("figcaption").textContent;
  }
  function openLb(k) {
    lastFocus = document.activeElement;
    show(k);
    lb.hidden = false;
    document.body.style.overflow = "hidden";
    lbClose.focus();
    document.addEventListener("keydown", onKey);
  }
  function closeLb() {
    lb.hidden = true;
    document.body.style.overflow = "";
    document.removeEventListener("keydown", onKey);
    if (lastFocus) lastFocus.focus();
  }
  function onKey(e) {
    if (e.key === "Escape") closeLb();
    if (e.key === "ArrowLeft") show(cur - 1);
    if (e.key === "ArrowRight") show(cur + 1);
  }
  buttons.forEach(function (b, k) {
    b.addEventListener("click", function () { openLb(k); });
  });
  lbClose.addEventListener("click", closeLb);
  lb.querySelector(".lb-prev").addEventListener("click", function () { show(cur - 1); });
  lb.querySelector(".lb-next").addEventListener("click", function () { show(cur + 1); });
  lb.addEventListener("click", function (e) { if (e.target === lb) closeLb(); });
})();

// Site assistants: `ask-rodrigo` on the home terminal, `ask-blog` on the blog terminal.
// The chat panel's data-scope attribute selects persona, command, and suggestions.
(function () {
  const termInput = document.getElementById("term-input");
  const chat = document.getElementById("chat");
  if (!termInput || !chat) return;

  const scope = chat.getAttribute("data-scope") || "site";
  const CMD = scope === "blog" ? "ask-blog" : "ask-rodrigo";
  const BOT = scope === "blog" ? "blog-bot: " : "rsf-bot: ";
  const WELCOME = scope === "blog"
    ? "Ask me about the blog posts: what they argue, what they review, and how the interactive notebooks work. I only answer from the published posts."
    : "Ask me about my work, projects, talks, publications, GitHub repositories, or professional background.";

  const termBody = termInput.closest(".terminal-body");
  const log = chat.querySelector(".chat-log");
  const form = chat.querySelector(".chat-form");
  const input = chat.querySelector(".chat-input");
  const sendBtn = chat.querySelector(".chat-send");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const getApiBase = function () { return (document.querySelector('meta[name="assistant-api"]') || {}).content || ""; };

  const SUGGESTIONS = scope === "blog"
    ? [
        "What is the latest post about?",
        "Why does Rodrigo recommend Generative AI in Action?",
        "What does the review say about the GenAI application stack?",
        "What can I do in the interactive notebook?",
        "What does the post say about evals and testing?",
        "How did Rodrigo end up with this book?",
      ]
    : [
        "Who is Rodrigo and what does he do?",
        "What is Rodrigo working on right now?",
        "Which projects should I look at first?",
        "What are his most cited publications?",
        "What talks has he given recently?",
        "How did a chemist end up building developer tools?",
        "How can I collaborate with or hire Rodrigo?",
      ];
  const history = [];       // {role, content} turns sent to the API
  const asked = [];         // for arrow-key recall
  let askedPos = -1;
  let busy = false;

  /* ----- terminal command handling ----- */
  function echo(line, isErr) {
    const s = document.createElement("span");
    s.className = "echo-line" + (isErr ? " echo-err" : "");
    s.textContent = line;
    const promptSpan = termInput.parentNode.previousElementSibling; // the "$" before the input
    termBody.insertBefore(s, promptSpan);
    termBody.insertBefore(document.createTextNode("\n"), promptSpan);
  }
  termInput.addEventListener("keydown", function (e) {
    if (e.key !== "Enter") return;
    const cmd = termInput.value.trim();
    termInput.value = "";
    if (!cmd) return;
    if (cmd === CMD || cmd === "ask") { openChat(); return; }
    if (cmd === "help") { echo("available commands: " + CMD + ", help"); return; }
    echo("command not found: " + cmd + " — try " + CMD, true);
  });

  /* ----- chat panel ----- */
  function openChat() {
    chat.hidden = false;
    if (!log.childElementCount) renderWelcome();
    input.focus();
    chat.scrollIntoView({ block: "nearest", behavior: reduceMotion ? "auto" : "smooth" });
  }
  function closeChat() {
    chat.hidden = true;
    termInput.focus();
  }
  chat.addEventListener("keydown", function (e) { if (e.key === "Escape") closeChat(); });

  function renderWelcome() {
    const m = msgEl("assistant");
    m.text.textContent = WELCOME;
    m.text.classList.add("chat-welcome");
    const sug = document.createElement("div");
    sug.className = "chat-suggest";
    sug.setAttribute("aria-label", "Suggested questions");
    SUGGESTIONS.forEach(function (q) {
      const b = document.createElement("button");
      b.type = "button";
      b.textContent = q;
      b.addEventListener("click", function () { send(q); });
      sug.appendChild(b);
    });
    m.wrap.appendChild(sug);
  }

  function msgEl(role) {
    const wrap = document.createElement("div");
    wrap.className = "chat-msg " + role;
    const who = document.createElement("span");
    who.className = "who";
    who.textContent = role === "user" ? "> you: " : BOT;
    const text = document.createElement("span");
    text.className = "msg-text";
    wrap.appendChild(who);
    wrap.appendChild(text);
    log.appendChild(wrap);
    log.scrollTop = log.scrollHeight;
    return { wrap, text };
  }

  // minimal safe renderer: escapes by construction, supports **bold** only
  function renderRich(el, raw) {
    el.textContent = "";
    raw.split("**").forEach(function (part, k) {
      if (k % 2 === 1) {
        const b = document.createElement("strong");
        b.textContent = part;
        el.appendChild(b);
      } else {
        el.appendChild(document.createTextNode(part));
      }
    });
  }

  function safeLink(title, url) {
    const a = document.createElement("a");
    if (/^https?:\/\//.test(url)) { a.href = url; a.rel = "noopener"; }
    a.textContent = title;
    return a;
  }

  function renderFooter(wrap, meta) {
    const foot = document.createElement("div");
    foot.className = "msg-footer";
    const conf = document.createElement("div");
    conf.innerHTML = "";
    const label = document.createElement("span");
    label.textContent = "Confidence: ";
    const val = document.createElement("span");
    val.className = "conf conf-" + meta.confidence;
    val.textContent = meta.confidence;
    conf.appendChild(label); conf.appendChild(val);
    foot.appendChild(conf);

    [["Sources", meta.sources], ["Related", meta.related]].forEach(function (pair) {
      if (!pair[1] || !pair[1].length) return;
      const row = document.createElement("div");
      row.className = "foot-row";
      row.appendChild(document.createTextNode(pair[0] + ": "));
      pair[1].forEach(function (s, k) {
        if (k) row.appendChild(document.createTextNode(" · "));
        row.appendChild(safeLink(s.title, s.url));
      });
      foot.appendChild(row);
    });
    wrap.appendChild(foot);

    if (meta.handoff) {
      const h = document.createElement("div");
      h.className = "chat-handoff";
      h.appendChild(document.createTextNode("Didn't find what you were looking for?"));
      const a = document.createElement("a");
      a.href = "mailto:rodrigosf672@gmail.com?subject=" + encodeURIComponent("Hello Rodrigo (via rodrigosf.com)");
      a.textContent = "Send Rodrigo a message";
      h.appendChild(document.createElement("br"));
      h.appendChild(a);
      wrap.appendChild(h);
    }
    log.scrollTop = log.scrollHeight;
  }

  async function send(q) {
    if (busy) return;
    q = (q || "").trim();
    if (!q) return;
    asked.push(q); askedPos = asked.length;
    msgEl("user").text.textContent = q;
    input.value = "";

    const m = msgEl("assistant");
    const apiBase = getApiBase();
    if (!apiBase) {
      m.text.textContent = "The assistant isn't connected yet — the API endpoint hasn't been configured. Meanwhile, everything it would tell you lives on this site: check the projects, talks, and publications pages, or email rodrigosf672@gmail.com.";
      return;
    }

    busy = true; sendBtn.disabled = true;
    const cursor = document.createElement("span");
    cursor.className = "stream-cursor";
    m.wrap.appendChild(cursor);
    let full = "";

    try {
      const res = await fetch(apiBase.replace(/\/$/, "") + "/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: q, history: history.slice(-8), scope: scope }),
      });
      if (!res.ok) {
        const err = await res.json().catch(function () { return {}; });
        throw new Error(err.error || ("Request failed (" + res.status + ")"));
      }
      const reader = res.body.getReader();
      const dec = new TextDecoder();
      let buf = "";
      for (;;) {
        const r = await reader.read();
        if (r.done) break;
        buf += dec.decode(r.value, { stream: true });
        const parts = buf.split("\n\n");
        buf = parts.pop();
        for (const part of parts) {
          if (!part.startsWith("data: ")) continue;
          let evt;
          try { evt = JSON.parse(part.slice(6)); } catch { continue; }
          if (evt.type === "delta") {
            full += evt.text;
            renderRich(m.text, full);
            log.scrollTop = log.scrollHeight;
          } else if (evt.type === "meta") {
            renderFooter(m.wrap, evt);
          } else if (evt.type === "error") {
            throw new Error(evt.error);
          }
        }
      }
      history.push({ role: "user", content: q }, { role: "assistant", content: full });
    } catch (e) {
      m.text.textContent = (full ? full + "\n\n" : "") + "⚠ " + (e.message || "Something went wrong — please try again.");
    } finally {
      cursor.remove();
      busy = false; sendBtn.disabled = false;
      log.scrollTop = log.scrollHeight;
    }
  }

  form.addEventListener("submit", function (e) { e.preventDefault(); send(input.value); });
  input.addEventListener("keydown", function (e) {
    if (e.key === "ArrowUp" && asked.length) {
      askedPos = Math.max(0, askedPos - 1);
      input.value = asked[askedPos];
      e.preventDefault();
    } else if (e.key === "ArrowDown" && asked.length) {
      askedPos = Math.min(asked.length, askedPos + 1);
      input.value = asked[askedPos] || "";
      e.preventDefault();
    }
  });
})();
