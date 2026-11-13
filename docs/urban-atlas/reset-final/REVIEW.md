# R0-RESET-FINAL owner review

Complete local development alternative. **Human visual approval is pending. No public deployment.**

The four unchanged storefront groups now face one civic promenade and a 210 m² Telaga Awan court. Arrival, market, fountain and the 10 × 8 m Guild reservation form one sequence. The old stairs, bridge system and detached forecourt are absent from this version. The Guild has a physical reservation noticeboard, not a building proxy. The arrival is a guarded paved threshold, not finished skyport architecture.

[Six review images](index.html) · [Actual explorer frame](../../../validation/reset-final/walking-forward.png) · [Coordinates](../../../validation/reset-final/layout.json) · [Provenance](../../../validation/reset-final/provenance.json)

| Measurement | Final result |
|---|---|
| Primary walk | 44.37 m; 42.00 m direct; 4 gentle changes of direction |
| Primary elevation / grade | 15.040–15.515 m; 2.02% maximum, no civic stairs |
| Clear street / square | 6 m spine; 15 × 14 m court |
| Building lower-shell gap | Maximum 2.85 cm at sampled plot perimeters; retained visible thresholds support door approaches |
| Terrain | 2501.9 m² affected triangles; 1453 vertices; -2.37 to +5.13 m |
| Earth-volume estimate | 2098.2 m³ fill / 367.3 m³ cut, integrated from triangle deltas; environment design only |
| Vegetation | 22 trees relocated, 2 removed; 2 palm adjustments; 68 understory instances cleared; 7 grass chunks regrounded |
| Active town geometry | 112,930 triangles; 91 render meshes; 55 materials; 4 texture objects; no missing textures |
| Source payload | 11,642,328 bytes across the unchanged market GLB and four civic exports; original market remains 10,007,904 bytes |

The largest +5.13 m fill is in the locally blended forest connector, removing its former deep dip. The island rim, cliffs, waterfall and highland ridge are unchanged. Rendered terrain and the existing height/collision sampler use the same modified triangles. Full ledger: [site validation](../../../validation/reset-final/site-validation.json), [vegetation changes](../../../validation/reset-final/vegetation-ledger.json).

Implementation: `assets/js/floating-atlas/entry.js` selects the version; `town-reconstruction.js` loads the assets; `reconstruction-plan.js`, `reconstruction-terrain.js`, `reconstruction-geometry.js`, `reconstruction-landscape.js` and `reconstruction-review.js` contain the isolated layout, shelf, paving, vegetation and evidence controls. Exact hashes are in `validation/reset-final/implementation-hashes.json`.

The three principal composition fixes are the continuous street-to-square alignment, continuous shopfront thresholds, and coordinated terrain/forest clearance. A detached source caption was omitted beside the fountain; the original export, sculpture and basin remain unchanged. Compatible guard fittings are batched by material. No approved building geometry was altered.

## Actual gameplay and regression evidence

- **11/11 real-game checks pass:** uninterrupted arrival-to-Guild-reservation and reverse; four door approaches; jump/landing; guard; fountain; optional forest branch both ways. [Live traces](../../../validation/reset-final/live-traversal.json).
- **13/13 CPU controller cases pass**, including both 20 Hz and 60 Hz civic traversals, actual terrain and visible imported floor support. Maximum terrain/raycast error 2.13e-14 m; pavement/support error 6.97e-08 m away from the original raised building thresholds. [Results](../../../validation/reset-final/controller-routes.json).
- **35 existing scoped tests pass**, covering landscape, character, experience, S2-F/G, square and circulation preservation. [Log](../../../validation/reset-final/regression.log).
- Static material batching retains all single-material and repeated-material face groups and world bounds. [Regression](../../../validation/reset-final/batch-regression.log).
- **Two exact restoration round trips pass:** every original terrain attribute, instance matrix, collider and scene-child identity. All 2201 baseline files were checked; only the entry integration and asset-manifest history changed. Approved native masters, GLBs, archives and research pages retain their hashes.
- Fresh default page requests no town assets; Home/editorial/adventure, Work's six studies, `project=mbr` and the old accepted town were checked in the browser. [Navigation record](../../../validation/reset-final/navigation-checks.json).

## Measured rendering cost

Same scene and renderer, Apple M4 Pro / ANGLE Metal, 1440 × 836 drawing buffer, DPR 1, standard shadows, antialiasing, exposure 0.96, Glass B. Each matched camera rail has 2 s warmup and 12 s sampling. rAF intervals are measured frame intervals, **not GPU timing or a device-independent FPS promise**.

| Setting | Median / p95 frame ms | Draw calls, all passes | Submitted triangles, all passes |
|---|---:|---:|---:|
| Original landscape / town OFF | 5.60 / 11.10 | 118–127 | 2,317,976–2,343,064 |
| Rebuilt town ON | 5.60 / 11.30 | 255–310 | 2,480,014–2,552,380 |

CPU render submission ON: 3.10/4.80 ms median/p95. Loading cache holds 7 files, with no added requests when toggled off/on. Browser memory counters and observed resource-transfer/cache entries are retained in [performance evidence](../../../validation/reset-final/live-performance.json); source file bytes are distinct from observed transfer bytes. No browser warnings/errors were reported. Authored Glass A remains reversible; B is the measured default.

## Review limits (maximum three)

1. The optional forest branch is traversable but retains short 52.8% pitches. It is an exploration branch, separate from the 2.03% civic route.
2. Approved Glass B remains darker and less reflective than the Blender transmission reference; lighting and architecture were preserved.
3. Guild and skyport architecture remain deliberately unbuilt. Their reservation/threshold does not establish a future building entrance or dragon landing system.

## Open and roll back

Local preview: `http://127.0.0.1:4175/index.html?experience=adventure&dev-town=s2f&town-layout=reset-final&town-review=1&build=reset-final`.

- Immediate original landscape: **Town off**, or remove `dev-town=s2f` and `town-layout=reset-final` from the URL.
- Previous accepted town: remove `town-layout=reset-final` and use `dev-town=s2f&terrain-study=c1a5&town-square=c1b&circulation=c1c&town-review=1`. The two towns are mutually exclusive.
- Code checkpoint: `codex/reset-final-checkpoint` (`ff8b545ebd7c13894bf4af59fc5406ee8e1a6ada`). Restore only the entry file if code rollback is wanted; do not reset unrelated working-tree changes. Its direct backup is `validation/reset-final/entry.js.before`. Native sources are additionally preserved by SHA256.

Reproduce: run `node validation/reset-final/test-routes.mjs`, `node validation/reset-final/site-validation.mjs`, and `node validation/reset-final/batch-regression.mjs`. Use the visible review controls for the real explorer, camera presets and camera-rail measurements. `captures.json` records every final camera/settings tuple. The isolated civic derivative is `validation/reset-final/civic-reuse.blend`; it is not a new town master.

Anti-slop delivery check: **Hard gate PASS** (authorized real scene assets, native review buttons, no fabricated claims or production UI change); **Purpose PASS** (forest/stone palette retained, gold only identifies the technical primary route); **Liveliness PASS** (ENERGY 2 / RHYTHM 2 / MOTION 1, fountain focal point and varied approved roofs); **Craftsmanship PASS** (actual captures, controller tests, restoration and measured costs). This internal check does not grant owner artistic approval.
