import { test, expect } from '@playwright/test';

test.describe('Site Critical Integrity', () => {

    test('Homepage loads with hero, social links, and stats', async ({ page }) => {
        const response = await page.goto('/');
        expect(response?.status()).toBe(200);

        await expect(page.locator('h1')).toContainText('Rodrigo');

        // Social links validation
        for (const host of ['github.com', 'linkedin.com', 'scholar.google.com', 'youtube.com']) {
            await expect(page.locator(`a[href*="${host}"]`).first()).toBeVisible();
        }

        // Stats strip renders
        await expect(page.locator('.stats .stat')).not.toHaveCount(0);
    });

    test('Primary navigation is healthy', async ({ page }) => {
        await page.goto('/');

        const navLinks = [
            { name: 'talks', hrefPattern: /\/talks\.html/ },
            { name: 'publications', hrefPattern: /\/publications\.html/ },
            { name: 'projects', hrefPattern: /\/projects\.html/ }
        ];

        for (const link of navLinks) {
            const navItem = page.locator('.nav-links a', { hasText: link.name }).first();
            await expect(navItem).toBeVisible();

            const href = await navItem.getAttribute('href');
            expect(href).toMatch(link.hrefPattern);

            const response = await page.goto(href!);
            expect(response?.status()).toBe(200);
            await page.goto('/');
        }
    });

    test('Talks page lists talks and embeds recordings playlist', async ({ page }) => {
        await page.goto('/talks.html');

        // Year sections
        for (const year of ['2026', '2025', '2024']) {
            await expect(page.locator('.year-heading', { hasText: year })).toBeVisible();
        }

        // All 19 conference appearances present
        await expect(page.locator('.talk')).toHaveCount(19);

        // YouTube playlist embed
        const iframe = page.locator('iframe[src*="youtube"]');
        await expect(iframe).toHaveCount(1);
        expect(await iframe.getAttribute('src')).toContain('PL2laqeiu5UqdUaDCc00i2i7YQxI_KbsBB');
    });

    test('Publications page lists all publications with links', async ({ page }) => {
        await page.goto('/publications.html');

        // All 8 publications from Google Scholar
        await expect(page.locator('.pub')).toHaveCount(8);

        // Every publication links out (doi, arXiv, or repository)
        const pubLinks = page.locator('.pub .pub-links a');
        expect(await pubLinks.count()).toBeGreaterThanOrEqual(8);

        // Scholar profile link present
        await expect(page.locator('a[href*="scholar.google.com"]').first()).toBeVisible();
    });

    test('Projects page structure', async ({ page }) => {
        await page.goto('/projects.html');

        const projectCards = page.locator('.card');
        await expect(projectCards.first()).toBeVisible();
        expect(await projectCards.count()).toBeGreaterThanOrEqual(6);

        // Each project card links to GitHub
        const projectLinks = page.locator('.card a[href*="github.com"]');
        expect(await projectLinks.count()).toBeGreaterThanOrEqual(6);
    });

    test('Theme toggle switches themes', async ({ page }) => {
        await page.goto('/');

        const toggle = page.locator('.theme-toggle');
        await expect(toggle).toBeVisible();

        const before = await page.evaluate(() => document.documentElement.getAttribute('data-theme'));
        await toggle.click();
        const after = await page.evaluate(() => document.documentElement.getAttribute('data-theme'));
        expect(after).not.toBe(before);
    });

    test('Gallery lightbox opens, navigates, and closes', async ({ page }) => {
        await page.goto('/');

        const firstPhoto = page.locator('.photo-btn').first();
        await firstPhoto.scrollIntoViewIfNeeded();
        await firstPhoto.click();

        const lightbox = page.locator('.lightbox');
        await expect(lightbox).toBeVisible();
        await expect(lightbox.locator('img')).toBeVisible();
        await expect(lightbox.locator('figcaption')).not.toBeEmpty();

        // arrow changes the photo
        const src1 = await lightbox.locator('img').getAttribute('src');
        await lightbox.locator('.lb-next').click();
        expect(await lightbox.locator('img').getAttribute('src')).not.toBe(src1);

        // escape closes
        await page.keyboard.press('Escape');
        await expect(lightbox).toBeHidden();

        // pagination dots exist
        await expect(page.locator('.g-dot')).toHaveCount(7);
    });

    test('No Console Errors', async ({ page }) => {
        const errors: string[] = [];
        page.on('console', msg => {
            // Ignore noise from the third-party YouTube embed
            if (msg.type() === 'error' && !msg.location().url.includes('youtube')) {
                errors.push(msg.text());
            }
        });

        for (const path of ['/', '/talks.html', '/publications.html', '/projects.html']) {
            await page.goto(path);
            await page.waitForTimeout(500);
        }
        expect(errors).toEqual([]);
    });

});
