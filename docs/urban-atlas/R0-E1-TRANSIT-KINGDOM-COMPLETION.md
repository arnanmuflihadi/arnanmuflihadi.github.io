# R0-E1 — Transit Kingdom completion master plan

10 November 2026 · Sol planning and technical judgment · Terra implementation handoff

**Planning only. No implementation is authorized by this document.** The owner’s latest approvals govern the baseline, including where older review documents still say approval pending. Dragons, boarding, flight and transfers are paused. Keep their evidence intact and inactive.

## 1. Executive decision and evidence

**Freeze the environment; connect it to a short research fieldwork quest.** The accepted local town is an explorable architectural environment with a working research endpoint, not yet a complete RPG level. Another architecture, terrain or asset-search phase is unnecessary. Reuse Nadia, the existing resident model, dialogue dialog, research registry, Guild trigger, input, camera, persistence plumbing and loader.

The accepted development URL is:

```text
http://127.0.0.1:4177/index.html?experience=adventure&project=transit&dev-town=s2f&town-layout=reset-final&town-props=cc0&town-guild=r0c2&town-skyport=r0c3&town-skyport-polish=r0c3-1&town-review=1
```

Port 4177 was accessible during this audit; a future executor should reuse a healthy documented loopback server rather than assume this port persists. **Omit `skyport-demo=r0d1`.** Omit `town-review` for clean player-facing review; it is a QA overlay, not a product feature.

Fresh evidence from the current working tree and actual browser:

- R0-C3.1 diagnostics confirm the rebuilt town, Guild and skyport/polish enabled, **17 prop types / 42 instances, Glass B, one renderer and one scene**. Arrival, Market Street, Guild-square and whole-island presets were inspected.
- Original animated explorer completed the existing forward route **42.22 m / 20.16 controller seconds**, and reverse **42.16 m / 20.16 s**. Both reached endpoints, with no reported errors/warnings. These are controller traces, not novice completion times or proof of future NPC/clue access.
- Actual **E** at the Guild opened the authentic transit panel. Scenario A displayed **29.67**, B **37.55**; closing returned to exploration. Switching to Professional Mode retained the same scene ID and renderer count. A separate `portfolio.html?project=mbr` visit exposed all six study links without gameplay.
- Fresh scoped command: `node --test tests/living-atlas.test.mjs tests/floating-atlas.test.mjs tests/atlas-guild.test.mjs tests/skyport-polish.test.mjs` → **17 passed, zero failed/skipped**. Some tests cover older district fixtures; they do not establish a working town quest.
- Review settings: **1280×656 game buffer within a 1280×720 browser, DPR 1, ACES exposure 0.96, standard shadows**. Live Market camera: position `(7.60365,16.94500,59.28728)`, quaternion `(0.00389,0.30070,-0.00123,0.95371)`, FOV 60°, eye **1.65 m** above support.

This read-only phase created no gallery or assets. Existing saved browser images below are **historical evidence**, supplemented by fresh live inspection, not represented as newly captured files: [arrival](../../validation/skyport-r0c3-1/02-spawn-after.png), [island](../../validation/skyport-r0c3-1/04-island-after.png), [actual explorer](../../validation/skyport-r0c3-1/06-gameplay.png), [Market Street](../../validation/atlas-guild-r0c2/04-game-market-after.png), [square/Guild](../../validation/atlas-guild-r0c2/05-game-square-after.png). Reproducible current cameras are in [reconstruction-review.js](../../assets/js/floating-atlas/reconstruction-review.js).

## 2. Current completeness audit

