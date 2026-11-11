# Pelabuhan Awan C3.1

**Localized polish complete; owner visual approval pending. No deployment.** [Matched gallery](index.html) · [Editable Blender derivative](pelabuhan-awan-polish.blend) · [Detail GLB](skyport-details.glb) · [Sources](SOURCES.md).

Only three refinements: **two 2.2 m mooring pylons** with closed eyes/cleats inside the unchanged guardrail; **one 5.1 m timber wind standard** with reused navigation fixture and a static tapered jade/bronze sleeve; **four small true-north-aligned bronze ticks** outside the existing windrose. No rope, extra ring, open boarding gate, animation, travel action or new material family.

Pylons: local `(u,v)=(±3.55,−10.5)`. Wind standard: `(-4.60,−8.30)`. All use the existing C3 datum **15.095 m**, metre scale and root transform. Shoes follow measured existing ground. No terrain, floor, guard, spawn, route or approved building transform changes. The C3 `.blend` and 731,580-byte GLB remain unchanged.

## Measurements and validation

Increment: **726 triangles**, **41,120 GLB bytes**, **10,571 bytes measured gzip-9 representation**. Local server delivers uncompressed GLB; gzip size is not a network-transfer claim. Three indexed geometry/material batches, **zero new rendered material definitions/textures/transmission**. All three slots reuse actual C3 material objects. Fixed-camera increments: **5–6 all-pass calls / 1,344–1,452 submitted triangles**; the three new main-pass batches plus relevant shadow submissions account for the cost. [Export metrics](export-metrics.json) · [Matched counters/cameras](comparisons.json).

Apple M4 Pro / ANGLE Metal, same 12 s rail plus 2 s warmup, standard shadows, exposure 0.96, Glass B, DPR 1. No simultaneous Blender render.

| Fresh matched run | Polish OFF | Polish ON |
|---|---:|---:|
| rAF median / p95 | 5.60 / 6.20 ms | 5.60 / 6.40 ms |
| CPU submission median / p95 | 0.70 / 0.90 ms | 0.70 / 0.90 ms |
| All-pass calls | 335–412 | 338–417 |
| Submitted triangles | 2,544,958–2,622,900 | 2,545,684–2,624,244 |

Both runs have 2,161 timing samples. This is rAF/CPU timing, not GPU time or a mobile result. Cold detail request: **41,420 transfer bytes / 41,120 encoded bytes / 1.3 ms local**. One extra cached GLB (11 files versus 10); no new texture requests. Final active runs contain no rendering warnings/errors. [Raw performance/resource inventory](performance.json).

The existing animated explorer completes the uninterrupted arrival → Market Street → Telaga Awan → Guild journey and return, a circuit around the wind standard, a mooring-pylon collision probe, the closed docking guard and jump/landing. [Actual live results](live.json). The existing Guild button still opens the authentic transit study and closes back to exploration. [Research result](research.json).

The first live mast circuit stalled at a tight corner despite the initial CPU pass. Moving only the new mast **0.25 m inward** and widening its test circuit corrected it; final live and CPU retests pass. The failed first run is retained in [first-live.json](first-live.json). Eight final CPU checks cover 20/60 Hz civic traversal, local movement, actual support, three visible-object colliders, shared materials and exact rollback. [Controller results](controller.json). **18 scoped regressions pass, none skipped:** C3.1/C3 flag and GLB checks, Guild, character and six-project portfolio/experience cases. [Regression output](regression.log).

## Visual inspection and preservation

Five matched game pairs plus [actual explorer](06-gameplay.png); camera tuples/FOV and settings accompany each PNG. Existing browser buffer **1280 × 656**, DPR 1, standard shadows, exposure 0.96, approved Glass B. No relighting or postprocessing change. The flat pennant was replaced by the more legible static wind sleeve; the docking camera now includes both complete pylons and the continuous guardrail. Final images supersede first-pass captures.

Internal observations: **world composition** stays subordinate to the terrain/Guild; **architecture** reuses the tropical palette; **streetscape** adds docking cues without clutter; **navigation** retains the open civic axis; **materials/light** remain shared and unchanged; **atmosphere** retains the forest/cliffs; **identity** improves through mooring hardware and wind indication; **character scale** is checked with the actual explorer. These observations do not grant human artistic approval. At whole-island distance, the marker remains subtle and fine docking details do not resolve; no oversized mast was added to compensate. Mobile/GPU timings are untested.

[Preservation hashes](preservation.json) verify the accepted C3 master/GLB, Guild, town, terrain, player/camera and earlier masters. CPU snapshots confirm unchanged terrain and every original instanced placement, including the 42 town props. No portfolio page or research content was edited. [Provenance and exact license references](SOURCES.md).

## Toggle and rollback

Add **`town-skyport-polish=r0c3-1`** to the existing local C3 flags. Removing it and reloading restores accepted C3 with **no detail asset request**. Review “Polish off” removes the child meshes and three colliders exactly; base C3/whole-town toggles continue to restore their layers in the same world and renderer. Cached assets are reused. [Fresh flag-off load](disabled-load.json) · [Live rollback](rollback.json).

Source rollback backups for the only edited integration/review files are in `baseline/`. New module: `assets/js/floating-atlas/skyport-polish.js`. A short root-manifest append records this phase. Preserve unrelated working-tree edits. Reuse the running loopback preview on **4176**, or `python3 validation/skyport-r0c3/serve.py`. Stop at C3.1 for owner review.

Scoped delivery QA: PASS for actual meshes/screenshots, functioning existing controls, measured claims, shared palette and exact preservation/rollback. The quiet comparison gallery uses ENERGY 1 / RHYTHM 1 / MOTION 0 to support review; no portfolio UI redesign.

Reproduce scoped checks: `node validation/skyport-r0c3-1/check.mjs`; `node --test tests/{skyport-polish,skyport,atlas-guild,atlas-character,living-atlas}.test.mjs`. A fresh flag-off preview tab initially failed to fetch the entry module; one reload recovered. The final loaded baseline has ten cached files, zero detail requests and no rendering errors; no production error-retry code was changed for this local preview issue.
