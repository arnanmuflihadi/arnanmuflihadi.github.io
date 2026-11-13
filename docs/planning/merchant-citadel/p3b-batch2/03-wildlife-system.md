# 03 — Wildlife: habitats, population, behaviour (Quaternius-only ecology)

Code: `merchant-citadel-p2a/wildlife.js` (system), `data/island-flora.json` -> `habitats` (generated layout), `source/p3b2_scatter.py` (layout rules), `p3b2-tests.js` (tests and capture helpers). Switch off with `?wild=0`. Review knob: `?wscale=1.3` draws every animal 30 % larger (default 1.0 = natural size). The first version of this batch used Gobkit chibi animals; the owner decided to change the source, see [08](08-animal-source-change.md). The old results are kept in `evidence/superseded-gobkit/` and `visuals/superseded-gobkit/`.

## Ecological layout (habitat -> who and why)

| Habitat | Identity | Species (count) | Rules that place them |
|---|---|---|---|
| **A Merchant settlement** (sparse) | domestic, urban | chicks (4), cats (2), pug (1), pigs (2) in the artisan back yard (x -34..-25), the porters' yard and the quay service corner; small blue birds (6) perched on town roof ridges | yard animals >= 1.0 m from solids and >= 1.6 m from any pedestrian route (plus a per-animal wall margin, below); roof perches from the highest roof band of 17 buildings; **nothing in streets, doorways, counters or the hall forecourt** |
| **B Caravan Green** (moderate) | meadow, caravan animals | sheep (5), lambs (2, follow a sheep), llamas (2), horses (2), cows (2), birds (2 in trees), swallowtails (6 over flower patches) | ground animals in the annulus 10.5-17 m from the Green's centre: the **9 m core stays free for dragon landing** |
| **C Counting Crag** (sparse, rocky) | cliff and scree | red foxes (2) near the woods; eagles (2) orbit at 35-40 m; birds (2) on crag rocks | slope <= 0.3, >= 5 of 12 escape bearings free for 6 m, never on risers |
| **D Tea terraces** (sparse-moderate) | gentle agricultural | llamas (2) on gentle benches, birds (3) on the three nearest roofs and the one tree, swallowtails (6) | gentle benches only, animals never leave the walk mask |
| **E Cloudfall** (sparse) | water | birds (2) in the stream trees and on stream boulders (39 candidate perches), swallowtails (4) | no ground animals (stream-side ducks were Gobkit-only) |
| **F Tea Lookout and Stack** (very sparse) | scenic | bird (1) on the pavilion roof, swallowtails (2) | few and quiet |
| **G Sky Quay** (restrained) | harbour | birds (2) on crane / beacon / lamps, dog (1) at the service corner | **no perch inside the 11 m landing core**; cargo routes untouched |

65 agents: 27 ground, 20 birds (18 songbirds + 2 eagles), 18 butterflies (was 83). Counts are a design choice from what looked right at the follow camera, not from a performance limit (see 05); deterministic seeds (layout 20261113, behaviour 7). Dropped with the Gobkit set (no Quaternius equivalent): hare, doe, goat, marmot, hedgehog, squirrel, quail, hens/rooster, duck, golden pheasant, hoopoe, kingfisher, hummingbird, puffin, seagull, pigeon, budgie.

## Species table (13 Quaternius species + the Gobkit swallowtail)

All at natural size (no apparent-size boost any more). `h` = standing height of the posed bounds (birds: largest extent).

