# 05 — Optimisation assessment (encoded files, validated in the browser)

Rule followed: nothing is claimed as an improvement until the **actual encoded file** loaded in the **actual engine** and was measured and looked at. The vendored three build was not changed and nothing was installed or purchased. The tools below are scripts in `docs/planning/merchant-citadel/p2a/blender/` (`p2a_quantize_glb.py`, `p2a_webp_variant.py`); numbers come from `evidence/quantize-report.json`, `merge-cells-b4-*.json`, `quant-webp-visual-diff.json`.

## 1. Files (the final kit, 51 nodes, 551 primitives)

| File | Raw bytes | gzip -9 | Raw vs default | gzip vs default |
|---|---|---|---|---|
| `merchant-citadel-p2a-kit.glb` (default, float) | 40,849,756 | 13,166,929 | — | — |
| `-webp.glb` (textures re-encoded as WebP q88, `EXT_texture_webp`) | 39,181,032 | 11,553,631 | −4.1 % | −12.3 % |
| `-quant.glb` (`KHR_mesh_quantization`) | 26,374,688 | 10,817,894 | **−35.4 %** | −17.8 % |
| `-quant-webp.glb` | 24,705,972 | 9,208,205 | **−39.5 %** | **−30.1 %** |

Batch 3 estimated "about −44 % of geometry" from the format sizes; the encoded file gives less: everything except the 3.3 MB of embedded images fell from 37.6 MB to 23.1 MB (−38.5 %), because **221 of 551 primitives (40 %) have texture coordinates outside [0, 1]** (tiling) that a normalised 16-bit coordinate cannot hold, so they stay float32.

**What quantisation does:** position float32 x3 → int16 x3 (stride 8, the node gets a power-of-two scale 2^−k, k = 8 for the world-placed dressing and up to 13 for small nodes: step 3.9 mm down to 0.12 mm, **largest error 1.95 mm**); normal → int8 x3 (stride 4); colour → uint8; texture coordinates → uint16 when they fit; `_AO` stays float (a one-byte scalar needs a 4-byte stride in glTF). Indices, images and materials are unchanged.

## 2. Does it look the same?

All 18 cameras rendered with the quantised GLBs (decoded at load, section 3) against the float GLB, same camera, same frame (`quant-webp-visual-diff.json`):

| Variant | PSNR min / mean | worst share of pixels differing by more than 24/255 |
|---|---|---|
| quantised | 48.0 / 50.5 dB | 0.05 % |
| quantised + WebP | 44.4 / 47.3 dB | 0.08 % |

The comparison is numerical (PSNR and pixel counts); the images were not compared by eye one by one, so "visually identical" is a measurement-based statement, not a judgement. **Merged geometry re-quantised at load** (`?qmerge=1`) was checked with the integrity test: no vertex outside its bounds, 32-bit indices, triangle totals equal, rendered difference to unmerged ≤ 0.3 mean / ≤ 0.1 % of pixels over 24 (`merge-integrity-quant-requantised-merge.json`).

## 3. Does it run faster or use less memory?

Measured with the merge test in alternating runs (shadows off / on, ms; 22 buildings, 1280 x 720):

| Configuration | Unmerged | 30 m cells | Resident geometry | Load |
|---|---|---|---|---|
| float GLB (two runs) | 8.79 / 13.94 and 8.05 / 12.37 | 7.56 / 11.63 and 7.31 / 10.98 | 38.4 MB unmerged, 45.3 MB merged | 129–163 ms |
| quantised GLB, used as loaded (int16 attributes in memory) | **10.90 / 15.22** | **10.10 / 13.79** | **21.6 MB**, merged 45.3 MB | 114 ms |
| quantised GLB, merged geometry re-quantised (`?qmerge=1`) | 11.65 / 15.54 | 10.55 / 13.08 | 21.6 MB, merged **22.6 MB** | 93 ms (merge 225 ms instead of 125) |
| **quantised GLB decoded to float at load** (`?dequant=1`) | 8.44 / 12.90 | 7.57 / 11.18 | 38.4 MB, merged 45.3 MB | 110 ms + **46 ms decode** |

