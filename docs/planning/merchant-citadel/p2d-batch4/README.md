# Merchant Citadel — P2-B batch 4: Eastern Trade Quarter, warehouse district and tea route

**Status: PENDING HUMAN REVIEW. No visual approval is claimed.** Dated 2026-11-12. Nothing was committed, pushed or deployed. No tracked file changed (`git status`: only `docs/planning/` and `merchant-citadel-p2a/`, both untracked); the first island's controller, camera, character, input, collision and the vendored three build are untouched (SHA-256 in [evidence/production-code-sha256.txt](evidence/production-code-sha256.txt)). Batch 3 was treated as approved because the brief for this batch started from it; that approval was never stated in words.

**22 of 24 permanent buildings now stand** (19 + E05, B13, E04). The next planned step, the Civic Terrace tower houses B15 and B16, was not started.

| # | Deliverable | Where |
|---|---|---|
| 1 | Three completed assemblies | [01-district-construction.md](01-district-construction.md); matched images in [visuals/](visuals) |
| 2 | Editable Blender sources / reproducible scripts | `docs/planning/merchant-citadel/p2a/blender/` (`p2a_bazaar.py` three new variants and custom geometry, `p2a_data.py`, `p2a_kit_export.py`, `p2a_quantize_glb.py`, `p2d_expected.py`, `p2d_before_after.py`); `.blend` files stay outside the package |
| 3 | Game-ready GLB exports | `merchant-citadel-p2a/models/merchant-citadel-p2a-kit.glb` (40,849,756 B, SHA-256 `2837f8cb…`) plus three experiment variants, [05-optimisation-assessment.md](05-optimisation-assessment.md); structural inspection [evidence/glb-structural-inspection.json](evidence/glb-structural-inspection.json) |
| 4 | Building and asset registry | [asset-registry.csv](asset-registry.csv) / [.json](asset-registry.json) (51 nodes) |
| 5 | Updated pedestrian network | [pedestrian-network-batch4.json](pedestrian-network-batch4.json), [nodes](pedestrian-network-batch4-nodes.csv), [edges](pedestrian-network-batch4-edges.csv) |
| 6 | Collision and camera validation | [03-camera-collision-navigation.md](03-camera-collision-navigation.md); `evidence/` |
| 7 | Matched Blender and Three.js images (provisional internal review: [02-visual-quality.md](02-visual-quality.md)) | [visuals/comparison](visuals/comparison) (15 pairs + 3 regression views) |
| 8 | Before/after district comparisons | [visuals/before-after](visuals/before-after) (15 sheets, 2 x 2: Blender and Three.js, before and after, same camera) |
| 9 | Measured rendering performance | [04-rendering-and-performance.md](04-rendering-and-performance.md) |
| 10 | Optimisation assessment | [05-optimisation-assessment.md](05-optimisation-assessment.md) |
| 11 | Source and licence documentation | [06-assets-licence-registry.md](06-assets-licence-registry.md), [asset-provenance.csv](asset-provenance.csv) / [.json](asset-provenance.json) |
| 12 | Remaining construction backlog | [07-backlog-risks.md](07-backlog-risks.md) |
| 13 | Human playtest checklist | [08-guided-playtest-checklist.md](08-guided-playtest-checklist.md) |
| — | Production configuration | [production-config.json](production-config.json) |

## Headline results

