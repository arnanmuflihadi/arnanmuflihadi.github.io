# 02 — Civic Terrace and Artisan Lane decisions: tested alternatives and the smallest effective changes

**Nothing in the town was changed.** Every alternative below was tested in the isolated preview by overriding the collision list in memory, with the game's real controller and camera, fade on; `scene.json` and the kit are untouched (results: `evidence/targeted-tests.json`, images `evidence/p3a-*.jpg`). Scripted, not a human playtest. A "spin" is the character standing still while the camera yaw sweeps 360° in 24 steps; values are minimum camera distance / share of yaws under 3 m / minimum character opacity.

## 1. The forecourt rail

**Finding: the rail treated a symptom. The cause is the porch roof's camera proxy.** When the player stands near the porch and the camera swings round, it meets the six camera-only bands of the porch roof and is pulled onto the character. Making those bands camera-transparent (the rule already used for lean-to roofs since batch 3) removes the collapse without any rail.

| Variant | walk to the doors (0, 79.3) and back | spin at the doors | spin on the forecourt (0, 75.4) |
|---|---|---|---|
| V0 batch 5: rail closed | doors unreachable; 2.96 m / opacity 0.83 | (behind the rail) | 2.17 m / 29 % / 0.51 |
| V1 batch 4: no rail | reached; **0.78 m / 0.14**, 18 % under 3 m | **0.77 m / 100 % / 0.14** | 2.17 m / 29 % / 0.51 |
| V2 rail with a 2 m gate | reached; 0.78 m / 0.14 | not run | not run |
| V5 chain across the porch mouth | 0.78 m / 0.14 | not run | not run |
| **V7 rail with the three centre bays open (6 m) + porch roof camera-transparent** | **reached**; 1.74 m / 0.42 for 2.7 % of frames while turning round at the wall | **2.87 m / 13 % / 0.78** | **4.55 m / 0 % / 1.00** |

V7 is better than the closed rail **even on the forecourt**, and the doors become a clear future entrance. The 1.74 m moment is the camera with its back to the hall wall, the same as at every other door of the town (2.8 m class). What the camera then shows under the porch (`evidence/p3a-rail-v4-door-north.jpg` approaching: the character is visible through the open gable front; `…-door-south.jpg` turned round: a steep view down inside the porch at 4 m) is acceptable to me but is a `PREFERENCE` call for a human.

**Recommended (smallest effective change):** remove the three centre rail bays (dressing rows at x −2, 0, 2 and their three proxies), keep the two end bays and the side returns as balustrade wings, and mark the six porch-roof bands of B01 camera-transparent. No geometry is rebuilt. If an interior is added later, the door trigger sits at the porch mouth (n 77.4: 2.79 m / 0.75).

## 2. Terrace and podium edges

Walked with the real body:

| Edge | Result | Judgement |
|---|---|---|
| Terrace sides (x ±14, n 62–74) | the body stops at x ±12.0 (n 73) | closed; fine |
| Terrace south edge beside the stairs | balustrade wings stop the body at n 64; a short open strip remains by the stair cheeks (1 m drop, batch 5 test) | fine |
| Podium front edge (n 74, beside the hall steps) | open: the body steps down 1 m onto the terrace | acceptable; balustrade wings would be more formal (optional) |
| **Podium east and west edges (x ±14, n 74–90)** | **open: the body walks off a 2.0 m drop** (ends at x ±16.6, y 0) | `CONFIRMED-TECH`, unguarded |
| **Podium north edge (n 90, behind the hall)** | **open: 2.0 m drop** | `CONFIRMED-TECH` |

**Recommended:** do not add 40 m of balustrade to a slab that should not be a slab. In the selected island the ground is raised to +2.0 m beside and behind the hall (the "hall shelf", doc 04), so the three 2 m drops become level ground and the podium reads as cut into a hillside. Until the terrain exists the drops remain; if the owner wants the preview safe now, three invisible wall proxies (x ±14.05 and n 90.05, top 3.0) are the interim fix. Optional: four balustrade bays each side of the hall steps on the podium front.

## 3. The 0.75 m gap between B10 and B11

