# 08 - Archetype specifications (P1.2)

Module ids prefixed MV- / FP- (Quaternius), SY- (Syntaxes of Play) and AV- (Avramania) exist in the downloaded archives and are instanced at authored scale. Architecture sits on a 2 m / 3 m grid with 90-degree rotations. Ids with `@` are material variants (cloth colour, dark roof). `CUS-` ids are custom geometry. See 03b.

**Material strategy, all archetypes:** downloaded materials with the colour grade of 05 baked into the base-colour textures; cloth and dark-roof variants as material instances; cafe-pack materials atlased; no per-building colours.

Facade codes: P plaster, G half-timber grid, F/R/T plaster window (wide flat / wide round / thin round), D/O plaster door (flat / round), I inset round portal, S stone, s/r stone window, o/d stone door, A open timber arch, X no module (hidden face or floor below the roof). Strings read left to right from outside, one per floor.

Renders: [archetype-assembly-sheet.png](visuals/archetype-assembly-sheet.png) (front and rear), [archetype-roof-plans.png](visuals/archetype-roof-plans.png) (roof junctions from above).

**Shared assembly order:** (1) 2 m grid and 3 m storey; (2) ground-floor wall bays per facade string; (3) window inserts, door leaves, shutters; (4) corner piers or posts per floor; (5) upper floors; (6) gable infills; (7) prefab roof at wall-top height; (8) dormers and chimney seated on the slope; (9) canopy, sign, lantern, seal, props.

## A01 - Exchange Hall (Balai Niaga Awan)

| Field | Value |
|---|---|
| Purpose | Dominant civic landmark and research venue |
| Instances planned | 1 |
| Nominal footprint (m) | 28 x 16 |
| Measured bounds incl. roof and props (m) | 29.7 x 18.0 x 22.99 high |
| Floors | 2 storeys + central tower (walls above the roof on levels 4-5), gabled entrance porch, 1 m podium |
| Roof | Roof_RoundTiles_6x6, Roof_RoundTiles_8x14, Roof_Tower_RoundTiles |
| Source | Quaternius Medieval Village [Standard] + Fantasy Props [Standard], glTF |
| Other publishers' models | None |
| Scale / rotation | 1.0; 0, 90, 180, 270 degrees |
| Module instances | 348 (28 ids) |
| Triangles, unoptimised | 87,904 (of which custom 1,320) |
| Triangles after the P2 substitutions (projection) | 53,214 |
| P1.2 change | Gabled entrance porch added (arches on stone piers, 6 x 6 roof run back into the main slope); three upper windows behind it became plain bays; all roofs civic dark; burgundy banners; new seal in the porch gable and on the tower. |
| Collision | Box proxies: main 14 x 8 x 6, tower 4 x 4 above 10 m, wings 6 x 6 x 6, podium 28 x 16 x 1, four porch pier proxies; stairs as five 0.2 m steps or one ramp proxy |
| Custom geometry | Guild seal x3 |
| Acceptance | Porch ridge buried in the main roof with no open end; doors reachable through the porch; tower seal visible from the bazaar and court |
| Readiness | READY |

| Block | W x D (m) | Floors | Roof | Offset (x, y, z) | front | right | back | left |
|---|---|---|---|---|---|---|---|---|
| main | 14 x 8 | 2 | 8x14 | [0, 0, 1.0] | rsoIosr / RRPPPRR | SXXS / PXXP | SsSsSsS / PRPRPRP | SXXS / PXXP |
| tower | 4 x 4 | 5 (walls from level 4) | tower | [0, 0, 1.0] | XX / XX / XX / PP / RR | XX / XX / XX / TT / RR | XX / XX / XX / PP / RR | XX / XX / XX / TT / RR |
| wing_e | 6 x 6 | 2 | 6x6 | [10, 0, 1.0] | sss / RRR | SsS / PRP | SsS / PRP | XXX / XXX |
| wing_w | 6 x 6 | 2 | 6x6 | [-10, 0, 1.0] | sss / RRR | XXX / XXX | SsS / PRP | SsS / PRP |
| porch | 6 x 2 | 1 | 6x6 | [0, -5, 1.0] | AAA | A | XXX | A |

