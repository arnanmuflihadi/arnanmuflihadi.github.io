# 09 - Walking network and spatial validation (P1.2)

## Technical constraints read from the project (configuration only)

| Item | Value | Source |
|---|---|---|
| Axes and units | +y up, metres, GLB/glTF through `GLTFLoader` | `assets/js/vendor/three-atlas.module.js` |
| Explorer | 1.9 m tall, collision radius 0.34 m, maximum step 0.42 m | `player-controller.js`, `floating-atlas/collision.js` |
| Movement | walk 2.1 m/s, run 4.6 m/s | `player-controller.js` |
| Camera | FOV 60, 11.8 m behind, +6.6 m, looks at player +1.25 m; shortened to (hit distance - 0.28 m), minimum 0.8 m | `urban-atlas/camera.js` |

The production controller and camera were not modified or run. Their constants were copied into `validate_envelopes.py`.

## Two layers of checking

1. **Nominal** (`town_data.py`): footprint rectangles, clear corridors, paved approaches, graph connectivity. Result: PASS.
2. **Actual geometry** (`validate_envelopes.py`, re-run on the P1.2 scene): the assembled Blender scene, 847,540 triangles, tested with ray casts and nearest-surface queries.
   Raw results: [asset-evidence/spatial-validation-actual-geometry.json](asset-evidence/spatial-validation-actual-geometry.json).

## A. Gaps between real building envelopes (roof overhangs included)

All pairs closer than 3 m:

| A | B | Gap (m) | Status |
|---|---|---|---|
| B05 | B06 | 0.89 | NARROW |
| B04 | B05 | 1.09 | OK |
| B11 | B12 | 1.09 | OK |
| B04 | G01 | 1.33 | OK |
| B07 | G01 | 1.46 | OK |
| B07 | B08 | 1.59 | OK |
| B08 | B09 | 1.59 | OK |
| B10 | B11 | 1.59 | OK |

Rule: under 0.3 m fails, under 1.0 m is narrow. **No pair fails.** The first P1.1 layout had two overlaps (gateway roofs against B04 and B07, -0.63 and -1.17 m);
the gateway was moved. P1.0's 2.5 m alleys, which left about 0.2 m between roofs, are now 3 to 3.5 m.

## B. Physical walkability of every edge

Each edge is sampled every 0.25 m. At each sample: a downward ray must find a paved tile or stair; the rise from the previous sample must be 0.42 m or less;
no geometry may lie within 0.34 m of the body axis at 0.5, 1.0, 1.5 and 1.85 m; headroom must be 2.0 m or more.

| Edge | Type | Length (m) | Unpaved samples | Largest step (m) | Least headroom (m) | Nearest obstacle at 1 m height (m) | Result |
|---|---|---|---|---|---|---|---|
| N20-N01 | reserved link | 16.0 | 32 | 0.03 | open sky | 3.32 | RESERVED (not built in P1-P3) |
| N01-N02 | primary | 5.0 | 0 | 0.0 | open sky | 1.86 | PASS |
| N02-N03 | primary | 17.0 | 0 | 0.0 | open sky | 1.86 | PASS |
| N03-N04 | primary | 14.0 | 0 | 0.0 | open sky | 3.8 | PASS |
| N04-N05 | primary | 9.5 | 0 | 0.0 | open sky | 1.94 | PASS |
| N05-N29 | primary | 4.4 | 0 | 0.0 | open sky | 0.74 | PASS |
| N29-N27 | primary | 4.4 | 0 | 0.0 | open sky | 0.4 | PASS |
| N05-N30 | primary | 4.4 | 0 | 0.0 | open sky | 0.6 | PASS |
| N30-N27 | primary | 4.4 | 0 | 0.0 | open sky | 0.51 | PASS |
| N27-N06 | primary | 9.5 | 0 | 0.0 | open sky | 1.37 | PASS |
| N06-N07 | primary | 5.0 | 0 | 0.0 | open sky | None | PASS |
| N07-N08 | primary, stairs | 8.0 | 0 | 0.22 | open sky | 0.79 | PASS |
| N01-N09 | secondary | 20.4 | 0 | 0.0 | open sky | 1.71 | PASS |
| N09-N10 | secondary | 18.0 | 0 | 0.0 | open sky | 0.7 | PASS |
| N10-N11 | secondary | 16.0 | 0 | 0.0 | open sky | 0.7 | PASS |
| N11-N04 | secondary | 20.1 | 0 | 0.0 | open sky | 0.72 | PASS |
| N11-N18 | market | 9.2 | 0 | 0.0 | open sky | 1.48 | PASS |
| N18-N31 | market | 6.5 | 0 | 0.0 | 2.86 | 0.83 | PASS |
| N31-N30 | market | 9.3 | 0 | 0.0 | 2.27 | 0.83 | PASS |
| N01-N12 | service | 20.4 | 0 | 0.0 | open sky | 1.71 | PASS |
| N12-N13 | service | 14.0 | 0 | 0.0 | open sky | 1.46 | PASS |
| N13-N14 | service | 20.0 | 0 | 0.0 | open sky | 1.19 | PASS |
| N14-N04 | service | 20.1 | 0 | 0.0 | open sky | 0.86 | PASS |
| N14-N19 | market | 9.2 | 0 | 0.0 | open sky | 1.48 | PASS |
| N19-N32 | market | 6.5 | 0 | 0.0 | 2.86 | 0.83 | PASS |
| N32-N29 | market | 9.3 | 0 | 0.0 | 2.27 | 0.83 | PASS |
| N14-N15 | secondary | 12.0 | 0 | 0.0 | open sky | 1.48 | PASS |
| N15-N16 | scenic | 20.0 | 0 | 0.0 | open sky | 1.56 | PASS |
| N16-N17 | scenic | 5.2 | 0 | 0.0 | 2.88 | 0.72 | PASS |
| N11-N23 | secondary | 20.5 | 0 | 0.0 | open sky | 1.48 | PASS |
| N23-N25 | secondary | 5.4 | 0 | 0.0 | open sky | 2.17 | PASS |
| N25-N21 | secondary | 5.9 | 0 | 0.0 | 11.56 | 0.66 | PASS |
| N25-N06 | secondary | 15.0 | 0 | 0.0 | open sky | 1.86 | PASS |
| N21-N07 | secondary | 17.0 | 0 | 0.0 | 11.77 | 0.66 | PASS |
| N15-N24 | secondary | 8.5 | 0 | 0.0 | open sky | 2.15 | PASS |
| N24-N26 | secondary | 5.4 | 0 | 0.0 | open sky | 1.74 | PASS |
| N26-N22 | secondary | 5.9 | 0 | 0.0 | 2.37 | 0.74 | PASS |
| N26-N06 | secondary | 15.0 | 0 | 0.0 | open sky | 1.45 | PASS |
| N22-N07 | secondary | 17.0 | 0 | 0.0 | 2.37 | 0.93 | PASS |