Batch 5 could not say whether it was enterable. **It is: the real body walks straight through** from the lane (−16, 15.8) to the open ground behind the row (ends at x −27.6), camera 2.8 m along the gap; a spin inside the gap gives 0.81 m / 83 % / 0.14. The B11–B12 gap is **not** enterable (the body stops at x −17.1). Batch 5's 0.84 m "B12 south" value was a probe point no body can reach.

**Recommended:** close the B10–B11 gap at both mouths with one fence or stacked-goods prop each (tested: two 0.2 × 1.6 m proxies; gap unreachable, lane route unchanged at 12.9 m). It is narrower than the 1.5 m minimum for a trail, leads nowhere, and is the precedent already used for the slot behind the east shops. If a secret passage is wanted instead, it needs 1.5 m and a destination, which is a layout change I do not recommend.

## 4. Camera compression round the Artisan Lane roofs (and seven other places)

**Finding: one cause explains nine of the worst spots in the town.** Low eave bands: the smithy/joiner roofs (A06), the single-storey shops (A04/A04b) and E04's wing have camera proxies that start 2.2–3.2 m above the ground and overhang the walls by about 1.2 m. A player standing under an eave has the camera pulled onto their head (`evidence/p3a-eave-current-B10S.jpg`: 0.84 m, the faded character fills the frame).

| Spot | now | rule A: roof bands that start below 3.2 m are camera-transparent |
|---|---|---|
| B10 south eave | 0.84 / 46 % / 0.14 | 2.93 / 8 % / 0.80 |
| B10 lane corner (NE) | 1.62 / 29 % / 0.25 | 2.79 / 17 % / 0.75 |
| B12 lane corner (SE) | 1.77 / 29 % / 0.30 | 2.80 / 17 % / 0.75 |
| E01 west and east sides | 1.39, 1.38 / 46 % / 0.17 | 2.93 / 8 % / 0.80 |
| B15 south-west (roof of E07) | 1.42 / 46 % / 0.19 | 2.72 / 25 % / 0.69 |
| E04 east, porters' path | 1.47 / 42 % / 0.21 | 2.93 / 8 % / 0.80 |
| Porters' path gate | 1.95 / 29 % / 0.35 | 2.83 / 13 % / 0.77 |
| Tea-house veranda | 1.49 / 38 % / 0.22 | **1.49 (unchanged: posts and balcony, not a roof)** |

Rule A removes 20 of 200 roof bands from the camera list (10 buildings); walls, upper roofs and every body proxy stay. With the rule the camera sits about 2.9 m behind the character with the eave's underside in the lower frame (`evidence/p3a-eave-ruleC-B10S.jpg`): the character is visible and not faded. A wider rule (below 4.3 m) gave no extra benefit except at the porch, where the whole porch roof must be transparent anyway (section 1). Lane walk 12.9 m and porters' path 2.94 m are unchanged.

**Recommended:** adopt rule A as a camera-proxy rule (data only). It is preview-side proxy data today and will be needed in the game's proxy data for this island; it does not touch the camera code.

## 5. Shortlist of essential corrections (all small, none rebuilds a building)

| # | Correction | Type | Status |
|---|---|---|---|
| C1 | Open the three centre rail bays; porch-roof bands camera-transparent | dressing + proxy data | recommended, **not applied** |
| C2 | Camera rule A: roof bands starting below 3.2 m are camera-transparent | proxy data | recommended, not applied |
| C3 | Close the B10–B11 gap at both mouths | 2 props + 2 proxies | recommended, not applied |
| C4 | Podium side and back drops: solved by the hall shelf in the terrain (interim: three wall proxies) | terrain (P3-B) | part of the island design |
| C5 | B15/B16 trade identity: larger signs, banner colour per house | dressing | recommended, not applied |
| — | Tea-house veranda (1.49 m / 0.22) | open | not solved by any rule tested; needs its own look (posts spacing or a veranda-specific camera volume) |

Applying C1–C3 and C5 is about one short batch (data and dressing, one kit re-export for C1/C3/C5 dressing) and can ride with the first P3-B step. I did not apply them because the brief asks for recommendations and the town is to be preserved pending your decision.
