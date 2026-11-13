# P2-A performance and budget reconciliation

> **Correction (2026-11-12, P2-A closeout):** the frame times in this document were taken with `gl.finish()`, which does not wait for the GPU in Chromium; they are CPU submission times and under-report the frame cost about 5x. Counts (draw calls, triangles, textures, materials) are unaffected. Revised measurements: [closeout/05-performance.md](closeout/05-performance.md). The proposed budgets in section 4 are superseded there.


## 1. Measurement conditions (read first)

* One machine: Apple M4 Pro, 12 logical cores, WebGL 2 through ANGLE/Metal, in the Claude desktop app's built-in browser pane (Chromium 156), pane **visible** during every measured run, devicePixelRatio 1, render target **1280 x 720**.
* Measured in the real preview with the real controller/camera/character: a 240-frame walk down the street at 60 Hz, each frame simulated, rendered and waited for with `gl.finish()`; plus 90 synchronised renders for GPU-inclusive time. `autotest=perf`, results in `evidence/performance.json` (two full runs were made; the second is quoted, the first agreed within noise on counts and differed on spikes).
* **This says nothing about integrated GPUs, laptops on battery, phones or a 4K display.** Frame times of 0.4–2.1 ms on an M4 Pro mean "the slice is not expensive on a fast GPU"; they cannot be extrapolated into an fps promise. Budgets below are therefore stated in counts (draw calls, triangles, texture MB), which transfer between machines.
* p99/max values of 22–34 ms appear in the runs that compile new shader programs (shadows on, merged scene): first-use shader compilation, not steady state. They are reported, not hidden.
* No post-processing, no MSAA control beyond the renderer default, no real-time tools such as Spector/GPU profilers.

## 2. Results

| Configuration | Draw calls | Triangles (renderer.info) | Walk frame mean / p50 / p95 ms | GPU-synced render mean / p95 ms | Programs |
|---|---|---|---|---|---|
| As loaded (194 meshes), shadows off | 268 | 315,093 | 0.77 / 0.6 / 1.1 | 0.57 / 0.8 | 18 |
| As loaded, **shadows on** (one 4096 x 4096 directional map) | 268* | 315,093* | 2.13 / 0.9 / 16.7 | 0.95 / 1.7 | 38 |
| Static-merged by material, shadows off | **91** | 315,093 | 0.38 / 0.3 / 0.6 | 0.73 / 0.7 | 38 |
| Merged, shadows on | 91* | 315,093* | 1.50 / 0.4 / 1.1 | 1.07 / 0.7 | 40 |

\* `renderer.info` reports the same numbers with shadows on and off, so the shadow-pass submissions are **not visible in it** (the counter reflects the main pass). Shadow cost appears only in frame time
(roughly 2x on the walk mean). The shadow pass re-submits the casters, so real draw calls with shadows are higher than shown; I did not isolate the figure and do not claim one.

Merged = one `Mesh` per (kit node group x material) built by baking world transforms; frustum culling is off for those meshes (a cost for a bigger town; P2-B should merge per district, not per scene).
Textures: 69 images, ~88 MB estimated GPU with mips (see 3); 194 geometries, 68 material objects.

## 3. The four definitions that were disagreeing

### Triangles

| Name | Value | What it counts |
|---|---|---|
| **P1.4 "unoptimised"** (10-technical-feasibility) | 968,466 for 24 buildings and all dressing | Blender loop-triangles per archetype x every instance in the full masterplan |
| Kit unique triangles | 257,007 | Sum over the 17 GLB nodes (each archetype counted **once**) |
| **Slice placed triangles** | 308,947 | Scene traversal: each node triangle count x number of placements (8 buildings, 4 stall rows, cross, terrace, podium, arches, 674 paving tiles, 87 dressing pieces) |
| **renderer.info main pass** | 315,093 | What WebGL was asked to draw this frame: placed triangles + character, ground, stand-in hall and sky (+6,146) |

