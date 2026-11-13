# 09 - Spatial and camera validation (P1.4 selected layout)

Method as P1.1-P1.3 (`validate_envelopes.py`): the assembled Blender scene, 968,826 triangles, ray casts and nearest-surface queries with constants copied from the project's controller and camera files.
The production controller and camera were not modified or run. Raw results: [asset-evidence/spatial-validation-actual-geometry.json](asset-evidence/spatial-validation-actual-geometry.json).

| Check | Result |
|---|---|
| Nominal: oriented footprint overlaps, clear corridors, paved door approaches, stalls and rows on paving, connectivity | PASS |
| Roof and envelope gaps | 0 failing; 7 narrow (0.3-1.0 m) |
| Walking edges on real geometry | **42 of 42 built edges pass** |
| Steps | Terrace steps: largest step on N06-N07 0.22 m; hall steps: 5 risers, largest 0.223 m (limit 0.42 m) |
| Hanging objects over paving (lanterns, banners, signs, awnings, pennants, flower boxes: 143 measured) | None below 2.1 m; lowest 2.18 m (`CUS-Awning_burgundy`) |
| Market hall arch | 1.67 m wide, 2.74 m high (unchanged) |
| Follow camera | 35 of 84 directions fully clear; 79% of all samples clear |

Walking graph: 35 nodes, 43 edges, 9 independent loops, 434.5 m built. Primary route 76.8 m. (P1.3: 37 nodes, 47 edges, 11 loops. The terrace has one flight of steps, so the two court-side loops of P1.3 are gone.)

## Defects found by validation during P1.4 and corrected

Roofs of the terrace tower house and the north-west shop overlapping by 0.02 m; tea-route shop and cloth seller 0.14 m apart; a stone skirt panel behind the terrace steps blocking the top riser;
a lane standard on the path to the workyard. All were corrected in the layout and re-tested. A void under the terrace deck, visible behind the top step, was closed with a temporary fill.

## Narrow gaps (not failures)

| A | B | Gap (m) | Status |
|---|---|---|---|
| E03 | E07 | 0.48 | NARROW |
| E05 | E06 | 0.64 | NARROW |
| B08 | B09 | 0.69 | NARROW |
| B14 | E06 | 0.73 | NARROW |
| B10 | B11 | 0.75 | NARROW |
| B11 | B12 | 0.75 | NARROW |
| B05 | B06 | 0.79 | NARROW |

## Every edge

| Edge | Type | Length (m) | Unpaved samples | Largest step (m) | Least headroom (m) | Nearest obstacle at 1 m (m) | Result |
|---|---|---|---|---|---|---|---|
| N20-N01 | reserved link | 16.0 | 32 | 0.03 | open sky | 3.02 | RESERVED (not built in P1-P3) |
| N01-N02 | primary | 5.0 | 0 | 0.0 | open sky | 1.86 | PASS |
| N02-N03 | primary | 15.0 | 0 | 0.01 | open sky | 1.86 | PASS |
| N03-N04 | primary | 17.5 | 0 | 0.01 | open sky | 1.89 | PASS |
| N04-N05 | primary | 8.0 | 0 | 0.0 | open sky | 1.94 | PASS |
| N05-N29 | primary | 4.4 | 0 | 0.0 | open sky | 0.74 | PASS |
| N29-N27 | primary | 4.4 | 0 | 0.0 | open sky | 0.4 | PASS |
| N05-N30 | primary | 4.4 | 0 | 0.0 | open sky | 0.6 | PASS |
| N30-N27 | primary | 4.4 | 0 | 0.0 | open sky | 0.51 | PASS |
| N27-N06 | primary | 6.9 | 0 | 0.0 | open sky | 1.37 | PASS |
| N06-N07 | primary | 7.6 | 0 | 0.22 | open sky | 1.03 | PASS |
| N07-N08 | primary, stairs | 8.0 | 0 | 0.22 | open sky | 0.79 | PASS |
| N01-N35 | secondary | 9.8 | 0 | 0.0 | open sky | 0.95 | PASS |
| N35-N09 | secondary | 7.0 | 0 | 0.0 | open sky | 1.5 | PASS |
| N09-N10 | secondary | 16.0 | 0 | 0.0 | open sky | 0.76 | PASS |
| N10-N11 | secondary | 18.5 | 0 | 0.0 | open sky | 0.42 | PASS |
| N11-N04 | secondary | 16.0 | 0 | 0.0 | open sky | 1.14 | PASS |
| N10-N03 | secondary | 16.0 | 0 | 0.01 | open sky | 0.58 | PASS |
| N01-N36 | service | 9.8 | 0 | 0.0 | open sky | 0.96 | PASS |
| N36-N12 | service | 7.0 | 0 | 0.0 | open sky | 1.77 | PASS |
| N12-N13 | service | 16.0 | 0 | 0.0 | open sky | 1.46 | PASS |
| N13-N14 | service | 18.5 | 0 | 0.0 | open sky | 1.81 | PASS |
| N14-N04 | service | 16.0 | 0 | 0.0 | 5.54 | 0.94 | PASS |
| N03-N13 | service | 16.0 | 0 | 0.01 | open sky | 1.77 | PASS |
| N11-N18 | market | 5.7 | 0 | 0.0 | open sky | 1.59 | PASS |
| N18-N31 | market | 6.5 | 0 | 0.0 | 2.86 | 0.83 | PASS |
| N31-N30 | market | 9.3 | 0 | 0.0 | 2.27 | 0.83 | PASS |
| N14-N19 | market | 5.7 | 0 | 0.0 | open sky | 1.01 | PASS |
| N19-N32 | market | 6.5 | 0 | 0.0 | 2.86 | 0.83 | PASS |
| N32-N29 | market | 9.3 | 0 | 0.0 | 2.27 | 0.83 | PASS |
| N11-N38 | secondary | 4.1 | 0 | 0.0 | open sky | 1.62 | PASS |
| N38-N23 | secondary | 17.6 | 0 | 0.0 | open sky | 1.28 | PASS |
| N14-N39 | secondary | 4.1 | 0 | 0.0 | open sky | 2.13 | PASS |
| N39-N24 | secondary | 17.6 | 0 | 0.0 | open sky | 1.86 | PASS |
| N24-N41 | scenic | 6.8 | 0 | 0.0 | open sky | 1.54 | PASS |
| N41-N16 | scenic | 10.0 | 0 | 0.0 | open sky | 1.33 | PASS |
| N16-N17 | scenic | 5.8 | 0 | 0.0 | 2.88 | 0.34 | PASS |
| N13-N33 | service | 9.0 | 0 | 0.0 | open sky | 2.24 | PASS |
| N11-N40 | secondary | 6.7 | 0 | 0.0 | open sky | 0.92 | PASS |
| N23-N06 | secondary | 19.2 | 0 | 0.0 | open sky | 0.62 | PASS |
| N24-N06 | secondary | 19.2 | 0 | 0.0 | open sky | 0.62 | PASS |
| N07-N21 | secondary | 9.6 | 0 | 0.02 | open sky | 1.11 | PASS |
| N07-N22 | secondary | 9.6 | 0 | 0.02 | open sky | 1.11 | PASS |