* **Built:** B13 guild warehouse (loading canopy, hoist jib, tally station), E04 counting house (tally loggia, strongroom wing, guild frontage), E05 tea route merchant house (two-storey, balcony gallery over the lane, three doors). Triangles 37,194 / 31,628 / 24,606 (P1.4 contract: 42,321 / 37,334 / 8,278 for the archetypes before variants).
* **The quarter is one connected environment:** the warehouse lane, a service court (loading apron, loggia, canopy), a **new porters' path (Jalur Teh, not in P1.4)** from the court's east opening to the lookout terrace and E05's east door, and a second exploration loop through it. Placement of all three buildings is unchanged from P1.4 (documented adjustments only to N41, dressing, and E05's archetype).
* **Navigation:** network **49 nodes / 63 edges all pass in both directions** (10 nodes and 14 edges added, 1 node moved); **35 of 35 district routes** (14 new, incl. both directions of the east exploration loop) and ring walks round B13 and E04; **248 of 248 solids stop the player**; **placement 22 of 22** within 5 cm (kit nodes vs Blender: 0.005 cm); a scripted **real-keyboard session reached 16 of 16 waypoints**.
* **Camera:** compression was investigated, not hidden behind opacity. Causes found and corrected: a 2.2 m slot between E05 and E06 (camera 0.52 m, median 1.13 m: closed by two fences), a dead-end pocket behind B14 (the autopilot jammed in it: closed), **low floor props acting as camera obstacles** (camera pulled to 0.5 m for 0.2 s next to a wagon: props at or below 1.25 m no longer block the camera), and roof-proxy resolution (3 → 6 bands: measured effect ≤ 2 points, kept for accuracy). Sampled with full 360° turns at 12 walking nodes the camera stays ≥ 1.48 m (≥ 2.78 m at 10 of 12); the autopilot routes of the quarter keep it ≥ 1.8 m; the deliberately tight ring walks round B13 and E04 go down to 1.9 m and 1.08 m (opacity 0.15), see 03.
* **Rendering (M4 Pro, 1280 x 720, 22 buildings):** unmerged 439 calls 8.0–8.8 / 12.4–13.9 ms (shadows off / on); district 211 calls 7.5 / 11.7; **30 m cells** 259 calls 7.3–7.6 / 11.0–11.6; scene-wide 120 calls 6.4 / 11.1 with 606k triangles in every view. 30 m cells remain the default; the 30 / 45 m inconsistency of batch 3 is reconciled. Merged-geometry integrity (32-bit indices, bounds, corruption control) passes.
* **Optimisation (encoded files, browser-validated):** quantised GLB −35 % raw / −18 % gzip; with WebP −39.5 % / −30 %; numerically near-identical in the browser (PSNR ≥ 44 dB, ≤ 0.08 % of pixels differ by more than 24/255; not compared by eye image by image). **Quantised vertex data in memory made frames +1.3 to +2.9 ms slower (+9 to +38 %) on this GPU**, so the recommended use is decode-at-load (+46 ms, same frame times as the float kit).

## Not done / not verified (plainly)

No human playtest. No GPU other than one Apple M4 Pro; no lower-end device (none was available, nothing is estimated). Mouse-rotated camera round the new corners, gamepad and touch untested. The character fade has not been tried on the first island and its 0.14–0.43 opacity in the ring-walk stress tests is **not** presented as acceptable. B15 and B16 are surrogates in the 24-building estimate. Ground, vegetation and sky are still stand-ins. Meshopt, Draco and KTX2 are untested (no decoders in the vendored three build; nothing was installed). The paving still reads cooler in the browser than in Blender in shade.

## Rebuild and run

```bash
python3 docs/planning/merchant-citadel/p2a/blender/p2a_data.py          # scene.json (buildings, collision, network, views)
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --disable-autoexec \
  --python docs/planning/merchant-citadel/p2a/blender/p2a_kit_export.py -- <inspection_dir> <out_dir> merchant-citadel-p2a/data/scene.json
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --disable-autoexec \
  --python docs/planning/merchant-citadel/p2a/blender/p2a_world_scene.py -- <inspection_dir> <out_dir> merchant-citadel-p2a/data/scene.json <data_scratch_dir> <view names>
python3 docs/planning/merchant-citadel/p2a/blender/p2d_expected.py <out_dir>/kit-report.json merchant-citadel-p2a/data/scene.json merchant-citadel-p2a/data
node merchant-citadel-p2a/server.mjs --port 4180     # http://127.0.0.1:4180/merchant-citadel-p2a/index.html
#   ?autotest=suite | network | district | merch | hallcam | compress | fademotion | platform | scale | mergecells | mergeintegrity | views
#   ?merge=none|district|cell30|... ?town24=1 ?glb=models/...-quant.glb ?dequant=1 ?qmerge=1 ?lowprops=<m> ?scenefile=scene-before.json ?shot=<tag> ?names=a,b
```

The extracted licensed packs (`.asset-inspection/merchant-citadel-p1/extracted`) and the `.blend` files are not in the review package.

## Review package

`docs/planning/merchant-citadel/merchant-citadel-p2d-batch4-review.zip` (25.9 MiB, 319 files, integrity-tested, GLB hash checked; the images in `visuals/` are JPEG at quality 74 to stay under the upload limit): this folder, the Blender and data scripts, the preview code (`p2a.js`, `loader.js`, `p2a-tests.js`, server), the data (`scene.json`, expected bounds and envelopes, heightfield), the final default GLB, the JSON evidence of the preview, and the corrected batch 3 document 03. Left out to keep it deliverable: evidence screenshots (the ones used are in `visuals/`), the three experiment GLB variants (regenerate with `p2a_quantize_glb.py` and `p2a_webp_variant.py`), the baseline copies, `.blend` files and the extracted licensed packs.