| Area | Verified implementation | Missing or limited; decision |
|---|---|---|
| Island silhouette, cliffs, waterfall | Authored floating island, geology, cloudscape and waterfall retained; whole-island composition inspected | Freeze. No evidence justifies terrain or distant-silhouette reconstruction. Detailed waterfall polish was not re-audited. |
| Forest, trails, exploration | Accepted vegetation and natural trail network; current scoped terrain/movement tests pass | Preserve. Highland/scenic exploration is optional, not a compulsory long quest leg. |
| Architecture and civic hierarchy | Four distinct tropical shopfronts, 6 m street, 210 m² square, fountain, pavilion, Guild and skyport | Freeze models/transforms/foundations. No interiors implied. |
| Shop function and street life | Named façades, café settings, books/counter, seating and curated props | Static scenery; no useful shopfront investigation actions. One guide exists elsewhere, not in the town journey. |
| Skyport | Finished arrival identity, guards, canopy, signage and polish | Future transport only. Keep the landing zone non-operational; no travel-shaped quest requirement. |
| Atlas Guild | Recognizable landmark, supported entrance/stairs, actual research trigger | Research opens correctly; no quest briefing/submission or completion acknowledgement. |
| Light/materials/atmosphere | Shared daylight, shadows, warm mineral/timber/terracotta palette, optimized Glass B | Close façades are subdued and inactive-looking. Only small interaction-readability corrections are justified; no global relighting. |
| Character and controls | 1.9 m explorer; walking/running/jumping, follow camera, collision/support and recovery | Preserve mechanics. New interaction footprints and camera clearances still require actual walks. |
| NPC/dialogue | `guide.js` creates **Nadia**, at legacy world `(-13,3)`, height 1.72 m, facing the player; native dialogue and authored resident animations exist | Current guide is disconnected from the new arrival/café route. No second NPC or wandering AI is needed. |
| Quest/progress | Legacy combat story modules and UI exist elsewhere | Active floating entry returns `adventure:null`; save/snapshot methods return null, request action only handles jump. No active research quest. Legacy “Lost Survey Signal” must not be mistaken for implemented Transit gameplay. |
| UI and onboarding | Mode switch, E prompt, controls, jump button, minimap, dialogs and study tabs work | Help/location/research copy still says buildings/realm are unconstructed. Minimap draws legacy trails and ignores the passed quest marker. No current objective/acknowledgement. |
| Portfolio | Shared six-project registry, canonical case studies and project panel, direct editorial access | Preserve content and IDs. Runtime constructed-capability and local return-link context need correction, not a second website. |
| Performance/assets | Shared world/library; instanced props; existing resident already loaded in Adventure Mode | Current guide bypasses cache ownership with a direct loader; reuse must fix ownership for the optional town guide without breaking flag-off behavior. |

Primary source files: [entry](../../assets/js/floating-atlas/entry.js), [guide](../../assets/js/floating-atlas/guide.js), [controller](../../assets/js/living-atlas-controller.js), [state](../../assets/js/living-atlas-state.js), [dialog UI](../../assets/js/adventure-ui.js), [registry](../../assets/js/project-registry.js), [Guild](../../assets/js/floating-atlas/guild-integration.js), [minimap](../../assets/js/floating-atlas/minimap.js). The installed skill’s R0-B1 context is historical; it must not override the approved RESET-FINAL town.

## 3. Three highest-impact visual/experience deficiencies

These are provisional internal observations, not a human score or an instruction to rebuild the island.

| Rank | Evidence and player impact | Bounded correction | Exposure / complexity / risk |
|---|---|---|---|
| **1 — No human focal point on arrival** | Live arrival/market view is architecturally coherent but has only static props; E offers “Find a guide or landmark.” Nadia is far away at the legacy valley point. | Reuse that **one** guide at the café-side arrival pocket, grounded on actual support, facing approaching visitors. Idle and optional existing Wave; no crowd. | Every arrival; small integration change; low asset risk. |
| **2 — Guidance contradicts the built town** | Live `project=transit` Adventure entry immediately opened a panel saying “realm is not constructed.” Minimap shows old trails/building dots without the civic spine or destination labels. Help repeats obsolete landscape-only guidance. | Runtime-aware copy/capability, one objective card, current promenade and three restrained map labels. Preserve natural trails and ordinary Professional Mode. | Entry and every navigation decision; moderate UI/state work; highest regression risk. |
| **3 — Useful frontages do not advertise a purpose** | Market/Guild views show deep-shaded glazing, closed façades and small signs. Existing books, seating and research entrance look decorative until the visitor is almost on them. | Make the existing book display and square seating edge readable investigation stops with concise contextual prompts and restrained focus emphasis. Inspect near-camera contrast first; only a tiny local label/material adjustment if still unreadable. | Repeated on the main route; low/moderate effort; avoid shared-material mutations. |

Freeze building forms, fountain scale, canopy, vegetation composition and daylight. Do not add more props to solve these three problems. Any major reconstruction requires separate owner approval with a reproduced defect.

## 4. One quest: “Beyond the Station”

**Premise:** Nadia, the existing fictional Transit Planner, is preparing an accessibility field note. She asks what a feeder network changes—and what an average improvement cannot tell us. The player investigates existing town objects, then files a short interpretation at Atlas Guild. The fantasy town is an analogy, not measured Jakarta geography or a simulated GTFS network.

