# 03 — Navigation, collision, camera and fade on the whole 24-building scene

Everything below was run with the game's unmodified controller, camera, collision and character on the final scene (`?autotest=suite`, 274 s, `evidence/autotest-suite.json`). These are **scripted** runs; a scripted run is not a human playtest.

## 1. Results

| Test | Result | File |
|---|---|---|
| Pedestrian network: nodes standable | 51 of 51 (the 52nd, N20 "future transport", is outside the slice) | `network.json` |
| Network edges, both directions | **65 of 65 pass**, 0 stuck frames; minimum node clearance 0.409 m (N17, tea-house veranda between two posts, unchanged since P2-A) | `network.json`, `pedestrian-network-batch5-*.csv` |
| Minimum raw camera distance on any edge | 1.50 m | `network.json` |
| District / loop / ring-walk routes | **45 of 45** (includes the new B15/B16 approaches, the bazaar → terrace → lookout → court → lane loop, the terrace stairs both ways and a ring walk of B10, B11, B12, E01, E02, B13, E04, B15, B16, each both ways) | `district-routes.json` |
| Solid proxies hit from outside | **271 of 271** | `merchandise-collision.json` |
| Platform / stairs | **7 of 7** with explicit criteria (below) | `platform-test.json` |
| Scripted real-key session (W, Q, R keys into the real controller, fade on) | 17 of 17 waypoints within 0.8 m, none stuck | `real-keyboard-session.json`, `visuals/camera/` |

Real-key session camera minima: 11 of 17 legs 12.8–13.1 m; the leg ends where the player turns round at the rail, in front of B15 and at the stair foot are 2.94–2.96 m.

## 2. Platform reporting corrected

Batch 4's `autotest-suite.json` showed "7 runs, 0 passes" because the suite counted a `pass` field that the run records never had. The records were not wrong; the aggregation was. The criteria below were fixed before the re-run and are in the comment above `testPlatform` in `p2a-tests.js`:

* arrival within 0.7 m of the target; end height within ±0.05 m of the design height (2.01 / 1.01 / 0.01 m) and of the heightfield support; not stuck (60 frames);
* stairs: no airborne steps (the jump run has exactly one jump); single-frame step up ≤ 0.45 m and down ≥ −0.45 m (measured 0.22 m);
* edge drop: starts on the terrace (1.01 m), ends grounded on the ground (0.01 m);
* terrace side wall approached from the ground: the height never rises and the body stops at or before the wall line (x ≤ −14.34 + 0.03).

First re-run 6 of 7: the side-wall test used the camera-centre position as the stop; it was changed to the body-stop criterion and its start moved to (−17, 72.5) (the old start is inside B15's envelope now). Then 7 of 7. A later change (the forecourt rail) made the old descent starts at n 78 unreachable, so the starts and ascent targets were retargeted to n 75.6 / 75.5. **Expectations were changed only where the scene changed; the criteria were not relaxed.**

## 3. Compression: investigated, causes, what remains

Method: yaw sweeps 1.8 m off every wall of a building ("ring walks") and at 21 named spots, each sample attributed to the obstacle that pulls the camera in (`compression-cause.json`). Raw camera distance, not opacity.

| Building ring walk | share < 3 m | share < 1.5 m | min m | main cause |
|---|---|---|---|---|
| B15 | 13 % | 0.5 % | 1.42 | walls, and the roof of E07 at the south-west corner |
| B16 | 7.7 % | 0 | 2.79 | walls |
| B13 | 4.8 % | 0 | 2.93 | walls |
| E04 | 10 % | 1.0 % | 1.47 | roof of E04, walls |
| E05 | 22 % | 0 | 1.56 | its own balcony, roofs of B03 and E06 |
| B10 | 33 % | 14 % | **0.84** | roofs of B10 / B11 / E01 |
| B12 | 30 % | 11 % | **0.84** | roofs of B12 / B11 |
| E01 | 29 % | 2 % | 1.40 | roofs |

Named spots at the new terrace: stair foot 12.9 m, terrace centre 9.4 m, beside each tower 2.81 m, at the two tower doors 2.79 m, hall steps foot 2.80 m (roof of B01). Warehouse/tea route unchanged from batch 4: porters' path gate 1.78 m, behind E04 2.07 m.

**Severe cases that remain (not fixed):** the B10 and B12 ring walks reach 0.84 m. The ring runs 1.8 m off the walls beside steep roofs (tops 6.7–8.3 m), and the west row has a gap of about 0.75 m between B10 and B11 (n 15.5–16.2) and an almost closed one between B11 and B12. A point probe of the walking proxies (not a body-sized test) found free, reachable cells in the B10–B11 gap, so it may be enterable; this was not confirmed with the real body, and it is a **question for the human playtest**. I tested whether short rails at the alley mouths would change what a player can reach (flood fill of the walking proxies) and the result was no change for the points tested, so no rails were added. **Remedy options, none applied:** close the two gaps with low fences (as was done for the slot and pocket at the east quarter), open them by 1 m, lower the lane-side eaves, or accept the pull-in as the camera's normal behaviour in a canyon. This needs a human to decide whether 0.84 m in a stress walk is acceptable.

## 4. Fade (the camera-side opacity of the character)

Sequences in `fade-motion.json`. A sequence's minimum opacity is reported next to its minimum camera distance.

| Sequence | min opacity | min camera m | frames under 0.9 | normal route or stress |
|---|---|---|---|---|
| hall walk, lane walk, tea lane (E05) | 0.99–1.00 | 3.7–13 | 0 % | normal |
| porch steps (hall forecourt) | 0.83 | 2.95 | 3.9 % | normal (was ~0.15 before the rail) |
| terrace approach | 0.82 | 2.94 | 3.7 % | normal |
| tower doors (B15/B16) | 0.78 | 2.63 | 5.9 % | normal |
| porters' path | 0.81 | 2.94 | 4.4 % | normal |
| vista and turn, workyard turn | 0.77–0.79 | 2.8 | 7.5–21 % | semi-normal |
| tea veranda | **0.25** | 1.55 | 30 % | **stress** (turning on the veranda between posts) |
| east lane court | **0.43** | 1.76 | 6.2 % | **stress** |

No normal route falls below 0.77. Two sequences still reach 0.25 and 0.43; I do not call those acceptable, I call them the known stress cases of the veranda and the east court. The fade system is the game's provisional one and has **not been tested on the first island**.

## 5. Not tested

Mouse-rotated camera round the new corners, gamepad, touch, a human playing at speed, different aspect ratios other than 1280 × 720 (the hall-camera test uses a fixed 1280 × 720 viewport).
