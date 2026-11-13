# Merchant Citadel / Kota Niaga Awan - P1 planning package (revision P1.2)

**Status: MERCHANT CITADEL P1.2 - PENDING HUMAN VISUAL AND ASSET APPROVAL.** Planning and concept only. Dated 2026-11-11. P2 has not started.

P1.2 carries out the owner's brief "P1.1 - Complete visual redesign and expanded asset integration". It is numbered P1.2 here because a
revision called P1.1 already exists and was approved by the owner on 2026-11-11 ([15-owner-approval-record.md](15-owner-approval-record.md)).
P1.2 **builds on that approved town**: no building, stall, walking node or paved surface moved. It changes how the town looks and what it
is dressed with. Everything approved in P1.1 is kept unchanged in [visuals/p1.1/](visuals/p1.1/) so the two can be compared and either can be chosen.

**Two approved items are superseded by this brief and need a fresh decision:** the guild seal (now crossing trade routes and a diamond, in
burgundy and gold) and the cloth colours (now burgundy for the guild and blue for the market). See [16-p1.2-change-log.md](16-p1.2-change-log.md).

| # | Document | P1.2 |
|---|---|---|
| 01 | [Town design bible](01-design-bible.md) | Rewritten around the "City of a Thousand Trades" vision |
| 02 | [External asset research](02-external-asset-research.md) | Targeted expansion: eight new sources examined, two adopted |
| 03 | [Verified asset inventory](03-verified-asset-inventory.csv), [custom and variant register](03b-custom-and-variant-register.csv) | 918 rows (was 613); register extended |
| 04 | [Source and licence register](04-source-license-register.md) | New sources, hashes and licence evidence added |
| 05 | [Architectural style specification](05-architectural-direction.md) | Palette, colour grade, signage and roof hierarchy |
| 06 | [Measured masterplan](06-measured-town-masterplan.md) | Positions unchanged; envelopes re-measured |
| 07 | [Building schedule](07-building-placement-schedule.csv), [stall schedule](07b-market-stall-schedule.csv) | Regenerated |
| 08 | [Archetype specifications](08-archetype-specifications.md) | Jetty, porch, signs, kits; readiness per archetype |
| 09 | [Walking network and spatial validation](09-walking-network.md) | Re-run on the new geometry |
| 10 | [Terrain interface contract](10-terrain-interface-contract.md) | Envelope re-measured; packed-earth courts added as a surface treatment |
| 11 | [Visual QA report, before and after](11-visual-qa-report.md) | Rewritten on the brief's ten criteria |
| 12 | [P2 construction contract](12-p2-construction-contract.md) | Exact dependencies, READY / CONDITIONAL / BLOCKED |
| 13 | [Risk and feasibility register](13-limitations-and-risks.md) | Updated |
| 14 | [P1.1 change log](14-p1.1-change-log.md) | Historical, unchanged |
| 15 | [Owner approval record](15-owner-approval-record.md) | Unchanged |
| 16 | [P1.2 change log and approval dependencies](16-p1.2-change-log.md) | New |

## Visuals

| File | Evidence class |
|---|---|
| [view-a-aerial.png](visuals/view-a-aerial.png), [view-b-merchant-street.png](visuals/view-b-merchant-street.png), [view-c-central-bazaar.png](visuals/view-c-central-bazaar.png), [view-d-exchange-court.png](visuals/view-d-exchange-court.png) | ASSET-BACKED BLENDER BLOCKOUT, P1.2 (one town, four cameras, same cameras as P1.1) |
| [before-after-a-aerial.png](visuals/before-after-a-aerial.png), [-b-](visuals/before-after-b-merchant-street.png), [-c-](visuals/before-after-c-central-bazaar.png), [-d-](visuals/before-after-d-exchange-court.png) | Approved P1.1 beside P1.2, same camera |
| [expansion-asset-contact-sheet.png](visuals/expansion-asset-contact-sheet.png) | REAL ASSET RENDER of the newly downloaded models, adopted and rejected |
| [real-asset-contact-sheet.png](visuals/real-asset-contact-sheet.png) | REAL ASSET RENDER of the original packs (unchanged from P1.0) |
| [archetype-assembly-sheet.png](visuals/archetype-assembly-sheet.png), [archetype-roof-plans.png](visuals/archetype-roof-plans.png) | ASSET-BACKED ASSEMBLY, front, rear and roof plan of all twelve assemblies |
| [orthographic-town-plan.png](visuals/orthographic-town-plan.png) | Measured drawing generated from layout data and measured envelopes |
| [blockout-top-orthographic.png](visuals/blockout-top-orthographic.png) | ASSET-BACKED BLENDER BLOCKOUT (top view) |
| [visuals/p1.1/](visuals/p1.1/), [visuals/p1.0/](visuals/p1.0/) | Earlier revisions, kept unchanged |

No ILLUSTRATIVE CONCEPT image and no AI-generated image is in this package.

## What is and is not downloaded geometry

- **Downloaded, as authored:** 139 models - 59 Quaternius Medieval Village, 34 Fantasy Props, 8 Stylized Nature, 26 Syntaxes of Play Medieval Cafe, 12 Avramania.
- **Material variants of downloaded models:** 15 ids - cloth in burgundy, blue and cream; civic roofs one value darker. Geometry unchanged.
- **Colour grade:** eleven downloaded materials are shifted towards the brief's palette (roof, timber, plaster, stone, paving, foliage). Geometry and UVs unchanged.
- **Custom, authored here:** the guild seal (12 placements) and 15 hanging trade signs in 9 pictogram/colour versions; 7,200 triangles in total.
- **Scaled:** the plain timber post (lamp posts, lane standards) and two floor jars.
- **Temporary, never an asset:** ground plane, packed-earth court planes, dark interior boxes, the 1.9 m explorer, and the afternoon light itself.

All of it is itemised in [03b-custom-and-variant-register.csv](03b-custom-and-variant-register.csv).

## Reproduce

```bash
D=.asset-inspection/merchant-citadel-p1; S=docs/planning/merchant-citadel/p1/blender-inspection; B="/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --disable-autoexec"
python3 $S/fetch_archives.py $D/archives && python3 $S/fetch_expansion.py $D/archives   # free uploads only; unzip each into $D/extracted/<pack_id>/
$B --python $S/measure_assets.py -- $D/extracted $D/measurements.json
$B --python $S/inspect_expansion.py -- $D/extracted $D/measurements-expansion.json $D/tiles-expansion 300
python3 $S/town_data.py $D/data                     # nominal checks
$B --python $S/render_archetypes.py -- $D/extracted $D/measurements.json $D/data/archetypes.json $D/archetypes
$B --python $S/build_town.py -- $D/extracted $D/measurements.json $D/data $D/renders $D/blender/merchant-citadel-p1-blockout.blend
$B --python $S/validate_envelopes.py -- $D/blender/merchant-citadel-p1-blockout.blend $D/data $D/validation.json
python3 $S/make_package_assets.py $D docs/planning/merchant-citadel/p1 && python3 $S/make_docs_p12.py $D docs/planning/merchant-citadel/p1
```
The before/after images need the P1.1 renders kept in `$D/p1.1/`. `make_docs.py` is the P1.1 generator and is kept for the record; do not run it over this revision.
