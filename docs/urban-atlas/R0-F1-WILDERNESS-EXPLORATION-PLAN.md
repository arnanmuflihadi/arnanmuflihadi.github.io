# R0-F1 — Wilderness & Exploration Master Plan

Planning only · 10 November 2026 · implementation and visual approval pending.

## 1. Recommendation

Develop **two optional discoveries: Cloudbreak Overlook and Crown Ridge**. Reuse the existing western trail circuit and the RESET-FINAL forest connection. Cloudbreak is the shorter out-and-back; Crown Ridge is the more strenuous extension that completes a loop. No new waterfall access, terrain work, buildings or asset search is justified.

The wilderness already has continuous support, a connected trail graph, distinct elevation zones and existing rock/plant accents. Its missing layer is destination recognition and a reason to stop. Add modest route cues, two contextual observations and independent discovery acknowledgement—not another research quest.

**Conditional implementation recommendation:** proceed to F1A only after owner authorization. Measurements and local browser movement support these choices, but do not establish a complete current-town-to-wilderness browser traversal. F1A must close that gap before advertising the circuit as safe. Do not reopen E1C.1; it remains deferred, neither fixed nor passed.

## 2. Evidence and measurement limits

Inspected current `assets/js/floating-atlas/plan.js`, `terrain.js`, `support.js`, `collision.js`, `nature.js`, `reconstruction-plan.js`, `reconstruction-terrain.js`, `town-reconstruction.js`, `scene.js`, `entry.js`, `presentation.js`, `transit-quest.js`; current player controller, native adventure UI and session persistence. Read the scenery/population source records and relevant landscape/E1C evidence. Historical settlement coordinates in skill reference documents are obsolete; the running RESET-FINAL transform below controls this plan.

Local browser baseline:

`http://127.0.0.1:4188/index.html?experience=adventure&project=transit&dev-town=s2f&town-layout=reset-final&town-props=cc0&town-guild=r0c2&town-skyport=r0c3&town-skyport-polish=r0c3-1&town-story=r0e1`

Fresh browser inspection used the existing `island-review` presets, then ordinary explorer movement to return to the **actual follow camera**. Review positioning is not evidence of walking there from town. At Crown Ridge the explorer walked from approximately `(-38.21,46.17,-41.31)` to `(-43.04,48.44,-48.20)`, remained grounded and rotated toward the town without a reproduced navigation-blocking occlusion. Cloudbreak and the ridge switchback received short local movement checks. These were third-person views, not calibrated 1.65 m eye cameras; no full loop, fall recovery or all-angle camera approval is claimed.

Reproduction records, positions in metres, quaternion `[x,y,z,w]`, FOV 60°, browser viewport 1280×720:

| View | Player XYZ | Follow-camera XYZ; quaternion | Observation |
| --- | --- | --- | --- |
| Crown looking back toward town | −43.04,48.44,−48.20 | −44.75,51.76,−51.17; `[.04376,.95214,.16381,−.25434]` | Town roofs visible beyond forest; existing rocks frame the stopping pocket. |
| Cloudbreak | −80.22,32.00,5.13 | −84.94,38.82,−2.84; `[.06163,.93787,.22516,−.25672]` | Broad cloud/cliff vista; player visible. Trees and terrain interrupt the water/town view. |
| Ridge switchback | −29.42,27.18,−.85 | −24.08,33.93,6.77; `[−.22037,.29257,.06948,.92791]` | Dirt tread remains recognizable, but repeated pale bands and broad grass slopes offer little destination identity. |

These fresh observations were viewed during planning, not saved as a new gallery. Existing [landscape comparisons](../landscape-detail-review/index.html), especially [forest](../landscape-detail-review/after-05-forest.jpg) and [overlook](../landscape-detail-review/after-06-overlook.jpg), are **historical** camera evidence, not proof of the current town or a player-height waterfall view. The current [E1C whole-island capture](../../validation/transit-e1c/evidence/island.jpg) supplies settlement context.