**Modules (id x count):** `MV-Floor_Brick` x112, `MV-Stairs_Exterior_SingleSide` x44, `MV-Window_Wide_Round1` x27, `MV-Wall_Plaster_Window_Wide_Round` x25, `MV-Wall_Plaster_Straight` x23, `MV-Corner_ExteriorWide_Wood` x16, `MV-Wall_UnevenBrick_Straight` x16, `MV-Wall_UnevenBrick_Window_Wide_Flat` x15, `MV-Window_Wide_Flat1` x15, `MV-Corner_Exterior_Brick` x10, `MV-Wall_Arch` x5, `FP-Banner_2_Cloth@burgundy` x4, `MV-Wall_Plaster_Window_Thin_Round` x4, `MV-Window_Thin_Round1` x4, `CUS-Seal_NiagaAwan` x3, `MV-Door_8_Round` x3, `MV-Roof_Front_Brick6` x3, `MV-Roof_RoundTiles_6x6@dark` x3, `MV-Stairs_Exterior_Straight_Center` x3, `FP-Lantern_Wall` x2, `MV-Roof_Front_Brick8` x2, `MV-Wall_UnevenBrick_Door_Round` x2, `MV-Wall_UnevenBrick_Window_Wide_Round` x2, `MV-Roof_RoundTiles_8x14@dark` x1, `MV-Roof_Tower_RoundTiles@dark` x1, `MV-Stairs_Exterior_Straight_L` x1, `MV-Stairs_Exterior_Straight_R` x1, `MV-Wall_Plaster_Door_RoundInset` x1

## A02 - Covered Market Hall (Los Pasar)

| Field | Value |
|---|---|
| Purpose | Covered market, used twice with different dressing kits |
| Instances planned | 2 |
| Nominal footprint (m) | 8 x 12 |
| Measured bounds incl. roof and props (m) | 10.68 x 15.42 x 9.01 high |
| Floors | 1, open timber arcade |
| Roof | Roof_RoundTiles_8x12 |
| Source | Quaternius Medieval Village [Standard] + Fantasy Props [Standard], glTF |
| Other publishers' models | Syntaxes of Play: counters, food display, shelf, table, cloth, kegs, crate, basket, sausage, scale. Avramania: loaf, cheese, ham, cabbage, fish, scales, grain sack |
| Scale / rotation | 1.0; 0, 90, 180, 270 degrees |
| Module instances | 61 (27 ids) |
| Triangles, unoptimised | 42,176 (of which custom 880) |
| Triangles after the P2 substitutions (projection) | 25,014 |
| P1.2 change | One assembly, two kits chosen per building: provisions (west) and crafts (east). Dark roof, new seal, blue or burgundy banners. |
| Collision | Post proxies only; arcade stays walkable; goods as box proxies clear of the aisle |
| Custom geometry | Guild seal x2 |
| Acceptance | Centre aisle and cross-passage bay free of geometry; goods rest on the measured surfaces (0.81, 0.75, 1.15 m) |
| Readiness | CONDITIONAL - see 12 |

| Block | W x D (m) | Floors | Roof | Offset (x, y, z) | front | right | back | left |
|---|---|---|---|---|---|---|---|---|
| hall | 8 x 12 | 1 | 8x12 | [0, 0, 0] | AAAA | AAAAAA | AAAA | AAAAAA |

**Modules (id x count):** `MV-Wall_Arch` x20, `AV-mdvl_food_grain_sack_01` x4, `FP-Banner_1@blue` x4, `MV-Corner_ExteriorWide_Wood` x4, `AV-mdvl_food_cabbage_01` x2, `AV-mdvl_food_fish_01` x2, `AV-mdvl_food_loaf_01` x2, `CUS-Seal_NiagaAwan` x2, `FP-Table_Large` x2, `MV-Roof_Front_Brick8` x2, `AV-mdvl_food_cheese_wheel_01` x1, `AV-mdvl_food_ham_01` x1, `AV-mdvl_food_scales_01` x1, `FP-Barrel` x1, `FP-Barrel_Apples` x1, `FP-Bench` x1, `FP-FarmCrate_Apple` x1, `FP-FarmCrate_Carrot` x1, `MV-Roof_RoundTiles_8x12@dark` x1, `SY-basket-of-pastries` x1, `SY-counter_L` x1, `SY-counter_M` x1, `SY-crate02` x1, `SY-food-display` x1, `SY-food-sausage` x1, `SY-keg01` x1, `SY-keg02` x1

