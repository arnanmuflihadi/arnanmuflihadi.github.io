# R0-B1.5 — Final layout validation

The owner provisionally accepted the overall hub. This pass refines that blockout;
it does not regenerate terrain, construct permanent architecture or replace the
R0-B1 source models. **Final owner approval remains pending. Stop before R0-B2.**

[Four decisive views and matched comparisons](town-layout-final/index.html) ·
[Playable preview](../town-layout-r0b15.html?build=R0-B1.5-final-validation-5#arrival) ·
[Measurements](town-layout-final/measurements.json) ·
[Native traversal samples](town-layout-final/navigation-browser.json).

## Focused changes

- Arrival retains its route but gains 6 m nominal primary paving. The optional
  2.4 m gravel loop has a quieter material and narrower entrance.
- M1 and M5 form the west commercial frontage, with faces at x=32 and x=31.5 m.
  M2 and M3 align exactly at x=42 m on the east side. Continuous frontage paving
  and flush, supported thresholds connect their doors. M4 faces the square.
- Atlas Guild moves to the north edge and faces south into the public plaza.
  Its existing planning crown and teal mass distinguish the civic landmark.
  A 4 m approach rises 1.8 m to the entrance. Source architectural GLBs are untouched.
- The 20 × 18 m chamfered square retains **352 m² gross paving**, approximately
  **299 m² level capsule-clear floor**, and a clear **10 × 7 m centre**.
- Landing joins, a plot-corner conflict and gravel/paving overlap were corrected.
  Camera-ray inspection found the Guild canopy lacked a collision proxy; six
  camera-only canopy proxies now match the rendered geometry. Player/camera code
  and jump mechanics were not changed.

## Measurements

| Route | Centreline length | Minimum clear width | Elevations | Maximum local / 3 m grade |
|---|---:|---:|---:|---:|
| Skyport → market | 38.0 m | 5.5 m | 17.15–21.5 m | 31.3% / 26.0% |
| Market → square | 15.6 m | 6.0 m | 21.5–22.3 m | 12.9% / 12.9% |
| Square → Guild | 16.0 m | 4.0 m | 22.3–24.1 m | 28.1% / 28.1% |
| Optional meadow branch | 60.0 m to arrival junction | 2.3 m | 17.35–22.3 m | 18.9% / 18.9% |
| Retained highland trail | 95.2 m beyond connector | 2.6 m | 21.0–48.7 m | 82.5% / 55.2% |

Routes use rendered support at 0.25 m stations; width cross sections use 0.05 m
steps and the character's 0.42 m step limit. Capsule-centre clearance is 0.68 m
narrower. The local highland maximum uses finer sampling than earlier reports;
the terrain itself is unchanged. These are game-navigation measurements, not an
accessibility claim. All urban route centres have zero paving gaps or solid
intersections; their largest rise per 0.25 m is below 8 cm.

All six plots were sampled at 0.5 m, including boundaries. They have no void samples;
floors clear the highest ground sample by at least 0.23 m. Foundation masses reach
0.15 m below each plot's lowest sample. Entrances face public paths and have clear
supported approaches, 2.4 × 2.9 m markers and 3.11 m canopy clearance. Guild-crown
terrain/massing sightlines are clear from arrival, market and square.

## Fresh gameplay and technical checks

- One continuous **215.0 m** native-keyboard traversal reached market, square,
  Guild, returned to the square and climbed to the highland: **no checkpoint reset,
  zero blocked time, zero grounded support error; one jump and landing**.
- The scenic return completed **190.3 m**, the optional meadow return **70.2 m**,
  and a separate Guild walk **15.1 m**, all with zero blocked/support error.
- W/Shift+W drove the actual animated character. Bearing assistance steered heading
  only. The main run mixed walking and running; meadow/Guild checks used walking.
  Unassisted Q turning, D strafing and W movement also passed. Moving times exclude
  inspection pauses. Exact centreline corners differ from the controller's 0.55 m
  waypoint acceptance, explaining modest distance differences.
- Recorded-camera ray checks improved from **12 intersections / 3,340 samples**
  before the canopy fix to **0 / 6,149** after it. The actual follow-camera regression
  also passes. [Camera audit](town-layout-final/camera-audit.json).
- **106 tests passed**, no failures or skips: all existing tests plus four focused
  regressions for route hierarchy, plots/entrances, usable square and canopy camera
  clearance. [Output](town-layout-final/tests.txt).
- **58 inherited static-audit findings**, identical to the recorded R0-A3 baseline;
  that unrelated audit remains failing. [Output](town-layout-final/static-audit.txt).
- Eight recorded production digests and both licensed archive hashes still match.
  Fresh browser checks confirm Home/adventure opens MBR, Work/editorial retains
  all six studies, and production has zero architecture instances.
  [Preservation](town-layout-final/preservation.json) ·
  [Portfolio check](town-layout-final/portfolio-preservation.json).

Four final 1280 × 720 images use matched fixed cameras, unchanged daylight/exposure
and 1.65 m pedestrian eyes at 60° FOV. A fresh side/underside view and actual Guild
traversal supplement them. Browser warnings/errors and missing textures are zero.
No mockup or generated concept image is used as implementation evidence.

## Performance and remaining issues

The final town sample contains **600 moving frames, 180.0 fps, 6.3 ms p95,
100 draw calls and 1,176,972 triangles**, standard quality, shadows enabled,
1280 × 658 drawing buffer / effective DPR 1. Mean CPU render submission is recorded
separately from GPU time. These are session/view-specific results, not a device
benchmark. The planning layer contains **32 draw meshes, 13,877 potential triangles,
17 materials and zero textures**. No extra GLB bytes; existing landscape/character
assets and caches remain in use. [Performance](town-layout-final/performance-walking-town.json)
· [Loaded resource inventory](town-layout-final/inventory-browser.json).

Raised backs still need up to **7.4 m** of foundation treatment in approved future
architecture. Blank facades, interiors and final retaining-wall design remain
outside this blockout. The existing steep highland route is playable but remains
an intentional terrain constraint. Final architectural models may alter sightlines
and must be checked again. No human score or automatic approval is assigned.

Changed scene files: `assets/js/town-layout/{plan,blockout,showcase,survey}.js`,
`town-layout-r0b15.html`. Supporting changes: `tests/town-layout.test.mjs`,
`scripts/record-town-layout.mjs` and its final-evidence helper, this report,
`ASSET_MANIFEST.md`, and the new `docs/town-layout-final/` evidence directory.
Previous review screenshots and records remain preserved. The existing two skills
were used without reinstalling or editing them.
