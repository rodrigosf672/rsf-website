#!/usr/bin/env node
/**
 * build-index.mjs — reproducible indexing pipeline for the Portfolio Assistant.
 *
 * Scans approved content only:
 *   - site/*.html          (about, experience, education, talks, publications, projects)
 *   - content/faq.md       (curated FAQ)
 *   - GitHub repositories  (public, non-fork: metadata + README)
 *
 * Embeds every chunk with Cloudflare Workers AI (@cf/baai/bge-base-en-v1.5) and
 * writes worker/src/index-data.js, which the Worker imports at deploy time.
 *
 * Usage:
 *   CF_ACCOUNT_ID=... CF_API_TOKEN=... npm run build:index
 *   npm run build:index -- --dry-run     # chunks only, no embeddings (for CI/tests)
 *
 * Optional: GITHUB_TOKEN to raise the GitHub API rate limit.
 */

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const SITE = "https://rodrigosf.com";
const GITHUB_USER = "rodrigosf672";
const EMBED_MODEL = "@cf/baai/bge-base-en-v1.5";
const DRY_RUN = process.argv.includes("--dry-run");

/* ---------------- helpers ---------------- */

const strip = (html) =>
  html
    .replace(/<[^>]+>/g, " ")
    .replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">")
    .replace(/&nbsp;/g, " ").replace(/&times;/g, "×").replace(/&rarr;|&larr;/g, " ")
    .replace(/\s+/g, " ")
    .trim();

const read = (p) => readFileSync(join(ROOT, p), "utf8");
const chunks = [];
const add = (type, title, url, text) => {
  if (!text || text.length < 30) return;
  chunks.push({ id: `${type}-${chunks.length}`, type, title, url, text: text.slice(0, 2400) });
};

/* ---------------- site pages ---------------- */

function indexHome() {
  const html = read("site/index.html");

  const lede = html.match(/<p class="lede">(.*?)<\/p>/s);
  if (lede) add("about", "About Rodrigo — intro", `${SITE}/`, strip(lede[1]));

  const about = html.match(/<div class="prose">(.*?)<\/div>/s);
  if (about) {
    for (const [k, p] of [...about[1].matchAll(/<p>(.*?)<\/p>/gs)].entries())
      add("about", `About Rodrigo (${k + 1})`, `${SITE}/#about-h`, strip(p[1]));
  }

  for (const item of html.matchAll(/<div class="tl-item">(.*?)<\/div>\s*(?=<div class="tl-item">|<\/div>)/gs)) {
    const b = item[1];
    const when = strip((b.match(/<span class="tl-when">(.*?)<\/span>/s) || [, ""])[1]);
    const role = strip((b.match(/<h3>(.*?)<\/h3>/s) || [, ""])[1]);
    const org = strip((b.match(/<p class="tl-org">(.*?)<\/p>/s) || [, ""])[1]);
    const desc = strip((b.match(/<p>(?!<)(?:(?!class=)[\s\S])*?<\/p>\s*$/s) || b.match(/<p(?![^>]*class)[^>]*>(.*?)<\/p>\s*<\/?$/s) || [, ""])[1] || b.split("</p>").pop());
    const body = strip(b.replace(/<span class="tl-when">.*?<\/span>|<h3>.*?<\/h3>|<p class="tl-org">.*?<\/p>/gs, ""));
    add("experience", `Experience: ${role} — ${org}`, `${SITE}/#exp-h`, `${role} at ${org} (${when}). ${body}`);
  }

  for (const card of read("site/index.html").matchAll(/<div class="card">\s*<h3>([^<]*)<\/h3>\s*<p>(.*?)<\/p>/gs)) {
    add("education", `Education: ${strip(card[1])}`, `${SITE}/#edu-h`, `${strip(card[1])}. ${strip(card[2])}`);
  }
}

function indexTalks() {
  const html = read("site/talks.html");
  let year = "";
  for (const m of html.matchAll(/<h2 class="year-heading"[^>]*>(\d{4})<\/h2>|<article class="talk">(.*?)<\/article>/gs)) {
    if (m[1]) { year = m[1]; continue; }
    const b = m[2];
    const when = strip((b.match(/<div class="talk-when">(.*?)<\/div>/s) || [, ""])[1]);
    const title = strip((b.match(/<h3 class="talk-title">(.*?)<\/h3>/s) || [, ""])[1]);
    const meta = strip((b.match(/<p class="talk-meta">(.*?)<\/p>/s) || [, ""])[1]);
    add("talk", `Talk: ${title.replace(/\s*(upcoming|accepted|poster|workshop|mentor|speaker|charla)[^]*$/i, "").trim()}`,
      `${SITE}/talks.html`, `Conference talk (${when}): "${title}" at ${meta}.`);
  }
  add("talk", "Talk recordings playlist", "https://www.youtube.com/playlist?list=PL2laqeiu5UqdUaDCc00i2i7YQxI_KbsBB",
    "Selected recordings of Rodrigo's conference talks are collected in a YouTube playlist, embedded on the talks page of his website.");
}

