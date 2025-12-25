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

Tests run automatically on GitHub Actions via the workflow defined in `smoke-test-job.yml`.
This workflow executes on deployment updates and ensures the live site (`BASE_URL`) remains healthy.
