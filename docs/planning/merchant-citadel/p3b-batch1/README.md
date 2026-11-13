# Merchant Citadel P3-B batch 1 — floating island terrain, playable landscape foundation, first visual pass

**Status: ready for human review. Nothing committed or deployed. Not approved.** Executor: Claude Sonnet 5.5. Baseline: P2-B batch 5 (24 buildings, unchanged) and the P3-A Concept S.

## Try it

```bash
node merchant-citadel-p2a/server.mjs --port 4180
```
`http://127.0.0.1:4180/merchant-citadel-p2a/index.html` (island on, targeted corrections on). `?island=0` restores the P2-B town-on-a-plane; `?fixes=0` (or `rail gates porch eaves gap signs`) switches the corrections off. WASD, Shift, Space, Q/R as before.

## What changed

* **Island**: 204 × 217 m (stack included, authoritative bounds from all geometry), asymmetric rim, strata in absolute elevation, keel underside with roots and floating debris, Sky Quay with a graded ramp, Caravan Green with wagons, hall shelf, Counting Crag with a switchback ascent, irregular tea contours, stream and 24 m Cloudfall, the Tea Stack with a pavilion and an optional 2.4 m bridge. 98.7 k static triangles + ~79 k instanced, 3.2 MB GLB, zero textures.
* **One definition feeds everything**: `source/p3b_model.py` → Blender GLB, int16 heightfield, walk mask, bounds. Visible mesh vs physical ground: mean 3 mm, p99 3.2 cm, max 0.85 m (hidden step under the podium).
* **Gameplay** (real controller and camera, scripted): 17/17 routes, 11/11 reachability, 65/65 town network edges (identical clearance to batch 5), falls recover, the rim cannot be left, 24 camera spots ≥ 2.79 m.
* **Corrections**: forecourt rail opened (and a pre-existing 1.0 m rail mesh/proxy mismatch fixed), porch and low-eave camera rules, B10–B11 gap closed, B15/B16 signage, Tea Lookout gate, podium drops removed by the shelf. Tea-house veranda unsolved.
* **Landing**: dragon measured (radius 2.44 m); 1,342 eligible nodes by criteria, no whitelist; all four P3-A areas eligible; the free-flight controller does not exist in this branch.
* **Performance**: 7.0–8.8 ms p50 to GPU completion at 1280 × 720 on this shared machine (two runs, ±2 ms), 868 k triangles in flight views. Lower-end hardware untested.

## Read

| | |
|---|---|
| [01](01-terrain-pipeline-and-contract.md) | pipeline, formats, bounds, deviations |
| [02](02-gameplay-validation.md) | routes, reachability, edges, camera (tables from evidence) |
| [03](03-targeted-town-corrections.md) | corrections with before/after |
| [04](04-dynamic-landing-assessment.md) | dragon landing |
| [05](05-performance.md) | measurements and limits |
| [06](06-assets-and-licences.md) | register |
| [07](07-backlog-and-risks.md) | defects, backlog, risks |

Visuals: `visuals/compare/compare-v*.jpg` (P3-A massing | P3-B Blender from the exported GLB | P3-B browser, 8 required views plus extras), `visuals/gameplay/` (8 gameplay-camera frames and a contact sheet), `visuals/blender/`, `visuals/browser/`. Evidence: `evidence/`. Source: `source/`.

## Files changed in the preview (isolated; production modules untouched, SHA-256 verified)

New: `merchant-citadel-p2a/island.js`, `island-landing.js`, `p3b-tests.js`, `p3b-fixes.js`, `data/island-*.{json,bin}`, `data/p3b-views.json`, `models/merchant-citadel-p3b-island.glb`, `baseline-p3b-batch1/` (pre-edit copies with SHA-256). Edited: `p2a.js` (island loader, corrections hooks, camera filter). Kit GLB and `scene.json` unchanged.

## Not verified / limits

No human playtest; scripted input only. No lower-end device, phone or other browser. The island is a first art pass: see 07. The route tests use the preview's collision, not the game's. Corrections are load-time edits, not yet in the kit. Quality scores are provisional internal observations; **owner approval pending**.

Rebuild: `bash docs/planning/merchant-citadel/p3b-batch1/source/build_all.sh`; Blender reference views: `source/p3b_blender_render.py`; sheets: `source/p3b_compose.py`.
