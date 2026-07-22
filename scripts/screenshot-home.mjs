// Capture a dark-theme, above-the-fold screenshot of the homepage for the README banner.
//
//   node scripts/screenshot-home.mjs            # shoots the live site
//   BASE_URL=http://localhost:4321 node scripts/screenshot-home.mjs
//
// Needs Chromium: npx playwright install chromium
// The monthly workflow (.github/workflows/homepage-screenshot.yml) runs this and
// commits docs/homepage.png back when it changes. The README points at a fixed
// path, so regenerating the file in place is all that's needed.

import { chromium } from "@playwright/test";
import { mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const URL = process.env.BASE_URL || "https://rodrigosf.com";
const OUT = join(ROOT, "docs", "homepage.png");

// channel: "chromium" uses the full Chromium build (what `playwright install
// --no-shell chromium` provides), not the headless shell.
const browser = await chromium.launch({ channel: "chromium" });
const page = await browser.newPage({
  viewport: { width: 1280, height: 800 },
  deviceScaleFactor: 2,
  colorScheme: "dark",
});

// Force the dark theme regardless of any stored preference (the site reads
// localStorage "theme" before first paint), and reduce motion so the blinking
// cursor and transitions can't make one capture differ from the next.
await page.emulateMedia({ colorScheme: "dark", reducedMotion: "reduce" });
await page.addInitScript(() => {
  try {
    localStorage.setItem("theme", "dark");
  } catch (e) {
    /* private mode */
  }
});

await page.goto(URL, { waitUntil: "networkidle" });

await page.evaluate(() =>
  document.documentElement.setAttribute("data-theme", "dark")
);
await page.addStyleTag({
  content: `*,*::before,*::after{animation:none!important;transition:none!important;caret-color:transparent!important;}
            .cursor{opacity:0!important;}`,
});

// Web fonts change text metrics; wait for them so the layout is stable.
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(300);

mkdirSync(dirname(OUT), { recursive: true });
await page.screenshot({ path: OUT }); // viewport (above the fold), not fullPage
await browser.close();
console.log(`Wrote ${OUT}`);
