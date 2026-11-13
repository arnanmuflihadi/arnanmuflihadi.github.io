# R0-RESET-A — owner decision pending

**Recommendation: RE-SITE on the southern bench.** B offers a shorter civic route and much smaller support gaps. A saves trees and preserves a shorter highland relationship, but retains the difficult cross-slopes. Neither option is implemented. R0-C2 is paused.

[A — salvage plan](alternative-a.png): rotate the market within the current clearing; re-centre Telaga; move the Guild reservation onto its axis. [B — coordinated cluster](alternative-b.png): two arrival storefronts and two square-facing storefronts; Telaga and the Guild reservation share one axis. [Terrain and route sections](terrain-comparison.png) use identical scales.

| Measurement | A — salvage | B — re-site |
|---|---:|---:|
| Contiguous cluster envelope | 974 m² | 904 m² |
| Raw terrain under programme | 15.23–22.00 m | 12.59–15.68 m |
| Raw grade: median / p90 | 25.3% / 83.5% | 11.4% / 31.8% |
| Largest connected raw ≤12% patch | 137.2 m² | 452.2 m² |
| Estimated cut / bounded fill¹ | 260 / 511 m³ | 94 / 363 m³ |
| Remaining support gap after grading¹ | 0–3.50 m | 0–0.29 m |
| Arrival + civic route² | 32.5 + 41.5 = 74.1 m | 27.1 + 29.5 = 56.7 m |
| Arrival path / direct distance | 32.5 / 24.2 m | 27.1 / 18.3 m |
| Civic path / direct distance | 41.5 / 40.0 m | 29.5 / 28.0 m |
| Market spine grade / entry bend | 8% / 17.8° | 2% / 32.5° |
| Square / Guild entrance levels | 20.52 / 20.67 m | 14.23 / 14.38 m |
| Potential trunk conflicts: plots / all | 1 / 4 | 9 / 12 |


¹ Cut/fill are **raster estimates**, including the 4 m arrival corridor, assuming grading limited to ±1.5 m. They exclude feathering, door aprons and optional trails. Residual gaps are support requirements, not constructed foundations. Raw floor-to-ground conflicts range −1.48 to +5.00 m in A; −1.30 to +1.79 m in B. Raised-edge proxies before grading are 193 / 123 m, not engineered retaining-wall quantities.

² Route lengths measure proposed horizontal polylines, **not controller walks**. Both have two arrival bends and four small bends around the fountain; the civic visual axis remains straight. Arrival grades are 7.65% / 7.68%. No traversal success is claimed.

Both fit the four existing footprints, a **14 × 13 m square reservation** (182 m² for the existing 177.2 m² programme), a movable **10 × 8 m Guild reserve**, and a **6 m promenade**. Pavilion roof reserve: 4.6 × 4.2 m, based on the existing roof. Paving needs rearrangement; fountain and pavilion geometry remain reusable. Conservative model envelopes leave ≥6.45 m opposing clearance. Entrances face public space, with 2.4 m apron reservations and assumed 0.15 m thresholds.

Both reserve Market → fountain → Guild sightlines without a building terminating the axis. **Rendered visibility is unverified**, including tree crowns. The actual controller radius/height/step limit is 0.34/1.9/0.42 m; its 9.5 m follow camera needs later obstruction testing. Full orbit clearance is not established.

**Reuse and likely work:** four building meshes (102,636 source triangles / 76 primitives), fountain and pavilion (3,876 triangles) remain reusable. Both need derivative paving, guards, thresholds, supports and placement data. Legacy interfaces/foundations contain 15,172 triangles; new geometry/bytes and labour remain unmeasured. A may reuse part of the arrival works; B needs old-site restoration. Approximately six site-specific modules/data records need localized changes; renderer, controller, cache, terrain engine and portfolio remain reusable. No quoted financial cost is implied.

**Three decision risks:**

1. **Vegetation:** B has 12 potential trunk conflicts including arrival, versus A's 4; 9 versus 1 lie in building/Guild plots. These are relocation candidates, not approved removals. Understory/crowns are uncounted.
2. **Skyport elevation:** retaining its provisional Y=17.15 m deck leaves B's market entry 3.20 m lower. At the new arrival crossing near (27,60), a roughly 1.35 m difference could use eight ~0.17 m risers. A direct step-free deck-to-market route needs ≥40 m at 8%. No connector was built or tested.
3. **Highland:** B's direct shortcut is rejected (108.9% local raw grade). The drawn optional return uses the market entry and original arrival trail: about 98 m from the square, up to 28.3% raw local grade. A's shorter link is about 34 m but reaches 38.2%. Neither is a default civic route or a tested new path.

**Method/evidence:** accepted C1A.5 terrain via the existing C1C fixture: 13,313 vertices, 369 × 369 exact height samples at 0.5 m; route queries ≤0.25 m. Slopes use 1 m centred differences. Search covered linear/hub arrangements and local refinement, not an exhaustive optimum. The 8% civic ceiling and ±1.5 m grading budget are study assumptions. A higher southern shelf needed ~848 m³ programme fill, versus ~354 m³ on the selected bench.

[Measurements](../../../validation/reset-a/comparison.json) · [Route details](../../../validation/reset-a/layout-details.json) · [Preservation](../../../validation/reset-a/preservation.json). Prior real-browser [approach](../../../validation/circulation-c1c/03-market-square-after.jpg) and [oblique](../../../validation/circulation-c1c/06-circulation-oblique-after.jpg) evidence shows the subsequently rejected arrangement: local traversal repairs left the square beside the main spine and retained infrastructure clutter. Those images do not approve either proposal.

**1,135 checkpointed files unchanged.** No new game captures, regression suite, Blender edits, GLB exports or game changes. STOP for the owner's SALVAGE / RE-SITE decision.
