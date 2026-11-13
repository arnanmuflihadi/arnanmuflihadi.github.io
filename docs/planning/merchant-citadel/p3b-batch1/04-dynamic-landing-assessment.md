# 04 — Dynamic landing compatibility (terrain side only)

**Not available in this branch:** the dragon free-flight controller (`travelConfig.implemented = false`; `skyport-boarding.js` only loads `assets/game/skyport/boarding/dragon.glb`). Nothing here claims compatibility with a controller that does not exist. What was measured is whether the loaded terrain offers surfaces for **the actual dragon model**, using this phase's proposed criteria. The game's own landing rules, when they exist, replace them.

## The dragon, measured (`dragon.glb`, CC0 Quaternius Ultimate Monsters)

Bind-pose bounds 4.38 × 1.51 × 2.45 m; maximum horizontal extent over the 12 phases of `Flying_Idle` 4.88 m → **footprint radius used 2.44 m**. (Landing/dismount poses were not animated or measured; clips present: Flying_Idle, Fast_Flying, Death, Headbutt, HitReact, No, Punch, Yes.)

## Criteria (no whitelist; evaluated on every node of the loaded terrain)

Disc of the dragon radius fully supported; height range ≤ 0.5 m and slope ≤ 0.18 inside it; ≥ 4 m of support beyond the disc in every direction; ≥ 1 m from the nearest solid (town proxies, trunks, props); at least one 15° approach bearing with a clear glide path (3 m over the disc rising 0.10 per m to 40 m, no terrain or solid above it); a comfortable ground cell 2–6 m outside the disc for dismount.

## Result (`evidence/p3b-landing.json`)

* 2 m grid scan: **1,342 eligible nodes**, forming 143 separate patches (7 m apart). They are open, flat surfaces **including some town squares and streets** (arrival court, bazaar edges): whether the game may land there is a design decision, the terrain does not forbid it. The largest patches are on the Sky Quay, the lawns west of the artisan block and the court.
* The four P3-A example areas, tested for this dragon (not as the only places):

| Area | Eligible for r 2.44 m | Largest eligible radius at its centre | Nearest solid | Approach bearings open |
|---|---|---|---|---|
| Caravan Green (−50, 18) | yes | 6 m (trees and wagons at the edges limit it; P3-A claimed 14 m for the bare lawn) | 4.2 m | 24 / 24 |
| Sky Quay (5, −52) | yes | 4.5 m (lamps and crane at the edges) | 2.6 m | 16 / 24 |
| Shoulder Table (−36, 112) | yes | 3 m (a 6 m clearing, slope-limited) | 6.3 m | 24 / 24 |
| Hall lawn west (−32.5, 85) | yes | 8 m | 11 m | 13 / 24 |

* Dressing was deliberately kept off the Caravan Green centre (wagons, campfire at 8–11 m) after the first placement made it ineligible (largest radius 1.5 m) — the scan caught it.

## Interface requirements for the future free-flight / landing code

1. Use `isl.terrainAt(x, n)` (support) and `isl.maskAt` (walkable/comfortable); the no-support value is −80 m, so "landing on the void" is detectable.
2. Landing must test the dragon's real footprint against terrain *and* the obstacle list; the preview's `isl.landing.evaluate` is a reference implementation.
3. Fall/dismount recovery is the controller's `recoveryPoint` / `isSafe`; `isSafe` is `comfortable` here.
4. Flight bounds: the island needs `airspace` beyond the 204 m × 217 m envelope; `travelConfig.airspace.radius` is 800 m.
5. **Untested:** approach from the dragon's actual flight path, wing collision with the crag or cliff, landing animation clearance, takeoff run, dismount onto slopes.