## A03 - Jettied Merchant Shophouse (gable to street)

| Field | Value |
|---|---|
| Purpose | Two-storey shophouse, gable to the street, jettied |
| Instances planned | 3 |
| Nominal footprint (m) | 6 x 8 |
| Measured bounds incl. roof and props (m) | 8.82 x 11.85 x 11.03 high |
| Floors | 2 |
| Roof | Roof_RoundTiles_6x8 |
| Source | Quaternius Medieval Village [Standard] + Fantasy Props [Standard], glTF |
| Other publishers' models | Avramania flower box x2 |
| Scale / rotation | 1.0; 0, 90, 180, 270 degrees |
| Module instances | 59 (21 ids) |
| Triangles, unoptimised | 19,238 (of which custom 116) |
| Triangles after the P2 substitutions (projection) | 15,156 |
| P1.2 change | Upper floor jettied 1.12 m on `Overhang_Plaster_Short` with side cheeks and brackets; roof is the 6 x 10 shifted 1 m forward; trade sign under the jetty; flower boxes; the timber canopy of P1.1 is removed. |
| Collision | One box 6 x 8 x 6; jetty non-colliding (underside 3.0 m) |
| Custom geometry | Trade sign x1 |
| Acceptance | Jetty windows sit flush without flicker; sign underside 2.1 m or more; roof covers the jetty |
| Readiness | CONDITIONAL - see 12 |

| Block | W x D (m) | Floors | Roof | Offset (x, y, z) | front | right | back | left |
|---|---|---|---|---|---|---|---|---|
| body | 6 x 8 | 2 | 6x8 | [0, 0, 0] | FDF / RGR | PFPP / PRPR | PPP / PTP | PPFP / RPRP |

Jetty: front facade from level 2 is built from `MV-Overhang_Plaster_Short` instead of the wall modules listed; windows are mounted on its face.

**Modules (id x count):** `MV-Wall_Plaster_Straight` x15, `MV-Corner_ExteriorWide_Wood` x6, `MV-Window_Wide_Round1` x6, `MV-Wall_Plaster_Window_Wide_Flat` x4, `MV-Wall_Plaster_Window_Wide_Round` x4, `MV-Window_Wide_Flat1` x4, `MV-Overhang_Plaster_Short` x3, `AV-mdvl_village_window_box_01` x2, `MV-Roof_Front_Brick6` x2, `MV-WindowShutters_Wide_Flat_Open` x2, `CUS-Sign_Loaf_wood` x1, `FP-Lantern_Wall` x1, `MV-Door_1_Flat` x1, `MV-Overhang_Side_Plaster_Short_L` x1, `MV-Overhang_Side_Plaster_Short_R` x1, `MV-Prop_Chimney2` x1, `MV-Roof_Dormer_RoundTile` x1, `MV-Roof_RoundTiles_6x10` x1, `MV-Wall_Plaster_Door_Flat` x1, `MV-Wall_Plaster_Window_Thin_Round` x1, `MV-Window_Thin_Round1` x1

## A03b - Medium Merchant Shophouse (eaves to street)

| Field | Value |
|---|---|
| Purpose | Two-storey shophouse, eaves to the street (variant of A03 without the jetty) |
| Instances planned | 1 |
| Nominal footprint (m) | 8 x 6 |
| Measured bounds incl. roof and props (m) | 10.53 x 8.82 x 11.31 high |
| Floors | 2 |
| Roof | Roof_RoundTiles_6x8 |
| Source | Quaternius Medieval Village [Standard] + Fantasy Props [Standard], glTF |
| Other publishers' models | Avramania flower box x2 |
| Scale / rotation | 1.0; 0, 90, 180, 270 degrees |
| Module instances | 63 (22 ids) |
| Triangles, unoptimised | 19,454 (of which custom 116) |
| Triangles after the P2 substitutions (projection) | 15,372 |
| P1.2 change | Timber canopy along the front, trade sign, flower boxes. |
| Collision | One box 8 x 6 x 6; canopy non-colliding |
| Custom geometry | Trade sign x1 |
| Acceptance | Canopy clears open shutters; sign visible along the street |
| Readiness | READY |

