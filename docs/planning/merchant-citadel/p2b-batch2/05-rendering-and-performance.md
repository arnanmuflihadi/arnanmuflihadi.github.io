# 05 — Rendering pipeline and measured performance

## 1. Conditions and limits (read first)

* **One machine:** Apple M4 Pro (12 cores), WebGL 2 via ANGLE/Metal, the Claude desktop app's built-in browser (Chromium 156), pane visible, devicePixelRatio 1, render target **1280 x 720** unless stated. Method as corrected in the closeout: every GPU-inclusive time ends with a 1 x 1 `readPixels` (Chromium's `gl.finish()` does not wait for the GPU); frame = 60 Hz simulation step + render + read-back; 240 walked frames and 90 synchronised renders per configuration (`p2a-tests.js: measure`).
* **The machine is shared with other applications** (WindowServer, other browsers, virtual machines were all running, load average 5–9). Timings moved by ±30 % between runs, so every number below is the **median of three interleaved runs** with the range, and the comparison with the closeout slice was re-measured **in the same session** (4 replay runs of the delivered closeout slice, interleaved with 3 runs of the final kit). The closeout report's absolute figures (3.0–5.9 ms) were taken at a quieter moment; the replay under today's load measured 5.4–11.1 ms for the same slice. Compare the pairs, not the absolute values to older documents.
* **No lower-end hardware was available and none was measured.** The only "lower-performance configuration" ever run was a CPU-software renderer (SwiftShader) in the closeout (about 1 s per frame at 418k triangles, a stress bound, not a device); it was not repeated for this kit. **Nothing here establishes compatibility with integrated GPUs, phones or older laptops.** The device gate stays open (06).
* Counts (draw calls, triangles, textures) are what the renderer was actually asked to draw (`renderer.info`, per camera), not theoretical budgets.

## 2. Loader features implemented or validated

| Requirement | Implementation | Measured result |
|---|---|---|
| **Material caching** | `loader.js: dedupeMaterials`: one material object per (name, colour, constants, flags, texture sources) | **114 → 75 material objects (−34 %)**; includes the collapse of the 15 identical palette materials after texture reuse |
| **Texture reuse** | kit export reuses one image datablock per byte-identical baked file (palette copies, duplicate normal maps) | 82 → **69 images** in the GLB; ~93 MB estimated GPU with mips (`autotest-scale.json`, 1024 px tier-1, 512/256 px tier-2) |
| **Shader pre-warming** | `p2a.js: prewarm()` renders once with shadows on, off and on again, culling disabled, before the first visible frame | costs **~630 ms** at load; first measured frame after it is **8–19 ms** against **230–350 ms** for the unwarmed closeout slice (first-frame shader compile) |
| **Per-district merging** | `loader.js: mergeByGroup` by district (D2 market street, D3 bazaar, D5 civic court, D8 tea lookout) x material, world transforms baked, bounding spheres computed, frustum culling kept | see section 3 |
| **LOD** | module LOD of the two heaviest repeated modules (corner brick 3,102 → 400 triangles, wall lantern 2,822 → 700), kept from the closeout | kit 336.5k unique triangles; **no distance LOD**: validated unnecessary at this scale (section 4), recommended for the town |
| **Frustum culling** | per-object when unmerged; per-district when merged; scene-wide merge has no culling benefit | section 3 |
| **Shadow-map configuration** | frustum **fitted** to the built area in light space (122 x 123 x 101 m instead of 120 x 120 x 260 m), default **2048**; `?smap=` | 1024 visibly soft, 2048 and 4096 close ([crops](visuals/ab/shadow-map-1024-2048-4096.jpg)); cost 10.2 / 10.2 / 10.8 ms for 1024 / 2048 / 4096 at 720p: no meaningful difference on this GPU |

## 3. Merged and unmerged, shadows off and on (median of 3 runs, whole-slice view)

