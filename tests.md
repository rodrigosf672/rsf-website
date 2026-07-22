# Testing Guide

This repository uses [Playwright](https://playwright.dev/) for automated smoke and critical integrity testing.

## Prerequisites

1.  **Install Node.js**: Ensure Node.js (v14+) is installed.
2.  **Install Dependencies**:
    ```bash
    npm install
    npx playwright install --with-deps chromium
    ```

## Running Tests

### Run All Tests (Headless)
To run the full site-critical test suite in headless mode (fast):
```bash
npx playwright test
```

### Run with UI (Interactive)
To visualize the tests running or debug failures using Playwright's UI mode:
```bash
npx playwright test --ui
```

### Run Specific Test File
```bash
npx playwright test tests/site-critical.spec.ts
```

## Test Strategy

The primary test suite is located in `tests/site-critical.spec.ts`. It verifies:

- **Homepage**: Loads correctly, checks for title and social links.
- **Navigation**: Ensures Blog, Projects, and Talks links are present and functional.
- **Blog**: Verifies the blog index loads and post links are valid.
- **Projects & Talks**: Checks presence of key content on these pages.
- **Sanity**: Fails if any Console Errors are detected.

## Continuous Integration

Tests run automatically on GitHub Actions via `.github/workflows/pages.yml`. The
`site-tests` job runs the site-critical suite (`npm run test:critical`) and the
references suite (`npm run test:references`) against a locally served copy of
`site/` before anything deploys, so a broken page can never ship.

After deploy, a `smoke-test` job re-runs the site-critical suite against the
live site; the deployed content is already validated by `site-tests`. To run
the suite against the live site from your own machine:
```bash
npx playwright test tests/site-critical.spec.ts   # BASE_URL defaults to https://rodrigosf.com
```
