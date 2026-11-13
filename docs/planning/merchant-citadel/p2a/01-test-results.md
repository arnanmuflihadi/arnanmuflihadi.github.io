# P2-A test results — scale, controller, camera, platform

> **Corrections (2026-11-12, P2-A closeout):** (1) the "1.34 m alley" between B04 and B05 was the roof-eave gap; the walls are 3.0 m apart (see closeout/01 and 02). (2) The camera-compression and N16–N17 findings below were acted on in the closeout. Superseding results: [closeout/03-camera-validation.md](closeout/03-camera-validation.md), [closeout/02-pedestrian-network-spec.md](closeout/02-pedestrian-network-spec.md).


Everything below was measured in the preview page with the game's **unmodified** `createPlayerController`, `createFollowCamera`, `createCharacter`, `createInput` and island `collision.js`
(`merchant-citadel-p2a/index.html`, tests in `p2a-tests.js`, raw results in `merchant-citadel-p2a/evidence/`). Routes are simulated at a fixed 60 Hz with a waypoint autopilot
(turn rate 2.4 rad/s, W held, Shift for runs); they use the same code path as keyboard play but are **not** a human's hands. A human playtest is still owed (see 05).

## 1. Scale, orientation and placement (`autotest-scale.json`)

| Check | Result |
|---|---|
| Kit node bounding boxes in three vs the Blender export | within 0.005 cm on all 17 nodes (min/max on three axes) |
| Node transforms baked (no stray rotation/scale after join) | 0 offenders (`transforms_clean: []`) |
| Orientation (glTF front = +z): A11 turret, A09 inn balcony, A08 tea-house veranda proud of the front | 3 / 3 pass |
| 8 placed buildings vs the P1.4 Blender world envelopes (`expected-envelopes.json`) | all within **0.49 cm** (limit 5 cm) |
| Textures | 69 images, all non-zero, mip-mapped; estimated GPU 88.0 MB |

## 2. Walking: routes and camera (`autotest-routes.json`, `camera-routes.json`)

14 routes x 5 camera-collision modes (A solids + roofs/jetties/balconies; B + cloth awnings; C + cloth + signs + pennants; D signs only; E pennants only).
Camera distance is measured to the head anchor (player y + 1.25); the unobstructed distance is 13.20 m (11.8 m behind, 6.6 m up, pitch 0.19).

| Route (mode A unless stated) | s | min cam m | median | share < 6 m | stuck | min side clearance m |
|---|---|---|---|---|---|---|
| Street axis, around the market cross (x = 2.6 at n 46–52), walk | 27.0 | 9.09 | 13.08 | 0 | 0 | 1.23 |
| Same, run | 12.4 | 9.73 | 13.26 | 0 | 0 | 1.31 |
| Straight down x = 0 (**documents** the market cross as a solid) | 23.8 | 12.9 | 13.08 | 0 | **1** at (0, 47.6) | 0.03 |
| Turret corner pass (B04 corner, n 12–22) | 9.7 | 2.94 | 13.08 | 0.18 | 0 | 1.06 |
| Awning rows walk (x = -3.4, n 45–54) | 10.7 | 8.61 | 13.08 | 0 | 0 | 1.13 |
| Cross passage at n = 46 | 8.6 | 2.99 | 13.06 | 0.21 | 0 | 0.10 |
| Inn lane N–S and S–N (x = -19.2) | 8.3 | 12.98 | 13.08 | 0 | 0 | 0.86 |
| Inn diagonal N38 → N11 (1.8 s) | 1.8 | 2.95 | 3.56 | 0.94 | 0 | 1.27 |
| Inn diagonal N11 → N38 | 1.8 | 5.85 | 7.39 | 0.11 | 0 | 1.59 |
| Tea route N24 → N41 → N16 → **N17** (node as specified in P1.4) | 12.7 | 0.50 | 13.08 | 0.06 | **1** at N17 | 0.03 |
| N17 → N16 (leaving) | 6.1 | 1.46 | 1.46 | 1.0 | **3** | -0.01 |
| N16 → centre of the first gap between veranda posts → (36.16, 63.4) | 2.9 | 12.98 | 13.08 | 0 | 0 | 0.31 |
| Same, reverse (standing on the veranda facing out) | 2.9 | 0.54 | 2.64 | 1.0 | 0 | 0.31 |
| Junction cross street (west alley between B04 and B05, 1.34 m wide) | 23.1 | 2.84 | 10.47 | 0.31 | **1** (return leg, B04 wall) | 0.00 |

Camera speed in mode A stays below 130 m/s peaks (a one-frame 0.5 m "pop" counts as a pop); pennants raise it to 417–490 m/s.

### Does cloth, sign or pennant geometry belong in camera collision?

| Route | A (none) | B (+ cloth) | D (signs only) | E (pennants only) |
|---|---|---|---|---|
| Street axis walk: min camera m / pops | 9.09 / 2 | 9.09 / 2 | 9.09 / 2 | **3.32 / 4** |
| Street axis run | 9.73 / 3 | 9.73 / 3 | 9.73 / 3 | **3.45 / 6** |
| Awning rows walk | 8.61 / 0 | **3.17 / 9** | 8.61 / 0 | 8.61 / 0 |
| Cross passage | 2.99 / 7 | **1.20 / 10** (median 10.6, 44 % of time < 6 m) | 2.99 / 7 | 2.99 / 7 |