| Block | W x D (m) | Floors | Roof | Offset (x, y, z) | front | right | back | left |
|---|---|---|---|---|---|---|---|---|
| body | 8 x 6 | 2 | 6x8 | [0, 0, 0] | FDFG / RRGR | PFP / PTP | PPPP / PRRP | PPP / PTP |

**Modules (id x count):** `MV-Wall_Plaster_Straight` x15, `MV-Corner_ExteriorWide_Wood` x8, `MV-Wall_Plaster_Window_Wide_Round` x5, `MV-Window_Wide_Round1` x5, `MV-Wall_Plaster_Window_Wide_Flat` x3, `MV-Window_Wide_Flat1` x3, `AV-mdvl_village_window_box_01` x2, `MV-Roof_Dormer_RoundTile` x2, `MV-Roof_Front_Brick6` x2, `MV-Roof_Wooden_2x1_Center` x2, `MV-Wall_Plaster_Window_Thin_Round` x2, `MV-Wall_Plaster_WoodGrid` x2, `MV-WindowShutters_Wide_Flat_Open` x2, `MV-Window_Thin_Round1` x2, `CUS-Sign_Loaf_wood` x1, `FP-Lantern_Wall` x1, `MV-Door_1_Flat` x1, `MV-Prop_Chimney2` x1, `MV-Roof_RoundTiles_6x8` x1, `MV-Roof_Wooden_2x1_L` x1, `MV-Roof_Wooden_2x1_R` x1, `MV-Wall_Plaster_Door_Flat` x1

## A04 - Compact Shop (gable to street)

| Field | Value |
|---|---|
| Purpose | Single-storey shop, gable to the street; registry office |
| Instances planned | 2 |
| Nominal footprint (m) | 4 x 6 |
| Measured bounds incl. roof and props (m) | 6.46 x 8.49 x 6.72 high |
| Floors | 1 |
| Roof | Roof_RoundTiles_4x6 |
| Source | Quaternius Medieval Village [Standard] + Fantasy Props [Standard], glTF |
| Other publishers' models | None |
| Scale / rotation | 1.0; 0, 90, 180, 270 degrees |
| Module instances | 25 (14 ids) |
| Triangles, unoptimised | 8,200 (of which custom 92) |
| Triangles after the P2 substitutions (projection) | 5,978 |
| P1.2 change | Timber canopy and trade sign added. |
| Collision | One box 4 x 6 x 3 |
| Custom geometry | Trade sign x1 |
| Acceptance | Matches the render |
| Readiness | READY |

| Block | W x D (m) | Floors | Roof | Offset (x, y, z) | front | right | back | left |
|---|---|---|---|---|---|---|---|---|
| body | 4 x 6 | 1 | 4x6 | [0, 0, 0] | DF | PFP | PP | PGP |

**Modules (id x count):** `MV-Wall_Plaster_Straight` x6, `MV-Corner_ExteriorWide_Wood` x4, `MV-Roof_Front_Brick4` x2, `MV-Wall_Plaster_Window_Wide_Flat` x2, `MV-Window_Wide_Flat1` x2, `CUS-Sign_Crate_wood` x1, `FP-Lantern_Wall` x1, `MV-Door_1_Flat` x1, `MV-Roof_RoundTiles_4x6` x1, `MV-Roof_Wooden_2x1_L` x1, `MV-Roof_Wooden_2x1_R` x1, `MV-Wall_Plaster_Door_Flat` x1, `MV-Wall_Plaster_WoodGrid` x1, `MV-WindowShutters_Wide_Flat_Open` x1

## A04b - Compact Shop (eaves to street)

| Field | Value |
|---|---|
| Purpose | Single-storey shop, eaves to the street (variant of A04) |
| Instances planned | 2 |
| Nominal footprint (m) | 6 x 4 |
| Measured bounds incl. roof and props (m) | 8.49 x 6.46 x 6.72 high |
| Floors | 1 |
| Roof | Roof_RoundTiles_4x6 |
| Source | Quaternius Medieval Village [Standard] + Fantasy Props [Standard], glTF |
| Other publishers' models | None |
| Scale / rotation | 1.0; 0, 90, 180, 270 degrees |
| Module instances | 25 (13 ids) |
| Triangles, unoptimised | 8,134 (of which custom 140) |
| Triangles after the P2 substitutions (projection) | 5,912 |
| P1.2 change | Trade sign, lantern and wall vine added. |
| Collision | One box 6 x 4 x 3 |
| Custom geometry | Trade sign x1 |
| Acceptance | Matches the render |
| Readiness | READY |

