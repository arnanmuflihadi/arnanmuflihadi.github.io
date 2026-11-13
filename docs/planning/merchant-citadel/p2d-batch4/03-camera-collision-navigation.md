# 03 — Navigation, collision and camera

All runs use the game's **unmodified** controller, follow camera, character and collision module in the isolated preview (`merchant-citadel-p2a/`, hashes in [evidence/production-code-sha256.txt](evidence/production-code-sha256.txt)). Autopilot routes use the same code path as keyboard play at a fixed 60 Hz; they are not a human's hands. A route passes only if it reaches its target within 0.7 m with no stuck state (no progress for 2 s). Preview-side camera rules that differ from the island's are listed in section 6. Evidence: `evidence/*.json` (final runs; `*-default.json` are the same suite before the low-prop camera rule, `*first-run*` the first one).

## 1. Network

**49 nodes standable, 63 of 63 edges pass in both directions** ([nodes](pedestrian-network-batch4-nodes.csv), [edges](pedestrian-network-batch4-edges.csv), [json](pedestrian-network-batch4.json)). Batch 3 had 38 / 48. Added: N47 (B13 lane doors), N48 (loading bays), N49 (tally loggia), N50 (E04 lane door), N51–N54 (porters' path), N58 (E05 west door), N59 (E05 east door); N33 (service court) is now inside the built slice. **N41 moved from n 58 to 59** (the gallery posts of E05 stand 0.6 m from the P1.4 position). The smallest node clearance is N17 (tea-house veranda, 0.41 m between two posts, unchanged since P2-A); the smallest new one is N59 at 0.72 m, between E05's wall goods and the terrace furniture.

First run of the new edges: five failed (lamp posts in the path, P1.4 terrace bench and table in the gate). Both were corrected and the full set re-run; the failure files are kept as `network-first-run.json`.

## 2. Routes

Final run, 35 of 35 pass (17 from batch 3 and 14 new routes and 4 ring walks):

| Route | s | camera min | camera < 3 m | min opacity |
|---|---|---|---|---|
| lane south → north / north → south (N36…N14) | 19.7 / 19.7 | 3.3 / 5.2 m | 0 % | 0.94 / 1 |
| bazaar → warehouse gable (N04 → N47) | 20.2 | 4.6 m | 0 % | 1 |
| court → loading bays and back | 13.2 | 1.8 m | 2.3 % | 0.46 |
| court → tally loggia and back | 12.5 | 3.1 m | 0 % | 0.87 |
| lane → counting house door and back | 10.0 | 3.1 m | 0 % | 0.89 |
| court → porters' path → E05 east door → terrace (and back) | 22.9 / 22.9 | 2.9 / 3.5 m | 1.7 / 0 % | 0.82 / 1 |
| tea lane in front of E05 and back | 17.2 | 7.1 m | 0 % | 1 |
| bazaar east lane → E05 west door → bazaar NE corner and back | 17.9 | 3.8 m | 0 % | 1 |
| E05 east door from the terrace and back via the gate | 11.8 | 2.3 m | 7.6 % | 0.59 |
| **loop east** (bazaar S → lane → court → path → gate → E05 east door → terrace → tea lane → bazaar NE → east market lane → bazaar), forward / reverse | 70.6 / 70.7 | 2.9 / 3.5 m | 0.4 / 0 % | 0.81 / 1 |
| street → cross street → court → lane → arrival court → street | 42.8 | 3.6 m | 0 % | 1 |
| ring walk round B13, ccw / cw (1.8 m off the walls) | 27.2 / 27.1 | 3.9 / 1.9 m | 0 / 3.0 % | 1 / 0.51 |
| ring walk round E04, ccw / cw | 30.0 / 30.3 | **1.2 / 1.1 m** | 7.7 / 10.9 % | **0.16 / 0.15** |

**Ring walks are stress tests, not play** (a grid search joins anchor points on all sides of a building 1.8 m off the wall and the real controller walks the result). E05 has no ring walk because its south slot is closed on purpose (below); the loops circle the E05–E06–B14 block instead. **The E04 ring drives the character to its minimum opacity (0.15) at the strongroom wing's east side** and that is not treated as acceptable (section 5).

## 3. Doors, corners, props

* **Doors:** each commercial door has a node on free ground in front of it and an edge that passes both ways (B13 lane doors N47, loading doors N48, E04 lane door N50, loggia door N49, E05 front door via N41, west door N58, east door N59). Doors do not open (no interiors in scope).
* **Corners and props:** the ring walks run every corner, lean-to post and prop edge of B13 and E04 (clockwise and counter-clockwise); the loops pass E05's gallery posts. **Solid props: 248 of 248 solids** (the ten batch-2/3 shops and halls, B13, E04, E05 and 105 dressing items) stop the player from every free direction of eight (closest approach to a footprint edge 1 mm; none ended inside; flat rugs and goods on counters have no proxy by design). New: B13 14 solids (10 props, 2 posts, wall, counter), E04 9 (3 posts, 3 props, 2 walls, counter), E05 16 (11 props, 4 posts, wall); batch 4's dressing (fences, lamp posts, goods) is in the 105. The hoist jib has no proxy (it is 5 m above the ground).
* **Placement:** 22 of 22 buildings within 5 cm of the Blender-built envelopes (B13 and E04 −2.9 cm at the lane side where their sign arms project); every kit node within 0.005 cm of its Blender bounding box; no kit node carries a transform.
* **Real-keyboard session** (scripted Playwright key events, not a human): 16 of 16 waypoints from the arrival court to the lookout terrace and back to the bazaar, [log](evidence/real-keyboard-session.json), [screenshots](visuals/camera).

## 4. The camera: what was found and what was done about it

The brief asked for the cause of any severe compression to be investigated rather than hidden by the fade. The method (`?autotest=compress`): a 360° turn in 24 steps, each settled for 1.5 s, at eight positions 1.8 m off each wall of B13, E04, E05 (and B10, B12, E01 of batch 3 for comparison) and at 12 walking nodes; for every yaw the camera ray is tested against each camera obstacle separately, so the compression is attributed to the obstacle that causes it.

| Building | yaws with camera < 3 m | < 1.5 m | minimum | what causes it |
|---|---|---|---|---|
| B13 | 6 % | 0 | 2.93 m | its own walls |
| E04 | 10.9 % | 1 % | 1.47 m | its walls, the wing's roof (strongroom side) |
| E05 | 22 % | 0 | 1.56 m | its walls, the neighbouring B03/E06 roofs and walls, its balcony |
| B10 / B12 / E01 (batch 3) | 33 / 30 / 29 % | 14 / 11 / 2 % | 0.84 / 0.84 / 1.4 m | roofs of the building and of B11 |

The new buildings compress the camera **less** than the artisan lane of batch 3 in this test. The cases below were *spatial or configuration* causes and were corrected:

1. **The E05–E06 slot (spatial).** Standing in the 2.2 m gap between two buildings of different heights, 92 % of yaws were under 3 m, the median 1.13 m and the minimum **0.52 m**, caused by E06's roof and wall. It is a dead end seen from nowhere; a player can walk in. **Closed by two fences** (the west one 0.8 m inside the mouth, so that E06's west-facing door stays clear). A first position (at the mouth) left a sliver at the south-west corner, found by a flood fill of the walkable area; the final positions were checked the same way (`slot interior unreachable`, every other node still reachable). Cost: E05 cannot be walked round.
2. **A dead-end pocket behind B14 (spatial).** The autopilot jammed in the 1.8 m gap between the lane fence and B14's wall. Closed by a fence (19.4, 37.3).
3. **Low floor props are camera obstacles (configuration).** The camera ray starts at head height (1.25 m) with a radius of 0.28 m; the preview's camera proxy of an oriented prop is its axis-aligned bound, so a player turning within 0.25 m of the wagon (2.9 x 2.0 m bound, 1.2 m high) had the camera pulled to its 0.5 m minimum for 0.2 s (opacity 0.42 → 0.18); seen in the real-keyboard session. **Floor props whose top is at or below 1.25 m are no longer camera obstacles** (still solid for the body); `?lowprops=0` restores the old behaviour. Effect on the stress tests: the 0.5 m minima of the B13 and E02 ring walks disappear (to 3.9 and 8.7 m), B13 clockwise 1.9 m, E04 0.5 → 1.1–1.2 m; mean share of the ring walks under 3 m 19.7 → 19.0 %. Stationary spots do not change. It was not in the P2-A to batch 3 camera configuration; it is a preview-side rule like the post, cloth and sign rules.
4. **Roof-proxy resolution (configuration, no effect).** The roof proxies were three stepped boxes per roof; six steps follow the roof more closely (they never lie inside it). On the routes that nothing else changed between the two runs, the share of time under 3 m moved by at most 2.5 points and the minima by under 0.05 m; so roof approximation was **not** the cause of the ring-walk compression. Kept for accuracy (`P2D_ROOF_STEPS=3` reproduces the old data; `scene-roof3.json`).

