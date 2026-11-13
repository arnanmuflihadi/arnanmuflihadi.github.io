# 07 - Archetype schedule (P1.3)

Sheet: [archetype-assembly-sheet.png](visuals/archetype-assembly-sheet.png). Ten of the eleven assemblies are those of P1.2, unchanged; their module lists,
facade strings, collision notes and acceptance criteria are in `../p1/08-archetype-specifications.md`. One variant is new.

| ID | Purpose | Instances | Used by | Footprint (m) | Height (m) | Module instances / ids | Triangles each | Verified sources | Readiness |
|---|---|---|---|---|---|---|---|---|---|
| A01 | Exchange Hall: civic landmark | 1 | B01 | 28 x 16 | 22.8 | 348 / 28 | 87,904 | custom (seal / sign), Quaternius Fantasy Props, Quaternius Medieval Village | READY |
| A02 | Covered market hall (two dressing kits) | 2 | B02, B03 | 8 x 12 | 9.0 | 61 / 27 | 42,176 | Avramania, custom (seal / sign), Quaternius Fantasy Props, Quaternius Medieval Village, Syntaxes of Play Medieval Cafe | CONDITIONAL |
| A03 | Jettied two-storey shophouse, gable to street | 2 | B07, B09 | 6 x 8 | 10.9 | 59 / 21 | 19,238 | Avramania, custom (seal / sign), Quaternius Fantasy Props, Quaternius Medieval Village | CONDITIONAL |
| A03b | Two-storey shophouse, eaves to street | 2 | B05, E03 | 8 x 6 | 10.9 | 63 / 22 | 19,454 | Avramania, custom (seal / sign), Quaternius Fantasy Props, Quaternius Medieval Village | READY |
| A03c | Shallow two-storey merchant house (8 x 4 m) for plots that back onto a lane - **new in P1.3** | 1 | E02 | 8 x 4 | 9.7 | 56 / 21 | 16,288 | Avramania, custom (seal / sign), Quaternius Fantasy Props, Quaternius Medieval Village | READY |
| A04 | Single-storey shop, gable to street | 2 | B06, B14 | 4 x 6 | 6.7 | 25 / 14 | 8,200 | custom (seal / sign), Quaternius Fantasy Props, Quaternius Medieval Village | READY |
| A04b | Single-storey shop, eaves to street | 4 | B08, B11, E01, E05 | 6 x 4 | 6.7 | 25 / 13 | 8,134 | custom (seal / sign), Quaternius Fantasy Props, Quaternius Medieval Village | READY |
| A05 | Stone-based corner building with two fronts | 4 | B04, B15, B16, E04 | 8 x 8 | 12.0 | 68 / 21 | 37,334 | Avramania, custom (seal / sign), Quaternius Fantasy Props, Quaternius Medieval Village | READY |
| A06 | Stone workshop | 2 | B10, B12 | 6 x 6 | 7.9 | 32 / 16 | 30,692 | custom (seal / sign), Quaternius Fantasy Props, Quaternius Medieval Village | READY |
| A07 | Guild warehouse | 1 | B13 | 8 x 14 | 12.0 | 80 / 22 | 42,321 | custom (seal / sign), Quaternius Fantasy Props, Quaternius Medieval Village | READY |
| A08 | Tea house with veranda | 1 | B17 | 6 x 6 | 10.9 | 65 / 21 | 20,976 | Avramania, custom (seal / sign), Quaternius Fantasy Props, Quaternius Medieval Village | CONDITIONAL |

Instances changed from P1.2: A03 3 to 2 (B16 re-typed), A03b 1 to 2, A03c 0 to 1, A04 2 to 2, A04b 2 to 4, A05 2 to 4. Total 22.

## A03c - Shallow Merchant House (new variant, READY)

| Field | Value |
|---|---|
| Why it exists | A two-storey house for a plot that backs onto a lane: 8 m of frontage but only 4 m deep, so its rear eave stays clear of the lane's follow-camera line. The 6 m deep A03b in the same position shortened the camera at the start of the warehouse lane to 1.8 m |
| Footprint, height | 8 x 4 m, 9.7 m; measured bounds 10.53 x 6.46 x 11.25 m |
| Assembly | Same wall, window, door, shutter and post modules as A03b on a 4 x 1 bay grid of two storeys; roof `MV-Roof_RoundTiles_4x8` with the ridge along the frontage; gables `MV-Roof_Front_Brick4`; timber canopy, one trade sign, lantern, two flower boxes, chimney |
| Facades | front `FDFG` / `RRGR`; sides `PP` / `PT`; back `PPPP` / `PRRP` |
| Modules | `MV-Wall_Plaster_Straight` x12, `MV-Corner_ExteriorWide_Wood` x8, `MV-Wall_Plaster_Window_Wide_Round` x5, `MV-Window_Wide_Round1` x5, `AV-mdvl_village_window_box_01` x2, `MV-Roof_Front_Brick4` x2, `MV-Roof_Wooden_2x1_Center` x2, `MV-Wall_Plaster_Window_Thin_Round` x2, `MV-Wall_Plaster_Window_Wide_Flat` x2, `MV-Wall_Plaster_WoodGrid` x2, `MV-WindowShutters_Wide_Flat_Open` x2, `MV-Window_Thin_Round1` x2, `MV-Window_Wide_Flat1` x2, `CUS-Sign_Scroll_wood` x1, `FP-Lantern_Wall` x1, `MV-Door_1_Flat` x1, `MV-Prop_Chimney2` x1, `MV-Roof_RoundTiles_4x8` x1, `MV-Roof_Wooden_2x1_L` x1, `MV-Roof_Wooden_2x1_R` x1, `MV-Wall_Plaster_Door_Flat` x1 |
| New downloads | None. `MV-Roof_RoundTiles_4x8` was verified in P1.0 and is first used here |
| Custom | Trade sign x1 (as every shop) |
| Collision | One box 8 x 4 x 6 |
| Triangles | 16,288 unoptimised |

## Dependencies carried over from P1.2

READY: A01, A03b, A03c, A04, A04b, A05, A06, A07, gateway, market cross. CONDITIONAL: A02 (cafe-pack materials re-linked on export, Avramania goods), A03 (windows mounted on the jetty face), A08 (Avramania sign and flower boxes). BLOCKED: none.
