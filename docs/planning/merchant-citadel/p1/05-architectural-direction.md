# 05 - Architectural style specification (P1.2)

## Language

Asset-native stylised merchant architecture from one kit, the Quaternius Medieval Village MegaKit: cream plaster, exposed timber frame,
stone ground floors on the heavier buildings, terracotta tile roofs. Warm and slightly whimsical; not a castle and not historically exact.
The merchant character comes from function: shopfronts, signs, halls, a warehouse, an exchange.

**Rule for mixing publishers:** architecture, roofs, paving and street furniture come from Quaternius only. Other publishers supply goods and
furniture below about 2.3 m, where a different shading style is not read as a different building.

## Palette and colour grade

The brief's palette is reached by grading the downloaded materials, not by repainting textures. Average texture colour was measured for each
material and a hue / saturation / value correction derived.

| Surface and material | Measured average | Palette target | Grade applied |
|---|---|---|---|
| Roof tiles `MI_RoundTiles` | #B35430 | #BB6345 | hue +0.012, saturation x0.90, value x0.94 |
| Civic roofs `MI_RoundTiles@dark` | - | #9F523D | further saturation x0.84, value x0.72 |
| Timber `MI_WoodTrim`, `_Wear` | #896A4A | #75543B | saturation x0.82, value x0.76 |
| Plaster `MI_Plaster` | #B29C80 | #E8D9BC | saturation x0.80, value x1.14 |
| Stone walls `MI_UnevenBrick` | #867966 | #858078 | saturation x0.50 |
| Paving `MI_Brick` | #918376 | #A69E8E | saturation x0.70, value x1.10 |
| Foliage `Leaves_NormalTree`, `Leaves` | #587B00 | muted natural green | saturation x0.70-0.75, value x0.90 |

| Accent | Colour | Carrier |
|---|---|---|
| Merchant burgundy | `#8C3E45` | Cloth variant; seal field; guild sign boards |
| Trading blue | `#345D80` | Cloth variant; heart of the seal |
| Civic gold | `#C8A15A` | Seal; sign pictograms |

Roofs stay in one terracotta family: shops at the main value, guild and civic roofs one step darker. No building has its own colour.

## Architectural identity contract

| Element | Rule | Verified modules |
|---|---|---|
| Shop, two storeys, gable to street | Upper floor **jettied 1.12 m** over the shopfront on timber brackets; flower boxes under the upper windows; one dormer and a chimney | `Overhang_Plaster_Short`, `Overhang_Side_Plaster_Short_L/R`, `Roof_RoundTiles_6x10` |
| Shop, two storeys, eaves to street | Timber shopfront canopy along the whole front; two dormers | `Roof_Wooden_2x1_L / _Center / _R` |
| Compact shop | Canopy on the gable-fronted form; shutters and a wall vine on the eaves-fronted form | as above, `Prop_Vine1` |
| Corner building, warehouse, workshop | Stone ground floor, stone piers below, timber posts above | `Wall_UnevenBrick_*`, `Corner_Exterior_Brick` |
| Market hall | Open timber arcade under a dark roof; seal on both gables; four cloth banners | `Wall_Arch`, `Roof_RoundTiles_8x12@dark` |
| Exchange Hall | Stone base across a 26 m front, wings, **gabled entrance porch on stone piers**, four burgundy banners, tower through the ridge, dark roofs, podium | 08, A01 |
| Roofscape | Three orientations to the street, 10 dormers, chimneys, the porch gable and two roof values | `Roof_Dormer_RoundTile`, `Prop_Chimney*` |
| Paving | Cobble for streets and plaza; dressed brick for the guild way, halls and court; red brick for the artisan lane and terrace; packed earth in the back courts (terrain treatment) | `Floor_UnevenBrick`, `Floor_Brick`, `Floor_RedBrick` |

## Signage and banner system

| Class | Carrier | Model | Mounting rule |
|---|---|---|---|
| Shop or workshop | Timber board with a gold pictogram | `CUS-Sign_<glyph>_wood` (custom) | Exactly one per shop, on an iron arm at right angles to the wall; underside 2.1 m or more above paving |
| Guild office | Same board with a burgundy field | `CUS-Sign_<glyph>_burgundy` (custom) | Registry and assay office only |
| Tea house | Cup sign plus a small hanging inn sign | `CUS-Sign_Cup_wood`, `AV-mdvl_village_sign_inn_01` | Side wall; under the veranda |
| Guild cloth | Burgundy | `FP-Banner_2_Cloth@burgundy`, `FP-Banner_1@burgundy`, `FP-Banner_2@burgundy` | Hall front between upper windows; east market hall corners; warehouse-lane standards |
| Market cloth | Blue | `FP-Banner_1@blue` | West market hall corners |
| Guild seal | Gold, burgundy, blue | `CUS-Seal_NiagaAwan` (custom) | Guild-run structures and the market cross only; 0.8 to 1.9 m across |

Long cloth banners no longer serve as shop signs. Lowest measured hanging edge over any walkable surface: **2.18 m** (09).

## Materials

53 distinct materials are in the town (P1.1: 29). The increase is 16 textured materials from the cafe pack, 1 palette material from Avramania,
7 flat custom materials and the cloth and roof variants. The cafe pack's materials carry normal and roughness maps; P2 should atlas them to a few (12).

## Lighting used for the views (presentation, not an asset)

Warm afternoon sun about 38 degrees above the horizon from the south-west, a blue-to-warm sky gradient for fill, soft shadows, and the
Khronos PBR Neutral view transform (the tone mapping three.js offers as `NeutralToneMapping`). Shadows fall across half the street, so
both lit and shaded facades are visible; nothing is hidden in darkness. The game's own lighting will differ and must be checked in P2.

Principal compromise, unchanged: this is a European half-timber language with its own guild identity, not the Indonesian-tropical look of the first island. That is the owner's stated direction.
