# 04 — Circulation, camera, collision and fade

All runs use the game's **unmodified** controller, follow camera, character, input and island collision (SHA-256 unchanged) in the isolated preview. The automated routes are a waypoint autopilot at 60 Hz (walking 2.1 m/s, body radius 0.34 m). **They are not a human's hands.** One scripted real-keyboard session (section 6) ran in the live page; it is also not a human playtest. A route passes only if it reaches the target with no stuck state (no progress for 2 s) and ends within 0.7 m of it.

## 1. Network (`pedestrian-network-batch3.json`, `-nodes.csv`, `-edges.csv`)

**38 nodes standable, 48 edges pass in both directions, 0 stuck** (batch 2: 32 nodes, 40 edges). Added: five door nodes (N42 smithy, N43 potter, N44 joiner, N45 outfitter, N46 carrier) with seven spur edges; N40 (workyard) moved from (-21, 34) to (-20.1, 35.4), because its P1.4 position was inside the well's footprint.

Rule (as in batch 2): a node is the point of maximum body clearance within 2.5 m of its P1.4 position, computed on the collision proxies. My first hand-placed nodes failed 5 edges (clearance 0.2-1.2 m off the free centre); after the move the five door nodes keep **1.29-1.38 m** beyond the body radius and N40 1.31 m. Narrowest side clearance along the new edges: N09-N42 0.38 m, N42-N10 0.14 m (the lane squeezes past the smithy's anvil and trough), N10-N44 0.40 m, N44-N11 0.64 m, court spurs 1.4-1.7 m.

## 2. District routes (`evidence/district-routes.json`): 17 / 17 pass

| Route | Seconds | Turns > 60° | Camera min (m) | Min alpha | Time faded below 0.9 |
|---|---|---|---|---|---|
| Lane south to north (N35 to N11) | 19.7 | 3 | 1.96 | 0.40 | 4.6 % |
| Lane north to south | 19.7 | 3 | 3.26 | 0.95 | 0 |
| Cross-street vista to the potter and back | 16.2 | 3 | 2.08 | 0.44 | 9.3 % |
| Arrival court: both shop fronts and back | 16.8 | 3 | 2.60 | 0.67 | 7.8 % |
| Workyard out and back | 6.2 | 1 | 1.07 | 0.15 | 29 % |
| **Loop: bazaar, lane, court, street, bazaar** | 61.9 | 3 | 3.32 | 0.96 | 0 |
| **Loop: bazaar, lane, cross street, east lane, bazaar** | 48.3 | 3 | 2.66 | 0.76 | 2.1 % |
| Round B10, B11, B12, E01, E02, both directions (10 routes; a grid search joins anchor points on all four sides at 0.12 m clearance, then the controller walks the path) | 16.3-28.5 | 1-5 | 0.50-2.94 | 0.14-0.81 | 4.5-52 % |

The ring walks hug walls on purpose (0.12 m off), so they are a worst case: the camera sits at its 0.5 m limit and the fade is active for 29-52 % of the walk. A normal lane walk keeps the character faded for 0-4.6 % of the time. **Findings:** (a) the workyard approach is camera-tight (1.07 m, character faded to 0.15 for 29 % of 6 s): a known tight spot, to be revisited when the buildings north of the lane exist; (b) the first fixed-rectangle ring walks failed on neighbours' and the buildings' own props, which is why the grid search replaced them; a building that could not be circumnavigated (B11, at the first potter layout) was the evidence for moving the kiln.

## 3. Collision with the new merchandise (`evidence/merchandise-collision.json`)

**104 / 104 solids stop the player** (batch 2: 51 for the five buildings of that batch; the new 53 are the five district buildings' walls, posts, goods and the kiln). Footprints are the measured bounding boxes of the source models, as before. Posts: 75 in the walk list, **0 in the camera list** (the batch-2 rule: thin posts block the body, not the camera). The lean-to roofs carry no camera proxy, as the P1.4 shop pentices.

## 4. 360° camera sweeps in the new spaces (`evidence/hall-camera.json`)

Full turns in place with the fade on; "raw" is the share of the turn in which the character covers over 25 % of the screen, "effective" the same after the fade.

| Spot | Camera min (m) | Raw > 25 % | Effective > 25 % | Min alpha |
|---|---|---|---|---|
| Lane at the smithy bay | 1.39 | 22 % | 2.1 % | 0.29 |
| Lane at the smithy door | 2.19 | 22 % | 2.4 % | 0.54 |
| Lane at the potter | 1.90 | 31 % | 0 | 0.40 |
| Lane at the joiner | 2.79 | 7 % | 0 | 0.76 |
| Cross street, B11 end | 2.79 | 3 % | 0 | 0.76 |
| Alley potter-joiner, mouth / middle | 0.78 / 0.78 | 49 % / 59 % | 3.7 % / 2.9 % | 0.14 |
| Alley smithy-potter, middle | 0.79 | 65 % | 2.4 % | 0.14 |
| Workyard | 2.84 | 2 % | 0 | 0.77 |
| Court by E01 / by E02 | 2.78 / 4.16 | 11 % / 0 | 0.3 % / 0 | 0.75 / 1.0 |

The two 3 m alleys compress the camera to its 0.8 m pull-in (inherent to the production camera's design) and the fade carries them. The Western and Eastern Hall sweeps are unchanged from batch 2 (camera 3.7-4.1 m, 2.75 m at the east hall's ends) after the polish.

## 5. Character fade in motion (`evidence/fade-motion.json`, six sequences)

Hall walk (min camera 4.07 m, no fade needed), Exchange Hall steps (0.97 m, alpha 0.14, 17.8 % faded, largest change 0.18 per frame), tea veranda (1.55 m, 0.25), **lane walk (camera never below 12.9 m, 0 % faded)**, vista and turns (2.80 m, 0.79, 7.6 %), workyard turn (2.82 m, 0.77, 21 %); largest single-frame opacity change over all six 0.18. Not judged: how 14 % opacity looks to a person in motion; the fade has still not been tried on the first island.

## 6. A real-keyboard session

In the live page (no autotest), a scripted browser sent real key events through the page's input handler: W for 5.5 s from the court to the lane (x -4 to -15.6), D (strafe) 3 s past the smithy (n 4 to 10.4) and 4.5 s past the potter (n to 19.9), W into the potter's shop front (stopped at x -18.16, as designed), W again (no movement). S (backwards, into a vase) did not move the character, A moved it 2.9 m south: **the player was pinned on one side by the shop's vases, never trapped**. Stills: [visuals/camera](visuals/camera). Controls in this preview are W/S forward-back, A/D strafe, Q/R turn the camera, so the session exercised strafing, wall contact and the camera, not mouse-look.

## 7. Not tested

A person's play; mouse-rotated camera round the new corners; gamepad and touch; the fade on the first island; running (shift) through the lane; the five unbuilt buildings' approaches.
