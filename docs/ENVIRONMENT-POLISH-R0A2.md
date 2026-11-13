# R0-A2: environmental art polish

Historical pre-detail record. Current evidence is in
[R0-A3 landscape detail](LANDSCAPE-DETAIL-R0A3.md).

Implemented in the existing working tree, 2 November 2026. **Human visual review
is pending. No score is assigned. R0-B has not started.**

[Walk the landscape](../index.html?experience=adventure&build=67) ·
[Eight before/after pairs](environment-polish-review/index.html) ·
[Asset manifest](../ASSET_MANIFEST.md)

## What changed

The upper landmass is unchanged: 177.62×183 m, elevation 10.28–49 m, 26,416
support triangles. Every upper vertex/index, 2,000-plus sampled support heights,
six route coordinates and reserved locations match the captured R0-A baseline.
The closed underside retains its −85 m tip; intermediate faces now have localized
ledges, irregular fractures, narrower mineral transitions and smoother tapering
instead of complete shelves around the perimeter.

The sky has a blue zenith, softer horizon and blue lower hemisphere, warm sunlight,
balanced ambient fill, 34 layered instanced cloud cards and four varied distant
island silhouettes. These are background geometry with no collision or travel.
No bloom, volumetrics or new postprocessing is used.

Three cached growth forms reuse the existing imported tree: spreading, emergent
and windswept. Branches and crowns deform together above the lower trunk, with
UVs, maps and original GLB buffers preserved. Forest, meadow and ridge planting
now differs in density and form. Authored understory, varied curved grass blades,
soil-color transitions and painted embedded pebbles enrich the existing paths.
None of these paint effects changes playable height or introduces steps.

| Changed source | Purpose |
| --- | --- |
| `assets/js/floating-atlas/atmosphere.js` | Sky, layered cloud shaders, varied background silhouettes |
| `assets/js/floating-atlas/terrain.js` | Ground color and path masks; closed cliff geology; exact upper mesh retained |
| `assets/js/floating-atlas/nature.js` | Cached growth forms, zoned planting, shrubs, actual ledge attachment, rock bounds |
| `assets/js/floating-atlas/groundcover.js` | New curved grass, shared near/far buffers, distance detail and wind |
| `assets/js/floating-atlas/scene.js` | Daylight balance, materials and environmental integration |
| `assets/js/floating-atlas/entry.js` | Grass quality handoff and actual detail counters |
| `assets/js/floating-atlas/plan.js` | Only three fixed QA cameras, added before baseline captures |
| `tests/environment-polish.test.mjs` | Exact terrain/layout preservation and reusable detail/source-buffer regressions |
| Home/Work HTML and controllers | Cache revision 67, new actual-canvas fallback |

Other active floating modules have cache-version-only changes. The pre-polish
source snapshot is retained in `assets/js/floating-atlas-legacy-r0a/`, never loaded
by production. Original archives, source licenses, loader/cache, player physics,
camera, guide, project registry and research content are preserved.
[Exact module classification](environment-polish-review/changed-modules.json).

## Visual evidence

All sixteen images are unretouched native browser captures at **1280×720**.
Eight pairs match camera position, orientation, FOV, aspect and player placement;
maximum numeric camera deviation is 1.11e−16. Lighting is intentionally changed
by this phase, using one consistent after preset. Cloud drift is not synchronized.
All eight after captures share one world/scene UUID.

| View | Position | FOV | Before / After |
| --- | --- | --- | --- |
| Full aerial | 135,105,175 | 43° | [Before](environment-polish-review/before-01-aerial.jpg) / [After](environment-polish-review/after-01-aerial.jpg) |
| Profile/underside | −145,5,155 | 53° | [Before](environment-polish-review/before-02-profile.jpg) / [After](environment-polish-review/after-02-profile.jpg) |
| Low cliff | −104,−15,57 | 57° | [Before](environment-polish-review/before-03-cliff.jpg) / [After](environment-polish-review/after-03-cliff.jpg) |
| Forest trail | 24,22,45 | 60° | [Before](environment-polish-review/before-04-forest.jpg) / [After](environment-polish-review/after-04-forest.jpg) |
| Mountain ridge | −51,53,−30 | 55° | [Before](environment-polish-review/before-05-ridge.jpg) / [After](environment-polish-review/after-05-ridge.jpg) |
| Overlook | −96,48,23 | 60° | [Before](environment-polish-review/before-06-overlook.jpg) / [After](environment-polish-review/after-06-overlook.jpg) |
| Player view | 29,19.2,65 | 60° | [Before](environment-polish-review/before-07-player.jpg) / [After](environment-polish-review/after-07-player.jpg) |
| Editorial | 108,76,136 | 48° | [Before](environment-polish-review/before-08-editorial.jpg) / [After](environment-polish-review/after-08-editorial.jpg) |

