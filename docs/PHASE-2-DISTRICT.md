# Phase 2: integrated Jakarta district review

Implemented 1 November 2026. **Human visual approval is pending.** The user's
Phase 2 brief approves the architectural components for integration, not the
finished district. No visual score has been assigned. Review target: average
4/5 with no criterion below 3/5. Stop here for review; no further region or game
system has been added.

## Play and inspect

- [Home adventure](http://127.0.0.1:4173/index.html?experience=adventure&build=46)
- [Work adventure / neighborhood study](http://127.0.0.1:4173/portfolio.html?experience=adventure&project=mbr&build=46)
- [Fixed arrival comparison](http://127.0.0.1:4173/index.html?experience=adventure&district-review=spawn&build=46)
- [Preserved architecture showcase](http://127.0.0.1:4173/asset-showcase.html?build=35#pedestrian-composition)

WASD walks, Shift runs, Space jumps, drag or Q/R turns, E inspects a nearby guide
or study, and Escape pauses. Phone direction buttons support held input.
Read the atlas returns to the existing editorial content without replacing the
world. All six research routes remain available; only Jakarta landmarks support
walking. Fixed review cameras are opt-in through `district-review`; walking
releases the fixed camera and restores normal follow behavior.

## What changed

The 88 m conceptual play area now has a central fountain plaza, a 6 m commercial
avenue and secondary street, 4.5 m neighborhood lane, continuous footways and
marked crossings. Four mixed-use buildings address the avenue; three smaller
shopfronts address the neighborhood lane. Menara Teras anchors the business
approach opposite the vaulted Stasiun Taman hall. Imported window/entrance modules
form the station frontage and civic pavilion glazing. A transit pocket park and
Taman Teduh green park connect to the plaza. Thirteen buildings outside the play
bounds form street walls and skyline context, rather than collision destinations.

The approved office, commercial and neighborhood prototypes retain uniform
scale, materials, recessed windows, roof treatments and exported collision
geometry. The factory and loader files were not rewritten. Seven main retail
frontages now have real shallow shelves, books, cups and pots, painted room
silhouettes and controlled transparent display glazing. Distinct door leaves
remain legible. No enterable interiors or commerce mechanic is implemented.

Trees, palms, planters, ten benches, sixteen lamps, three café groups, cycle racks
and a bicycle, a shelter, bins, eight imported drains and five imported manholes
occupy furnishing zones. Shop signs use 2048 px wide CanvasTextures, aspect-matched
height, mipmaps, trilinear filtering and anisotropy capped at eight/device maximum.
The sky gradient, warm sunlight, soft shadows and distance haze provide atmosphere
without postprocessing or protected game assets.

## Technical evidence

| Check | Result and evidence |
| --- | --- |
| Full existing/new test suite | **67/67 pass**, zero skipped: [final log](district-review/test-results.txt). Original baseline: 55/60, [unaltered log](district-review/baseline-tests.txt). |
| Original scoped regressions | All 16 architecture, asset-foundation and character tests pass; their assertions remain intact. |
| Real imported assembly | **21 buildings = 8 main + 13 background**. **4 loaded GLBs / 4 requests / 3 prototypes**, [actual browser counts](district-review/loaded-assets.json). |
| Geometry and textures | Imported assembly **684,861 triangles**: 610,103 imported/source-derived + 74,758 authored; **125 batches**, independent tree graphs, **49 referenced textures, zero missing**. Whole-scene counters differ by view. |
| Main building collision | Every generated approved proxy compared to the planned transform within 0.00001 m, including the rotated neighborhood frontages. |
| Props | All four planters use their actual 2.5 m imported bounds; two imported bollards use actual bounds. Trees use imported lower-trunk bounds. Final minimap data includes async prop proxies. |
| Walkability | A half-metre-grid pedestrian-only search reaches all three research approaches, both parks, rear promenade and **every main retail door** using final imported obstacles. |
| Ground support | More than 4,000 unobstructed samples raycast the rendered geometry and match support within 0.035 m. Public paving excludes roads, ramps, pond and service court. |
| Movement | Primary and neighborhood crosswalks traverse grounded with smooth height transitions. Existing jump/wall/ceiling/tunneling tests pass. |
| Camera | Four public approaches at eight yaw angles remain outside actual building proxies; native walking also exercised the normal follow camera. |
| Failure and retry | Unit failure/retry passes; a temporary localhost fixture returned one deliberate tree 503. Research stayed readable, a study opened, and reload restored all 21 buildings. [Recorded result](district-review/failure-recovery.json), [fallback screenshot](district-review/asset-failure.jpg). Fixture stopped afterward. |
| Browser health | Final production preview has **zero captured warnings/errors**, one renderer: [record](district-review/final-browser.json). The deliberate 503 fixture is separate. |
| Source checks | 40 district/controller modules pass Node syntax checks; 23 touched source/test/doc files have no trailing whitespace or conflict markers. [Record](district-review/source-checks.json). System Git checks are unavailable because Git invokes an unaccepted Xcode license; no license was accepted. |
| Static audit | **58 unchanged findings, zero added/resolved**. It still exits with failure. [Every finding classified](district-review/static-audit-comparison.json), [final log](district-review/static-audit.txt), [baseline](district-review/baseline-static-audit.txt). |

The source parser used by Node tests intentionally removes image decoding only
from in-memory fixtures because Node has no browser image loader. Production
GLBs are not changed. Embedded buffers, source digests and textures have separate
foundation checks; the native browser confirms actual rendered materials and no
missing textures.

### Five inherited failures

No tests were deleted or skipped. Historical coordinates were migrated to
declared current surfaces, while actual support and circulation defects were fixed.

| Original failed test | Classification and evidence | Final repair |
| --- | --- | --- |
| `atlas-phase3`: NPC routes and quest approaches | Obsolete stoop fixture: `(8,-26.85)` and `(-20,35.15)` expected 0.365 m after the former buildings had moved; baseline returned -0.02 m. | Assert real approved porches at `(-24,-18.65)` and `(-19.2,28)`, top 0.26 m. Route assertions and the legacy court remain. Phase 2 activates only three existing research guides, not the optional encounter. |
| `atlas-repair`: steps and station ramp support jumping | Obsolete pre-shift station approach at z=-3.9, now inside the shifted hall; it was not a ramp start. A genuine pavilion datum issue was also found: the ramp previously began below its paved approach. | Test station approach z=7.1 and real ramp z=7..5. Pavilion ramp now starts on the actual 0.24 m promenade and rises to 0.57 m. Existing jump, solid wall and low-ceiling assertions remain. |
| `atlas-streets`: north sidewalk and curb ramps | Obsolete continuous strip z=-26.7 across changed building footprints; the south strip z=-19 also no longer described the public avenue. | Test the current unobstructed covered walk z=-17.9, south walk z=-8 and actual crossings. Fix a genuine 1 m rear-spine gap and relocate café chairs away from a door. New final-collision route test reaches every entrance. |
| `atlas-streets`: rendered paving/support | Obsolete ground sample `(15,-24)`: the baseline ray hit an old blocked landscape planter at y=0.14 while the fixture expected bare ground -0.02. That sample was not an unobstructed footway. | Keep the render/support and road-clearance assertions on actual public paving; shared polygon paving removes road-bridging/coplanar slabs. Add more than 4,000 unobstructed rendered/support comparisons. |
| `urban-atlas`: feet follow station ramp | Obsolete ramp coordinates z=-4/-5/-6 after the existing +11 m hall shift. Baseline returned the hall's 0.52 m at the supposed 0.24 m ramp start. | Use actual z=7/6/5 with heights 0.24/0.38/0.52 m. Keep all movement checks. `(20,27)` now correctly expects the deliberately paved green-park loop at 0.24 m. |

Other genuine defects found during integration: station corner support did not
follow its chamfered rendered outline; planter collision was too small; a café
chair obstructed one neighborhood door; the distant sky dome exceeded the aerial
camera's far plane. These are corrected and covered by geometry/route checks or
the final captures. This does not reclassify the old planter fixture as a footway
defect.

The 58 audit findings are explicitly retained: 24 genuine inherited footer-link
omissions, 9 inherited transition-markup contracts requiring a separate portfolio
review, 3 genuine eager-iframe performance issues, 20 obsolete pre-living-atlas
hero/analyst/overlay delivery contracts, and 2 inherited manual-fallback contracts
requiring research-page review. They are not silently waived or reported green.

## Native gameplay and interface checks

[Gameplay record](district-review/gameplay-evidence.json),
[Work integration](district-review/work-integration.json),
[phone record](district-review/mobile-checks.json).

- Held W moves the actual physics root; a 2.5 s hold moved about 5.24 m. The
  [walking capture](district-review/after-walking-live.jpg) records `Walk`, not a
  staged pose. The rolling moving-only sample contains 600 actual moving frames.
- From business focus `(21,11)`, held forward stops at `(21,9.098)` on the 0.26 m
  porch, grounded and Idle. Space launches one jump; the recorded airborne height
  is 1.107 m. The follow camera remains outside the building.
- E opens the existing CBD study, including real case-study/map links.
  Close study returns to play. Read the atlas returns to editorial; Take control
  resumes the same `(21,9.098)` position, CBD selection, scene UUID and renderer.
  Back/Forward restores editorial/adventure with CBD still selected.
- Work opens the same assembled district with MBR selection and one renderer.
  Controls/pause opens help and freezes movement; closing resumes. Quality Eco
  disables shadows and uses pixel ratio one. No world rebuild is triggered.
- At 390×844 and 320×720 there is no horizontal overflow; direction, jump, pause,
  quality and menu targets are at least 44 px high. Holding the right direction
  for one second moved x=0 to x=1.547. Menu opens/closes, pauses the world and
  exposes real navigation. Both theme states were inspected and the original
  setting restored. Phone sizes are emulated desktop viewports.
- Reduce camera and environmental motion changes the source-exposed setting to
  `true`; the original setting was restored. Escape closes the guide and returns
  focus to the playable canvas. [Motion check](district-review/motion-check.json).

## Measured rendering performance

These measurements come from the **integrated playable district**, never the
isolated showcase. Actual requestAnimationFrame intervals exclude the first 60
frames and use up to 600 samples. The walking subset requires measured player
displacement. CPU submission time is not GPU duration. Refresh rate caps these
results; they do not establish performance on another computer or a phone.
Raw values, browser agent, buffer size and quality: [performance record](district-review/performance.json).

| Recorded condition | Canvas / shadows | Mean frame / p95 | Observed rate |
| --- | --- | --- | --- |
| Actual walking, 600 moving frames | 1280×723, on, pixel ratio 1 | 8.337 / 8.40 ms | 119.95 fps |
| Work neighborhood, Standard, 600 frames | 1280×656, on, pixel ratio 1 | 8.336 / 9.20 ms | 119.96 fps |
| Work neighborhood, Eco, 600 frames | 1280×656, off, pixel ratio 1 | 8.335 / 9.30 ms | 119.98 fps |
| 390 px viewport, Eco, 600 frames | 390×784, off, pixel ratio 1 | 8.336 / 8.40 ms | 119.96 fps |

The walking snapshot reports 263 draw calls, 683,722 submitted triangles and
1.63 ms mean CPU submission. Those counters include the current camera/culling,
context and existing animated guides, not just the asset assembly. Other views
vary. The production preview also records the natural narrow viewport separately;
its compact default disables shadows and uses pixel ratio 1.15.

No new package, external model request, postprocessing pass, light or additional
renderer is introduced. Four GLB downloads remain 6,659,124 bytes. District
instances share source geometry and materials through three prototypes; repeated
architecture and props are instanced. Trees retain independent graphs to cut
near-camera canopy with hysteresis. Original signs and three painted display
textures increase generated texture storage; the exact dimensions are in source
and the loaded record. Generated resources have explicit cleanup. This phase
does not claim a universal memory budget or GPU benchmark.

## Eight fixed before/after comparisons

All sixteen JPEGs are **1280×720** with a **1280×656 canvas**, FOV **50°**.
Each pair has identical camera position, quaternion, field of view and aspect;
maximum numeric camera difference is **0**. Approved component scale is retained.
Lighting intentionally changes from the old district to Phase 2 daylight. All
nine after review views use one persistent scene and cached assets. Captures are
unaltered native browser screenshots including the real interface. They are not
renders from a separate gallery. [Camera tuples](district-review/after-cameras.json),
[comparison verification](district-review/comparison-verification.json).

| View | Before | After | Live fixed camera |
| --- | --- | --- | --- |
| 1. Arrival plaza | [original](district-review/before-spawn.jpg) | [district](district-review/after-spawn.jpg) | [open](http://127.0.0.1:4173/index.html?experience=adventure&district-review=spawn&build=46) |
| 2. Commercial avenue | [original](district-review/before-avenue.jpg) | [district](district-review/after-avenue.jpg) | [open](http://127.0.0.1:4173/index.html?experience=adventure&district-review=avenue&build=46) |
| 3. MRT approach | [original](district-review/before-station.jpg) | [district](district-review/after-station.jpg) | [open](http://127.0.0.1:4173/index.html?experience=adventure&district-review=station&build=46) |
| 4. Business district | [original](district-review/before-commercial.jpg) | [district](district-review/after-commercial.jpg) | [open](http://127.0.0.1:4173/index.html?experience=adventure&district-review=commercial&build=46) |
| 5. Neighborhood street | [original](district-review/before-neighborhood.jpg) | [district](district-review/after-neighborhood.jpg) | [open](http://127.0.0.1:4173/index.html?experience=adventure&district-review=neighborhood&build=46) |
| 6. Transit pocket park | [original](district-review/before-park.jpg) | [district](district-review/after-park.jpg) | [open](http://127.0.0.1:4173/index.html?experience=adventure&district-review=park&build=46) |
| 7. Third-person promenade | [original](district-review/before-walking.jpg) | [district](district-review/after-walking.jpg) | [open](http://127.0.0.1:4173/index.html?experience=adventure&district-review=walking&build=46) |
| 8. Aerial overview | [original](district-review/before-aerial.jpg) | [district](district-review/after-aerial.jpg) | [open](http://127.0.0.1:4173/index.html?experience=adventure&district-review=aerial&build=46) |

Additional evidence: [green park](district-review/after-garden.jpg),
[actual walking](district-review/after-walking-live.jpg),
[study dialog](district-review/research-study.jpg),
[editorial return](district-review/editorial-return.jpg),
[390 px phone](district-review/mobile-adventure.jpg),
[320 px phone](district-review/mobile-320.jpg).
Gameplay/interaction extras use the natural browser viewport and are not claimed
to match the calibrated comparison resolution.

### Visual inspection notes, without a human score

The captured avenue shows recessed shopfronts, readable primary names, distinct
display contents and clear canopy walks. Neighborhood scale, timber framing,
clay roofs and sage plaster differ from the taller commercial and office blocks.
The station roof and Menara Teras remain orientation anchors; palms and broadleaf
trees add layers rather than occupying carriageways. The aerial shows connected
blocks and parks instead of separate showcase plinths. Screenshots also expose
the remaining simplifications: repeated background variants, intentionally shallow
window displays, a bounded conceptual terrain horizon, and strong tree shadows.
Fine sign subtitles are for close range; principal names carry wayfinding.

These are agent inspection observations, not human approval. Please assess
architectural coherence, environmental detail, walkability, landmark visibility,
character scale, painterly atmosphere and variety. Human approval and score
remain unset until the owner reviews the evidence.

## Antislop delivery checks, scoped to this phase

These technical/interface checks do not award the required human art score or
claim that the inherited static-site audit passes.

| Gate | Status and concrete evidence |
| --- | --- |
| Hard Gate | **PASS for changed district/interface scope.** Native movement, jump, study open/close, mode return, history, pause, quality, phone direction and menu were exercised above. Failure/loading states are real; a deliberately failed asset left research accessible. 390/320 layouts have no horizontal overflow and 44 px targets. New signs/displays are explicitly fictional authored game scenery. No fabricated score, FPS, testimonial, external link or photorealistic asset. Semantic controls, existing focus/reduced-motion paths and navigation are preserved. No scripted source patching or dependency added. |
| Purpose Gate | **PASS.** Sky gradient communicates daylight/atmospheric depth; scene shadows ground physical geometry. Existing paper/forest/bronze surfaces frame controls. The circular map communicates player orientation and landmark location. No generic icon decoration, card glow, promotional badge or gratuitous animation was added. |
| Liveliness | **PASS.** Design Read and ENERGY 2 / RHYTHM 2 / MOTION 1 are recorded in the design spec. Plaza, station and office establish focal points; covered streets and quiet green pockets provide rhythm. One bronze interface accent and consistent physical sign system maintain identity. Motion supports walking, orientation and restrained foliage; pause is available. |
| Craftsmanship / Quality Locks | **PASS for implemented scope.** One shared ground plan drives visible supports; all major buildings use approved imported architecture; factory proxy transforms and final pedestrian routes are tested. Fixed cameras match exactly, licensed source digests remain intact, zero missing textures and no production browser errors were recorded. Native screenshots were visually inspected. Human aesthetic acceptance remains pending. |

## Provenance and scope boundary

[Current integration record](../assets/game/scenery/district-integration.json),
[architecture source](../assets/game/scenery/architecture-source.json),
[vegetation/planter source](../assets/game/scenery/source.json),
[archive verification](../assets/game/scenery/verification.json),
[original enhancement snapshot](../assets/game/scenery/architecture-enhancements.json).

All four scenery GLBs and both Quaternius CC0 license records are unchanged.
Approved architecture factory SHA-256 remains
`17d18deb5e304380493ba962bbf80e61e0ae2bc5073ec2223161ceb285ef7b72`.
The older Phase 1.5 manifest's unassigned score is preserved as a historical
snapshot; current component-integration authorization is recorded separately.
No new third-party asset or protected game artwork was introduced.

The existing optional story implementation, saves and regression tests remain
in the repository, but this district runtime is exploration-only. Its encounter,
service-yard story meshes and extra quest guide are not activated. No Bandung,
West Java realm, travel system, monster, equipment shop or new quest is added.
No commit, push or deployment was performed. The local preview remains running.