Remaining, not corrected:

* **Lane spots** (N47 at B13's gable, the counting house lane door, the east market lane by E05): 20–40 % of a full turn has the camera at 2.8–3 m with walls on both sides. At a 16:9 viewport the character covers more than 25 % of the screen in **none** of the sweeps at 11 of 12 nodes (1 % at the path gate); an earlier run of the same test, at the narrower pane of the browser, showed 14–46 %, so **the figure depends on the viewport** and the test is now fixed to 1280 x 720 (`hall-camera.json`).
* **The path gate (N54)** and **the strip behind the strongroom wing** (N52): minima 1.5–1.8 m and 2.0 m; causes: E06's roof, E05's east wall, the wing's roof.
* **The E04 ring** (1.1 m, opacity 0.15), see above.

## 5. The character fade

The preview-side fade (opacity from camera distance with a time filter) is **provisional**. The new quarter's walking routes have a minimum opacity between 0.46 (the loading bays) and 1.0; the lowest values (0.15) are in the ring-walk stress tests. In motion (`fade-motion.json`, nine sequences incl. three new: east lane and court, porters' path, tea lane) the largest opacity change in one frame is 0.10 (0.18 at the Exchange Hall porch steps of batch 2) and the minimum opacities are 0.43 (east lane and court, at the loading bays), 0.81 (porters' path), 1.0 (tea lane). 14 % opacity occurs only in ring-walk stress tests and at the porch steps; it is not offered as a general solution. **Direct playtest cases** are in [08](08-guided-playtest-checklist.md).

## 6. Preview-side camera and collision configuration (differences from the island)

| Rule | State |
|---|---|
| Structural posts (≤ 0.5 m) | solid for the body, excluded for the camera (batch 2) |
| Cloth, signs, pennants | excluded from camera collision (batch 2) |
| Lean-to roofs | no camera proxy (batch 3) |
| **Floor props ≤ 1.25 m tall** | **solid for the body, excluded for the camera (batch 4)** |
| Roof proxies | six steps (batch 4; three before) |
| Open arcade roofs (market halls) | shell, no slab (batch 2) |
| Character fade | preview-side, provisional |

Everything else, including the follow camera's inward and outward rates, is the island's code.

## 7. What the tests do not show

Human speed and feel; mouse-rotated camera round the new corners (only Q/R key turns and stationary sweeps); gamepad and touch; the fade on the first island; interiors; moving carts; many characters.
