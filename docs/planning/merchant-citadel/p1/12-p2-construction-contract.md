# 12 - P2 construction contract (revised in P1.2; not started; needs explicit authorisation)

P2 builds the eight archetypes with their two variants, the split gateway, the market cross and the stall kits as reusable assemblies. It does not
assemble the town (P3) or build terrain (P4). No further asset search is needed; the sources are fixed in 04.

## Inputs

- Archives and hashes: 04. Modules per archetype, with exact model identifiers, material strategy, collision and acceptance: 08. Custom and variant items: 03b. Assembler and data: `citadel_lib.py`, `town_data.py`.
- Grid: 2 m bays, 3 m storeys, authored scale, 90-degree rotations.

## Roster, readiness and triangle budget

| ID | Archetype | Instances in town | Module instances | Triangles now | Triangle budget (projection) | Readiness |
|---|---|---|---|---|---|---|
| A01 | Exchange Hall (Balai Niaga Awan) | 1 | 348 | 87,904 | 53,214 | READY |
| A02 | Covered Market Hall (Los Pasar) | 2 | 61 | 42,176 | 25,014 | CONDITIONAL |
| A03 | Jettied Merchant Shophouse (gable to street) | 3 | 59 | 19,238 | 15,156 | CONDITIONAL |
| A03b | Medium Merchant Shophouse (eaves to street) | 1 | 63 | 19,454 | 15,372 | READY |
| A04 | Compact Shop (gable to street) | 2 | 25 | 8,200 | 5,978 | READY |
| A04b | Compact Shop (eaves to street) | 2 | 25 | 8,134 | 5,912 | READY |
| A05 | Corner Commercial Building | 2 | 68 | 37,334 | 18,338 | READY |
| A06 | Artisan Workshop | 2 | 32 | 30,692 | 15,996 | READY |
| A07 | Warehouse (Gudang Niaga) | 1 | 80 | 42,321 | 22,791 | READY |
| A08 | Tea House (Rumah Teh) | 1 | 65 | 20,976 | 12,692 | CONDITIONAL |

**READY** (essential modules verified, assembly executable as written): A01, A03b, A04, A04b, A05, A06, A07, gateway, market cross.

**CONDITIONAL** (one specific dependency each):

| ID | Dependency | Closes when |
|---|---|---|
| A02 | The two dressing kits use the cafe pack, whose FBX files need their materials re-linked from the pack's Blender file, and Avramania goods | One conversion of the used cafe models to GLB with materials embedded is made and checked; owner approves both sources |
| A03 | Windows are mounted on the face of the jetty module, which has no opening | First A03 export shows no flicker in the engine, or an opening is cut |
| A08 | Hanging inn sign and flower boxes are Avramania models | Owner approves the source |

**BLOCKED:** none.

Items P2 must author rather than assemble (03b): the seal, one trade-sign mesh with seven pictograms and three field colours, three cloth material
instances, the dark roof material instance, the graded textures, and a purpose-made lamp post.

## Shared components (build first)

| Component | Used by |
|---|---|
| Plaster bays `Wall_Plaster_*`; stone bays `Wall_UnevenBrick_*` | all enclosed archetypes |
| Window inserts, shutters, door leaves | all enclosed archetypes |
| Posts `Corner_ExteriorWide_Wood`; ground-floor piers `Corner_Exterior_Brick` | all |
| Roofs `Roof_RoundTiles_4x6, 6x6, 6x8, 8x8, 8x12, 8x14`, `Roof_2x4_RoundTile`; gables `Roof_Front_Brick2/4/6/8` | all |
| Dormer, chimneys, timber canopy | A03, A03b, A04, A05, A06, A07, A08 |
| Jetty set `Overhang_Plaster_Short`, `Overhang_Side_Plaster_Short_L/R`, roof `6x10` | A03 |
| Porch set: `Wall_Arch`, `Corner_Exterior_Brick`, roof `6x6`, gable `Roof_Front_Brick6` | A01 |
| `Wall_Arch` arcade bay | A02, gateway |
| Signage kit: custom trade sign, burgundy / blue / cream cloth instances, seal, lantern | all frontages |
| Goods kit: cafe counters, tables, shelves, kegs; Avramania food; Quaternius pots, bottles, books | A02, stalls, tea terrace |

## Sequence

1. Scale scene: 2 m grid, 3 m storey, 1.9 m explorer.
2. Bake the colour grade of 05 into copies of the base-colour textures. Merge duplicate materials **only where the node set-up is identical** (same-named Quaternius materials differ by whether the mesh has vertex colours). Author the cloth and dark-roof instances, the seal and the sign.
2b. Convert the used cafe-pack models to GLB once, with their materials; atlas them.
3. Shared wall, window and door sub-assemblies.
4. A04 and A04b. 5. A03 and A03b. 6. A05 and A06.
7. A02 market hall, gateway lodges, market cross (same arcade system).
8. A01 Exchange Hall: main block, wings, tower above the roof, entrance porch, deck and skirt, stairs.
9. A07 warehouse, A08 tea house.
10. Apply the substitutions below; join static meshes per building by material.
11. One archetype exported and loaded in the real Three.js scene; measurements recorded; stop for approval.

## Quantified preliminary optimisation plan

Measured in Blender for the P1.2 blockout: **2,184 instances, 139 downloaded models, 847,312 triangles, 53 distinct materials
(232 duplicated slots as imported)** (architecture and nature textures up to 2048 px, props up to 4096 px, cafe pack with normal and roughness maps). The approved P1.1 was 779,806 triangles and 29 materials.

