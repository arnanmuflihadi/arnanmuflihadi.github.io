# Guided playtest checklist — Central Bazaar (about 10 minutes)

Start the preview and open it in a normal browser window (not a hidden pane):

```bash
node merchant-citadel-p2a/server.mjs --port 4180
```

`http://127.0.0.1:4180/merchant-citadel-p2a/index.html` — W A S D / arrows move, Shift runs, Space jumps, Q / R turn the camera, drag to look. The buttons teleport. Tick each line; write what you saw where it is not as described.

## 1. Arrival and the street (1 min)
- [ ] Press **Arrival**, walk north along the market street. The Exchange Hall tower stays visible at the end of the street; the two halls and the awning rows frame it.
- [ ] At the junction (n ≈ 20) look west and east: both cross streets are open and 4 m wide.

## 2. Entering the Western Hall — provisions (2 min)
- [ ] Press **Western Hall** (or walk to n ≈ 40, x ≈ −13). The red-brick threshold marks the entrance; blue awnings sit over the outer bays, the loaf and crate signs hang over the centre.
- [ ] Walk in along the aisle. Bread, cheese, fish and sausage counters on the east side; fruit, barrels and hay on the west and north. You can walk the whole aisle; the bench at the far end blocks the centre, so turn before it.
- [ ] **Turn around inside** (hold A or D): the camera stays 4 m or more behind you and the explorer does not cover the screen.
- [ ] Walk into a counter, a barrel, a table: you are stopped each time (nothing can be walked through). Walk between the posts: they stop you too.
- [ ] Leave through the **east side**: you arrive in the back lane between the hall and the blue awning row, 2.5 m wide.

## 3. Crossing the market to the Eastern Hall — crafts (2 min)
- [ ] Walk round the **market cross** clockwise and counter-clockwise: 3.85 m of room on each side.
- [ ] Enter the Eastern Hall from the west side opening. This hall is different: plaster bays with windows at the front and back, a closed east side, a wall of hanging cloth at the north end, a rug, a book stand, pottery and shelves.
- [ ] Leave by the south entrance (the 4 m opening between the windowed bays) and back to the red-brick threshold.

## 4. The shops (1 min)
- [ ] Press **East shops**: B14 (registry office, scroll sign) and E06 (cloth seller) face the bazaar; walk along their fronts.
- [ ] Press **Potter** (E07, north-west): walk along its front; the jar sign hangs over the door.

## 5. Camera and fade (2 min)
- [ ] Walk out onto the Exchange Hall steps and stand on the porch landing facing south: the explorer turns ghost-like when the camera is squeezed against the facade and returns to solid when you walk away. No flicker.
- [ ] Stand on the tea-house veranda and turn: same behaviour.
- [ ] Toggle **Cloth blocks camera** and walk under an awning row to see why it is off by default (the camera is pulled in close).

## 6. Return to the main street (1 min)
- [ ] From either hall walk back to the spine, then south to the arrival court. No invisible walls; no spot where you cannot turn.

## 7. Report
- [ ] Anything that looked flat, repetitive or generic (which building, which view).
- [ ] Any place you got stuck, saw through a wall, or lost the character.
- [ ] Frame rate you saw and the machine you used (the measurements in 05 are from one Apple M4 Pro).

Debug switches: `?fade=0` no character fade, `?postsblock=1` thin posts block the camera, `?merge=none|scene|district` geometry merge mode, `?smap=1024|2048|4096` shadow map, `?ao=0` no baked AO, `?matcache=0`, `?prewarm=0`.
