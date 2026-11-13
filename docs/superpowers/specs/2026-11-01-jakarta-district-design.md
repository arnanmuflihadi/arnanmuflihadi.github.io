# Phase 2 Jakarta district integration

The user-supplied Phase 2 brief is the authorized design and implementation scope.
Approved Phase 1.5 components may now be integrated, but a completed environment
still requires human review. This document records implementation choices within
that brief, not a new approval gate. No deployment, commit or new game region.

## Spatial design

Keep the existing 88 m conceptual play bounds, plaza at (0,10), arrival at (0,28),
station west of the plaza and business center east. Builder choices: four enhanced
commercial buildings face the 6 m avenue at z=-12 from a shared frontage at z=-20;
a 6 m secondary street at z=-36 bounds the rear of those blocks. Three enhanced
neighborhood buildings face east onto a 4.5 m lane at x=-14, with frontage x=-20
and centers z=21,28,35. The approved office faces the plaza from (23,8.5 frontage).
The west park lies between transit, the plaza promenade and the neighborhood lane.
Existing public research pavilion stays in the southeast. Background imported
office/building instances outside the play bounds establish the skyline.

Paving, support heights, roads, ramps, building placements and collision transforms
come from shared metre-scale records. Preserve the station's current +11 m shift
and its 5..7 m access ramp. Entrances are external research approaches, not enterable
interiors. Existing character physics, animations, project registry and mode/history
synchronization remain authoritative. Existing optional story code is retained,
without adding or expanding quests, monsters or equipment commerce.

## Art and content

Use the unchanged architecture design system and verified four-file GLB library.
Cache variants; batch repeated meshes across placements. No major box-built visual
buildings. A custom vaulted station uses genuine imported glazing/entrance modules;
the pavilion retains its authored roof with imported façade modules. Occupied
shop windows use original shallow display geometry and intentional painted room
textures, not complete interiors. Physical sign textures fit the sign aspect,
use higher resolution, mipmaps, restrained anisotropy and strong contrast.

Grounded trees, purposeful seating, cycle parking, shelter, lamps, drains, bins and
café furniture occupy furnishing zones, leaving continuous footways. Warm daylight,
a gradient sky, soft shadows and restrained depth haze preserve painterly geometry.
The page's established paper/forest/bronze interface remains; no protected game art.
Design Read: a walkable tropical research neighborhood, with the station and office
as orientation anchors. ENERGY 2 / RHYTHM 2 / MOTION 1 for review controls.

## Verification and stop

Add eight fixed review viewpoints to the existing integrated adventure route,
not another standalone page. Capture a before set before replacing scenery and an
after set from identical camera settings. Also exercise actual third-person input,
research selection, return to editorial, history and restoration. Measure frame
intervals, draw calls and triangles in the running district, including device,
viewport and quality. Never infer FPS from the showcase.

Run all existing tests, keep the 16 asset/architecture/character assertions, and add
real imported-district collision and route coverage. Classify the five inherited
failures explicitly; migrate obsolete coordinate assertions to declared current
surfaces and fix actual support/render discrepancies. Compare the static audit with
the saved 58-finding baseline; do not suppress it. Preserve manifests and source
archives. Deliver screenshots, provenance, technical results and measured resource
implications. Human visual target remains average 4/5 with no criterion below 3/5;
no self-awarded score. Stop after this district.
