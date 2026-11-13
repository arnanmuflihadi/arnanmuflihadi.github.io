# 04 — Circulation, camera and collision validation

All runs use the game's **unmodified** `createPlayerController`, `createFollowCamera`, `createCharacter`, `createInput` and island `collision.js` in the isolated preview (hashes unchanged). Routes are simulated at a fixed 60 Hz with a waypoint autopilot (W held, walking 2.1 m/s, body radius 0.34 m); they use the same code path as keyboard play but are not a human's hands, so the guided checklist (07) is still owed. **A route does not pass because the character crosses a straight line:** it passes when it reaches the target without a stuck state (no progress for 2 s) and the ending position is within 0.7 m of the target; every edge is walked in both directions, and the route set includes representative turns.

Files: `merchant-citadel-p2a/evidence/` — `network.json`, `bazaar-routes.json`, `autotest-routes.json`, `merchandise-collision.json`, `hall-camera.json`, `fade-motion.json`, `camera-cases.json`, `camera-shots.json`, `platform-test.json`; network records in [pedestrian-network-batch2.json](pedestrian-network-batch2.json), [nodes](pedestrian-network-batch2-nodes.csv), [edges](pedestrian-network-batch2-edges.csv).

## 1. Network: N18/N31 and N19/N32 and the whole slice

**32 / 32 nodes standable, 40 / 40 edges pass in both directions, 0 stuck states** (the closeout slice had 28 nodes and 34 edges; the four market-hall nodes and six edges are new).

| Edge | Length | Walk (each way) | Narrowest side clearance | Against | Camera min |
|---|---|---|---|---|---|
| N11 – N18 (south-west bazaar to the West Hall front) | 5.0 m | 2.25 s | 2.83 m | merchandise (barrel/crates at the door) | 5.4 m / 13.0 m |
| N18 – N31 (entrance to the aisle centre) | 6.5 m | 2.95 s | 1.71 m | counter | 13.0 m |
| N31 – N30 (aisle to the cross passage, through the open east side) | 10.1 m | 4.67 s | 0.84 m | counter | 4.1 m / 13.0 m |
| N14 – N19 | 5.0 m | 2.25 s | 2.07 m | hall wall (east) | 5.4 m / 13.0 m |
| N19 – N32 (entrance to the East aisle centre) | 6.5 m | 2.95 s | 1.66 m | merchandise / hall wall | 6.1 m / 13.0 m |
| N32 – N29 (aisle to the cross passage, through the open west side) | 10.1 m | 4.67 s | 0.84 m | counter | 3.8 m / 13.0 m |

**Corrections to the P1.4 nodes** (rule: a node is the centre of the free span, measured on the collision proxies): N18 (−12, 42.5) → **(−13, 42.5)**, N31 (−12, 49) → **(−13, 49)**, N19 (12, 42.5) → **(13, 42.5)**, N32 (12, 49) → **(13, 49)**: the aisle centres. The P1.4 positions were 1 m off the hall axis and gave 0.71 m side clearance on the entrance edges; now 1.7 m. Clearance at the nodes: 2.8 m (N18), 2.0 m (N31), 2.1 m (N19), 2.0 m (N32). The cross-passage nodes N29/N30 (±2.9) keep 1.56 m from the market cross.

## 2. Market entry, exit, turning and the cross (`bazaar-routes.json`): 19 / 19 pass

| Route | Time | Turns > 60° | Camera min / median | Side clearance |
|---|---|---|---|---|
| West: enter from the south front; leave south | 5.3 s each | 0 | 12.9 / 13.1 m; 5.9 / 13.1 m | 1.71 m |
| West: leave by the east side; enter from the cross passage | 4.7 s each | 0 | 4.1 / 5.2 m; 13.0 / 13.1 m | 0.84 m |
| West: loop round the aisle between tables and counters | 12.3 s | 1 | 4.1 / 10.9 m | 0 (brushes merchandise) |
| West: north end, turn three ways in front of the bench | 10.0 s | 4 | 4.1 / 5.9 m | 0.001 |
| East: enter, leave south, exit west, enter from cross | 4.7–5.3 s | 0 | 3.8–13.0 m | 0.84–1.66 m |
| East: loop round the aisle | 12.2 s | 2 | 2.9 / 7.5 m | 0 |
| Hall to hall across the cross passage and back | 15.3 s | 4 | 3.8–4.1 / 11.2–12.1 m | 0.20 m (awning-row post) |
| Market cross: full circle clockwise and counter-clockwise | 10.6 s | 3 | 6.9 / 11.6–12.8 m | 1.16 m |
| **Circuit**: bazaar west, both halls, cross, spine, back (744° of turning) | 42.2 s | 7 | 4.2 / 11.4 m | 0.21 m |
| Fronts of B14, E06, E07 (out and back) | 3.2–3.5 s | 1 each | 1.0–2.0 / 3.1–8.2 m | 0.2–0.8 m |

