#!/usr/bin/env node
/**
 * build-rss.mjs — generate a valid RSS 2.0 feed from the published blog posts.
 *
 * Reads only site/blog/*.html (the deployed posts; drafts live in drafts/ and
 * are never served, so they are excluded automatically). All feed metadata is
 * sourced from existing page metadata rather than duplicated here:
 *   - base URL, feed title/description  <- site/blog/index.html
 *   - per-post title/excerpt/date/URL   <- each post's own <head>/<h1>
 *   - categories                        <- the blog index listing's venue line
 *
 * Writes site/rss.xml. Run it after publishing a post:  npm run build:rss
 */

import { readFileSync, writeFileSync } from "node:fs";
import { readdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const read = (p) => readFileSync(join(ROOT, p), "utf8");
const AUTHOR = "Rodrigo Silva Ferreira";
const AUTHOR_EMAIL = "rodrigosf672@gmail.com";

const pick = (html, re) => (html.match(re) || [, ""])[1].trim();
const decode = (s) =>
  s.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">")
   .replace(/&quot;/g, '"').replace(/&#39;|&apos;/g, "'").replace(/&nbsp;/g, " ");
const esc = (s) =>
  s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
   .replace(/"/g, "&quot;").replace(/'/g, "&apos;");

const MONTHS = ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"];
const DOW = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

/** "July 21, 2026" -> Date at UTC midnight (deterministic, timezone-free). */
function parseDate(str) {
  const m = str.match(/([A-Za-z]+)\s+(\d{1,2}),\s+(\d{4})/);
  if (!m) return null;
  const month = MONTHS.indexOf(m[1]);
  if (month < 0) return null;
  return new Date(Date.UTC(Number(m[3]), month, Number(m[2])));
}

/** Date -> RFC-822 (required by RSS 2.0), e.g. "Tue, 21 Jul 2026 00:00:00 +0000". */
function rfc822(d) {
  const pad = (n) => String(n).padStart(2, "0");
  return `${DOW[d.getUTCDay()]}, ${pad(d.getUTCDate())} ${MON[d.getUTCMonth()]} ${d.getUTCFullYear()} `
    + `${pad(d.getUTCHours())}:${pad(d.getUTCMinutes())}:${pad(d.getUTCSeconds())} +0000`;
}

// ---- site-level metadata, from the blog index page ----
const blogIndex = read("site/blog/index.html");
const feedTitle = decode(pick(blogIndex, /<title>(.*?)<\/title>/s));
const feedDesc = decode(pick(blogIndex, /<meta name="description" content="(.*?)"/s));
const blogCanonical = pick(blogIndex, /<link rel="canonical" href="(.*?)"/s); // https://rodrigosf.com/blog/
const BASE = new URL(blogCanonical).origin; // https://rodrigosf.com
const feedUrl = `${BASE}/rss.xml`;

// categories per post, from the listing's venue line ("essay · interactive marimo notebook")
const categoriesByPath = {};
for (const m of blogIndex.matchAll(
  /<article class="talk">[\s\S]*?<a href="(\/blog\/[^"]+)"[\s\S]*?<span class="venue">([^<]*)<\/span>/g,
)) {
  categoriesByPath[m[1]] = decode(m[2]).split("·").map((s) => s.trim()).filter(Boolean);
}

// ---- one <item> per published post ----
const items = readdirSync(join(ROOT, "site/blog"))
  .filter((f) => f.endsWith(".html") && f !== "index.html")
  .map((f) => read(`site/blog/${f}`))
  .filter((html) => html.includes('class="post-body"'))
  .map((html) => {
    const canonical = pick(html, /<link rel="canonical" href="(.*?)"/s);
    const title = decode(pick(html, /<h1>(.*?)<\/h1>/s));
    const description = decode(pick(html, /<meta name="description" content="(.*?)"/s));
    const dateText = pick(html, /<p class="post-meta">([^·]*?)·/s);
    const date = parseDate(dateText);
    const path = new URL(canonical).pathname;
    const categories = categoriesByPath[path] || [];
    return { canonical, title, description, date, categories };
  })
  .filter((it) => it.canonical && it.date) // skip anything missing a URL or a real date
  .sort((a, b) => b.date - a.date); // newest first

if (!items.length) {
  console.error("No published posts found in site/blog/. Aborting RSS build.");
  process.exit(1);
}

const itemXml = items
  .map((it) => {
    const cats = it.categories.map((c) => `      <category>${esc(c)}</category>`).join("\n");
    return `    <item>
      <title>${esc(it.title)}</title>
      <link>${esc(it.canonical)}</link>
      <description>${esc(it.description)}</description>
      <dc:creator>${esc(AUTHOR)}</dc:creator>
${cats ? cats + "\n" : ""}      <pubDate>${rfc822(it.date)}</pubDate>
      <guid isPermaLink="true">${esc(it.canonical)}</guid>
    </item>`;
  })
  .join("\n");

const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <channel>
    <title>${esc(feedTitle)}</title>
    <link>${esc(blogCanonical)}</link>
    <description>${esc(feedDesc)}</description>
    <language>en-us</language>
    <managingEditor>${AUTHOR_EMAIL} (${esc(AUTHOR)})</managingEditor>
    <webMaster>${AUTHOR_EMAIL} (${esc(AUTHOR)})</webMaster>
    <lastBuildDate>${rfc822(items[0].date)}</lastBuildDate>
    <atom:link href="${esc(feedUrl)}" rel="self" type="application/rss+xml"/>
${itemXml}
  </channel>
</rss>
`;

writeFileSync(join(ROOT, "site/rss.xml"), xml);
console.log(`wrote site/rss.xml — ${items.length} item(s):`);
for (const it of items) console.log(`  ${rfc822(it.date).slice(0, 16)}  ${it.canonical}`);
