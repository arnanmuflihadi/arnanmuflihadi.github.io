# 04 — Rendering architecture and measured performance

## 1. Conditions and limits (read first)

* **One machine:** Apple M4 Pro (12 cores), WebGL 2 through ANGLE/Metal, the Claude desktop app's built-in browser (Chromium 156), pane visible, devicePixelRatio 1, **1280 x 720**. Every GPU-inclusive time ends with a 1 x 1 `readPixels` (`gl.finish()` does not wait for the GPU in Chromium); "synced frame" = render + read-back, "walk frame" = a 60 Hz simulation step with the real controller and camera + render + read-back along the street axis.
* **The machine was shared** (load average 5–9 while measuring; Blender and the browser tests ran at other times, never during a measurement, except that the machine's own background load is not controlled). Run-to-run differences of ±10–15 % are normal: the float kit's unmerged case measured 8.79 ms in one run and 8.05 ms in another; all comparisons below come from **medians of three interleaved repeats** per configuration, and the experiments that matter (quantisation) were repeated in alternation.
* **No lower-end hardware was available and none is estimated.** Nothing here says how the scene runs on an integrated GPU, a phone or an older laptop. The device gate stays open (07).
* Counts are what the renderer was asked to draw (`renderer.info`, per view), not budgets. The shadow pass is not in `renderer.info`; its cost is the frame-time difference.
* The stray-tab effect found in batch 3 (a second browser tab rendering in the background doubles timings) was respected: one tab only.

## 2. Strategies compared

* **Unmerged:** every placed object a draw per mesh, frustum culling per object, geometry shared between instances.
* **District:** static merge per district (D1–D8) x material (batch 2 production mode).
* **30 m cells (default):** static merge per 30 m cell x material; a mesh that fits a cell stays whole in the cell of its centre; ground, paving and dressing meshes are split by triangle centroid into the cells.
* **Scene-wide:** one merged set (diagnostic): fewest calls, no culling.
* 20 / 45 / 60 m cells were kept for the 24-building estimate.

## 3. The built slice: 22 buildings, 62 placed instances (no surrogates)

15 cameras (the 10 of batch 3 plus five of the east quarter), medians of three repeats. Mean over the 15 views unless stated.

| Strategy | Calls | Triangles submitted | Synced frame ms off / on (range on) | Synced p50 / p95 / p99 ms (on) | Walk frame p95 / max ms (on) | CPU submit ms (on) | Mean view ms off / on | Resident geometry MB | Meshes | Merge ms |
|---|---|---|---|---|---|---|---|---|---|---|
| Unmerged | 439 | 383,231 | 8.79 / 13.94 (12.9–14.1) | 13.5 / 18.2 / 19.1 | 18.4 / 20.4 | 3.4 | 7.2 / 10.6 | 38.4 | 679 | 0 |
| District | 211 | 456,047 | 7.48 / 11.74 (11.6–12.2) | 11.4 / 15.3 / 17.8 | 15.0 / 17.4 | 2.0 | 6.1 / 10.2 | 45.3 | 277 | 66 |
| **30 m cells** | 259 | 447,940 | 7.56 / 11.63 (11.4–13.3) | 11.4 / 15.1 / 17.4 | 16.5 / 20.2 | 2.3 | 6.6 / 9.9 | 45.3 | 344 | 124 |
| Scene-wide | 120 | 605,684 | 6.39 / 11.08 (9.8–12.1) | 11.0 / 13.6 / 17.1 | 14.3 / 17.1 | 1.5 | 5.9 / 9.4 | 45.3 | 99 | 53 |

A second, independent run of the unmerged and 30 m cases gave 8.05 / 12.37 and 7.31 / 10.98 ms (shadows off / on): the ordering is stable, the absolute numbers move by about a millisecond.

**Frame-time distribution** (shadows on; the synced percentiles come from 90 back-to-back renders per repeat, the walk figures from 240 walked frames per repeat, medians of the repeats): the 99th percentile of the synced frame is 17–19 ms and the worst walked frame 17–20 ms in every mode; no mode shows a hitch beyond about 20 ms on this machine, and the unmerged mode has the widest spread (p95 18.2 against 13.6–15.3 for the merged modes).

### View-dependent culling (shadows on: calls / triangles submitted / ms)

| View | Unmerged | District | 30 m cells | Scene-wide |
|---|---|---|---|---|
| town aerial | 743 / 612,974 / 12.2 | 326 / 612,974 / 11.4 | 396 / 612,974 / 10.1 | 138 / 612,974 / 9.6 |
| bazaar aerial | 488 / 409,502 / 12.7 | 223 / 540,698 / 12.7 | 276 / 529,483 / 11.6 | 121 / 610,333 / 11.1 |
| lane north (artisan) | 611 / 504,703 / 10.3 | 268 / 520,686 / 10.0 | 328 / 544,058 / 10.4 | 137 / 612,962 / 8.8 |
| bazaar aisle at eye height | 286 / 297,117 / 8.6 | 158 / 421,875 / 8.6 | 191 / 346,243 / 9.1 | 112 / 607,649 / 8.3 |
| inside the West Hall | 180 / 173,114 / 9.1 | 117 / 286,117 / 8.7 | 140 / 276,030 / 7.9 | 102 / 600,578 / 7.7 |
| gateway from behind | 102 / 107,346 / 8.9 | 89 / 152,192 / 6.8 | 95 / 173,590 / 7.9 | 83 / 580,651 / 7.3 |
| hall axis | 379 / 342,570 / 10.0 | 188 / 439,222 / 9.2 | 220 / 365,919 / 8.9 | 121 / 610,469 / 8.8 |
| follow camera in the bazaar | 451 / 385,644 / 11.3 | 212 / 453,025 / 10.3 | 275 / 490,986 / 10.2 | 130 / 611,177 / 9.7 |
| **east aerial** | 563 / 487,051 / 11.5 | 260 / 530,424 / 12.9 | 309 / 535,393 / 10.9 | 127 / 599,923 / 11.0 |
| **lane east (eye)** | 598 / 519,369 / 11.1 | 269 / 562,715 / 10.5 | 340 / 575,046 / 10.2 | 134 / 611,853 / 9.9 |
| **court from the lane (eye)** | **83 / 102,666 / 7.6** | 82 / 281,737 / 8.1 | 98 / 188,999 / 7.3 | 90 / 584,987 / 7.5 |
| **follow camera in the lane** | 596 / 507,651 / 11.5 | 267 / 564,288 / 10.8 | 338 / 576,619 / 11.0 | 134 / 611,853 / 10.0 |
| **route aerial** | 549 / 470,917 / 11.9 | 258 / 557,632 / 10.4 | 317 / 553,582 / 11.1 | 130 / 609,641 / 10.6 |

**Reading.**

1. **The fewest draw calls is not the best in every view.** Scene-wide merging has 120 calls and the lowest mean time, but it submits about 600k triangles in every view; in the court (eye level) unmerged culls to **103k triangles at 83 calls**, 5.7 x fewer than scene-wide and 1.8 x fewer than 30 m cells, and its frame time (7.6 ms) is level with every merged mode. Where the view sees much of the town (the town aerial: 12.2 ms unmerged against 11.4 / 10.1 / 9.6) merging wins by 0.8–2.6 ms; in the lane looking north the modes are within 0.3 ms of each other except scene-wide; in enclosed views (inside a hall, the court, behind the gateway) the merged modes draw 1.4–5.7 x more triangles than unmerged for no measurable gain.
2. **30 m cells and district merging are equal within the spread** at this size (11.6 vs 11.7 ms on, 7.6 vs 7.5 off). Cells cull better in enclosed views than whole-scene merging and keep a constant cell size as the town grows; districts have uneven sizes (D3 holds the bazaar and both halls). 30 m remains the default for that reason, not because it won.
3. **Merging costs memory:** merged geometry bakes world transforms, so repeated modules stop sharing buffers: 45.3 MB resident merged against 38.4 MB unmerged (+18 %; batch 3 reported +43 % with a smaller kit and more repeats).

## 4. The 24-building estimate

`?town24=1` adds two surrogates (copies of existing nodes at the sites of B15 and B16, no collision, not architecture), so the renderer sees 24 buildings; batch 3's estimate had five surrogates and this one has two, and B13, E04, E05 are the real ones. Six strategies, three repeats.

| Strategy | Calls | Triangles | Synced ms off / on (range on) | Synced p95 ms (on) | Meshes | Merge ms |
|---|---|---|---|---|---|---|
| Unmerged | 449 | 406,491 | 8.95 / 13.99 (13.6–14.4) | 17.3 | 691 | 0 |
| District | 221 | 479,307 | 8.20 / 11.86 (11.2–12.4) | 14.7 | 289 | 82 |
| Cells 45 m | 232 | 509,292 | 7.84 / 13.07 (11.3–13.2) | 16.7 | 281 | 65 |
| **Cells 30 m** | 263 | 471,398 | 7.95 / 12.33 (12.2–13.2) | 16.0 | 348 | 150 |
| Cells 20 m | 351 | 424,284 | 8.75 / 12.66 (12.6–12.8) | 16.6 | 511 | 124 |
| Scene-wide | 120 | 634,818 | 7.13 / 11.79 (11.3–12.8) | 15.3 | 99 | 65 |

Versus batch 3's estimate (surrogates for B13, E04, B15, B16, E05, measured on another day): unmerged 8.65 / 13.77 ms, 30 m cells 7.39 / 11.13, district 7.31 / 10.52. The differences (0.1–1.3 ms) are inside the run-to-run spread, so replacing three surrogates by the real buildings (+94k unique triangles) shows **no measurable change**; it is not evidence that it costs nothing. 20 m cells again cost the most calls; 45 m culled worst in the dense centre.

## 5. Loading, merge and memory

| Item | Measured |
|---|---|
| GLB parse and instantiate (`GLTFLoader`, local server) | float kit 129–163 ms over four runs (40.8 MB; includes reading from the local server, not a network); quantised GLB 93–114 ms |
| Shader pre-warm before the first frame | 0.77–1.13 s (74–76 programs) |
| Merge build | 53 ms (scene) to 150 ms (cells 30, town24) |
| Resident geometry | unmerged 38.4 MB; merged 45.3 MB; GPU texture memory estimate **96.6 MB** with mips for 78 textures (the Blender report, which counts identical copies, gives 111.8 MB for 108); JS heap median 214–246 MB |
| Unique geometries / materials | 551 / 95 (material caching on) |

## 6. Merged-geometry integrity (`?autotest=mergeintegrity`)

For each of district, 20, 30, 45, 60 m cells and scene-wide: index array type against vertex count, maximum index against vertex count, NaN positions, every vertex inside the geometry's bounding sphere and box, degenerate triangles, triangle totals, and a rendered comparison of ten cameras against the unmerged render (640 x 360, shadows off).

* **Index precision:** all 1,706 merged meshes across the six modes use 32-bit indices (the source GLB is 16-bit; the merge writes `Uint32Array`); the largest merged mesh has 117,608 vertices (scene-wide), 69,952 at 30 m cells. A 16-bit index on any of them would wrap.
* **Bounding volumes:** no vertex outside its bounding sphere or box (worst 0 m); frustum culling therefore cannot drop visible geometry.
* **Corruption:** no index beyond its vertex count, no NaN, no degenerate triangle; triangle counts equal the unmerged scene (576,398 placed triangles); rendered difference to unmerged 0.001–0.012 mean absolute (of 255), no pixel over 24 in any of the ten views.
* **Control:** the test would have caught a real fault: re-creating the largest merged mesh with a 16-bit index gave mean difference 1.29 and 2.2 % of pixels over 24 ([control](evidence/merge-integrity-control.json)).
* **Defect found and fixed in the loader:** `mergeByGroup` assumed non-interleaved attributes; a quantised GLB (interleaved) made it build broken geometry and the page threw in the first render. It now rebuilds Float32 attributes (or, with `?qmerge=1`, quantised ones) from any source.

## 7. Scaling strategy for the 24-building town

1. **Keep 30 m cells for static architecture and paving; do not merge the whole scene.** Cells keep the triangle count honest in enclosed views.
2. **Do not cell-merge repeated props you want to keep cheap in memory** (barrels, crates, lanterns): merged copies cost +18 % geometry; a later InstancedMesh pass per repeated module is the remedy and was **not** built or measured here (05).
3. **Keep module LOD for repeated high-poly modules** (corner brick 3,102 → 400, lantern 2,822 → 700, sacks, barrels, baskets; two added: window box 1,330 → 700, chest 816 → 500). Distance LOD for roofs and props stays an open task for the town.
4. **Budget:** at 24 buildings the unique kit is about 516k triangles (P1.4 projected 532k after substitutions) and the worst measured view submits 575k with 30 m cells and 613k scene-wide. This is a count, not a verdict: the frame times (7–14 ms at 720p on this GPU) say nothing about weaker hardware.
5. **Load:** the kit is 13.2 MB gzipped (05 shows −30 % reachable); a lazy load per district is still the remedy for the whole town and is not implemented.

## 8. What this does not tell

No GPU but the M4 Pro; no thermal or battery state; no network transfer; no memory measurement beyond JS heap and the resident-geometry/texture estimates; frame times include the preview's own UI; shadows-on cost is inferred from frame-time differences.
