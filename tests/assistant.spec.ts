import { test, expect, Page } from '@playwright/test';

// UI tests for the Portfolio Assistant. The API is mocked with page.route,
// so these run without a deployed Worker.

const API = 'https://mock-assistant.example';

const sse = (events: object[]) =>
    events.map(e => `data: ${JSON.stringify(e)}\n\n`).join('');

async function setup(page: Page, events: object[], status = 200, jsonBody?: object) {
    await page.addInitScript(() => {
        // point the site at the mocked API before main.js reads the meta tag
        addEventListener('DOMContentLoaded', () => {
            document.querySelector('meta[name="assistant-api"]')!
                .setAttribute('content', 'https://mock-assistant.example');
        });
    });
    await page.route(`${API}/api/chat`, async route => {
        if (jsonBody) {
            await route.fulfill({ status, contentType: 'application/json', body: JSON.stringify(jsonBody) });
        } else {
            await route.fulfill({ status, contentType: 'text/event-stream', body: sse(events) });
        }
    });
    await page.goto('/');
}

async function openChat(page: Page) {
    const term = page.locator('#term-input');
    await term.scrollIntoViewIfNeeded();
    await term.fill('ask-rodrigo');
    await term.press('Enter');
    await expect(page.locator('#chat')).toBeVisible();
}

test.describe('Portfolio Assistant UI', () => {

    test('ask-rodrigo command opens the chat with welcome, suggestions, and disclaimer', async ({ page }) => {
        await setup(page, []);
        await openChat(page);

        await expect(page.locator('.chat-welcome')).toContainText('Ask me about my work');
        await expect(page.locator('.chat-suggest button')).toHaveCount(7);
        await expect(page.locator('.chat-disclaimer')).toContainText('AI-generated responses may be incomplete or inaccurate');

        // accessibility contract
        await expect(page.locator('.chat-log')).toHaveAttribute('aria-live', 'polite');
        await expect(page.locator('.chat-log')).toHaveAttribute('role', 'log');
        await expect(page.locator('#chat-input')).toHaveAttribute('maxlength', '800');
    });

    test('unknown terminal command prints an error line', async ({ page }) => {
        await setup(page, []);
        const term = page.locator('#term-input');
        await term.fill('sudo make-me-a-sandwich');
        await term.press('Enter');
        await expect(page.locator('.echo-err')).toContainText('command not found');
        await expect(page.locator('#chat')).toBeHidden();
    });

    test('suggested prompt streams an answer with confidence, sources, and related', async ({ page }) => {
        await setup(page, [
            { type: 'delta', text: '**Notebook Observatory** is a daily census ' },
            { type: 'delta', text: 'of public Jupyter notebooks.' },
            {
                type: 'meta', confidence: 'High',
                sources: [{ title: 'GitHub repo: notebook-observatory', url: 'https://github.com/rodrigosf672/notebook-observatory', type: 'repo' }],
                related: [{ title: 'Project: Conda-Lens', url: 'https://github.com/rodrigosf672/conda-lens', type: 'project' }],
                handoff: false,
            },
            { type: 'done' },
        ]);
        await openChat(page);
        await page.locator('.chat-suggest button').first().click();

        const answer = page.locator('.chat-msg.assistant').last();
        await expect(answer).toContainText('daily census of public Jupyter notebooks');
        await expect(answer.locator('strong')).toContainText('Notebook Observatory'); // markdown bold rendered

        await expect(answer.locator('.msg-footer .conf-High')).toHaveText('High');
        const src = answer.locator('.msg-footer a', { hasText: 'notebook-observatory' });
        await expect(src).toHaveAttribute('href', 'https://github.com/rodrigosf672/notebook-observatory');
        await expect(answer.locator('.msg-footer')).toContainText('Related:');
    });

    test('refusal path shows low confidence and contact handoff (explicit send only)', async ({ page }) => {
        await setup(page, [
            { type: 'delta', text: "I couldn't find enough information in Rodrigo's portfolio to answer that reliably." },
            { type: 'meta', confidence: 'Low', sources: [], related: [{ title: 'Projects', url: 'https://rodrigosf.com/projects.html', type: 'project' }], handoff: true },
            { type: 'done' },
        ]);
        await openChat(page);
        await page.locator('#chat-input').fill('What is the capital of France?');
        await page.locator('.chat-send').click();

        const answer = page.locator('.chat-msg.assistant').last();
        await expect(answer).toContainText("couldn't find enough information");
        await expect(answer.locator('.conf-Low')).toBeVisible();

        const handoff = answer.locator('.chat-handoff');
        await expect(handoff).toContainText("Didn't find what you were looking for?");
        // mailto link = requires the visitor to explicitly send; nothing auto-submits
        await expect(handoff.locator('a')).toHaveAttribute('href', /^mailto:rodrigosf672@gmail\.com/);
    });

    test('HTML in responses is rendered inert, never executed', async ({ page }) => {
        await setup(page, [
            { type: 'delta', text: '<img src=x onerror="window.__pwned=1"> <script>window.__pwned=2</script>' },
            { type: 'meta', confidence: 'Medium', sources: [], related: [], handoff: false },
            { type: 'done' },
        ]);
        await openChat(page);
        await page.locator('#chat-input').fill('injection test');
        await page.locator('.chat-send').click();

        const answer = page.locator('.chat-msg.assistant').last();
        await expect(answer).toContainText('<script>'); // shown as text
        expect(await page.evaluate(() => (window as any).__pwned)).toBeUndefined();
        expect(await answer.locator('img, script').count()).toBe(0);
    });

    test('empty input does not send; API error is surfaced gracefully', async ({ page }) => {
        await setup(page, [], 429, { error: 'Rate limit reached — please try again in a little while.' });
        await openChat(page);

        await page.locator('.chat-send').click(); // empty input -> nothing happens
        await expect(page.locator('.chat-msg.user')).toHaveCount(0);

        await page.locator('#chat-input').fill('a real question');
        await page.locator('.chat-send').click();
        await expect(page.locator('.chat-msg.assistant').last()).toContainText('Rate limit reached');
    });

    test('arrow-up recalls previous question; Escape closes the panel', async ({ page }) => {
        await setup(page, [
            { type: 'delta', text: 'ok' },
            { type: 'meta', confidence: 'High', sources: [], related: [], handoff: false },
            { type: 'done' },
        ]);
        await openChat(page);
        await page.locator('#chat-input').fill('first question');
        await page.locator('#chat-input').press('Enter');
        await expect(page.locator('.chat-msg.assistant').last()).toContainText('ok');

        await page.locator('#chat-input').press('ArrowUp');
        await expect(page.locator('#chat-input')).toHaveValue('first question');

        await page.locator('#chat-input').press('Escape');
        await expect(page.locator('#chat')).toBeHidden();
    });

    test('unconfigured API shows a graceful notice instead of failing', async ({ page }) => {
        await page.goto('/'); // no meta override, no route -> content=""
        await openChat(page);
        await page.locator('#chat-input').fill('hello');
        await page.locator('.chat-send').click();
        await expect(page.locator('.chat-msg.assistant').last()).toContainText("isn't connected yet");
    });

});
