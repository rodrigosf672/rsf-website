import { defineConfig, devices } from '@playwright/test';

// Runs tests/references.spec.ts against a locally served copy of site/, so the
// references page can be tested without being deployed. `npm run test:references`.
export default defineConfig({
    testDir: './tests',
    testMatch: 'references.spec.ts',
    fullyParallel: true,
    forbidOnly: !!process.env.CI,
    retries: 0,
    workers: process.env.CI ? 1 : undefined,
    reporter: 'line',
    use: {
        baseURL: 'http://localhost:4321',
        trace: 'on-first-retry',
    },
    webServer: {
        command: 'python3 -m http.server 4321 --directory site',
        url: 'http://localhost:4321/references.html',
        reuseExistingServer: !process.env.CI,
        timeout: 30_000,
    },
    projects: [
        { name: 'chromium', use: { ...devices['Desktop Chrome'], channel: 'chromium' } },
    ],
});
