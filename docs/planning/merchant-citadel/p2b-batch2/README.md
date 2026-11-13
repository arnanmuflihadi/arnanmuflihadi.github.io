# Merchant Citadel — P2-B batch 2: Central Bazaar

**Status: PENDING HUMAN VISUAL AND TECHNICAL REVIEW.** Dated 2026-11-12. The remaining districts are **not** built and nothing here authorises them. Nothing was committed, pushed or deployed; the first island and the game's controller, camera, character and collision modules are untouched (SHA-256 unchanged); the Exchange Hall was not rebuilt.

Built in the isolated preview: **B02 Western Hall (provisions), B03 Eastern Hall (crafts and textiles), B14, E06, E07**, integrated with the existing rows, cross, inn and court, as two distinct market buildings (an open produce arcade and a windowed shop-hall), per-building trade signs, red-brick thresholds and per-hall merchandise stories. Loader: material cache, shader pre-warm, per-district merge with culling, fitted shadow frustum.

| # | Deliverable | File |
|---|---|---|
| 1 | Construction report, architectural causes and corrections | [01-construction-report.md](01-construction-report.md) |
| 2 | Asset dependencies, provenance, licensing, GLB inspection | [02-assets-and-provenance.md](02-assets-and-provenance.md), [asset-provenance.csv](asset-provenance.csv), [evidence/glb-structural-inspection.json](evidence/glb-structural-inspection.json) |
| 3 | Visual quality, matched views, concept comparison, AO test | [03-visual-quality.md](03-visual-quality.md), [visuals/](visuals) |
| 4 | Circulation, camera, collision, fade in motion | [04-circulation-camera-collision.md](04-circulation-camera-collision.md), pedestrian-network-batch2 files |
| 5 | Rendering pipeline and measured performance | [05-rendering-and-performance.md](05-rendering-and-performance.md) |
| 6 | Registry, dependencies, risks, limitations | [06-registry-risks-and-limitations.md](06-registry-risks-and-limitations.md), [asset-registry.csv](asset-registry.csv), [production-config.json](production-config.json) |
| 7 | Guided playtest checklist | [07-guided-playtest-checklist.md](07-guided-playtest-checklist.md) |

Preview: `node merchant-citadel-p2a/server.mjs --port 4180`, then `http://127.0.0.1:4180/merchant-citadel-p2a/index.html`. Code and data: `merchant-citadel-p2a/` (preview, loader, tests, GLB, evidence), `docs/planning/merchant-citadel/p2a/blender/` (reproducible scripts).

## Headline results

* **Assembled and placed:** all 5 buildings within 0.43 cm of the P1.4 envelopes; 14 of 14 slice buildings pass. GLB structural inspection passes (36 nodes, 341 primitives, 336,528 triangles, no missing attributes after two defects were found and fixed).
* **Circulation:** 32 / 32 nodes standable, 40 / 40 edges pass in both directions (N18/N31, N19/N32 included, nodes moved to the aisle centres), 19 / 19 bazaar routes pass including turning loops, the market-cross circle and a 42 s, 744° circuit; 51 / 51 merchandise and structure solids stop the player; posts solid for the body, excluded for the camera.
* **Camera:** the covered halls put the camera 0.94 m behind the player everywhere (P2-A roof proxy was a slab); a roof shell and a thin-eave rule give **4.0 m**; cloth/sign/pennant exclusion re-confirmed (circuit 0.91 m with cloth); the character fade flickered in motion and was smoothed.
* **Visual:** two distinct halls, same geometry in all views; the lighter AO bake looks the same but removes the clamping (56 % → 0.8 % of vertices at the floor).
* **Performance (Apple M4 Pro, honest read-back method, shared machine):** 6.5–8.5 ms unmerged/merged without shadows, 10.7–12.9 ms with, at 720p; 503 unmerged / 115 scene-merged / 195 per-district draw calls; 428k triangles in the worst view (+39 % over the closeout slice, about +1.1 to +2.2 ms). **No lower-end hardware was available.**

## Not done / not verified

Human playtest; any lower-end device; mouse-rotated camera round the new corners; fade look in real time and on the first island; the Syntaxes of Play licence page copy; mesh quantisation; distance LOD; the remaining districts.

## Review package

`docs/planning/merchant-citadel/merchant-citadel-p2b-batch2-review.zip` (29.7 MB): this folder, the P2-A/closeout documents and Blender scripts, `merchant-citadel-p2a/` with the final GLB, data, code and JSON evidence. Left out to keep it small: evidence PNGs (screenshots used in the reports are under `visuals/`), the AO A/B test GLBs, the unlowered-LOD test export, earlier-phase screenshots (already in the P2-A and closeout zips), `.blend` files.
