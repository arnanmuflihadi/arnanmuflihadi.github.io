# R0-C1A — Telaga Awan Town Square

**Isolated design proposal. Human visual approval pending before R0-C1B. No production integration or public deployment.**

[Native Blender scene](../../../validation/town-square-r0c1a/town-square-design.blend) · [Measured site/route plan](../../../validation/town-square-r0c1a/site-plan.json) · [Checks](../../../validation/town-square-r0c1a/validation.json) · [Sources](ASSET-RECORD.md)

## Preferred concept

A small stepped civic court west of the protected market forecourt: two swept bronze rain leaves in a quiet jade basin, warm stone paving with terracotta borders, an open timber/limasan shade bay, timber seating against the higher apron, planted edges and one two-person café table. The fountain is a static design object; animated water is not implemented.

The approved four buildings, forecourt, tree, bench, existing stair and garden ramp stay in place. A direct west-edge shortcut was rejected after mesh inspection found the existing bench blocking it. The proposal instead reaches the court from the established north landing through a shallow supported walk. This preserves the market, at the cost of a longer approach.

The original concept boards remain available in `validation/asset-selection-s1/references/`. Their broad single-level ceremonial plaza and completed Guild exceed this protected reservation. This proposal uses two smaller linked gathering floors; it does not reproduce or imply a finished Guild.

## Measured site and interfaces

All elevations below use **game Y**. Survey point arrays are **[game X, game Z, elevation Y]**, explicitly marked in JSON. Camera records also provide conventional Three.js **[X,Y,Z]** positions. Blender mapping: `(u,v,h)=(X−36,44−Z,Y−18.6)`, one unit = one metre.

| Element | Measured design |
|---|---|
| New court | X20.5–28.0, Z4.0–14.4; **7.5×10.4 m / 78 m²**, finished Y21.800 |
| Protected forecourt | X28–44, Z8–14.2; **16×6.2 m / 99.2 m²**, Y22.614; unchanged |
| Linked gathering floors | 177.2 m²; approach walks are additional circulation |
| Terrain under new court | Y18.811–21.620, from 1,271 exact-mesh samples |
| Local retaining exposure | Floor-to-ground **0.180–2.989 m**; walls scribed to the terrain, with embedded toes |
| Civic walk | 10.65 m horizontal length, 2.6 m nominal width; **10.2%** maximum designed centreline grade |
| Walk support | Floor-to-ground 0.196–1.479 m over all 44 edge vertices; visible stone shoes, timber posts and bearers |
| Walk clear width | **2.41 m minimum** over 20 actual guard-face ray samples at 0.70 m above the deck; geometry check only |
| North landing flight | Existing Y20.754735 → new walk Y22.530; **10 risers, 0.134–0.188 m**, 0.260 m treads; 2.6 m nominal width |
| Tread/terrain check | All 40 corners above the terrain; minimum clearance 0.026 m after correction |
| Fountain / seating | Basin diameter 2.84 m; eastern passing gap 1.68 m; seat height 0.45 m |
| Shade | 4.5×4.1 m roof; **2.56 m** lowest header clearance |
| Highland interface | Nine 0.132 m steps to a 2.1 m-wide earth trail; trail length 24.05 m horizontally, joining the existing ridge at X−5,Z5,Y21.046 |
| Guild reservation | Via the existing X36,Z0 landing toward X44,Z−8; surveyed ground Y23.535 at the far endpoint. No Guild geometry |

No terrain is flattened or sculpted. The isolated proposal replants **three small groundcover clumps** outside the court at their original scale; original trees remain. Foundations are game/environment design geometry, not certified engineering.

The existing controller reference is 0.68 m wide / 1.9 m high with a 0.42 m snap limit. These dimensions informed the design; **no new route has been playtested**. The stair/ramp tests from S2-E/F/G are historical evidence for the unchanged existing approach, not approval of these additions.

A geometry ray from the square to a hypothetical Guild target 5 m above its surveyed ground is clear. This reserves an upper-level sightline; it does not establish a complete Guild vista or future building approval.

## Actual visual evidence

Four real Blender MCP/Cycles renders, **1800×1200**, 64 samples, AgX, shared daylight. The two pedestrian cameras are 1.65 m above their supports. Camera position, rotation, lens/FOV and lighting are recorded in the site JSON. The aerial shows the market as context; the plan shows the actual terrain, proposed paths and dimensions. Labels appear only in the plan.

1. [Market/garden-ramp arrival](../../../validation/town-square-r0c1a/01-market-arrival.png) — original tree, fern and guard retained; the bronze focal feature is visible beyond them.
2. [Square interior](../../../validation/town-square-r0c1a/02-square-interior.png) — basin, shade, planting and human-scale paving.
3. [Elevated composition](../../../validation/town-square-r0c1a/03-elevated.png) — both floors, new walk, existing market and grounded supports.
4. [Measured top-down plan](../../../validation/town-square-r0c1a/04-measured-plan.png) — solid route to the court; dashed Guild reservation; natural highland link.

The correction passes addressed three groups: obstructed/steep proposed access, incorrect imported context foliage and overlarge replanted clumps, and weak focal/paving presentation including coincident basin faces and an unnecessary new rail against the higher apron. Internal inspection is not human artistic approval; no review score is awarded.

## Cost and preservation

**46,534 evaluated triangles / 12 new design materials**, measured in Blender. This is the editable inventory, including hidden authoring lettering; plan labels and the scale reference are excluded. Paving accounts for 32,508 triangles, the main future simplification target. Existing reference context adds 555,368 triangles and is not a new game export. The nine source images are packed; new design materials use lightweight PBR inputs without new texture downloads.

No square GLB, browser draw calls, transfer size or frame timings were measured: export/integration is outside this phase. The context-only GLB contains existing island vegetation for Blender reference, not deployable square geometry. Browser material matching and batching remain future work.

Preservation checks compare **3,255 pre-existing files** and **1,828 copied market/interface object transforms**. No approved source file or transform is changed. No whole-game regression suite was run during isolated authoring. See the saved validation record for fresh artifact, preservation and geometric checks.

## Remaining issues — maximum three

1. New stairs, seams, guard collisions, camera clearance and the route must be tested with the real controller in an approved later phase. No new traversal success is claimed.
2. The preserved market tree/fern/guards partly screen the first arrival view. The highland link has local grades up to 39.1%; the unbuilt Guild corridor needs its own detailed slope/vegetation study. The short planning ray does not approve the whole view corridor.
3. The roughly 3 m north-west retaining face and simple foliage need owner visual review; game export/material matching, batching and water motion are unverified.

**Stop here for owner design approval before R0-C1B.**

Reopen with Blender: `open -a Blender "/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/town-square-r0c1a/town-square-design.blend"`. Select the four `C1` camera presets; enable `C1 / Plan annotations` only for the plan render.
