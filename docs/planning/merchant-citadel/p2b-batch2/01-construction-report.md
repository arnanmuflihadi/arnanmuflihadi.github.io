# 01 — Construction report: Central Bazaar (P2-B batch 2)

Baseline: P1.4 layout D, the P2-A closeout slice and the Exchange Hall (batch 1, not rebuilt). Same pipeline: reproducible Blender scripts → one kit GLB → three.js preview with the game's unmodified controller, camera, character and collision modules (SHA-256 of those modules unchanged, `merchant-citadel-p2a/baseline-p2a/PRODUCTION-MODULES-SHA256.txt`; `git status` shows only new untracked folders).

## 1. What was built

| ID | Building | Node(s) | Position (x, n) / rotation | Triangles (final kit) | Collision proxies | Signs |
|---|---|---|---|---|---|---|
| **B02** | Western Covered Market Hall (provisions) | `A02p` | (−13, 50) / 0° | 52,909 | 39 (4 posts, 10 roof-shell boxes, 17 merchandise, 4 counters, 2 awnings, 2 signs) | loaf + crate hung over the front, blue banner x 4 |
| **B03** | Eastern Covered Market Hall (crafts and textiles) | `A02c` | (13, 50) / 0° | 42,264 | 37 (4 posts, 4 wall runs, 10 roof boxes, 13 merchandise, 2 counters, cloth, signs) | coin + scroll hung over the front, burgundy banner x 4 |
| **B14** | Registry Office (guild), bazaar edge | `A04` | (25.5, 40.2) / −90° | 5,778 | 7 | scroll, burgundy |
| **E06** | Cloth seller, bazaar perimeter east | `A04` | (25.8, 46.9) / −82° | 5,778 (shared node) | 7 | crate |
| **E07** | Potter's outlet, bazaar north-west | `A04b` | (−24.8, 55.6) / 98° | 6,028 | 8 | jar |

Also new: nine `SIGN_*` kit nodes (1,732 triangles in total; every building now carries the sign its P1.4 schedule names), per-district dressing nodes `DRESSING_D2/D3/D5/D8`, a red-brick threshold apron in front of each hall (one tile row, hall width), 7 teleport buttons and 11 new reference cameras. Existing market stalls (R01–R04), awnings, the market cross, the inn, all P2-A buildings and the Exchange Hall are unchanged except for the corrections in section 4. Measured placement: all 14 buildings within **0.43 cm** of the P1.4 envelopes (`evidence/autotest-scale.json`); kit bounds within 0.005 cm; orientation checks pass.

## 2. Why the first assembly was generic, and what was done about it

The first assembly used the P1.4 archetype A02 as specified (its screenshots were overwritten by later captures; the P1.4 concept view in [before-after/ba-view-c-central-bazaar.jpg](visuals/before-after/ba-view-c-central-bazaar.jpg) shows the same repeated shell): **one** open timber arcade, 8 x 12 m, used twice. Both halls had the same plan, the same four arches on every side, the same blue banners and the same seal; only the merchandise kit differed. Seen from the street the pair read as one building repeated, and neither had a "strong entrance": the arcade was equally open on all four sides. The cause was architectural (one shell, no hierarchy of fronts), not a lack of props. Corrections, all in `p2a_bazaar.py`:

| | Western Hall — provisions | Eastern Hall — crafts and textiles |
|---|---|---|
| Shell | stays the open produce arcade (four open sides) | **partly closed shop-hall**: windowed plaster bays flank the entrance on the front, the back wall and the east side are closed, the west side stays open to the cross passage |
| Entrance | 4 m open front, **blue** striped cloth awnings over the outer bays, loaf and crate trade signs, red-brick threshold | 4 m opening between the windowed bays, **burgundy** awnings, coin and scroll signs, red-brick threshold |
| Colour tie to the street | blue = the provisions rows R01/R02 beside it | burgundy = the crafts rows R03/R04 beside it |
| Interior story | produce zone at the door (barrow, fruit baskets), bakery table, fish/sausage counters with scales, grain and kegs at the north end, hay bales, herbs hung from the roof | pottery shelf and bottles at the door, rug, apothecary table, merchant's desk (books, scrolls, coin pile, scale), book stand, dummy and bags, **wall of hanging dyed cloth** (burgundy, gold, blue, cream) at the back, chest |
| Silhouette from the aerial view | open arcade with blue awnings | solid-looking gabled shop with burgundy awnings |