**Start:** café-side arrival pocket by Kopi Awan. First greeting: “A station is only part of a journey. Help me compare what becomes reachable when feeder routes join the network.” Choices: **Start the field note / Explain accessibility / Show the full study / Later**. Mark Nadia as a fictional guide, not a real project collaborator.

Three objectives maximum:

| Objective | Existing location / action | Authentic learning and completion event |
|---|---|---|
| **1. Compare the two networks** | Lembaran book/counter display. Inspect A and B cards using `projectById('transit').scenarios`; explicitly **Record comparison** after both have been opened. | Same 60-minute setting; backbone versus Mikrotrans-integrated network. Mean modeled scores 29.67/37.55. `networkRecorded`; merely walking past/opening a journal does not count. |
| **2. Interpret the improvement** | Existing Telaga Awan seating edge. Read registry `finding` and `caveat`; answer “Does a higher average mean equal access everywhere?” | Correct response: **No—gains remain geographically uneven.** Explain gently and allow retry; no penalty, timer or health. `equityRecorded` after acknowledgement. |
| **3. File the research note** | Existing Guild entrance. E must still open the authentic study. When ready, an additional **File field note** action acknowledges the conclusion. | `guildSubmitted` requires both observations and an actual Guild-origin study interaction. Show “Field note complete,” concise finding/limitation, **Read complete case study / Keep exploring**. Optional return to Nadia gives a thank-you, not another objective. |

The journal gives one active objective, 0/3→3/3 progress and the next named destination. Completion is an explicitly fictional field-note acknowledgement, not a professional certificate, new statistic or research result. Full research is always available before accepting/completing anything.

**Content authority:** [project-transit.html](../../project-transit.html), sections `#ch-01`–`#ch-05`, and the existing registry. Explain cumulative opportunities within a time budget; the page documents **r5py transit+walk routing, AHP-weighted destinations and Getis-Ord Gi***. Use the registry’s existing finding of **26.6% average modeled improvement across 261 villages**, retaining uneven gains and modeled-not-observed caveats. Do not recompute a precise uplift from rounded 29.67/37.55, claim a time saving, invent station/facility counts, or assign real findings to fictional shops. Any additional factual teaching copy must cite its canonical page section in data comments; missing evidence blocks that copy.

**Timing:** first-visitor target 5–10 minutes, not measured yet. Budget roughly 30–60 s orientation, 45–90 s conversation, 60–120 s comparison, 45–90 s interpretation, 45–90 s Guild review, plus walking/exploration. The existing spine takes only ~20 s to walk: do not pad it with detours, forced reading waits or fetch items to manufacture duration. Faster informed visitors may finish sooner. Measure a novice run in E1C.

## 5. Landmark functions and planned interaction anchors

| Place | Minimal role |
|---|---|
| Pelabuhan Awan | Arrival, short control/orientation hint; “Future destinations” information only if useful. No operational transport prompt. |
| Kopi Awan | Nadia’s briefing and optional later acknowledgement; exterior only. |
| Lembaran | Network-comparison field note at existing books/counter; first environmental interaction beyond Guild. |
| Rupa Rimba / Serambi | Preserve artisan/corner identities, clear doors, balconies and square enclosure. No fabricated shop/inventory system or forced interaction for every façade. |
| Telaga Awan | Interpret findings at existing seating, fountain as orientation focus; second environmental interaction beyond Guild. Pavilion stays a shaded gathering place. |
| Atlas Guild | Authentic study plus final field-note submission. Door remains an exterior interaction; no playable interior. |
| Highland/forest/overlook | Optional exploration after/between objectives; no compulsory climb or new quest waypoint. |

Use the existing `reconstruction-plan.js` **u/v coordinates and `toWorld`**, never obsolete town coordinates. Proposed anchors are planning candidates, not approved placements:

| Purpose | Candidate u/v | World X/Z and current support | Evidence limit |
|---|---|---|---|
| Nadia | `(-2.4,0.9)` | `(6.842,62.384)`, Y≈15.249 | Capsule-point predicate clear in current town/prop fixture. |
| Player talking to Nadia | `(-1.2,0.9)` | `(7.825,61.696)`, Y≈15.253 | 1.2 m from NPC anchor; actual animation, camera and access untested. |
| Book-display approach | `(1.8,4.2)` | `(8.390,57.272)`, Y≈15.317 | Clear predicate; visual target is counter `(3.3,3)`. |
| Square-note approach | `(4.1,17)` | `(2.932,45.467)`, Y≈15.515 | Clear predicate; target existing stone seating at `(5.4,17)`. |
| Guild | Existing `guild.interaction()` region | Existing entrance floor Y=16.05 | Reuse tested trigger; no replacement reservation. |

