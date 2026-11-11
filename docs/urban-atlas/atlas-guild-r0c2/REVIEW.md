# Atlas Guild R0-C2

**Complete local integration; owner visual approval pending. No deployment.** [Play the Guild](../../../index.html?experience=adventure&dev-town=s2f&town-layout=reset-final&town-props=cc0&town-guild=r0c2&build=guild-c2-final) · [Matched gallery](index.html) · [Editable master](../../../validation/atlas-guild-r0c2/atlas-guild.blend) · [Optimized GLB](../../../assets/game/atlas-guild/atlas-guild.glb).

The C2A-derived research hall now terminates the accepted civic route. A broad, compact observation lantern sits in the roof mass rather than on a tall pole. The timber portal, sun screens, blue-green glazing, complete limasan roof, survey-compass fanlight and actual entrance lettering distinguish it from the four shops. No detailed interior is implied.

## Site and gameplay

The **9.525 × 7.337 m** roof/entrance envelope fits the existing **10 × 8 m** reservation, centred at world **(-9.03007, 35.53187)**, with a **35° Y rotation**. Floor **16.05 m**; existing ground beneath it **15.480–15.971 m**. The shallow stone support is **0.079–0.570 m** above the ground and embeds below it; no empty air gap beneath the foundation. Three **178.3 mm** risers, **0.90 m** total run and **1.111 m** landing serve the **2.392 × 2.70 m** doorway. No terrain sculpting, extra bridge, route detour or tree move.

Original-controller CPU checks pass at **20/60 Hz**, including both directions, jump/landing, closed building approach and portal pier. Five live animated-explorer checks and the real E interaction are recorded in the linked evidence; holding W against the closed door stops after approximately 0.062 m. The forward route is **42.22 m**, reverse **42.18 m**. The promenade and highland branch remain in their accepted positions.

At the door, **Explore Transit Research** / **E** opens the existing `transit` project panel and authentic case study. Closing it retains adventure mode, player position and scene. Research content, findings, registry and external editorial access are reused unchanged.

The first entrance check exposed camera penetration into the avatar. The Guild's oriented movement proxies are now excluded from the legacy axis-aligned camera sweep; the existing camera uses actual Guild mesh rays instead. Movement physics and the shared camera implementation are unchanged. The entrance location label is handled locally in the Guild integration; the shared portfolio controller remains byte-identical. Seven movement proxies correspond to the visible hall and six measured timber piers. Native and game visuals were inspected separately; no artistic approval is inferred from traversal.

## Measured delivery and performance

**1,527,656 bytes**, **14,697 triangles**, **16 static batches/materials**, **zero textures/transmission**. Existing glTF tools index shared vertices and prune/deduplicate resources; no silhouette decimation. Cold GLB request **1,527,956 transfer bytes**, **10.3 ms** on the available local server. One additional shared-loader GLB, nine cached model files versus eight without the Guild; no extra texture requests.

| Matched 12-second camera rail | Guild OFF | Guild ON |
|---|---:|---:|
| rAF median / p95 | 5.60 / 11.20 ms | 5.60 / 11.20 ms |
| CPU submission median / p95 | 1.00 / 1.30 ms | 1.10 / 1.50 ms |
| All-pass draw calls | 296–365 | 327–396 |
| Submitted triangles | 2,501,014–2,564,356 | 2,530,358–2,593,700 |

Net **+31 calls / +29,344 submitted triangles**, including shadows and removal of the old noticeboard/posts. Apple M4 Pro / ANGLE Metal, standard shadows, exposure **0.96**, original lighting, Glass **B**, DPR **1**, game buffer **1280×656** below the site header. Same cameras and settings, 2-second warmup, no concurrent native render. rAF and CPU submission are not GPU timings. No measurable rAF regression in this short desktop comparison; mobile hardware is untested. [Raw timing](../../../validation/atlas-guild-r0c2/performance.json).

## Evidence and preservation

Five clean actual-game before/after pairs: [Market Street](../../../validation/atlas-guild-r0c2/04-game-market-after.png), [Telaga Awan](../../../validation/atlas-guild-r0c2/05-game-square-after.png), [entrance](../../../validation/atlas-guild-r0c2/06-game-entrance-after.png), [town](../../../validation/atlas-guild-r0c2/07-game-town-after.png), [whole island](../../../validation/atlas-guild-r0c2/08-game-island-after.png). Pedestrian cameras are **1.65 m above support**. Camera tuples/settings accompany every PNG. The original explorer and real panel have separate captures. Cycles renders are supplemental reference only.

**22 scoped regression tests pass** (15 integration/character/population plus 7 portfolio). [Controller/support/fit](../../../validation/atlas-guild-r0c2/controller.json), [integration tests](../../../validation/atlas-guild-r0c2/regression.log), [portfolio tests](../../../validation/atlas-guild-r0c2/portfolio-regression.log), [E interaction](../../../validation/atlas-guild-r0c2/interaction.json), [preservation](../../../validation/atlas-guild-r0c2/preservation.json).

Four buildings/transforms, the 6 m street, 210 m² square, fountain/pavilion, 17 CC0 prop types / 42 placements, terrain and all existing instanced matrices are preserved. Original masters, GLBs, character/camera code and research registry match the verified checkpoint. No new critical rendering error or missing texture was observed. Human visual approval remains pending.

## Rollback

Remove **`town-guild=r0c2`** and reload to restore the accepted populated town with **no Guild asset request**. Other town/prop flags remain. Local “Guild off” restores the noticeboard, its exact geometry and collision order while retaining the cached Guild for comparison. “Town off” still restores the original landscape; on restores the requested development layers in the same scene/renderer.

Verified checkpoint: **`codex/populated-town-baseline`**, **`a2871dbeeb86435144f46ac4336b22c8f3e02801`**. Exact integration backups are in `validation/atlas-guild-r0c2/baseline/`; restore only this phase's files, preserving unrelated working-tree changes. [Source/license record](ASSET-RECORD.md).