Read-only measurements used the current triangle height sampler with the RESET shelf enabled in memory. Profiles subdivide each route segment into intervals no longer than 0.5 m; maximum grade is the largest absolute sampled rise/run, not an accessibility standard or an exhaustive maximum. Point slopes use 1 m central differences. Heights are ground/support metres, not sea-level survey elevations.

The existing real-mesh fixture imports geometry and generates nature colliders, omitting textures. Both directions of all six natural routes and the 24.20 m forest connector reached their endpoints with the unchanged controller, grounded and without jumps. This simulation includes the adjusted shelf but **not every active town/Guild/prop collider**. Runtime shelf sampling uses the rendered triangles; `support.js` alone describes the original natural terrain and must not replace `town.heightAt` at town interfaces.

Fresh focused command: `node --test --test-name-pattern='rendered terrain support|every ridge and valley route' tests/landscape-r0a.test.mjs` — **2 passed, 0 failed**. These tests cover exact natural-terrain support/watertightness and authored routes with nature collisions, not final wilderness gameplay acceptance. No full-game suite or new benchmark was run.

## 3. Current spatial inventory

World axes are Three.js X/Z horizontal, Y up. Town local coordinates use `reconstruction-plan.js`: origin `[-1,47]`, heading 235°; `toWorld(u,v)` offsets v by 18. Do not reinterpret old arrival `[27,57]` as the accepted skyport. Wilderness locations below are world coordinates; UV values only aid overlay alignment.

| Candidate/interface | XYZ; current town UV | Approach and distance from forest-branch head | Ground and constraints | Nearby assets / opportunity / uncertainty |
| --- | --- | --- | --- | --- |
| Town forest-branch head | −.59,15.48,34.51; 7.5,28 | Existing square-side branch, no new town exit | 24.20 m to `[11,22]`; median 16.1%, sampled max 33.1% | Existing pavilion-side public realm and ferns. Full populated-town entry/return still needs browser validation. |
| Valley junction | −5,21.01,5; 20.81,54.70 | Branch → `[11,22]` → `[6,15]` → junction: **47.67 m** | Point slope 11.8%; routes diverge here | Open clearing between groves. Use as orientation only, not a third discovery or new square. |
| **Cloudbreak Overlook** | **−80,32.01,5; −40.62,97.72** | Valley → reverse of `return`, 84.81 m; **132.48 m total** | Point slope 6.3%; 7.18 m horizontal to top-mesh rim; nearest nature AABB 7.0 m | Existing rocks, broadleaf/fern accents, western cloud vista. Waterfall body not established as visible from player view. |
| **Crown Ridge stopping pocket** | **−43.04,48.45,−48.20; 20.17,120.10** | Valley → `ridge`; authored summit at `[-45,-49]` is **138.21 m total**, pocket ≈2.12 m from it | Point slope 27.6%; rim 10.41 m away. A 1.2 m-radius perimeter has 0/32 blocked nature samples; 1.8 m has 5/32 | Existing summit boulders and low trail plants; broad town/forest view. No flat gathering platform; constrain interaction to the small pocket. |
| Stream source — **not selected** | −22,22.75,25; −4.58,48.07 | Trial spur `[-31,19]→[-26,21]→[-22,25]`, 11.04 m | Sampled max 157.8%; 2.54 m ascent plus 3.79 m descent | Existing spring pool, channel and bank stones. Simulation reaches it, but that does not make this steep bank a good designed route. Reject this spur. |
| Waterfall lip — **not selected** | −72,10.28,38 | No approved walking approach | Low cliff-edge stream termination; substantial vertical separation from overlook | Existing animated water/mist. The cinematic `waterfall` camera is outside the playable surface; never use it to imply safe discovery access. |
| Eastern clearing/meadow — reserve | 32,21.98,12 | Existing `clearing` then `meadow` routes | Authored widths 3.0/2.6 m; sampled max grades 20.4/19.6% | Existing palms/trees; lower technical risk, but weaker distinct discovery payoff. Preserve; not a third stop by quota. |