Result: the pair reads as two buildings of one family (same posts, roof and seal), see [aerial](visuals/comparison/cmp-p3-bazaar-aerial.jpg), [West entrance](visuals/comparison/cmp-p3-west-entrance.jpg), [East entrance](visuals/comparison/cmp-p3-east-entrance.jpg). The Exchange Hall stays the dominant landmark: its tower is visible from the aisle and from the axis at the end of the street ([axis view](visuals/comparison/cmp-p3-axis-to-hall.jpg)), the halls' ridges (9 m) stay far below the tower (26 m) and the hall roofs use the same dark civic tile as the Exchange Hall, so they read as one civic family under it.
Deviation from P1.4 (owner may revert in one line in `p2a_bazaar.py`): the east hall is no longer an open arcade on four sides.

## 3. Camera and collision causes found while building (details in 04)

* The P2-A roof proxy for an open arcade was a **solid slab** from 2.2 m up over the whole footprint: inside either hall the camera sat **0.94 m** behind the player everywhere. The proxy is now a two-slope shell with the space below free; the camera stands at **4.0–4.3 m** in the aisles.
* The outermost 0.83 m eave step clipped the camera when standing under the eave; removed from the camera list (thin overhang). Result: 4.07 m minimum at the side openings (was 0.94 m).
* Merchandise collision is measured from the real models (bounding boxes of the source files), not hand-typed footprints: 51 solids in the new buildings, all stop the player.

## 4. Corrections to earlier deliverables found in this batch

| Finding | Effect | Fix |
|---|---|---|
| Vertex-coloured materials (`MI_Trim_Props_Vertex`, `MI_Trim_Metal_Vertex`: pottery, coins, bottles, many stall goods) exported **without** `COLOR_0`: the Color Attribute nodes still named the original layer while the exporter step had renamed the mesh layer to "Color". They rendered white-blue and shiny, including in the P2-A stalls | visible in P2-A/closeout stall rows | export now points every Color Attribute node at "Color"; goods now show their colours |
| A shared sign per archetype: B07 showed B09's loaf sign (P2-A) | wrong signs | signs are placed objects, one per building (`SIGN_*` nodes) |
| `FP-Chest_Wood` is origin-centred: half sunk into the floor | a hole and a missing-material primitive found by the GLB inspection | replaced by `AV-mdvl_dungeon_chest_01` (floor origin) |
| Fade opacity followed the raw camera distance and jumped by up to 0.75 in one frame | flicker in motion | temporal smoothing (out 0.06 s, in 0.3 s); max step 0.18 per frame |

## 5. Source and rebuild

`docs/planning/merchant-citadel/p2a/blender/`: `p2a_data.py` (slice, collision, network, views), `p2a_bazaar.py` (hall variants and per-asset footprints), `p2a_hall.py`, `p2a_kit_export.py` (kit, bake, GLB), `p2a_world_scene.py` (Blender assembly and parity renders), `p2a_registry.py`, `p2a_provenance.py`, `p2a_glb_inspect.py`, `p2a_compare.py`. The two source `.blend` assemblies (kit and slice) are in `.asset-inspection/merchant-citadel-p1/p2a/`; they embed third-party textures and are not in the zip.

```bash
python3 docs/planning/merchant-citadel/p2a/blender/p2a_data.py
Blender --background --factory-startup --disable-autoexec --python docs/planning/merchant-citadel/p2a/blender/p2a_kit_export.py -- <inspection> <out> merchant-citadel-p2a/data/scene.json
Blender --background --factory-startup --disable-autoexec --python docs/planning/merchant-citadel/p2a/blender/p2a_world_scene.py -- <inspection> <out> merchant-citadel-p2a/data/scene.json merchant-citadel-p2a/data
```
