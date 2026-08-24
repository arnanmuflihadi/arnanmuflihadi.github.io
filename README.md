# Arnan Muflihadi — Geospatial Portfolio

This is a static multi-page portfolio (HTML, CSS, and JavaScript only). It has no build step, backend, or framework requirement, and is intended to remain compatible with GitHub Pages.

The shared visual system uses **Roboto Flex** and **Roboto Mono**, an editorial geospatial palette, and progressive enhancement for navigation and motion. All links and assets are relative so the site can be served from a repository root or a GitHub Pages project path.

## Routes

| Route | Purpose |
| --- | --- |
| `index.html` | Homepage: editorial geospatial introduction and selected work. |
| `portfolio.html` | Complete selected-work index. |
| `about.html` | Profile, CV download, experience, education, and publications. |
| `contact.html` | Direct email, LinkedIn, Tableau, and CV links. |
| `project-transit.html` | DKI Jakarta transit accessibility case study. |
| `project-pangan.html` | West Java rice-supply-network case study. |
| `project-alphaearth-food.html` | Historical paddy-screening case study. |
| `project-mbr.html` | Satellite proxy for low-income communities case study. |
| `project-cbd.html` | Indonesia business-center clustering case study. |
| `404.html` | Recovery page for unknown routes. |

## Local preview

Run a plain static server from this folder:

```bash
cd "/Users/arnanmuflihadi/Documents/Portofolio GIS/website"
python3 -m http.server 4173 --bind 127.0.0.1
```

Open [http://127.0.0.1:4173/index.html](http://127.0.0.1:4173/index.html). Use the server rather than `file://` URLs so relative map embeds and browser-module-like fetches behave consistently.

For a Pages-equivalent staging directory, use the repository server rather than adding a dependency:

```bash
node scripts/serve-pages-preview.mjs --root /absolute/path/to/_site --port 4173
```

The preview builds deterministic gzip level-9 copies of eligible text files into an OS-temporary cache before it listens, streams all responses, keeps media/PDFs and `dki-3d/` identity-encoded, and removes that cache on clean shutdown. It serves `404.html` with an HTTP 404 status for unknown paths, matching the recovery behavior expected from a Pages artifact.

## Shared shell and motion ownership

- `assets/js/theme-init.js` applies the stored colour preference before first paint.
- `assets/js/main.js` owns the baseline theme control, year, legacy progressive enhancements, and case-study utilities that are still loaded by the relevant pages.
- `assets/js/site-shell.js` owns the shared editorial header: the mobile menu, Escape handling, and page-curtain navigation policy.
- `assets/js/transition-init.js` enables the page curtain only when JavaScript is available.
- `assets/js/motion.js` is the shared GSAP/ScrollTrigger/Lenis orchestration layer. It activates only where supported hooks exist (principally the homepage) and is deliberately not a second animation engine for case studies.
- `assets/css/motion.css` contains the shared motion presentation and reduced-motion fallbacks. Keep substantive content visible when `prefers-reduced-motion: reduce` is active.
- Vendor files live in `assets/js/vendor/`: `gsap.min.js`, `ScrollTrigger.min.js`, and `lenis.min.js`. Keep their loading order before `motion.js` on pages that use the shared motion layer.

All ten top-level routes use the canonical `site-header`, `page-curtain`, and `site-footer` markup. When editing a route, retain the `data-site-*`, `data-nav-*`, and `data-theme-toggle` hooks so the shared shell remains accessible.

The precise local-library versions, licences, sources, and checksums are recorded in [assets/js/vendor/THIRD_PARTY.md](assets/js/vendor/THIRD_PARTY.md). Do not replace or update a vendored file without updating that provenance record and re-running the static audit.

## Asset and cache discipline

- The approved homepage environment master is `assets/img/redesign/hero-environment.png`; its WebP sibling is a delivery derivative, not a replacement for the master. Keep the PNG fallback in the `<picture>` element.
- The analyst walk frames and live SVG route are separate, original assets. Do not substitute reference-site artwork or regenerate them during a CSS/JS-only pass.
- Project listing images use committed responsive derivatives where available. Derivatives must preserve the source image's analytical meaning, dimensions/aspect intent, and alt/caption relationship; they are not a licence to alter data graphics.
- When changing a shared CSS or JavaScript asset, bump its query version consistently in every top-level route. Then test a fresh local URL or a new local server origin so an old cached response cannot masquerade as current work.

## Local validation

The repository has no package install step. Run the static route and asset checks from the site root after any shared-shell, route, asset, or map change:

```bash
node scripts/audit-static-site.mjs
node --check assets/js/main.js
node --check assets/js/site-shell.js
node --check assets/js/transition-init.js
node --check assets/js/motion.js
git diff --check
```

The audit is a release gate, not a visual substitute: also inspect desktop, tablet, mobile, reduced-motion, keyboard, explicit-map, and case-story states in a browser before publishing.

## Explicit map embeds

Interactive maps are committed static documents, embedded by case-study pages with local `iframe` URLs. They are not fetched from a runtime map service.

| Case study | Local embed(s) |
| --- | --- |
| Transit | `maps/transit_dashboard.html` and `dki-3d/` |
| Food systems | `maps/pangan_dashboard.html` |
| Business centers | `maps/jakarta_map.html` and `maps/indonesia_map.html` |

`assets/js/embed-loader.js` owns the explicit opt-in map controls. Keep iframe titles descriptive, a static preview, and a direct “Open full map” action for every heavy embed; never restore an automatic iframe `src` on page entry.

## Repository layout

```text
website/
├── index.html
├── portfolio.html
├── about.html
├── contact.html
├── 404.html
├── project-*.html
├── maps/                       # committed interactive map documents and data
├── dki-3d/                     # committed static transit simulation
├── assets/
│   ├── css/                    # base, editorial, and motion styles
│   ├── js/                     # shared shell, motion, and case-study scripts
│   ├── data/                   # committed data used by case studies
│   ├── img/                    # portfolio imagery and map assets
│   └── cv.pdf                  # downloadable CV
└── .nojekyll                   # preserves static assets on GitHub Pages
```

## GitHub Pages

Publish this directory as the repository root (or configure it as the Pages source). Because this is a static MPA, no dependency installation or build command is needed before publishing.

When adding a route or changing shared assets, prefer relative URLs, preserve the `404.html` recovery page, and ensure the target path works through a local static server before publishing.
