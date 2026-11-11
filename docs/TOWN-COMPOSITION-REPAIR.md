# Transit Kingdom — R0-B1.5 composition repair

Owner visual review is pending. This is a reversible, playable greybox proposal;
R0-B2 has not started. The previous layout's technical passes did not establish
visual acceptance.

## Diagnosis of the rejected views

- **Arrival:** M5's rear wall occupied the approach axis. The path bent behind it,
  and only a small part of the Guild crown appeared above unrelated slabs.
- **Market:** five large commercial masses did not create a repeated, two-sided
  street frontage. The eye-height camera faced a mixture of side walls and ends.
- **Square:** the very tall Guild slab and individual access wedges overwhelmed
  the small visible public floor. There was no convincing gathering-room shape.
- **Aerial:** large separated footprints and podiums read as demonstrations rather
  than a compact connected settlement.

The rejected screenshots and camera records remain in `town-layout-final/` and
are copied, without alteration, into this repair's comparison gallery.

## Repaired composition

The arrival now sweeps gently east into a 28 m commercial spine. Eight smaller
envelopes form four opposing frontage pairs. M1 steps back to keep the oblique
arrival vista open; M3/M5/M7 share the west building line and M2/M4/M6/M8 the east
line. Heights range from 5.8 to 8.4 m above their street floors, with simple gable
and setback roof volumes. Recessed ground floors and porch piers communicate
frontage depth and entrance orientation without constructing finished facades.

The street opens into a chamfered **328 m² square**. A flush 4.2 m circle reserves
a future focal point; it is not a fountain or a new gameplay object. A clear
**7 × 10 m** central rectangle remains usable. M9 faces its northern edge and
M10 marks the western trail gateway. The Guild occupies the northeast end: two
lower wings, a recessed civic entrance, a layered hall roof and a single higher
observatory mass. The Guild is a greybox landmark, not a finished asset.

One mineral-paved route is dominant; the quieter meadow loop remains gravel.
The trail gateway bends around M10 and reconnects to the unchanged highland and
scenic return. Terrain was not flattened or regenerated. Street and threshold
levels share a common section; lower building volumes extend to surveyed ground.

## Browser evidence and correction passes

[Gallery](town-composition-review/index.html),
[camera records](town-composition-review/captures.json),
[matched-camera checks](town-composition-review/comparisons.json).

The first repair pass exposed an overly tall Guild, a gap at the chamfered plaza
corner, and overlapping meadow/connector surfaces. The Guild was reduced, a
continuous paved gateway added, and duplicate shared surfaces removed. Shared
paving receives a small depth bias at coplanar junctions; no postprocessing or
landscape lighting change conceals geometry.

The last rendering correction removes the Guild ribbon's folded section over the
already supported square, aligns the arrival's end section with the market and
keeps fine paving joints on the level gathering reserve. Thin walkable surfaces
receive building shadows without casting overlapping surface shadows themselves.

Six decisive fixed views cover arrival, market, square, Guild, trail and island
aerial. Extra context and labeled top-down browser views show the complete street
and optional loop. All are actual **1280 × 720** browser captures, standard
quality, **1280 × 658** drawing buffer and effective DPR 1. Pedestrian views use
**1.65 m** above actual support and **60° FOV**. Daylight and exposure 0.96 are
unchanged.

Four comparisons retain the exact old absolute camera pose, rotation and FOV.
The old square camera now sits under the west arcade and looks away from the
relocated Guild; that obstructed comparison is retained, not presented as an
improved plaza view. The decisive new square view stands on the repaired street.
Cloud phase and staged character placement can differ between historical images.

## Traversal, measurements and regression

[Native route samples](town-composition-review/navigation-browser.json),
[navigation summary](town-composition-review/navigation-summary.json),
[rendered-geometry camera audit](town-composition-review/camera-audit.json),
[full survey](town-composition-review/measurements.json).

Native W/Shift+W drives the existing third-person controller. Bearing assistance
steers only heading; no automated locomotion or hidden browser teleport is used.
The final continuous check covers skyport → market → square → Guild → square →
highland, with a real Space jump and landing. Separate checks cover the scenic
return, meadow return and all ten commercial entrance markers. Unassisted strafe,
turn, walk, backward movement and jumping are recorded separately. Guided checks
are controlled validation, not independent owner playtesting.

