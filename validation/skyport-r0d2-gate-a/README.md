# R0-D2 Gate A · creature direction

**Decision requested:** approve or revise the illustrated original tropical dragon and the proposed custom Blender direction. This sheet is AI-generated concept art, not modeled geometry, an animation, or evidence of game integration. The illustration is an intent reference; its rider, saddle/wing clearance and proportions are not mechanically verified. Gate B and C remain unauthorized until their respective approvals.

## R0-D1 diagnosis

The existing `Dragon.gltf` is a real skinned CC0 Quaternius asset with 13 joints, 4,562 triangles and authored `Flying_Idle` / `Fast_Flying` clips. It looks like a head with wings: the body, limbs, passenger area and tail are visually insufficient for a believable mount. The player remains on the deck. The cinematic follows a departing asset rather than boarding, flight with a rider, landing and dismount.

Actual D1 code uses local positions `(u=4, v=-19)` to `(u=4, v=-37)` and world heights 19 to 29 m, a roughly 18 m horizontal / 10 m vertical flight. The idle model origin is 3.905 m above the platform datum of 15.095 m; its center is approximately 12.65 m from the platform center, whose radius is 6.5 m. These are root positions, not measured physical skin clearance. They demonstrate why the existing preview cannot be treated as a safe boarding arrangement. The existing circular guard is continuous; do not assume it may be opened or walked through.

See historical actual game captures in `../skyport-r0d1/`, especially `08-boarding-edge.png`, `02-cinematic-near.png`, `03-departure.png`, `01-arrival.png`, `07-island.png`.

## Asset comparison

| Candidate | Evidence and licensing | Assessment |
|---|---|---|
| Existing Quaternius Ultimate Monsters Dragon | [Creator page](https://quaternius.com/packs/ultimatemonsters.html), CC0. Actual file and two flight clips already in D1; 4,562 triangles. | Cheapest to reuse, but its anatomy is unsuitable for the requested rider scale. Reject as the final mount. |
| Regina Cachoa [European Dragon](https://sketchfab.com/3d-models/european-dragon-82f393a2e6c048ad80c171ce3b3a7b87) | Listing says CC BY 4.0, FBX, 42.3k triangles, hand-painted 2K/4K textures and idle/walk/run/fly. Page and viewer inspected; download requires Sketchfab sign-in. File, rig and rights chain not independently inspected. [CC BY 4.0 terms](https://creativecommons.org/licenses/by/4.0/) permit sharing/adaptation with attribution, license link and change notice. | More complete flight-ready starting point in principle; visual preview is dark, fierce and heavily detailed, so substantial silhouette/material/rider work is needed. Clip quality, conversion and rider compatibility unverified. Candidate only, no download or integration selected. |
| Drummyfish / Cethiel [Cethiel's Dragon 3D](https://opengameart.org/content/cethiels-dragon-3d) | Page identifies CC0; downloaded 1.4 MB ZIP was inspected without importing. Contains Blender 2.79/2.80 files, OBJ, DAE and two textures. Files named idle, walk, attack and die; no flight-named clip. Rig and actual compatibility remain unverified. | Editable legal candidate, but the preview is spiky and ground-oriented and the archive does not establish a flight cycle. Substantial new creature/wing/animation work would still be needed. |
| Custom Blender model | Original project-authored model and textures, with source provenance for any reused rig parts. | Best control over calm silhouette, saddle, tropical palette and six-appendage anatomy. Highest modeling, rigging and animation risk; no asset or animation exists yet. |

A model advertised as CC BY but explicitly described by its uploader as a proprietary game extraction was rejected; a listing license alone cannot grant rights the uploader lacks. No candidate other than the existing D1 dragon has been loaded into the game.

## Recommended concept

An original calm quadrupedal sky dragon with two additional wings, a long counterbalancing tail and a close-fitting woven timber/leather saddle. Muted celadon and teal with warm-stone underside and restrained terracotta accents connect it to the town. The target is a readable, painterly animal, not a Nintendo design or a literal copy of any named character.

Initial design envelope (not a measurement of an existing model): approximately 7.5 m nose-to-tail, approximately 10 m unfolded wingspan, and a 1.65 m scale reference. A 10 m span leaves only 1.5 m per side within a nominal 13 m diameter before accounting for railings, wing motion, player and camera; **this is not evidence of fit**. Gate B must test the folded, takeoff and landing swept volumes against the actual canopy, pylons, guard, ground and camera. A physically supported and guarded mounting position is not yet identified. If none fits without changing protected C3.1 geometry, report the conflict instead of hiding it or inventing an unsupported boarding point.

## Proposed technical plan after approval

Prefer a custom Blender creature, with optional reuse of legally verified components only if they materially reduce rigging work without retaining incompatible visual identity. Preserve an editable master. Initial performance target **20–40k triangles**, one creature, approximately 2–5 draw calls/materials excluding shadow passes, and one suitably sized texture atlas; these are authoring targets, not measurements or promises. Validate real browser rendering at the same quality, camera and resolution as D1 before choosing final budgets.

Gate B should prove four-legged anatomy, independent deforming wings, saddle-to-rider fit and repeatable idle / takeoff / flight / bank / landing clips with a meaningful weighted rig. Boarding and dismount animations and an actual safe ground-to-saddle transition remain separate tasks; custom animations, collision and camera fitting have not yet been built or tested. Use the existing model cache, renderer, controller and separate local flag only after Gate C approval.

Blender MCP was checked read-only: connected to Blender 5.2.3, currently displaying the existing C3.1 independent derivative. No scene was modified. No performance benchmark, automated test, game change or production deployment was performed in Gate A. Prior D1 performance and regression numbers remain historical evidence only.
