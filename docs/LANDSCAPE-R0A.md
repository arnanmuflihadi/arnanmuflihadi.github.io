# R0-A: landscape correction

Historical pre-polish record. Current screenshots and checks are in
[R0-A2 environmental polish](ENVIRONMENT-POLISH-R0A2.md).

Scope follows the owner's 2 November 2026 brief. Build from the current local
tree, preserve gameplay/research, retire every existing building from the active
island. Stop before fantasy architecture. Human visual approval is pending.

## Implementation decisions

- Keep Three.js, existing loader/cache, character, physics, camera, registry,
  research panels and one persistent renderer. No dependency migration.
- Snapshot the rejected floating assembly in `assets/js/floating-atlas-legacy-r0/`.
  Keep its regression tests against that isolated snapshot. Add active-landscape
  tests; never claim the old settlement assertions verify the new environment.
- Shape a roughly 175 m asymmetric landmass: eastern low meadow, central valley,
  a rising western switchback ridge and a natural western rock overlook. Blend
  authored ridges, depressions and clearings, with modest deterministic erosion.
- Keep exact render-triangle support. Remove constructed decks, pads, buildings,
  transit/skyport meshes, plazas and physical project landmarks. Preserve one
  existing research guide on a trail; no new NPC/content/mechanics.
- Reserve five coordinates in the plan for later architecture and travel.
  Clearings only. Every project remains readable, with no landmark teleport.
- Chisel the underside into varied shelves and buttresses, add tropical groves,
  grouped understory, wind-responsive batched grass and a waterfall. Layer cloud
  banks and distant silhouettes with coordinated sky/fog. No postprocessing.
- Design read: painterly tropical exploration for portfolio visitors, ENERGY 2 /
  RHYTHM 3 / MOTION 2. Terrain is the focal point; parchment/forest UI stays.
  Gradients express atmosphere, amber indicates trails/sunlight, motion indicates
  wind and water and follows pause/reduced-motion controls.

## Short execution plan

1. Inspect five references selectively and record separate code/asset rights.
2. Save baseline tests and comparable native browser capture; isolate old world.
3. Shape terrain/trails/geology, batch natural dressing and atmosphere.
4. Reconnect the existing controller, research and cinematic cameras honestly.
5. Run regression/active-terrain tests, walk/run/jump in the browser, inspect
   camera/support/mode/history/MBR, capture eight views and actual frame counters.
6. Publish evidence and remaining limits here, then stop for owner review.

## Delivered landscape and source changes

