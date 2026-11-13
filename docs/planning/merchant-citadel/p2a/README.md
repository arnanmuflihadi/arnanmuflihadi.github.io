# Merchant Citadel P2-A — production vertical slice

**Status: MERCHANT CITADEL P2-A — PENDING HUMAN VISUAL AND TECHNICAL APPROVAL.** Dated 2026-11-12. P2-B has **not** started and is not authorised by this package. Nothing was committed, pushed or deployed; the first island and all game code are untouched.

One representative commercial street segment of the approved P1.4 layout D, built from the verified external models, exported as a reproducible game-ready GLB and walked with the game's real, unmodified player controller and follow camera in an isolated preview.

| What | Where |
|---|---|
| Playable preview (isolated) | `merchant-citadel-p2a/index.html` via `node merchant-citadel-p2a/server.mjs --port 4180` → `http://127.0.0.1:4180/merchant-citadel-p2a/index.html` |
| Production GLB (15.2 MB, 17 kit nodes, 68 materials, 69 textures) | `merchant-citadel-p2a/models/merchant-citadel-p2a-kit.glb` |
| Slice data, height field, expected bounds | `merchant-citadel-p2a/data/` |
| Raw test evidence (JSON, screenshots) | `merchant-citadel-p2a/evidence/` |
| Blender build scripts (data, kit export, world assembly, comparison) | [`blender/`](blender) |
| Source Blender assemblies (85 MB and 95 MB, third-party textures embedded, **not in the zip**) | `.asset-inspection/merchant-citadel-p1/p2a/out/merchant-citadel-p2a-kit-source.blend`, `.../p2a/world/merchant-citadel-p2a-slice-source.blend` |
| Test results: scale, controller, camera collision, N16–N17, inn, platform | [01-test-results.md](01-test-results.md) |
| Performance and the reconciled triangle/material/draw-call/texture definitions, proposed budgets | [02-performance-and-budget-reconciliation.md](02-performance-and-budget-reconciliation.md) |
| Blender vs browser comparison and deviations from P1.4 | [03-visual-comparison-and-deviations.md](03-visual-comparison-and-deviations.md), [visuals/](visuals) |
| Reusable construction, material and collision rules | [04-construction-and-material-rules.md](04-construction-and-material-rules.md) |
| P2-B readiness, decisions, risks, how to run/rebuild | [05-p2b-readiness-and-risks.md](05-p2b-readiness-and-risks.md) |

## Headline results

* Scale and placement: all 8 buildings within 0.49 cm of the P1.4 Blender world; kit bounds within 0.005 cm; orientation 3/3.
* Controller: 14 routes simulated; street spine (walk/run) clean, both stair flights (1 m + 1 m, 0.22 m risers) ascended/descended walking, running and with a jump, 1 m drop landed.
* Camera: **cloth awnings, signs and pennants should not participate in camera collision** (cloth → 1.2–3.2 m, pennants → 3.3 m with pops); roofs/balconies/jetties do. Inn compression is the inn's own wall (8.2 m settled); the tea-house veranda and hall steps compress by geometry.
* N16–N17: node N17 sits 0.55 m from a veranda post and cannot be stood on; the veranda itself is passable (1.49 m clear). The B04–B05 alley is 1.34 m. The market cross blocks the straight spine.
* Performance (Apple M4 Pro, 1280 x 720, DPR 1): 268 draw calls as loaded, 91 merged by material; 315k triangles drawn; ~88 MB textures; frame time 0.4–2.1 ms. Fast-GPU result only.
* Visual: architecture and materials match; lighting finish is flatter (no AO, ACES vs Neutral). A white-banner export bug found in comparison was fixed.

## Not done / not verified

No human playtest, no low-end hardware measurement, no AO, Exchange Hall is a stand-in, shadow-pass draw calls not visible in `renderer.info`. See 05.
