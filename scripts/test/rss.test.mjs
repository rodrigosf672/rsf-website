// RSS feed validity + freshness tests.
// Run: npm run test:scripts   (node --test scripts/test/*.test.mjs)
//
// Guards: the feed exists, is well-formed RSS 2.0, uses only absolute URLs,
// escapes correctly, and contains every published post (so publishing a post
// without running `npm run build:rss` fails CI instead of shipping a stale feed).

import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync, readdirSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const RSS_PATH = join(ROOT, "site/rss.xml");
const BLOG_DIR = join(ROOT, "site/blog");

const feed = existsSync(RSS_PATH) ? readFileSync(RSS_PATH, "utf8") : "";

const publishedCanonicals = readdirSync(BLOG_DIR)
  .filter((f) => f.endsWith(".html") && f !== "index.html")
  .map((f) => readFileSync(join(BLOG_DIR, f), "utf8"))
  .filter((html) => html.includes('class="post-body"'))
  .map((html) => (html.match(/<link rel="canonical" href="(.*?)"/) || [, ""])[1])
  .filter(Boolean);

test("rss.xml exists and declares RSS 2.0", () => {
  assert.ok(feed, "site/rss.xml is missing — run npm run build:rss");
  assert.match(feed, /^<\?xml version="1\.0" encoding="UTF-8"\?>/);
  assert.match(feed, /<rss version="2\.0"/);
  assert.match(feed, /<channel>[\s\S]*<title>[\s\S]*<link>[\s\S]*<description>[\s\S]*<\/channel>/);
  assert.match(feed, /<atom:link[^>]+rel="self"[^>]+type="application\/rss\+xml"/);
});

test("every published post appears in the feed as an item + guid", () => {
  assert.ok(publishedCanonicals.length >= 1);
  const itemCount = (feed.match(/<item>/g) || []).length;
  assert.equal(itemCount, publishedCanonicals.length, "feed item count does not match published post count — run npm run build:rss");
  for (const url of publishedCanonicals) {
    assert.ok(feed.includes(`<link>${url}</link>`), `${url} missing <link> in rss.xml (stale feed?)`);
    assert.ok(feed.includes(`<guid isPermaLink="true">${url}</guid>`), `${url} missing <guid> in rss.xml`);
  }
});

test("every item carries the required RSS fields", () => {
  for (const item of feed.match(/<item>[\s\S]*?<\/item>/g) || []) {
    for (const tag of ["title", "link", "description", "pubDate", "guid"]) {
      assert.match(item, new RegExp(`<${tag}[ >]`), `an <item> is missing <${tag}>`);
    }
    // pubDate must be RFC-822 (day, DD Mon YYYY hh:mm:ss +0000)
    assert.match(item, /<pubDate>[A-Z][a-z]{2}, \d{2} [A-Z][a-z]{2} \d{4} \d{2}:\d{2}:\d{2} [+-]\d{4}<\/pubDate>/);
  }
});

test("all feed URLs are absolute", () => {
  for (const url of feed.match(/<link>([^<]*)<\/link>/g) || []) {
    assert.match(url, /<link>https?:\/\//, `non-absolute <link>: ${url}`);
  }
  for (const g of feed.match(/<guid[^>]*>([^<]*)<\/guid>/g) || []) {
    assert.match(g, /https?:\/\//, `non-absolute <guid>: ${g}`);
  }
});

test("feed has no unescaped ampersands (well-formedness)", () => {
  const bad = feed.match(/&(?!(amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)/g);
  assert.equal(bad, null, `unescaped & found in rss.xml: ${bad}`);
});

test("main pages advertise the feed for auto-discovery", () => {
  const pages = ["site/index.html", "site/blog/index.html", "site/publications.html"];
  for (const p of pages) {
    const html = readFileSync(join(ROOT, p), "utf8");
    assert.match(
      html,
      /<link rel="alternate" type="application\/rss\+xml"[^>]+href="\/rss\.xml"/,
      `${p} is missing the RSS <link rel="alternate"> discovery tag`,
    );
  }
});
