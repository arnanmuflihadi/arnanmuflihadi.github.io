#!/usr/bin/env node
// Export the fallback from the SAME authored model, not separate artwork.
// Uses an existing Playwright/Chrome installation; installs nothing.
import { writeFile } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const modulePath = process.env.PORTFOLIO_PLAYWRIGHT_PATH;
const { chromium } = await import(modulePath ? pathToFileURL(modulePath) : 'playwright');
const browser = await chromium.launch({ channel: 'chrome', headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 320, height: 400 }, deviceScaleFactor: 1 });
  await page.setContent('<style>body{margin:0}.hero-walker{width:320px;height:400px}canvas{width:100%;height:100%;display:block}</style><span class="hero-walker" data-hero-walker></span>');
  await page.addScriptTag({ path: resolve(root, 'assets/js/vendor/three-hero.min.js') });
  await page.addScriptTag({ path: resolve(root, 'assets/js/vendor/gsap.min.js') });
  await page.addScriptTag({ path: resolve(root, 'assets/js/analyst-3d.js') });
  const png = await page.evaluate(() => {
    const host = document.querySelector('[data-hero-walker]');
    host.style.display = 'block';
    const character = window.createAnalyst3D(host, { gsap: window.gsap });
    if (host.dataset.renderer !== 'webgl') throw new Error('Model could not render');
    character.static();
    const data = character.snapshot();
    character.destroy();
    return data;
  });
  const output = resolve(root, 'assets/img/redesign/analyst-3d-poster.png');
  await writeFile(output, Buffer.from(png.split(',')[1], 'base64'));
  console.log(`Exported source-matched static pose: ${output}`);
} finally {
  await browser.close();
}