Fresh read-only measurements used the existing RESET-FINAL fixture plus solid prop-ledger bounds, radius 0.34 m. They do **not** prove reachability, ray visibility or camera clearance. A western square candidate was blocked and discarded; do not move its tree. Terra must walk the accepted candidates and may adjust only the **new NPC/interaction anchor** locally (about ≤1 m) if needed. Preserve doors and the central clear route; no furniture/tree/building relocation to force an anchor.

## 6. Minimal reusable gameplay architecture

**One small new module:** `assets/js/floating-atlas/transit-quest.js`. Keep immutable quest copy/field references, anchor descriptors, save validation, pure event transitions and snapshot selection together. Do not make a general quest-engine package.

State: tagged/versioned `transit-field-note`, realm/project `transit`, accepted flag, viewed scenario IDs, `networkRecorded`, `equityRecorded`, `guildSubmitted`. Derive phase/objective/completion; never trust a saved `complete` string. Unknown IDs/versions/events are sanitized; repeated events are idempotent. Gate observations by acceptance, current objective and the active in-world interaction. A Professional Mode study open does not complete a physical objective. Declining, closing a dialog, cancelling a panel or taking a scenic detour never resets progress.

Reuse/extend these exact seams:

| File | Authorized future change |
|---|---|
| `floating-atlas/entry.js` | Read `savedAdventure` (currently supplied by controller but ignored); own optional quest runtime; return real save/snapshot; dispatch existing `atlas:dialogue`, `atlas:interact`, `atlas:adventure-event`; resolve one prompt; expose runtime walkable-project capability. Preserve Guild’s ordinary E path and all lifecycle hooks. |
| `floating-atlas/guide.js` | Optional town guide spec/position/support and cache dependency. Reuse Nadia rather than add another resident. Ground via **town.heightAt**, not old terrain-only sampler. Stationary, limited face-player behavior; one visible-body collider through current obstacles. |
| `adventure-ui.js` | Add a research snapshot/journal/dialogue branch using the existing native dialog/buttons/status announcer. Do not require health/enemy fields for research snapshots. Resolve dialogue before taking input ownership; null/failed copy must not strand the player paused. Keep legacy encounter behavior isolated. |
| `living-atlas-controller.js` | Persist on existing quest-change/pagehide hooks; refresh pause/focus as today. Runtime capability must replace stale “unconstructed” decisions **only when the accepted town is actually loaded**. Fix conditional help/location/status text. |
| `project-panel.js` | E1B: optional contextual **File field note** action/callback, shown only for the active Guild-origin transit panel when prerequisites pass. Same registry/long-form links; ordinary study behavior unchanged. |
| `floating-atlas/minimap.js` | E1B: optional town context with current promenade, named skyport/square/Guild and active quest marker. Retain actual island boundary/trails; marker currently passed by caller is ignored. No new map engine. |
| `living-atlas-state.js`, `experience-controller.js` | E1B, only necessary routing/persistence edits: versioned optional save validation and localhost allowlisted review-context return links. Avoid globally changing `realmSpecs.constructed` or enabling other realms. |
| `assets/css/atlas-adventure.css` | Small journal/prompt/readability rules only; no portfolio redesign or global theme change. |

Flag proposal: **`town-story=r0e1`**, localhost-only/default-off and requiring the accepted populated town/Guild baseline. E1 review uses the skyport/polish flags above. Story off retains current guide/portfolio behavior and makes no new story-specific requests; invalid/public origins cannot activate it. Use an isolated story session namespace/version while retaining the existing mode/project/position mechanisms. Keep this same state when switching modes; preserve it through case-study navigation and browser Back. Propagate only known local development parameters on same-origin return links, never arbitrary query strings or public activation.

