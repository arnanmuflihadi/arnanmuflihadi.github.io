# R0-C1B — Telaga Awan integration

**Development integration delivered for owner review. No public deployment. Stop before R0-C2.**

[Local playable review](http://127.0.0.1:4173/index.html?experience=adventure&dev-town=s2f&terrain-study=c1a5&town-square=c1b&town-review=1) · [GLB](../../../validation/town-square-c1b/town-square-optimized.glb) · [Independent Blender derivative](../../../validation/town-square-c1b/town-square-export.blend) · [Sources](ASSET-RECORD.md)

## Approved design and terrain fit

The bronze-leaf fountain, jade basin, timber pavilion, jointed stone/terracotta paving, seating, planters, civic walk, stairs and guards are exported from C1A. The four buildings, S2-G foundations and C1A.5 terrain are unchanged. One existing scene, renderer, cached model library and animated explorer serve the integration.

The 78 m² court remains at **Y21.800** beside the unchanged 99.2 m² forecourt at **Y22.614**. Ground below the court leaves **0.18–1.98 m** of retaining exposure, median 0.48 m. Existing walls cover it; no new terrain sculpting or hidden floor is added. All 64 checked bottom corners of the 16 approach shoes embed 0.037–0.150 m into the accepted terrain. [Survey](../../../validation/town-square-c1b/site-survey.json), [shoe contacts](../../../validation/town-square-c1b/footing-verification.json).

Three correction groups were necessary:

1. **Support and access:** inward stair/deck normals were corrected; diagonal rails received oriented bounds. A live return failed where the preserved market-ramp rail overlapped the civic approach. The derivative's short walk now bows west by at most **0.75 m**, with the same endpoints and floor heights. The tightest measured body-clear passage is **1.93 m**; the deck remains nominally 2.6 m wide. This is a local fit correction, not a new square layout.
2. **Terrain contact:** the old highland ribbon was locally buried by 0.213 m. Its existing surface follows accepted ground, with small earth skirts meeting the slope. Three approved small groundcover clumps are replanted outside the court; intersecting grass indices are filtered only while the square is enabled. Original trees and terrain remain.
3. **Browser material transfer:** square-only bronze fill and the existing S2-G closed-stone shadow technique restore readable leaves and remove self-shadow stripes. No lighting, glass, exposure or quality change is used to improve the comparison.

## Geometry and loading

The original design inventory was 46,534 evaluated triangles, including 32,508 paving triangles. The derivative preserves the 300 joints and top arrises while removing underside bevel rings. Paving becomes **6,108 evaluated triangles**. The actual GLB contains **19,310 triangles, 14 mesh primitives, 12 materials and zero texture references**, at **1,513,244 bytes**. The editable derivative inventory differs from export totals because hidden authoring lettering and degenerate faces are excluded. [Measured export](../../../validation/town-square-c1b/export-metrics.json), [component costs and collision bounds](../../../validation/town-square-c1b/export-manifest.json).

The square uses its actual visible paving, stairs and walk triangles as support. It adds no separate movement system or invisible collision platform. Bounds and orientation were inspected in an [isolated GLB preview](../../../validation/town-square-c1b/asset-preview.html) before game validation. The terrain mesh and accepted sampler still agree to **1.8e-14 m**. Square ray/support comparisons differ by at most **0.000297 m**, within the existing edge-tolerance behavior; no sampler algorithm is changed. [Height checks](../../../validation/town-square-c1b/height-verification.json).

## Real explorer traversal

All six completed live walks use the actual animated explorer and original controller, without route teleporting after the initial start placement. Distances below are horizontal walking distance. The corrected final run has no unplanned air height or support-seam events.

| Route | Out / return distance | Out / return time | Result |
|---|---:|---:|---|
| Market ↔ forecourt | 24.90 / 24.91 m | 11.92 / 11.92 s | PASS |
| Forecourt ↔ court, new stairs/walk | 25.33 / 25.30 m | 12.30 / 12.29 s | PASS |
| Court ↔ highland junction | 38.27 / 38.31 m | 18.28 / 18.28 s | PASS |

Fountain approach and court-edge attempts are physically stopped by their corresponding colliders, without falling. A manual courtyard jump launches and lands on the paving. The tightest live camera distance is **1.56 m** on the civic connection; the existing follow camera retracts near the guard assembly. No camera or movement tuning changes were made. [Live walks](../../../validation/town-square-c1b/live-traversal.json), [jump landing](../../../validation/town-square-c1b/jump-landing.json).

The original failed return is retained in `pre-final-live.json`; it is not counted as a pass. Fixed-step checks now cover all three pairs at **20/60/180 Hz**, 18 runs. Terrain-only walks from C1A.5 are historical support evidence and are not used to claim these raised surfaces work.

## Browser evidence

Five real-game screenshots, all 1280×720, with a 1280×656 drawing buffer at DPR 1. Eye views are 1.65 m above their approved support floors. Standard quality, antialiasing, PCF soft shadows and exposure 0.96 remain unchanged. All measurements use **Glass B**; authored A remains available through the existing comparison controls.

- [Market arrival](../../../validation/town-square-c1b/01-market-arrival.jpg).
- [Court at player eye height](../../../validation/town-square-c1b/02-square-interior.jpg).
- [Elevated town composition](../../../validation/town-square-c1b/03-elevated-town.jpg).
- [Foundations and slope](../../../validation/town-square-c1b/04-square-foundations.jpg).
- [Complete floating island](../../../validation/town-square-c1b/05-full-island.jpg).

Each has a `before-` OFF capture and adjacent JSON containing URL, camera/quaternion/FOV, quality, resources, all-pass counters and errors. All five pairs match cameras and settings. [Pair audit](../../../validation/town-square-c1b/capture-pairs.json). In these views the square adds **28 draws** and **37,948–38,532 submitted triangles**, including the shadow pass and square-specific grass clearance.

Three additional browser presets match the native Blender camera positions, view axes and horizontal field of view. Fresh 1280×656 native renders match the browser's drawable aspect. The approved C1A renders remain unchanged. Blender uses its existing Cycles/AgX daylight; the game retains its existing renderer and sky, so tone/reflections differ. These are geometry/composition comparisons, not pixel-identical lighting claims.

[Arrival comparison](../../../validation/town-square-c1b/comparison-blender-arrival.jpg) · [Interior comparison](../../../validation/town-square-c1b/comparison-blender-interior.jpg) · [Elevated comparison](../../../validation/town-square-c1b/comparison-blender-elevated.jpg)

## Measured performance

Apple M4 Pro / ANGLE Metal, same existing renderer and 12-second market-to-fountain camera rail after 2 seconds warmup. No Blender render, asset export or test suite ran alongside these benchmarks. Both states keep terrain harmonization and Glass B; OFF hides only the square and reverses its vegetation/collision changes.

| Run | Square OFF median / p95 | Square ON median / p95 |
|---|---:|---:|
| First pair | 11.1 / 16.6 ms | 11.1 / 16.6 ms |
| Warm pair | 11.1 / 16.7 ms | 11.1 / 16.8 ms |

OFF submits **312–385 draws / 2,631,080–2,730,982 triangles**; ON submits **340–413 / 2,669,028–2,768,930**, including passes. Warm CPU render-submission median/p95 is 1.3/1.6 ms OFF and 1.5/1.9 ms ON. These are browser rAF intervals and CPU submission, not GPU timings or a claim of zero overhead. [All four runs](../../../validation/town-square-c1b/performance-comparison.json).

The measured square request transfers **1,513,544 bytes including response overhead**, with 1,513,244 encoded/decoded body bytes. The model-library cache remains **seven requests / seven loaded files** across repeated toggles. The warmed renderer reports 260 geometry resources, 22 textures and 41 programs; no square textures are added. Browser JS heap was about 106 MB at the saved sample, not total unified/GPU memory. No missing square textures or final browser errors/warnings were recorded.

## Regressions and preservation

**16/16 scoped tests pass**: existing S2-F/G tests, accepted terrain regressions and new square checks covering original assets, ray/support agreement, restoration, actual controller route records, fountain collision and jumping. The inherited terrain assertions run unchanged through a small output-path wrapper so prior approved JSON evidence is not overwritten. Final commands:

```
node validation/town-square-c1b/test-routes.mjs
node --test tests/town-s2f.test.mjs tests/town-s2g.test.mjs tests/town-square-c1b.test.mjs validation/town-square-c1b/terrain-regression.mjs
```

[Regression log](../../../validation/town-square-c1b/regression.log). **3,347 of 3,350 checkpointed files are unchanged**, including all **233 checked assets/licenses**. Only `entry.js`, `town-integration.js` and `town-review.js` changed among pre-existing files. All new source/export/evidence is separate. [Preservation](../../../validation/town-square-c1b/preservation.json).

A fresh URL containing the square/terrain parameters but no `dev-town=s2f` shows one original renderer, no town-review panel and only the original tree/fern model requests in editorial mode. `project=mbr` opens the real study. Home/Work navigation, default editorial/adventure switching and the six-study index were checked in the browser; their source files and research registry remain unchanged. [Default-off evidence](../../../validation/town-square-c1b/default-off.json), [MBR screenshot](../../../validation/town-square-c1b/default-mbr.jpg), [Work index](../../../validation/town-square-c1b/portfolio-work.json).

## Rollback and remaining review

**Square off** restores the accepted C1A.5 market/terrain baseline; remove `town-square=c1b` to avoid requesting the GLB on a fresh load. **Town off**, or removing `dev-town=s2f`, restores the original island and vegetation. The development gate accepts only the exact flag on localhost; public hosts remain rejected. Removing `terrain-study=c1a5` as well returns to the earlier town workflow. Source copies are in `validation/town-square-c1b/pre-change/`; do not reset the unrelated working tree.

The two-way route is technically verified. Human visual approval remains pending. Three remaining visual/design limitations:

1. Preserved market planting and layered guardrails still partly screen the arrival basin. The sculpture remains visible; simplifying approved market rails would need a separate design decision.
2. The compact two-level centre requires the supported civic approach, rather than the broad single-level plaza in the original concept. Retaining faces and the 1.56 m camera retraction deserve owner review.
3. Fountain water is static, and the highland exploration trail remains steep (accepted terrain survey peaks at 41.8%). No accessible-route claim or Guild/skyport construction is implied.

**No public deployment, Guild, skyport architecture, new storefronts, NPC gameplay or R0-C2 work was performed.**
