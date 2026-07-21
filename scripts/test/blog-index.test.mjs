// Integrity tests for blog indexing and site consistency.
// Run: npm run test:scripts   (node --test scripts/test/*.test.mjs)
//
// These guard the exact classes of bug that have bitten this repo:
//   - post-body extraction truncating on nested <div>s (dropping sections)
//   - publishing a post but forgetting to reindex the assistant
//   - bumping styles.css on some pages but not others (stale CSS cache)

import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync, readdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { extractBody, headingsOf } from "../lib/parse-blog.mjs";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const BLOG_DIR = join(ROOT, "site/blog");

const posts = readdirSync(BLOG_DIR)
  .filter((f) => f.endsWith(".html") && f !== "index.html")
  .map((f) => ({ f, html: readFileSync(join(BLOG_DIR, f), "utf8") }))
  .filter((p) => p.html.includes('class="post-body"'));

/* ---------- extractBody: the truncation bug ---------- */

test("extractBody is not truncated by nested divs (the card/figure bug)", () => {
  const html =
    '<div class="post-body"><h2>First</h2><p>a</p>' +
    '<figure><div><div>nested</div></div></figure>' +
    '<h2>Last</h2><p>final section text</p></div>' +
    '<section class="notebook-embed">x</section>';
  const body = extractBody(html);
  assert.deepEqual(headingsOf(body), ["First", "Last"]);
  assert.ok(body.includes("final section text"), "text after nested divs survives");
});

test("extractBody falls back to the back-link anchor without a notebook", () => {
  const html =
    '<div class="post-body"><h2>Only</h2><p>text here</p></div>' +
    '<p class="post-back"><a href="/blog/">back</a></p>';
  assert.ok(extractBody(html).includes("text here"));
});

/* ---------- every real post keeps all its sections ---------- */

test("published posts retain their last section after extraction", () => {
  assert.ok(posts.length >= 1, "at least one published blog post exists");
  for (const { f, html } of posts) {
    const allH2 = [...html.matchAll(/<h2[^>]*>(.*?)<\/h2>/gs)]
      .map((m) => m[1].replace(/<[^>]+>/g, "").trim())
      .filter((h) => h && !h.toLowerCase().includes("interactive companion"));
    const lastContentHeading = allH2[allH2.length - 1];
    const bodyHeadings = headingsOf(extractBody(html));
    assert.ok(
      bodyHeadings.includes(lastContentHeading),
      `${f}: last section "${lastContentHeading}" was dropped (extraction truncation regression)`,
    );
  }
});

/* ---------- assistant index freshness ---------- */

test("every published post is present in the committed assistant index", async () => {
  const { default: INDEX } = await import("../../worker/src/index-data.js");
  const blogUrls = new Set(
    INDEX.chunks.filter((c) => c.type === "blog").map((c) => c.url),
  );
  for (const { f } of posts) {
    const url = `https://rodrigosf.com/blog/${f}`;
    assert.ok(
      blogUrls.has(url),
      `${f} is not in worker/src/index-data.js — run scripts/reindex-deploy.sh after publishing`,
    );
  }
});

test("no blog chunk in the index is empty or truncated", async () => {
  const { default: INDEX } = await import("../../worker/src/index-data.js");
  for (const c of INDEX.chunks.filter((c) => c.type === "blog")) {
    assert.ok(c.text && c.text.length >= 30, `blog chunk "${c.title}" is too short`);
  }
});

/* ---------- CSS cache-version consistency ---------- */

test("all site pages reference one styles.css cache version", () => {
  const versions = new Set();
  const walk = (dir) => {
    for (const e of readdirSync(dir, { withFileTypes: true })) {
      if (e.isDirectory()) {
        if (!e.name.endsWith("-notebook")) walk(join(dir, e.name)); // skip exported marimo assets
      } else if (e.name.endsWith(".html")) {
        const m = readFileSync(join(dir, e.name), "utf8").match(/styles\.css\?v=(\d+)/);
        if (m) versions.add(m[1]);
      }
    }
  };
  walk(join(ROOT, "site"));
  assert.equal(
    versions.size,
    1,
    `styles.css cache versions differ across pages: ${[...versions].join(", ")} (bump them all together)`,
  );
});
