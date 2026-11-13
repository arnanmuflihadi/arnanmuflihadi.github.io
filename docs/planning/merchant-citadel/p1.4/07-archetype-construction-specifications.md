# 07 - Archetype and construction specifications (P1.4)

Sheet with renders: [new-asset-evidence-sheet.png](visuals/new-asset-evidence-sheet.png). Module lists, facade strings and collision notes of the unchanged archetypes are in `../p1/08` and `../p1.3/07`.
The data that builds every assembly is `blender-inspection/town_data.py`; exact module ids and counts per assembly are in `asset-evidence/usage-and-triangles.json`.

| ID | Purpose | Instances | Used by | Footprint (m) | Height (m) | Module instances / ids | Triangles each | Sources | Readiness |
|---|---|---|---|---|---|---|---|---|---|
| A01 | Exchange Hall: taller tower with the seal on four faces, dormers, porch; stands on the terrace | 1 | B01 | 28 x 16 | 25.8 | 394 / 29 | 91,784 | custom, Q. Fantasy Props, Q. Medieval Village | READY |
| A02 | Covered market hall (two dressing kits) | 2 | B02, B03 | 8 x 12 | 9.0 | 61 / 27 | 42,176 | Avramania, custom, Q. Fantasy Props, Q. Medieval Village, SoP Medieval Cafe | CONDITIONAL (cafe-pack materials re-linked on export; Avramania goods) |
| A03 | Jettied two-storey shophouse | 2 | B07, B09 | 6 x 8 | 10.9 | 59 / 21 | 19,238 | Avramania, custom, Q. Fantasy Props, Q. Medieval Village | CONDITIONAL (windows mounted on the jetty face) |
| A03b | Two-storey shophouse, eaves to street | 1 | B05 | 8 x 6 | 10.9 | 63 / 22 | 19,454 | Avramania, custom, Q. Fantasy Props, Q. Medieval Village | READY |
| A03c | Shallow two-storey merchant house | 1 | E02 | 8 x 4 | 9.7 | 56 / 21 | 16,288 | Avramania, custom, Q. Fantasy Props, Q. Medieval Village | READY |
| A04 | Single-storey shop with a cloth awning | 3 | B06, B14, E06 | 4 x 6 | 6.7 | 25 / 13 | 7,980 | custom, Q. Fantasy Props, Q. Medieval Village | CONDITIONAL (custom cloth awning to author) |
| A04b | Single-storey shop, eaves to street, cloth awning | 5 | B08, B11, E01, E05, E07 | 6 x 4 | 6.7 | 28 / 14 | 8,278 | custom, Q. Fantasy Props, Q. Medieval Village | CONDITIONAL (custom cloth awning to author) |
| A05 | Stone-based corner building with two fronts | 1 | E04 | 8 x 8 | 12.0 | 68 / 21 | 37,334 | Avramania, custom, Q. Fantasy Props, Q. Medieval Village | READY |
| A06 | Stone workshop | 2 | B10, B12 | 6 x 6 | 7.9 | 32 / 16 | 30,692 | custom, Q. Fantasy Props, Q. Medieval Village | READY |
| A07 | Guild warehouse | 1 | B13 | 8 x 14 | 12.0 | 80 / 22 | 42,321 | custom, Q. Fantasy Props, Q. Medieval Village | READY |
| A08 | Tea house with veranda | 1 | B17 | 6 x 6 | 10.9 | 65 / 21 | 20,976 | Avramania, custom, Q. Fantasy Props, Q. Medieval Village | CONDITIONAL (Avramania sign and flower boxes) |
| A09 | **New.** Merchants' inn: 10 x 8 m, stone ground floor, balcony on posts, two dormers, two chimneys | 1 | E03 | 10 x 8 | 12.0 | 89 / 29 | 46,435 | Avramania, custom, Q. Fantasy Props, Q. Medieval Village, SoP Medieval Cafe | CONDITIONAL (Avramania inn sign and flower boxes) |
| A11 | **New.** Corner tower house: A05 body with a three-storey corner turret standing 1 m proud of both fronts | 2 | B04, B15 | 8 x 8 | 15.8 | 99 / 22 | 49,370 | Avramania, custom, Q. Fantasy Props, Q. Medieval Village | READY |
| A11m | **New.** Mirror of A11 (turret on the left) | 1 | B16 | 8 x 8 | 15.8 | 99 / 22 | 49,370 | Avramania, custom, Q. Fantasy Props, Q. Medieval Village | READY |
| A10p | **New.** Market awning row, provisions (blue) | 2 | R01, R02 | 8 x 2 | 3.3 | 22 / 13 | 11,592 | Avramania, custom, Q. Fantasy Props, Q. Medieval Village, SoP Medieval Cafe | CONDITIONAL (custom cloth awning; cafe counters; stretched posts) |
| A10c | **New.** Market awning row, crafts (burgundy) | 2 | R03, R04 | 8 x 2 | 3.3 | 22 / 13 | 7,992 | custom, Q. Fantasy Props, Q. Medieval Village, SoP Medieval Cafe | CONDITIONAL (custom cloth awning; cafe counters; stretched posts) |