**Decision (measured): none of the three groups participates in camera collision.** Cloth awnings pull the camera to 1.2–3.2 m and pennant lines to 3.3 m with 4–6 pops per walk;
signs change nothing in these routes, are thin and sit at 2.5–3 m, so they are also left out (flag `cameraOnly` + `group: 'sign'`, switchable with `P2A.camGroups`).
Roofs (stepped bands), jetties/balconies, overhangs and arches stay as camera obstacles; they are the ones that put the camera inside a building.
Cost of the decision: with cloth and pennants excluded the camera can pass through an awning or bunting line; the cloth is single-sheet geometry with `side: DoubleSide`, so nothing
renders wrongly, but a rapid camera swing can show the awning from underneath. Not seen as a defect in the captured views.

### What limits the camera at the awkward spots (`camera-cause.json`)

Each case is run to its end, the camera settles for 1.5 s, then the unobstructed camera ray is tested against every camera obstacle on its own.

| Case | Settled distance | First thing the ray hits |
|---|---|---|
| Inn, after N38 → N11 (camera behind = north-west) | 8.23 m | **E03 wall box** at 8.52 m, then E03 roof band at 8.83 m |
| Inn, after N11 → N38 | 10.01 m | B06 roof band at 10.29 m |
| Tea-house veranda facing out | 2.80 m | **B17 wall** at 3.08 m, then the veranda balcony proxies at 3.56–3.78 m |
| Turret corner, after the pass | 5.73 m | B04 turret wall at 6.01 m |

So the "camera compression near the Merchants' Inn" is the inn's own massing behind the player when walking away from it; it settles at 8.2 m (62 % of full) and is **not** a proxy error.
The 2.95 m minimum in the 1.8 s diagonal is the camera still swinging while the route is only 4 m long. The veranda is a 1.5 m deep porch against a wall: the camera cannot sit behind the
player there at any setting, which is why it falls to 0.5–2.8 m.

### N16–N17

* N17 (37.6, 62.6) is 0.55 m from the veranda post at (37.06, 62.53). With the 0.34 m body radius and 0.20 m post half-width the player cannot stand on N17: the routes stop 0.49 m short, three stuck steps when leaving.
* Posts are 1.89 m apart centre to centre = **1.49 m clear**, so the veranda is passable (0.81 m slack on a 0.68 m body); routed through the middle of the first gap (36.16) the route completes with the camera at 12.98 m.
* Correction for P2-B: move N17 to the gap centre, (36.16, 62.30), or drop the post at (37.06, 62.53). The N16 → N17 segment stays 5.8 m.

### Other findings

* **Market cross (M01)** is a 2 x 2 m solid at (0, 49) on the street axis. A player cannot walk straight down the spine; the 2.6 m side bypass has 1.23 m clearance to the cross. This is a P1.4 plan feature, not a bug, but P1.4 route notes that assumed a straight spine need the bypass.
* **B04–B05 side alley is 1.34 m wide** (B04 north face n 19.83, B05 south face n 21.17), under the 1.5 m trail rule. The player can enter, gets stuck turning round (stuck 1) and the camera pops 29 times (min 2.84 m). Recommend closing it (gate or fence) or opening it to ≥ 2.0 m.
* **Unobstructed camera 12.92 m, not 13.20 m**: `clearDistance` subtracts a 0.28 m padding. This is the "11.55 m vs 11.8 m" shortening (11.8 − 0.28 = 11.52 horizontal) and exists on the first island as well.

## 3. Raised civic platform (`platform-test.json`)

Terrace steps (1.0 m, ~5 risers of 0.2 m) and Exchange Hall steps (another 1.0 m) were built from the real Medieval Village (`MV-Stairs_*`) stair modules; the walkable height field is ray-cast from their actual treads (0.2 m cells).

| Run | Time | End | Max step up | Airborne | Stuck |
|---|---|---|---|---|---|
| Ascend both flights, walk (n 56 → 77) | 10.1 s | y 2.01 (= support) | 0.22 m | 0 | 0 |
| Descend, walk | 10.6 s | y 0.01 | −0.22 m | 0 | 0 |
| Ascend, run | 4.65 s | y 2.01 | 0.22 m | 0 | 0 |
| Descend, run | 4.87 s | y 0.01 | −0.22 m | 0 | 0 |
| Ascend with a jump on the third riser | 6.75 s | y 1.01 | 0.22 m | 41 steps | 0 |
| Walk off the terrace edge (1 m drop) | – | y 0.01, phases grounded → airborne → landing | – | – | – |
| Walk into the terrace side from the ground | – | stays y 0, blocked at x = −14.0 | 0 | – | – |

Controller maxStep is 0.42 m; the 0.22 m maximum riser rise leaves a 0.20 m margin. Camera minimum while ascending is 12.8 m; descending toward the hall it drops to 2.9–3.1 m because the
player starts about 2 m from the face of the **temporary stand-in hall mass** (n ≈ 80) and the camera sits inside it. The real Exchange Hall needs a portico or door rule for the camera (P2-B). The terrace has no rail at its south edge: the 1 m drop is survivable but unprotected.

## 4. What was not tested

* No human keyboard/gamepad play session; no mobile touch input; no 390 x 844 layout check of the preview UI.
* Moving NPCs, quests, dragons: out of scope.
* Camera with the user rotating yaw by mouse around corners: only the default follow behaviour was simulated.
