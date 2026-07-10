# rsf-website

Source for [rodrigosf.com](https://rodrigosf.com/) — the personal website of Rodrigo Silva Ferreira.

Handcrafted static HTML and CSS — no framework, no build step. Dark-first, terminal-inspired design with a light theme toggle.

## Structure

```
site/               # everything that gets deployed to GitHub Pages
  index.html        # home: about, experience, education, photo gallery, assistant
  talks.html        # conference talks + recordings playlist
  publications.html # research publications (Google Scholar)
  projects.html     # open-source projects (featured + more)
  404.html
  styles.css        # design system (CSS custom properties, dark/light themes)
  main.js           # theme toggle, gallery, portfolio assistant client
worker/             # "ask-rodrigo" Portfolio Assistant API (Cloudflare Worker + Workers AI)
scripts/            # build-index.mjs — RAG indexing pipeline (npm run build:index)
content/            # curated FAQ content indexed by the assistant
tests/              # Playwright tests (site + assistant UI with mocked API)
```

The AI Portfolio Assistant is documented in [worker/README.md](./worker/README.md).

## Develop locally

Any static file server works:

```sh
python3 -m http.server 4321 --directory site
```

## Test

```sh
npm install
BASE_URL=http://localhost:4321 npx playwright test   # site + assistant UI tests
npm run test:worker                                  # assistant API unit tests
```

See [tests.md](./tests.md) for details.

## Deploy

Pushing to `main` deploys `site/` to GitHub Pages via `.github/workflows/pages.yml`, then runs the Playwright smoke tests against the deployed site.

## Licensing

- **Website code** (HTML, CSS, JavaScript, configuration): **MIT License** — see [`LICENSE`](./LICENSE).
- **Content** (text, images, and other authored materials): **[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)** unless otherwise noted.

If you reuse or adapt content from this site, please attribute it as:

> © Rodrigo Silva Ferreira (2026), licensed under CC BY-SA 4.0.

## Contact

For questions, reuse beyond the scope of the licenses, or collaboration inquiries, please feel free to reach out.
