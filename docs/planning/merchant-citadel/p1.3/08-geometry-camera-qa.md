# 08 - Actual geometry and camera QA (P1.3 selected layout)

Method unchanged from P1.1 and P1.2 (`validate_envelopes.py`): the assembled Blender scene, 915,314 triangles, tested with ray casts and nearest-surface queries
using constants copied from the project's controller and camera files. The production controller and camera were not modified or run.
Raw results: [asset-evidence/spatial-validation-actual-geometry.json](asset-evidence/spatial-validation-actual-geometry.json).

## Summary

| Check | Result |
|---|---|
| 1 Nominal footprints: overlaps, clear corridors, paved door approaches, stalls on paving, connectivity | PASS |
| 2 Measured envelopes (roofs, signs, props) | 24 structures measured; in 05 |
| 3 Building and roof overlap | 0 failing; 2 narrow (0.3-1.0 m) |
| 4-6 Routes, loops, paving continuity | 46 of 46 built edges pass |
| 7 Entrance clearances | Arch 1.67 m wide, 2.74 m high (unchanged); hall stairs five risers, largest 0.223 m; lowest hanging object over paving 2.18 m |
| 8 Follow camera | 48 of 92 travel directions fully clear; details below |
| 9 Hall visibility | Tower seal visible from 7 of 15 tested points (massing) |
| 10 Terrain support envelope | Recalculated in 09 |

## Roof gaps under 3 m

| A | B | Gap (m) | Status |
|---|---|---|---|
| B08 | B09 | 0.69 | NARROW |
| B05 | B06 | 0.79 | NARROW |
| B10 | B11 | 1.09 | OK |
| B11 | B12 | 1.09 | OK |
| B07 | G01 | 1.46 | OK |
| B04 | G01 | 1.6 | OK |
| B04 | B05 | 2.19 | OK |

Two pairs are narrow by design: the 2 m gated gaps on the merchant street. The first run had B08-B09 at 0.09 m (a clash in practice); B09 and B06 were each moved 0.4-0.6 m.
No pair overlaps.

## Follow camera

A ray from the look-at point (player +1.25 m) to the camera position (11.8 m behind, +6.6 m) for every edge, both directions.

| | P1.2 | P1.3 |
|---|---|---|
| Travel directions tested | 76 | 92 |
| Fully clear | 48 (63%) | 48 (52%) |
| Shortest camera distance anywhere | 0.8 m | 1.56 m |
| Primary axis, walking towards the hall | clear except 6 m past the market cross | clear except 6 m past the market cross |

**Stated plainly: the denser town has a smaller share of fully clear directions than P1.2 (52% against 63%).** More buildings near more corners means more
moments when a camera placed directly behind the player would be inside a roof. The shortest camera distance anywhere improved (0.8 m to 1.56 m), and so did the shortest distance at the three worst spots of P1.2. The clear share did not improve everywhere: at the two court corner doors it fell (37% and 31% to 20%), and under the hall roofs nothing changed:

| Travel | Situation | P1.2: clear share / shortest | P1.3: clear share / shortest |
|---|---|---|---|
| N17->N16 | leaving the tea-house veranda | 0% / 0.97 m | 0% / 1.56 m |
| N21->N07 | leaving the west court corner house (B15) | 37% / 0.82 m | 20% / 1.92 m |
| N22->N07 | leaving the east court corner house (B16) | 31% / 0.8 m | 20% / 1.92 m |
| N25->N21 | into the west court side | 0% / 6.15 m | 42% / 5.63 m |
| N26->N22 | into the east court side | 0% / 6.15 m | 42% / 5.63 m |
| N31->N30 | leaving Market Hall West under its roof | 0% / 2.33 m | 0% / 2.33 m |
| N32->N29 | leaving Market Hall East under its roof | 0% / 2.33 m | 0% / 2.33 m |
| N18->N31 | into Market Hall West | 71% / 3.56 m | 71% / 3.56 m |

The test assumes the camera sits exactly behind the direction of travel. At a corner or when stepping away from a door the real camera is still swinging round
from the previous heading, so these are worst cases; they are also exactly the places a camera-collision system exists for.

New in P1.3 (edges that did not exist in P1.2), worst first:

| Travel | Type | Samples unobstructed | Shortest camera distance (m) | Blocked by |
|---|---|---|---|---|
| N40->N11 | secondary | 36% | 2.25 | B12 |
| N10->N03 | secondary | 55% | 2.46 | B11 |
| N38->N11 | secondary | 0% | 2.62 | E03 |
| N39->N14 | secondary | 10% | 2.62 | B14 |
| N14->N39 | secondary | 0% | 3.54 | B09, DRESSING |
| N23->N38 | secondary | 58% | 4.66 | B15 |
| N24->N39 | secondary | 58% | 4.66 | B16 |
| N35->N09 | secondary | 60% | 4.98 | G01 |
| N36->N12 | service | 60% | 4.98 | G01 |
| N01->N35 | secondary | 85% | 5.1 | E02, G01 |
| N01->N36 | service | 95% | 5.1 | G01 |
| N11->N38 | secondary | 0% | 6.32 | B06 |

What was done about camera conflicts by layout: the tea lane leaves the bazaar north of the east hall instead of beside it (a hall-side exit put the camera inside the hall roof);
the two arrival buildings were made 4 m deep after the first build showed them shortening the camera at both lane starts (1.8 m and 2.9 m; now clear of the lane line);
the tea house approach is across an open terrace.

## Exchange Hall visibility (eye height 1.65 m, massing geometry)

| From | Place | Tower seal | Porch gable |
|---|---|---|---|
| N01 | Arrival court | yes | yes |
| N02 | Gateway centre lane | yes | yes |
| N03 | Simpang Timbangan (street junction) | yes | no |
| N04 | Bazaar south entrance | yes | no |
| N05 | Bazaar, south of the market cross | no | no |
| N27 | Bazaar, north of the market cross | yes | yes |
| N06 | Court south | yes | yes |
| N07 | Civic court centre | no | yes |
| N10 | Artisan lane at the cross street | yes | no |
| N13 | Warehouse lane at the cross street | no | no |
| N11 | Bazaar south-west | no | no |
| N14 | Bazaar south-east | no | no |
| N23 | Bazaar north-west | no | no |
| N24 | Bazaar north-east (tea lane entrance) | no | no |
| N16 | Lookout terrace | no | no |

The tower is visible from the arrival court, the gate, the junction, the bazaar entrance, the bazaar north of the market cross and the court's south edge, and now also from the artisan lane at the cross street. Standing exactly on the axis just south of the market cross, the cross's post hides it; at the court centre the porch gable hides the tower seal while the porch itself is in view.
It is not visible from inside the lanes north of the junction, the bazaar's side lanes or the terrace: the market halls and two-storey houses stand in the way, as in P1.2.

## Outstanding in-engine validation (cannot be settled in Blender)

1. Camera behaviour at the listed corners and door exits with the game's real collision set and smoothing.
2. Controller on the hall stairs, through the market-hall arches and across the 4 m lanes at running speed.
3. Whether thin objects (signs, lamp arms, vines, fences) are in the camera collision set at all.
4. Frame time with five more buildings; nothing here is a browser measurement.
