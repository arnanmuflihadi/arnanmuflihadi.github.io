# R0-B1 — Tropical Sky Metropolis

Four original architectural prototypes render in a reversible layer on the exact R0-A3 island. **Human artistic approval remains pending.** No visual score has been assigned and R0-B2 has not started.

[Live inspection](../architecture-r0b1.html?build=R0-B1.6#ensemble) · [19 fixed-camera views and nine comparisons](architecture-r0b1-review/index.html) · [Full measured evidence](architecture-r0b1-review/technical-evidence.json) · [Asset manifest](../ASSET_MANIFEST.md)

## Delivered geometry

| Prototype / GLB root | Width × depth × height | Triangles | Draw batches / materials | Imported placements |
|---|---:|---:|---:|---:|
| Ruang Niaga / `RuangNiaga` | 14.85 × 10.75 × 10.87 m | 18,236 | 17 / 15 | 24 |
| Atlas Research Centre / `AtlasResearchCentre` | 13.45 × 12.47 × 18.20 m | 20,240 | 16 / 13 | 27 |
| Stasiun Antara / `StasiunAntara` | 24.97 × 16.53 × 10.40 m | 23,980 | 14 / 13 | 6 |
| Pelabuhan Awan / `PelabuhanAwan` | 22.50 × 21.94 × 8.86 m | 15,420 | 17 / 14 | 10 |

The four roots contain **77,876 triangles / 64 draw batches**. Adaptive foundations and entrance steps bring the review layer to **78,632 potential triangles, 97 meshes/geometries, 25 shared materials and 13 textures**, with none missing. The hidden raw-source inspector adds nine model types, 11 mesh objects, 804 triangles, three materials and two source textures. The existing explorer remains 1.9 m tall; pedestrian presets use a 1.65 m eye height above the relevant entrance/platform datum.

Ruang Niaga has a shaded shop arcade, modeled displays, opening door leaves, imported square windows, continuous facade infill, a planted setback terrace and roof pergola. Atlas uses a stepped sage/mineral envelope, recessed glazing, bronze shading, public reception and an observation sail. Antara has a new split butterfly roof, branching supports, static rail bed, connected switchback stairs, lift core and guarded upper exit. Awan has an original swept roof, boarding lounge, protected circular apron, navigation mast and observation stair. Major visual massing uses imported components and original modeled panels, openings, beveled plates and closed roof shells. Primitive boxes are limited to small site steps and inspection/collision work.

## Sources and rights

| Candidate | Verified result and decision |
|---|---|
| [Kenney Modular Buildings](https://kenney-assets.itch.io/modular-buildings) | Official free archive downloaded and inspected. Bundled version **2.1**, **108 actual GLBs**, CC0-1.0; attribution optional. Selected clean window and door parts. |
| [Kenney Building Kit](https://kenney-assets.itch.io/building-kit) | Official free archive downloaded and inspected. Bundled version **1.0**, **79 actual GLBs**, CC0-1.0; attribution optional. Selected square window walls, portal and column parts. |
| [Kenney City Kit Commercial](https://kenney.nl/assets/city-kit-commercial) | Official page evaluated. Direct `kenney_city-kit-commercial_2.1.zip` download returned HTTP 403. No files imported or counted. |
| [Kenney City Kit Roads](https://kenney.nl/assets/city-kit-roads) | Official page evaluated. Direct `kenney_city-kit-roads.zip` download returned HTTP 403. No files imported or counted. |
| [Poly Haven](https://polyhaven.com/license) | CC0 material library evaluated. Concrete Wall 006 and Wood Planks Dirt were too distressed/photographic for this palette; neither was downloaded or used. |
| [Quaternius Downtown City Megakit](https://quaternius.com/packs/downtowncitymegakit.html) | Existing archives and licenses preserved. Rejected completed office/ruko/station designs are not imported by R0-B1. Existing nature and character assets remain unchanged. |
| [Synty POLYGON City](https://syntystore.com/products/polygon-city-pack) | Optional commercial candidate assessed. No applicable project license established; no purchase, restricted download or import. |

The A/B comparison favored A's clean fenestration and B's square openings/structural parts. Both were inspected as actual textured geometry in the browser before assembly. Complete sample buildings were excluded. The two official ZIPs and extracted licenses remain unmodified under `source-assets/r0b1/`.

Six actual source files appear in the prototypes:

- `window-white-detailed.glb` — 12 placements.
- `window-white-tall.glb` — 19 placements.
- `door-white-glass.glb` — 11 placements.
- `wall-window-wide-square-detailed.glb` — 12 placements.
- `wall-doorway-wide-square.glb` — 2 placements.
- `column-thin.glb` — 11 placements.

`door-rotate-square-a.glb`, `stairs-open-short.glb` and `border-high-corner-round.glb` were inspected but are **not counted as used prototype components**. The steep source stair was replaced with original comfortable-rise stair geometry. [Exact archive, license and individual-model hashes](../assets/game/architecture-r0b1/components-source.json) and [conversion/authoring hashes](../assets/game/architecture-r0b1/prototypes.json) are retained.

## Placement and collision

| Site | Root datum | Entrance world coordinate | Sampled terrain range | Adaptation |
|---|---:|---|---|---|
| Ruang Niaga | 22.05 m | 35.13, 22.30, 9.60; south | 19.64–22.00 m | Piers, stone terrace and local frontage steps; clearing trail retained. |
| Atlas | 32.20 m | 38.00, 32.50, −23.50; south | 29.74–32.13 m | Eastern shoulder, piers and local entrance stair. Continuous uphill access is conditional future work. |
| Antara | 21.65 m | −13.70, 21.65, 15.50; south | 15.91–23.53 m | Platform datum 27.40 m leaves about 3.87 m above the highest ground sample beneath the conservative envelope. Variable foundations and switchback access. |
| Awan | 16.40 m | 27.70, 16.68, 56.80; north | 13.76–16.31 m | Deck on piers, north-entry steps and observation stair. Final accessible arrival ramp remains future work. |

No terrain is flattened. Footprints, entrance directions, conservative clear widths, support heights, approach requirements and collision counts are in the [measured feasibility record](../assets/game/architecture-r0b1/site-feasibility.json). Public door clearances are conservatively recorded as 1.0 m for the shop and 1.3 m for the paired research/terminal entries; the station has an open stair entrance. The reference approach width is 2.4 m; canopy clearances are 2.90 m or greater.

Wall/column/barrier proxies are cross-sections of actual geometry, preserving opening gaps. Fixed glass and door leaves are solid at their actual positions. Overhead slabs are height-aware; upward-facing render triangles provide walking support without snapping a player onto an overhead roof. The station's junction remains passable underneath. Collision inspection uses one batched wireframe mesh.

Vegetation is masked only in this dedicated preview. Whole palm trunks and crowns are handled together. Switching the layer off restores every original instance matrix/count, palm visibility, grass resources and obstacle list. Terrain position buffers and all eight recorded production-file digests match the starting build.

## Visual correction evidence

Three deliberate inspection passes and subsequent close-up checks corrected:

1. **Massing/facades:** blank side treatment, unsupported glazing rhythm, missing terrace protection, unreadable black signage and entrance-obscuring site props.
2. **Pedestrian conditions:** opaque source-door glazing, blocked stair/platform access, disconnected switchback landings and a skyport fence crossing the boarding route.
3. **Rear/island context:** painted source surfaces incorrectly classified as glass, missing lift-exit apron, missing observation access and inconsistent palm masking.
4. **Targeted verification:** open facade-module seams, overly narrow shop-door placement and nonsolid fixed glazing. A rear camera that sat below the hillside was rejected and replaced with a clear, recorded inspection position; it is not used as a before/after comparison.

The [nine comparison pairs](architecture-r0b1-review/comparisons.json) keep camera tuples, FOV, resolution, daylight and exposure consistent. Live cloud and actor states differ between early and final captures. No lighting or postprocessing changes conceal geometry. All 19 final architectural screenshots are actual 1280 × 720 browser captures; a separate gameplay image, collision view, loading/retry pair and responsive check provide supplementary evidence.

## Payload and measured performance

- `transit-kingdom.glb`: **6,045,540 bytes**, four roots, all dependencies embedded.
- `components.glb`: **76,360 bytes**, nine raw inspected parts.
- Total new GLBs: **6,121,900 bytes / 6.12 MB**, below the 10 MB target.
- Twelve original wayfinding PNGs: **1024 × 256** each. Shared original soft-sky reflection: **512 × 256**. Two raw source palettes: **512 × 512** each.
- Uniform source normalization, linear vertex-color palette baking, removal of degenerate triangles, material/geometry deduplication, welded vertices and per-prototype material/role batching. No mesh-compression extension or new runtime dependency is required.

| Actual 600-moving-sample run | Drawing buffer | Calls at endpoint | Triangles at endpoint | Moving fps | Mean CPU render submission |
|---|---|---:|---:|---:|---:|
| Landscape only, preview hidden | 1728 × 888 | 69 | 1,219,310 | 30.00 | 1.19 ms |
| Standard, preview enabled | 1728 × 888 | 107 | 1,162,688 | 30.00 | 1.40 ms |
| Eco, preview enabled | 1280 × 658 | 107 | 1,120,576 | 30.00 | 1.42 ms |

The matched route is 12 seconds forward and 10 seconds backward from the same spawn, using native key input and the original walk speed. Standard adds **38 calls / about 0.20 ms CPU submission** at the sampled endpoint. Triangle totals fall because vegetation inside review clearings is hidden; the production island is not simplified. CPU submission excludes GPU execution and is not total frame cost. These localhost/session measurements do not establish mobile or internet-delivery performance. The older published R0-A3 120 fps result used a different buffer/session and is not a directly comparable benchmark.

The first uncached prototype URL transferred its full payload in **97.7 ms**; all scene assets/character/inspection parts were ready in **503.3 ms**. Other dependencies were already warm. The warm reload was ready in **441.4 ms**, with a 300-byte prototype revalidation. Renderer allocation counters were 186 geometries / 17 textures / 27 programs in Standard and 205 / 21 / 35 after the Eco switch; cached allocations remain until disposal. These are renderer resources, separate from model-file counts.

Authoring uses temporary Three.js/glTF Transform/Sharp tooling outside the repository. No project dependency migration occurred. The temporary environment emits a duplicate native libvips delegate warning from its two Sharp installations; exports complete and pass geometry/image checks. The normal browser session reports no warnings or errors.

## Verification and remaining gate

**96/96 tests pass:** the 81 original tests plus 15 new checks for source hashes/licenses, embedded assets, metric bounds, finite geometry/normals/indices, source sharing, concurrent cache/error retry, late-load cleanup, measured sites, exact restoration, floor/overhead support, solid glazing/passable entries, palm consistency, collision batching, camera presets and production isolation. [Results](architecture-r0b1-review/final-tests.txt).

The static audit has **58 inherited findings**, byte-identical to the R0-A3 baseline. It is not reported as passing. [Audit](architecture-r0b1-review/static-audit.txt).

Native browser checks confirmed one renderer, four prototypes after a deliberate 404/retry, zero missing textures, a complete jump/landing, keyboard walking, and touch-button movement in an actual 390 × 844 iframe viewport without horizontal overflow. This is responsive-layout evidence on the desktop browser, not a mobile GPU benchmark. Home adventure, editorial switching, Work navigation, `project=mbr`, the six-study index and landscape-only production were checked live; no R0-B1 files loaded on those production routes.

Artistic review remains open across the eight requested criteria: silhouette/composition, facade detail, materials/lighting, pedestrian experience, Indonesian tropical-modern identity, distinction, landscape fit and originality. **Target: owner average ≥4/5, no category below 3/5. Scores: unassigned.** Sheltered glass still reads flat in some views, dark bronze frames are visually strong, and service elevations are plainer than public faces. Continuous accessible approaches and complete upper-floor circulation/interiors are not a completed district. Station lift/rail operations and dragon flight are outside this phase.

## Changed files and reproduction

New files: `architecture-r0b1.html`; `assets/css/architecture-r0b1.css`; `assets/js/architecture-r0b1/{preview,showcase,views}.js`; `assets/game/architecture-r0b1/*`; `source-assets/r0b1/*`; `scripts/prepare-r0b1-components.mjs`; `scripts/bake-r0b1-architecture.mjs`; `scripts/lib/r0b1-{forms,prototypes}.mjs`; `scripts/record-r0b1-evidence.mjs`; `tests/architecture-r0b1.test.mjs`; this report and `docs/architecture-r0b1-review/*`.

The existing model library gained an optional catalog argument. Its default production catalog, loader, palette, normalization and cache behavior remain compatible. `ASSET_MANIFEST.md` now identifies the isolated architectural review separately from the unchanged production landscape.

```sh
node scripts/prepare-r0b1-components.mjs --deps /private/tmp/atlas-r0b1-tools/node_modules
node scripts/bake-r0b1-architecture.mjs --deps /private/tmp/atlas-r0b1-tools/node_modules
node --test tests/*.test.mjs
node scripts/record-r0b1-evidence.mjs
```

Retain the native browser captures/measurements when regenerating the evidence page; that script validates their dimensions, camera tuples, current payload and production hashes. No commit, push or deployment was performed. **STOP for owner review before R0-B2.**
