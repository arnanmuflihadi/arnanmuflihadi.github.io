# AR(N)AN: Living Urban Atlas

Implemented on `codex/jakarta-experience`, retaining the existing uncommitted
portfolio work. The current repair adds imported main-street architecture,
project guides and jumping. No deployment or framework migration. See the
[repair report](LIVING-ATLAS-REPAIR.md) for current evidence and the historical
[Phase 3 implementation](LIVING-ATLAS-PHASE-3.md) for the optional encounter.

## Visitor experience

Home and Work immediately present the real Jakarta district behind readable
semantic HTML. Each project chapter coordinates its research preview with an
authored camera composition. The same site header offers **Take control**.
First activation adds the licensed explorer to the existing scene with a small
inline status; subsequent activations reuse it. **Read the atlas** pauses movement,
restores the current study and blends back to its editorial camera.

The district, renderer and character survive these mode changes. Explicit **Walk
here** moves to a safe landmark approach; ordinary **Take control** resumes the
last position. All case-study and map URLs remain conventional links. The study
dialog is shared by chapter inspection and E interaction in the district.

Three Jakarta landmarks correspond to transit accessibility, business clustering
and satellite urban morphology. Food systems, historical paddy screening and
Bandung café research use clearly labeled atlas-pavilion compositions. Those
regions are not constructed. This is thematic urban space, not a digital twin or
a geographic visualization of the research results.

## One scene and one camera owner

| File | Responsibility |
| --- | --- |
| `assets/js/experience-controller.js` | Small entry shim; mounts Home/Work or adds a contextual atlas link on other pages. |
| `assets/js/living-atlas-controller.js` | Mode, scroll, selection, history, dialogs, loading status and shell coordination. |
| `assets/js/living-atlas-state.js` | Validated routes and safe saved state. |
| `assets/js/project-registry.js` | Six case studies, actual map URLs, findings and caveats. |
| `assets/js/project-panel.js` | One native research dialog for both modes; no game progression. |
| `assets/js/urban-atlas/entry.js` | One persistent scene/renderer/camera; editorial compositions or follow control. |
| `assets/js/urban-atlas/presentation.js` | Cinematic targets, safe spawn points and interaction zones. |
| `assets/js/urban-atlas/scene.js`, `architecture.js`, `environment.js` | Authoritative Jakarta construction, lighting and collision. |
| `assets/js/urban-atlas/character.js`, `player-controller.js`, `animation-controller.js` | Genuine skinned GLB, physics root, actual-speed locomotion and crossfades. |
| `assets/js/urban-atlas/licensed-scenery.js` | Progressive local GLB scenery, shared geometry/materials and disposal. |
| `assets/js/urban-atlas/minimap.js` | Conceptual plan from actual collision footprints and player position. |
| `assets/css/living-atlas.css` | Editorial layers, shared header and compact adventure UI. |

The original decorative hero renderers and pinned work rail no longer run on
Home/Work. GSAP remains available for compatible UI effects; native scrolling
owns chapter progress. Mode events coordinate the existing motion lifecycle.
Mobile menu locking suspends scene input and scroll selection; scroll restoration
is immediate so it cannot temporarily select another project.

This remains a static multipage site. A full Home↔Work document navigation creates
a new instance of the same district factory; session storage carries safe player
coordinates. Within a document, editorial↔adventure keeps the identical scene
UUID and renderer. The old `assets/js/rpg/` scaffold is retained as historical
work but is not mounted by the current controller. `urban-atlas.html` remains an
isolated, noindex art-review route using the same scene implementation.

## Character and architecture

The explorer is the actual Quaternius Adventurer: 62 bones, 15 skinned material
primitives and 10,202 triangles. Idle, Walk and Run are authored clips played by
AnimationMixer, with crossfades and playback rates driven by resolved movement.
The 1.9 m visual sits below a stable collision root. Walk is 2.1 m/s; run is
4.6 m/s. Collisions suppress locomotion when movement is blocked. Facing blends
with input; there is no separate authored turn-in-place clip. Phase 3 adds matching authored punches, roll, hit and defeat clips, with the
source sword-idle pose reused as a guard stance. Those clips load only when the
optional story is accepted. Jump Start/Air/Land clips from Quaternius's CC0
Universal Animation Library are retargeted offline onto this rig. A vertical
physics controller supplies gravity, grounding and landing. Transport remains
unimplemented.

