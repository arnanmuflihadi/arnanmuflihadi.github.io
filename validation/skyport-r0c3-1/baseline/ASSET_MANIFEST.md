# AR(N)AN Urban Atlas: asset manifest

## R0-B1.5 composition repair — current owner review

[Composition gallery and matched comparisons](docs/town-composition-review/index.html) ·
[Reversible preview](town-layout-r0b15.html?build=R0-B1.5-composition-repair-3#arrival) ·
[Composition report](docs/TOWN-COMPOSITION-REPAIR.md).

The previous layout failed owner visual review. The current planning layer replaces
its six masses with **ten commercial envelopes and one civic landmark composition**:
eight small market envelopes along two frontages, two square/gateway envelopes,
and the Atlas Guild hall, wings and observatory tower. These are original custom
greybox volumes, not finished architecture or replacements for the R0-B1 assets.
The model loader, GLB pipeline/cache, licensed source models and archives are retained.
No new GLBs, textures, asset downloads or dependencies are introduced. Production
remains the unchanged R0-A3 landscape; this composition is isolated to its preview.
Current measurements, actual browser counts and performance are recorded in the
linked gallery. **Human approval remains pending; STOP before R0-B2.**

## Previous R0-B1.5 final layout validation — rejected visual review

[Final four-view review and measurements](docs/town-layout-final/index.html) ·
[Playable preview](town-layout-r0b15.html?build=R0-B1.5-final-validation-5#arrival) ·
[Validation report](docs/TOWN-LAYOUT-FINAL-VALIDATION.md).

The provisionally accepted hub is retained. The dominant mineral-paved approach,
secondary gravel loop, aligned M1–M5 frontages and plaza-facing Guild are planning
geometry only. **No new GLBs, textures, source-model replacements or dependencies.**
The R0-B1 archives, license notices and model geometry remain preserved. Production
continues to use the R0-A3 landscape; the refined town stays on its dedicated preview
page. Final owner visual approval remains pending. R0-B2 has not started.

## Earlier R0-B1.5 alternatives and initial blockout (historical)

[Playable settlement plan](town-layout-r0b15.html?build=R0-B1.5.review#context) ·
[Alternatives, screenshots and navigation evidence](docs/town-layout-review/index.html) ·
[Scope and validation](docs/TOWN-LAYOUT-R0B15.md).

The selected Central Plaza Hub uses six explicitly temporary building envelopes,
an arrival platform and connected paving on the unchanged R0-A3 terrain. These
original planning primitives are **not finished architectural assets**. No new
GLBs, textures, asset downloads or dependencies were added. The existing landscape
and animated character reuse their licensed files below. The four R0-B1 prototypes,
original archives, component provenance and licenses are retained unchanged; the
station is omitted from this layout preview. Production remains landscape-only.
The preview restores vegetation buffers and collision on removal. Owner layout
approval is pending; R0-B2 has not started.

## Current review: R0-B1 architectural foundation (isolated)

[Live architectural inspection](architecture-r0b1.html?build=R0-B1.6#ensemble) ·
[19 final views / nine matched corrections](docs/architecture-r0b1-review/index.html) ·
[Source, changed-file and validation record](docs/ARCHITECTURE-R0B1.md) ·
[Actual browser measurements](docs/architecture-r0b1-review/technical-evidence.json).

Four original prototypes—Ruang Niaga, Atlas Research Centre, the newly authored
Stasiun Antara, and Pelabuhan Awan—use **67 placements of six actual components**
from two newly downloaded, verified **Kenney CC0-1.0** collections. Modular
Buildings **2.1 contains 108 actual GLBs**; Building Kit **1.0 contains 79**.
Official archives, license notices and original extracted models remain unchanged
in `source-assets/r0b1/`. Attribution is optional; Kenney is credited here.

Selected files: `window-white-detailed.glb`, `window-white-tall.glb`,
`door-white-glass.glb`, `wall-window-wide-square-detailed.glb`,
`wall-doorway-wide-square.glb`, `column-thin.glb`. Nine types were inspected;
the other three are not counted as used prototype components.

Sources: [Modular Buildings](https://kenney-assets.itch.io/modular-buildings),
[Building Kit](https://kenney-assets.itch.io/building-kit).
Commercial/Roads direct downloads returned HTTP 403 and contributed no files.
Poly Haven photographic finishes were evaluated and not selected. No Synty or
other restricted commercial files were obtained. Rejected completed Quaternius
Jakarta designs are not reused by this review layer.

| Browser artifact | Actual payload | Geometry / use |
|---|---:|---|
| `assets/game/architecture-r0b1/transit-kingdom.glb` | 6,045,540 bytes | Four original roots, 77,876 triangles, 64 material/role draw batches; 12 embedded original signage PNGs. |
| `assets/game/architecture-r0b1/components.glb` | 76,360 bytes | Nine raw inspected types, 11 meshes, 804 triangles, two embedded 512 px palettes. |
| Total new GLBs | **6,121,900 bytes** | No external buffers/textures or new browser dependencies. |

Original project-authored facades, openings, roof shells, terraces, stairs,
supports, planting and wayfinding are combined with genuine imported geometry.
Source palette texels become controlled linear vertex colors; source-blue door
surfaces become real glazing. Original source archives and their textures are
preserved. [Archive/model/license hashes](assets/game/architecture-r0b1/components-source.json),
[authoring/output hashes and per-root counts](assets/game/architecture-r0b1/prototypes.json),
[design vocabulary](assets/game/architecture-r0b1/design-system.json),
[measured placement/clearance/collision plan](assets/game/architecture-r0b1/site-feasibility.json).

The running review layer includes adaptive supports and entrance steps:
**97 meshes/geometries, 78,632 potential triangles, 25 shared materials and 13
textures, none missing**. The hidden raw-source inspector adds its separate two
textures. Normal browser logs are clean. A deliberate missing-file test recovers
four models through Retry with one renderer and two cached new GLBs.

**96/96 tests pass**, including the unchanged 81-test baseline. The static audit
still has **58 inherited findings**. Three visual passes and targeted follow-up
corrections have recorded evidence; no human score or artistic approval is claimed.
Human review is pending. **R0-B2 has not started.** Home/Work remain landscape-only;
the eight recorded production-source hashes, existing assets, licenses and
research integration remain unchanged. No deployment was performed.

## Production landscape: R0-A3 landscape detail

[Play build 73](index.html?experience=adventure&build=73) ·
[Seven matched comparisons](docs/landscape-detail-review/index.html) ·
[Changed files and checks](docs/LANDSCAPE-DETAIL-R0A3.md) ·
[Machine-readable record](assets/game/scenery/landscape-detail-r0a3.json).

R0-A2's exact upper terrain, footprint, support, routes, reservations, sky, lighting,
player and research are preserved. The active scene adds localized fractured stone,
28 embedded slab pieces in seven formations, a closed curved waterfall volume,
source pool, wider channel, eleven bank rocks, spill foam and nine mist cards.
All new stone, plant and water geometry/shaders are project-authored, with no new
third-party downloads or dependency changes. Prior GitHub references remain
technique references only; no reference code/assets are copied.

The same CC0 tree now uses **five cached growth forms / ten derived geometries**:
33 spreading, 22 emergent, 24 windswept, 22 tiered and 33 umbrella trees. Tree count
and trunk positions remain **134**. Imported ground ferns rise from 660 to **678**;
24 cliff ferns, ten palms, 131 shrubs, 28,063 grass blades and the 34 cloud cards
remain. Eighteen selected route-side clusters each add a broadleaf plant, a small
flowering plant and a low stone. Source GLB buffers, UVs and texture maps remain.

Actual browser environment before actors: **82 mesh objects, 1,335,218 potential
triangles, 73 attached geometries, 40 materials and four textures, none missing**.
Potential triangles increase **14,092 / 1.07%** from R0-A2. Measured walking submits
92 calls and 1,255,902 triangles, versus 86 / 1,229,590 before. These are view-specific
render counters, separate from potential inventory. [Measurements](docs/landscape-detail-review/walking-performance.json).

All six previous inventory GLB hashes match. The five active files still total
**3,859,228 bytes**, with the same two scenery requests totaling **824,100 bytes**.
All source/license records and archives remain. The new actual-canvas fallback is
`assets/img/floating-atlas/landscape-detail-poster.webp`, **62,822 bytes / 1728×874**;
older posters remain. The pre-pass source is retained in
`assets/js/floating-atlas-legacy-r0a2/` and is not loaded by Home/Work.

**81/81 tests pass**, retaining all previous 79. The growth-cache expectation changes
from six to ten because two new forms are intentionally added. Two new regressions
cover the waterfall's closed volume, source connection, cliff clearance, safe stream
edge, route-side spacing and reduced water/mist motion. Static audit: the same
58 inherited findings. **Human visual score and approval remain pending; stop before R0-B.**

## Historical review: R0-A2 environmental polish

The existing landscape is polished, with its exact upper terrain, support triangles,
six routes, research registry and reserved coordinates preserved. No architecture
or additional playable realm is added. Human visual approval remains pending.

[Play](index.html?experience=adventure&build=67) ·
[Eight before/after pairs](docs/environment-polish-review/index.html) ·
[Changes, checks and limits](docs/ENVIRONMENT-POLISH-R0A2.md) ·
[Machine-readable provenance](assets/game/scenery/environment-polish-r0a2.json) ·
[Current hashes and inventory](docs/environment-polish-review/inventory.json).

The same five active GLBs total **3,859,228 bytes**; scenery remains the same two
files, **824,100 bytes**. All six prior inventory hashes, including the retired
architecture GLB, match. CC0 notices and original source archives are untouched.
No new third-party assets, dependencies, reference code or downloads are included.

The existing imported Quaternius broadleaf model now has three cached growth
forms: spreading, emergent and windswept. Six derived geometries preserve source
buffers, material maps and UVs. **134 trees** comprise 60/36/38 growth forms, zoned
as 107 forest, 24 meadow and three ridge trees. Imported ferns comprise **660
ground and 24 cliff instances**. The scene also has ten retained original palms,
131 authored shrubs, 28,063 curved grass blades in 31 chunks, 34 instanced cloud
cards and four uninhabited distant silhouettes. These are instances, not downloads.

Browser environment inventory before actors: **73 mesh objects, 1,321,126 potential
triangles, 61 currently attached geometries, 33 materials and four textures, none
missing**. Potential triangles increase by 45,057 (3.53%) from R0-A. Distance-based
grass uses prebuilt near/far index buffers sharing vertex attributes; the renderer
holds up to 113 geometries including those levels and actors. Counts and submitted
triangles are separate measures. [Actual counts](docs/environment-polish-review/browser-assets.json)
and [600-frame moving samples](docs/environment-polish-review/walking-performance.json).

The new static fallback, `assets/img/floating-atlas/environment-polish-poster.webp`,
is a **60,546-byte, 1728×874** actual-canvas export. Older posters and all previous
evidence remain. The pre-polish R0-A source is preserved in
`assets/js/floating-atlas-legacy-r0a/`, never imported by the active world.

**79/79 tests pass**, preserving the previous 77. The static audit retains the
same 58 inherited findings; it is not a passing audit. No human art score is assigned.

## Historical review: R0-A landscape correction

The active Home/Work world is now landscape only. All previous buildings, station,
skyport structures and plazas are retired to `assets/js/floating-atlas-legacy-r0/`.
The architecture GLB, approved generator, original archives and source licenses
remain unchanged. The active scene does not import that legacy assembly.

[Play](index.html?experience=adventure&build=63) ·
[New screenshot gallery](docs/landscape-review/index.html) ·
[Report and changed files](docs/LANDSCAPE-R0A.md) ·
[Reference techniques and separate code/asset rights](docs/landscape-review/references.md) ·
[Current inventory and preserved hashes](docs/landscape-review/inventory.json).

Machine-readable active/retired asset provenance and license paths are in
[`landscape-r0a.json`](assets/game/scenery/landscape-r0a.json).

Actual browser environment, before player/guide: **40 mesh objects, 1,276,069
potential triangles, 23 unique geometries, 36 materials and four textures, zero
missing**. Twelve instanced vegetation batches represent 145 imported broadleaf
trees, 710 ground ferns and 42 cliff ferns. Ten original palms, 27,444 authored
grass blades, chiseled geology, stream, clouds and daylight sky complete the
landscape. There are **zero architecture instances**, no constructed decks, and
no physical research landmarks or new NPCs. One existing guide is retained.

Only `canopy-tree.glb` (719,224 bytes) and `fern.glb` (104,876 bytes) are scenery
requests, **824,100 bytes total**. The same player, resident and jump files bring
the active five-GLB inventory to **3,859,228 bytes**. All remain under their
previously verified Quaternius CC0 provenance below. No reference assets/code or
new third-party downloads are included. Reference license uncertainty does not
change the licenses of the assets actually shipped.

The current static fallback is `assets/img/floating-atlas/landscape-poster.webp`,
47,340 bytes, 1265×648, exported from the actual live WebGL scene. It is not a
QA screenshot. The original `atlas-poster.webp` and previous evidence are retained.

Human visual review is pending. No aesthetic score has been assigned.

## Historical review: R0 Floating Urban Atlas

Transit Kingdom is implemented for owner review. No visual score or human approval
has been assigned. Target: average 4/5, no category below 3/5. Only this first island
is constructed. [Play](index.html?experience=adventure&build=57),
[review gallery](docs/floating-review/index.html),
[technical report](docs/FLOATING-ATLAS-R0.md),
[source/integration record](assets/game/scenery/floating-atlas-r0.json).

The previous Phase 2 environment was not visually approved. It is retained as
[documented legacy modules](docs/LEGACY-JAKARTA-DISTRICT.md), with its evidence,
licenses, GLBs and tests. Its district assembly is not invoked by the new Home/Work
loader. Shared engine helpers remain in use with preserved legacy defaults.

Actual R0 environment: **393,127 triangles**, 369 mesh objects, 167 geometries,
98 materials and **35 referenced textures, zero missing** before adding the player
and Nadia. It loads **three cached scenery GLBs / three requests / two approved
architecture prototypes**. There are one commercial and two neighborhood support
buildings, eleven imported station-glazing modules, 32 imported trees, 76 ground
ferns and 14 cliff ferns. Ferns use three instanced batches. Nine palms and the two
major landmarks, skyport, market canopy, terrain, geology, sky and furnishings
are project-authored. No repeated office towers are placed.

The three unchanged scenery GLBs total **6,204,348 bytes**. Including the unchanged
player, jump-animation and existing resident GLBs, six files total **9,239,476
bytes**. Original provenance, source hashes, archives and all CC0 notices remain.
No new third-party download was made. Full inventory and hashes are in the R0
record and `docs/floating-review/inventory.json`.

The island's static fallback is a genuine live-canvas export at
`assets/img/floating-atlas/atlas-poster.webp`, **1265×648 / 39,298 bytes**. It is
separate from the ten unretouched native browser review screenshots. The old city
poster is no longer used as the Home/Work world fallback.

All **73 tests pass**, retaining all original 67 and the 16 scoped asset,
architecture and character regressions. The **58 inherited static-audit findings
remain unchanged** and explicitly documented. Actual integrated walking measured
163.62 fps locally at 1280×656, shadows on; see raw evidence and device limits in
the report. This is not an isolated-showcase extrapolation or a human art score.
No additional realm, flight, dragon placeholder, monster or new quest is added.

## Historical snapshot: Phase 2 integrated Jakarta district

The following counts and approval status describe the preserved Phase 2 delivery,
before the user's R0 reboot request.

Implemented for review, 1 November 2026. The user's Phase 2 brief approves the
Phase 1.5 architecture **as reusable components**. Environment approval remains
pending; no human score has been assigned. Target: average 4/5, no criterion below
3/5. This is one district inside the existing Home/Work adventure experience.

Open [the playable district](index.html?experience=adventure&build=46) or
[the fixed arrival view](index.html?experience=adventure&district-review=spawn&build=46).
Read [the review and all eight comparison pairs](docs/PHASE-2-DISTRICT.md),
[current integration provenance](assets/game/scenery/district-integration.json),
[actual browser asset counts](docs/district-review/loaded-assets.json) and
[measured playable performance](docs/district-review/performance.json).

The unchanged approved architecture factory now supplies **21 buildings**:
eight main buildings and thirteen background buildings. The three original
variants remain distinct. Four unchanged CC0 GLBs total **6,659,124 bytes**;
the browser confirms **4 loaded files, 4 requests and 3 cached prototypes**.
Imported asset assembly contains **684,861 triangles**, including **610,103
imported/source-derived** and **74,758 authored** triangles, in **125 batches**
plus independent tree graphs. It references **49 textures with zero missing**.
These are assembly counts, not the view-dependent whole-scene render counters.

Actual imported instances: office 4, shop/source-derived neighborhood 17,
tree 19, planter 4, fern 187 (including terraces), AC 12, station entrance 10,
glazing 12, civic window 6, bollard 2, drain 8 and manhole 5. Names count model
instances before batching, not network requests. Source filenames and unchanged
digests remain in `architecture-source.json`, `source.json` and the new integration
record. No third-party assets were downloaded in Phase 2.

District-authored additions include shared nonoverlapping paving, ramps, vaulted
station integration, physical signs, shallow occupied-window displays, street
furniture, a bicycle, palms and atmosphere. Shop lettering is generated at 2048 px
width, with mipmaps and device-capped anisotropy. These generated textures and
details do not replace the imported major-building foundation. Source archives,
licenses, model loader and approved architecture generator remain unchanged.

Final verification: **67/67 tests pass**, including all original 16 scoped tests.
The five inherited district failures are individually classified in the review.
The static audit still reports **the exact same 58 inherited findings**, with
zero new findings; this is documented, not presented as a passing audit.
Eight camera-matched before/after pairs, a green-park view, actual walking,
research/state restoration, mobile and controlled asset-failure evidence are
retained under `docs/district-review/`. No Phase 3 expansion has started.

## Historical snapshot: Phase 1.5 focused final visual correction

The following is the preserved Phase 1.5 delivery record. Its pending-review and
paused-district wording describes that capture, before the user's Phase 2 brief.

Completed for review, 1 November 2026. The previous three-building screenshot
was **not visually approved**. This correction is **pending human visual review**.
Target average: **4/5**; human score: **unassigned**. Phase 2 remains paused.

Open [the enhanced showcase](asset-showcase.html?build=35#pedestrian-composition).
It now provides thirteen live viewpoints, five new pedestrian captures and eight
refreshed comparison captures. Every new pedestrian capture uses a **1.65 m eye
height above the sidewalk datum, 40° field of view, 1280 × 720 resolution and the
same neutral daytime lighting**. Original/enhanced pairs continue to share their
camera tuple, source scale and lighting.

| Variant | Preserved imported foundation | Focused correction |
| --- | --- | --- |
| Contemporary Tropical Office | `Building_Large_2.gltf`; normalized source height 22.4 m; composed height 23.79 m | Locally clear the obsolete entrance surround and wall overlaps on the enhanced clone. Framed double doors, transom, pulls and a 20 mm stone porch. Cool concrete, warm plaster, soft sky glass and restrained parapet caps. Glazed leaves 0.91 × 2.40 m; clearance above porch 3.06 m. |
| Urban Mixed-Use Commercial Building | `Building_Small_1.gltf`; normalized source height 13.6 m; composed height 16.21 m | Clear residual stoop fragments locally. Two articulated door/display bays, clean central pier and header, metal frames and timber soffit. Fired-clay roster remains distinct from painted terracotta plaster. Glazed leaves 0.98 × 2.20 m; 20 mm porch; clearance above porch 2.86 m. |
| Human-Scale Neighborhood Shopfront | Lower-storey source-derived geometry from `Building_Small_1.gltf`, original uniform scale; composed height 8.18 m | Separate entrance leaf and transom, clean frontage header, brown timber, sage plaster, fired-clay eaves and timber fascia. Glazed leaf 0.98 × 2.15 m; 20 mm porch; clearance above porch 2.80 m. |

The architecture is preserved and refined, not rebuilt. Source GLBs, original
archives, CC0 notices, provenance, optimization pipeline, model cache, scale
normalization and collision exports remain intact. All **16 existing collision
proxies match the pre-correction captured records exactly**, including overhead
clearances. The displayed entrance dimensions describe visual geometry; the
existing solid-building collision behavior is retained.

### Materials, light and ground connections

- Concrete is pale cool gray; plaster is warmer and more matte; andesite is dark
  gray-green with a subtle wash. Timber uses a separate warm brown wash; fired
  clay is deeper red than terracotta plaster. Satin frames use restrained metalness.
- Glass uses a smooth project-authored sky/reflection wash, modest emissive fill
  and real recessed geometry. It uses no transmission, screen-space reflections
  or expensive photorealistic shader. Vegetation finish clones retain their
  original maps while removing source vertex wear colors.
- A gentle sky gradient, natural hemisphere fill and warm directional sunlight
  provide neutral daytime depth. The existing 2048 px soft shadow map remains;
  source occlusion is retained where appropriate. There is no postprocessing.
- Porch plates rise only 20 mm above paving. The continuous sidewalk support now
  sits below the imported pavers, avoiding coplanar overlap. Pavers receive
  building shadows without casting self-shadow stripes. Thin instanced joints
  make the paving modules readable. Soil meets the road datum; thin foundation
  supports fill the space below the existing building footprints up to sidewalk
  level. They add no collision obstacle and preserve the model transforms.

### Actual loaded geometry and resource implications

The three-variant view contains **78,449 architectural triangles**:
**71,321 imported/source-derived** and **7,128 project-authored**.
There are **359 visible authored instances**, **108 architectural mesh batches**
and **26 instanced detail batches**. These include three building foundations,
three imported AC units and twenty-four imported terrace ferns. Context retains
two imported trees, two planters, two additional ferns and thirty-four paving
modules. The scene loads **four cached GLBs** and **three cached architectural
prototypes**, with **32 referenced textures and zero missing textures**.

Compared with the preceding Phase 1.5 capture: architectural triangles decrease
by **564**, authored triangles increase by **538**, and architectural mesh batches
increase by **16**, including one additional instanced detail batch. Local
source-derived frontage edges add mesh batches; they are generated once per
cached prototype. Twenty-one sidewalk joint instances add **252 context
triangles in one batch**. Draw calls depend on viewpoint and culling.
Three foundation supports add **36 context triangles in one additional batch**.

The four unchanged GLBs total **6,659,124 bytes**. Base procedural texture data is
**44,032 bytes**, an increase of **35,840 bytes**, excluding unchanged sign maps
and driver allocations. No model download, light, shadow map or continuous render
loop is added. Generated/context resources have explicit disposal. Thirteen lazy
gallery JPEGs total **879,663 bytes**, including **353,317 bytes** for the five
new captures. These are measured resource counts, not a frame-rate benchmark.

### Evidence and verification

- [Architectural enhancement record](assets/game/scenery/architecture-enhancements.json):
  source references, current generator digest, dimensions, material changes,
  measured geometry and resource deltas.
- [Five calibrated pedestrian captures and camera evidence](assets/img/architecture-review/final-correction-evidence.json).
- [Refreshed comparison evidence](assets/img/architecture-review/scene-evidence.json).
- [Final verification record](docs/architecture-review/final-correction-verification.json),
  [browser checks](docs/architecture-review/final-browser-checks.json) and
  [preserved pre-correction colliders](docs/architecture-review/pre-correction-colliders.json).
- [Architectural design and reuse guide](docs/ARCHITECTURAL-ART-DIRECTION.md).

| Check | Executed result |
| --- | --- |
| Existing scoped tests | **PASS 16/16**, unchanged assertions: `node --test tests/architecture-design-system.test.mjs tests/asset-foundation.test.mjs tests/atlas-character.test.mjs`. |
| Source and licenses | PASS: original GLB hashes match retained manifests; source/cache fingerprints remain unchanged; both retained scenery license hashes match their verified archive notices. No source archive was edited. |
| Geometry and transforms | PASS: 108 meshes inspected through decoded attribute components, including interleaved/quantized source data; no nonfinite components, empty indices or nonpositive transform determinants. Real imported meshes remain in all three variants. |
| Collision compatibility | PASS: 5 office, 6 commercial and 5 neighborhood proxies match pre-correction evidence exactly. Existing clearance, body blocking and rotated-proxy tests pass. |
| Five pedestrian captures | PASS: saved and visually inspected office entrance, commercial arcade, neighborhood shopfront, sidewalk interface and full three-building composition. All five share resolution, eye height, lens and light. No obvious clipping or floating geometry in these views. |
| Fair comparisons | PASS: original/enhanced camera tuples match exactly for both office and shop. Eight earlier gallery views recaptured under the same new daylight. |
| Browser and textures | PASS: fresh review tab has zero warnings/errors; all thirteen JPEGs decode at 1280 × 720; no referenced model texture is missing. |
| Review controls | PASS: all thirteen view buttons and thirteen gallery links select their correct live view. Keyboard Enter activates a gallery link; Space toggles collisions both ways; focus outline is 3 px; diagnostic disclosure opens. |
| Narrow layout | PASS: requested 390 × 844 and 320 × 740 widths produce no horizontal document overflow (measured 375/375 px and 305/305 px client/scroll widths). Controls remain at least 44 px tall; viewport override reset. |
| Artistic acceptance | **PENDING HUMAN REVIEW**. No score, automatic visual approval or Phase 2 expansion. |

The previously recorded broader repository run was **55/60**, with five inherited
district failures; its static audit had **58 inherited findings**. Those broader
checks were not rerun or repaired during this focused correction. Prior error/
retry fixture results remain historical, not newly executed checks.

Scoped antislop delivery gate for this review interface and evidence:

- **Hard Gate PASS:** all new image links and view controls exercised, decoded
  images have dimensions/alt text, narrow layouts stay within the viewport,
  keyboard focus works, existing loading/error/retry states remain, and counts
  and review status come from recorded evidence.
- **Purpose Gate PASS:** the sky gradient serves daylight balance; paired captures
  serve fair architectural comparison; pedestrian close-ups expose actual doors,
  materials and thresholds. Cream paper, forest text and bronze focus preserve
  the established review identity.
- **Liveliness PASS:** ENERGY 2 / RHYTHM 2 / MOTION 1; the model remains the focal
  point, paired and wide views have distinct roles, and no continuous motion was
  introduced. The design direction remains a tropical architectural asset study.
- **Craftsmanship PASS:** 16 regression tests, exact collider preservation,
  thirteen functioning views/gallery links and five inspected pedestrian
  captures. This gate covers technical/interface craft, **not human architectural
  approval**.

## Retained Phase 1 asset foundation record

Reviewed 1 November 2026. Scope: a small imported asset showcase and reusable loading
foundation. The earlier district work is paused. This phase does not rebuild or
claim visual acceptance of the entire city.

## Review scene

Serve the repository with its usual static server, then open
[`asset-showcase.html`](asset-showcase.html). It is an isolated, noindex development
route. Home and Work are not switched to a new district implementation.

The five viewpoint controls inspect the streetscape, complete multi-story building,
shopfront, urban tree and street furniture. `Other side` changes the viewing corner.
`Collision bounds` displays the actual exported proxy shapes. `Primitive comparison`
replaces only the two visible buildings with clearly labeled blockouts under the
same camera and lighting; these blockouts are not claimed to be finished assets.

The historical primitive city is visible in
[`docs/urban-atlas-review/commercial.jpg`](docs/urban-atlas-review/commercial.jpg).
Its camera differs from this isolated review. New browser screenshots accompany
the Phase 1 delivery; the controlled in-scene comparison is a fresh blockout,
not a mislabeled historical screenshot.

## Sources and rights

| Source | Verification and decision |
| --- | --- |
| [Quaternius Downtown City MegaKit](https://quaternius.com/packs/downtowncitymegakit.html) | Official page lists CC0. Downloaded `Downtown City MegaKit[Standard].zip` from the creator's itch.io free-download flow. All eleven library models and the planter match the recorded source glTF hashes. Every referenced buffer/texture exists in the archive. Its `License_Standard.txt` exactly matches the retained notice. Only Standard files are used. |
| [Quaternius Stylized Nature MegaKit](https://quaternius.com/packs/stylizednaturemegakit.html) | Official page lists CC0. Downloaded `Stylized Nature MegaKit[Standard].zip` through the creator's free-download flow. `CommonTree_1.gltf`, `Fern_1.gltf`, their dependencies and included license verified. The Standard archive has no palm glTF; this review uses its broadleaf shade tree and ferns. It does not claim an identified Indonesian tree species or a licensed palm. |
| [Kenney City Kit Commercial](https://kenney.nl/assets/city-kit-commercial) | Official page lists 50 files and CC0. The official `kenney_city-kit-commercial_2.1.zip` download returned HTTP 403. Archive contents and its bundled license could not be verified, so no Kenney files are imported. To consider it later, download version 2.1 using “Continue without donating” on this page and supply the intact ZIP including its license. Exact attempted URL: `https://kenney.nl/media/pages/assets/city-kit-commercial/a742d900eb-1753115042/kenney_city-kit-commercial_2.1.zip`. No substitute is labeled as Kenney. |
| [Quaternius Ultimate Modular Characters](https://quaternius.com/packs/ultimatemodularcharacters.html) | Evaluated and retained: the existing `Individual Characters/glTF/Adventurer.gltf` conversion has a self-contained real skinned mesh, 62 joints and Idle/Walk/Run clips. The creator page and retained pack notice list CC0. Its delivered hash matches `assets/game/characters/urban-explorer/source.json`; the character regression tests verify geometry/rig/animation. The source archive was not downloaded again in this phase. No new character or animation is imported into the asset showcase. |

[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) permits copying,
modification and commercial distribution without attribution requirements.
Creator notices are preserved voluntarily. No paid Pro/Source files or source
engine shaders are claimed, acquired or redistributed.

Retained notices:

- [`downtown-city-megakit-LICENSE.txt`](assets/game/scenery/downtown-city-megakit-LICENSE.txt)
- [`stylized-nature-megakit-LICENSE.txt`](assets/game/scenery/stylized-nature-megakit-LICENSE.txt)
- [`CC0-Quaternius.txt`](assets/game/characters/urban-explorer/CC0-Quaternius.txt)

## Delivered files

| Local file | Bytes | Contents and use |
| --- | ---: | --- |
| `assets/game/scenery/architecture-library.glb` | 5,380,248 | Eleven real source templates. Seven types placed in this review; the four other templates remain cached and unplaced. 19 embedded images, quantized geometry, 3,621,804 accessor bytes. |
| `assets/game/scenery/canopy-tree.glb` | 719,224 | Actual CommonTree_1 mesh, bark and leaf textures. |
| `assets/game/scenery/fern.glb` | 104,876 | Actual Fern_1 mesh and texture. |
| `assets/game/scenery/city-planter.glb` | 454,776 | Actual Prop_Planter_Single mesh and mapped material. |
| **Showcase payload** | **6,659,124** | Four GLB files. Vendor, page and styles excluded. This is a byte budget, not a frame-rate claim. |

All GLBs embed their buffers and images; there are no external texture URLs or
runtime requests to model stores. Output SHA-256 digests and conversion details
are in [`architecture-source.json`](assets/game/scenery/architecture-source.json)
and [`source.json`](assets/game/scenery/source.json). The older `city-building.glb`
is retained historical work and is not requested by this showcase.

## Actual placed assets

| Source filename | Library name | Instances | Source triangles per instance |
| --- | --- | ---: | ---: |
| `Building_Large_2.gltf` | office | 1 | 45,122 |
| `Building_Small_1.gltf` | shop | 1 | 18,344 |
| `CommonTree_1.gltf` | tree | 1 | 6,265 |
| `Prop_Planter_Single.gltf` | planter | 1 | 118 |
| `Fern_1.gltf` | fern | 3 | 288 |
| `Prop_Bollard.gltf` | bollard | 4 | 190 |
| `Sidewalk_NoCurb_3m.gltf` | paving | 22 | 42 |
| `Prop_Drain.gltf` | drain | 1 | 10 |
| `Prop_ManholeCover.gltf` | manhole | 1 | 118 |
| `Prop_ACUnit.gltf` | aircon | 1 | 136 |

The running scene reports **36 instances, 10 distinct placed types, 61 mesh objects,
35 unique geometries, 72,661 imported triangles and 28 referenced decoded textures**.
These values are calculated from the loaded scene graph, not from pack advertising.
It also reports four file requests and eight collision bodies. Expand “Running
scene evidence” to inspect the current URLs, transforms, bounds and counts.

## Loading, normalization and collision

[`model-library.js`](assets/js/urban-atlas/model-library.js) exposes
`createModelLibrary()`, `get(assetId)` and `instantiate(assetId, options)`.
The URL-keyed promise cache coalesces concurrent loads; failed promises are removed
so they can retry. Instances share original geometry, textures and palette
materials. A missing mesh or load failure raises a visible error and retry control;
there is no silent primitive replacement. The library owns its resources and must
outlive its instances. Call `dispose()` after removing them.

[`showcase-plan.js`](assets/js/urban-atlas/showcase-plan.js) is the reusable placement
record. Y is up and building façades face +Z. Rotation is applied before computing
bounds. Uniform scale preserves source proportions; the building is 22.4 m tall and
the shop is 13.6 m, approximately 0.8 times their source size. Tree height is 6.5 m,
bollards 0.8 m and planter 0.8 m. Root offsets place each model's true minimum at
its support level. The façade approaches share the 0.16 m sidewalk. Drain/manhole
tops are 0.005 m above the road; the AC unit is intentionally wall mounted.

Collision proxies derive from transformed mesh bounds. Trees use only vertices
in the lower trunk region, so a canopy does not create an invisible wall. The
records use the existing collision system's `{x,z,w,d,minY,h}` format. Tests verify
that the road and walking strip stay clear and a moving point stops at the real
building footprint. The showcase is an inspection scene, not another playable city.

## Finish and optimization

The architecture conversion welds/deduplicates meshes, shares maps, prunes unused
resources and quantizes position/normal/UV buffers. Color textures are at most
512 px; normal/ORM maps at most 256 px. Scenery maps are at most 256 px. Source UVs,
normals, recessed openings, cornices and roof geometry remain actual imported data.

Mapped masonry/trim receive neutral mineral washes. Photographic fake interiors
become solid muted green glass. Runtime finishes use warm concrete, desaturated
mineral trim, rough nonmetal surfaces, softer glass specular response and lifted
leaf color. Downtown's vertex-color engine wear masks are disabled as paint;
ornament color maps are deliberately replaced by a mineral finish. Other referenced
maps remain embedded and decoded. This uses matte PBR lighting for the stylized
study; the paid pack's painterly/wind shaders are not included.

The review uses hemisphere fill, warm sun, 2048 px soft shadow maps and capped pixel
ratio. It renders on demand when loaded, resized or inspected; there is no perpetual
animation. Primitive geometry is confined to the base/road/curb, invisible collision
proxies and the explicitly labeled optional blockout comparison. Both major visible
buildings are imported meshes.

## Reproduce and verify

Use the official free Standard archives. Keep the large downloads outside the site.

```sh
python3 scripts/verify-asset-sources.py --city /path/city-standard.zip --nature /path/nature-standard.zip
node scripts/prepare-atlas-architecture.mjs --source /path/extracted-city --deps /path/temporary-node_modules
node scripts/prepare-atlas-scenery.mjs --source /path/pack-parent --deps /path/temporary-node_modules
node --test tests/asset-foundation.test.mjs tests/atlas-character.test.mjs
```

The existing authoring tools use `@gltf-transform/core@4.2.1`,
`@gltf-transform/functions@4.2.1`, `@gltf-transform/extensions@4.5.1` and
`sharp@0.34.5`. They are build-time tools and are not deployed. The architecture
converter rejects a source glTF or license that differs from the reviewed files.

[`verification.json`](assets/game/scenery/verification.json) records the actual
archive SHA-256 hashes, included license hashes, 14 checked source models and their
buffer/image dependencies. Re-running the verification checks the source glTF
against the approved per-file digests before writing an updated record.

Foundation tests cover real geometry/hash/license checks, rotated uniform scale,
ground/collision alignment, shared geometry/cache identity, a clear walking strip,
flush covers, load failure retry, invalid transforms and disposal. Broader district
acceptance remains outside this phase.

## Executed browser and delivery checks

Tested the actual local page at `http://127.0.0.1:4173/asset-showcase.html?build=7`
in the Codex in-app browser using native browser controls. Viewports: default
1265 × 721, 390 × 844, 320 × 740 and 768 × 1024. Temporary viewport overrides were
reset. No external Playwright browser or new browser dependency was installed.

| Check | Result and evidence |
| --- | --- |
| Page identity / nonblank / no error overlay | PASS: correct asset-foundation title and route; real building, shop and greenery visible. |
| Imported meshes and maps | PASS: 36 instances, 61 mesh objects, 72,661 imported triangles, 28 decoded referenced textures, zero missing textures. Browser resource inventory shows exactly the four expected GLB URLs. |
| Complete building | PASS: full building visible on desktop and phone. Projected bounding corners remain within the camera frame, including the 320 px check. |
| Ground and collision | PASS: mesh support error below 0.000001 m; eight derived bodies; trunk-only tree proxy; unit checks confirm passable pavement/road and solid building footprint. |
| Inspection controls | PASS: all five views, both viewing corners, collision overlay, blockout on/off and evidence disclosure exercised. Space toggles the focused comparison button; visible focus retained. |
| Responsive controls | PASS: no horizontal document overflow at 320/390/768 px; phone buttons measured 44 px tall and at least 175 px wide at 390 px. |
| Text and control contrast | PASS: normal text pairs 4.88:1 or higher; main text 10.31:1, pressed control 9.09:1, pressed hover 7.08:1; control boundaries 4.03:1 and focus 5.08:1. This is a scoped review, not a whole-site accessibility certification. |
| Error / retry | PASS: separate localhost fixture deliberately returned one tree 404; page showed a visible error, disabled inspection controls and withheld success counts. Native Retry loading restored all 36 instances with zero missing textures. The fixture server was then stopped. |
| Normal console | PASS: no warnings or errors in the normal showcase tab after inspection. The intentional 404 belonged only to the separate error fixture. |
| Manifest download | PASS: native Download manifest control produced `ASSET_MANIFEST.md`; no placeholder link. |
| Automated foundation and character checks | PASS: `node --test tests/asset-foundation.test.mjs tests/atlas-character.test.mjs`, 9/9. Syntax checks and `git diff --check` pass. |

The broader district suite was already **44/49** before this phase's changes.
Its five failing checks concern the unfinished district's NPC approaches, station
ramp, street support samples and old coordinate assertions. The whole-site static
audit still reports **58 inherited findings**. Neither suite is reported as passing;
those issues are outside this asset-only approval gate. No deployment was made.

The antislop delivery gate is scoped to the new showcase:

- **Hard Gate PASS:** actual sourced models, documented rights, no invented counts,
  working controls/download, loading/error/retry states, responsive checks and
  measured text contrast.
- **Purpose Gate PASS:** warm mineral finishes unify the imported kits; cream text
  panels keep labels readable; serif view captions identify the field-atlas study;
  the bronze focus/collision accent marks inspection state. No decorative glows,
  animation, stock icons or filler sections.
- **Liveliness PASS:** ENERGY 2 / RHYTHM 2 / MOTION 1; the façade is the focal point,
  larger scene space is separated from compact controls and a supporting record,
  with a repeated warm-paper/forest atlas identity and deliberate bronze accent.
- **Craftsmanship PASS:** five inspected camera views, visible full building,
  shared mesh resources, distinct selected/hover/focus states, no silent primitive
  substitutions, truthful scope/limitations and recorded browser evidence.

## R0-RESET-FINAL settlement reconstruction (local development only)

The alternate town repositions the four unchanged groups in
`validation/market-street-s2d/market-street-optimized.glb`. Their source geometry,
materials, archives and editable masters remain unchanged. Existing Kenney CC0
window and Quaternius CC0 fern rights remain recorded in the
[S2-C asset record](docs/urban-atlas/market-street-s2c/ASSET-RECORD.md).

`validation/reset-final/{fountain,pavilion,bench,cafe-set}.glb` are normalized
exports of existing project-original C1A components, produced through Blender
MCP in the independent `validation/reset-final/civic-reuse.blend`. The approved
`validation/town-square-r0c1a/town-square-design.blend` was not overwritten.
Runtime civic-material batching preserves the selected visible source triangles. The detached fountain caption is omitted from this placement; its source GLB and the sculpture/basin remain unchanged. Small paving,
arrival guard and physical reservation-noticeboard details are original interface
work. No new pack, external texture or architecture was acquired.

The terrain shelf and vegetation changes are reversible scene data behind both
localhost `dev-town=s2f` and `town-layout=reset-final`; no source landscape asset
is replaced. Glass B is the explicit development selection; A remains available.
See [provenance and hashes](validation/reset-final/provenance.json),
[site measurements](validation/reset-final/site-validation.json) and
[owner-review record](docs/urban-atlas/reset-final/REVIEW.md).
No public deployment or owner visual approval is implied.

## Transit Kingdom — development-only CC0 population

The accepted RESET-FINAL terrain, four building transforms, fountain, pavilion,
circulation and landscape composition remain unchanged. An additive opt-in
`town-props=cc0` layer adds **17 imported model types / 42 placements**: 16 selected
Kenney Furniture/Food models and the existing Quaternius fern. Repeated meshes use
27 instanced geometry/material batches. The delivery GLB is **117,052 bytes**, with
8 shared materials and one embedded atlas; no source archive or approved GLB changes.

Both Kenney archives were downloaded through the official free flow and their
bundled CC0 notices verified. Existing Quaternius provenance is retained.
[Asset rights, hashes and inventory](docs/urban-atlas/town-population/ASSET-RECORD.md)
· [Matched real-game screenshots and results](docs/urban-atlas/town-population/REVIEW.md).
This layer requires localhost plus the existing development-town flag and
`town-layout=reset-final`; it is default-off and unavailable on public origins.
No public deployment. Owner visual approval remains pending.

## R0-C2 Atlas Guild: local development landmark

An independent editable Blender derivative reuses the C2A portal, shading,
glazing, materials and lantern concept for the accepted new-town 10 × 8 m site.
The new roof-integrated lantern replaces the old tall shaft; the obsolete tree-cut
roof is rebuilt as a complete limasan roof. Both original Guild reference masters
remain unchanged. The entrance carries actual mesh lettering: “ATLAS GUILD” and
“Balai Riset · Transit Kingdom”.

`assets/game/atlas-guild/atlas-guild.glb`: **1,527,656 bytes**, **14,697 triangles**,
**16 static batches/materials**, **zero textures**, no transmission pass. It uses
one existing cached loader and the existing game renderer/controller. No new
external asset, archive, font binary, NPC, research finding or terrain edit.
[Source and license record](docs/urban-atlas/atlas-guild-r0c2/ASSET-RECORD.md) ·
[Actual browser evidence and measured results](docs/urban-atlas/atlas-guild-r0c2/REVIEW.md).

Requires localhost and the existing populated-town flags plus
`town-guild=r0c2`. Default/public experience remains unchanged. Removing that flag
restores the accepted populated town and reservation noticeboard. One existing
research-panel interaction at the door opens the authentic `transit` study.
Owner visual approval pending. No public deployment.

## R0-C3 Pelabuhan Awan / local opt-in

`validation/skyport-r0c3/pelabuhan-awan.blend` is the editable skyport master.
`assets/game/skyport/pelabuhan-awan.glb`: **731,580 bytes**, **14,600 triangles**,
**eight static batches/materials**, **zero textures/transmission**. Existing cached
GLTFLoader, one scene/renderer and original explorer/controller are retained.

Selected local Kenney Furniture Kit 2.0 CC0-1.0 meshes: `bench.glb`,
`pottedPlant.glb`, `cardboardBoxClosed.glb`, `lampSquareCeiling.glb`, two placements
each. Existing project-authored pavilion piers/shoes and C1/S2A palette reused;
site-fitted curved canopy, braces, identity fascia/mesh lettering and boarding
inlays are original Blender geometry. No downloads, new source archive or paid asset.
[Exact selected files, hashes and licenses](docs/urban-atlas/skyport-r0c3/ASSET-RECORD.md).

Requires localhost, accepted town/props/Guild flags and **`town-skyport=r0c3`**.
Removing this flag restores the accepted town and Guild with no skyport request.
The 13 m original platform, spawn, terrain, vegetation, shop/Guild coordinates,
fountain/pavilion and 17 CC0 types / 42 earlier placements remain unchanged.
No functioning transport, flight, new island, quest or portfolio redesign.
[Actual game evidence, measured costs and rollback](docs/urban-atlas/skyport-r0c3/REVIEW.md).
Owner visual approval pending. No public deployment.