NPC source is already present: `assets/game/phase3/city-resident.glb`, **1,186,388 bytes / 5,776 triangles**, four meshes, nine materials, no textures, Idle/Interact/Walk/Run/Wave clips. Provenance: `assets/game/phase3/source.json` and `CC0-Characters.txt`, Quaternius CC0. No download/modeling needed. Use `world.library.get` through the existing optional catalog; clone the rig through the existing actor helper. **Library owns cached source geometry/materials; guide owns its clone/skeleton/recolored materials.** Do not call `disposeAsset` on a library-owned source or instantiate a second loader/cache. Preserve the existing default guide path unless the story flag is active.

Do not activate/rewrite the older combat `urban-atlas/quest-state.js` or copy its Sari/mosskeeper story into Transit. Do not build behavior trees, inventory, currency, combat, voice generation or an escort framework.

## 7. Player flow and preservation

Arrival reveals the approved street→fountain→Guild axis. Show one dismissible hint for move/look/jump/E and “Meet Nadia by Kopi Awan”; preserve touch/keyboard controls and reduced motion. Nadia’s pose and existing café setting provide the initial human cue. Use proximity + unobstructed context for prompts, with explicit disabled/completed states; do not use persistent floating arrows.

E opens the one appropriate interaction. Dialogue/journal/research/help/site menu pause movement through the existing coordinator. Enter chooses a focused option, Space must not trigger a jump while a dialog is open, Escape closes/cancels safely, focus returns to the canvas/control. Blur, hidden tab, mode changes, load failures and teardown clear held input. Do not change camera or controller physics; test a physical NPC collider instead of invisible walls/floors. Safe respawn retains quest progress.

Retain the original island, terrain/sampler agreement, trails, vegetation, four building transforms, supports, all 42 prop placements, fountain/pavilion, Guild/skyport GLBs, source masters and licenses. No whole-level relighting or material-quality downgrade. Keep Glass B with A as reversible reference. No new skyport/transport/Guild architecture.

## 8. Three implementation milestones

Common exclusions: no asset research, Blender authoring, interiors, extra NPCs, dragons/flight, new islands, terrain/town changes, renderer/controller replacement, dependencies or deployment. Each milestone gets an exact changed-file checkpoint including currently untracked files; preserve unrelated dirty work. A Git HEAD alone is insufficient in this working tree.

### E1A — Functional research gameplay core

- **Scope/result:** flag-gated Nadia at the café pocket, briefing/accept/decline, working network-comparison object, first objective recorded, compact journal and safe persistence/interruptions. Encode the three-objective state contract now, but wire only objective 1. After recording, expose truthful 1/3 progress; do not claim the complete quest is playable or add fake working square/Guild-submission actions.
- **Files:** new `transit-quest.js`; scoped changes to `entry.js`, `guide.js`, `adventure-ui.js`, `living-atlas-controller.js`, minimal `atlas-adventure.css`. No canonical research-number edits. Implement runtime-aware entry/help needed to stop the misleading initial study modal in the enabled town.
- **Reuse/assets:** existing resident/animations, books, dialogs, panel, cached models. No new binary assets. NPC placement and the comparison trigger must preserve all door/café clearances.
- **Tests:** one focused `tests/transit-quest.test.mjs` for order, invalid saves/IDs, idempotency, both-scenario requirement and no progress from unrelated/editorial study opens. Reuse living-atlas, floating-atlas, Guild, experience/registry tests. Check flag dependency/public rejection, disabled requests and shared-source disposal ownership. No exhaustive combat/historical suites.
- **Browser evidence:** actual explorer meeting Nadia; grounded eye-height NPC; comparison with genuine A/B values; journal 1/3; close/reopen, Escape, keyboard/touch controls, mode switch and reload. Walk arrival→NPC→counter→Guild and return; no AABB-only success claim.
- **Performance:** matched story off/on using current rail/settings and resident visibility; report calls/triangles/resources and walking median/p95. Reusing the already-loaded NPC should not add another character download or clone. Verify rather than promise zero rendering delta.
- **Rollback/DoD:** removing `town-story` restores baseline without changing any approved asset/placement. State is scoped; no stuck input, duplicate guide, resource disposal fault or false completion. **Stop for owner gameplay/visual review.**

### E1B — Complete the field-note quest