* **Quantised vertex data in memory is slower on this GPU: +1.3 to +2.9 ms per frame (+9 to +38 %) in every configuration.** The likely cause is that ANGLE on Metal has no native 3-component 16-bit or 8-bit vertex formats and converts them per draw; that is a hypothesis, I did not instrument ANGLE. A 4-component padded layout (int16 x4, int8 x4) might avoid it and was **not tested**. On another GPU or browser it may differ; no other device was measured.
* **Decode-at-load keeps the transfer win and removes the cost:** frame times equal the float kit's (within run-to-run spread); parsing the quantised file takes 110 ms and the decode 46 ms, 155 ms in all against 129–163 ms for the float file, with a 35 % smaller file to fetch.
* **Memory:** quantisation halves resident geometry (−44 % unmerged, −50 % merged) **but only if it is kept quantised**, which costs the frame time above. Whether the 17–22 MB matters depends on a target device that was not available.

## 4. The other options

| Option | Result |
|---|---|
| **Existing module LOD** | kept: corner brick 3,102 → 400, lantern 2,822 → 700, barrel 2,348 → 800, basket 2,200 → 800, sack 1,529 → 600, rope coil 1,388 → 600, wheelbarrow 1,736 → 899, fruit basket 3,646 → 1,300, rope 1,748 → 700, anvil 3,808 → 1,400; **two added in this batch: window box 1,330 → 700 and chest 816 → 500**. Usage x reduction gives about 239k triangles not in the kit (an estimate from instance counts, not a render count). No artefacts were noticed in the images looked at (02). |
| **Material reuse** | already on (batch 2): one material object per distinct (colour, constants, textures): 95 materials and 551 geometries in the page. Byte-identical baked textures are stored once: 78 images against 108 texture slots. Nothing new here. |
| **Repeated geometry instancing** | **analysed, not built.** Five kit nodes are placed more than once as whole buildings (A04 x3, A03, A04b, A10p, A10c: 56,720 triangles repeated, 10.7 % of the placed building triangles). Unmerged, those already share their geometry buffers; merged, they are copied, which is part of the +18 % memory of 05's merged sets. Making them `InstancedMesh` would trade that memory for more draw calls (one per primitive per node) and worse culling (one bound for all instances). Not worth building at the current size; revisit if the town adds repeated terrace houses. |
| **Selective mesh simplification** | the LOD list above is the selective simplification, done in Blender with a decimate modifier on modules (not on buildings). No further module was found worth the artefact risk: the next largest repeated modules are the balcony rail (1,120 triangles, five on E05) and the door leaf (1,142, five on B13). |
| **WebP textures** | −4.1 % raw, −12.3 % gzip alone; PSNR 44–54 dB per image (batch 3), in-engine renders ≥ 44 dB (above). Cheap and safe; `EXT_texture_webp` is supported by the vendored `GLTFLoader`. |
| **Meshopt, Draco, KTX2 / Basis** | **not tested.** The vendored three build has no decoders for them and an npm download of a tool to produce them was refused in batch 3 and not retried; nothing was installed. They remain the likely larger win for texture memory (KTX2) and geometry transfer (Meshopt), and the one thing this document cannot give. |

## 5. Recommendation (a recommendation, not a decision)

1. **Ship the float GLB as the default** (no risk) and **add the quantised + WebP GLB as a transfer variant with decode-at-load** (−30 % gzip, same frame times, +46 ms). That needs a decode step in the game's loader, which is **new loader code in the game** and therefore the owner's call; it is not in the preview's default.
2. **Do not keep quantised vertex data resident** until it has been measured on the target hardware (and a 4-wide layout tried).
3. Keep 30 m cells, module LOD and material caching.
4. Ask for the target device and measure there before spending effort on KTX2/Meshopt.