Rim distance means shortest XZ distance to the existing upper-surface boundary, **not** a guarded setback or proof of every surrounding slope. The collider checks include the controller's 0.34 m radius. Perimeter samples are not continuous clearance guarantees. Crown's small pocket and Cloudbreak's 1.8 m perimeter need final browser checks before marker placement.

### Route hierarchy and accessibility

| Existing route | Authored width | Plan / sampled surface length | Median / maximum sampled absolute grade | Use |
| --- | --- | --- | --- | --- |
| Town connector | Approx. 2.7 m visual branch corridor | 24.20 / 24.54 m | 16.1 / 33.1% | Single wilderness exit; do not claim an accessible ramp. |
| Arrival trail, full original route | 3.1 m | 63.21 / 63.94 m | 9.7 / 54.9% | Reuse only its `[11,22]→valley` portion for this loop. Shelf changed southern sections. |
| `return`, valley ↔ Cloudbreak | 2.8 m | 84.81 / 85.69 m | 13.0 / 23.7% | Preferred shorter scenic excursion. |
| `ridge`, valley ↔ summit | 2.6 m | 90.54 / 95.15 m | 29.4 / 73.7% | Optional strenuous climb. |
| `overlook`, summit ↔ Cloudbreak | 2.5 m | 66.72 / 69.35 m | 24.8 / 49.2% | Optional loop descent/ascent, validate both ways. |

Authored widths are paint/path descriptors, not measured guaranteed clear widths. The controller walks at 2.1 m/s, runs at 4.6 m/s, is 1.9 m tall and snaps up at most .42 m. It has no explicit slope-angle limit. Smooth steep terrain can therefore pass simulation while remaining visually uncomfortable. Do not change physics or grade the ridge to make this plan pass.

## 4. Selected experience and visual priorities

**Optional loop:** Telaga Awan side exit → existing forest branch → valley junction → Cloudbreak → optional Crown Ridge extension → valley → same branch → town. Either direction around the western circuit is possible; introduce the easier Cloudbreak out-and-back first. Full authored circuit from branch head is **337.42 m plan / 346.51 m sampled surface**, excluding small stopping deviations and the walk within the square. Cloudbreak out-and-back is **264.96 m plan**. At normal input speed these imply roughly 2.7 and 2.1 minutes of uninterrupted horizontal travel respectively; allow **5–8 minutes as a design estimate** with stops, orientation and reading, not a timed novice result.

Cloudbreak interaction: **“Observe Cloudbreak”**. Short fictional place note about the cloud-facing edge and the return trail; acknowledgement “Cloudbreak discovered.” Promise a cloud/forest panorama, not a close waterfall view. Retain water as scenery and sound only if an existing audio resource actually exists—none was verified here.

Crown interaction: **“Read the ridge marker”** or “Observe Crown Ridge” if no physical marker is used. Fictional field-observer note inviting the player to look back toward the town and distinguish the low valley route from the ridge trail. Acknowledge “Crown Ridge discovered.” No fabricated historic survey, Indonesian location, transport statistic or research conclusion. Provide an optional link to the existing transit study through the shared panel, clearly separate from the fictional landscape note.

The two discoveries are independent, available before/after/between quest objectives. Neither unlocks research, changes Nadia's dialogue, or advances Beyond the Station. Discovering both gives one short “Two viewpoints explored” message, with no item, currency or quest reward.

### Three highest-impact issues

