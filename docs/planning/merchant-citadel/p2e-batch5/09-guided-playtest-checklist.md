# 09 — Guided human playtest checklist (about 25 minutes)

**Nothing below has been done by a person.** Run the preview from the worktree root:

```bash
node merchant-citadel-p2a/server.mjs --port 4180
```

Open `http://127.0.0.1:4180/merchant-citadel-p2a/index.html` (default 30 m cells, shadows on). Controls: W forward, A/D strafe, Q/R turn the camera, Shift run, Space jump, drag to look. Useful switches: `?merge=none`, `?lowprops=0`, `?shadows=0`.

| # | Do this | Judge |
|---|---|---|
| 1 | Start at the arrival court, walk north along Merchant Street to the bazaar | does the hall's tower pull you forward? does the street feel like a place, not a corridor? |
| 2 | Walk round the market cross and through the awning rows | is movement smooth; do the awnings or posts catch the character? |
| 3 | Climb the terrace stairs, walk to the seal in the middle, turn 360° | is the terrace the town's centre? does the hall dominate **from here**? |
| 4 | Walk to the hall steps and the forecourt rail; turn round and descend | does the rail feel like a deliberate balustrade or a wall that blocks the doors? (decision: keep / open the centre bays) |
| 5 | Visit B15's door (west) and B16's door (east); turn round at each | do the two tower houses read as different trades? is the assay balance / map board legible at walking distance? is the camera comfortable? |
| 6 | Walk round B15 and B16 on the plaza, then off the terrace's side and south edge | no stuck states; the 1 m drop at the south edge is acceptable? |
| 7 | West: Artisan Lane, all the way round B10 / B11 / B12 | is the 0.75 m gap between B10 and B11 enterable? is the canyon camera acceptable? |
| 8 | East: warehouse lane, service court, counting-house loggia, porters' path to the lookout | the closed fences (slot, pocket) feel arbitrary? camera at the path gate (1.8 m)? |
| 9 | Tea route: E05 front, the veranda of the tea house | read the E05 sign: leaf, or heart? turn the character on the veranda: does it fade too far? |
| 10 | Jump on stairs and onto the terrace edge; run down both flights | any bounce, stuck frame or airborne stair step? |
| 11 | Rotate the camera with the mouse at 3 narrow places (alley, path gate, tower door) | does the camera pass through walls or collapse? (not tested by me) |
| 12 | Load `?merge=none`; compare feel with the default | any visible difference or hitch? |
| 13 | Open `?autotest=suite` only if you want to re-run the scripted tests (it rewrites `merchant-citadel-p2a/evidence/`; run in a copy) | — |

Note on what you see: the ground, sky and absence of trees are stand-ins. Frame rate: watch for hitches and tell me the machine; **I did not measure frame rate validly in this batch**.

Please record: what felt wrong (with the spot), what felt right, the machine and browser, and whether you would approve P2-B construction as it stands.
