# 03 — Scalable rendering: merge strategies, memory, compression

## 1. Conditions (read first)

* **One machine:** Apple M4 Pro, the Claude desktop app's built-in browser (Chromium 156, WebGL 2 via ANGLE/Metal), 1280 x 720, device pixel ratio 1. Every GPU-inclusive time ends in a 1 x 1 `readPixels` (the method corrected in the closeout). The machine is shared and heavily loaded (load average 58-73 during the final runs), so each number is the **median of 3 interleaved repeats** with the range shown; differences under about 1 ms between merged modes are inside that range.
* **A stray tab inflates timings.** A first final run was taken while a Playwright tab was still open on the live preview; every time doubled (e.g. 14.7 ms for district merging). The tab was closed and both runs repeated; the tables below are the clean repeats. (The same artefact was found in batch 2.)
* **No lower-end hardware was available.** Nothing here establishes behaviour on an integrated GPU, a phone or an older laptop. The tables separate **draw calls** and **submitted triangles** so a reader can weigh a call-bound or a vertex-bound device; that weighing is an argument, not a measurement.
* Counts are what the renderer was asked to draw (`renderer.info` per camera, shadow pass excluded), not budgets.
* **Surrogates.** Nineteen buildings are built. For the "24-building" scene, five existing kit nodes of similar size stand at the five unbuilt P1.4 sites (B13 and E04, B15 and B16, E05: A09, A11, A11, A11m, A04b; `?town24=1`). They have no collision and are not the final architecture; they exist only so the renderer sees a 24-building town. The 24-building results are therefore an estimate of the finished town, not a measurement of it.

## 2. Strategies compared