- **Scope/result:** connect square interpretation and Guild submission; all three objectives, correct retries, final acknowledgement and optional Nadia thanks. Full study/dashboard remain independently accessible throughout. No required NPC relocation/escort.
- **Files:** extend `transit-quest.js`, entry, dialogue/controller; add optional Guild action in `project-panel.js`, town/quest context in minimap; only necessary local return-link/state seams in `living-atlas-state.js` / `experience-controller.js`. Preserve E1A observations across reloads; no silent quest reset.
- **Tests:** extend the focused reducer tests for wrong order/answer, return visits, replay, forged completion, submission away from Guild and non-transit panels. Reuse experience/living/Guild/character tests; add behavior checks at existing seams, not a second test framework.
- **Browser evidence:** one continuous first-accept→two investigations→Guild completion run and return; journal at each change, incorrect-answer recovery, Guild panel close/Back, mode switches, full-case-study roundtrip, all six Work links and `project=mbr`. Capture square interpretation and final acknowledgement with the actual explorer. The tests must prove the newly added interactions, not merely rerun the old spine.
- **Performance:** same matched rail and active interaction walk; no new GLBs/textures expected. Verify repeated dialogs/re-entry do not grow renderer resources/listeners. Capture warnings/errors.
- **Rollback/DoD:** remove story flag or restore E1A-only file checkpoint; base Guild E still works regardless of quest state. Quest has an achievable ending without combat/transport; story cannot gate real research. **Stop for owner review of the complete loop.**

### E1C — Focused art, onboarding and final QA

- **Scope/result:** correct only the three ranked issues still visible: Nadia grounding/facing/greeting, coherent navigation/objective copy/map, readable investigation/Guild affordances. Reuse Wave only if useful. No architecture novelty or decorative density pass.
- **Files:** existing quest/guide/UI/minimap/controller seams, minimal local CSS or instance-owned label/material adjustment. No approved GLB re-export. Any proposed major reconstruction stops for separate Sol/owner review.
- **Tests:** rerun changed quest/UI seams and relevant experience, living-atlas, character, Guild, population, skyport/polish regressions. Reuse the current traversal/capture harness for doors, jumps, guards, fountain, highland and NPC/clue accesses; do not create another harness.
- **Browser evidence:** clean arrival, NPC/café, comparison, square, Guild completion and whole-island composition; one uninterrupted actual third-person quest recording/trace. Use existing fixed cameras for before/after; include the real HUD as well as clean art views. One novice timed run tests discovery/understanding; owner artistic approval remains separate from automated tests.
- **Performance:** fresh matched off/on sample, same hardware/DPR/shadows/Glass B and 2 s warmup + 12 s rail; active-walking timing separately. Investigate >10% median or p95 increase against this matched baseline before accepting it. Record cold/warm asset requests, calls, triangles, texture/geometry counts and errors. No mobile/GPU-readiness claim without those tests.
- **Rollback/DoD:** cumulative story-off/default-public restoration, same renderer/world, accepted assets preserved, accessible Professional Mode, no progression/camera/support blocker. Deliver concise evidence and remaining defects. **Stop for final owner acceptance; public release remains a separate decision.**

## 9. Completion gates, costs and risk controls

| Pillar | Definition of Done |
|---|---|
| **Environment** | Existing arrival, four façades, civic square, Guild and natural exploration remain coherent at 1.65 m and aerial views. New guide/interaction cues are grounded, readable and do not block doors, the route or research boundaries. No new major clipping/material defect. |
| **Gameplay** | One memorable fictional NPC starts an optional activity. Three or fewer objectives include two useful environmental interactions beyond Guild; journal/progress/acknowledgement work. Complete, retry, interrupt, return, save/reload and restart all behave predictably. Actual explorer walks every new approach. |
| **Portfolio** | Visitor can identify the transport-access problem, methods, feeder-network result and its limits; every factual statement traces to current registry/case study. All six studies and `project=mbr` work without playing. Study/panel/mode navigation retain context and exploration can resume. |
| **Engineering** | One scene/renderer/controller/cache, no new dependency or premature realm engine. Relevant tests pass with honest coverage limits. No unexpected requests when disabled, leaks or unhandled errors. Exact rollback and current performance evidence exist. |

Historical C3.1 matched rail (M4 Pro/ANGLE Metal, 1280×656 DPR 1, Glass B) measured **5.6/6.4 ms median/p95**, **338–417 all-pass calls**, **2.546–2.624 million submitted triangles** with polish on. These are [historical measurements](../../validation/skyport-r0c3-1/performance.json), not a new benchmark or GPU cost.