1. **Destination/route identity is weak** — highest exposure and low-risk fix. The real ridge/Cloudbreak HUD still says “Market Street”; trail junctions do not explain which branch returns to town. Add locality-aware place labels and at most two restrained wayfinding cues at the existing branch head and valley junction. Avoid constant arrows and do not replace the research objective HUD.
2. **Ridge foreground is repetitive and has no clear stopping cue** — prominent during the climb. Fresh switchback and summit views show broad smooth green areas, repeated pale tread bands and isolated grass strokes. Preserve the terrain/material system and existing boulders. First use a small observation marker and a deliberate viewing orientation; only if still weak, reuse one existing low trail-plant cluster beside the pocket. No blanket groundcover increase, global relighting or new rock scatter.
3. **The scenic reward needs honest framing and edge legibility** — Cloudbreak's cinematic view exposes water that its follow view does not. Keep the interaction inland, look across clouds/forest, and make the return direction readable. No cliff descent, new deck or clearing trees to force a waterfall panorama. Retain current canopy variety and forest boundary; no broad vegetation redistribution is warranted.

These are provisional scene observations, not owner approval or a numerical art score. The short wilderness camera checks did not reproduce a critical blocker. If full F1A traversal does, record exact player/camera/obstacle evidence and escalate; do not turn F1 into E1C.1 repair.

## 5. Asset-first scope

Available now: cached `assets/game/scenery/canopy-tree.glb` (719,224 bytes) and `fern.glb` (104,876 bytes), Quaternius Stylized Nature MegaKit, **CC0-1.0**, recorded in `assets/game/scenery/source.json` and `ASSET_MANIFEST.md`. Existing `nature.js` supplies reusable rock/low-plant geometry, five cached canopy forms and instanced trail details. Existing town props are Kenney Furniture/Food Kit CC0 models with exact records in `assets/game/town-population/sources.json`; a bench exists but is **not needed** on these sloping sites. Preserve all 42 town placements.

No downloaded trail sign or survey-marker GLB was verified. Do not describe one as available. Prefer the project's existing timber/material and sign-authoring patterns for two small original wayfinding cues; these are a bounded future implementation allowance, not an asset-acquisition task. If text cues suffice, add no mesh at the discovery points. Do not extract an existing approved building's geometry or alter its shared materials.

## 6. Minimal interaction and persistence design

Use one small future `assets/js/floating-atlas/wilderness.js` containing descriptors, proximity selection and save sanitization; no quest engine. Descriptor fields: `id`, `realm`, `worldXZ`, `interactionRadius`, `routeId`, `viewDirection`, `title`, `fictionalText`, optional `projectId`. This is the only abstraction needed for later realms.

Extend existing `entry.js` interaction selection, `getDialogue`, action dispatch and frame snapshot. Priority remains active modal → existing Guild/research/quest/Nadia interaction → wilderness proximity. Existing targets must never be shadowed. Check grounded state, vertical separation and unobstructed approach; radius alone must not activate through a slope or rock. Crown radius initially ≤1.2 m, Cloudbreak ≤1.8 m; final values depend on F1A.

Reuse `createAdventureUI` native dialogue and the existing close/Escape/focus/pause ownership in `living-atlas-controller.js`. Its current research-journal branch is quest-specific; add a narrow wilderness copy branch **before** research/legacy-story selection. Do not route wilderness through the legacy combat story or its journal. Mark discovery only on the explicit observation action; repeat interaction is idempotent. Use the existing status announcer for acknowledgement. An optional short discoveries section may be added to the native journal without changing the research quest's 0/3–3/3 meaning.

Save separately as an optional sibling of `adventure`, e.g. `exploration: {type:'transit-discoveries',version:1,realm:'transit',visited:['cloudbreak','crown-ridge']}` in the existing session envelope. Accept only these IDs, deduplicate and discard malformed/wrong-version/wrong-realm data. Never modify the quest save contract. Pass `savedExploration` through the existing mount/restore path; merge the sibling in the existing `persist()` hook on discovery and mode transition. Preserve it when Professional Mode is active or the wilderness layer is temporarily disabled. Session reload and Adventure ↔ Professional retain it; a fresh browser session may reset it. Do not promise cross-device or permanent persistence.

