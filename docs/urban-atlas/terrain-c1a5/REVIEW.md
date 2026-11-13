# R0-C1A.5 — Terrain harmonization

**Owner review pending before R0-C1B. No public deployment or Town Square construction.**

Recommendation: retain the bounded western-market and civic-ground adjustments. Keep the highland slope unchanged: real controller tests pass, and flattening it would diminish the landscape.

[Local study](http://127.0.0.1:4173/index.html?experience=adventure&dev-town=s2f&terrain-study=c1a5&town-review=1) · [Survey](../../../validation/terrain-c1a5/survey.json) · [Validation](../../../validation/terrain-c1a5/validation.json)

## Scope and terrain

The existing terrain mesh is edited in place, with a per-world triangle sampler feeding the existing controller and camera-clearance checks. No second scene, renderer or movement system is added. Normals and local vertex colors update; disabling restores the original positions, normals, colors, sampler and vegetation. Cliff-rim vertices, waterfall and approved buildings/support assets remain unchanged.

Three priorities were studied: exposed western market footings, the low courtyard/forecourt interface, and the steep highland link. Only the first two receive local earth adjustments. The courtyard's gold outlines are planning references, not constructed paving, fountain or pavilion. The approved C1A Blender master remains untouched.

| Measure | Result |
|---|---:|
| Affected triangle footprint | **825.1 m² / 3.99%** of the island's top footprint |
| Changed vertices | 539 of 13,313; topology remains 26,416 triangles |
| Uplift | Zero outside the adjustment; affected vertices 0.00002–1.388 m; median **0.24 m**; no cuts |
| Geometric fill estimate | 312.9 m³, integrated over affected projected triangles |
| Grounded vegetation/props | 3 fern, 5 understory and 2 small-rock instances; Y only, no removal or horizontal relocation |
| Grounded grass | 905 blades; original counts/indices preserved |
| Detail cache | 10 near/far geometry copies, 6,064,080 raw array bytes; not a GPU-byte measurement |

Floor-to-ground gaps, **median / maximum**, from identical before/after sample grids:

| Area | Before | After |
|---|---:|---:|
| Kopi Awan | 4.97 / 5.93 m | 3.97 / 4.69 m |
| Rupa Rimba | 5.10 / 7.45 m | 4.12 / 6.69 m |
| Proposed courtyard | 0.81 / 2.99 m | 0.48 / 1.98 m |

Tall braced undercrofts remain intentional. The east buildings are unchanged. No island-wide flattening, concrete pad or new architectural model is introduced.

## Actual route verification

| Live existing-controller walk | Out / return distance | Out / return time | Result |
|---|---:|---:|---|
| Natural arrival ↔ existing square threshold | 69.45 / 69.45 m | 33.12 / 33.12 s | PASS |
| Market ↔ courtyard reservation, bare ground | 54.50 / 54.49 m | 26.03 / 26.03 s | PASS |
| Reservation ↔ existing highland junction | 33.86 / 33.86 m | 16.19 / 16.19 s | PASS |

All six live walks used terrain-adjusted mode, with zero unexpected air height or support events. The existing approach includes its market stairs. The initially attempted reservation shortcut encountered an existing ramp guard; the verified natural-ground route goes around its north end without editing the guard.

**This proves access to the reservation on natural ground. It does not test the unbuilt C1A courtyard floor, pavilion or proposed raised civic walk.**

The prior Blender study reported 39.1% highland grade. A finer live-height survey at 0.025 m intervals finds a short **41.8%** peak near X3.455,Z7.818. It is a steep exploration trail; both live directions pass unchanged, so no terrain smoothing is applied there.

Fresh scoped regression: **11/11 tests pass**, including the S2-F/G regressions, exact restoration, LOD preservation, jumping, camera-ground consistency and 16 new fixed-step route runs at 20/60 Hz. Command: `node --test tests/town-s2f.test.mjs tests/town-s2g.test.mjs tests/terrain-c1a5.test.mjs`. [Log](../../../validation/terrain-c1a5/regression.log).

The modified sampler matches **522 actual mesh-ray samples**, maximum numerical error 1.8e-14 m. [Height verification](../../../validation/terrain-c1a5/height-verification.json). The minimum live follow-camera distance was 1.57 m under the existing structures; movement physics and camera tuning are unchanged.

## Matched browser evidence and costs

All four pairs have identical camera, scene, FOV, rendering settings and **Glass B**. Screenshots are 1280×720; the drawing buffer is 1280×656 at DPR 1. Exposure 0.96, antialiasing and PCF soft shadows are unchanged. The civic view is at 1.65 m above the existing forecourt. Clouds and foliage retain their normal animation.

- [Island aerial pair](../../../validation/terrain-c1a5/comparison-island.jpg).
- [Market foundation pair](../../../validation/terrain-c1a5/comparison-foundations.jpg).
- [Market-to-square interface pair](../../../validation/terrain-c1a5/comparison-civic.jpg).
- [Courtyard/highland interface pair](../../../validation/terrain-c1a5/comparison-courtyard.jpg).
- [Actual moving explorer](../../../validation/terrain-c1a5/walking-market.jpg), [live traversal record](../../../validation/terrain-c1a5/live-traversal.json), [camera/settings checks](../../../validation/terrain-c1a5/capture-validation.json).

The terrain reuses its existing triangles and draw. One unlit planning-overlay mesh is present in both comparison states; it has no collision or shadow. Before/after render counters match in each captured view. The matched camera rail submits **285–392 draws / 2,596,608–2,731,002 triangles**, including rendering passes. Each benchmark uses a 2 s warmup and 12 s sample on Apple M4 Pro / ANGLE Metal:

| Run | Original median / p95 | Adjusted median / p95 |
|---|---:|---:|
| First pair | 5.6 / 6.7 ms | 5.6 / 11.2 ms |
| Warm repeats | 5.6 / 11.2 ms | 5.6 / 11.2 ms |

Warm render-submission CPU median/p95 was 0.8/1.0 ms in both states. These are rAF intervals and CPU submission measurements, not GPU timings or proof of zero overhead. All four runs are retained in [performance evidence](../../../validation/terrain-c1a5/performance-comparison.json). Textures stayed at 22 and shader programs at 43; the renderer's warmed geometry counter varied 247–263 as cached LODs were exercised. No missing textures, final errors or warnings were recorded.

The approved Market Street remains **10,007,904 GLB bytes**; no GLB was re-exported. The six-file model cache remains six requests across terrain toggles.

## Preservation and rollback

**3,284 pre-existing files are unchanged**; only five integration/sampler/review source files changed. All **233 checked asset/license files**, including approved Blender masters and GLBs, are unchanged. [Preservation record](../../../validation/terrain-c1a5/preservation.json).

`terrain-study=c1a5` requires the existing localhost-only `dev-town=s2f` flag. A fresh browser check with the study parameter alone showed the original island, one renderer, no Town GLB requests, and readable `project=mbr` content. [Default-off evidence](../../../validation/terrain-c1a5/default-off.json).

Immediate rollback: **Terrain before** restores original ground while retaining the market and Glass B. **Town off**, or removing `dev-town=s2f`, restores the original island. Removing `terrain-study=c1a5` returns to the S2-G town. Original copies of the five changed source files are in `validation/terrain-c1a5/pre-change/`; avoid resetting unrelated working-tree changes.

Remaining limitations: the actual square architecture is unbuilt; the highland trail remains steep; preserved rails/planting still partly screen the civic approach and Rupa Rimba retains a tall braced undercroft. C1B must use this updated ground survey when fitting new square supports. **Stop for owner approval.**
