import { test, expect } from '@playwright/test';

// Interactive behaviour of the references page. Runs against a locally served
// copy of site/ (see playwright.references.config.ts), so it does not depend on
// the page being deployed.

test.describe('References page', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('/references.html');
    });

    test('loads with heading, word cloud, and testimonials', async ({ page }) => {
        await expect(page.locator('h1')).toContainText('References');
        await expect(page.locator('.nav-links a[aria-current="page"]')).toContainText('references');
        expect(await page.locator('.skill').count()).toBe(9);
        expect(await page.locator('.ref').count()).toBe(6);
    });

    test('theme chips are visually uniform — same size and colour', async ({ page }) => {
        const sizes = await page.$$eval('.skill', els => [...new Set(els.map(e => getComputedStyle(e).fontSize))]);
        const colors = await page.$$eval('.skill', els => [...new Set(els.map(e => getComputedStyle(e).color))]);
        expect(sizes).toHaveLength(1);
        expect(colors).toHaveLength(1);
    });

    test('hovering a theme reveals its keywords and quotes; leaving hides them', async ({ page }) => {
        const chip = page.locator('.skill', { hasText: 'User advocacy' });
        await chip.hover();
        const pop = chip.locator('.skill-pop');
        await expect(pop).toBeVisible();
        await expect(pop.locator('.sp-kw')).toContainText('model keywords');
        expect(await pop.locator('.sp-jump').count()).toBeGreaterThanOrEqual(1);
        await page.mouse.move(3, 3);
        await expect(pop).toBeHidden();
    });

    test('hovering empty space beside a chip does NOT open a popover', async ({ page }) => {
        const chip = page.locator('.skill', { hasText: 'Python data science' });
        const b = await chip.boundingBox();
        await page.mouse.move(b!.x + b!.width + 140, b!.y + b!.height + 4);
        await page.waitForTimeout(200);
        await expect(chip.locator('.sp-jump').first()).toBeHidden();
    });

    test('clicking a quote highlights it in the testimonial and closes the popover', async ({ page }) => {
        const chip = page.locator('.skill', { hasText: 'Finding critical issues' });
        await chip.hover();
        const jump = chip.locator('.sp-jump').first();
        const href = (await jump.getAttribute('href'))!;
        await jump.click();

        const target = page.locator(href);
        await expect(target).toHaveClass(/\bon\b/);
        await expect(chip.locator('.skill-pop')).toBeHidden();

        // clicking anywhere else clears the highlight
        await page.mouse.click(4, 320);
        await expect(target).not.toHaveClass(/\bon\b/);
    });

    test('author / LinkedIn links open in a new tab', async ({ page }) => {
        const targets = await page.$$eval('.sp-by a, .ref-name a', els => els.map(e => e.getAttribute('target')));
        expect(targets.length).toBeGreaterThanOrEqual(6);
        expect(targets.every(t => t === '_blank')).toBe(true);
    });

    test('how-it-was-built shows the pipeline diagram and five numbered steps', async ({ page }) => {
        await page.getByText('how this was built').click();
        await expect(page.locator('.method-diagram svg')).toBeVisible();
        expect(await page.locator('.method-steps li').count()).toBe(5);
    });

    test('no console errors on load', async ({ page }) => {
        const errors: string[] = [];
        page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
        await page.goto('/references.html');
        await page.waitForTimeout(400);
        expect(errors).toEqual([]);
    });
});
