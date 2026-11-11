# R0-C1C — Settlement circulation repair

**One reversible development proposal, delivered for owner review. No public deployment or R0-C2 work.**

[Before/after gallery](index.html) · [Local playable review](http://127.0.0.1:4173/index.html?experience=adventure&dev-town=s2f&terrain-study=c1a5&town-square=c1b&circulation=c1c&town-review=1) · [Blender derivative](../../../validation/circulation-c1c/circulation-design.blend) · [Interfaces GLB](../../../validation/circulation-c1c/circulation-interfaces.glb) · [Court GLB](../../../validation/circulation-c1c/circulation-square.glb) · [Asset record](ASSET-RECORD.md)

## Diagnosis and correction

The rejected C1B network reached the court by going north, crossing the raised civic walk, then returning south. Its forecourt bench and planting blocked the obvious direct entrance despite a level difference of only **0.814 m**. A parallel garden ramp, civic stairs and several landings competed with the square. At natural arrival, the old bridge crossed the actual spawn **1.213 m above ground**; its tested stair entry was about **9.49 m away** from that spawn.

Three focused repairs address those failures:

1. **Direct civic entrance.** Five stone risers at **0.1628 m**, over **1.62 m**, join the forecourt at Y22.614 to the court at Y21.800. Nominal width is **2.8 m**. The bench moves to the eastern seating edge; its accompanying town tree/bed and selected flower clumps move out of the desire line. Reused signs shrink to 65% scale. The old ten-riser civic detour and redundant garden ramp are removed. The existing north eleven-riser flight remains an optional return.
2. **Actual natural arrival.** A short terrain-scribed gravel fan joins the original dirt trail at **(27,57)** to six **0.1525 m** risers and a visible stone landing. This replaces the disconnected thirteen-riser entry, provisional platform and 8.8 m bridge. The route joins the preserved garden connector at **(30.15,51.8)**. No full skyport is built.
3. **Deliberate branches.** The existing court/highland steps connect to the original clearing trail through a short stone/gravel transition, replacing the parallel dirt ribbon. Four **0.1483 m** risers and a ground-following path lead from the court toward the **Guild reservation boundary (44,−8)**. No Guild architecture is implied.

The fountain, pavilion, four buildings, foundations, terrain vertices, ridge and waterfall remain intact. Guards are retained on exposed drops. New closed stone reuses C1B's back-face shadow convention to remove stair-face striping, without changing lighting, exposure or glass. [Measured plan and exact inventories](../../../validation/circulation-c1c/circulation-plan.json).

## Distances, levels and clearances

Identical endpoint comparison: upper forecourt **(35,12.6)** to lower court **(26.2,12.6)**, direct horizontal separation **8.8 m**. The unchanged real controller walked **34.48 / 34.46 m** before and **8.68 / 8.68 m** after, out/return at 60 Hz. This is approximately **75% shorter**, with **six intermediate turns reduced to zero**. The earlier C1B 25.3 m figure used different endpoints and is not used for this comparison. [Controller comparison](../../../validation/circulation-c1c/route-comparison.json).

| Connection | Nominal width | Minimum body-clear estimate | Level transition |
|---|---:|---:|---:|
| Natural arrival gateway | 3.00 m | 2.32 m | +0.915 m / 6 risers |
| Direct forecourt–court | 2.80 m | 2.59 m | −0.814 m / 5 risers |
| Court–Guild garden gate | 2.40 m | 2.08 m | −0.593 m / 4 risers |

Clear widths come from 5 mm transverse scans against actual height-filtered colliders at five sections, using the existing 0.34 m controller radius and 1.9 m body height. They are clearance measurements, not traversal proof. Original max-step remains **0.42 m**; no movement tuning is changed. [Site measurements](../../../validation/circulation-c1c/site-measurements.json).

The natural highland-junction branch measures **25.53 m** with a maximum sampled ground grade of **33.36%**; the ground branch toward Guild peaks at **32.10%**. These are steep exploration routes, not accessible paths. The higher ridge is unchanged and its previously reported 41.8% section lies beyond this junction test. [Branch grade samples](../../../validation/circulation-c1c/natural-branch-grades.json).

## Actual gameplay verification

All live walks use the original animated explorer in the existing game. Only the starting position is placed; there is no waypoint teleporting during a walk.

| Live route | Out / return distance | Result |
|---|---:|---|
| Natural arrival → market → court → highland junction | 94.52 / 94.54 m | PASS both ways |
| Court → Guild reservation boundary | 31.03 / 31.08 m | PASS both ways |
| Direct civic entrance | 8.71 / 8.71 m | PASS both ways |
| Court guard, fountain basin, retained market edge | Collision stops the explorer | PASS |
| Market jump and landing | One launch, one landing | PASS |

Primary and Guild walks have **zero unplanned air height and zero support-seam events**. The follow camera retracts to **1.57 m** on the primary journey and remains functional; this close view is retained for review. [Live records](../../../validation/circulation-c1c/live-traversal.json).

Fixed-step checks pass all **18 runs** for journey, portal and Guild, both directions at **20/60/180 Hz**. Maximum actual support rise/drop is **0.1743 m**, with no airborne frames. The optional northern return was separately walked with the real controller at 60 Hz in both directions, **32.32 / 32.30 m**, without air gaps; this extra loop check is Node-based, not an additional live browser walk. [Route records](../../../validation/circulation-c1c/controller-routes.json), [optional loop](../../../validation/circulation-c1c/optional-loop.json).

## Visual evidence

Six matched pairs are actual browser renders at **1280×900**, drawable **1280×836**, DPR 1. Camera/quaternion/FOV and quality match exactly in each pair. Eye-height market, direct entrance and return views are 1.65 m above their floors; the trail-arrival camera is 1.82 m above sampled ground. The plan is an actual orthographic game view at **80 m vertical span**, with a 10 m scale bar and separate annotation layer.

1. [Scaled network](../../../validation/circulation-c1c/01-network-after.jpg): primary blue, optional green, removed red, relocated props amber; all public hardware inventoried in JSON.
2. [Natural arrival](../../../validation/circulation-c1c/02-trail-arrival-after.jpg).
3. [Market toward square](../../../validation/circulation-c1c/03-market-square-after.jpg).
4. [Direct entrance](../../../validation/circulation-c1c/04-direct-entrance-after.jpg).
5. [Court back toward market](../../../validation/circulation-c1c/05-square-return-after.jpg).
6. [Oblique network](../../../validation/circulation-c1c/06-circulation-oblique-after.jpg).

The gallery includes the six original matched views. [Pair audit](../../../validation/circulation-c1c/capture-match-audit.json). A separate [actual Blender render](../../../validation/circulation-c1c/blender-direct-stair.png) verifies the native derivative; Cycles lighting differs from the browser and is not substituted for game evidence.

Visual inspection confirms an open direct entrance, visible fountain sculpture, fewer competing paths and a legible highland branch. Architecture, palette, landscape atmosphere and existing public-space proportions are preserved. This is a circulation correction, not a claim that the settlement matches finished concept art or has received human artistic approval.

## Geometry, loading and performance

| Independent derivative | GLB bytes | Triangles | Mesh primitives / materials | Texture references |
|---|---:|---:|---:|---:|
| Shared interfaces | 471,680 | 7,924 | 17 / 17 | 0 |
| Court and connections | 1,037,056 | 17,670 | 14 / 12 | 0 |
| Total | **1,508,736** | **25,594** | 31 primitives | 0 |

These replace 2,040,416 bytes / 27,714 triangles of active common-interface/square geometry. A further **1,390 selected original market triangles** are reversibly hidden, and one town tree is moved using its two existing instance components. Public circulation inventory reduces **587→293 elements**, including rail members/posts **410→172**. No complete vegetation group is removed. Approved market GLB remains **10,007,904 bytes**, unchanged. [Export measurements](../../../validation/circulation-c1c/export-metrics.json).

On Apple M4 Pro / ANGLE Metal, four real browser samples use the same market-to-fountain camera rail, 2 s warmup + 12 s measurement, standard quality, PCF soft shadows, exposure 0.96 and **Glass B**. A/C remain available.

| Run order | Frame median / p95 | CPU submission median / p95 |
|---|---:|---:|
| C1B before | 5.6 / 11.2 ms | 0.8 / 1.0 ms |
| C1C after | 7.0 / 11.4 ms | 1.1 / 1.4 ms |
| C1C warm | 5.6 / 11.2 ms | 0.8 / 1.0 ms |
| C1B warm | 5.6 / 11.2 ms | 0.8 / 1.0 ms |

C1B submits **322–410 draws / 2,657,232–2,760,754 triangles**; C1C **335–431 / 2,649,690–2,753,554**, including shadow and canvas passes. New material batches add draws despite fewer triangles. rAF intervals and CPU submission are not GPU timings; the warm results do not establish zero overhead. [Full performance record](../../../validation/circulation-c1c/performance-comparison.json).

The two new requests transfer **1,509,336 bytes including response overhead**, with 1,508,736 encoded/decoded body bytes. The comparison deliberately preloads both C1B and C1C for instant rollback: cache **nine requests / nine loaded files** remains stable across toggles, so review memory includes both variants. No missing new textures, errors or warnings were recorded. Fresh default-off behavior is tested separately.

## Regressions and preservation

**22/22 scoped regressions pass:** 16 inherited S2-F/G, terrain and C1B checks plus six circulation checks. Coverage includes protected assets, actual controller paths, visible surface/support agreement, terrain accuracy, reversible furniture/instance/collision restoration, jump/landing and three guard/fountain barriers. [Log](../../../validation/circulation-c1c/regression.log).

```
node validation/circulation-c1c/test-routes.mjs
node --test tests/circulation-c1c.test.mjs validation/circulation-c1c/inherited-regression.mjs
```

Terrain ray/sampler error remains **1.95e−14 m**; nine visible imported stair/landing samples agree with gameplay support to **3.56e−15 m**. No hidden floor is introduced. [Height verification](../../../validation/circulation-c1c/height-verification.json).

**3,458 of 3,462 checkpointed files are unchanged.** Only existing `entry.js`, `town-integration.js`, `town-square.js` and `town-review.js` changed. New circulation/plan modules and all derivative/evidence files are separate. Approved GLBs, native masters, source licenses, controller, renderer/world construction, terrain, research registry and portfolio pages remain byte-identical. Inherited regression outputs are redirected to this phase's folder. [Preservation](../../../validation/circulation-c1c/preservation.json).

Town OFF restores original terrain, original prop geometry/instances and obstacles while retaining the same scene and one renderer. A fresh page with circulation/square parameters but **without `dev-town=s2f`** has no review panel or town GLB requests. `project=mbr`, adventure/editorial switching, Home/Work and all six study links were checked in the browser. [Default-off evidence](../../../validation/circulation-c1c/default-off.json), [Work index](../../../validation/circulation-c1c/work-index.json), [live rollback](../../../validation/circulation-c1c/town-off-restoration.json).

## Rollback and remaining issues

- **C1B before** immediately restores the accepted C1B circulation, selected furniture and tree. Remove `circulation=c1c` and reload to avoid both new GLBs and the plan JSON entirely.
- **Town off**, or removing `dev-town=s2f`, restores the original public island. The exact localhost gate remains unchanged; no deployment command was run.
- Pre-change copies of the four edited game files and the hash checkpoint are in `validation/circulation-c1c/pre-change/` and `before-hashes.json`. Do not reset the unrelated working tree.

Maximum three remaining review issues:

1. The fountain's sculpture is visible from the lower market approach, but its basin becomes fully legible nearer the forecourt. Essential retained market guards and the 1.57 m camera retraction still deserve owner visual review.
2. The primary route uses stairs; no continuous step-free route is provided. Natural highland/Guild branches remain steep, and this phase does not validate the entire ridge beyond the tested junction.
3. Material batches add 13–21 draws on the measured camera rail. Warm frame timings are similar, but lower-end/mobile performance is untested. No unrelated optimization is attempted.

**STOP for owner approval. No Guild, full skyport, new storefronts, terrain reconstruction, NPC gameplay, public deployment or R0-C2 work.**
