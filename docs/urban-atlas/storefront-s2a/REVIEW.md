# S2-A: Kopi Awan architectural art prototype

One original two-storey tropical shopfront, built and inspected through live Blender MCP. No town, island or production website changes. Human visual approval remains pending; S2-B/C/D have not started.

## Review files

- [Native Blender project](../../../validation/storefront-s2a/kopi-awan-prototype.blend), active scene **S2-A Tropical Storefront**. Earlier S1 scenes remain as reference data; only one S2-A building was authored.
- [Street-level view](../../../validation/storefront-s2a/01-street-level.png), 1500×1200, nominal eye height 1.65 m, 37 mm lens.
- [Elevated three-quarter view](../../../validation/storefront-s2a/02-elevated.png), 1500×1500, 45 mm lens.
- [Façade and roof detail](../../../validation/storefront-s2a/03-facade-roof-detail.png), 1500×1200, 44 mm lens.
- [Measured geometry and camera transforms](../../../validation/storefront-s2a/geometry-and-cameras.json).
- [Component attribution](ATTRIBUTION.md).

All three are actual Cycles renders from Blender, 64 samples with denoising. Lighting uses warm directional sunlight, cool world fill and restrained interior bounce lights. No image generation, atmospheric concealment or façade overlays. Lighting and interior bounce are presentation settings, not promised browser lighting.

## Architecture and reuse

The original generated floating-town concept was accessible in S1's `references/` folder and inspected again. Its shaded balconies, warm plaster, natural timber and terracotta roof family informed this prototype. The sign “Kopi Awan” is original fictional architectural lettering, not an operating shop or new game interaction.

The body is 7.2 m wide and 8.55 m deep. The balcony projects to approximately 9.4 m overall depth. The roof, including its overhangs, measures about 8.74×10.44 m; maximum height is 8.81 m. Roof dimensions intentionally exceed the approximate body dimensions to provide tropical shade.

- Real 220 mm plaster wall shells have modeled window/door openings and welded junctions.
- Recessed 1.56 m entrance bay, timber door frame, brass pulls, fixed transom and low threshold. The leaf zone is approximately 2.4 m high. This is a static art prototype, not an animated or collision-tested door.
- Bronze-framed shop glazing, a simple visible café interior and a contrasting stone plinth establish a commercial ground floor.
- Upper floor near 3.5 m, timber balcony with approximately 1.1 m clear rail height, planted troughs, shaded sliders and angled timber screen blades.
- Roof is custom-authored hip geometry with lifted corners, real terracotta tile courses, fitted hip covers, curved fascia and a raised ventilated ridge. A thin brass crest supplies the restrained fantasy accent.
- Licensed Kenney frame geometry is reused in six side/rear windows. Quaternius fern geometry is instanced in the four integrated troughs. No unmodified library building was used.

Collections separate Shell, Joinery, Roof, Terrace, Interior, Streets, Landscape, Props, Collision References and Cameras. Editable Bevel, Solidify and Array modifiers retain control of thicknesses, edge treatment, decking and screen rhythm. Major architecture uses custom wall/opening meshes and lofted roof surfaces; small beams, frames and fixtures use simple native solids. Collision References is empty: no playable/collision-certified prefab is claimed.

## Visual QA and corrections

The first elevated and street-level renders are retained under `validation/storefront-s2a/first-pass-*.png`. Review found three major issues and corrected the underlying geometry/materials:

1. **Opaque-looking glazing and weak entrance identity:** increased glass transmission, reduced tint, added restrained interior fill, a timber-framed entrance transom and threshold. The door is now distinguishable from the display bays.
2. **Exposed wall grid seams and misplaced side windows:** welded wall vertices before thickness/bevel evaluation, corrected side-wall orientation, rotated imported window frames properly, fitted their scale to the openings and added glazed inserts/sills. Lower side glazing now reaches its intended sill.
3. **Discontinuous eave and floating hip caps:** rebuilt fascia to follow the curved roof profile, fitted segmented hip caps to the roof surface, added ridge-vent supports and modestly strengthened roof pitch. The final detail camera includes the complete ridge cap.

Final views were visually inspected at pedestrian, overall and detail scales. The shell now reads as a designed building rather than a greybox; warm plaster, timber, terracotta, metal and glass are differentiated. This is a provisional internal observation, not a human quality score or artistic approval.

## Validation and export suitability

- **46,940 evaluated building triangles**; **52,894** in the full presentation scene including plants, ground and reference geometry. Counts include evaluated modifiers and converted lettering.
- **295 mesh objects**, 303 total scene objects, 19 used materials. These are Blender inventory counts, not measured Three.js draw calls. Separate editable details are the primary delivery inefficiency.
- Two used images, 256×256 fern leaves and 512×512 Kenney palette, are populated and packed. No missing image datablocks found. No negative-scale building objects detected.
- Native file saved and reopened successfully through live Blender MCP, with `S2-A Tropical Storefront` active and 303 scene objects.
- **1,260 production/source files unchanged** against this phase's starting hash baseline. [Preservation evidence](../../../validation/storefront-s2a/preservation-check.json). No unrelated production test suite was run because no production implementation changed.

Expected glTF compatibility is good for solid mesh geometry and standard Principled base color/roughness/metallic materials. Apply/evaluate supported modifiers for export, convert lettering to mesh, consolidate by material and retain clean object origins. Export Blender Z-up through the normal glTF Y-up conversion once. Keep an editable native master before consolidation.

Transmission glass requires glTF material-extension support and a suitable Three.js lighting/environment setup. A cheaper opaque/alpha glass alternative may be preferable for multiple storefronts. Rendered transmission/reflections will not transfer identically. No GLB export, browser load, browser draw-call measurement, walking test or collision validation was performed in S2-A. The native art prototype is not yet a delivery-optimized game prefab.

## Known issues / next approval boundary

The presentation is deliberately restrained; wood and plaster use clean color/roughness separation rather than baked painterly surface variation. Fine tile courses can alias at distance and should receive a roof LOD or bake later. Side-window frames retain the source's simpler design language. The shallow interior is staged for the glazing; stairs, full upper-floor access and interior gameplay are not modeled. The apron is an isolated display ground, not a connection to island terrain.

Any future storefront variants should keep shared floor/door modules, balcony depth and roof construction while varying signage, opening rhythm and roof proportions. No variants or full street were made here. Stop for owner visual approval before further phases.