| Block | W x D (m) | Floors | Roof | Offset (x, y, z) | front | right | back | left |
|---|---|---|---|---|---|---|---|---|
| body | 6 x 4 | 1 | 4x6 | [0, 0, 0] | FDF | PP | PGP | PP |

**Modules (id x count):** `MV-Wall_Plaster_Straight` x6, `MV-Corner_ExteriorWide_Wood` x4, `MV-Roof_Front_Brick4` x2, `MV-Wall_Plaster_Window_Wide_Flat` x2, `MV-WindowShutters_Wide_Flat_Open` x2, `MV-Window_Wide_Flat1` x2, `CUS-Sign_Jar_wood` x1, `FP-Lantern_Wall` x1, `MV-Door_1_Flat` x1, `MV-Prop_Vine1` x1, `MV-Roof_RoundTiles_4x6` x1, `MV-Wall_Plaster_Door_Flat` x1, `MV-Wall_Plaster_WoodGrid` x1

## A05 - Corner Commercial Building

| Field | Value |
|---|---|
| Purpose | Heavy corner building with two active fronts |
| Instances planned | 2 |
| Nominal footprint (m) | 8 x 8 |
| Measured bounds incl. roof and props (m) | 10.68 x 10.78 x 12.01 high |
| Floors | 2, stone ground floor, two active fronts |
| Roof | Roof_RoundTiles_8x8 |
| Source | Quaternius Medieval Village [Standard] + Fantasy Props [Standard], glTF |
| Other publishers' models | Avramania flower box x2 |
| Scale / rotation | 1.0; 0, 90, 180, 270 degrees |
| Module instances | 68 (21 ids) |
| Triangles, unoptimised | 37,334 (of which custom 328) |
| Triangles after the P2 substitutions (projection) | 18,338 |
| P1.2 change | Two trade signs (one per front) replace the banners; flower boxes. |
| Collision | One box 8 x 8 x 6 |
| Custom geometry | Trade sign x2 |
| Acceptance | Both fronts read as entrances |
| Readiness | READY |

| Block | W x D (m) | Floors | Roof | Offset (x, y, z) | front | right | back | left |
|---|---|---|---|---|---|---|---|---|
| body | 8 x 8 | 2 | 8x8 | [0, 0, 0] | sosr / RGGR | rsos / RGGR | SSSS / PTTP | SsSS / PRRP |

**Modules (id x count):** `MV-Window_Wide_Round1` x8, `MV-Wall_UnevenBrick_Straight` x7, `MV-Wall_Plaster_Window_Wide_Round` x6, `MV-Wall_UnevenBrick_Window_Wide_Flat` x5, `MV-Window_Wide_Flat1` x5, `MV-Corner_ExteriorWide_Wood` x4, `MV-Corner_Exterior_Brick` x4, `MV-Wall_Plaster_Straight` x4, `MV-Wall_Plaster_WoodGrid` x4, `AV-mdvl_village_window_box_01` x2, `CUS-Sign_Coin_wood` x2, `FP-Lantern_Wall` x2, `MV-Door_8_Round` x2, `MV-Roof_Front_Brick8` x2, `MV-Wall_Plaster_Window_Thin_Round` x2, `MV-Wall_UnevenBrick_Door_Round` x2, `MV-Wall_UnevenBrick_Window_Wide_Round` x2, `MV-Window_Thin_Round1` x2, `MV-Prop_Chimney2` x1, `MV-Roof_Dormer_RoundTile` x1, `MV-Roof_RoundTiles_8x8` x1

## A06 - Artisan Workshop