| Species | Source file | h (m) | Walk / flee (m/s) | Clips used | Notes |
|---|---|---|---|---|---|
| Sheep / Lamb | Farm Animals | 0.9 / 0.6 (same rig) | 0.7 / 2.8 | Idle, Walk, Run | graze with Neck+Head pitch; lambs follow a sheep |
| Cow | Farm Animals | 1.4 | 0.6 / 2.6 | Idle, Walk, Run | graze |
| Horse | Farm Animals | 1.7 | 0.9 / 5.0 | Idle, Walk, Run | graze; alert 10 m |
| Llama | Farm Animals | 1.6 | 0.8 / 4.0 | Idle, Walk, Run | **no graze** (long neck: head pitch does not reach the ground, checked in the browser) |
| Pig | Farm Animals | 0.85 | 0.6 / 3.2 | Idle, Walk, Run | rooting = graze |
| Pug | Farm Animals | 0.4 | 0.9 (calm, never flees) | Idle, Walk | |
| Dog | Animal Pack Vol.2 | 0.65 | 1.0 (calm) | Idle, Walking | |
| Cat | Animal Pack Vol.2 | 0.3 | 0.7 / 4.2 | Idle, Walking | flees at 3.5 m, prefers cover |
| Red fox | Animals Pack | 0.5 | 1.0 / 5.5 | one walk cycle | alert 14 m, flees at 10 m; flee = walk cycle at up to 2.8x |
| Chick | Animals Pack | 0.2 | 0.45 / 2.0 | one walk cycle | |
| Songbird ("Bird") | Animals Pack | 0.3 | flies 4.2 m/s | one flap cycle (0.67 s) | perches and hops between perches |
| Eagle | Animal Pack Vol.2 | 0.8 (span about 1.9) | soars 7 m/s | Flying, Idle (unused) | circles over the crag at 35-40 m |
| Swallowtail | Gobkit (kept) | 0.22 | 0.9 | fly, perch | the only butterfly |

**Clip alias layer.** The packs name clips differently, so `wildlife.js` maps them: idle = `Idle`, else a single-action rig (fox, chick, songbird) holds a standing frame of its walk/flap cycle with the clip rate set to 0; walk = `Walk` / `Walking` / the single action; run (FLEE) = `Run`, else the walk cycle at a higher rate; fly = `Flying` (eagle) or the flap action (songbird). The clip rate follows ground speed (`cs`, `csr` = metres one rate-1 cycle covers, estimates, **foot sliding not measured**). Procedural wing code was removed: all flight uses real clips.

## State machines

* Ground: IDLE, WANDER (to a validated point inside the activity radius), GRAZE, REST, LOOK_AROUND (slow yaw sweep), ALERT (face the player), FLEE (best of 72 candidate points: away from the player, line walkable, cover preferred, not beyond 2.6x the home radius), RETURN_TO_HABITAT (beyond 1.4x the radius). Alert habituation 14 s. Lambs follow a sheep.
* Songbird and eagle: PERCHED -> TAKEOFF -> FLY -> LAND -> PERCHED for songbirds (arc, banking, destination another perch 12-90 m away; takes off when the player is within 7 m or after 8-40 s; a single-perch bird flies a loop and returns); CIRCLE for eagles (orbit with altitude drift, clip rate 0.3-0.8 for soaring).
* Butterflies: FLY between flower positions, PERCH for 3-8 s with the real `perch` clip.

## Movement validation (every step)

Walk mask, slope <= 0.5, step <= 0.3 m, **a per-animal wall margin** (0.25-0.8 m: horse 0.8, cow 0.75, llama 0.55, pig 0.5, sheep 0.45, cat 0.28; the old fixed 0.28 m let long bodies clip walls) against the same obstacle list the player collides with (town solids, trunks, boulders, props), dragon-landing keep-outs, terrain height each frame, slope-aligned pitch/roll. A bounded fallback relocates a cornered, player-adjacent animal (counted; fired 0 times).

## Performance design

Skinned rigs cloned with `cloneSkeleton`, one mixer per agent. Distance LOD for logic and mixers (see 05), shadow casting only within 26 m, hidden beyond 130 m. The 13 GLBs are 2.3 MB (+ 0.4 MB swallowtail). Fauna albedo is multiplied by 0.86 (white wool and feathers clipped under this scene's lighting).

## Dragon coexistence

Keep-outs: Caravan Green core 9 m, Sky Quay core 11 m, Shoulder Table 6.5 m, Hall lawn 7.5 m, Counting Stone 3.5 m. No ground animal and no perch is inside them (tested). **Untested** with a dragon: the free-flight controller does not exist in this branch; birds do not yet react to a flying dragon and there is no collision with animals by design.
