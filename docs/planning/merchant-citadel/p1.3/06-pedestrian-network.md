# 06 - Pedestrian network (P1.3)

37 nodes, 47 edges (46 built, 1 reserved link), **11 independent loops**, 452.5 m of built route. P1.2: 31 nodes, 39 edges, 9 loops, 437 m.
Primary route, arrival court to the hall podium: **76.8 m**, about 37 s walking or 17 s running.

## Named loops (measured along the graph)

| Loop | Nodes | Length (m) | Walk at 2.1 m/s | What it passes |
|---|---|---|---|---|
| Artisan loop | 03 - 10 - 11 - 04 - 03 | 68 | 32 s | Junction, cross street, artisan lane past two workshops and the workyard, bazaar south-west corner, back down the street |
| Warehouse loop | 03 - 13 - 14 - 04 - 03 | 68 | 32 s | Junction pocket court, warehouse lane past the counting house (service court on the right), bazaar south-east corner, back down the street |
| Arrival west loop | 01 - 35 - 09 - 10 - 03 - 02 - 01 | 69 | 33 s | Arrival court, gateway shop, artisan lane south, cross street, back through the gate |
| Arrival east loop | 01 - 36 - 12 - 13 - 03 - 02 - 01 | 69 | 33 s | Arrival court, carrier's house, warehouse lane south past the warehouse, cross street, back through the gate |
| Bazaar west circuit | 04 - 11 - 38 - 23 - 25 - 06 - 27 - 30 - 05 - 04 | 85 | 40 s | Round the west hall by the perimeter shop and the assay office |
| Bazaar east circuit and tea spur | 04 - 14 - 39 - 24 - 26 - 06 - 27 - 29 - 05 - 04 | 85 | 40 s | Round the east hall by the registry; the tea lane leaves at N24 |

Every loop above passes at least two building fronts and one of the small public spaces. In P1.2 the street had no side exit: the only way from it to either lane was back through the arrival court or on to the bazaar.

## Physical validation of every edge (actual geometry)

Sampled every 0.25 m: paved surface below, step 0.42 m or less, no geometry within 0.34 m of the body at four heights, headroom 2.0 m or more.

| Edge | Type | Length (m) | Unpaved samples | Largest step (m) | Least headroom (m) | Nearest obstacle at 1 m height (m) | Result |
|---|---|---|---|---|---|---|---|
| N20-N01 | reserved link | 16.0 | 32 | 0.03 | open sky | 3.02 | RESERVED (not built in P1-P3) |
| N01-N02 | primary | 5.0 | 0 | 0.0 | open sky | 1.86 | PASS |
| N02-N03 | primary | 15.0 | 0 | 0.0 | open sky | 1.86 | PASS |
| N03-N04 | primary | 17.5 | 0 | 0.0 | open sky | 3.8 | PASS |
| N04-N05 | primary | 8.0 | 0 | 0.0 | open sky | 1.94 | PASS |
| N05-N29 | primary | 4.4 | 0 | 0.0 | open sky | 0.74 | PASS |
| N29-N27 | primary | 4.4 | 0 | 0.0 | open sky | 0.4 | PASS |
| N05-N30 | primary | 4.4 | 0 | 0.0 | open sky | 0.6 | PASS |
| N30-N27 | primary | 4.4 | 0 | 0.0 | open sky | 0.51 | PASS |
| N27-N06 | primary | 9.5 | 0 | 0.0 | open sky | 1.37 | PASS |
| N06-N07 | primary | 5.0 | 0 | 0.0 | open sky | None | PASS |
| N07-N08 | primary, stairs | 8.0 | 0 | 0.22 | open sky | 0.79 | PASS |
| N01-N35 | secondary | 9.8 | 0 | 0.0 | open sky | 0.95 | PASS |
| N35-N09 | secondary | 7.0 | 0 | 0.0 | open sky | 1.77 | PASS |
| N09-N10 | secondary | 16.0 | 0 | 0.0 | open sky | 0.7 | PASS |
| N10-N11 | secondary | 18.5 | 0 | 0.0 | open sky | 0.7 | PASS |
| N11-N04 | secondary | 16.0 | 0 | 0.0 | open sky | 0.96 | PASS |
| N10-N03 | secondary | 16.0 | 0 | 0.0 | open sky | 1.5 | PASS |
| N01-N36 | service | 9.8 | 0 | 0.0 | open sky | 0.96 | PASS |
| N36-N12 | service | 7.0 | 0 | 0.0 | open sky | 1.77 | PASS |
| N12-N13 | service | 16.0 | 0 | 0.0 | open sky | 1.46 | PASS |
| N13-N14 | service | 18.5 | 0 | 0.0 | open sky | 1.81 | PASS |
| N14-N04 | service | 16.0 | 0 | 0.0 | 5.54 | 0.78 | PASS |
| N03-N13 | service | 16.0 | 0 | 0.0 | open sky | 1.77 | PASS |
| N11-N18 | market | 5.7 | 0 | 0.0 | open sky | 1.59 | PASS |
| N18-N31 | market | 6.5 | 0 | 0.0 | 2.86 | 0.83 | PASS |
| N31-N30 | market | 9.3 | 0 | 0.0 | 2.27 | 0.83 | PASS |
| N14-N19 | market | 5.7 | 0 | 0.0 | open sky | 1.01 | PASS |
| N19-N32 | market | 6.5 | 0 | 0.0 | 2.86 | 0.83 | PASS |
| N32-N29 | market | 9.3 | 0 | 0.0 | 2.27 | 0.83 | PASS |
| N11-N38 | secondary | 4.5 | 0 | 0.0 | open sky | 2.18 | PASS |
| N38-N23 | secondary | 17.5 | 0 | 0.0 | open sky | 1.76 | PASS |
| N23-N25 | secondary | 9.2 | 0 | 0.0 | open sky | 1.45 | PASS |
| N25-N21 | secondary | 5.8 | 0 | 0.0 | open sky | 1.61 | PASS |
| N25-N06 | secondary | 11.0 | 0 | 0.0 | open sky | 1.64 | PASS |
| N21-N07 | secondary | 12.0 | 0 | 0.0 | open sky | 1.61 | PASS |
| N14-N39 | secondary | 4.5 | 0 | 0.0 | open sky | 1.93 | PASS |
| N39-N24 | secondary | 17.5 | 0 | 0.0 | open sky | 1.92 | PASS |
| N24-N26 | secondary | 9.2 | 0 | 0.0 | open sky | 0.95 | PASS |
| N26-N22 | secondary | 5.8 | 0 | 0.0 | open sky | 1.61 | PASS |
| N26-N06 | secondary | 11.0 | 0 | 0.0 | open sky | 1.62 | PASS |
| N22-N07 | secondary | 12.0 | 0 | 0.0 | open sky | 1.61 | PASS |
| N24-N41 | scenic | 6.3 | 0 | 0.0 | open sky | 1.69 | PASS |
| N41-N16 | scenic | 10.0 | 0 | 0.0 | open sky | 1.33 | PASS |
| N16-N17 | scenic | 5.3 | 0 | 0.0 | 2.28 | 0.89 | PASS |
| N13-N33 | service | 9.0 | 0 | 0.0 | open sky | 2.24 | PASS |
| N11-N40 | secondary | 6.7 | 0 | 0.0 | open sky | 1.0 | PASS |

