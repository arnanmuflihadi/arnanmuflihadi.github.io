# R0-RESET-B1 — NO-GO recommendation

**Do not advance B under the current minimal-disturbance and tall-tree-preservation brief.** The bench can hold the programme, but neither of the two permitted arrangements resolves its tree/arrival conflicts economically. This is a design recommendation, not a claim that construction is technically impossible. Owner decision remains pending; R0-C2 stays paused.

The original **B0** remains the less costly studied configuration: anchor **X −1.000, Z 47.000**, forward **(−0.573576, −0.819152)**, angle **235° from +X toward +Z** (**325° bearing from north**). Market entry: **(9.324, 13.949, 61.745)** in game X/Y/Z metres. Square floor: **14.229 m**; Guild entrance reserve: **14.379 m**. Four original structural footprints, conservative model envelopes, 182 m² plaza, 10 × 8 m Guild reserve and 6 m promenade remain unchanged in size. The Guild wire envelope uses an assumed 11 m height, not an approved building design.

| Measurement | Original B0 | Only adjustment: +3.5 m laterally |
|---|---:|---:|
| Anchor X, Z | −1.000, 47.000 | 1.867, 44.992 |
| Entry elevation | 13.949 m | 16.509 m |
| Legacy point-buffer plot conflicts | 9 | 6 |
| Full trunk-collider plot/reserve intersections | 10 | 6 |
| Tree conflicts including model envelopes | 12 incl. arrival | ≥10; arrival not finalized |
| Trees ≥10 m high affected | 5 | ≥4 |
| Estimated programme cut / bounded fill | 48 / 354 m³ | 17 / 844 m³ |
| Maximum remaining support after assumed grading | 0.29 m | 2.96 m |
| Nearest programme corner to cliff lip | 14.85 m | 18.05 m |

Estimates reuse RESET-A's exact-sampler 0.5 m grid and ±1.5 m grading allowance; no terrain was graded. Volumes exclude edge feathering, door aprons and the arrival. The shifted cluster hits rising ground and needs a 2.56 m higher common datum. It is rejected. Full collider rectangles also catch T13 touching the Guild reserve, missed by the earlier centre-point buffer. Thus B0 still has **12 overall conflicts**, but **10 actual plot/reserve intersections**, rather than nine heuristic plot candidates.

**Arrival choice: retain the provisional threshold (A), if B is reconsidered.** From **(27,17.15,60)**, the paper route bends at **(20,58.8)** to avoid T61, then reaches the market. It spans **18.18 m horizontally**, descends **3.201 m**, and uses **two flights of nine 0.178 m risers**, 0.32 m treads, a 3 m clear width and landings at least 3.30 m long. Its stepped polyline is 21.38 m. Across the full 3 m corridor, 2,613 raster samples give maximum cut/support estimates of 1.32/1.22 m. Risers are below the existing 0.42 m step cap; **no actual stair traversal is claimed**. The skyport threshold is itself unbuilt.

Alternative arrival B places an on-axis threshold at **(12.192,14.861,65.840)**, a 15.92 m relocation. Its 5 m connection still needs six risers. A 15 m landing reserve behind it crosses the actual cliff lip (5 of 192 sampled points outside; maximum island fraction 1.007). This requires an overhang/support decision, so it is not the simpler demonstrated solution.

**Two blockers:**

1. **Forest loss:** B0 conflicts with 12 trunks; T3/T8/T11/T13/T16 are ≥10 m high. Preserve these in place; their conflicts remain unresolved. Seven smaller trees are only potential relocation candidates, requiring separate approval. No trees were hidden, moved or removed. The translated envelopes still intersect four tall-tree colliders, so it does not preserve two tall trees as the initial point test suggested. Height is a size proxy, not verified tree age. [Treatment inventory](../../../validation/reset-b1/tree-treatment.csv).
2. **Arrival composition:** actual browser views and ray checks show the skyport-to-fountain sightline blocked by foliage **and B2's mass**. The market itself reads as a street and its fountain ray is clear. The central square-to-Guild entrance and upper-reserve rays are also clear; adjacent crowns crowd the broader landmark frame. Do not describe the entire Guild sightline as blocked. No finished Guild appearance is demonstrated by a wire reservation.

All views use the existing renderer/world, unchanged lighting and real vegetation. Eye cameras sit 1.65 m above proposed floors; an additional follow reference uses 9.5 m. Proxies have **no support/collision**. No detailed building GLBs, new Blender work, new site search or production town movement occurred. [Screenshots](index.html), [layout measurements](../../../validation/reset-b1/layout-study.json), [arrival section](../../../validation/reset-b1/arrival-comparison.json), [full collider check](../../../validation/reset-b1/trunk-collision-check.json).

Rollback: remove `reset-layout=b1` and reload. The hook is localhost-only and default-off; the old town feature flags and approved asset transforms remain intact. To remove the study entirely, remove the three-line RESET-B1 import guard from `assets/js/floating-atlas/entry.js`; its phase-start copy is in `validation/reset-b1/entry.js.before`.

**Validation:** five 1440 × 900 browser captures; 90 terrain checks match RESET-A exactly; one renderer/scene; zero building GLB loads, hidden trees or new colliders. Original-ground walk/jump/landing, default-off, MBR and editorial smoke checks pass. 1,164 checkpointed files unchanged; only the localhost entry hook changed. Identical aerial overlay ON/OFF: 245/135 draw calls and 2,276,072/2,270,064 submitted triangles, including shadow passes and annotations. This is a static diagnostic, not a walking/GPU benchmark. [Checks and costs](../../../validation/reset-b1/checks.json). No unrelated regression suite ran.

**STOP. No relocation, construction or additional search is authorized.**
