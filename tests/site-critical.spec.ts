import { test, expect } from '@playwright/test';

test.describe('Site Critical Integrity', () => {

    test('Homepage loads and has critical metadata', async ({ page }) => {
        const response = await page.goto('/');
        expect(response?.status()).toBe(200);

        // Site title/hero validation
        await expect(page.locator('h1, .site-title, .navbar-brand')).not.toHaveCount(0);

        // Social links validation (at least one)
        const socialLinks = page.locator('a[href*="github.com"], a[href*="linkedin.com"], a[href*="scholar.google.com"]');
        await expect(socialLinks.first()).toBeVisible();
    });

    test('Primary navigation is healthy', async ({ page }) => {
        await page.goto('/');

        const navLinks = [
            { name: 'Blog', hrefPattern: /\/blog\/?/ },
            { name: 'Projects', hrefPattern: /\/projects\/?/ },
            { name: 'Talks', hrefPattern: /\/talks/ }
        ];

        for (const link of navLinks) {
            const navItem = page.getByRole('link', { name: link.name }).first();
            await expect(navItem).toBeVisible();

            const href = await navItem.getAttribute('href');
            expect(href).toMatch(link.hrefPattern);

            // Verify it loads
            const response = await page.goto(href!);
            expect(response?.status()).toBe(200);
        }
    });

    test('Blog structure and first post', async ({ page }) => {
        await page.goto('/blog/index.html');

        // Check for at least one blog post link
        // Check for at least one blog post link
        // Identifying post links: usually in a listing container.
        // We'll look for links typically found in Quarto listings (title, more, or just links in main)
        // Robust selector: h3 a (default listing), .quarto-post a, or any link to a blog post in main content
        const postLinks = page.locator('.quarto-listing a, .list a, h3 a, a[href*="/blog/post"]');
        await expect(postLinks.first()).toBeVisible();

        const firstPostHref = await postLinks.first().getAttribute('href');

        // Click/Navigate to first post
        const response = await page.goto(firstPostHref!);
        expect(response?.status()).toBe(200);

        // Post structural check
        await expect(page.locator('h1')).toHaveCount(1);
        await expect(page.locator('main')).toBeVisible();

        // No broken internal links on this page (simple check)
        // We'll just check that we don't have empty hrefs for main content links
        const contentLinks = page.locator('main a');
        const count = await contentLinks.count();
        for (let i = 0; i < Math.min(count, 10); i++) { // Check first 10 links to be fast
            const href = await contentLinks.nth(i).getAttribute('href');
            expect(href).toBeTruthy();
        }
    });

    test('Projects page structure', async ({ page }) => {
        await page.goto('/projects/index.html');

        // Ensure at least one project card exists
        const projectCards = page.locator('.card, .project, .quarto-listing-item'); // Generic selectors for Quarto listings
        // Fallback if standard classes aren't used: look for rows/items
        const listingRows = page.locator('tr[data-index], .quarto-grid-item');

        const anyProjectItem = projectCards.or(listingRows).first();
        await expect(anyProjectItem).toBeVisible();

        // Check for content within the item (Title, Description)
        // This is a bit loose to accommodate structure changes, but ensures content exists.
        await expect(anyProjectItem).toContainText(/\w+/);

        // Check for external link (GitHub or similar) if visible in the card
        // This might be brittle if not all projects have external links visible immediately,
        // so we'll just check that *some* project link exists on the page.
        const projectLinks = page.locator('a[href^="http"]');
        await expect(projectLinks.first()).toBeVisible();
    });

    test('Talks page structure', async ({ page }) => {
        await page.goto('/talks.html');

        // Look for typical talk entries (Event name, Year)
        // Assuming structure based on markdown '## Year' or '**Event**'
        const talkEntry = page.locator('strong, h3, h4').filter({ hasText: /\w+/ }).first();
        await expect(talkEntry).toBeVisible();

        // Ensure page isn't empty
        await expect(page.locator('main')).not.toBeEmpty();
    });

    test('No Console Errors', async ({ page }) => {
        const errors: string[] = [];
        page.on('console', msg => {
            if (msg.type() === 'error') {
                errors.push(msg.text());
            }
        });

        await page.goto('/');
        await page.waitForTimeout(1000); // Wait a bit for async errors
        expect(errors).toEqual([]);
    });

});