* **Unmerged:** one object per placed module (the kit's per-building meshes, one primitive per material), per-object frustum culling.
* **District:** static merge per district x material (batch 2's production mode).
* **Scene-wide:** one merged set; no culling benefit.
* **Spatial cells (new):** static merge by 20/30/45/60 m cell x material. A mesh that fits a cell stays whole in the cell of its centre; ground, paving and district dressing meshes (larger than 0.6 of a cell) are split **by triangle centroid** into the cells; frustum culling stays on each cell mesh. `loader.js: mergeByGroup(cellSize)`, `splitMeshByCell`.

> **Correction (P2-B batch 4, 2026-11-12):** the two tables below labelled the 45 m row "new default" while the shipped default has been 30 m cells (`p2a.js`: `merge: 'cell30'`; `production-config.json: merge_default`; section 5 of this document). The label was a leftover of an earlier draft. The rows are unchanged; the labels now say which row is the default.

### 24-building scene (19 built + 5 surrogates, 60 placed instances)

| Strategy | Draw calls (mean of 10 views) | Triangles submitted (mean) | Shadows off: synced ms (median, range) | Shadows on: synced ms (median, range) | JS submit ms off / on | Worst view ms (on) | Resident geometry MB | Meshes | Build ms |
|---|---|---|---|---|---|---|---|---|---|
| Unmerged | 411 | 379,968 | 8.65 (6.7-9.0) | 13.77 (13.6-15.4) | 4.1 / 6.7 | 14.7 | 31.1 | 635 | 0 |
| District (per district x material) | 204 | 444,042 | 7.31 (7.0-7.3) | 10.52 (10.5-10.6) | 3.0 / 3.7 | 12.1 | 44.6 | 273 | 194 |
| Cells 60 m | 197 | 532,429 | 6.69 (6.6-7.0) | 10.02 (9.9-10.3) | 2.8 / 3.4 | 11.5 | 44.6 | 221 | 141 |
| Cells 45 m | 214 | 489,144 | 7.14 (6.9-7.3) | 10.73 (10.4-11.9) | 2.9 / 3.7 | 12.1 | 44.6 | 262 | 197 |
| Cells 30 m (**shipped default**) | 238 | 438,619 | 7.39 (7.3-8.1) | 11.13 (10.9-11.3) | 3.4 / 4.1 | 12.8 | 44.6 | 317 | 201 |
| Cells 20 m | 320 | 393,310 | 8.44 (8.2-8.7) | 12.12 (12.1-12.7) | 3.8 / 5.0 | 13.1 | 44.7 | 461 | 241 |
| Scene-wide (one set) | 110 | 605,941 | 6.25 (6.2-6.9) | 9.53 (8.7-9.6) | 2.2 / 2.5 | 11.9 | 44.6 | 84 | 106 |

### 19 built buildings only (56 placed instances)

| Strategy | Draw calls (mean of 10 views) | Triangles submitted (mean) | Shadows off: synced ms (median, range) | Shadows on: synced ms (median, range) | JS submit ms off / on | Worst view ms (on) | Resident geometry MB | Meshes | Build ms |
|---|---|---|---|---|---|---|---|---|---|
| Unmerged | 383 | 331,574 | 6.83 (6.8-8.6) | 12.52 (12.4-12.7) | 3.0 / 5.0 | 13.7 | 31.1 | 580 | 0 |
| District (per district x material) | 176 | 396,425 | 6.79 (6.3-6.8) | 9.67 (9.7-9.9) | 2.8 / 3.5 | 11.4 | 37.6 | 220 | 142 |
| Cells 60 m | 191 | 449,400 | 6.53 (5.8-6.7) | 9.68 (9.6-11.9) | 2.5 / 2.8 | 11.3 | 37.6 | 212 | 104 |
| Cells 45 m | 207 | 415,112 | 6.49 (6.0-6.8) | 9.99 (9.6-10.1) | 1.9 / 2.6 | 12.2 | 37.6 | 246 | 150 |
| Cells 30 m (**shipped default**) | 229 | 375,986 | 6.99 (6.0-7.2) | 10.43 (10.0-11.5) | 2.6 / 4.1 | 11.5 | 37.6 | 297 | 110 |
| Cells 20 m | 293 | 340,338 | 8.54 (7.6-8.6) | 11.67 (11.5-11.7) | 3.7 / 4.9 | 11.9 | 37.7 | 417 | 182 |
| Scene-wide (one set) | 109 | 504,867 | 5.90 (5.6-5.9) | 9.13 (8.8-9.1) | 2.2 / 2.6 | 9.9 | 37.6 | 84 | 80 |

### What the renderer was asked to draw, per camera (24-building scene, shadows on; calls / triangles)

| View | Unmerged calls / tris | District | Cells 45 | Cells 30 | Scene-wide |
|---|---|---|---|---|---|
| p4-town-aerial | 697 / 612,430 | 321 / 612,430 | 307 / 612,430 | 366 / 612,430 | 120 / 612,430 |
| p3-bazaar-aerial | 490 / 431,090 | 218 / 518,789 | 238 / 556,779 | 259 / 527,059 | 112 / 610,045 |
| p4-district-aerial | 694 / 609,174 | 320 / 612,196 | 306 / 612,196 | 365 / 612,196 | 120 / 612,430 |
| p4-lane-north | 599 / 526,173 | 262 / 536,791 | 258 / 563,897 | 314 / 563,395 | 119 / 611,830 |
| p3-aisle-eye | 291 / 310,195 | 163 / 436,225 | 183 / 459,885 | 190 / 360,707 | 110 / 610,009 |
| p3-west-interior | 193 / 200,844 | 130 / 313,543 | 132 / 345,679 | 142 / 273,189 | 102 / 604,774 |
| p4-gate-back | 102 / 108,346 | 89 / 157,602 | 101 / 225,788 | 94 / 172,402 | 83 / 568,191 |
| p3-axis-to-hall | 379 / 357,412 | 192 / 454,648 | 222 / 532,662 | 217 / 392,947 | 111 / 610,033 |
| p3-gameplay | 440 / 398,844 | 207 / 466,579 | 233 / 543,068 | 264 / 521,031 | 111 / 610,033 |
| p2b-hall-aerial | 229 / 245,167 | 137 / 331,612 | 164 / 439,059 | 173 / 350,836 | 107 / 609,638 |

## 3. Findings

1. **Every merge mode except 20 m cells helps on this GPU: 15-28 % off the frame time with shadows off** (8.7 to 6.3-7.4 ms) **and 19-31 % with shadows on** (13.8 to 9.5-11.1 ms), and halves JavaScript submit time (4.1 / 6.7 ms to 2.2-3.4 / 2.5-4.1 ms). That is the same direction as batch 2, now with 5 more buildings.
2. **The fewest draw calls did not give the best views.** Scene-wide merging is fastest here (110 calls, 6.3 / 9.5 ms) but it submits **every** triangle in every camera: 568k in the arrival view that unmerged culls to 108k, 5.2 times as many; on a vertex-bound device that view would cost five times as much. District and cell merging keep culling: the same arrival view submits 158k (district), 172k (30 m cells), 226k (45 m cells).
3. **Cell size has an optimum, and it is not large.** 20 m cells cost 320 calls and 8.4 / 12.1 ms (as slow as unmerged without shadows); 45 and 60 m cells keep the call count (214, 197) but cull poorly in the dense centre (45 m: 346k in the Western Hall interior, against 273k at 30 m and 201k unmerged). **30 m cells (the batch's starting hypothesis) are the best compromise**: 238 calls, the lowest submitted triangles of the merged modes in the interior and entrance views, and a frame time equal to district merging within the spread (7.4 / 11.1 vs 7.3 / 10.5 ms).
4. **At the current town size district merging is as good as 30 m cells** (204 vs 238 calls, 444k vs 439k triangles). The reason to prefer cells is scaling, not today's number: a district's extent and the amount of geometry in it grow with the town; a 30 m cell stays the same size, so culling granularity and the cost of re-merging one cell do not degrade. That is an argument from the construction of the method; it was not measured on a larger town.
5. **Memory.** Merging bakes world transforms, so repeated modules stop sharing vertex buffers: resident geometry rises from 31.1 MB (unmerged, 60 instances sharing kit geometry) to 44.6 MB merged (+43 %) in the 24-building scene, 37.6 MB in the 19-building one. A production build must drop the unmerged source after merging (the preview keeps both). The JS heap figure (about 340-370 MB) is dominated by the page and the kept sources and did not separate the strategies, so it is not used. GPU texture memory is unchanged by merging: 75 textures, about 95 MB estimated with mip chains.
6. **Merge cost at load:** 106-241 ms for the 24-building scene on this machine, once; trivial next to the 630 ms shader pre-warm.

## 4. Strategy for the complete town

1. **Merge static, non-repeating geometry in 30 m cells** (default `cell30`), including ground and paving split at cell borders. Keep culling on.
2. **Do not merge heavy repeated props** (barrels, sacks, baskets, lanterns, benches): keep them as shared-geometry instances (or `InstancedMesh`) so memory does not grow +43 %; they are what the module LOD already trimmed.
3. **Keep the shader pre-warm and the material cache** (unchanged from batch 2); the merge never creates new programs.
4. **Per cell, not per scene, for shadows**: the fitted frustum (batch 2) stays; with the town twice the area a cascaded or per-cell shadow cost should be measured before the full town, on the target hardware.
5. **Budget check against the contract:** the 24-building scene submits 605,941 triangles when every cell is in view (scene-wide), 439k on average with 30 m cells, against the P1.4 projection of 532k. The finished town can be expected near the projection only if the five missing buildings come in at the surrogate sizes; this is an extrapolation, not a measurement.
6. **A target device must be named and measured** before the town budget is fixed. That item remains open.

## 5. Geometry and texture compression

What was investigated, on the final kit (`evidence/compression-size-analysis.json`):

| Item | Size or result | Status |
|---|---|---|
| Kit GLB | 33.37 MB raw, 10.99 MB gzipped (batch 2: 27.03 / 9.10) | measured |
| Geometry in the file | 30.09 MB of it: positions 7.49, normals 7.49, UV 4.98, vertex colour 5.10 (float), baked AO 2.50 (float), indices 2.52 | measured |
| **KHR_mesh_quantization** (int16 positions, int8 normals, uint16 UVs, uint8 colour and AO) | about **16.7 MB, -44.5 % of the geometry bytes**; the same saving on the GPU buffers | **analytic estimate only**: supported natively by the vendored GLTFLoader, but no rewritten GLB was produced or loaded |
| **WebP textures** (EXT_texture_webp, quality 88, every embedded image) | images 2.90 MB to 1.30 MB; GLB 33.37 to 32.00 MB raw, 10.99 to 9.67 MB gzipped (-12 %); GPU memory unchanged (decoded to RGBA) | **built and loaded in the engine** (`p2a_webp_variant.py`, `?glb=models/merchant-citadel-p2a-kit-webp.glb`) |
| WebP visual check | same four cameras, baseline vs WebP: PSNR 45.5-54.2 dB, mean absolute difference 0.21-0.64 of 255, 99th percentile 2-3 levels | measured; I judge it visually identical, the owner has not seen it |
| KTX2 / Basis (GPU-compressed textures, about 4x less texture memory: about 95 MB to about 24 MB estimated) | not tested | the vendored three build does not export `KTX2Loader` or its transcoder |
| Meshopt / Draco geometry compression | not tested | the vendored build exports no decoder; the npm CLI that would have produced these files was not permitted to run (auto-mode refused a `npx` download), so I did not work around it |

Recommendation: (a) adopt quantisation at export when a quantising writer is available (largest low-risk saving: 13 MB and GPU memory); (b) WebP is safe and loadable today but saves little because geometry, not images, dominates the file; (c) GPU-compressed textures are the real memory lever (95 MB of mipped RGBA), and need the KTX2 loader and transcoder added to the vendored build, which is a dependency decision for the owner.

## 6. Loader changes this batch

`loader.js`: `mergeByGroup({cellSize})`, `splitMeshByCell`. `p2a.js`: default merge `cell30`, `?merge=cellN`, `?town24=1`, `?warm=`/`?warmb=`. `p2a-tests.js`: `mergecells` (this comparison), `district` (04), view names and shot tags. Production modules are untouched (hashes checked).