## New and changed assemblies

| Assembly | Construction | Collision | Acceptance |
|---|---|---|---|
| **A01 Exchange Hall v2** | As P1.2, plus: tower walls on levels 4-6 (was 4-5), middle level plain with a 2.3 m seal on each face, top level with round windows; two dormers on the front slope; a plinth row of stair-skirt panels 1 m below the podium on the sides and back, because the hall now stands on the terrace | Boxes as before, raised 1 m; plinth 28 x 16 x 2 | Tower reads from the gate; no gap under the podium at the sides and back |
| **A09 Merchants' Inn** | Body 10 x 8, two storeys, stone ground floor (`srors` / `RORGR`), roof `Roof_RoundTiles_8x10` with the ridge along the frontage; balcony of three dark-wood floor tiles and five rail pieces on four posts; two dormers, two chimneys; cup sign, hanging inn sign, two flower boxes, two lanterns | One box 10 x 8 x 6; four post proxies | Balcony posts clear the side lane by 1.4 m; nothing below 2.1 m over paving |
| **A11 / A11m Corner Tower House** | A05 body (8 x 8, two storeys, stone ground floor) with one corner post omitted; turret 4 x 4, three storeys (`Ss` / `PR` / `RR` on the two outer faces), centred 3 m out on both axes so it stands 1 m proud of both fronts; roof `Roof_Tower_RoundTiles`. A11m is the mirror | One box 8 x 8 x 6 plus one 4 x 4 x 9 | Turret roof rises clear of the body roof; projection 1 m, leaving 3 m of the cross street at the junction |
| **A10p / A10c Market Awning Row** | 8 m long: three front posts (2.46 m) and three back posts (3.2 m), all `Corner_Exterior_Wood` scaled in height; four custom awning bays fixed to the back rail; two cafe counters and one table beneath; goods of one trade | Six post proxies; counters as two boxes | Customers' side clear; front edge of the cloth 2.3 m above paving; cross-passage 2.8 m between rows |
| **Civic terrace** | 84 brick tiles at +1.0 m; six stair modules; skirt panels on the front (not behind the steps) and sides; eight cross-braced balustrade pieces. Hollow in the blockout with a temporary dark fill | One box 28 x 12 x 1; steps as five 0.2 m treads or a ramp proxy | Top riser is the deck edge (0.18 m); no visible void |
| **A04, A04b** | Timber canopy replaced by two or three custom cloth awning bays | unchanged | Valance 2.18 m above paving |
| **Gate arches** | One `Wall_Arch` in each of the two closed street gaps | Two post proxies | Not a route |

## Custom elements: construction strategy for P2

| Element | Blockout | P2 |
|---|---|---|
| Cloth awning bay | 48 triangles, flat colours, two-sided | One mesh with a woven cloth texture and vertex-coloured stripes; three colourways as material instances |
| Pennant line | 42-76 triangles | One instanced pennant along a curve, or keep as a single mesh per length |
| Paving seal | 266 triangles, 3 cm proud | A decal or a texture on one paving plane |
| Seal, trade signs | as P1.2 | as P1.2 |