The main shop shells, office tower, apartment blocks, entrances and façade bands
now use imported Downtown City MegaKit Standard meshes. Original station vaults,
arcades, canopies, signs, pavilion roof and road composition customize the kit.
Imported planters, canopy trees and ferns add textured vegetation.
Warm plaster, teal glazing, terracotta, tropical palms, soft toon pigment washes,
mapped matte scenery, warm sunlight, fog and restrained motion unify the district.

## Asset provenance and reproducibility

| Delivered asset | Source and license | Size |
| --- | --- | --- |
| `urban-explorer.glb` | [Quaternius Ultimate Modular Characters](https://quaternius.com/packs/ultimatemodularcharacters.html), CC0 | 1,581,480 B |
| `architecture-library.glb` | [Downtown City MegaKit](https://quaternius.com/packs/downtowncitymegakit.html), eleven selected Standard CC0 templates | 5,529,408 B |
| `jump-animations.glb` | [Universal Animation Library](https://quaternius.com/packs/universalanimationlibrary.html), Standard CC0; retargeted animation only | 267,260 B |
| `city-planter.glb` | Same pack, Standard CC0 | 454,776 B |
| `canopy-tree.glb` | [Stylized Nature MegaKit](https://quaternius.com/packs/stylizednaturemegakit.html), Standard CC0 | 719,224 B |
| `fern.glb` | Same pack, Standard CC0 | 104,876 B |

License notices and per-file source/output SHA-256 manifests are adjacent to the
assets under `assets/game/characters/urban-explorer/` and `assets/game/scenery/`.
The source pages and included Standard license notices were inspected. The repair
report records actual requests, instantiated counts and visible screenshot locations.
The architecture library has quantized geometry and embedded maps capped at
512 px (color) or 256 px (normal/ORM). Nature and planter maps remain capped at
256 px. Runtime placement scales assets into the authored layout, and foliage
receives a small diffuse/emissive lift. No Kenney road assets were imported.

Full vendor archives stay outside the published tree. To reproduce scenery,
extract the specified source glTFs and their dependencies beneath directories
named for their packs, along with each `License_Standard.txt`, then run:

```sh
node scripts/prepare-atlas-scenery.mjs --source /path/to/source-root --deps /path/to/node_modules
```

The conversion uses glTF-Transform core/functions 4.2.1 and Sharp 0.34.5 in a
temporary tooling directory. It is an authoring operation, not a runtime or
deployment dependency. The existing character and vendor scripts record their
own pinned workflows. Three.js 0.180.0 and GLTFLoader are vendored locally with
their MIT notice and provenance. Static serving requires no build or packages.

## Progressive enhancement and limits

HTML research is visible before imports resolve. The editorial world does not
load resident, explorer or jump assets. Scenery is progressive; narrow initial
viewports retain the imported architecture but omit the planter download and use
a lower pixel ratio without shadows.
Data Saver skips automatic world loading. Eco quality reduces rendering cost.
Reduced motion snaps editorial compositions and stops environmental oscillation;
essential walking animation remains functional. The guide preference persists.

The renderer stops when the story is scrolled out of view, the document is hidden
or the page is suspended. Scene resources, imported textures and skeletons have
disposal paths, including cancellation during loading. Rendering/import failure
keeps the poster, semantic content, study inspection and ordinary links available.
WebGL context loss exits control and offers a reload; automatic context rebuilding
has not been implemented.

Browser screenshots and unit checks validate this milestone, not a hardware-wide
performance target. No mobile physical-device or Safari/Firefox coverage is
claimed. Four current-district guides and one optional quest/combat encounter are implemented.
Other districts and intercity travel remain unimplemented.
