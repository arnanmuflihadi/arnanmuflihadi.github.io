# Revised performance measurements (P2-A closeout)

## 0. Correction first

The P2-A figures called "GPU-synchronised" used `gl.finish()`. **In Chromium `finish()` does not wait for the GPU.** Measured on the same frame, same machine: no sync 1.8 ms, `finish()` 1.6 ms, a 1 x 1 `readPixels` read-back **10.8 ms mean / 6.1 ms median**. The P2-A frame times (0.6–2.4 ms) were therefore CPU submission time and **under-reported the frame cost by roughly 5x**. All numbers below use the read-back. Evidence files from the invalid method are kept and labelled: `baseline-p2a/evidence/performance.json` and `evidence/performance-swiftshader-UNSYNCED-invalid.json`.

## 1. Conditions

* **Machine A:** Apple M4 Pro (12 cores), WebGL 2 via ANGLE/Metal, Claude desktop app's built-in browser (Chromium 156), pane visible, device pixel ratio 1, render target 1280 x 720 unless stated. `evidence/performance-m4pro-synced.json`, `performance-scaling.json`.
* **Machine B (the only "lower-performance configuration" available):** the same Mac's CPU running **SwiftShader** (software Vulkan/WebGL, `--use-angle=swiftshader-webgl`, headless Chrome 157), 1280 x 720, 12 frames per configuration. `evidence/performance-swiftshader.json`. This is not a low-end GPU; it is a pessimistic bound that is raster-bound instead of GPU-bound.
* **No integrated-GPU laptop, phone or older discrete GPU was available.** A measurement on the intended minimum-spec device is still owed and is a gate for the whole-town budget (see 07). Nothing here should be read as a frame-rate promise for other hardware.
* Frame = fixed 60 Hz simulation step + render + read-back, 240 frames walking the street with the real controller (`walk`), plus 90 renders with a read-back (`synced`). Times in ms.

## 2. Slice with the Exchange Hall (machine A)

| Configuration | Draw calls | Triangles (renderer.info) | Walk frame mean / p95 | Synced render mean / p50 / p95 / max | Programs |
|---|---|---|---|---|---|
| As loaded, shadows off | 335 | 418,295 | 4.46 / 5.5 | 4.38 / 4.2 / 5.6 / 5.9 | 24 |
| As loaded, **shadows on** (4096 map) | 335* | 418,295* | 6.40 / 8.4 | 5.92 / 5.7 / 7.6 / 9.9 | 50 |
| Merged by material, shadows off | **123** | 418,591 | 3.45 / 4.5 | 3.46 / 3.4 / 4.6 / 4.8 | 50 |
| Merged, **shadows on** | 123* | 418,591* | 5.62 / 6.6 | 5.73 / 5.6 / 7.4 / 8.2 | 50 |

\* The counter does not include the shadow pass (shown earlier: identical with shadows on and off). Shadow cost is read from frame time: **about +1.5–2.3 ms** (+35–60 %).