| Field | Value |
|---|---|
| Purpose | Stone workshop with outdoor work area |
| Instances planned | 2 |
| Nominal footprint (m) | 6 x 6 |
| Measured bounds incl. roof and props (m) | 8.82 x 8.75 x 8.35 high |
| Floors | 1, stone |
| Roof | Roof_RoundTiles_6x6 |
| Source | Quaternius Medieval Village [Standard] + Fantasy Props [Standard], glTF |
| Other publishers' models | None |
| Scale / rotation | 1.0; 0, 90, 180, 270 degrees |
| Module instances | 32 (16 ids) |
| Triangles, unoptimised | 30,692 (of which custom 116) |
| Triangles after the P2 substitutions (projection) | 15,996 |
| P1.2 change | Trade sign (hammer) and wall vine added. |
| Collision | One box 6 x 6 x 3 plus prop proxies |
| Custom geometry | Trade sign x1 |
| Acceptance | Matches the render |
| Readiness | READY |

| Block | W x D (m) | Floors | Roof | Offset (x, y, z) | front | right | back | left |
|---|---|---|---|---|---|---|---|---|
| body | 6 x 6 | 1 | 6x6 | [0, 0, 0] | sos | SsS | SSS | SSs |

**Modules (id x count):** `MV-Wall_UnevenBrick_Straight` x7, `MV-Corner_Exterior_Brick` x4, `MV-Wall_UnevenBrick_Window_Wide_Flat` x4, `MV-Window_Wide_Flat1` x4, `MV-Roof_Front_Brick6` x2, `CUS-Sign_Hammer_wood` x1, `FP-Anvil_Log` x1, `FP-Barrel` x1, `FP-Lantern_Wall` x1, `FP-WeaponStand` x1, `FP-Workbench` x1, `MV-Door_8_Round` x1, `MV-Prop_Chimney` x1, `MV-Prop_Vine1` x1, `MV-Roof_RoundTiles_6x6` x1, `MV-Wall_UnevenBrick_Door_Round` x1

## A07 - Warehouse (Gudang Niaga)

| Field | Value |
|---|---|
| Purpose | Guild warehouse with paired doors and loading yard |
| Instances planned | 1 |
| Nominal footprint (m) | 8 x 14 |
| Measured bounds incl. roof and props (m) | 13.18 x 16.58 x 12.05 high |
| Floors | 2, stone ground floor |
| Roof | Roof_RoundTiles_8x14 |
| Source | Quaternius Medieval Village [Standard] + Fantasy Props [Standard], glTF |
| Other publishers' models | None |
| Scale / rotation | 1.0; 0, 90, 180, 270 degrees |
| Module instances | 80 (22 ids) |
| Triangles, unoptimised | 42,321 (of which custom 440) |
| Triangles after the P2 substitutions (projection) | 22,791 |
| P1.2 change | Dark roof, new seal, two wall vines. |
| Collision | One box 8 x 14 x 6 |
| Custom geometry | Guild seal x1 |
| Acceptance | Matches the render |
| Readiness | READY |

| Block | W x D (m) | Floors | Roof | Offset (x, y, z) | front | right | back | left |
|---|---|---|---|---|---|---|---|---|
| body | 8 x 14 | 2 | 8x14 | [0, 0, 0] | SooS / PGGP | SSsSsSS / PPTPTPP | SSSS / PGGP | SSsSsSS / PPTPTPP |

**Modules (id x count):** `MV-Wall_UnevenBrick_Straight` x16, `MV-Wall_Plaster_Straight` x14, `MV-Corner_ExteriorWide_Wood` x4, `MV-Corner_Exterior_Brick` x4, `MV-Wall_Plaster_Window_Thin_Round` x4, `MV-Wall_Plaster_WoodGrid` x4, `MV-Wall_UnevenBrick_Window_Wide_Flat` x4, `MV-Window_Thin_Round1` x4, `MV-Window_Wide_Flat1` x4, `MV-Prop_Crate` x3, `MV-Roof_Dormer_RoundTile` x3, `FP-Barrel` x2, `FP-Lantern_Wall` x2, `MV-Door_8_Round` x2, `MV-Roof_Front_Brick8` x2, `MV-Wall_UnevenBrick_Door_Round` x2, `CUS-Seal_NiagaAwan` x1, `FP-Crate_Wooden` x1, `MV-Prop_Vine1` x1, `MV-Prop_Vine5` x1, `MV-Prop_Wagon` x1, `MV-Roof_RoundTiles_8x14@dark` x1

