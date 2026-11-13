# R0: The Floating Urban Atlas

The user's complete reboot brief is the approved direction and execution scope.
This is an environment replacement within the portfolio, not a repository rewrite.
Human visual acceptance is separate from engineering verification. No automatic
4/5 score, extra realm, flight, monster, inventory, shop mechanic or quest system.

## Preservation and architecture

Use branch `codex/floating-atlas-r0`. Preserve the Phase 2 world in
`assets/js/urban-atlas/` with its tests, provenance and eight comparison pairs.
Its scene/assembly/layout stay available to tests and the documented legacy
entry, but are not loaded alongside the new island. New environment modules live
in `assets/js/floating-atlas/`. The portfolio mode controller retains one renderer,
URL/history state and the existing study/dialog interfaces.

Generalize the existing player and camera with optional world dependencies,
retaining default legacy behavior. Reuse the actual skinned character, animations,
jump physics, input, GLB cache, architecture prototypes and licensed models.
Only Transit has a constructed research landmark in R0. MBR/CBD and other deep
links select their real studies without inventing a destination or teleport.

## Authored island design

Builder choice: an approximately 130 by 145 m asymmetric island, about 55 m of
modeled tapered rock underneath and 20 m of useful terrain elevation. A radial
triangulated surface follows hand-placed boundary controls and graded area/path
anchors. Physics evaluates the same triangles as rendering. This provides a
compact connected level rather than empty land or randomly noisy terrain.

Area anchors (x,z; approximate surface height): arrival (12,47;10), merchant
(24,18;12), transit (-8,-10;16), highlands (-32,-32;28), overlook (-49,-2;22).
Graded winding routes connect arrival/merchant/transit/highlands/overlook and a
return loop. Imported supporting buildings sit on deliberate terraces. Designed
retaining walls conceal terrain/foundation seams. Overlook and skyport receive
visible rails; unguarded wild edges permit a fall and safe recovery rather than
an invisible wall immediately at the cliff. Saved positions are world-versioned.

Rock walls use irregular strata and tapering offset rings, with sculpted spurs.
Vegetation follows groves, stream banks, cliff ledges and path margins. Warm stone,
copper/clay roofs, sage vegetation and blue-green air unify the original palette.
Layered clouds below the landmass make its floating height legible. A few distant
uninhabited silhouettes imply future journeys, not implemented realms.

## Settlement and identity

Two original landmarks: a terraced transit hall with split sweeping canopies and
imported glazing, and an open highland pavilion with stepped tropical roof forms.
The merchant cluster combines one approved commercial and two small approved
shopfront variants with original market timberwork and differing orientations.
No repeated office-tower ring or rectangular street grid. Real shallow window
displays and physical signs remain part of geometry, not UI scenery overlays.

Design Read: a tropical research settlement carried on a geological sky island;
arrival reveals city, highlands and open sky together. ENERGY 2 / RHYTHM 3 /
MOTION 1 for the interface; dramatic environmental composition comes from terrain,
silhouettes and depth, not animated UI. The established professional interface
stays intact with honest floating-world labels and map.

## Subphases, review and tests

R0-A: preserve baseline, coordinates, interfaces, source digests and tests.
R0-B: build terrain/underside/sky/vegetation, integrate a testable walking surface,
capture aerial/oblique/walking views. Inspect these before any settlement work.
If the terrain remains weak, stop and present that gate for visual review.
R0-C: build terrain-responsive settlement, gateway, transit, highland pavilion.
R0-D: exercise controller/camera/jumps/cliffs, existing dialogue and studies,
editorial/adventure/history, MBR deep link, no duplicate scene/loop.
R0-E: improve real screenshots, performance and cleanup; deliver ten native
browser views plus prior district comparison. Stop for owner visual approval.

Test terrain/support raycasts; graded route reachability; actual imported proxy
transforms; no out-of-island validated spawn; cliff fall/recovery; camera terrain
clearance; ground/run/jump regressions; research mapping; cache/disposal; all old
67 tests unchanged except additive engine dependency injection. Preserve and
compare the 58 inherited audit findings. Measure actual moving-frame intervals,
draw calls, triangles, transfer bytes and browser load time, documenting device
and quality rather than extrapolating from the showcase.

Future travel configuration stores realm IDs, skyport takeoff/landing markers,
airspace and load/unload lifecycle only. It implements no dragon or flight.
