# Merchant Citadel / Kota Niaga Awan - P1.4 planning package

**Status: MERCHANT CITADEL P1.4 - PENDING HUMAN VISUAL APPROVAL.** Planning and Blender concept only. Dated 2026-11-12. P2 has not started.

P1.4 is a creative redesign on the P1.3 foundation. The street network of P1.3 is kept; what changed is what stands on it and how it is composed:
a raised civic terrace with a 12 m flight of steps, a taller Exchange Hall tower, three corner tower houses, a merchants' inn, two more bazaar-edge shops,
a market street lined by four striped awning rows in place of scattered stalls, cloth awnings and pennant lines, and six buildings turned off the grid.
**24 buildings** (22 in P1.3). No asset was adopted from a new source; one new pack was downloaded, examined and rejected on its licence.

This folder is separate from `../p1.3/` and `../p1/`, which are unchanged.

| # | Deliverable | File |
|---|---|---|
| 1 | Revised town design bible | [01-town-design-bible.md](01-town-design-bible.md) |
| 2 | Visual reference board R01-R11 and traceability | [02-visual-reference-board.md](02-visual-reference-board.md) |
| 3 | Updated external asset inventory | [03-asset-inventory-update.md](03-asset-inventory-update.md), [03b-asset-inventory-additions.csv](03b-asset-inventory-additions.csv) |
| 4 | Evidence of newly verified models | [new-asset-evidence-sheet.png](visuals/new-asset-evidence-sheet.png) |
| 5 | Alternative layout studies | [04-layout-alternatives.md](04-layout-alternatives.md), [alternatives-plans.png](visuals/alternatives-plans.png), [alternatives-massing.jpg](visuals/alternatives-massing.jpg) |
| 6 | Selected measured masterplan | [05-selected-masterplan.md](05-selected-masterplan.md), [OUTPUT G](visuals/output-g-orthographic-masterplan.png) |
| 7 | Building schedule | [06-building-schedule.csv](06-building-schedule.csv), [06b-stall-and-awning-row-schedule.csv](06b-stall-and-awning-row-schedule.csv) |
| 8 | Archetype and construction specifications | [07-archetype-construction-specifications.md](07-archetype-construction-specifications.md) |
| 9 | Seven visual outputs | [A](visuals/output-a-hero-aerial.png), [B](visuals/output-b-merchant-street-gameplay.png) / [B2](visuals/output-b2-merchant-street-eye.png), [C](visuals/output-c-central-bazaar.png) / [C2](visuals/output-c2-central-bazaar-eye.png), [D](visuals/output-d-exchange-hall.png), [E](visuals/output-e-secondary-service-court.png) / [E2](visuals/output-e2-secondary-artisan-lane.png), [F](visuals/output-f-tea-lookout.png), [G](visuals/output-g-orthographic-masterplan.png); experiment: [bazaar from the terrace](visuals/experiment-bazaar-from-terrace.jpg) |
| 10 | Before/after comparison and visual quality review | [08-before-after-and-visual-review.md](08-before-after-and-visual-review.md) |
| 11 | Spatial and camera validation | [09-spatial-camera-validation.md](09-spatial-camera-validation.md) |
| 12 | Technical feasibility and optimisation | [10-technical-feasibility-optimisation.md](10-technical-feasibility-optimisation.md) |
| 13 | Town-first terrain support contract | [11-terrain-support-contract.md](11-terrain-support-contract.md) |
| 14 | P2 construction contract | [12-p2-construction-contract.md](12-p2-construction-contract.md) |
| 15 | Remaining decisions and risks | [13-decisions-and-risks.md](13-decisions-and-risks.md) |

Evidence classes: outputs A-F and the archetype tiles are ASSET-BACKED BLENDER BLOCKOUT; the alternatives massing is boxes and prisms at module dimensions; plans are drawings generated from the layout data.
No illustrative concept image and no AI-generated image is included. No image from any reference is reproduced in this package.

## Reproduce

```bash
D=.asset-inspection/merchant-citadel-p1; S=docs/planning/merchant-citadel/p1.4/blender-inspection; B="/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --disable-autoexec"
python3 $S/town_data.py $D/p1.4/data
$B --python $S/render_archetypes.py -- $D/extracted $D/measurements.json $D/p1.4/data/archetypes.json $D/p1.4/archetypes
$B --python $S/massing_p14.py -- $D/p1.4/data/archetypes.json $D/p1.4/massing
$B --python $S/build_town.py -- $D/extracted $D/measurements.json $D/p1.4/data $D/p1.4/renders $D/p1.4/merchant-citadel-p1.4-blockout.blend
$B --python $S/validate_envelopes.py -- $D/p1.4/merchant-citadel-p1.4-blockout.blend $D/p1.4/data $D/p1.4/validation.json
$B --python $S/inspect_p14.py -- $D/extracted $D/measurements.json $D/p1.4/tiles
python3 $S/make_p14_package.py $D docs/planning/merchant-citadel/p1.4
```