## A08 - Tea House (Rumah Teh)

| Field | Value |
|---|---|
| Purpose | Tea house with a veranda |
| Instances planned | 1 |
| Nominal footprint (m) | 6 x 6 + 2 m veranda |
| Measured bounds incl. roof and props (m) | 8.82 x 9.04 x 11.17 high |
| Floors | 2, with a post-supported veranda and balcony |
| Roof | Roof_RoundTiles_6x6 |
| Source | Quaternius Medieval Village [Standard] + Fantasy Props [Standard], glTF |
| Other publishers' models | Avramania inn sign x1, flower box x2 (terrace furniture is town dressing, not part of the archetype) |
| Scale / rotation | 1.0; 0, 90, 180, 270 degrees |
| Module instances | 65 (21 ids) |
| Triangles, unoptimised | 20,976 (of which custom 116) |
| Triangles after the P2 substitutions (projection) | 12,692 |
| P1.2 change | Cup sign on the side wall, hanging inn sign under the veranda, flower boxes on side windows, vine. |
| Collision | One box 6 x 6 x 6; four post proxies; deck not walkable in P2 |
| Custom geometry | Trade sign x1 |
| Acceptance | Nothing hangs below 2.1 m over the veranda approach |
| Readiness | CONDITIONAL - see 12 |

| Block | W x D (m) | Floors | Roof | Offset (x, y, z) | front | right | back | left |
|---|---|---|---|---|---|---|---|---|
| body | 6 x 6 | 2 | 6x6 | [0, 0, 0] | FOF / ROR | PFP / PRP | PPP / PTP | PFP / PRP |

**Modules (id x count):** `MV-Wall_Plaster_Straight` x13, `MV-Corner_ExteriorWide_Wood` x8, `MV-Balcony_Simple_Straight` x5, `MV-Corner_Exterior_Wood` x4, `MV-Wall_Plaster_Window_Wide_Flat` x4, `MV-Wall_Plaster_Window_Wide_Round` x4, `MV-Window_Wide_Flat1` x4, `MV-Window_Wide_Round1` x4, `MV-Floor_WoodDark` x3, `AV-mdvl_village_window_box_01` x2, `MV-Door_8_Round` x2, `MV-Roof_Front_Brick6` x2, `MV-Wall_Plaster_Door_Round` x2, `AV-mdvl_village_sign_inn_01` x1, `CUS-Sign_Cup_wood` x1, `FP-Bench` x1, `MV-Prop_Chimney2` x1, `MV-Prop_Vine1` x1, `MV-Roof_RoundTiles_6x6` x1, `MV-Wall_Plaster_Window_Thin_Round` x1, `MV-Window_Thin_Round1` x1

## G01 - Gerbang Niaga split gateway (structure)

Two open timber lodges, each 2 x 4 m with arches on all sides and a small gabled roof (`Roof_2x4_RoundTile`, `Roof_Front_Brick2`), flank a 4 m lane open to the sky. Seal on each south gable; dark roofs. Readiness: READY. 33 instances, 13,740 triangles, measured 10.35 x 6.12 x 5.32 m.

`MV-Wall_Arch` x12, `MV-Corner_ExteriorWide_Wood` x8, `MV-Roof_Front_Brick2` x4, `CUS-Seal_NiagaAwan` x2, `FP-Lantern_Wall` x2, `MV-Roof_2x4_RoundTile@dark` x2, `FP-Barrel` x1, `FP-Table_Large` x1, `MV-Prop_Crate` x1

## M01 - Tugu Timbangan market cross (structure)

One stair block as a 2 x 2 x 1 m base, one timber post, two seals, two bracket lanterns at 2.4 m, goods at the foot. Readiness: READY. 9 instances, 8,504 triangles, measured 4.1 x 4.91 x 4.0 m.

`CUS-Seal_NiagaAwan` x2, `FP-Lantern_Wall` x2, `FP-Bag` x1, `FP-Barrel` x1, `MV-Corner_ExteriorWide_Wood` x1, `MV-Prop_Crate` x1, `MV-Stairs_Exterior_Platform` x1

## Market stall kits

