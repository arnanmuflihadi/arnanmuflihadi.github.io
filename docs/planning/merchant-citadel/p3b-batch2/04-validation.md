# 04 — Validation (scripted tests in the real preview; not a human playtest)

Town/landscape data in `evidence/validation/`; **wildlife data was re-run after the Quaternius swap** in `evidence/validation-quaternius/` (`p3b2q-*.json`); the Gobkit results are in `evidence/superseded-gobkit/`. Controller, camera, character and collision modules are the unmodified production files (SHA-256 of the six files re-verified). The preview supplies its own terrain collision as in batch 1.

## Town and landscape regression with flora and wildlife present

*Run in the Gobkit stage; terrain, collision, town, flora and the routes were not changed by the animal swap (flora, trunks, perches and keep-outs verified byte-identical in the regenerated data) and animals are not collision obstacles, so these were **not re-run** for the swap. The wildlife sections below were.*

| Check | Result |
|---|---|
| 17 landscape routes (quay, court, street, terrace, hall doors, crag ascent/descent, shoulder table, tea promenade, porters loop, Green road, bridge) | **17/17 pass** (no stuck waypoint, end within 0.6 m) |
| A* reachability, 11 pairs | all found |
| Town pedestrian network (batch 5, both directions) | **65 edges, 0 failed**, minimum node clearance 0.409 m (identical to batches 3-5) |
| Rim sprints from 11 starts, quay jump test, void placements | none left the island; all falls recover |
| Camera yaw sweeps at 24 landscape spots | minimum 2.79 m (crag upper 2.79, east podium edge 2.79, crag summit 2.92); none collapses; groves are handled by the foliage dither |

Trunks (83) and boulders (126) are solid body proxies; none blocked a route or a network edge.

## Wildlife spawn validity (27 ground agents, 20 birds, 18 butterflies; final code)

| Check | Result |
|---|---|
| Ground agents on a walkable cell | 27/27 |
| Inside a solid proxy (per-animal margin 0.25-0.8 m) | 0 |
| Inside a dragon-landing keep-out | 0 (birds perched in keep-outs: 0) |
| Maximum slope under an agent | 0.288 (limit 0.5) |
| Minimum clearance to a town solid | 0.489 m (the margin of the animal concerned is respected; a first run with the fixed 0.28 m margin gave 0.28 m, which is why the margin is per animal now) |
| Feet vs support height | maximum error 0.000 m |
| Per habitat | A_settlement: 9, B_caravan_green: 13, C_counting_crag: 2, D_tea_terraces: 2, G_sky_quay: 1 (E and F have birds and butterflies only) |

## 600 s ambient simulation at full rate (nobody near; 4.5 s wall time)

Walkability, solid contact, keep-out entry, ground error > 2 cm, slope > 0.5 and leaving 3x the species radius: **all zero**. Largest height step between samples 0.089 m. Distance walked in 10 minutes (mean per species, m; 600 s sim): Chick 104, Cat 60, Pug 62, Pig 61, Sheep 93, Lamb 158, Llama 98, Horse 85, Cow 42, RedFox 121, Dog 117. Cornered-relocation fallback: 0 times.

## Reactions to a walking player (2.1 m/s, 14 m approach, then retreat)

| Species | Alert at (m) | Flee at (m) | After the player left |
|---|---|---|---|
| Sheep | 5.9 | 2.95 | back near home, legal |
| Lamb | 5.9 | 2.5 | follows its sheep |
| Cow | 5.9 | 2.96 | legal |
| Horse | 9.9 | 4.9 | settles 11.6 m from home (radius 10; returns beyond 14 m) |
| Llama | 9.0 | 4.5 | legal |
| Pig | 5.0 | 2.3 | legal |
| Cat | 7.0 | 3.5 | legal |
| Red fox | 13.9 | 9.9 | legal |
| Chick | 2.9 | 1.8 | legal |
| Pug, Dog | calm | calm | deliberately never flee |

Final positions were walkable and outside keep-outs for all 11. Birds: the songbird completes PERCHED -> TAKEOFF -> FLY -> LAND -> PERCHED and lands exactly on the destination perch (0 m error) in four habitats (settlement roofs, Caravan Green tree, tea terrace roofs, Sky Quay props; flights of 7.8-16 s; destination never in a keep-out); eagles circle at 35.5-40.5 m radius 32 m over the crag. The tea-terrace and Cloudfall birds had only one shared perch in the first run: fixed (4 and 39 candidate perches now). A first reaction bug-check showed the old test list still named Gobkit species: the test lists were rewritten.

## Animation quality (inspected in the browser; `visuals/quaternius/`)

* All 13 Quaternius rigs and the swallowtail load, skin and loop (no console errors, 0 failed requests, 13 animal GLBs + swallowtail fetched with 200). Farm animals and pug use `Idle`/`Walk`/`Run`; cat and dog `Idle`/`Walking`; eagle `Flying`; fox and chick one walk cycle; songbird one flap cycle. `p3b-q-clip-phases-fox-chick-bird.jpg` shows 8 phases per cycle: the fox trots, the chick waddles subtly, the songbird flaps (small wings).
* Grazing / rooting: Neck + Head pitch (sheep, lamb, cow, horse, pig). The sign was wrong on the first try (the head went up); fixed and checked (`p3b-q-graze-pose-check.jpg`). Llamas do not graze (the head pitch does not reach the ground on a long neck).
* Real clips replaced the procedural wing flap and the Gobkit chibi idle/walk.
* **Foot sliding is not measured** (`UNVERIFIED`): clip rate follows ground speed by an estimated `cs`/`csr` per species. The fox, chick and songbird idle is a held frame of the cycle (rest poses look acceptable in the portraits, not tuned). Eagle `Idle` is unused (eagles never perch; its pose looked like a stoop).
* Orientation: models face +Z; ground alignment pitch/roll limited as before.
* Capture limits: follow-camera encounter shots show small animals as specks (cat, chick, pug, fox, songbird); close-camera variants exist for them (`*-close.jpg`). The fox encounter shot (`p3b-q-encounter-crag-fox.jpg`) caught the fox already fleeing behind a boulder (weak image; the flee GIF is the evidence). The songbird flight GIF is dominated by landscape; the songbird is hard to track at its size.