function indexPublications() {
  const html = read("site/publications.html");
  for (const m of html.matchAll(/<article class="pub">(.*?)<\/article>/gs)) {
    const b = m[1];
    const title = strip((b.match(/<h3><a href="[^"]*">(.*?)<\/a><\/h3>/s) || [, ""])[1]);
    const url = (b.match(/<h3><a href="([^"]*)"/s) || [, `${SITE}/publications.html`])[1];
    const authors = strip((b.match(/<p class="authors">(.*?)<\/p>/s) || [, ""])[1]);
    const venue = strip((b.match(/<p class="venue-line">(.*?)<\/p>/s) || [, ""])[1]);
    add("publication", `Publication: ${title}`, url, `"${title}" by ${authors}. Published in ${venue}.`);
  }
  const stats = html.match(/<dl class="stats"(.*?)<\/dl>/s);
  if (stats) add("publication", "Publication metrics", `${SITE}/publications.html`,
    "Rodrigo has 8 research publications with 307+ citations and an h-index of 3, including three papers in Nature Communications and one in Angewandte Chemie International Edition. Full record on Google Scholar: https://scholar.google.com/citations?user=FoA5dgMAAAAJ");
}

function indexProjects() {
  const html = read("site/projects.html");
  for (const m of html.matchAll(/<article class="card(?: card-featured)?">(.*?)<\/article>/gs)) {
    const b = m[1];
    const title = strip((b.match(/<h3><a href="[^"]*">(.*?)<\/a><\/h3>/s) || [, ""])[1]);
    const url = (b.match(/<h3><a href="([^"]*)"/s) || [, `${SITE}/projects.html`])[1];
    const desc = strip((b.match(/<p>(.*?)<\/p>/s) || [, ""])[1]);
    const tags = [...b.matchAll(/<span class="chip">([^<]*)<\/span>/g)].map((c) => c[1]).join(", ");
    const featured = m[0].includes("card-featured") ? "Featured project. " : "";
    add("project", `Project: ${title}`, url, `${featured}${title}: ${desc} Topics: ${tags}.`);
  }
}

function indexFaq() {
  const md = read("content/faq.md");
  for (const sec of md.split(/^## /m).slice(1)) {
    const [title, ...rest] = sec.split("\n");
    add("faq", title.trim(), `${SITE}/`, rest.join(" ").replace(/\s+/g, " ").trim());
  }
}

/* ---------------- GitHub ---------------- */

async function indexGitHub() {
  const headers = { "User-Agent": "rsf-website-indexer" };
  if (process.env.GITHUB_TOKEN) headers.Authorization = `Bearer ${process.env.GITHUB_TOKEN}`;
  const res = await fetch(`https://api.github.com/users/${GITHUB_USER}/repos?per_page=100&sort=updated`, { headers });
  if (!res.ok) throw new Error(`GitHub API ${res.status}`);
  const repos = (await res.json()).filter((r) => !r.fork && !r.private);
  for (const r of repos) {
    let readme = "";
    try {
      const rr = await fetch(`https://raw.githubusercontent.com/${GITHUB_USER}/${r.name}/${r.default_branch}/README.md`, { headers });
      if (rr.ok) readme = (await rr.text()).replace(/```[\s\S]*?```/g, " ").replace(/[#*_>`\[\]()!]/g, " ").replace(/\s+/g, " ").slice(0, 1800);
    } catch { /* no readme */ }
    add("repo", `GitHub repo: ${r.name}`, r.html_url,
      `${r.name} — ${r.description || "no description"}. Language: ${r.language || "n/a"}. Stars: ${r.stargazers_count}. Topics: ${(r.topics || []).join(", ") || "none"}. ${readme}`);
  }
}

/* ---------------- embeddings ---------------- */

async function embedAll(texts) {
  const { CF_ACCOUNT_ID, CF_API_TOKEN } = process.env;
  if (!CF_ACCOUNT_ID || !CF_API_TOKEN)
    throw new Error("Set CF_ACCOUNT_ID and CF_API_TOKEN, or pass --dry-run.");
  const out = [];
  for (let i = 0; i < texts.length; i += 25) {
    const batch = texts.slice(i, i + 25);
    const res = await fetch(
      `https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/ai/run/${EMBED_MODEL}`,
      { method: "POST", headers: { Authorization: `Bearer ${CF_API_TOKEN}`, "Content-Type": "application/json" }, body: JSON.stringify({ text: batch }) },
    );
    const json = await res.json();
    if (!json.success) throw new Error(`Workers AI embed failed: ${JSON.stringify(json.errors)}`);
    out.push(...json.result.data);
    process.stdout.write(`embedded ${Math.min(i + 25, texts.length)}/${texts.length}\r`);
  }
  return out.map((v) => v.map((x) => Number(x.toFixed(6))));
}

/* ---------------- main ---------------- */

indexHome();
indexTalks();
indexPublications();
indexProjects();
indexFaq();
await indexGitHub();

console.log(`\ncollected ${chunks.length} chunks:`);
for (const t of [...new Set(chunks.map((c) => c.type))])
  console.log(`  ${t}: ${chunks.filter((c) => c.type === t).length}`);

if (!DRY_RUN) {
  const vecs = await embedAll(chunks.map((c) => c.text));
  chunks.forEach((c, k) => (c.vec = vecs[k]));
}

const banner = `// GENERATED by scripts/build-index.mjs — do not edit by hand.
// model: ${EMBED_MODEL} · chunks: ${chunks.length} · built: ${new Date().toISOString()}${DRY_RUN ? " · DRY RUN (no vectors)" : ""}`;
mkdirSync(join(ROOT, "worker/src"), { recursive: true });
writeFileSync(join(ROOT, "worker/src/index-data.js"), `${banner}\nexport default ${JSON.stringify({ model: EMBED_MODEL, chunks })};\n`);
console.log(`wrote worker/src/index-data.js${DRY_RUN ? " (dry run — run again with CF credentials before deploying)" : ""}`);
