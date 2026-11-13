# 05 — Optimisation and file-size assessment (final 54-node kit)

Rule kept from batch 4: nothing is claimed as an improvement until the **encoded file** loaded in the **actual engine** was checked. The vendored three build and the game's loader were not changed; nothing was installed.

## 1. Files

| File | Raw bytes | gzip -9 | raw vs default | gzip vs default | SHA-256 prefix |
|---|---|---|---|---|---|
| `merchant-citadel-p2a-kit.glb` (**default, float**) | 46,517,600 | 14,519,495 | — | — | 9288a67693af |
| `-webp.glb` (textures as WebP, `EXT_texture_webp`) | 44,834,784 | 12,887,998 | −3.6 % | −11.2 % | 6bc7395a08c1 |
| `-quant.glb` (`KHR_mesh_quantization`) | 29,795,412 | 11,878,324 | **−35.9 %** | −18.2 % | fb3e492eb2bd |
| `-quant-webp.glb` | 28,112,616 | 10,254,786 | **−39.6 %** | **−29.4 %** | 8944258bcc39 |
| batch 4 kit (22 buildings, for scale) | 40,849,756 | 13,166,929 | | | 2837f8cb2ee9 |

Quantisation: positions float32×3 → int16×3 with a per-node power-of-two scale (**largest position error 1.95 mm**), normals int8, colours uint8, UVs uint16 where they fit; 241 of 602 primitives (40 %) have tiling UVs outside [0, 1] and stay float (`quantize-report.json`). `_AO` stays float.

## 2. Does the encoded file look the same?

All 14 town and terrace cameras rendered from each variant (decoded to float at load) against the float GLB, same camera, same frame (`quant-webp-visual-diff.json`):

| Variant | PSNR (dB) over 14 views, min / typical | worst share of pixels differing by > 24/255 |
|---|---|---|
| quantised | 35.7 / 41–53 | 0.64 % (c04) |
| quantised + WebP | 35.4 / 40–50 | 0.64 % (c04) |

The weak case is **c04, the camera one metre from the forecourt rail**: a large close-up of wood grain, where the difference sits along the grain edges and not on silhouettes (`quant-diff-c04.jpg`). It is already 35.7 dB with quantisation alone, so WebP is not the cause; the cause (position step 2–4 mm on the rail, or UV precision on tiling wood) was not isolated. Every other view is ≥ 40 dB. This is a numerical comparison plus one image looked at, not a judgement of every view by eye. Merged geometry re-quantised at load (`?qmerge=1`) was checked in batch 4 with the integrity test and not repeated in this batch.

## 3. Does it run faster or use less memory?

**Not re-measured in batch 5** (frame times are invalid on the loaded machine; see 04). The batch 4 result, on the 22-building kit and a quiet-enough machine, stands as the best available:

* Quantised vertex data kept resident was **slower** (+1.3 to +2.9 ms per frame) although geometry memory halved (38.4 → 21.6 MB unmerged). Hypothesis (not instrumented): the Metal backend converts 3-component 16/8-bit vertex formats per draw.
* **Decode-at-load** (`?dequant=1`, in the preview's loader only): frame times equal to the float kit; decode 46 ms plus parse 110 ms against 129–163 ms for the float file; transfer 35 % smaller.
* A 4-component padded layout was **not tested**.

For the final kit the same decode-at-load path was **only checked for visual equivalence** (the table above), not for timing. I do not claim that compression speeds rendering; it reduces transfer and, only if kept resident, memory, and the one resident test cost frame time.

## 4. Other options

| Option | State |
|---|---|
| Module LOD (corner brick, lantern, barrel, basket, sack, rope, wheelbarrow, fruit basket, anvil, window box, chest) | kept, no new targets this batch |
| Material reuse, baked texture dedupe | kept: 115 materials in the GLB, 98 in the page, 79 images |
| Instancing of repeated whole buildings | analysed in batch 4 (≤ 10.7 % of placed triangles), not built |
| Distance LOD for roofs and props, lazy load per district | open; become relevant if the lower-end measurement is bad |
| Meshopt, Draco, KTX2 / Basis | not tested (no decoders in the vendored three build) |

## 5. Recommendation (not a decision)

1. Ship the **float GLB as the default**; offer **quant + WebP with decode-at-load** as a transfer variant (−29 % gzip, 10.3 MB) once the game's loader gets a decode step (new game code: the owner's call).
2. Do not keep quantised vertex data resident before measuring on the target device.
3. Keep 30 m cells.
4. Name the target device, then measure on a quiet machine and on that device before any further optimisation.