**38 of 38 built edges pass.** The reserved link to the future transport pad is unpaved by design.
P1.2 added jetties, a porch, signs, goods and furniture and re-ran the whole test: no edge failed on the first run, because new items were placed against the P1.1 clear zones.
(P1.1's first run had failed seven edges, all corrected then.) The tightest passages are beside the market cross (0.4 to 0.6 m to its goods).

### The two transitions named in the review

N23-N21 and N24-N22 no longer exist. In P1.0 they ran from the bazaar corners diagonally to the court sides, across 1 m of unpaved ground and through the
corners of B15 and B16. Each is replaced by two paved edges through new court entrances: N23-N25-N21 and N24-N26-N22. Both pass.

## C. Exchange Hall stair approach (edge N07-N08)

Measured risers: 0.22, 0.20, 0.18, 0.20, 0.19 m. **5 risers, largest 0.223 m against the 0.42 m limit, total rise 0.99 m.**
The approach is paved from the court to the podium deck with no gap. Whether the controller climbs it smoothly is an engine test for P2.

## D. Lanterns, banners, trade signs, flower boxes and vines

All 97 hanging or wall-mounted objects were measured against the surface beneath them. Rule: 2.1 m or more over walkable paving.

| Lowest five over paving | On | Clearance (m) |
|---|---|---|
| `CUS-Sign_Scroll_wood` | B07 | 2.18 |
| `CUS-Sign_Loaf_wood` | B09 | 2.18 |
| `CUS-Sign_Scroll_wood` | B16 | 2.18 |
| `CUS-Sign_Jar_wood` | B08 | 2.26 |
| `CUS-Sign_Hammer_wood` | B10 | 2.26 |

**None is below 2.1 m.** P1.0's lamp-post lanterns hung at about 1.6 m inside the walking line. They are now on 3.9 m posts with the lantern at 2.5 m,
set 0.7 m outside the street's clear width with the arm along the frontage. P1.2's first run flagged two flower boxes 0.68 m above the tea-house balcony deck (moved to side windows) and showed the trade signs under the jetties at 2.11 m (raised; now 2.18 m).

## E. Market hall arch opening (`MV-Wall_Arch`, measured on the mesh)

Clear width 1.67 m from the ground to 1.9 m, 1.57 m at 2.2 m; clear height at the centre 2.74 m.
The 0.68 m wide, 1.9 m tall explorer passes with about 0.5 m each side. Edges N18-N31, N31-N30, N19-N32 and N32-N29 walk through arches and pass.

## F. Follow-camera line of sight

For every edge and both directions of travel, a ray is cast from the look-at point (player +1.25 m) to the documented camera position (11.8 m behind, +6.6 m).
Full distance is 12.96 m.

- **48 of 76 travel directions are completely unobstructed.**
- **The whole primary axis, walking towards the hall, is unobstructed** except the 6 m after the market cross, where the cross's post stands between player and camera (camera shortens to 3.4 m, then recovers). The new porch, jetties and signs do not enter the camera line on the axis.
- Where the camera does shorten:

| Travel | Type | Samples unobstructed | Shortest camera distance (m) | Blocked by |
|---|---|---|---|---|
| N22->N07 | secondary | 31% | 0.8 | B16 |
| N21->N07 | secondary | 37% | 0.82 | B15 |
| N17->N16 | scenic | 0% | 0.97 | B17 |
| N15->N16 | scenic | 66% | 2.18 | B03 |
| N31->N30 | market | 0% | 2.33 | B02 |
| N32->N29 | market | 0% | 2.33 | B03 |
| N22->N26 | secondary | 0% | 2.44 | B16 |
| N21->N25 | secondary | 0% | 2.52 | B15 |
| N30->N31 | market | 42% | 2.53 | M01, B02 |
| N29->N32 | market | 42% | 2.53 | M01, B03 |
| N18->N11 | market | 5% | 2.94 | B02 |
| N19->N14 | market | 5% | 2.94 | B03 |
| N05->N04 | primary | 70% | 3.43 | M01 |
| N27->N06 | primary | 70% | 3.43 | M01 |
| N08->N07 | primary, stairs | 0% | 3.49 | B01 |
| N18->N31 | market | 71% | 3.56 | B02 |
| N19->N32 | market | 7% | 3.56 | B09, B03 |
| N04->N14 | service | 95% | 4.37 | B06 |
| N23->N11 | secondary | 64% | 4.57 | B15 |
| N24->N15 | secondary | 28% | 5.67 | B16 |
| N25->N21 | secondary | 0% | 6.15 | B02 |
| N26->N22 | secondary | 0% | 6.15 | B03 |
| N11->N04 | secondary | 95% | 6.94 | DRESSING |
| N31->N18 | market | 21% | 7.13 | B02 |
| N32->N19 | market | 21% | 7.13 | B03 |
| N23->N25 | secondary | 36% | 8.61 | DRESSING |
| N04->N11 | secondary | 61% | 9.16 | B09 |
| N07->N06 | primary | 82% | 11.55 | B01 |

These are the expected cases: walking away from a facade the player is standing against (court sides, hall podium, tea house), and walking under a roof (market halls, veranda).
Under the hall roofs the camera settles at about 2.3 to 2.9 m. The game's own collision set may differ from this ray test (it may ignore thin banners and posts), so P2 must repeat it in the engine.

## Nodes

| Node | x | z | Place |
|---|---|---|---|
| N01 | 0 | 0 | Arrival court |
| N02 | 0 | -5.0 | Gateway centre lane |
| N03 | 0 | -22 | Merchant street mid |
| N04 | 0 | -36 | Bazaar south entrance |
| N05 | 0 | -45.5 | Bazaar, south of the market cross |
| N29 | 2.7 | -49 | Cross-passage east of the cross |
| N30 | -2.7 | -49 | Cross-passage west of the cross |
| N27 | 0 | -52.5 | Bazaar, north of the market cross |
| N06 | 0 | -62 | Court south |
| N07 | 0 | -67 | Civic court centre |
| N08 | 0 | -75 | Exchange Hall podium, top of stairs (+1.0 m) |
| N09 | -20 | -4 | Artisan lane south |
| N10 | -20 | -22 | Artisan lane mid |
| N11 | -20 | -38 | Bazaar south-west |
| N12 | 20 | -4 | Warehouse lane south |
| N13 | 20 | -18 | Warehouse door |
| N14 | 20 | -38 | Bazaar south-east |
| N15 | 20 | -50 | Bazaar east exit |
| N16 | 40 | -49 | Lookout terrace |
| N17 | 40 | -54.2 | Tea house veranda |
| N18 | -12 | -42.5 | Market Hall West south arch |
| N31 | -12 | -49 | Market Hall West interior |
| N19 | 12 | -42.5 | Market Hall East south arch |
| N32 | 12 | -49 | Market Hall East interior |
| N20 | 0 | 16 | Future transport reservation |
| N21 | -17 | -67 | Court west / corner house |
| N22 | 17 | -67 | Court east / shophouse |
| N23 | -19.5 | -58.5 | Bazaar north-west |
| N24 | 19.5 | -58.5 | Bazaar north-east |
| N25 | -15 | -61.5 | Court south-west entrance |
| N26 | 15 | -61.5 | Court south-east entrance |

31 nodes, 39 edges, 9 independent loops, 453.4 m in total. Primary route from arrival to the hall podium: **76.8 m**, about 37 s walking or 17 s running.

## Vertical design

Flat at y = 0 except the Exchange Hall podium (+1.0 m, five risers over 2.08 m). No ramp module exists in the kit.