| Configuration | Draw calls | Triangles drawn | Synced frame mean ms (median / min–max) | p95 ms | First render ms | Programs |
|---|---|---|---|---|---|---|
| Unmerged, shadows off | 503 | 427,804 | 8.51 (7.96–9.35) | 11.7 | 15.8–17.9 | 58 |
| Unmerged, **shadows on** | 503* | 427,804* | 12.86 (12.85–13.72) | 17.0 | 15.1–19.4 | 60 |
| Merged **scene-wide**, shadows off | 115 | 428,100 | 6.49 (6.36–7.16) | 9.6 | 10.7–14.9 | 60 |
| Merged scene-wide, shadows on | 115* | 428,100* | 10.68 (10.47–12.15) | 14.5 | 11.1–13.5 | 60 |
| Merged **per district**, shadows off | 195 | 427,866 | 7.13 (6.36–8.23) | 10.4 | 7.2–9.4 | 60 |
| Merged per district, **shadows on** | 195* | 427,866* | 11.30 (10.86–13.67) | 14.8 | 11.8–14.6 | 60 |
| *Closeout slice (replay), unmerged, off / on* | 335 | 308,503 | 6.31 / 11.14 | 9.7 / 15.0 | 282–347 / 228–292 | 24 / 50 |
| *Closeout slice (replay), merged, off / on* | 123 | 308,799 | 5.38 / 9.06 | 7.8 / 13.3 | 13–97 / 10–37 | 50 |

\* `renderer.info` does not include the shadow pass; its cost is the frame-time difference (about +4.2 to +4.4 ms here).

* Triangles drawn are the same for every mode in the whole-slice view because the whole slice is in view (427,8xx = the placed 406,942 plus the character, ground and sky). The batch added **+39 % triangles and +50 % draw calls (unmerged)** to the closeout slice and about **+1.1 to +2.2 ms** per frame (+15–35 %).
* **Merging:** unmerged 503 calls vs 115 scene-wide vs 195 per district. Scene-wide merging has the fewest calls and the same triangles in every view, so it never culls; district merging culls (next table). On this GPU the frame times of the two merged modes are within the run-to-run spread (6.5 vs 7.1 ms off, 10.7 vs 11.3 ms on); both beat unmerged by 1.4–2.2 ms.

### What the renderer was asked to draw per view (shadows on, culling active)

| View | Unmerged calls / triangles | Scene-merged | **District-merged** |
|---|---|---|---|
| Elevated bazaar | 429 / 351,962 | 112 / 427,436 | 163 / 410,594 |
| Central aisle (eye) | 276 / 277,476 | 110 / 427,400 | 150 / 408,169 |
| Inside the West Hall | 179 / 166,255 | 100 / 412,812 | 117 / **285,487** |
| West Hall entrance | 224 / 215,928 | 102 / 412,944 | 134 / 368,790 |
| Axis toward the Exchange Hall | 351 / 322,260 | 111 / 427,424 | 165 / 420,500 |
| Gameplay camera | 412 / 363,692 | 111 / 427,424 | 179 / 423,964 |
| Whole slice (aerial) | 505 / 428,100 | 115 / 428,100 | 196 / 428,100 |

District merging trades 55–80 extra draw calls against up to 33 % fewer triangles in enclosed views. Per-object culling gives the fewest triangles (166k inside the hall) at the most calls. For the whole town the district size matters: **merge per cell of about 30 m, not per district**, so that culling stays effective as the town grows (06).

## 4. Triangles, textures, LOD: budgets against observation

* Kit: 336,528 unique triangles in 36 nodes (halls 52.9k and 42.3k, the Exchange Hall 59k in five modules, buildings 5.8–49k); placed in the slice 406,942; drawn in the worst view 428k; drawn inside the hall 166k.
* P1.4's projection for the whole town is 532k after substitutions. The slice holds 14 of the 24 buildings and already draws 428k from above; scaling by building count suggests **roughly 700–800k in the worst view of the whole town**, above the projection. The two module LOD substitutions saved 31 % of kit triangles; **further P1.4 substitutions (window boxes, doors, crates, barrels) are still needed before the town**, and distance LOD for roofs and props becomes worthwhile then. This is an extrapolation, not a measurement.
* GLB 27.0 MB raw / **9.1 MB gzipped** (closeout 17.4 MB): +9.6 MB for the two halls (95k triangles, 125k vertices), signs, goods and the bazaar dressing; mesh quantisation not done (see 02).
* Textures 69 images, ~93 MB estimated GPU; unique material objects in the scene 75.

## 5. Sensitivity (`performance-scaling.json`, unmerged-district kit of the day)

| Output size (district merge, shadows on) | Synced mean ms |
|---|---|
| 1280 x 720 | 13.3 (first sample, includes warm-up) |
| 1920 x 1080 | 13.8 |
| 2560 x 1440 | 17.3 |
| 3840 x 2160 | 29.5 (34 fps equivalent) |

Shadows off at 720p: 6.5 ms. This run was taken one kit before the final export (same geometry, older chest) while the machine was loaded; treat as indicative.

## 6. What this does not tell

No GPU other than the M4 Pro; no battery or thermal state; no memory measurement beyond the texture estimate; no real keyboard session (all frames are autopilot-driven); frame times include the preview's own UI.
