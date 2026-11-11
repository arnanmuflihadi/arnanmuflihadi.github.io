# S2-G integrated town stabilization

**Implementation and evidence collection complete. No deployment. Glass A remains the default. Owner approval is pending.**

[Local game](http://127.0.0.1:4173/index.html?experience=adventure&dev-town=s2f&town-review=1) · [Evidence gallery](index.html) · [Rollback](ROLLBACK.md) · [Sources](ASSET-RECORD.md)

## Changes

The four buildings, world coordinates, terrain, source GLBs/Blender masters, renderer, camera, player controller and original collision functions are preserved. The same localhost-only, default-off feature flag is retained.

- Relocated **four original trees**, **one palm with its ten fronds**, and **seven individual small plants**. Each follows existing natural ground. Trunks/crowns stay paired, and tree collision proxies move with their trees. No vegetation batch is removed or reduced.
- Clipped **91 of 28,063 grass blades** where individual blades crossed actual paving or enclosed building space. Four chunks retain correct near/far LOD selection; original attributes and indices remain intact for rollback. This removes 728 near-LOD or 104 far-LOD triangles across the affected chunks.
- Applied explicit back-face shadow casting to **17 solid stone/paving/base meshes**, reducing the conspicuous diagonal shadow banding on stairs. Material colors, roughness, global sunlight, exposure and shadow-map settings are unchanged. No architecture, retaining geometry, foundation elevation or decorative objects were added.
- Inspected the existing terrain-scribed footings and structural supports. Their approved ground contacts and support geometry were retained. Clearing intersecting vegetation makes these interfaces more legible.

The complete instance/blade ledger is in `validation/town-s2g/clearance-ledger.json`. It contains 25 adjusted instanced primitives (eight trunk/crown entries, ten fronds and seven small plants), one palm-trunk object, and 91 blade identifiers. No unresolved placement was returned by the clearance survey. This is not a claim that every possible forest-view intersection has been exhaustively inspected.

## Glass comparison and recommendation

All views use the existing game, identical camera tuples, daylight, geometry, resolution and renderer settings. No new textures or environment lighting were introduced.

| Option | Actual material treatment | Appearance / recommendation |
|---|---|---|
| **A: authored, default** | Exact original physical material, transmission about 0.96; 556 glass triangles | Retains the approved tinted, refracted/softened interior appearance. Keep as default until owner chooses otherwise. |
| **B: stylized alpha** | Shared standard PBR material; source tint × 0.48, opacity 0.18, roughness 0.19, metalness 0.12, front faces, depth-write off; zero transmission | Crisper interiors and less optical depth. **Recommended performance compromise for owner review**, not automatically installed as the default. |
| **C: hybrid** | Original transmission on 132 café-front triangles; B on 424 remaining triangles | Preserves the close frontage but still incurs the scene-wide transmission pass. No compelling performance advantage on this route. |

An earlier opaque-looking alpha trial was rejected during inspection and refined before the final comparison. Its exploratory files are retained separately; the gallery shows the final low-opacity version.

At the fixed café view, actual WebGL draw invocations were **A 468** (168 shadow + 145 transmission + 155 canvas), **B 323** (168 shadow + 155 canvas), **C 470** (169 + 145 + 156). B removes the extra framebuffer pass; merely reducing transmission polygons in C does not remove it.

## Final performance measurements

Final buffer-sharing implementation; no background tests running during the measurements. Apple M4 Pro / ANGLE Metal / Chrome 156. Standard quality, antialiasing on, DPR 1, **1280 × 656 drawing buffer**, 1280 × 720 full capture, PCFSoft 2048 shadows, ACES exposure 0.96, camera far 1600. No quality or glass changes are hidden in these measurements.

The same 60° arrival-to-square camera rail runs after a two-second warmup, with a twelve-second sample and the existing explorer at the same natural-ground position. All passes are counted. Disabled means the town is detached while resources remain cached.

| Scenario | Samples | Frame median / p95 | CPU render median / p95 | Draw-call range | Submitted triangle range |
|---|---:|---:|---:|---:|---:|
| Town off | 1,123 | 11.1 / 16.7 ms | 0.7 / 0.9 ms | 138–150 | 2.341–2.362 M |
| Town on, A | 790 | 16.6 / 17.9 ms | 3.7 / 4.5 ms | 283–587 | 2.596–4.144 M |
| Town on, B | 959 | 11.2 / 17.0 ms | 1.5 / 1.8 ms | 283–390 | 2.596–2.731 M |
| Town on, C | 772 | 16.6 / 22.1 ms | 3.7 / 4.5 ms | 284–589 | 2.596–4.143 M |

B reduced peak submitted triangles by about 34% and median CPU render submission by about 59% relative to A in this run. Frame timing improved in the final run, but timing varied across repeated runs; these are local observations, not a guaranteed FPS increase or a mobile benchmark. CPU submission is not GPU time; GPU timer queries were not measured.

All four unchanged town exports still total **11,084,692 body bytes**. The library retains six cached/requested files, including the existing island tree/fern; glass and clearance switches require no new model or texture requests. There are no missing textures or new image textures.

A final ownership audit removed unnecessary preview-buffer duplication. Incremental retained typed arrays fell from **10,148,280 bytes to 280,968 bytes**: 277,632 for filtered grass indices and 3,336 for hybrid glass indices. Approved position/normal/UV/color buffers are now shared, and remain owned by their source. These are measured CPU-array lengths, not GPU or browser-process memory. No source buffers are edited or released by the subset cleanup.

## Real gameplay and regression

The existing animated explorer completed the same main route with A, B and C: about **69.6 m in 33.1 s** each. Default A also completed the complete reverse route. The first material-study walking samples were A 16.4 / 22.2 ms median/p95, B 11.2 / 17.5 ms, C 15.7 / 22.2 ms. Those walking comparisons preceded the ownership-only buffer deduplication; they are retained separately from the final camera table above. Final default forward/return traversal was repeated after that cleanup.

Guard and jump tests passed: the lateral guard stopped the explorer, and the jump test recorded one takeoff and one landing. No large support discontinuities or unexpected falls occurred on the normal routes. The original 9.5 m follow camera remained in use; no clipping was observed in the recorded traversal views. Arbitrary free-camera angles are not exhaustively covered.

- **85/85 unique relevant regression checks passed.** After the final ownership cleanup, the six S2-F/S2-G integration tests were rerun and passed without warnings. They verify exact off-state instance/count/position restoration, both grass LODs, borrowed-buffer ownership, original source bytes, A/B/C materials, and production-controller traversal in both directions at 20/30/60 Hz.
- Default reload: **one game canvas/renderer**, no review UI, only the original tree, fern, explorer, resident and jump-animation GLBs; no town-model requests.
- Editorial/adventure switching, Work, its six-study registry and the MBR research panel remain available in the actual browser.
- On/off and glass switches retain the same scene UUID and renderer. No second scene, renderer, controller or movement system is introduced.
- Current browser checks report no errors or warnings. A transient bundled-material-constant warning was corrected before final captures and tests.
- The broad static audit still reports **58 inherited findings** concerning old footer/hero/manual-fallback expectations. Its script and audited pages are unchanged; this audit is not claimed as passing.

Full logs and camera/performance/controller records are under `validation/town-s2g/`. Earlier S2-F and approved art evidence are not overwritten. Matched-camera checks cover arrival, market, return, foundations, island and A/B/C glazing.

## Remaining review items — three maximum

1. **Owner glass choice:** B is recommended for reduced rendering cost; A remains default. B loses refractive softening and can show transparent-pane sorting limitations from unusual interior angles.
2. **Minor shading limits:** oblique plaster/roof shadow aliasing and dark upper façades remain. The major stair/paving banding is corrected; no broad lighting or architecture redesign was authorized here.
3. **Coverage:** mobile/lower-end hardware, GPU timing and exhaustive manual camera sweeps remain untested before any deployment decision.

No new district, square, Guild, skyport architecture, NPC expansion or gameplay system was built. **Stop for owner approval.**