[Play](http://127.0.0.1:4173/index.html?experience=adventure&build=63) ·
[Actual browser screenshots](landscape-review/index.html) ·
[Reference mapping and licenses](landscape-review/references.md).

The current working tree on `codex/floating-atlas-r0` was used, with all earlier
work retained. No commit, push or deployment was performed. The rejected R0
assembly is isolated under `assets/js/floating-atlas-legacy-r0/`; source hashes
are recorded in `landscape-review/legacy-hashes.json`. The original six R0 tests
now explicitly target that snapshot. The original 67 other tests are retained.
The old Jakarta and architecture showcase sources/licenses also remain.

Changed sources: `floating-atlas/plan.js`, `terrain.js`, `scene.js`, `support.js`,
`collision.js`, `presentation.js`, `minimap.js`, `entry.js`, `world-manager.js`
and `guide.js` (the last two only change versioned imports). Added `nature.js`
and `atmosphere.js`. The settlement assembler is absent from the active module
folder and retained in the legacy copy. Home/Work, experience/living controllers
and project-panel text now describe a landscape with unbuilt physical landmarks.
The existing registry, rig, animation, input and core camera/controller remain.
Added `tests/landscape-r0a.test.mjs`, fallback image, manifest and review evidence.

The 177.62×183 m outline has an eastern meadow, central valley, western ridge
and switchback/loop trails. Bare terrain ranges from 10.28 to 49 m. A continuous
208-sector, 64-ring top mesh contains 26,416 triangles; support interpolates
these exact triangles. Eleven irregular geological rings, shelves and attached
buttresses taper below it to about −85 m. The underside is closed. No rectangular
city pads, constructed decks or invisible immediate coastline wall remain.

Reserved coordinates (conceptual metres, x/y/z; exact support also in inventory):

| Future use | Coordinate | Current treatment |
| --- | --- | --- |
| Arrival skyport | 27 / 16 / 57 | Natural meadow clearing |
| Transit station | −5 / 21 / 5 | Valley clearing |
| Fantasy settlement | 32 / 22 / 12 | Eastern clearing |
| Scenic overlook | −80 / 32 / 5 | Natural western rim and walking loop |
| Dragon landing/takeoff | 27 / 16 / 57, radius 6.5 m | Clearing only, disabled travel configuration |

The two scenery GLBs remain Quaternius CC0. Actual browser counts are 145 trees,
710 ground ferns, 42 cliff ferns in twelve instanced batches, ten authored palms
and 27,444 grass blades. Vegetation follows groves/stream margins and avoids
trails/clearings. New grass uses real tapered blade geometry with a wind uniform;
cloud banks use forty batched camera-facing shapes. All motion respects pause
and reduced-motion controls. No reference implementation or artwork is copied.

## Verification and measurements

**77/77 tests pass, none skipped**: the preserved 73 plus four active-landscape
tests. [Final test log](landscape-review/test-results.txt),
[baseline](landscape-review/baseline-tests.txt). Active tests confirm zero city
objects/BoxGeometry meshes, only two scenery files, no missing textures, a
watertight underside, more than 1,800 render/support samples with error below
0.00002 m, final-collider walking routes, jumps/landings/fall recovery, camera
clearance at all five areas and complete observed resource disposal.

Controller traversal simulations at 60 steps/s: arrival trail 30.08 s, ridge
43.08 s, overlook 31.77 s, return 40.38 s; clearing/meadow branches 18.87/21.37 s.
The main loop is about 305 m and 145 simulated walking seconds without stops.
All routes finish grounded without jumping. These are controller simulations,
not browser wall-clock journey times. [Terrain, routes and cleanup](landscape-review/terrain-and-cleanup.json).

Native browser W for five seconds moved z=57 to 46.505; five seconds S returned
to 56.991. Shift+W for two seconds verifies running displacement. A real jump
was captured airborne, then landed on the ridge with jump/landing counters 1/1.
The Home editorial/adventure pair retains scene UUID and player position. MBR's
exact adventure deep link opens the real study and explicitly states the realm
is unbuilt, with zero false walking links. All six studies remain on Work.
Work's MBR editorial/adventure pair also preserves project, position and scene.
Back/Forward retains the selected project and scene; a stale study flag exposed
by this check was fixed by synchronizing the restored panel state back to the
current URL. [Final history check](landscape-review/history-final.json),
[research and Work evidence](landscape-review/research-and-work.json).

At 390×844 and 320×720 there is no horizontal overflow and visible controls are
at least 44 px high. Holding the right touch button for one second moved x=27
to 29.109. Mobile menu opening pauses the world; reduced motion, Escape return,
both themes and Eco/Standard were exercised and restored. Eco disables shadows.
These are browser viewport checks on this Mac, not physical mobile tests.
[Mobile record](landscape-review/mobile.json),
[controls and quality](landscape-review/mobile-controls.json).

Final browser environment before actors: 40 meshes, 1,276,069 potential triangles,
23 geometries, 36 materials, four textures, zero missing. Five active GLBs total
3,859,228 bytes, including 824,100 bytes scenery. The architecture GLB is absent
from browser resource requests. All six original GLB hashes remain unchanged.
[Inventory](landscape-review/inventory.json), [actual loaded assets](landscape-review/browser-assets.json).

Actual walking, this Mac/Chromium 156, 1280×656 canvas, DPR 1, Standard/shadows on:
600 moving frames, **5.555 ms mean / 5.80 ms p95 / 180.01 FPS**. The recorded
view submits **58 calls / 1,291,255 triangles**, with 48 renderer geometries,
16 textures and 20 programs. Mean CPU submission is 0.553 ms, not GPU timing.
The 1.28 million potential environment triangles are higher than R0's 0.39 million;
batching substantially reduces object/draw counts. No cross-device speed claim
is made. [Raw moving-frame evidence](landscape-review/walking-performance.json).

Warm-cache world assembly measured 97 ms, first frame 198.5 ms and explorer
readiness 243.9 ms. The actor stage measured 141.4 ms. All five GLBs reported zero
network transfer from cache; encoded body sizes match inventory. Cold-network
loading, GPU memory bytes and physical phones are unbenchmarked. Node cleanup
observed all 23 scene geometries and 36 materials disposed, an empty scene and
zero cache entries. Node fixtures omit image decoding; four live browser
textures are counted separately. This is not a GPU-driver release benchmark.

The static audit still fails with **58 inherited findings, none added/resolved**.
[Exact comparison](landscape-review/audit-comparison.json). They were neither
suppressed nor represented as passing.

## Visual evidence and remaining issues

The gallery contains the requested aerial, profile/underside, low cliff,
third-person spawn, elevated trail, overlook, airborne/landed and editorial
views, plus resumed adventure. All ten primary captures use the same final
scene UUID. Fixed camera tuples are in `cameras.json`; jump and mode state are
in `jump.json` and `integration.json`. Native adventure captures are 1280×720;
editorial uses the browser's native 1265×712 layout.

The before and comparison aerials use the identical [110,82,135] camera,
[0,−3,0] target, 43° FOV and 1280×720 viewport. Lighting and world dimensions
change as part of the correction. The separate full-island aerial is framed
wider so the larger silhouette is fully visible. Screenshots are unretouched.
The 47,340-byte static poster is a separate actual-canvas export.

Owner review is required for the overall landscape, repeated source tree crowns,
simplified grass tufts, broad rock bands, smooth slope patches, cloud shapes,
waterfall ribbon and distant silhouettes. This remains a stylized procedural
landscape. Distant islands are low-detail scenery. The natural overlook has no
guardrails; cliff falls use recovery. No new buildings, complete realms, dragon,
flight, NPC expansion, quests, monsters or inventory were implemented.

## Antislop delivery checks

- Hard Gate: PASS for changed scope, backed by actual movement/jump/study/mode
  checks, exact inventory, accessible existing controls and native screenshots;
  no invented performance or human rating.
- Purpose Gate: PASS. Sky gradients/fog indicate distance and altitude; trails,
  groves and warm sunlight establish navigation and hierarchy. Existing research
  typography/UI are preserved, with no new decorative interface system.
- Liveliness: PASS. ENERGY 2 / RHYTHM 3 / MOTION 2; ridge, valley, meadow and
  cliff compositions vary, and wind/water/cloud motion has pause/reduction.
- Craftsmanship: PASS for technical/interface scope. Preserved source hashes,
  exact support, reachable routes, actual browser evidence and passing tests
  back the implementation. Human aesthetic approval remains pending.

Stop here for human visual review. R0-B architecture has not started.