## Follow camera

| | P1.3 | P1.4 |
|---|---|---|
| Travel directions tested | 92 | 84 |
| Fully clear | 48 (52%) | 35 (41%) |
| Share of all samples with a clear camera line | 79% | 79% |
| Shortest camera distance anywhere | 1.56 m | 1.5 m |

**Stated plainly:** fewer travel directions are fully clear than in P1.3, although the share of the walked distance with a clear camera is the same. More things now stand near the routes (awning rows, pennant lines, turrets), so more
directions have at least one obstructed sample. Thin objects such as pennant lines are counted here and may not be in the game's camera collision set.

Primary axis, walking towards the hall:

| Travel | Samples clear | Shortest camera distance (m) | Blocked by |
|---|---|---|---|
| N01->N02 | 100% | 12.96 | - |
| N02->N03 | 100% | 12.96 | - |
| N03->N04 | 100% | 12.96 | - |
| N04->N05 | 100% | 12.96 | - |
| N05->N29 | 100% | 12.96 | - |
| N29->N27 | 89% | 11.16 | DRESSING |
| N27->N06 | 57% | 3.43 | M01 |
| N06->N07 | 94% | 7.07 | DRESSING |
| N07->N08 | 100% | 12.96 | - |

Twelve shortest camera distances:

| Travel | Type | Samples clear | Shortest (m) | Blocked by | P1.3: clear / shortest |
|---|---|---|---|---|---|
| N38->N11 | secondary | 0% | 1.5 | E03 | 0% / 2.62 |
| N40->N11 | secondary | 50% | 2.32 | B12 | 36% / 2.25 |
| N31->N30 | market | 0% | 2.33 | B02 | 0% / 2.33 |
| N32->N29 | market | 0% | 2.33 | B03 | 0% / 2.33 |
| N17->N16 | scenic | 0% | 2.37 | B17 | 0% / 1.56 |
| N23->N06 | secondary | 69% | 2.4 | E07 | new edge |
| N10->N03 | secondary | 55% | 2.43 | B11 | 55% / 2.46 |
| N30->N31 | market | 42% | 2.53 | M01, B02 | 42% / 2.53 |
| N29->N32 | market | 42% | 2.53 | M01, B03 | 42% / 2.53 |
| N18->N11 | market | 0% | 3.08 | B02 | 0% / 3.08 |
| N19->N14 | market | 0% | 3.08 | B03 | 0% / 3.08 |
| N05->N04 | primary | 65% | 3.43 | M01 | 65% / 3.43 |

The test places the camera exactly behind the direction of travel, so corners and door exits are worst cases. The inn's balcony on the west side lane (1.5 m) is the new worst case and the first candidate for adjustment if it troubles the game camera.

## Outstanding in-engine validation

Camera at the listed corners with the game's collision set and smoothing; controller on both flights of steps and on the 0.18 m deck-edge riser; whether pennants, awnings and signs collide with the camera; frame time.
