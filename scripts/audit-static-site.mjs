#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(fileURLToPath(new URL("..", import.meta.url)));
const pages = [
  "index.html",
  "portfolio.html",
  "about.html",
  "contact.html",
  "404.html",
  "project-transit.html",
  "project-pangan.html",
  "project-alphaearth-food.html",
  "project-mbr.html",
  "project-cbd.html"
];
const projectPages = new Set(pages.filter((page) => page.startsWith("project-")));
const canonicalFooterHrefs = [
  "mailto:arnanmuflihadi@gmail.com",
  "https://linkedin.com/in/arnan-m-999ab5165",
  "https://public.tableau.com/app/profile/arnan.muflihadi",
  "assets/cv.pdf",
  "#top"
];
const failures = [];

function count(source, expression) {
  return (source.match(expression) || []).length;
}

function check(page, condition, message) {
  if (!condition) failures.push(`${page}: ${message}`);
}

function localHrefExists(page, href) {
  if (!href || /^(?:[a-z][a-z0-9+.-]*:|\/\/|#)/i.test(href)) return true;
  const pathname = href.split(/[?#]/, 1)[0];
  if (!pathname) return true;
  const resolved = path.resolve(root, path.dirname(page), pathname);
  if (!resolved.startsWith(root + path.sep) && resolved !== root) return false;
  if (fs.existsSync(resolved)) return true;
  return pathname.endsWith("/") && fs.existsSync(path.join(resolved, "index.html"));
}

for (const page of pages) {
  const source = fs.readFileSync(path.join(root, page), "utf8");
  const mainStart = source.search(/<main\b/gi);
  const mainEnd = mainStart >= 0 ? source.indexOf("</main>", mainStart) : -1;
  const h1Start = source.search(/<h1\b/gi);
  check(page, count(source, /<main\b/gi) === 1, "must contain exactly one <main> landmark");
  check(page, count(source, /<h1\b/gi) === 1, "must contain exactly one <h1>");
  check(page, mainStart >= 0 && h1Start > mainStart && h1Start < mainEnd, "must place its visible H1 inside <main>");
  check(page, /<body\b[^>]*\bid=["']top["']/.test(source), "must expose the #top return target");
  check(page, /<header\b[^>]*data-site-header/.test(source), "is missing the shared site header");
  check(page, /class="site-footer"/.test(source), "is missing the shared footer");
  check(page, /<link\b[^>]*\brel=["'][^"']*\bicon\b/.test(source), "is missing a favicon declaration");
  check(page, /class="site-footer__links"/.test(source), "is missing the canonical footer link group");
  for (const href of canonicalFooterHrefs) {
    check(page, source.includes(`href="${href}"`), `is missing canonical footer destination: ${href}`);
  }
  const transitionBeforeHeader = page === 'index.html'
    ? /<script defer src="assets\/js\/transition-init\.js\?v=\d+"><\/script>\s*<header\b/.test(source)
    : /<script src="assets\/js\/transition-init\.js\?v=\d+"><\/script>\s*<header\b/.test(source);
  check(page, transitionBeforeHeader, page === 'index.html'
    ? "must load its deferred transition-init immediately before the shared header"
    : "must load transition-init immediately before the shared header");
  check(page, !/YOUR_FORM_ID|formspree\.io|data-contact-form|data-contact-status/i.test(source), "contains retired contact-form markup");
  check(page, !/user-scalable\s*=\s*["']?no|maximum-scale\s*=\s*1/i.test(source), "contains an accessibility-hostile viewport restriction");

  for (const match of source.matchAll(/<a\b[^>]*\bhref\s*=\s*(["'])(.*?)\1/gi)) {
    const href = match[2];
    check(page, localHrefExists(page, href), `links to a missing local target: ${href}`);
  }

  if (projectPages.has(page)) {
    check(page, !/<iframe\b[^>]*\ssrc\s*=/i.test(source), "contains an eagerly loaded iframe; use data-src and the explicit loader");
  }
}

for (const page of ["project-transit.html", "project-pangan.html", "project-mbr.html", "project-cbd.html"]) {
  const source = fs.readFileSync(path.join(root, page), "utf8");
  check(page, /data-literature-map=["'][^"']+["'][^>]*\brole=["']region["']/.test(source), "must expose its literature map as a named region");
}

for (const mapPage of ["maps/transit_dashboard.html", "maps/pangan_dashboard.html", "maps/jakarta_map.html", "maps/indonesia_map.html"]) {
  const source = fs.readFileSync(path.join(root, mapPage), "utf8");
  check(mapPage, !/user-scalable\s*=\s*["']?no|maximum-scale\s*=\s*1/i.test(source), "contains an accessibility-hostile viewport restriction");
}

const readme = fs.readFileSync(path.join(root, "README.md"), "utf8");
check("README.md", !/capabilities\.html/i.test(readme), "mentions retired capabilities.html route");

const home = fs.readFileSync(path.join(root, "index.html"), "utf8");
check("assets/img/redesign", fs.existsSync(path.join(root, "assets", "img", "redesign", "hero-environment.png")), "is missing the approved hero environment master");
for (const width of [640, 828, 960]) {
  check("assets/img/redesign", fs.existsSync(path.join(root, "assets", "img", "redesign", `hero-environment-${width}.webp`)), `is missing the ${width}px approved-environment delivery derivative`);
}
check("index.html", /hero-environment-640\.webp/.test(home) && /hero-environment-828\.webp/.test(home) && /hero-environment-960\.webp/.test(home), "is missing responsive approved-environment delivery sources");
check("index.html", /assets\/img\/redesign\/analyst-walk-01-idle\.webp/.test(home), "is missing the optimized static analyst-frame delivery entry point");
check("assets/img/redesign", fs.existsSync(path.join(root, "assets", "img", "redesign", "analyst-walk-01-idle.webp")), "is missing the static analyst-frame delivery derivative");
for (const frame of ["01", "02", "03", "04", "05", "06"]) {
  check("assets/img/redesign", fs.existsSync(path.join(root, "assets", "img", "redesign", `analyst-walk-${frame}.png`)), `is missing approved analyst PNG master ${frame}`);
  check("assets/img/redesign", fs.existsSync(path.join(root, "assets", "img", "redesign", `analyst-walk-${frame}.webp`)), `is missing lossless analyst WebP delivery derivative ${frame}`);
}
check("index.html", /class="route-overlay"/.test(home), "is missing the live route overlay");
check("index.html", !/geo-walker|hero-geospatial-(?:field|editorial)|hero-transit\.svg/.test(home), "still contains retired hero artwork");
check("index.html", !/URBAN FIELD|MOBILITY SIGNAL/.test(home), "still contains retired hero labels");
check("index.html", /id="selected-work"/.test(home), "is missing the hero CTA anchor target");
check("project-transit.html", /data-transit-scrolly[^>]*data-static-story/.test(fs.readFileSync(path.join(root, "project-transit.html"), "utf8")), "must retain the explicit static/manual transit fallback");
check("project-pangan.html", /data-pangan-scrolly[^>]*data-static-story/.test(fs.readFileSync(path.join(root, "project-pangan.html"), "utf8")), "must retain the explicit static/manual Pangan fallback");

if (failures.length) {
  console.error("Static audit failed:\n- " + failures.join("\n- "));
  process.exitCode = 1;
} else {
  console.log(`Static audit passed: ${pages.length} top-level routes and 4 map documents checked.`);
}
