# rsf-website

Source for [rodrigosf.com](https://rodrigosf.com/) — the personal website of Rodrigo Silva Ferreira.

Handcrafted static HTML and CSS — no framework, no build step. Dark-first, terminal-inspired design with a light theme toggle.

## Structure

```
site/                 # everything that gets deployed to GitHub Pages
  index.html          # home: about, experience, education, photo gallery, assistant
  talks.html          # conference talks + recordings playlist
  publications.html   # research publications + external blog posts
  projects.html       # open-source projects (featured + more)
  references.html     # recommendations, with a topic-modeled "skills" word cloud
  blog/               # blog index + posts, each with an interactive marimo notebook (WASM)
  rss.xml             # RSS 2.0 feed (generated); rss.xsl renders it as a friendly page
  404.html
  styles.css          # design system (CSS custom properties, dark/light themes)
  main.js             # theme toggle, gallery, ask-rodrigo / ask-blog assistant client
worker/               # Cloudflare Worker: ask-rodrigo (site) + ask-blog (blog) RAG assistant
scripts/
  build-index.mjs     # RAG indexing pipeline for the assistant (npm run build:index)
  build-rss.mjs       # RSS feed generator (npm run build:rss)
  reindex-deploy.sh   # re-embed content and redeploy the assistant Worker
  lib/parse-blog.mjs  # shared blog-post HTML parsing
  test/               # node integrity tests (blog index, RSS, references)
content/              # curated FAQ content indexed by the assistant
drafts/               # unpublished post sources (marimo notebooks + rendered HTML)
tests/                # Playwright tests (site, assistant, references)
```

The AI assistant is documented in [worker/README.md](./worker/README.md). One Worker serves two scopes: **ask-rodrigo** (portfolio Q&A on the home page) and **ask-blog** (grounded only in published posts, on the blog page).

## Blog, feeds & references

- **Blog** — posts live in `site/blog/`, each paired with an interactive [marimo](https://marimo.io) notebook exported to WebAssembly (runs entirely in the browser, no server). After publishing a post, regenerate the feed and reindex the blog assistant:

  ```sh
  npm run build:rss                 # regenerate site/rss.xml from the published posts
  bash scripts/reindex-deploy.sh    # re-embed content for the ask-blog assistant
  ```

- **RSS** — `site/rss.xml` is a generated RSS 2.0 feed, auto-discoverable via `<link rel="alternate">` on every page, and rendered as a friendly HTML page (via `rss.xsl`) when opened in a browser.

- **References** — `site/references.html` presents recommendations plus a word cloud of skills surfaced by **NMF topic modeling** over the review sentences (see the page's "how this was built"), where every skill traces back to its source quotes and each quote links into the testimonial it came from.

## Develop locally

Any static file server works:

```sh
python3 -m http.server 4321 --directory site
```

## Test

```sh
npm install

npm run test:worker        # assistant API unit tests (node)
npm run test:scripts       # integrity tests: blog index, RSS feed, references page (node)
npm run test:references    # references page interactive tests (Playwright, local server)
BASE_URL=http://localhost:4321 npx playwright test   # site + assistant UI tests
```

On every push and pull request the node tests (`test:worker`, `test:scripts`) gate the build; after deployment, Playwright smoke tests (site-critical + references) run against the site. See [tests.md](./tests.md) for details.

## Deploy

Pushing to `main` deploys `site/` to GitHub Pages via `.github/workflows/pages.yml`, then runs the Playwright smoke tests against the deployed site.

## Licensing

- **Website code** (HTML, CSS, JavaScript, configuration): **MIT License** — see [`LICENSE`](./LICENSE).
- **Content** (text, images, and other authored materials): **[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)** unless otherwise noted.

If you reuse or adapt content from this site, please attribute it as:

> © Rodrigo Silva Ferreira (2026), licensed under CC BY-SA 4.0.

## Contact

For questions, reuse beyond the scope of the licenses, or collaboration inquiries, please feel free to reach out.
