# Existing browser evidence workflow

Paths are relative to the repository root. Prefer the current phase's tools and records; the examples below describe the R0-B1 baseline, not permanent phase requirements.

## Preview and capture

- Reuse the running `http://127.0.0.1:4173` preview when healthy. `scripts/serve-pages-preview.mjs` documents a dependency-free alternative: `node scripts/serve-pages-preview.mjs --root <served-root> --port <available-port>`. Inspect it before starting another server; do not replace an existing session unnecessarily.
- Production: `index.html?experience=adventure&project=mbr&build=73`. Architecture review: `architecture-r0b1.html?build=R0-B1.6#ensemble`.
- Fixed cameras: `assets/js/architecture-r0b1/views.js`. Existing evidence: `docs/architecture-r0b1-review/captures.json`, `comparisons.json`, `final-*.jpg`, `technical-evidence.json` and `normal-browser-check.json`.
- Use the configured browser tool and its current instructions. In this workspace, native/browser interactions use CUA. Preserve user tabs; restore temporary viewport overrides. Save actual screenshot bytes and verify their dimensions. If a viewport override does not apply, do not claim mobile coverage; the existing `responsive-check.html` provides a real 390 × 844 iframe layout check, not a mobile GPU benchmark.
- Check the page's visible diagnostics/data attributes and browser logs; do not invoke hidden application functions to fabricate states or measurements.

## Regression and measurements

- Existing suite: `node --test tests/*.test.mjs`; focused files include `tests/architecture-r0b1.test.mjs`, `landscape-detail.test.mjs`, `landscape-r0a.test.mjs` and `atlas-character.test.mjs`.
- Static audit: `node scripts/audit-static-site.mjs`; compare its findings with the recorded baseline instead of declaring inherited failures resolved.
- Recorded R0-B1 runs: `performance-standard-preview.json`, `performance-standard-landscape.json`, `performance-eco-preview.json`, `load-first-observed.json` and `load-warm.json` in the review folder. They use real moving rAF samples, not an idle screenshot's frame rate. Refresh when the task calls for new performance evidence.
- Recheck `ASSET_MANIFEST.md`, `assets/game/architecture-r0b1/prototypes.json`, `components-source.json` and `site-feasibility.json` for current files, source rights, counts, dimensions and collision/support assumptions.
- `scripts/record-r0b1-evidence.mjs` validates cameras, payload and production digests and writes the gallery/JSON/feasibility records. It is **not read-only**: run it only when updating that evidence is authorized. Reuse or minimally adapt it for an authorized phase; do not duplicate it inside this skill.

For the installation dry-run, read the existing ensemble and pedestrian captures. Diagnose whether modern facades front shared urban paving or terminate beside isolated dirt trails. Report observations as planning/streetscape findings, with owner approval still pending; do not alter the approved landscape or start settlement construction.