**46 of 46 built edges pass.** First run of the new layout: three edges failed (two court benches on the new court-side paths, a stall's barrel on the path to the east court entrance); benches and the two north stalls were moved and the test repeated.

## Nodes

| Node | x | z | Place |
|---|---|---|---|
| N01 | 0 | 0 | Arrival court |
| N02 | 0 | -5.0 | Gateway centre lane |
| N03 | 0 | -20 | Simpang Timbangan (street junction) |
| N04 | 0 | -37.5 | Bazaar south entrance |
| N05 | 0 | -45.5 | Bazaar, south of the market cross |
| N29 | 2.7 | -49 | Cross-passage east of the cross |
| N30 | -2.7 | -49 | Cross-passage west of the cross |
| N27 | 0 | -52.5 | Bazaar, north of the market cross |
| N06 | 0 | -62 | Court south |
| N07 | 0 | -67 | Civic court centre |
| N08 | 0 | -75 | Exchange Hall podium, top of stairs (+1.0 m) |
| N35 | -9 | -4 | Arrival court west exit |
| N09 | -16 | -4 | Artisan lane south |
| N10 | -16 | -20 | Artisan lane at the cross street |
| N11 | -16 | -38.5 | Bazaar south-west |
| N36 | 9 | -4 | Arrival court east exit |
| N12 | 16 | -4 | Warehouse lane south |
| N13 | 16 | -20 | Warehouse lane at the cross street |
| N14 | 16 | -38.5 | Bazaar south-east |
| N18 | -12 | -42.5 | Market Hall West south arch |
| N31 | -12 | -49 | Market Hall West interior |
| N19 | 12 | -42.5 | Market Hall East south arch |
| N32 | 12 | -49 | Market Hall East interior |
| N38 | -19.75 | -41 | Market west side lane, south |
| N23 | -19.75 | -58.5 | Bazaar north-west |
| N39 | 19.75 | -41 | Market east side lane, south |
| N24 | 19.75 | -58.5 | Bazaar north-east (tea lane entrance) |
| N25 | -11 | -61.3 | Court south-west entrance |
| N26 | 11 | -61.3 | Court south-east entrance |
| N21 | -12 | -67 | Court west (corner house door) |
| N22 | 12 | -67 | Court east (corner house door) |
| N41 | 26 | -58 | Tea lane |
| N16 | 36 | -57 | Lookout terrace |
| N17 | 36 | -62.3 | Tea house veranda |
| N20 | 0 | 16 | Future transport reservation |
| N33 | 25 | -20 | Service court (Pelataran Gudang) |
| N40 | -21 | -34 | Artisan workyard |