After the final surface correction, Market Street → Square and Square → Guild
were rechecked with native W input. Both completed with zero recorded stationary
input time and zero grounded support error. Their samples are appended to the
four comprehensive journey records.

Route lengths, actual movement times, slopes, minimum clear widths and elevation
transitions are in the linked records. Urban clear-width sampling requires actual
rendered paving, not just a line on a plan. All eleven plots are sampled at 0.5 m
including their boundaries. Sightlines target three actual heights on the Guild,
rather than only a tip above the skyline; foliage is additionally checked visually.

**106 regressions pass, none failed or skipped**, using
`node --test tests/*.test.mjs`. The ten town checks remain; the old exact-six-masses
assertion now requires ten small commercial envelopes, and the full-solid Guild
assertion now checks its solid wings and open porch. Terrain restoration, source
hashes, controller traversal, support, thresholds, grass restoration, clear widths,
square capacity and the actual follow-camera ray test remain enforced. All other
architecture, character, landscape, asset and integration tests are preserved.

The static audit still has **58 inherited findings**. It is not reported as a
clean audit. [Test output](town-composition-review/tests.txt),
[audit output](town-composition-review/static-audit.txt),
[production/license checks](town-composition-review/preservation.json),
[browser portfolio check](town-composition-review/portfolio-preservation.json).

## Assets, resources and performance

No new GLBs, textures, external code or dependencies. R0-B1 source models, source
archives, licenses, loader/cache and production scene remain unchanged. The
preview loads **11 planning envelopes** (10 commercial and one composed Guild),
**zero architecture GLBs**, two existing landscape GLB templates and the existing
1.9 m character. Greybox geometry totals **11,936 triangles, 41 meshes, 31 geometry
resources, 17 materials, zero textures**. The character has 15 meshes and 10,202
triangles. Existing character/animation and tree/fern files total **2,672,840 bytes**;
this is bundled payload size, not HTTP transfer. Existing manifests retain source
filenames and license provenance.

Relative to the rejected preview, planning geometry adds nine mesh objects and
eleven geometry resources, keeps the same material count and removes 1,941
triangles. It adds no asset payload. View-specific landscape visibility and camera
position prevent treating the old and new draw counters as a matched benchmark.

The final active-walking town sample records **93 draw calls**, **1,114,449
triangles**, **600 moving frames**, approximately **150 fps** and **11.2 ms p95**
on this browser session. CPU render submission averages **0.348 ms**; it is not
GPU time. Renderer counters show six textures and 22 programs. The ridge sample
has a different visible scene and is not a matched performance comparison.
These results are not a mobile-device benchmark.

[Town timing](town-composition-review/performance-walking-town.json),
[ridge timing](town-composition-review/performance-walking-ridge.json),
[loaded inventory](town-composition-review/inventory-browser.json),
[asset footprint](town-composition-review/asset-footprint.json),
[browser errors/warnings](town-composition-review/console.json).

## Remaining limits and owner gate

- Upper walls, roof forms and entrance markers are deliberately unfinished
  planning volumes; they do not match the finished concept art's facade richness.
- Downhill building backs still require lower mass/support up to approximately
  7.2 m. Their final terraces, retaining structure and architecture are unapproved.
- The Guild ramp reserves gameplay access; it is not a finished civic stair.
  Temporary terrace edges lack permanent railings. No accessibility certification
  is implied by the gameplay measurements.
- The preserved highland trail remains steep. It was not flattened to improve
  the town's statistics or screenshots.
- The optional meadow junction narrows to 1.2 m in the conservative cross-section
  survey; its connector reaches a 32.5% three-metre grade. The actual character
  completed both directions, but this remains a narrow secondary route. The
  arrival measures 6.6 m minimum and the market 8.0 m.

Changed implementation: `assets/js/town-layout/{plan,blockout,survey,views,showcase}.js`,
`town-layout-r0b15.html`, two scope-dependent town test assertions,
`scripts/record-town-composition.mjs`, `ASSET_MANIFEST.md` and this new evidence
folder. No production terrain/controller/camera/model files were modified.

**STOP for owner visual approval before R0-B2. No human score is self-awarded.**