* **Frame time:** 3.5–6.4 ms on machine A, i.e. 150–290 frames per second equivalent. Merging by material saves 0.9–1.0 ms and 212 draw calls.
* **Triangles (unreduced kit):** 418k drawn in the whole-slice view; +103k against P2-A (315k) of which the Exchange Hall is 90.2k (five modules); see 2b for the final kit (308.5k). The slice's placed total is 399,157 triangles (`scene_triangles`); 19k more are the character, ground and sky.
* **Textures:** 72 images (87.98 → 89.98 MB estimated GPU with mips; the Blender report says 94.4 MB, a different formula); 73 glTF materials in the kit with 58 distinct names (the Blender report's signature-merged count is 60; 56 in P2-A), 86 three.js material objects in the scene once the character, ground and instanced paving are included.
* **GLB:** 21.3 MB (P2-A 15.1 MB): +6.2 MB: the hall geometry and its textures' share, plus the `_AO` attribute (4 bytes per vertex, 428,675 vertices = 1.7 MB). The split between the two was not measured separately.

## 2b. Final kit: module LOD for the two heaviest repeated modules (machine A, synced)

P1.4's own feasibility study named two modules as the largest triangle contributors: the exterior brick corner (3,102 triangles, 51 in the town) and the wall lantern (2,822, 46). The kit export now collapse-decimates their templates before any archetype is built (corner brick → 400, lantern → 700; `--no-lod` exports the unreduced kit). Visual check at 1–2 m on the junction house, the hall porch and the inn: the quoin stones keep their silhouette and texture; the difference is not visible in the matched crops (`visuals/lod/`).

| | Unreduced kit (section 2) | **Final kit (module LOD)** |
|---|---|---|
| Kit triangles (17 + 5 nodes, each archetype once) | 347,241 | **239,571 (−31 %)** |
| GLB | 21.3 MB | **17.4 MB** |
| Triangles drawn, whole-slice view | 418,295 | **308,503 (−26 %)** |
| Draw calls as loaded / merged | 335 / 123 | 335 / 123 |
| Synced frame, as loaded, shadows off / on | 4.38 / 5.92 ms | 4.39 / 5.91 ms |
| Synced frame, merged, shadows off / on | 3.46 / 5.73 ms | **3.02 / 5.43 ms** |
| 4K output, merged, shadows on | 17.69 ms | **12.62 ms** |
| 1080p / 1440p | 7.12 / 11.04 ms | 6.49 / 8.37 ms |

The triangle cut matters when the GPU is fill/vertex-bound (4K: −29 %) and little at 720p on this GPU, where submission dominates. Per node: hall main 37,502 → 22,450, wings 14,058 → 8,654 each, porch 11,196 → 5,792, A11 corner house 49,394 → 28,358, inn 46,447 → 31,395, DRESSING 53,678 → 26,092. `evidence/performance-m4pro-lod.json`, `performance-scaling.json` (final kit); the earlier file `performance-m4pro-synced.json` is the unreduced kit. The software-rendered run in section 4 was made on the unreduced kit (418k) and was not repeated.
Scale/placement re-run on the final kit: all 9 buildings within 0.5 cm of the P1.4 envelopes, kit bounds within 0.005 cm, orientation 3/3.

## 3. Sensitivity on machine A (unreduced kit; the final-kit figures are in 2b) (merged, shadows on)

| Output size | Synced mean ms | p95 |
|---|---|---|
| 1280 x 720 | 5.54 | 6.1 |
| 1920 x 1080 | 7.12 | 8.6 |
| 2560 x 1440 | 11.04 | 13.7 |
| 3840 x 2160 | **17.69** | 20.6 |

| Shadow map (1280 x 720) | Synced mean ms |
|---|---|
| off | 3.73 |
| 1024 | 5.59 |
| 2048 | 5.61 |
| 4096 | 6.17 |

The slice is fill-rate sensitive (cost grows ~3x from 720p to 2160p) but still ~56 fps-equivalent at 4K on this GPU. The map size matters little here (0.6 ms between 1024 and 4096); on a smaller GPU, 2048 should be the default and 4096 an option. The cost of having shadows at all (1.8–2.4 ms) dominates the choice of map size.

## 4. Software-rendered configuration (machine B)

| Configuration | Draw calls | Walk frame mean ms | Synced mean ms | First render ms |
|---|---|---|---|---|
| As loaded, shadows off | 335 | 841 | 902 | 5,396 |
| As loaded, shadows on | 335 | 1,141 | 1,166 | 8,148 |
| Merged, shadows off | 123 | 1,010 | 1,009 | 1,145 |
| Merged, shadows on | 123 | 1,249 | 1,167 | 1,419 |

About **1 frame per second**: a CPU rasteriser pushing 418k triangles at 720p, 150–200x slower than machine A. What it shows: (1) cost is raster-bound, not draw-call-bound, so merging does **not** help here (it even slowed the shadows-off case by 20 %, which is within the run-to-run spread of 12 frames); (2) shadows cost +30 % there; (3) the first frame costs 1.1–8.1 s because 50 shader programs must be compiled (see 5). It is not a usable frame rate (expected of a CPU rasteriser) and says nothing about how a real low-end GPU would behave; it is a stress bound only.

## 5. Material compilation stutter

First render after a configuration change, machine A: **225–279 ms** when the program set is new (24 programs without shadows; 50 with shadows), **9–16 ms** once warm. Machine B: 1.1–8.1 s. Spikes of 22–50 ms in the earlier unsynchronised runs coincided with these first renders. A shader pre-warm (render once with shadows off and on, behind a loading screen, before the first visible frame) removes the stutter at the cost of the load time shown; the slice does not do this yet (P2-B task).
The AO and Neutral tone-mapping injection adds **no extra programs**: all standard materials share one `customProgramCacheKey` (24 → 50 programs is the shadow variants, as in P2-A).

## 6. Geometry merging behaviour

`P2A.setMerged(true)` merges every placed mesh by (material) with world transforms baked: 335 → 123 draw calls, triangles unchanged (418,591 vs 418,295, +296 = the instanced paving counted differently), geometry count 246 → 357 (merged copies are additional while the originals stay hidden; a production loader would drop the originals), frustum culling off for the merged meshes. Merging helps CPU submission (−0.9 ms here) and is neutral for raster cost. For the whole town merge **per district** so culling still works.

## 7. What is not measured

* AO's own cost (the code is always compiled in; a run with `?ao=0` still executes the multiply). Expected negligible; not isolated.
* Memory use (JS heap, GPU memory) beyond the texture estimate.
* Mobile/touch devices, battery-power throttling, 4K at DPR 2, long sessions.
* Any low-end GPU.