[Camera verification](environment-polish-review/camera-comparison.json).
The separate 1728×874, 60,546-byte WebP fallback is exported from the real canvas;
it is not used as a replacement for these QA screenshots. Older posters remain.

## Verification and cost

**79/79 tests pass, none skipped:** all previous 77 plus two polish regressions.
This retains the asset-foundation, architecture, character, jumping, terrain,
final-obstacle route traversal, camera and cleanup coverage. The new checks prove
exact ground/layout preservation, unchanged source buffers, three growth forms,
distance detail reuse and reduced-motion cloud stability.
[Full log](environment-polish-review/test-results.txt).

Actual native input: W for 5 s moves 10.507 m; S for 5 s returns within 0.008 m;
Shift+W for 2 s moves 9.183 m. Space records airborne takeoff and grounded landing,
counters 1/1. Pause blocks movement and freezes animation time. Reduced motion is
enabled through the real controls and then restored. Eco switches shadows off and
uses fewer detailed grass chunks. Editorial/adventure round trips retain the exact
player position, scene UUID and one renderer. MBR deep linking opens the real study
with its interpretation limits; the complete article and all six Work links remain.
[Browser state](environment-polish-review/browser-checks.json) ·
[Research checks](environment-polish-review/research-checks.json).

Actual local Mac/Chromium 156 measurements below use **600 moving frames** each,
1280×656 canvas, DPR 1, warmed cache. Mean render submission is CPU time, not GPU
time. Draw/triangle counters describe the sampled view, not a universal maximum.

| Moving sample | Mean / p95 | Measured FPS | Calls / submitted triangles | Grass near/far |
| --- | --- | --- | --- | --- |
| Arrival trail, Standard/shadows on | 8.3345 / 8.50 ms | 119.98 | 86 / 1,237,358 | 16 / 15 |
| Forest trail, Standard/shadows on | 8.3355 / 8.40 ms | 119.97 | 77 / 1,201,034 | 17 / 14 |
| Arrival return, Eco/shadows off | 8.3317 / 8.40 ms | 120.02 | 85 / 1,169,094 | 6 / 23 |

Standard arrival submission averages 0.732 ms; Eco 0.456 ms. These views and walks
are not identical benchmark traces, so no percentage speedup is claimed. R0-A's
earlier report recorded 180 FPS/58 calls on a different run; this phase does not
claim a frame-rate improvement. [Raw measurements](environment-polish-review/walking-performance.json).

Environment potential geometry rises **3.53%**, from 1,276,069 to 1,321,126 triangles.
The environment has 73 mesh objects, 61 attached geometries, 33 materials and four
textures, zero missing. Splitting grass into 31 distance chunks increases draw calls
and buffer objects. Near/far levels are prebuilt once and share vertex attributes;
the measured renderer holds 113 geometries, 16 textures and 20 programs including
actors, lighting resources and detail levels. No per-frame geometry is allocated.
The same five active GLBs remain 3,859,228 bytes; all six prior inventory hashes
match, including the inactive architecture GLB.
[Actual counts](environment-polish-review/browser-assets.json) ·
[Inventory and license paths](environment-polish-review/inventory.json).

No browser warnings/errors were captured. The static audit still fails with
**58 inherited findings**, exactly the same text, none added/resolved.
[Console](environment-polish-review/console.json) ·
[Audit comparison](environment-polish-review/audit-comparison.json).

## Review limits and stop

Owner review is still needed for broad low-poly cliff faces, the inherited foliage
texture and crown repetition, sparse ridge planting, smooth upper slopes, distant
grass transitions, cloud silhouettes and the retained narrow waterfall ribbon.
The new atmosphere improves separation but does not imply a human 4/5 rating.
Physical phones, cold-network transfers and GPU frame times are not benchmarked.
No new architecture, playable realm, flight, NPC, quest, monster or shop is added.

Anti-slop remains in **during** mode (user's session instruction). Design read:
existing tropical adventure landscape, olive vegetation, blue atmospheric depth,
warm soil paths and preserved editorial typography. ENERGY 2 / RHYTHM 2 / MOTION 1.
Review gallery controls are ordinary links; motion remains pausable/reducible.

Delivery gates, scoped to the implemented interface and recorded technical work:

- **Block 1 — PASS:** working browser scene, real captures and measurements, no invented assets or approval.
- **Block 2 — PASS:** blue gradients, cloud layering, warm paths and foliage variation serve the owner's explicit environmental brief.
- **Block 3 — PASS:** island/trail focal compositions, restrained motion, paired gallery rhythm and existing atlas identity retained.
- **Block 4 — PASS:** preserved workflows and regressions verified; visual judgments and device limits remain explicit.

These gates are not human art approval. **Stop at R0-A2 for owner review before R0-B.**
