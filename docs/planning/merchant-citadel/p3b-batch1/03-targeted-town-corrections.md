# 03 — Targeted town corrections (preview-side, behind flags)

The kit GLB and `scene.json` are **unchanged** (hashes verified). Each correction is a load-time edit in `merchant-citadel-p2a/p3b-fixes.js`; `?fixes=0` restores batch 5 behaviour, individual flags `rail gates porch eaves gap signs` (`=0`). Before/after: `evidence/p3b-corrections-before-after.json` (same spots, 24-yaw sweeps, real controller and camera).

| # | Correction | Before (fixes=0) | After |
|---|---|---|---|
| C1 | **Forecourt rail**: three centre bays cut from the dressing geometry (398 triangles), their proxies removed; end bays and returns stay | doors unreachable: body stops at n 75.7 | doors reached (0, 79.3); forecourt camera 2.17 m / 29 % under 3 m / opacity 0.51 → **4.55 m / 0 % / 1.00** |
| C1b | **Porch roof camera-transparent** (six camera-only bands of B01) | at the doors 0.77 m, 100 % of yaws under 3 m, opacity 0.14 | **2.28 m, 21 %, 0.54**; porch mouth 0.94 → 2.79 m |
| C2 | **Low-eave rule**: camera-only roof bands starting below 3.2 m are camera-transparent (22 of 200 bands, 12 buildings); walls, upper bands and all body proxies intact | B10 south eave 0.80 m / 54 % / 0.14; B12 corner 0.77 / 50 % / 0.14; B10 corner 1.45 / 38 % / 0.20 | **2.94 / 4 % / 0.77; 2.93 / 4 % / 0.78; 2.99 / 4 % / 0.80** |
| C3 | **B10–B11 gap closed** at both mouths with stacked crates and barrels (custom props) and two solid proxies | the body walks through to x −27.5 | closed: stops at x −17.05 |
| C4 | **Podium side/rear drops**: the hall shelf (+2.0 m) makes the east, west and north edges flush | three unguarded 2 m drops | walk test (west of the terrace): up the bank to the shelf, y 2.0, no fall |
| C5 | **B15/B16 identity**: a second, projecting sign on each tower (scale 1.5) and three banners each (burgundy assay office, blue cartographer) | one 1.4× sign each | 8 additions, visible in `compare-v4-exchange-hall.jpg` and `compare-v4b-hall-from-street.jpg`. `PREFERENCE`: a human should judge whether it is enough |
| C6 | **Tea Lookout gate** (new, required by the route "tea house → promenade"): one 2 m bay of the terrace fence cut, proxy removed | promenade unreachable from the terrace | passes |

## Findings made while testing (not in the brief)

* **CONFIRMED-TECH, pre-existing (batch 5): the forecourt balustrade mesh stood 1.0 m away from its collision proxies** — front rail mesh at n 75.1–75.3, proxies at n 76.2; side returns at x ±6.0 vs proxies at ±5.0. The player walked 0.7 m through the visible rail before being stopped. The four remaining proxies are moved onto the mesh (`removeRailProxies`). Whether the same offset exists for other dressing rows is **not checked** (backlog).
* The eave rule keeps looking through eaves acceptable in the tested spots (character visible, not faded; camera 2.9 m behind); it does not help the **tea-house veranda** (min camera 1.49 m on `tea_house_to_overlook`): posts and balcony, not a roof band. **Unsolved; investigated, not fixed.**
* Camera-transparent bands are a data rule; the game's proxy data would need the same flag if the rule is adopted outside the preview.
