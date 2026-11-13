# Camera validation (P2-A closeout)

Evidence: `merchant-citadel-p2a/evidence/` — `autotest-routes.json`, `camera-routes.json`, `camera-cases.json`, `camera-cause.json`, `camera-shots.json`, `cam-*-fade-*.png`. All runs use the game's **unmodified** `createFollowCamera` and `createPlayerController` (SHA-256 of `camera.js`, `player-controller.js`, `character.js`, `input.js` and both `collision.js` files identical before and after the closeout: `baseline-p2a/PRODUCTION-MODULES-SHA256.txt`). `git status` shows only the two new untracked folders.

How to read the numbers: the follow camera sits 11.8 m behind and 6.6 m above (13.20 m to the head anchor, 12.92 m once its 0.28 m padding is taken off). It moves **inward fast** (rate 32/s) and **outward slowly** (4/s) and lifts when squeezed (`camera.js`). "Pops" in the route tables count frames in which the camera distance changes by more than 0.5 m; nearly all are that designed fast inward move when a corner swings the camera into a wall and are **not defects**; the slow outward recovery is smooth.

## 1. Decisions

| Question | Decision | Evidence |
|---|---|---|
| Cloth awnings in camera collision | **No** (confirmed) | with cloth on: awning rows 8.6 → 3.2 m min, cross passage 9.6 → 1.2 m, 13 vs 2 pops (modes G vs F) |
| Pennant lines | **No** (confirmed) | spine walk min 12.3 → 3.3 m (mode H) |
| Signs | **No** (confirmed) | no effect on any route; thin, 2.5–3 m up |
| **Thin posts (0.4–0.5 m: porch posts, awning-row posts, the market-cross post)** | **New: ignored by the camera** | spine walk (corrected route round the cross): min 3.64 → **12.25 m**, pops 15 → 0; spine run 4.33 → 12.68; cross passage 2.99 → 9.61; tea west oblique 0.50 → 12.98. The 4 m market-cross post sat exactly between the camera and a player north of the cross |
| Roofs (stepped bands), balconies, jetties, overhangs, arches, walls | Stay camera obstacles | they are what keeps the camera outside buildings |
| Character fade when the camera is squeezed | **Adopted, preview-side only** | section 3 |
| Change to the production camera or controller | **None needed** | section 4 |

Implementation of the decisions: data tags (`group`), `P2A.camGroups` / `P2A.camOff` in `p2a.js`; `?postsblock=1` restores the P2-A behaviour. If posts are adopted in the island's collision data, they take `cameraOnly`-style exclusion in the camera's obstacle list; no change to `camera.js`.

## 2. The four critical cases

Mode F (closeout default), fade as noted. "Cov" = share of the viewport covered by the character's projected bounding box.

| Case | What limits the camera | Route result | Worst yaw sweep (360° turn in place) |
|---|---|---|---|
| **Tea House veranda** | The 1.5 m-deep porch against B17's wall (3.1 m) and the balcony proxies (3.6–3.8 m) when facing out | N16→N17: camera 12.98 m, no pops. N17→N16 (facing out): min 1.50, median 3.09 m | at N17: min 1.49 m; character fills > 25 % of the view 37 % of the time → **0.8 % with fade** (max effective cover 0.26) |
| **Merchants' Inn** | The inn's own wall (8.52 m) and roof band (8.83 m) when walking away from it: settles at 8.2 m (62 % of full). Not a proxy error | N38→N11 min 3.44 m (was 2.95; the 1.8 s route is shorter than the swing), N11→N38 min 5.85, lane N–S 12.98 | at N38 min 3.10, never over 25 % cover; at the inn door min 2.87 |
| **Tower corner (A11 turret, B04)** | B04's turret wall (6.0 m) and wall box (7.7 m) | turret pass min 2.91 m (8 inward pops), turret hug min 8.76, west cross street min 4.07 (23 inward pops at the 90° turns) | standing at the turret foot facing away: min 0.51 m, cover > 25 % for 40 % of the time → **0 % with fade** (max effective 0.21) |
| **Exchange Hall approach** | The hall's front wall a few metres behind the stair top (N08) and the porch | stairs up: 12.94 m, 0 pops; stairs down: min 2.97 m (starts at the porch, recovers within 1 s); porch landing: min 0.97 m | at N08 min 2.79 m (max cover 0.28); on the porch landing facing out: min 0.94 m, cover > 25 % for 64 % of the time → **0 % with fade** (max effective 0.20) |

Screenshots with fade off/on: [`closeout/visuals/camera/`](visuals/camera) (`cam-tea-veranda-facing-out-fade-*`, `cam-hall-porch-facing-out-fade-*`). The production camera's own lift raises the view over the player in these spots (it looks down at the paving), so nothing is hidden by walls; what was wrong is that the character's back fills the lens. The fade makes it a ghost; the surroundings stay readable.
The inn-door and tower-foot screenshot positions I chose did not actually compress the camera (12.9 m) and are not evidence; the yaw-sweep rows above are.

## 3. Smallest effective solution for severe compression

Options tried or considered:

| Option | Result |
|---|---|
| **Character obstruction fade** (opacity ramps from 100 % at 3.4 m to 14 % at 1.3 m camera distance; `P2A.fade`) | Cuts the time the character covers more than a quarter of the screen from 37–64 % to 0–0.8 % in the three squeezed cases. Zero collision, controller or camera code changes. No extra draw calls (the explorer's materials are `transparent`). Cost: ghosted limbs overlap slightly (depth write stays on). **Adopted** |
| Adaptive camera repositioning | Not built. The camera already gains elevation when squeezed; above the porch roof and hall the camera cannot go higher than the roof bands. Any change would be a camera-controller change without a demonstrated need |
| Camera framing change (shorter follow distance in the courts) | Not needed: the compressed spots are facade-hugging positions, not wide spaces |
| Small spatial changes | Applied where they fixed a defect (B04, N17, N29/N30), not to hide compression |
| Interaction-position changes | The one real candidate: when the Exchange Hall and the tea house get interactions, put the interaction point **in front of** the porch/gap (N08, N16) so the player faces the building with the camera behind in open space, not on the threshold |

## 4. Regression check against the first island

The production camera and controller are untouched, so first-island behaviour cannot regress through this work (hashes above). The fade and the thin-post rule live in this folder's preview and are switchable (`?fade=0`, `?postsblock=1`). To carry the fade to the island later it would be a character-material opacity update from the existing camera distance (`updateFade` in `p2a.js`, ~6 lines); I have **not** tested it on the island's own spaces and do not claim to have.

## 5. Still open

* Human check in the preview of the fade's look (the stills show it working; motion at the 0.14 minimum opacity is not judged).
* Fade with the explorer's cloth/hair at high opacity ramps shows slight overlap; acceptable for a preview, to be reviewed before it goes near the game.
* The camera is only validated for the default follow behaviour; mouse-rotated yaw round the corners was simulated only through the 360° turn-in-place sweeps.
