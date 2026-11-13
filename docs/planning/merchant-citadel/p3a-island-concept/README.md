# Merchant Citadel — P2-B final art-direction review and P3-A floating-island concept

**Status: concept package for human visual approval. Nothing is approved, committed, deployed or integrated. The built town is unchanged** (no file of the kit, `scene.json` or the game was edited). Executor: Claude Fable 5.2. Date 2026-11-13.

## Recommendation (the four answers the brief asks for)

1. **Accept P2-B architectural construction?** I recommend **yes, with the small corrections below**. The 24 buildings do not need rebuilding; what the town lacks is its landscape and three camera/dressing fixes (doc 01). This is a recommendation; no human has played it and performance is unmeasured, so I do not claim either has passed.
2. **Necessary targeted corrections** (doc 02, tested but **not applied**): C1 open the three centre bays of the forecourt rail and make the hall's porch roof camera-transparent (doors reachable; camera at the doors 0.77 m → 2.87 m); C2 camera rule "roof bands starting below 3.2 m are camera-transparent" (nine worst spots 0.84–1.95 m → 2.7–2.9 m); C3 close the 0.75 m B10–B11 gap (it is enterable); C4 the podium's unguarded 2 m side and back drops are removed by the island's hall shelf; C5 stronger trade identity on B15/B16 by dressing. Open: the tea-house veranda (1.49 m) is not solved.
3. **Island to take to production:** **"Terraced Merchant Highlands with the Tea Stack"** (concept C refined with one idea from B): 178 × 216 m, a quay prow 3 m below the arrival court, a layered crag behind the hall, tea benches stepping 8.5 m down to the east cliff, a stream and waterfall, a detached stack, a keel-shaped underside (docs 03, 04).
4. **Technical risks to test before integration** (doc 05): a valid frame-time baseline (none exists); distant and dragon-flight views drawing the whole 588 k-triangle town plus the island (far LOD needed, to be measured); a new support grid (the current one is uint8 centimetres, 0–2.55 m, town-sized); safe-ground and fall recovery; camera against real terrain; one lower-end device.

**I stop here for your visual approval before any island construction.**

## Documents

| File | Content |
|---|---|
| [01](01-final-p2b-visual-assessment.md) | independent whole-town review, weaknesses by cause, rubric |
| [02](02-targeted-corrections.md) | forecourt rail, terrace/podium edges, B10–B11 gap, lane roofs: tested alternatives |
| [03](03-island-concepts-and-comparison.md) | concepts A, B, C, evaluation, choice |
| [04](04-selected-island-masterplan.md) | measured masterplan, integration, routes, edge safety, dragon landing |
| [05](05-construction-strategy-and-p3b-handoff.md) | construction strategy, assets, collision/camera interface, performance risks, P3-B handoff |

## Visual evidence (all Blender massing prototypes with the real town; none is a browser render)

| Brief item | File |
|---|---|
| 1 Full aerial on the island | `visuals/selected/v1-aerial.jpg`, `v1b-aerial-northwest.jpg` |
| 2 Side profile and underside | `v2-side-east.jpg`, `v2b-side-south.jpg` |
| 3 Southern arrival and island edge | `v3-southern-arrival.jpg`, `v3b-arrival-edge.jpg` |
| 4 Exchange Hall with landscape | `v4-exchange-hall.jpg`, `v4b-hall-from-street.jpg` |
| 5 Tea Lookout panorama | `v5-tea-lookout.jpg`, `v5b-tea-benches.jpg` |
| 6 Distant dragon-flight approach | `v6-dragon-approach.jpg`, `v6b-dragon-approach-east.jpg` |
| 7 Measured top-down plan | `visuals/plans/plan-S.jpg` (and `plan-A/B/C.jpg`), `v7-top.jpg` |
| 8 Side-by-side alternatives | `visuals/comparison/compare-aerial|side|approach|top.jpg` |
| extra | `v8-crag-to-town.jpg`, `v9-caravan-green.jpg` |

`evidence/`: `targeted-tests.json` and seven preview captures for doc 02, `island-measurements.json`, massing statistics per concept, the batch 5 terrain interface used.

## Reproduce

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background .asset-inspection/merchant-citadel-p1/p2e/after/merchant-citadel-p2a-slice-source.blend --python docs/planning/merchant-citadel/p3a-island-concept/blender/p3a_island_blender.py -- .asset-inspection/merchant-citadel-p1/p3a/final S all --save
```

```bash
python3 docs/planning/merchant-citadel/p3a-island-concept/blender/p3a_plan.py docs/planning/merchant-citadel/p2e-batch5/terrain-interface.json .asset-inspection/merchant-citadel-p1/p3a/plans
```

Replace `S` with `A`, `B` or `C` for the alternatives. The town .blend is the batch 5 Blender assembly (built by `p2a_world_scene.py`); the script deletes only `TMP_ground` in memory and never saves over it.

## Limits, stated plainly

* The island exists only as massing in Blender: flat colours, faceted geometry, placeholder trees, clouds and water. Rock, foliage and water quality are not shown.
* Nothing of the island is in the browser; camera, collision, readability and cost on the island are unverified.
* The corrections in doc 02 were tested with in-memory overrides and scripted input, not applied and not played by a person.
* No performance measurement was made in this phase, and batch 5's frame times remain invalid.
* Landing-zone criteria are my concept criteria, not the game's landing system.
* Triangle figures for production terrain are estimates.