| Kit | Base model | Canopy | Goods and props | Collision footprint (m) | Used |
|---|---|---|---|---|---|
| S01b | FP-Stall_Empty | blue cloth (variant) | AV-mdvl_food_cheese_wheel_01, AV-mdvl_food_grain_sack_01, AV-mdvl_food_loaf_01, FP-Barrel_Apples, FP-FarmCrate_Apple | 1.9 x 1.0 | 2 |
| S01g | FP-Stall_Empty | burgundy cloth (variant) | FP-Bag, FP-Crate_Wooden, FP-Pot_1, FP-Vase_2, FP-Vase_4 | 1.9 x 1.0 | 2 |
| S01c | FP-Stall_Empty | cream cloth (variant) | FP-Barrel, FP-Bottle_1, FP-Bucket_Wooden_1, FP-Potion_1, FP-SmallBottles_1 | 1.9 x 1.0 | 1 |
| S02c | FP-Stall_Cart_Empty | cream cloth (variant) | FP-Bag, FP-Pot_1, FP-Vase_2, MV-Prop_Crate | 3.1 x 1.2 | 1 |
| S02g | FP-Stall_Cart_Empty | burgundy cloth (variant) | FP-Bag, FP-Barrel, FP-Vase_4 | 3.1 x 1.2 | 1 |
| S03 | AV-mdvl_village_stall_01 | as shipped | AV-mdvl_food_cabbage_01, AV-mdvl_food_fish_01, AV-mdvl_food_ham_01, AV-mdvl_food_produce_crate_01, SY-crate02 | 2.3 x 1.2 | 2 |
| S04 | SY-counter_L | as shipped | AV-mdvl_food_scales_01, SY-basket-of-pastries, SY-counter_M, SY-food-bread01, SY-food-bread03, SY-keg01 | 3.2 x 1.0 | 1 |
| S05 | SY-table03 | as shipped | FP-Chalice, FP-Coin_Pile, FP-Crate_Wooden, FP-Scroll_1, FP-Vase_2, SY-table-cloth03 | 2.4 x 1.2 | 2 |

Goods rest on flat tops measured on the meshes: Quaternius stall and cart 0.83 m, Avramania stall 0.96 m, cafe counter 1.15 m, cafe long table 0.75 m. Readiness: READY (S03, S04, S05 depend on the cafe and Avramania packs).

## Assembly notes: junctions checked

| Junction | State |
|---|---|
| Exchange Hall tower and main roof | **Fixed.** Tower walls begin at level 4, above the roof surface; the roof passes into the tower's dark core. No eave is cut |
| Exchange Hall wings and main block | Wing ridges (10.9 m) sit below the main roof's gable overhang; wing roofs run 1 m into the main gable wall. Intended telescoping; hidden inside the wall |
| Podium | **Fixed.** One brick deck; stone skirt on all four sides including behind the stair flanks |
| Tea house balcony | **Fixed.** Deck, three rails and four posts form a complete veranda |
| Dormers | Seated so the dormer ridge meets the slope; the cheeks sink into the tiles by a few centimetres |
| Chimneys | Shafts pass through the slope without a flashing piece. Acceptable at gameplay distance; noted |
| Gable infill and roof | Infill sits inside the roof's barge boards; small overlap at the verge by design of the kit |
| Stone piers and wall trims | Timber wall trims run into the stone pier at corners (2-3 cm overlap) |
| Timber canopy and shutters | Open shutters stand under the canopy; no intersection |
| Gate lodge roofs | 2.7 m apart across the lane; clear of B04 and B07 by 1.3 m and 1.5 m |
| Exchange Hall porch and main roof (P1.2) | Porch roof is a full 6 x 6 roof centred 1.4 m behind the porch, so its ridge runs 3 m into the main slope and is buried. The hidden half passes through the upper wall into the dark core. No open roof end |
| Jetty and roof (P1.2) | 6 x 10 roof shifted 1 m forward covers the jetty; gable infill moved to the jetty face; side cheeks are the kit's own two-storey pieces with brackets |
| Jetty windows (P1.2) | Window inserts are mounted on the plain jetty face (the overhang module has no opening). Looks correct in Blender; check for flicker in the engine |
| Timber canopy and trade sign | Signs are mounted above or beside canopies; none intersects |