Rule for budgets: **use the renderer.info figure for the camera's view and the placed figure for the scene**. They differ by the non-kit objects only. The P1.4 968k figure is the whole town; the slice holds 8 of its 24 buildings and
reaches 32 % of it, consistent with the P1.4 projection (532k after substitutions for the full town) being the number that is still reachable. Nothing in the slice contradicts it; a full-town count is a P2-B measurement.
Not all triangles are in view: this 315k is the *whole slice drawn*, and the aerial view (all of it visible) is the worst case.

### Materials

| Name | Value | Meaning |
|---|---|---|
| Blender material slots, merged archetypes | 169 | Before signature merge (same texture set and constants = same material) |
| Blender after signature merge | 56 | Reported in `kit-report.json` |
| **glTF materials in the GLB** | 68 | 55 distinct names; the other 13 are duplicates of the same name across kit nodes (A03, A04, DRESSING each carry their own copy) |
| three.js material objects | 68 | One per glTF material; GLTFLoader does not de-duplicate across nodes |
| WebGL programs | 18 (no shadows) / 38–40 (shadows) | Shadows add depth/distance programs per material variant |
| P1.4 "distinct materials" | 59 | Planning count by base name |

Rule: **count distinct material names for design, glTF material objects for loading cost, programs for compile time.** A material cache in the loader (key = name + textures) would take the 68 objects to 55 with no visual change; that is a P2-B task.

### Draw calls

Per mesh x material primitive: 268 as loaded (194 geometries; some with several material primitives; 674 tiles in 3 `InstancedMesh`; 87 dressing pieces merged into one DRESSING node of 28 primitives). After merging by material: 91. The remaining 91 are bounded by materials rather than by object count, as P1.4 predicted ("depends on materials, not building count").

### Texture memory

| Name | Value |
|---|---|
| Source resolution (as downloaded, 2048 px maps) | ~828 MB GPU if loaded as is |
| P2-A policy (tier 1: base 1024, ORM 512, normal 512; tier 2: 512/256/256) | **92.3 MB** by the Blender report, **88.0 MB** by the in-engine estimate (w x h x 4 x 4/3); 4 % apart; the two estimators use different formulas and were not reconciled further |
| GLB file | 15.16 MB (embedded JPEG/PNG, one kit file so textures upload once) |
| `renderer.info.memory.textures` | 74–75 (69 images + shadow map, environment, character, etc.) |

The tier policy cut texture memory by 9x; no visible loss was found in the parity comparisons; the effect of the 512 px normal maps was not isolated.

## 4. Proposed budgets for P2-B (slice-proven, whole-town to be re-measured)

| Budget | Proposed | Basis |
|---|---|---|
| Draw calls in view | ≤ 150 after per-district merge (91 slice-wide today) | measured merged result; town ~3x slice if built the same way |
| Triangles drawn in the worst view | ≤ 700k (slice 315k whole) | town is ~3x the slice; ≤ 532k expected after P1.4's own substitutions; keep headroom |
| Distinct material names | ≤ 70 (55 now) | programs grow with materials |
| Texture GPU memory | ≤ 150 MB (88 MB now) | tier policy kept |
| GLB total on disk | ≤ 60 MB | 15 MB for 8 buildings x 17 archetypes |
| First-load parse (this machine) | 107–175 ms for the 15 MB GLB | measured `load_ms`, decode of textures included lazily; slower elsewhere |

These are proposals for approval, not guarantees; the town needs its own measurement on a slower device before they are fixed.

## 5. Recommendations from the numbers

1. Ship **merged-by-material per district** for static architecture; keep `InstancedMesh` for tiles and repeated small props.
2. Keep **one shadow-casting sun** (4096 here; test 2048 on slower GPUs); shadow cost is the largest single item (2x frame time) and affects every material variant (+20 programs).
3. Add a loader **material cache** and warm the shaders before the first frame (the 22–34 ms spikes are compile hitches).
4. Measure a low-end GPU / 4K DPR 2 / battery laptop before P2-B starts; the numbers here cannot.