Fresh audit walks measured **11.1/22.3 ms** forward versus **5.6/6.0 ms** reverse; their views, load/timing conditions and directions differ. Do not call that a regression or compare it directly with the old rail. Fresh off/on measurements are required for each change. Renderer counters include relevant passes when the QA harness disables auto-reset; do not mix them with a lone color-pass counter.

Largest risks:

1. **State/input/lifecycle:** current save/snapshot stubs, combat-specific UI assumptions, dialog pause/focus and cache disposal can create softlocks or lost progress. Keep the pure reducer small; test interruption and repeated mount/unmount early.
2. **Truth and navigation:** stale `constructed:false`, old labels/minimap and flags stripped on Work/case-study links can contradict the loaded town or strand a local return. Use runtime capability and strict local URL context; do not globally mark other realms built.
3. **Visual/scale/performance:** a legally available resident still needs real grounding, facing, door clearance and camera review. Use only the selected new anchors; static predicate checks and old approved route tests cannot approve them. Avoid broad “polish” work when a prompt/location fixes the issue.

Terra owns bounded implementation and repeatable QA. Escalate to Sol only for a new state-ownership/renderer architecture decision, a need to move accepted geometry, canonical research ambiguity, or a reproduced performance problem whose cause lies outside these seams. Ordinary local bug fixes stay with Terra. No repeated historical audits or asset catalogs.

## 10. Future realm reuse boundary

Reuse only project-linked dialogue descriptors, validated quest save/events, landmark trigger descriptors, research-panel opening, runtime realm capability, navigation hints and shared cached actors/resources. Keep narrative, coordinates and environment separate from those seams. No multi-island transport manager now.

Future IDs already exist: `cbd` Merchant Citadel, `mbr` Mosaic District, `bandung-cafe` Bandung Highlands, `pangan` Harvest Valley, `alphaearth-food` Terra Observatory. Preserve their real research meanings; the last currently documents **historical paddy screening**, not unrestricted land-cover claims. Every realm remains unbuilt until separately authorized; none inherits Transit’s layout, quest text or completion flags.

## 11. Copy-paste Terra prompt — E1A only

```text
Implement R0-E1A only after the owner authorizes execution. Read
docs/urban-atlas/R0-E1-TRANSIT-KINGDOM-COMPLETION.md and use the installed
fantasy-level-design and game-visual-qa skills. Do not repeat the audit.

Preserve the accepted RESET-FINAL town, four shops, terrain/forest, 42 props,
fountain/pavilion, Guild, C3/C3.1 skyport, player/camera/controller and six studies.
Checkpoint the exact current changed/untracked integration files; preserve all
unrelated working-tree changes. Do not deploy or develop transport.

Behind localhost-only default-off town-story=r0e1 with the accepted town flags:
reuse the existing Nadia resident at the proposed café-side anchor, grounded via
town.heightAt, with the shared cache and correct source/clone disposal ownership.
Validate the anchor with the actual explorer; change only the new anchor locally
if necessary, never approved props/terrain/buildings. Keep one guide.

Create one small transit-quest.js module with the specified tagged/versioned
three-objective reducer/save contract. Wire briefing/accept/decline and objective 1
at Lembaran: inspect both registry scenarios, explicitly record the comparison,
show truthful 1/3 journal progress. Do not implement square/Guild submission yet.
Reuse native dialogue/status UI, pause/input/focus handling and existing research
panel. Add the research UI branch without activating legacy combat. Consume
savedAdventure and persist valid progress through existing hooks. Fix misleading
enabled-town entry/help decisions using actual runtime capability; keep public
and flag-off behavior unchanged. No new binary assets or research numbers.

Limit changes to the E1A file list. Add one meaningful focused quest-state test;
reuse relevant existing experience/living/floating/Guild tests and QA cameras.
Verify accept/decline, both-scenario gating, invalid saves, duplicate events,
close/Escape, movement resume, reload, mode switching, existing Guild study,
arrival→NPC→counter→Guild and return. Capture real NPC, comparison and journal
views; measure matched off/on walking/render costs and disabled requests.
No new renderer, movement engine, AI framework, interiors or dependencies.

Fix ordinary defects within scope. Escalate major architecture/research/approved-
geometry changes to Sol. Deliver the playable E1A core, exact changed files,
real evidence, test/performance results and rollback. Do not claim the full quest
complete. STOP for owner approval before E1B.
```

**E1 hard stop:** this plan and handoff are the sole new deliverable. No E1A implementation, asset creation, deployment or next phase has started.
