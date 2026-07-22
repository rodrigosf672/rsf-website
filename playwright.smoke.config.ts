import { defineConfig, devices } from '@playwright/test';

// Runs tests/site-critical.spec.ts against a locally served copy of site/, so
// CI validates the exact content being deployed. Testing through the live
// domain is unreliable from CI: Cloudflare's bot protection 403s headless
// browsers on GitHub runners. `npm run test:critical`.
export default defineConfig({
    testDir: './tests',
    testMatch: 'site-critical.spec.ts',
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
        url: 'http://localhost:4321/',
        reuseExistingServer: !process.env.CI,
        timeout: 30_000,
    },
    projects: [
        { name: 'chromium', use: { ...devices['Desktop Chrome'], channel: 'chromium' } },
    ],
});
