# R0-B1.5 — Gameplay-first town layout

Status: **owner visual approval pending; stop before R0-B2**.

[Playable preview](../town-layout-r0b15.html?build=R0-B1.5.review#context) ·
[Review gallery](town-layout-review/index.html) ·
[Measured terrain](town-layout-review/terrain-survey.json) ·
[Native browser journeys](town-layout-review/navigation-browser.json).

## Decision

Recommend **A, Central Plaza Hub**. Arrive at Pelabuhan Awan, follow the paved
market approach, discover the shared square, then choose the Atlas Guild or the
highland trail. A meadow bypass returns to the skyport; the longer natural circuit
passes Cloudbreak and returns to the square. Five commercial envelopes face shared
public space. The Guild's crown is visible from arrival, market and square in the
terrain/massing sightline checks. No MRT is required.

| Alternative | Core bounding area | Ground range under footprints | Footprint above 35% terrain grade | Gameplay assessment |
|---|---:|---:|---:|---|
| A — Central Plaza Hub | 1,744 m² | 14.1–23.0 m | 48.7% | Readable arrival/reveal, short branches, shared enclosure, clear Guild crown. Local terraces still necessary. |
| B — Terraced Hillside Town | 1,596 m² | 15.8–32.1 m | 73.8% | Strong skyline and vertical exploration; longer uphill arrival and repeated retaining structures compete with the hillside. |
| C — Curved Market Loop | 3,125 m² | 12.6–31.7 m | 52.5% | Good optional circuit and serial discoveries; dispersed frontages, weaker central focus and separate Guild spur. |

All options use the actual support mesh: 1 m footprint sampling, 0.5 m slope
baseline and 0.4 m route sampling. Bounding areas exclude the common skyport and
wilderness circuit. A wins on terrain compatibility and destination grouping,
not merely smallest area. Diagrams share the same island scale and north direction.
Qualitative judgments are internal design recommendations, not human approval.

## Reversible implementation

- Dedicated `town-layout-r0b15.html`; production does not import this layer.
- Square: 20 × 18 m, top 22.3 m; arrival platform: 18 m diameter, top 17.15 m.
- Primary commercial route: 6 m; arrival approach: 5 m; secondary links: 3–4 m.
- Six planning envelopes: five commercial masses, 7–12 m high, and a 16 m Guild
  body with a distinguishable crown. Source prototypes are preserved, not replaced.
- Entrance markers: 2.4 × 2.9 m; canopy underside approximately 3.11 m. Every
  threshold has visible support connected to public paving. Interiors are unbuilt.
- Exact rendered triangles provide floor support; height-aware solid proxies
  protect the masses. The existing player, jump physics and follow camera are used.
- Toggle restores original instance matrices/counts, palm visibility, both grass
  detail index buffers and collision arrays. Disposal is idempotent. Terrain
  positions are unchanged. Eight production hashes and both R0-B1 source archives
  match the recorded baseline.
- Guild approach offers the real transit study; its shelves link all six existing
  research projects, including MBR. No NPC, quest, merchant or transport system.

## Fresh validation

`node --test tests/*.test.mjs`: **102 passed, zero failed/skipped**. This includes
all 96 previous tests and six new layout regressions covering alternatives,
restoration, thresholds, actual capsule traversal, production preservation and
grass distance-detail changes. [Full output](town-layout-review/tests.txt).

All six native browser checks completed: skyport → market, market → square,
square → Guild, square → highland, Cloudbreak return and meadow → skyport.
The first four and meadow used walking; Cloudbreak return used running.
Recorded grounded support error and blocked time were zero. One Space-triggered
jump and landing passed. Route-bearing assistance only steered heading; actual
native W/Shift+W drove the existing character. Explicit start controls placed each
check at its checkpoint. These are not claims of an independent unguided playtest.
Unassisted Q turning and D strafing also passed at the square.
After the final visual-only soil-edge trim, a targeted repeat passed market →
square and the first 33.7 m of the highland route with zero blocked time/support
error. The complete earlier six-route record is retained separately from this
partial repeat in `visual-correction-smoke.json`.

Actual moving distances: approximately **37.3, 16.6, 19.4, 130.5, 190.3 and
70.3 m** respectively. Moving times exclude inspection pauses. The natural ridge
reaches 48.7 m support and includes existing grades up to 71%; it is playable with
this controller, not an accessibility-compliant route. No unreachable sampled
sections were found. Camera distance contracted to 4.57 m on the scenic return;
no obvious camera clipping appeared in inspected views.

Static audit: **58 inherited findings, byte-for-byte identical to R0-A3's audit**.
It remains failing; this phase does not claim to fix unrelated footer, analyst
image or static-map fallback findings. [Output](town-layout-review/static-audit.txt).

## Visual inspection

The gallery contains the eight requested real browser views, a side/underside
check and a matched layer-off/on context comparison. Desktop captures are
1280 × 720; canvas 1280 × 658. Pedestrian views use 1.65 m support-relative eyes,
60° FOV and unchanged R0-A3 lighting. No generated concept image is evidence.

Context and pedestrian passes corrected: disconnected paving joins (one shared
sloping forecourt), an unsupported side threshold, M5's conflict with the meadow
route (moved 1.5 m), grass returning through paving after distance-detail changes,
and a coplanar soil/paving overlap at the square's trail exit. The Guild approach
camera was widened at the same eye height. Prior context and traversal images are
retained as intermediate evidence; final images use numbered filenames.

Internal observations across the eight rubric categories: the compact massing
leaves hills/geology legible; frontages share a centre; paving distinguishes the
town from natural trails; measured branches and loops are connected; the mineral
and teal planning palette remains intentionally simple; approved atmosphere is
unchanged; the route graph is original; actual character/door scale is shown.
Finished facade richness, detailed streetscape and final architectural identity
are **not evaluated as complete** in a greybox phase. No human score is awarded.

## Resources and limitations

No additional GLB payload or texture files. Two existing landscape templates are
cached/loaded; the existing character and authored jump clips also load. Six
envelopes are original planning volumes, not imported final architecture. Browser
diagnostics report no missing textures and console warnings/errors were empty.
`inventory-browser.json` distinguishes authored landscape placement totals from
view-specific draw counts; masked vegetation is not claimed to remain all visible.
The final planning layer adds 31 draw meshes, 14,057 potential triangles and
15 materials, with zero new textures. Existing landscape placement totals
(134 trees, 678 ground ferns and 24 cliff ferns) describe the authored island
before reversible town masking, not an active rendered-instance claim.

Final standard-quality walking sample: **600 moving frames, 180.0 fps average,
5.8 ms walking p95, 69 draw calls, 1,152,162 triangles**, 1280 × 658 drawing buffer
(effective DPR 1 in this session), shadows enabled. Mean CPU render submission
0.345 ms; this is not GPU timing. Geometry memory counters: 132 geometries,
6 textures, 25 programs. Costs are view/session-specific; the town context has
different draw counts. The longer ridge sample also recorded 600 moving frames
at 161.7 fps, 59 calls and 1,131,698 triangles before the final cosmetic edge trim.
Both runs are retained in `walking-performance*.json`; no comparison against
older different-device/DPR FPS is made.

Remaining: blank massing faces, large raised podium backs, no interiors, simple
skyport envelope and sparse planned square furnishing. Final roofs/planting may
change sightlines; recheck them during approved architecture work. Unguided owner
playtesting and artistic approval remain outstanding. **Do not start R0-B2.**

## Files and references

New scene: `assets/js/town-layout/{plan,blockout,views,showcase}.js`,
`assets/css/town-layout.css`, `town-layout-r0b15.html`.
Evidence: `docs/town-layout-review/`, this report, `scripts/record-town-layout.mjs`,
`tests/town-layout.test.mjs`. `ASSET_MANIFEST.md` records the temporary scope.
Installed skills and existing game files were not recreated or migrated.

[Nintendo's Skyloft overview](https://zelda.nintendo.com/skyward-sword-hd/world/):
high-level landmark orientation. [Folio zones](https://github.com/brunosimon/folio-2025/blob/main/sources/Game/Zones.js)
and [interaction points](https://github.com/brunosimon/folio-2025/blob/main/sources/Game/InteractivePoints.js):
proximity-based content access independent of movement.
[Sky Isles](https://github.com/stas4000/sky-isles): connected discovery destinations
as described by its README; its world source could not be retrieved. No external
code or assets were copied. Attached concept boards informed destination grouping;
their embedded older production prompts did not expand this phase's authorization.
