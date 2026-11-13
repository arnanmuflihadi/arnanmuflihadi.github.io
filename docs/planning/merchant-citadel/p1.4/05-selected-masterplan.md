# 05 - Selected measured masterplan (P1.4, alternative D)

Drawing: [OUTPUT G](visuals/output-g-orthographic-masterplan.png). Data: `layouts_p14.py`, `town_data.py`. Metres; origin = centre of the arrival court; plan x = east, n = north; project (x, y, z) = (x, elevation, -n).
`rotation_y`: 0 = front faces south, 90 = east, -90 = west; any angle is allowed, and footprints are oriented rectangles.

Developed envelope: x -30.5..42 (72.5 m), z -90.0..8 (98 m). P1.3 was 70.5 x 98 m; the inn adds 2 m on the west.

**24 permanent buildings, 14 building archetypes in use, 4 awning rows (16 bays), 4 free stalls, split gateway, market cross, civic terrace.**

## Levels

| Surface | Elevation | Reached by |
|---|---|---|
| Streets, lanes, bazaar, lookout | y = 0 | - |
| Civic terrace, x -14..14, z -74..-62 | y = +1.0 | Steps 12 m wide at z = -60..-62 (five risers, modules `Stairs_Exterior_Straight_L / _Center / _R`) |
| Exchange Hall podium | y = +2.0 | Hall steps 10 m wide from the terrace (unchanged modules) |

## Public spaces and street widths

| Space | Size | Note |
|---|---|---|
| Merchant street | 10 m between facades, 8 m clear | unchanged |
| Market street in the bazaar | 10.1 m between awning-row fronts; 2.8 m cross-passage; 2.45 m back lanes between rows and halls | new |
| Bazaar plaza | 44 x 26 m | unchanged outline |
| Civic terrace | 28 x 12 m, +1.0 m | raised |
| Lanes, cross street, tea lane | 4 m | unchanged |
| Pocket court, workyard, service court, lookout terrace | 8 x 6, 6 x 4, 14 x 8, 12 x 10 m | unchanged |

## Building positions

| ID | Archetype | Name | Position (x, y, z) | rotation_y | Measured envelope (m) | Change since P1.3 |
|---|---|---|---|---|---|---|
| B01 | A01 | Exchange Hall on the civic terrace | (0, 2.0, -84) | 0 | 28.09 x 18.0 | kept |
| B02 | A02 | Market Hall West (provisions) | (-13, 0.0, -50) | 0 | 9.95 x 15.42 | kept |
| B03 | A02 | Market Hall East (crafts and general trade) | (13, 0.0, -50) | 0 | 9.95 x 15.42 | kept |
| B04 | A11 | Junction Tower House (money changer) | (-9, 0.0, -14) | 90 | 10.8 x 10.8 | re-typed A05 to A11 |
| B05 | A03b | Shophouse W1, eaves to street (baker) | (-8, 0.0, -26) | 90 | 8.64 x 9.68 | kept |
| B06 | A04 | Compact Shop W2 (dry goods) | (-8, 0.0, -34.4) | 90 | 8.32 x 5.51 | kept |
| B07 | A03 | Jettied Shophouse E1 (map and book seller) | (9, 0.0, -13) | -90 | 11.85 x 8.25 | kept |
| B08 | A04b | Compact Shop E2, eaves to street (potter) | (7, 0.0, -25) | -90 | 6.29 x 7.59 | kept |
| B09 | A03 | Jettied Shophouse E3 (provisioner) | (9, 0.0, -33.6) | -90 | 11.85 x 8.25 | kept |
| B10 | A06 | Workshop South (smith) | (-21.5, 0.0, -11) | 84 | 9.07 x 8.92 | turned 90 to 84 |
| B11 | A04b | Lane Shop closing the cross street (potter's yard) | (-20.5, 0.0, -20) | 90 | 6.29 x 7.59 | kept |
| B12 | A06 | Workshop North (joiner) | (-21.5, 0.0, -29) | 96 | 9.28 x 9.12 | turned 90 to 96 |
| B13 | A07 | Guild Warehouse | (25.5, 0.0, -12) | -90 | 16.23 x 12.96 | kept |
| B14 | A04 | Registry Office (guild), on the bazaar edge | (25.5, 0.0, -40.2) | -90 | 8.32 x 5.51 | moved 0.8 m |
| B15 | A11 | Terrace Tower House West (assay office, guild) | (-18, 0.0, -67) | 0 | 10.8 x 10.8 | re-typed A05 to A11 |
| B16 | A11m | Terrace Tower House East (chart maker) | (18, 0.0, -67) | 0 | 10.8 x 10.8 | re-typed A05 to A11m; turned -90 to 0 |
| B17 | A08 | Tea House, turned to the view | (36.5, 0.0, -67.5) | 18 | 9.96 x 10.61 | moved 0.7 m; turned 0 to 18 |
| E01 | A04b | South Gateway Shop (traveller's outfitter) | (-12, 0.0, 1) | 78 | 7.48 x 8.47 | turned 90 to 78 |
| E02 | A03c | Arrival Corner Merchant House (carrier's office) | (12, 0.0, 2) | -90 | 6.28 x 9.68 | kept |
| E03 | A09 | Merchants' Inn (Penginapan Saudagar) | (-26.5, 0.0, -45) | 90 | 11.08 x 11.86 | re-typed A03b to A09; moved 1.4 m |
| E04 | A05 | Merchant Counting House (guild) | (22.5, 0.0, -28) | -90 | 10.46 x 10.36 | kept |
| E05 | A04b | Tea Route Merchant House (tea and spice seller) | (25.5, 0.0, -53.5) | 180 | 7.59 x 6.29 | kept |
| E06 | A04 | Bazaar Perimeter Shop East (cloth seller) | (25.8, 0.0, -46.9) | -82 | 8.87 x 6.41 | new |
| E07 | A04b | Bazaar Perimeter Shop North-West (potter's outlet) | (-24.8, 0.0, -55.6) | 98 | 7.12 x 8.21 | new |

11 of 24 are new, re-typed, turned or moved against P1.3; 13 are unchanged. Nothing was deleted. Full figures: [06-building-schedule.csv](06-building-schedule.csv).

## Key sightlines (drawn on the plan)

Arrival court, street junction and bazaar entrance to the hall tower: all clear in the massing test (04). Tower visible from 8 of 15 tested points: N01, N02, N03, N04, N27, N06, N07, N10.
