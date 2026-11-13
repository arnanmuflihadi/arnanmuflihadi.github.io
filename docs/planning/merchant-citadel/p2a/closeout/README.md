# Merchant Citadel — P2-A closeout and P2-B first construction gate

**Status: PENDING HUMAN VISUAL AND TECHNICAL APPROVAL.** Dated 2026-11-12. Nothing was committed, pushed or deployed. The first island, the production controller/camera/character/collision modules (SHA-256 unchanged) and all P1.x/P2-A packages are untouched; the P2-A slice is preserved in `merchant-citadel-p2a/baseline-p2a/`.

| # | Deliverable | File |
|---|---|---|
| 1 | Updated P2-A correction report (incl. three corrections to my own P2-A claims) | [01-correction-report.md](01-correction-report.md) |
| 2 | Before/after visual evidence | [visuals/before-after/](visuals/before-after), [visuals/comparison/](visuals/comparison) (Blender vs browser), [visuals/camera/](visuals/camera), [visuals/lod/](visuals/lod) |
| 3 | Corrected pedestrian-network specification | [02-pedestrian-network-spec.md](02-pedestrian-network-spec.md), [json](pedestrian-network-p2a.json), [nodes](pedestrian-network-p2a-nodes.csv), [edges](pedestrian-network-p2a-edges.csv) |
| 4 | Camera validation results | [03-camera-validation.md](03-camera-validation.md) |
| 5 | Lighting/material improvements | [04-lighting-and-materials.md](04-lighting-and-materials.md) |
| 6 | Revised performance measurements | [05-performance.md](05-performance.md) |
| 7 | First P2-B construction batch (built: Exchange Hall + court; proposed: D3 Pasar Awan) | [06-p2b-batch1-proposal.md](06-p2b-batch1-proposal.md), [asset-registry.csv](asset-registry.csv), [production-config.json](production-config.json) |
| 8 | Dependencies and risks, approval checkpoint | [07-dependencies-risks-approval.md](07-dependencies-risks-approval.md) |

Code: `merchant-citadel-p2a/` (preview, tests, GLB, data, evidence), `docs/planning/merchant-citadel/p2a/blender/` (data, hall split, kit export with AO and module LOD, world scene, comparison and registry scripts).

## Headline

* **Circulation:** 28/28 nodes standable, 34/34 edges pass both ways; N17 moved to the centre of the veranda gap, B04 moved 1.2 m so the cross street is 4.2 m and centred on its junction, the market cross kept with 3.85 m either side.
* **Camera:** production camera untouched; thin posts and (re-confirmed) cloth, signs, pennants stay out of camera collision; a preview-side character fade removes the back-on-the-lens view in the compressed spots.
* **Visual:** a mirrored sun was the main lighting error (MAE 23–26 → 9); Neutral tone mapping and baked vertex AO added; the Exchange Hall now reads like the Blender render.
* **Exchange Hall:** five reusable modules, 59k triangles, 23 collision proxies, stairs/porch verified.
* **Performance (Apple M4 Pro, honest method):** 3.0–5.9 ms per frame at 720p, 12.6 ms at 4K; 308k triangles, 335 → 123 draw calls merged; kit triangles −31 % and GLB 17.4 MB after module LOD. **No lower-end hardware available**; software rendering (SwiftShader) ≈ 1 s per frame is a stress bound only.
* **Not done / not verified:** human playtest, lower-end hardware, the fade in motion or on the island, hall interior, batch 2 construction.
