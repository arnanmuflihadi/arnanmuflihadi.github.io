# R0: The Floating Urban Atlas

Historical pre-correction delivery. The active world is now the
[R0-A landscape correction](LANDSCAPE-R0A.md); these original measurements and
screenshots remain as the rejected-build comparison record.

**Transit Kingdom is implemented for owner visual review.** No human score or
approval has been assigned. Target: average 4/5, no scored category below 3/5.
The other five realms and dragon travel are not implemented.

[Play the island](http://127.0.0.1:4173/index.html?experience=adventure&build=57) ·
[Visual review gallery](floating-review/index.html) ·
[MBR research deep link](http://127.0.0.1:4173/index.html?experience=adventure&project=mbr&build=57) ·
[Asset/source record](../assets/game/scenery/floating-atlas-r0.json)

## Audit and preservation

The old district's engineering worked, but its flat 88 m footprint, repeated
commercial/office masses, road grid and rectangular boundary produced an
architectural collection rather than an adventure landscape. Its 67 passing tests
were a regression baseline, not evidence of artistic approval.

The previous environment remains in the documented [legacy modules](LEGACY-JAKARTA-DISTRICT.md),
with its source manifests, original GLBs, licenses, tests and eight comparison
pairs. The new Home/Work loader does not invoke the legacy district assembly.
Shared character, animation, input, geometry, camera, model-cache and dialogue
helpers are reused. Player/camera changes add optional world dependencies and
preserve old defaults. All original tests remain.

Work is on `codex/floating-atlas-r0`. Existing uncommitted work was retained.
No reset, blanket commit, push or deployment was performed.

## Island and level design

The upper landmass is **131 × 142.6 m**, with bare walking terrain from about
**7.42 to 28 m** above the fictional datum and rock tapering to approximately
**−57 m**. It has an asymmetric authored outline, terraced settlement, exposed
cliffs, closed modeled underside, basalt spurs, a stream and falling water ribbon.
There is no rectangular ground slab or reused road grid.

| Area | Anchor (x,z) | Design |
| --- | --- | --- |
| Pelabuhan Awan | 12,47 | Railed arrival terrace, original arch/leaf-roof gateway, physical signage and marked future landing zone. Opens toward settlement and highlands. |
| Stasiun Antara | −8,−10 | Original split leaf canopies, arches and continuous roof supports; imported glazing; graded rear platform; slotted transit beacon. The only constructed research destination. |
| Pasar Angin | 24,18 | Bent cluster of one enhanced commercial and two neighborhood buildings, an original open market, occupied windows, shaded frontages and seating. No commerce mechanic. |
| Bukit Lestari | −32,−32 | Graded winding path, rock outcrops and the original stepped-roof Balai Angin pavilion. |
| Teras Langit | −49,−2 | Cantilevered stone overlook, visible balustrades, city/skyport views, river edge and open sky. Two walking approaches. |

The main paths form a loop rather than a building grid. Three short branches reach
merchant frontages. Route grading is deliberate, not random terrain noise.
Actual controller simulations at 60 steps/second reach each route endpoint with
final imported collisions and no jump required:

| Route | Controller traversal time |
| --- | --- |
| Arrival to merchant plaza | 15.18 s |
| Merchant plaza to station | 24.27 s |
| Station to highlands | 25.28 s |
| Highlands to overlook | 21.40 s |
| Overlook return to junction | 14.70 s |

Arrival-to-station is about 39.45 simulated walking seconds; arrival-to-overlook
about 86.13 seconds, excluding stops. These are measured controller simulations,
not browser wall-clock journey benchmarks. Speeds remain 2.1 m/s walking and
4.6 m/s running. [All eight route results](floating-review/traversal-and-cleanup.json).

## Terrain and materials

The surface uses 156 boundary sectors and 44 radial rings, totaling **13,572 top
triangles**. Hand-placed outline controls, area terraces, foundation pads and
graded path anchors determine elevation. The support lookup interpolates the
same triangles that are rendered. A closed, offset, tapered rock mesh joins the
surface exactly and varies strata, color and geological depth.

Vertex color blends distinguish meadow, path stone, urban paving and exposed
slopes. Concrete/stone, stained timber, clay, copper-green roof surfaces and soft
sky glazing follow one restrained palette. No photographic noise, expensive
postprocessing or protected game artwork is used. Warm directional light,
hemisphere fill, 2048 px soft shadows, a sky gradient and layered soft-edged clouds
provide depth. Cloud/foliage/water motion respects pause and reduced motion.

Thirty-two imported trees, nine original palms, 76 ground ferns and 14 cliff ferns
follow groves, stream margins, slopes and path edges. Ferns use three instanced
batches; grass is batched. Tree canopies can cut away near the camera with
hysteresis. Three distant uninhabited silhouettes are background scenery, not
constructed future realms.

Public decks have explicit support matching their chamfered rendered outlines,
including the overlook beyond the terrain edge. Rails are physical collision
objects. Wild unguarded edges allow gravity falls and recovery to a valid recent
position; no invisible wall is placed immediately at the coastline. Tall terrain
steps and solid outcrops block walking. Rotated buildings use oriented walking
proxies, while camera clearance conservatively tests architecture and terrain.

## Reused assets and new geometry

No new third-party download was introduced. Existing CC0 Quaternius sources and
archives remain unchanged:

| Delivery file | Use | Existing provenance/license |
| --- | --- | --- |
| `architecture-library.glb` | `Building_Small_1` source-derived commercial/neighborhood variants and eleven station glazing modules | `architecture-source.json`, Downtown City MegaKit CC0 notice |
| `canopy-tree.glb` | Broadleaf groves, height/orientation/finish variation | `source.json`, Stylized Nature MegaKit CC0 notice |
| `fern.glb` | Ground, terrace and cliff vegetation | Same nature provenance and notice |
| `urban-explorer.glb` | Preserved skinned player and locomotion | `characters/urban-explorer/source.json`, `CC0-Quaternius.txt` |
| `jump-animations.glb` | Preserved authored jump animation | `jump-source.json`, `jump-LICENSE.txt` |
| `city-resident.glb` | Existing fictional guide Nadia | `phase3/source.json`, `CC0-Characters.txt` |

The approved architecture generator remains SHA-256
`17d18deb5e304380493ba962bbf80e61e0ae2bc5073ec2223161ceb285ef7b72`.
Its office variant is preserved but not placed on this island. Only two approved
prototypes are instantiated: one commercial and two neighborhood buildings.
The gateway, station canopies/arches/beacon, market timberwork, pavilion roofs,
overlook, terrain, sky, palms, furnishings and lettering are project-authored.
Primitive geometry supplies small details and supports; it is not the complete
visual foundation of the major buildings.

Actual browser environment snapshot: **393,127 triangles**, 369 mesh objects,
167 unique geometries, 98 materials and **35 textures with zero missing**.
This snapshot is taken before adding the player and guide. The live renderer's
view-dependent submission counters include them. Three scenery files are loaded
through three cached requests; two architecture prototypes are cached.
The six scenery/character/animation GLBs total **9,239,476 bytes**; scenery alone
is **6,204,348 bytes**. [Filenames, sizes and hashes](floating-review/inventory.json),
[actual browser counts](floating-review/browser-assets.json).

The static fallback now shows this island too. It is a **39,298-byte, 1265×648 WebP**
exported directly from the live WebGL canvas, not concept art or a fake QA
screenshot. The ten review images are separate unretouched browser screenshots.

## Module structure

| Module | Responsibility |
| --- | --- |
| `floating-atlas/plan.js` | Area/path/building coordinates, review cameras, six realm specifications and disabled future travel routes |
| `terrain.js` | Authored top/cliff geometry and exact triangle support lookup |
| `support.js`, `collision.js` | Constructed decks, safe positions, oriented solids and terrain-aware camera clearance |
| `scene.js`, `settlement.js` | Environment, original architecture, licensed mesh placement, materials and cleanup |
| `world-manager.js` | Deduplicated world load, cancellation, unload and disposal; rejects unbuilt realms |
| `entry.js` | Adapter to the existing renderer/mode/controller contract; character, input, telemetry and lifecycle |
| `guide.js` | Existing rig, Nadia and existing research dialogue |
| `presentation.js`, `minimap.js` | Actual island cinematic compositions and island/path map |

The professional pages, case-study files, GIS visualizations and shared research
registry are retained. No complete future realm is loaded.

## Verification

**73/73 tests pass, zero skipped**, including all original 67 and all 16 scoped
asset/architecture/character regressions. [Final log](floating-review/test-results.txt),
[baseline](floating-review/baseline-tests.txt).

New tests verify closed terrain/rock seams, more than 1,500 exact render/support
samples (error below 0.00001 m), real imported geometry/cache counts, visible sign
faces in front of their backings, every graded route with final collisions,
cantilever deck support, jumping/landing, an actual simulated walk off a cliff
followed by gravity recovery, invalid-position recovery, camera clearance at five
areas/eight yaw angles, and world load/cancellation/disposal.

Native browser checks exercised:

- Held W moved the player from z=47 to z=36.479 in five seconds. Captures record
  actual `Walk` and `Run` poses. Space launched an airborne jump; a subsequent
  moving jump landed grounded with a recorded landing count.
- Nadia's greeting, research and limitations dialogue work. Show me the project
  opens the real transit study. Scenario B changes the displayed score to 37.55;
  scenario A restores 29.67. Case-study/dashboard links remain available.
- Read the atlas and Take control preserve the same scene UUID, one renderer,
  transit selection and player position (within 1 mm of the sampled moving-to-idle
  handoff). Back/Forward preserve the same world and project. The opt-in review
  camera no longer reapplies a teleport on mode handoff.
- The exact MBR adventure deep link selects MBR, opens its real study, states that
  the realm is unbuilt and offers **no false walking destination**. The player
  remains on Transit Kingdom. A fresh Work adventure load does the same.
- At 390×844 and 320×720 there is no horizontal overflow; visible movement,
  jump, pause, quality and menu targets are at least 44 px high. A one-second held
  right button moved x=12 to x=14.105. Menu opening pauses the world. Reduced
  motion, Escape return, both themes and Eco quality were exercised and restored.

[Gameplay/state record](floating-review/gameplay.json),
[future-realm/Work record](floating-review/unbuilt-research-and-work.json),
[fresh clean Work check](floating-review/fresh-work-check.json),
[phone checks](floating-review/mobile-checks.json).

One local preview navigation initially failed to fetch the entry module. The
research fallback stayed readable; reload recovered it, the local module returned
HTTP 200 with the correct JavaScript MIME type, and a fresh Work load has zero
warnings/errors. That historical event is retained in the Work record, not
silently removed. Final Home/Work checks show required assets loaded correctly.
The final fresh Home load also records one WebGL renderer, ready scenery/player/
guide, no missing textures and zero warnings/errors in
[the final browser check](floating-review/final-browser-check.json). The second
canvas is the 2D minimap. The static gallery was scrolled through and all twelve
image elements (ten required views plus the two comparison images) decoded
successfully without overflow or browser warnings/errors:
[gallery check](floating-review/gallery-check.json).

The static audit still exits with **58 inherited findings**, exactly matching the
Phase 2 baseline. None were removed or suppressed. The existing individual
classification remains linked from [the comparison](floating-review/audit-comparison.json).
These include inherited footer omissions, transition contracts, eager embeds,
obsolete hero-delivery contracts and manual-fallback contracts. This is not a
claim that the whole site's old static audit passes.

## Actual performance and cleanup

Measured in the integrated island on this Mac, Chromium 156, with a 1280×656
canvas and pixel ratio one:

| Condition | Mean frame | p95 | Measured rate | Submission |
| --- | --- | --- | --- | --- |
| Actual walking, Standard/shadows on, 600 moving frames | 6.112 ms | 11.10 ms | 163.62 fps | 322 calls / 319,739 triangles |
| Stationary Eco/shadows off, 600 frames | 5.556 ms | 6.30 ms | 180.00 fps | 301 calls / 309,252 triangles |

The walking sample reports 1.38 ms mean CPU submission, 190 renderer geometries,
47 renderer textures and 33 compiled programs. These are object counters, not
GPU memory bytes. First 60 frames are excluded; moving samples require actual
displacement. CPU submission is not GPU time. Frame rate is hardware/refresh/camera
dependent and is not extrapolated from the old architecture showcase.

The recorded warm-cache load took 287.1 ms for world assembly, 929.0 ms to the
first world frame and 1011.8 ms to explorer readiness. The character/guide stage
took 716.4 ms. All six GLB resource entries reported zero network transfer due
to cache, while encoded body sizes match the 9.24 MB inventory. **Cold network
loading and physical mobile hardware have not been benchmarked.**

[Moving-frame raw evidence](floating-review/walking-performance.json),
[Eco sample](floating-review/eco-performance.json),
[load/transfer evidence](floating-review/browser-assets.json).

The real-geometry Node fixture observed disposal of all 167 geometries, 98
materials and 20 fixture textures, with zero remaining scene children and an
empty model cache. Fixture image decoding is omitted in Node; browser texture
counts are reported separately. Cancellation generations are tested. Scene,
renderer, input, observers, generated resources and animation ownership have
explicit cleanup. Mode switching intentionally retains one world and renderer.
This is not a GPU-driver memory-release benchmark.

## Visual evidence and remaining limits

The [gallery](floating-review/index.html) contains all ten required native views:
aerial, underside, skyport, station, merchant quarter, pedestrian path, overlook,
third-person exploration, editorial and adventure. Nine captures are 1280×720;
the native editorial capture is 1265×712. The eight fixed camera tuples are in
[cameras.json](floating-review/cameras.json); the paired mode captures' shared
scene/selection evidence is in [gameplay.json](floating-review/gameplay.json).
R0-B's aerial/underside/walking captures were saved before settlement construction.

The old and new full-area aerial views use documented different camera tuples,
because the island is larger and elevated. They are not claimed to be identical
camera comparisons. [Comparison settings](floating-review/comparison.json).
No screenshot has been retouched or replaced by concept art.

Owner review is still needed for the landform silhouette, broad rock facets,
dark canopy undersides, foliage density, skyline, shallow shop displays, path
compositions and character-scale experience. Simplified background islands are
not destinations. There are no operating trains, complete interiors, new quests,
monsters, equipment commerce, inventory expansion or flight. The architecture
showcase remains available for component regression review.

## Antislop checks for this delivery

| Block | Status and evidence |
| --- | --- |
| Hard Gate | **PASS for changed interface scope.** Real movement, jump, dialogue, study controls, mode/history, pause, quality and phone menu were clicked. Phone targets are 44 px and layouts do not overflow. Fictional-world labels are explicit; performance is measured and no human score is fabricated. Research remains readable in failure states. |
| Purpose Gate | **PASS.** Sky gradients convey atmosphere, world shadows ground geometry, the map communicates terrain/routes, and paper/forest surfaces preserve portfolio identity. No promotional badges, generic icon decoration, glow or template animation was added. |
| Liveliness | **PASS.** Design Read and ENERGY 2 / RHYTHM 3 / MOTION 1 are recorded in the design spec. Terrain terraces, two landmark silhouettes and quiet natural pockets provide hierarchy. Movement and environmental animation have a purpose and can be paused/reduced. |
| Craftsmanship / Quality Locks | **PASS for implemented technical/interface scope.** Preserved source hashes, exact terrain support, final-collision traversal, disposal checks, real screenshots, one-scene handoff and clean fresh Work load provide evidence. The owner's aesthetic approval is still pending. |

## Recommendation after visual approval

Start a separate flight prototype only after this island is accepted. Validate a
legally reusable rigged dragon, its footprint and animations against the marked
4.3 m landing zone before committing to takeoff. Exercise Explore → Mount →
Takeoff → Fly → Load Destination → Land → Explore using the existing disabled
travel configuration and world-manager cancellation/unload contract. Establish
flight-camera and streaming budgets before constructing another full realm.
No dragon or flight placeholder is included in R0.
