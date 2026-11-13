# 08 — Human playtest checklist

**Nothing below has been done by a person.** Everything in 03 and 04 is an autopilot, a scripted key session, or a measurement. This list is what a human should try, and the cases the tests flagged as needing a human judgement. Run: `node merchant-citadel-p2a/server.mjs --port 4180`, open `http://127.0.0.1:4180/merchant-citadel-p2a/index.html` (W forward, A/D strafe, Q/R turn the camera, Shift run, Space jump, drag to look). Spawn: the arrival court.

## A. The route (about 4 minutes)

| # | Do | Look for |
|---|---|---|
| 1 | Walk east along the cross lane to the warehouse lane, turn north | The lane looks like a working lane, not a canyon (the follow camera sees roofs 10–12 m high over 4.6 m of lane). Does B13's gable read as a warehouse (two doors, seal, crates)? |
| 2 | Stop at B13's lane doors, turn the camera all the way round | Camera position at 2.8 m behind the wall; does the character fade help or distract? |
| 3 | Continue to the cross street, turn east into the court | First view of the court: loading doors, the hoist jib with a crate, the tally table; is it clear what the space is for? |
| 4 | Walk under B13's canopy to the loading doors, then to E04's loggia | Can you walk in and out of both without catching on goods? Does the camera stay stable while you turn under the canopy? |
| 5 | Turn near the wagon (the camera used to drop to 0.5 m there) | The camera should no longer jump; report if it does |
| 6 | Go through the court's east opening onto the porters' path, walk north to the gate | Path width (2 m) and fence; does it feel like a back path to the lookout? |
| 7 | Take the gate to E05's east door and the lookout terrace | The terrace furniture is at its new place; can you reach the door? |
| 8 | Walk west along the tea lane in front of E05 | Gallery posts, tables, awnings: is this the quiet scenic district's entrance? Can you pass the posts comfortably? |
| 9 | Go round the corner to E05's west door on the bazaar's east market lane | Is it clear from the bazaar that the tea lane begins here? |
| 10 | Try to enter the 2.2 m slot between E05 and E06 and the pocket behind B14 | Both are closed by fences; do they look arbitrary? |

## B. Cases the tests flagged (judge these by hand)

1. **The lane canyon:** the follow camera looking up the warehouse lane (`?autotest=views&names=p5-quarter-gameplay`); camera minima of 2.78 m at lane spots with walls on both sides.
2. **The path gate and the strip behind E04's strongroom wing:** camera minima of 1.5–1.8 m and 2.0 m; roofs of E06 and E04 are the cause.
3. **The E04 ring** (walk round E04 at about 1.8 m off the wall, both ways): the character fades to 0.15 and the camera reaches 1.1 m on the strongroom side. Is that acceptable, or should the wing move or shrink?
4. **E05's gallery:** the balcony rails are camera obstacles; minima 1.56 m at the lane edge. Do the posts and tables block the way under the gallery?
5. **The east market lane between the East Hall and E05** (3.5 m wide): camera 2.78 m for a quarter of a turn.
6. **The low-prop camera rule:** walk past barrels, crates and the wagon; does the camera ever clip through a prop in a way that looks wrong? (`?lowprops=0` restores the old behaviour.)
7. **Mouse-rotated camera round corners:** untested; try B13's and E04's corners and E05's gallery.
8. **Fade opacity** at 0.15–0.45 in motion: not offered as acceptable in general.
9. **Closed fences** (slot, pocket) and the **tea-green awnings**: do you accept them?
10. **E05's second storey** (deviation) and the **dark roof of B13** from the lane.
11. **Feel at running speed** (Shift): do the gate, the court's east opening and the lane corners catch the character?
12. **Performance feel** on the target device: not measured here.

## C. Record

For each case: pass / fail / comment, device, browser, and whether it was walked with keyboard, mouse or pad. Do not mark a case passed because the automated test passed.
