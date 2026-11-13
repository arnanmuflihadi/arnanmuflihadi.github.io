# Merchant Citadel / Kota Niaga Awan - P1.3 planning package

**Status: MERCHANT CITADEL P1.3 - PENDING HUMAN REVIEW.** Planning and Blender concept only. Dated 2026-11-12. P2 has not started.

P1.3 changes the **form of the town**, which P1.1 and P1.2 had left alone. Three measured layouts were compared; the selected one has
**22 buildings** (17 before), lanes moved in behind the street rows, a cross street through the middle of the merchant street, buildings on
the bazaar and arrival edges, and the warehouse and tea house pulled into the town. Materials, signs, goods and light are those of P1.2, so
the before/after images differ only in layout.

This folder is separate from `../p1/`, which still holds the P1.2 package unchanged and reproducible.

| # | Deliverable | File |
|---|---|---|
| 1 | Urban morphology diagnosis | [01-urban-morphology-diagnosis.md](01-urban-morphology-diagnosis.md) |
| 2 | Three alternative masterplans | [02-three-alternative-masterplans.md](02-three-alternative-masterplans.md), [alternatives-plans.png](visuals/alternatives-plans.png), [alternatives-massing.png](visuals/alternatives-massing.png) |
| 3 | Alternative evaluation matrix | [03-alternative-evaluation-matrix.md](03-alternative-evaluation-matrix.md) |
| 4 | Selected layout design bible | [04-selected-layout-design-bible.md](04-selected-layout-design-bible.md), [orthographic-town-plan.png](visuals/orthographic-town-plan.png) |
| 5 | Building schedule | [05-building-schedule.csv](05-building-schedule.csv), [05b-market-stall-schedule.csv](05b-market-stall-schedule.csv) |
| 6 | Pedestrian network | [06-pedestrian-network.md](06-pedestrian-network.md) |
| 7 | Archetype schedule | [07-archetype-schedule.md](07-archetype-schedule.md), [archetype-assembly-sheet.png](visuals/archetype-assembly-sheet.png) |
| 8 | Visual views | A [aerial](visuals/view-a-aerial.png), B [street, gameplay camera](visuals/view-b-merchant-street.png), B2 [street, eye height](visuals/view-b2-merchant-street-eye.png), C [bazaar](visuals/view-c-central-bazaar.png), D [Exchange Hall](visuals/view-d-exchange-court.png), E [service court](visuals/view-e-service-court.png), E2 [artisan lane](visuals/view-e2-artisan-lane.png), F [tea route](visuals/view-f-tea-route.png) |
| 9 | Actual geometry and camera QA | [08-geometry-camera-qa.md](08-geometry-camera-qa.md) |
| 10 | Terrain interface contract | [09-terrain-interface-contract.md](09-terrain-interface-contract.md) |
| 11 | P2 construction contract | [10-p2-construction-contract.md](10-p2-construction-contract.md) |
| 12 | Before/after comparison | [11-before-after-comparison.md](11-before-after-comparison.md), before-after [A](visuals/before-after-a-aerial.jpg) [B](visuals/before-after-b-merchant-street.jpg) [C](visuals/before-after-c-central-bazaar.jpg) [D](visuals/before-after-d-exchange-court.jpg) |
| - | Changed files and approval dependencies | [12-changes-and-approval-dependencies.md](12-changes-and-approval-dependencies.md) |

Evidence classes: the eight views and the archetype sheet are ASSET-BACKED BLENDER BLOCKOUT; the alternatives images are MASSING (boxes and roof prisms at real
module dimensions, no downloaded model); the plans are drawings generated from the layout data. No illustrative concept image and no AI-generated image is included.

Asset sources, licences, hashes and the register of custom and variant items are unchanged from P1.2 and stay in `../p1/` (02, 03, 03b, 04). **No new asset was downloaded in P1.3.**

## Reproduce

```bash
D=.asset-inspection/merchant-citadel-p1; S=docs/planning/merchant-citadel/p1.3/blender-inspection; B="/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --disable-autoexec"
python3 $S/town_data.py $D/p1.3/data                                  # selected layout, nominal checks
$B --python $S/render_archetypes.py -- $D/extracted $D/measurements.json $D/p1.3/data/archetypes.json $D/p1.3/archetypes
$B --python $S/massing_p13.py -- $D/p1.2/data $D/p1.3/massing $D/p1.3/data/archetypes.json && python3 $S/compare_p13.py $D docs/planning/merchant-citadel/p1.3
$B --python $S/build_town.py -- $D/extracted $D/measurements.json $D/p1.3/data $D/p1.3/renders $D/p1.3/merchant-citadel-p1.3-blockout.blend
$B --python $S/validate_envelopes.py -- $D/p1.3/merchant-citadel-p1.3-blockout.blend $D/p1.3/data $D/p1.3/validation.json
python3 $S/make_p13_package.py $D docs/planning/merchant-citadel/p1.3
```
