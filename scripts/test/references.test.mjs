// Static integrity tests for the references page (site/references.html).
// Run: npm run test:scripts   (node --test, no browser)
//
// The page has several moving parts wired together at build time — a word cloud,
// hover popovers, quote-to-testimonial jump links with highlight targets, a
// recolored Mermaid diagram, and new-tab author links. These tests assert the
// wiring is internally consistent so a future regeneration can't silently break it.

import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const html = readFileSync(join(ROOT, "site/references.html"), "utf8");
const all = (re) => [...html.matchAll(re)];

test("ten themes, each with a keyword line and a popover", () => {
  assert.equal(all(/<span class="skill"[^>]*role="button"/g).length, 10);
  assert.equal(all(/class="skill-pop"/g).length, 10);
  assert.equal(all(/class="sp-kw"/g).length, 10, "each theme shows its model keywords");
});

test("word cloud is uniform — no size/rank cues", () => {
  assert.doesNotMatch(html, /class="skill skill-[sabc]"/, "tiered chip classes must be gone");
  assert.doesNotMatch(html, /class="skill"[^>]*style="font-size/, "no per-chip font size");
  assert.doesNotMatch(html, /<span class="count"/, "no count badges (would imply ranking)");
});

test("every quote jump link resolves to a real highlight target", () => {
  // a jump always resolves to exactly one <span id> — but a single quote can be
  // surfaced under more than one theme (e.g. a storytelling quote also filed under
  // communication), so this is many-jumps-to-one-span, not strict 1:1.
  const jumps = all(/<a class="sp-jump" href="#(q\d+)"/g).map((m) => m[1]);
  const idList = all(/<span id="(q\d+)" class="hl"/g).map((m) => m[1]);
  const ids = new Set(idList);
  assert.equal(idList.length, ids.size, "each highlight id must appear exactly once in the testimonials");
  assert.ok(jumps.length >= 20, "expected the full set of clickable quotes");
  for (const j of jumps) assert.ok(ids.has(j), `jump #${j} has no matching highlight span`);
  for (const id of ids) assert.ok(jumps.includes(id), `highlight #${id} is never linked from a theme popover`);
});

test("all author / LinkedIn links open in a new tab", () => {
  // reviewer profile links only (not the owner's own footer link)
  const links = all(/<a href="https:\/\/www\.linkedin\.com\/in\/[^"]+"[^>]*>/g)
    .map((m) => m[0])
    .filter((l) => !l.includes("/in/rsf309"));
  assert.ok(links.length >= 8, "expected the eight reviewers plus their popover mentions");
  for (const l of links) {
    assert.match(l, /target="_blank"/, `missing target=_blank: ${l}`);
    assert.match(l, /rel="[^"]*noopener/, `missing rel=noopener: ${l}`);
  }
});

test("eight testimonials, each tagged with a cross-functional role", () => {
  assert.equal(all(/<article class="ref">/g).length, 8);
  assert.equal(all(/class="ref-pill">/g).length, 8);
  for (const fn of ["Product Marketing", "Engineering Manager", ">Engineering<", "Product<", "Data Science<"]) {
    assert.ok(html.includes(`ref-pill">${fn.replace(/[<>]/g, "")}`) || html.includes(fn),
      `missing function pill: ${fn}`);
  }
});

test("the how-it-was-built diagram is present, recolored to moss, and names the tools", () => {
  assert.match(html, /class="method-diagram"/);
  assert.match(html, /<svg[^>]*aria-label="[^"]+"/, "diagram carries an accessible label");
  assert.doesNotMatch(html, /#9370DB|#ECECFF/i, "no leftover Mermaid purple");
  for (const tool of ["TF-IDF", "NMF", "scikit-learn"]) {
    assert.ok(html.includes(tool), `explanation should name ${tool}`);
  }
});

test("the explanation is a five-step numbered list", () => {
  assert.equal(all(/<li><span class="step-n">\d<\/span>/g).length, 5);
});

test("the interaction script is present", () => {
  assert.match(html, /classList\.add\('on'\)/, "click-to-highlight logic present");
  assert.match(html, /pop-open/, "hover-open logic present");
});