Gate future work behind localhost-only, default-off `wilderness=r0f1` plus the accepted town flags. No new assets/modules requested with it disabled. No auto-walk, teleport, forced camera turn, new input/controller, pathfinding, renderer or collision engine.

## 7. Performance and preservation constraints

Latest relevant integrated evidence: [E1C performance](../../validation/transit-e1c/performance.json), M4 Pro, standard shadows, Glass B, 1280×656 DPR 1. Matched warm camera rail: story off/on median **16.7/16.7 ms**, p95 **27.8/22.3 ms**, **338–417 all-pass draw calls**, **2.546–2.624 million submitted triangles**. Scheduling differed; this is historical evidence, not a measured wilderness budget or proof of improvement. Older R0-A3 timings describe a different scene and must not be substituted.

Future incremental targets, **estimates until measured**: no network binary additions; two batched cues and up to one reused low plant cluster, ideally <1,000 visible triangles, ≤2 new materials, ≤4 all-pass draws at matched settings, no transmission, no new large textures. Text-only observations add zero 3D triangles; proximity checks involve two destinations/two junctions, not per-frame island-wide mesh queries. Any existing alpha foliage addition must be assessed for overdraw and rejected if unnecessary.

Measure matched off/on walking and one existing rail using the same resolution, quality, Glass B, cache and active town layers. Report frame median/p95, calls, submitted triangles, texture/resource deltas and disabled requests. Do not infer GPU or mobile performance. If timing differs materially, repeat only the relevant matched run before attributing causality.

Freeze terrain vertices/sampler, cliff/waterfall geometry, tree instances/colliders, all town transforms/props, skyport/Guild, controller/camera and six studies. No shared-material mutation. Checkpoint exact changed/untracked files before future implementation, preserve unrelated work, and own/dispose only new resources. Removing `wilderness=r0f1` must restore the accepted view and behavior without deleting quest/discovery saves.

## 8. Terra-ready execution roadmap

### F1A — Make the existing circuit readable and verify access

- **Scope:** authorize only `assets/js/floating-atlas/wilderness.js` (route/junction data and two cues, no discovery state yet), `entry.js`, and the smallest locality/minimap-label adaptation if required in `minimap.js`. Reuse current sign/material/cache patterns. Approved terrain, `plan.js` route geometry, town placement and physics remain read-only.
- **Playable result:** from the square, the player can recognize the forest exit, choose Cloudbreak versus the strenuous ridge, and find the way back. No fake discovery buttons, quest objectives or completion counter.
- **Validation:** walk branch → valley → Cloudbreak → ridge → valley → town continuously with the real explorer, then reverse, without review teleports. Test stopping pockets, turns, running/jump/landing on supported ground and a controlled recovery check using existing recovery behavior. Record actual clear widths, bottlenecks, slips/falls, camera occlusions and end-to-end time. Sampled simulation is supporting evidence only.
- **Checks:** reuse the two focused landscape checks above plus relevant character tests. Capture actual departure junction, Cloudbreak follow view and Crown return vista; include calibrated eye-height inspection where the existing QA harness supports it, clearly separate from traversal. One matched off/on cost sample; disabled requests/resource restoration.
- **Rollback/DoD:** default/public and flag-off untouched; one scene/controller; all routes acceptable in both directions with no new obstruction. If an existing route fails, permit only a bounded new cue/anchor adjustment within the same clearing. If support/approved geometry or camera changes are needed, stop with evidence for owner/Sol decision; no stealth repair. Owner review required before F1B.

### F1B — Two meaningful observations and reliable restoration

