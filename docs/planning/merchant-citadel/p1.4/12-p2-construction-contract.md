# 12 - P2 construction contract for the P1.4 design (not started; needs explicit authorisation)

P2 builds the archetypes as reusable assemblies and proves one in the real Three.js scene. It does not assemble the town (P3) or build terrain (P4).
This replaces `../p1.3/10-p2-construction-contract.md` where they differ.

## Roster

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

Structures: split gateway (READY), market cross (READY), civic terrace (READY), two gate arches (READY). Free-stall kits as P1.2.

**READY** 8 of 16; **CONDITIONAL** 8 (each with one named dependency above); **BLOCKED** none.
The conditional items share three dependencies: the custom cloth awning (new in P1.4), the cafe-pack material conversion, and owner acceptance of Avramania.

## To author rather than assemble

Seal; trade sign with seven pictograms; **cloth awning bay in three colourways; pennant line; paving seal**; cloth and dark-roof material instances; graded textures; a purpose-made lamp post; a solid terrace mass.

## Sequence

1. Scale scene: 2 m grid, 3 m storey, 1.9 m explorer.
2. Materials: bake the colour grade; merge duplicates only where node set-ups match; material instances; one palette texture for the custom flat colours. Convert the used cafe-pack models to GLB once.
3. Shared wall, window, door, roof and signage sub-assemblies; the awning bay.
4. A04, A04b. 5. A03b, A03c, A03. 6. A05, **A11 / A11m**, A06.
7. A02, **A10 rows**, gateway, market cross. 8. **Terrace**, A01. 9. A07, A08, **A09**.
10. Substitutions of 10; join static meshes per building by material.
11. One archetype exported and loaded in the real scene; measurements recorded; stop for approval.

## Measurable verification steps

| Step | Measure | Pass condition (proposed) |
|---|---|---|
| 1 | Triangles per archetype GLB | At or below an agreed budget |
| 2 | Distinct materials and textures | At or below 59; no texture above 2048 px |
| 3 | One archetype in the real page: `renderer.info.render.triangles` and `.calls` at three fixed cameras against the island-1 baseline | Recorded |
| 4 | Scale and orientation: door 2.1 m, storey 3.0 m, +y up | Within 1 cm |
| 5 | Controller on both flights of steps, the 0.18 m deck-edge riser, a hall arch and a 4 m lane | No sticking |
| 6 | Follow camera at the places listed in 09, with awnings and pennants in or out of the collision set | Recorded; decision on the set |
| 7 | Double-sided cloth renders correctly from below | Visual check |
| 8 | Frame time over a fixed 60 s walk at 1280 x 720 | Recorded with hardware |

**Browser performance has not been validated.**
