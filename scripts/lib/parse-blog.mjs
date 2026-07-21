// Pure, dependency-free helpers for parsing published blog-post HTML.
// Extracted from build-index.mjs so the tricky bits are unit-testable
// (see scripts/test/blog-index.test.mjs).

/**
 * Return the inner HTML of a post's <div class="post-body">.
 *
 * The naive /post-body">([\s\S]*?)<\/div>/ is wrong: a non-greedy match stops
 * at the FIRST </div>, so any nested <div> inside a figure or card truncates
 * the body and silently drops every section after it. We anchor the closing
 * </div> on what actually follows the body (the notebook embed, then the
 * back-link), and only fall back to a greedy match if neither is present.
 */
export function extractBody(html) {
  const m =
    html.match(/<div class="post-body">([\s\S]*?)<\/div>\s*<section class="notebook-embed"/) ||
    html.match(/<div class="post-body">([\s\S]*?)<\/div>\s*<p class="post-back"/) ||
    html.match(/<div class="post-body">([\s\S]*)<\/div>/);
  return (m || [, ""])[1] || "";
}

/** Heading texts of the <h2> sections within a post body, in order. */
export function headingsOf(body) {
  return body
    .split(/<h2>/)
    .slice(1)
    .map((sec) => sec.split("</h2>")[0].replace(/<[^>]+>/g, "").trim())
    .filter(Boolean);
}
