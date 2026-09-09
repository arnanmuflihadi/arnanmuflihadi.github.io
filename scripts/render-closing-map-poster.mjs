#!/usr/bin/env node
// Reproducible static fallback from the SAME authored 3D scene. No new artwork.
import { writeFile } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const modulePath = process.env.PORTFOLIO_PLAYWRIGHT_PATH;
const { chromium } = await import(modulePath ? pathToFileURL(modulePath) : 'playwright');
const browser = await chromium.launch({ channel: 'chrome', headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 1200, height: 720 }, deviceScaleFactor: 1 });
  await page.setContent('<style>body{margin:0}.closing-map{width:1200px;height:720px}canvas{width:100%;height:100%;display:block}</style><div class="closing-map"></div>');
  for (const file of ['vendor/three-hero.min.js', 'vendor/gsap.min.js', 'closing-map-3d.js']) {
    await page.addScriptTag({ path: resolve(root, 'assets/js', file) });
  }
  const variants = {
    city: 'closing-map-3d.webp',
    district: 'district-map-3d.webp',
    garden: 'garden-map-3d.webp',
    river: 'river-map-3d.webp',
    atlas: 'atlas-map-3d.webp',
    method: 'method-map-3d.webp',
    fieldnotes: 'fieldnotes-map-3d.webp',
    inquiry: 'inquiry-map-3d.webp'
  };
  for (const [variant, filename] of Object.entries(variants)) {
    // The work atlas is a horizontal transect. Preserve its wide framing in
    // the fallback instead of baking unused portrait whitespace into the asset.
    const height = variant === 'atlas' ? 462 : 720;
    await page.setViewportSize({ width: 1200, height });
    await page.locator('.closing-map').evaluate((host, value) => { host.style.height = `${value}px`; }, height);
    const webp = await page.evaluate((name) => {
      const host = document.querySelector('.closing-map');
      host.dataset.mapVariant = name;
      const map = window.createClosingMap3D(host, { gsap: window.gsap });
      if (host.dataset.renderer !== 'webgl') throw new Error(`Map variant ${name} could not render`);
      map.static();
      const data = map.snapshot();
      map.destroy();
      return data;
    }, variant);
    const output = resolve(root, 'assets/img/redesign', filename);
    await writeFile(output, Buffer.from(webp.split(',')[1], 'base64'));
    console.log(`Exported source-matched ${variant} map: ${output}`);
  }
} finally {
  await browser.close();
}