Notes: "side 0" means the route brushed a counter or table and slid along it (the target points of the loops are deliberately close to the stalls to test turning and sliding); a first version of the loops aimed through a bench at the north end of each hall and stalled, which is the bench doing its job. The loops and the north-end test were re-aimed round the bench, the bench stays solid. The shop-front camera minima (1.0 m at E06/E07) are the route reversing against the shop front with the lane's eaves behind: tight, and cured by the fade (below).

## 3. Collision with merchandise and structure (`merchandise-collision.json`)

Footprints are taken from the **measured bounding boxes of the source models** (not estimated), rotated and scaled as placed. Test: for every solid of the five new buildings (51: 17 + 13 merchandise props, 6 counters, 8 posts, 4 hall wall runs, 3 shop walls) the character walks at it from every free direction of eight (1–8 directions per solid depending on what is around it) and the final position must stay outside the footprint expanded by the body radius.
**51 / 51 stop the player** (the closest any run came to a footprint edge was 1 mm outside it; none ended inside). Flat rugs and items on counters have no proxy by design.
**Structural posts stay solid for the body even though small posts are excluded from the camera:** 65 posts in the walk list, 0 in the camera list (`posts_in_walk_list` 65, `posts_in_camera_list` 0); the post rule is explicit in `p2a.js` (`camOff = ['post']`, `?postsblock=1` restores the P2-A behaviour).

## 4. Covered-hall camera (`hall-camera.json`)

The measure: a full 360° turn in place at eight spots in the halls, camera distance to the head anchor and the share of the viewport covered by the character.

| | Before (P2-A roof proxy, a solid slab from 2.2 m) | After (open two-slope shell, outer eave step excluded) |
|---|---|---|
| Aisle centres and ends | camera **0.94 m** behind the player at every yaw, character covering > 25 % of the screen 85–100 % of the time | **4.07 m** minimum (West), 3.71 m centre / 2.75 m aisle ends (East: closed walls) |
| Side openings (under the eave) | 0.94 m, 85 % covered | 4.07 m, 0 % covered |

The "before" row is the first test run on the new halls (its file was overwritten by the final run, the numbers are from that run's output); it can be reproduced with the slab proxy. Cause and fix: the A02 archetype is an open arcade, so the P2-A stepped bands (a full-footprint slab at the eave height) fill the volume where the player walks; `roof_shell()` in `p2a_data.py` models the pitched roof as thin stepped boxes on both slopes and leaves the space below free. With the character fade the effective coverage over 25 % is **0 %** in every sweep.
**Cloth, signs and pennants stay out of camera collision** — re-measured on the bazaar routes (modes in `autotest-routes.json`): the circuit with cloth in the camera list drops to **0.91 m** minimum (4.19 m in the default mode) and the hall-to-hall route to 2.9 m (4.1 m); pennants alone: 4.1 m (no effect).

## 5. Character fade in motion (`fade-motion.json`, [strips](visuals/fade))

Three walked sequences, one 640 x 360 frame every 0.5 s, plus the opacity trace:

| Sequence | Seconds | Minimum camera | Minimum opacity | Time below 0.9 | Largest opacity change in one frame |
|---|---|---|---|---|---|
| Walk into the West Hall, turn at the north end, leave | 31.3 | 4.07 m | 1.0 (never needed) | 0 % | 0 |
| Exchange Hall steps up, porch landing, steps down | 18.3 | 0.97 m | 0.14 | 17.8 % | 0.18 |
| Tea-house veranda gap and back | 5.8 | 1.55 m | 0.25 | 30 % | 0.10 |

**Found by watching it in motion:** the first fade followed the raw camera distance and changed opacity by up to **0.75 in a single frame** when the production camera snapped inward (its inward rate is fast by design): a flicker. Fixed in `p2a.js` with a time filter (opacity falls with a 0.06 s time constant and recovers with 0.3 s); the largest change is now 0.18 per frame. Cost of smoothing: the share of the 360° sweeps where the character still covers more than 25 % of the screen is 1.9–4.2 % at the porch landing, turret foot and veranda (it was 0–0.8 % unsmoothed), because opacity lags the squeeze by a few frames. **Not judged:** the look at 14 % opacity in real motion by a person (the strips show it working); the fade has not been tested on the first island.
In the bazaar halls the camera no longer compresses, so the fade does not trigger there.

## 6. Other cameras checked again

Exchange Hall approach (up 12.9 m, down 3.0 m at the first second, porch landing 0.97 m with fade), tea veranda (1.5 m, fade), inn and tower corner (unchanged from the closeout: 2.8–3.4 m minima, 4–8 inward snaps at corners, all inherent to the production camera's fast inward / slow outward design). The platform test (stairs up/down, walking and running, jump on a riser, drop, side blocked) passes unchanged.

## 7. What the tests do not show

Human feel and speed; mouse-rotated camera round the new corners (only 360° turn-in-place sweeps); gamepad/touch; many characters or NPCs; moving carts; the interior of anything but the two arcades.
