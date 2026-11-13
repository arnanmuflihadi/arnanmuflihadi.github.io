# Phase 1.5 architectural design system

Focused final correction ready for human review, 1 November 2026. The preceding
three-building visual review was not approved. Target average human score: 4/5.
The current correction has no human score or approval. The full district remains paused.

## Architectural direction

The reference vocabulary comes from climate-responsive Indonesian architecture:
[Andramatin's AD Premier](https://www.andramatin.com/project/ad-premier/) uses deep
strips and a planted ground composition;
[HMP's Indragraha Office](https://www.hmparchitects.com/indragraha-office-1) describes
layered shading, roof projections and planted terraces;
[TWS's Riverside Office](https://twspartners.com/project/riverside-office/) uses
vent blocks and overlapping terraces. The three Atlas compositions are original
concepts informed by these principles. Reference photographs and model files from
these practices are not included in the project.

Design Read: an architectural asset study for portfolio visitors and visual
reviewers, with tropical shade, mineral surfaces and restrained planting.
ENERGY 2 / RHYTHM 2 / MOTION 1. The main model is the focal point. Before/after
images sit in explicit pairs; material and street views support their evaluation.
The cream paper, forest text and bronze focus accent continue the atlas identity.

## The three variants

| Variant | Massing and roof | Façade rhythm and material hierarchy | Ground floor |
| --- | --- | --- | --- |
| Contemporary Tropical Office | Retains the uniformly scaled 22.4 m imported tower; composed height 23.79 m. Flat parapet, mechanical equipment and a light rooftop pergola. | Six primary concrete fins, secondary mullions and floor-aligned horizontal blades. Imported glass physically set back another 0.22 m. Dark stone base, pale mineral middle, bronze/green roof edge. Two selective planted ledges. The formerly blind side gains shaded glazed ribbons and a service screen. | Broad, recessed lobby glazing, timber accents, cantilevered entrance canopy and original TERAS ATLAS nameboard. Clearance above porch: 3.06 m. |
| Urban Mixed-Use Commercial Building | Retains the source shop's 13.6 m proportions. Composed height 16.21 m including a roof-access pavilion with a 1.95 m door, pergola and planted edge. | Terracotta painted plaster; original brick normal/color/occlusion maps removed from the painted surfaces. Projecting floor bands, a timber screen, a balcony planter and actual hollow roster blocks. Quiet party walls support later rowhouse placement. | Full-width glazed frontage behind a 2.86 m-clear arcade above the porch. Imported raised stoop geometry is clipped away on the enhanced instance. Original RUKO SENJA lettering is applied to the canopy fascia. |
| Human-Scale Neighborhood Shopfront | Source shop cropped to a 4.2 m-wide, 6.2 m-high two-story body while retaining its original uniform scale. A vented clay gable and deep eaves give a composed height of 8.18 m. | Sage plaster, a timber window frame and shutters. Original lower-storey source geometry remains; original project-authored surfaces close the cut sides and rear. | Narrow ground-level glazing and a timber canopy with 2.80 m clearance above the porch. Original RUANG JIRAN stationery signage on the fascia. |

All names are fictional architectural artwork. The scene adds no NPCs, transactions,
transport simulation, monsters or other realms.

## Geometry, materials and resource ownership

The Quaternius GLB files, hashes, licenses, archive verification, scale loader and
original asset tests are retained. The Phase 1 imported baseline remains available
in the comparison views. No source buffer or cached baseline material is modified.

`architecture-design-system.js` clones the affected source meshes before editing.
It clips the neighborhood body and raised shop stoops with interpolated positions,
normals and UVs. Front glazing moves inward on real geometry. The source interior
atlas UVs are remapped for pane-scale, project-authored sky tones. This is an
intentional stylized texture treatment, with modest emissive fill to keep shaded
glass legible. It does not use expensive transmission or screen-space reflections.

The added architecture is real, instanced geometry. Roster blocks use an extruded
shape with an actual hole. The small roof uses sloping surfaces, a ridge, battens
and an open timber gable. Imported ferns and air-conditioning units remain real
Quaternius meshes from the verified existing files. Canopy signs are canvas
textures on physical planes, not interface text over the rendered façade.

Materials distinguish stone, cast concrete, painted plaster, clay, timber, bronze,
glass and vegetation. A small procedural tonal wash provides controlled surface
variation. Existing mapped occlusion remains on appropriate materials; geometry
recesses and a 2048 px soft shadow map provide contact and depth. Rendering happens
on load, view changes and resizing; the review has no animation loop.

The three visible variants total 78,449 architectural triangles, including 7,128
project-authored triangles. Architectural detail is consolidated into 26 instanced
batches plus door, sign and roof surfaces. Four existing GLBs total 6,659,124 bytes;
thirteen actual browser captures total 879,663 bytes and load lazily. These are
measured geometry/file counts, not frame-rate or device-performance claims.

## Focused final correction

The silhouettes and source scale remain intact. Local cuts on enhanced source
instances remove entrance pediment/stoop overlaps; retained source buffers stay
shared and immutable. Interpolated boundary geometry closes the clipped frontage
edges. Actual door planes, transoms, frames and slim pulls establish clear human
scale. The commercial arcade receives a clean central pier/header; neighborhood
glazing receives a clean header. Parapet caps and timber fascia stay within the
existing architectural envelopes.

All porch plates now rise 20 mm above the paving. Above-porch canopy clearances
are 3.06 m (office), 2.86 m (commercial) and 2.80 m (neighborhood), with their
existing collision clearances unchanged. Office glass leaves measure 0.91 × 2.40 m;
commercial leaves 0.98 × 2.20 m; neighborhood leaf 0.98 × 2.15 m. The solid-building
collision behavior is preserved; these are visual frontage details.

Cool cast concrete, warm painted plaster, dark andesite, warm timber, red fired
clay, satin metal and soft reflected sky now use separate finish treatments.
Smooth low-resolution tonal washes avoid photographic noise. Finish clones disable
the vegetation source vertex wear colors while retaining its original maps.

`showcase-daylight.js` defines a shared neutral daytime preset: a 2 × 128 sky
gradient, hemisphere strength 2.05, warm sun strength 2.15, exposure 1 and the
existing 2048 px soft shadow map. Fog starts at 90 m, beyond the inspected assets.
There is no postprocessing. Imported paving receives architectural shadows, with
self-shadow casting disabled to avoid grazing-angle acne. The underlying sidewalk
support sits 15 mm below paver tops; one instanced batch supplies subtle joints.
Soil meets road level. Three thin foundation supports, in one instanced batch,
fill the ground-to-building space under the existing footprints. They add 36
context triangles and no new obstacle or model transform.

Relative to the preceding captured variants, geometry decreases by 564 triangles;
authored triangles increase by 538 and visible mesh batches by 16. Local frontage
edge meshes are built once per cached variant. Procedural base texture data rises
by 35,840 bytes to 44,032 bytes, excluding unchanged sign maps and driver overhead.
The four GLBs, two lights, shadow-map size and on-demand rendering remain. Owned
geometry, materials, textures and the shadow resource have explicit disposal.

## Reuse and collisions

```js
const system = createArchitectureDesignSystem(library, { signTexture });
const office = await system.create('office');
office.position.set(x, groundY, z);
office.rotation.y = heading;
scene.add(office);
const obstacles = system.collisionBodies(office);
```

Variant IDs: `office`, `commercial`, `neighborhood`. The factory caches one generated
prototype per ID and returns separate instances sharing geometry, maps and finishes.
The clone has independent transform and collision metadata. The normalized source
origin stays at the centre; `root.userData.architecture.front` gives the local +Z
frontage offset. The showcase subtracts this offset to align the three frontages.

`collisionBodies()` exports transformed `{x,z,w,d,minY,h}` records compatible with
the existing controller. The source body stays solid, separate columns block at
ground level, and overhead elements use `cameraOnly` with explicit lower heights.
The body proxy follows the revised shop frontage after removal of the raised stoop.
Tests verify clear paths beneath all canopies, building blocking and rotated bounds.

The system and the source model library own the shared resources. Keep both alive
while any instances use them; remove those instances before disposing the system
and library. The binary source/optimization pipeline remains unchanged. Enhanced
variants are reproducible runtime compositions; no new composed GLB export is
claimed in this phase.

## Gallery and evidence

The showcase retains its eight original views and adds five pedestrian inspections.
Before/after pairs use precomputed union bounds; camera position, quaternion, lens,
aspect, lighting and source scale are identical. The capture route hides review
chrome and fills a fixed 1280 × 720 canvas; it renders the same scene and materials.
Browser screenshots are saved directly. No image-generation or retouching step is
used. Captured camera tuples and scene counts are retained in
`assets/img/architecture-review/scene-evidence.json`.

The five new captures are office entrance, commercial arcade, neighborhood
frontage, sidewalk interface and full pedestrian composition. They share a 1.65 m
eye height above the 0.16 m sidewalk datum, 40° lens, 1280 × 720 viewport and the
same daytime preset. Their camera tuples and actual loaded counts are in
`assets/img/architecture-review/final-correction-evidence.json`. All five saved
images were visually inspected for door proportions, canopy clearance, interface
heights, material separation, clipping and grounded geometry. This inspection does
not assign a human approval score.

The 1.65 m street camera is measured above the 0.16 m sidewalk. No mannequin or NPC
was added to manufacture a scale reference. Use the live collision overlay to
inspect the ground and overhead proxies.

## Human review gate

The technical checks do not award visual approval. Review these five criteria on
a 1–5 scale: Indonesian urban identity, architectural coherence, façade/material
richness, street-level scale and painterly atmosphere. Target average: at least
4/5. Current score: unassigned. Full-district work remains paused until that review.

## Verification result

The asset, character and architectural suites pass **16/16** with unchanged
assertions. Both original/enhanced camera tuples match. All thirteen view controls
and gallery links were exercised, including keyboard Enter and Space, collision
overlay on/off and the diagnostic disclosure. A fresh browser tab has no warnings
or errors; all thirteen gallery images decode and no model texture is missing.
Decoded geometry attribute and transform inspection found no invalid components.
All sixteen collision proxies match the preserved pre-correction capture exactly.
See `docs/architecture-review/final-correction-verification.json` and its browser
and pre-correction collider records. The deliberately failed tree/retry fixture
was verified in the preceding phase and was not rerun during this correction.

The complete office was inspected on a phone-sized viewport. Narrow and tablet
layouts have no horizontal document overflow and controls remain at least 44 px
tall. Desktop review and calibrated gallery captures are separate from these
responsive checks. Temporary overrides were reset.

The preceding broader repository run recorded five district test failures and
58 static-audit findings. Those broader checks were not rerun during this focused
correction. They remain outside this phase and are recorded in the asset manifest.
None of these technical checks assigns a human visual score.