Triangles by category: architecture modules 327,590, goods, furniture and street props 198,063, vegetation 170,091, lanterns 124,168, stall bases 16,856, custom seal and signs 7,200, paving 3,344.
Island 1 is documented at 327-412 draw calls and about 2.5 million submitted triangles across all passes.

High-triangle components and the substitution proposed for each:

| Component | Instances | Triangles each | Total now | Target each | Saving | How |
|---|---|---|---|---|---|---|
| `FP-Lantern_Wall` | 44 | 2,822 | 124,168 | 600 | 97,768 | simplified bracket lantern (flat chain, 8-sided cage) |
| `MV-Corner_Exterior_Brick` | 30 | 3,102 | 93,060 | 300 | 84,060 | simplified quoin pier, same silhouette |
| `SN-CommonTree_3` | 27 | 3,505 | 94,635 | 1,500 | 54,135 | lower-detail tree for the backdrop ring |
| `SN-CommonTree_1` | 6 | 6,265 | 37,590 | 1,500 | 28,590 | lower-detail tree for the backdrop ring |
| `SN-Bush_Common_Flowers` | 16 | 1,368 | 21,888 | 500 | 13,888 | fewer leaf cards |
| `AV-mdvl_village_window_box_01` | 14 | 1,330 | 18,620 | 400 | 13,020 | flowers as cards |
| `FP-Crate_Wooden` | 9 | 1,576 | 14,184 | 230 | 12,114 | swap for MV-Prop_Crate (existing model, measured 230) |
| `FP-FarmCrate_Apple` | 3 | 4,028 | 12,084 | 600 | 10,284 | produce as a textured mound |
| `MV-Door_8_Round` | 13 | 1,142 | 14,846 | 400 | 9,646 | flatten studs and ring into the texture |
| `FP-Barrel` | 17 | 824 | 14,008 | 300 | 8,908 | 12-sided barrel |
| `FP-Barrel_Apples` | 4 | 2,480 | 9,920 | 700 | 7,120 | apples as a textured mound |
| `AV-mdvl_food_cabbage_01` | 6 | 1,448 | 8,688 | 300 | 6,888 | lower-detail cabbage |
| `FP-Bag` | 11 | 858 | 9,438 | 300 | 6,138 | simplified sack |
| `SN-TwistedTree_2` | 1 | 9,134 | 9,134 | 3,000 | 6,134 | lower-detail feature tree |
| `MV-Balcony_Simple_Straight` | 5 | 1,120 | 5,600 | 132 | 4,940 | swap for MV-Balcony_Cross_Straight (existing model, measured 132) |
| `FP-Stall_Cart_Empty` | 2 | 3,936 | 7,872 | 1,500 | 4,872 | simplify wheel and frame |
| `AV-mdvl_food_grain_sack_01` | 8 | 938 | 7,504 | 350 | 4,704 | simplified sack |
| `FP-FarmCrate_Carrot` | 1 | 5,262 | 5,262 | 600 | 4,662 | produce as a textured mound |
| `AV-mdvl_food_cheese_wheel_01` | 3 | 1,270 | 3,810 | 300 | 2,910 | 16-sided wheel |
| `FP-Dummy` | 1 | 2,858 | 2,858 | 900 | 1,958 | simplified armour stand |
| `AV-mdvl_food_fish_01` | 4 | 600 | 2,400 | 250 | 1,400 | simplified |
| `AV-mdvl_food_ham_01` | 3 | 750 | 2,250 | 300 | 1,350 | simplified |
| `AV-mdvl_village_well_01` | 1 | 1,004 | 1,004 | 600 | 404 | simplified well |

| Projection | Triangles |
|---|---|
| P1.2 blockout, measured | 847,312 |
| After the substitutions above | **461,419** (46% lower) |
| Paving as one plane per surface instead of 700 tiles | saves a further 3,312 |

Two of the targets are existing models with measured counts (`MV-Prop_Crate` 230, `MV-Balcony_Cross_Straight` 132). The others are **targets for a
simplified mesh that P2 has to produce and measure**; they are not achieved results. Draw calls: 53 materials means roughly 53 to 106 static batches if each
building is merged by material and grouped by district; instanced props add a handful.

## Measurable P2 verification steps

| Step | Measure | Pass condition (proposed, to be agreed) |
|---|---|---|
| 1 | Triangles per archetype GLB (glTF accessor counts, `docs/tooling/glb-inventory.mjs`) | At or below the budget column above |
| 2 | Distinct materials and textures in the exported set | Materials at or below 53; no texture above 2048 px |
| 3 | One archetype in the real page: `renderer.info.render.triangles` and `.calls` at three fixed cameras, against the island-1 baseline at the same cameras | Recorded; increase within the agreed budget |
| 4 | Scale and orientation in Three.js: door 2.1 m, storey 3.0 m, +y up, front on +z | Matches within 1 cm |
| 5 | Controller on the hall stairs and through a market-hall arch | Climbs and passes without sticking |
| 6 | Follow camera on the primary route in the engine | Matches section F of 09 or better |
| 7 | Frame time over a fixed 60 s walk at 1280 x 720, standard quality | Recorded with hardware noted; no claim before this exists |

The brief's earlier figure of about 350,000 triangles is treated as provisional: the projection above does not reach it with substitutions alone. Reaching it would need fewer or lower-detail backdrop trees, lower-detail wall and roof modules, or fewer lanterns, each to be decided on measured evidence, not by deleting architecture.

**Browser performance has not been validated.** Every number in this section comes from Blender.

## Acceptance for P2 as a whole

Each archetype matches its P1.2 render, uses only inventoried modules plus the items in 03b, loads in the real scene at correct scale, and has triangle,
material and draw-call counts recorded. Then stop for approval before P3.
