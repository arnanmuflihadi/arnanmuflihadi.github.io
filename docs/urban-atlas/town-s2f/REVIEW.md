# S2-F controlled integration

**Implemented locally; off by default. Not deployed. Owner visual review pending.**

[Game review](http://127.0.0.1:4173/index.html?experience=adventure&dev-town=s2f&town-review=1) · [Screenshot gallery](index.html) · [Rollback](ROLLBACK.md) · [Measured results](../../../validation/town-s2f/results.json)

## Implementation and preservation

The existing `mountUrbanAtlas`, world manager, scene, renderer, explorer, input and follow camera remain authoritative. A localhost-only `dev-town=s2f` flag dynamically loads the four approved exports through the shared model library and cached GLTFLoader. Public origins reject the flag. Default URLs request none of the town exports. Development saves use a separate session key.

The roots retain translation `(36, 18.6, 44)`, unit scale and approved orientation. The four building transforms, physical glass, textures and approved Blender/GLB files are unchanged. Three old study-grading meshes remain hidden, consistently with S2-D/E. No second terrain reference, scene, renderer, character or movement system is instantiated. The 100-triangle support reference is queried but never rendered. Existing support indexing, collision slide/block functions and the original character controller handle the new surfaces. Mesh raycasts extend the existing follow-camera clearance to the imported town.

Only the four documented showcase-canopy instance adjustments are applied. Every original island vegetation matrix/count and terrain vertex remains unchanged. The original obstacle-array identity is restored on toggle-off. Re-enabling reuses the same scene, meshes and cache without new requests.

The complete pre-change tree is checkpointed as `codex/checkpoint-s2e-before-s2f` / `3f9e479fb0e656ee563fd9ec66ed2bfbac73c1aa`. All 3,102 pre-existing non-ignored files were compared: only the two authorized integration files and two historical preservation tests changed. No approved asset/archive or source license changed. The historical tests now verify the exact pre-integration bytes and a narrow before/after authorization record for those two seams; they still freeze every other original path.

## Live traversal

These are real-time runs of the **existing animated game explorer**, normal update loop, collision, terrain support and follow camera. They are not AABB-only or standalone-preview claims.

| Route | Result | Distance | Time |
|---|---|---:|---:|
| Natural ground → provisional landing → bridge → market stairs → square threshold | PASS | 69.49 m | 33.12 s |
| Complete reverse route to natural ground | PASS | 69.50 m | 33.12 s |
| Garden ramp toward square threshold | PASS | 16.82 m | 8.11 s |
| Garden ramp return toward market | PASS | 16.83 m | 8.11 s |
| Market jump/landing run | PASS | 17.89 m | 8.59 s |
| Lateral guard probe | PASS, stopped by guard | 4.64 m | 4.28 s |

Main/return maximum stair increments were 0.1743 m / 0.1690 m, below the existing controller's 0.42 m step limit. No unexpected airborne frames or large support discontinuities occurred on the main/ramp runs. The jump test recorded exactly one takeoff and landing, approximately 1.16 m maximum foot clearance. The garden alternative remains a steep controller-compatible route, not a claim of universal wheelchair access.

The original 9.5 m follow distance is retained. Closest measured camera-to-player-root distance was approximately 1.57 m during constrained views; it retracts using original camera logic plus town mesh clearance. This is not a guaranteed camera-volume sweep for every possible user angle. Fixed architectural captures hide the avatar only because a camera at its 1.65 m eye position would otherwise be inside its head. Manual movement exits that inspection state and restores the avatar. The mandatory third-person capture records **Walk**, real displacement and advancing animation time. A complete main-route run was repeated after the inspection correction.

Additionally, the production controller completed all four main/ramp directions at 20/30/60 Hz in 12 deterministic regression scenarios, with no unexpected falls.

## Performance

Hardware reported by the browser: **Apple M4 Pro, ANGLE Metal, Chrome 156**. Standard quality, antialiasing on, DPR 1, 1354 × 1130 drawing buffer, PCFSoft 2048 shadows, ACES exposure 0.96, camera far 1600. The full screenshot includes the existing header, making it 1354 × 1194. No glass downgrade, lighting change, quality change or texture substitution was used.

Paired measurements used the same existing world, 60° camera rail from arrival toward the square, stationary explorer at the same natural-ground point, two-second warmup and 12-second sampling interval. Town-off retains cached GPU resources; it measures rendering removal, not cold-load memory reclamation.

| Measurement | Town OFF | Town ON |
|---|---:|---:|
| Actual rAF samples | 2,138 | 1,144 |
| Frame time median / p95 | 5.5 / 6.6 ms | 11.1 / 16.7 ms |
| CPU render submission median / p95 | 0.6 / 0.7 ms | 3.5 / 4.8 ms |
| All-pass draw-call range | 135–144 | 280–575 |
| All-pass submitted triangles | 2.332–2.359 M | 2.587–4.143 M |

Actual moving main-route samples: 5.6 ms median / 11.2 ms p95, 249–589 draws and 2.502–4.152 M submitted triangles. The reverse route measured 5.7 / 11.4 ms. CPU submission is not GPU time; GPU timer, mobile hardware and browser process memory were not measured.

One fixed market-view WebGL capture counted **569 actual draw invocations**: 183 shadow, 188 additional offscreen/transmission and 198 canvas. The matched town-off view counted 141: 65 shadow and 76 canvas. This isolates the major cost: the authored transmission glass introduces an additional scene render, alongside extra static geometry/material draws and shadows. No further material optimization was performed. Current local performance supports continued owner review; it is not proof of lower-end/mobile readiness.

Town asset payload is **11,084,692 bytes**, including the unchanged 10,007,904-byte market. Actual Resource Timing recorded **11,085,892 transferred bytes** including response overhead, **11,084,692 encoded/decoded body bytes**, and local per-asset durations of 1.5–10.2 ms. These are localhost measurements, not internet delivery estimates.

Loaded asset inventory: 107 market meshes, six interface meshes, seven foundation meshes; one non-rendered support mesh. Potential visible geometry totals 186,361 triangles before view culling and render passes. Market: 59 runtime material variants / five textures; interfaces: six materials; hybrid: seven materials / one texture. No missing textures. The live game reported 234 geometries, 23 textures and 62 programs in a representative town-on view; heap was available around 85 MB, not a process/GPU-memory measurement.

Shared-library cache: six requested/loaded/cached files (four town exports plus the island tree and fern). Repeated off/on switches retained six requests and the same scene UUID/renderer. The explorer, resident and jump-animation files retain their existing separate character loader. Default reload verified only the original landscape/character resources, no town GLBs and no review UI.

## Evidence and regression

Seven fixed captures and one active third-person capture are in `validation/town-s2f/`. Each fixed view stores its current camera/quaternion/FOV, URL, player support, renderer/scene identity and settings. The aerial and street comparisons use the same cameras for town-off/on. The contact sheet arranges actual screenshot pixels, not generated illustrations.

- **52/52** focused landscape, character, architecture, living-atlas, town-layout and new integration tests passed.
- **28/28** asset-foundation, architecture-design-system, experience/navigation and atlas-repair checks passed.
- **2/2** environment-polish tests passed. Total: **82/82 relevant automated checks**.
- Home/editorial/adventure switching, Work's six-study index, `project=mbr` research panel, default reload and in-place off/on were checked in the actual browser. One game canvas/renderer remained in each page; toggles kept the same scene UUID.
- Current integrated QA reported **zero errors and warnings**, and no missing textures. An initial development-only use of a non-exported Matrix4 constructor was corrected to the bundled Object3D matrix API before the recorded validation runs.
- The broad static-site audit still fails **58 inherited editorial/footer/hero/manual-fallback expectations**. Its script, all audited pages and referenced missing assets are unchanged from the checkpoint. These are explicitly recorded in `static-audit-summary.json`; this report does not claim that audit passes.

Commands and full results: `regression.log`, `asset-navigation-regression.log`, `integration-tests.log`, `static-audit.log` and `results.json` beside the captures. No unrelated full-town construction or deployment was performed.

## Remaining visual limits (owner review)

1. **Protected vegetation overlaps:** original grass/foliage can protrude through paving and some town margins. Correcting those instances requires a separately approved vegetation-clearance edit; none were silently removed here.
2. **Lighting/export appearance:** the existing game's broad daylight and absent studio environment make the glass and shaded timber darker/flatter than Blender's presentation. Approved material identities and glass were preserved; no new material pass or postprocessing was introduced. Fine paving/roof patterns also alias in some views.
3. **Unfinished destination composition:** the threshold opens onto the reserved natural landscape, with no built square/Guild/skyport landmark yet. The route is traversable and guarded, but its final vista and arrival architecture remain visibly incomplete by phase scope.

Compared with the original concept, the four-building family now occupies the real island with continuous stairs, planted edges and legible supports. This is a limited integrated vertical slice, not the completed concept town. No human artistic score or approval is awarded. **Stop for owner review; do not deploy or start another district.**
