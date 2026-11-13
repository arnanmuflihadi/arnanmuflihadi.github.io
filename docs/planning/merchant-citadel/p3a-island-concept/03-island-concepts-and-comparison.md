# 03 — Three island concepts round the real town, and the choice

## What the images are

**Blender massing prototypes, labelled as such.** `blender/p3a_island_blender.py` opens the saved batch 5 Blender assembly of the 24 buildings **unchanged** (no building moved), removes only the temporary ground plane, and builds each concept from `blender/p3a_island_shape.py`: a terrain top, cliffs with rock strata, an underside, massing trees, paths and water. Flat-colour materials, faceted geometry, placeholder clouds. They show shape, proportion and relationships, not finished rock, foliage or water. The same four cameras are used for every concept (`visuals/comparison/compare-aerial|side|approach|top.jpg`); the measured plans come from the same shape file and the real building envelopes (`visuals/plans/plan-A|B|C|S.jpg`, `evidence/island-measurements.json`). Nothing here is in the browser.

## The three concepts

| | A — Merchant Plateau | B — Fractured Trading Isle | C — Terraced Merchant Highlands |
|---|---|---|---|
| Idea | compact irregular table, the hall on a small headland, even cliffs | a broken landmass: arrival on a detached shard across a bridge, a lookout stack, a dropped slab, overhangs, a long hanging root | a tilted table rising to a layered crag behind the hall, tea benches stepping down to the east cliff, a stream and a waterfall off the edge, a low quay prow to the south, a keel-shaped underside |
| Size (E–W × N–S) | 125 × 142 m | 136 × 144 m (plus three shards) | 178 × 216 m |
| Top area | 13,747 m² | 19,093 m² | 25,832 m² |
| Town's share of the top | 52 % | 37 % | 28 % |
| Terrain relief on top | −0.3 … +4.2 m | −3.5 … +7.3 m | −8.7 … +23.7 m |
| Underside depth below the rim | 46–58 m | 22–82 m | 48–94 m |
| Closest building to the rim | 13.6 m | 11.5 m | 18.5 m |
| Largest flat open disc the land can offer (8 m clear of rim and buildings) | 8.0 m radius | 11.1 m (plus 12 m on the arrival shard) | 13.4 m and 12.0 m |

## Evaluation (my reading of the comparison sheets; provisional)

| Criterion | A | B | C |
|---|---|---|---|
| Town support | good, tight | good on the main mass; **arrival and one viewpoint depend on bridges** | good, generous |
| Rock silhouette | generic "table with stalactites" | **most dramatic** from far away (shards, deep root) | strong and specific: strata, keel, crag, waterfall notch |
| Aerial appearance | the town fills the rock: "a town on a rock" | lively outline, but the top itself is flat lawn | **the only one with a landscape on top**: crag, benches, stream, green, quay |
| Town–terrain integration | hall shelf only | hall shelf, two fault steps | hall backed by the crag, tea house given its benches, warehouses given a porters' loop, arrival given a quay |
| Player-scale landscape | lawns and rim | lawns, a chasm, two bridges | climbs, descents, a stream to follow, four destinations |
| Scenic viewpoints | 2 (lookout, headland) | 3 (lookout, stack, chasm bridge) | 4–5 (lookout, Cloudfall overlook, Counting Stone, quay prow) |
| Transport access (N20) | apron only 14 m deep to the rim | **across a 22 m bridge**: every arrival and any cart crosses it | broad quay 3 m below the court, 14 m wide stair on the axis |
| Dragon approach and landing | little room: 8 m discs | good shard for landing, little on the main mass | four separate zones, 6–14 m radius |
| Modelling feasibility | easiest | hardest: four landmasses, overhangs, two bridges with collision and fall cases | medium: one landmass; benches and crag are stepped (modular), the stream is one ribbon |
| Browser cost (expected, not measured) | lowest | highest: most cliff surface per m² of land, more always-visible undersides | middle: largest top, but relief gives natural occlusion from street level |

**A** is safe and forgettable: it answers "where does the town stand" and nothing else, and it cannot host the dragon. **B** has the best distant silhouette and the best single moment (the bridge), but its drama is all at the edges while the top stays a lawn, and it makes the town's only entrance depend on a bridge. **C** is the only concept that gives each district the thing it was named for and fixes the top three weaknesses of doc 01 (the hall's backdrop, the arrival threshold, the lookout's view).

## Choice: C, refined with one idea from B

**Selected: "Terraced Merchant Highlands with the Tea Stack"** (key `S`), which is concept C unchanged plus two elements taken from B because the comparison showed C lacked them:

1. **The Tea Stack**, one detached rock stack off the eastern cliff south of the waterfall (an 8 m bridge span in the massing), carrying a small pavilion. It gives the tea lookout's panorama a focal point and gives the east side the fracture drama B had, without putting any required route on a bridge (the stack's rope bridge is optional exploration).
2. **Long hanging roots** under the thick northern end, to sharpen the distant silhouette.

I did not choose the most complex concept (that is B). The refinement is shown beside A, B and C in every comparison sheet so the choice can be checked by eye. **This is my recommendation; the choice is yours.**