- **Scope:** extend `wilderness.js` and `entry.js`; narrow changes to `adventure-ui.js` and `living-atlas-controller.js` for the dialogue branch, independent exploration sibling and acknowledgement. Existing `project-panel.js`/registry API reused unchanged where possible. No new binary assets.
- **Playable result:** both landmarks can be observed in either order; truthful 0/2–2/2 discovery acknowledgement remains separate from Beyond the Station. Full authentic study remains independently readable.
- **Checks:** one focused sanitizer/idempotence test file; relevant `transit-quest`, `living-atlas`, `experience` tests. Browser: discover before accepting Nadia's quest, repeat, Escape/close, resume movement, reload, switch modes and return, open/close Guild study, preserve partial/completed quest saves. Screenshots: each observation and combined acknowledgement. Compare matched costs only if new render resources were added.
- **Rollback/DoD:** independent tagged state survives the existing session lifecycle; invalid saves fail closed; no input/focus leak or combat activation; removing the flag restores E1C without losing its progress. Stop for owner review.

### F1C — Bounded composition polish and final circuit acceptance

- **Scope:** new wilderness-layer placements/cues and locality copy only; optional single reused plant cluster, grounded through current support. Reuse `nature.js` resources without redistributing the forest or changing its source generation. If reuse requires broad refactoring, omit the plant addition. No lighting/camera overhaul.
- **Playable result:** two distinct, uncluttered stopping experiences and an intelligible town/forest transition. Preserve already good canopy, geology, water and atmosphere.
- **Checks:** correct only the three issues above; matched before/after departure, Cloudbreak and ridge views with player scale, plus one context aerial. Repeat affected route segments and the full optional loop once, verify research/Professional access, relevant landscape/character/Guild/quest tests and final matched performance/resource deltas. No unrelated historical suite.
- **Rollback/DoD:** approved source/geometry hashes unchanged outside the authorized additions; no blocking collisions/camera failures; acknowledgements accurate, no forced research gating, owner visual approval still required. Any reproduced critical camera blocker is escalated as deferred E1C.1 evidence, not silently repaired. No deployment or automatic next phase.

## 9. Copy-paste F1A implementation prompt

> Implement R0-F1A only after owner authorization. Read this plan; do not repeat the island audit. Preserve E1C and deferred E1C.1 behavior. Checkpoint exact affected dirty/untracked files without disturbing unrelated changes. Behind localhost-only default-off `wilderness=r0f1` and the accepted town flags, make the existing Telaga-side branch and valley junction readable using at most two restrained shared-material cues and correct local place names. Limit changes to `floating-atlas/wilderness.js`, `floating-atlas/entry.js`, and a necessary minimal `minimap.js` label adaptation. Use the current RESET transform and `town.heightAt`; do not use old skyport coordinates or edit paths/terrain/vegetation/controller/camera. Preserve one world/cache and all research access. No discovery state, quest extension or inactive placeholder interaction in F1A. Validate the actual explorer continuously town→branch→valley→Cloudbreak→Crown Ridge→valley→town and reverse, including stopping pockets, camera rotation, jump/landing and existing recovery. The local simulations are not full traversal approval. Keep Crown's cue outside its narrow walkable pocket; no bench/platform. Do not create waterfall access. If actual safety or support needs approved geometry/camera changes, stop with exact evidence rather than rebuilding. Reuse focused landscape/character tests and QA presets, capture real route/player views, measure matched flag-off/on costs and disabled requests. Deliver the readable playable circuit, exact changes, traversal limitations, preservation/rollback evidence and concise metrics. STOP for owner review before F1B. No deployment.

## 10. Stop and unresolved gates

Only this planning document is delivered. No game, asset, scene or camera changes are authorized by F1.

1. Full populated-town departure/return and continuous browser loop remain unverified; F1A is the gate.
2. Steep ridge segments and Crown's constrained stopping pocket need player/camera acceptance, not merely controller success.
3. No safe player-height waterfall discovery has been established; it is excluded, not an unfinished promised feature.

This pattern can later be reused as descriptors + existing support + contextual interaction + independent acknowledgement. Do not build a generalized six-realm engine or reuse Transit Kingdom's fictional notes as research for another island.
