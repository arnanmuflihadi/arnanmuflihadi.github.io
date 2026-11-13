# 07 — Polish plan (proposed P3-B batch 3). PLAN ONLY: nothing here is started or authorised.

Input: owner approval of batch 2 as the base, "plan polish". Source of every item: the defects in [06](06-defects-risks-roadmap.md) and the measurements in [04](04-validation.md) and [05](05-performance.md). Rule for the batch: each work package ends with a visible before/after in the real browser, the existing regression suite re-run (17 routes, 65 network edges, wildlife simulation), and a frame-time check; no package is accepted on a test result alone.

## Decisions needed before work starts

| # | Decision | Why it matters | My recommendation |
|---|---|---|---|
| D1 | **Animal style.** (Decided: **change source**; see [08](08-animal-source-change.md): Quaternius farm/pack animals obtained and verified, species coverage and the hybrid-or-Quaternius-only question still open.) Original question: keep the Gobkit chibi animals, or change source? | They are the biggest style mismatch (06 #1). Quaternius Animals would need *you* to download the Drive folders (not fetchable here); no paid pack without your authorisation. | Keep them for this batch, fix readability and motion (WP5), revisit the source when the town and flora style is final. |
| D2 | **Cliffs.** Custom Blender rock formations, or buy the Stylized Nature **Pro** tier (cliffs, big rocks) | Pro adds the missing cliff and large-rock meshes; it costs money and needs your authorisation. | Start custom (WP3); buy Pro only if the custom hero rocks fail review. |
| D3 | **Production touch.** May the batch propose (not apply) changes to the game's collision/bounds modules? | Batch 1/2 collision and the town corrections are preview-side only (the game's `blocked()` is limited to ±105 m). | Allow a written proposal and a patch file in WP8; no production edit without a separate go-ahead. |

## Work packages in order of visual return

| WP | What | Fixes | Approach | Accepted when | Size |
|---|---|---|---|---|---|
| **1 Ground and paths** | Sharp path edges, readable terraces, no stains | 06 #6 | A decal/splat layer for paths, bench risers and tea rows (texture-free where possible: signed-distance paths in the terrain shader from the same path definitions); soil colour only under rows; edge pebbles aligned to the new edge | at the follow camera and at 1.65 m eye height the path border is crisp; no new texture over 2 MB; mesh-vs-physics numbers unchanged | M |
| **2 Foliage shader** | Replace the tint hack, add life | 06 #10, risk "tint multipliers" | One stylised foliage material: per-instance colour variation (instance colour), wind sway in the vertex shader, leaf-card softening; keep the near-lens dither | tints gone from `flora.js`; Blender and browser agree without a multiplier table; frame-time cost <= 0.5 ms at the Green and the crag bench | M |
| **3 Cliffs, crag, underside** | The weakest large-scale element | 06 #8, #5 | Custom hero formations in Blender (Cloudfall notch, quay prow, crag face, 2-3 underside masses with overhangs), blended into the shell by vertex colour and normal; a real strata geometry at the cliff top band; fix the smooth crag dome (more benches, scree, dead trees) | side/underside and crag views visibly different from batch 2 in the comparison sheets; shell triangle budget +25 k at most; walk mask re-exported and routes still 17/17 | L |
| **4 Cloudfall** | The brief's "main attraction" | 06 #5 | Three layered falling sheets with animated edge foam, spray particles, a wider lip with a visible pool/ledge, stream depth and bank vegetation; softer cloud puffs replacing the faceted ones | the fall reads as volume from the overlook and from the east approach; draw-call cost <= 12 | M |
| **5 Wildlife readability and motion** | Make the animals worth watching | 06 #2-#4 | Measure foot sliding and tune clip speed to stride; turn-in-place; sleeping/resting pose by spine and head offsets; small hop for perch-only birds; softer apparent-size boost per species; a faint contact shadow so tiny animals anchor; a `dragon-near` event hook so fleeing/flying reacts when a dragon exists (stub only); **no new species, no higher counts** | foot-slide measured per species (target < 15 % of stride) and reported; encounter stills at the follow camera show each species clearly; wildlife simulation still zero violations | M |
| **6 Scale and performance** | Be ready for more islands | risks in 06 | Spatial cells for flora instead of a flat bucket; extend the shadow frustum with a second near-player cascade (trees and animals outside the town get shadows); WebP/KTX2 test for the 10.9 MB flora GLB; test a throttled/low-end profile (CPU/GPU throttle in the browser, and a real second device if you can provide one); prototype animation instancing only if a test with 200+ agents shows need | p50 and p95 reported on the throttled profile; flora GLB size reported with and without WebP/KTX2; no regression at the 9 existing cameras | M |
| **7 Camera tight spots** | Remaining camera findings | tea veranda 1.49 m; crag upper/summit/podium bank 2.8-2.9 m | A veranda-specific camera volume or post-spacing rule, tested like the eave rule (before/after sweeps); crag summit approach re-framed | each spot >= 3.0 m or the cause documented as accepted | S |
| **8 Production hand-off** | Close the preview-only gaps | batch 1 deviations | Written proposal and patch files (not applied): terrain-aware collision and bounds >= 147 for the game, the town corrections moved into the kit/proxy data, the 12 rig-name findings, the asset register as production data | patches apply cleanly to a scratch copy and the regression suite passes there | S |

Order: 1 -> 3 -> 4 (the three largest visible gains), 2 alongside 1, then 5, 7, 6, 8. Sizes: S about one short session, M about one batch-2-sized slice of it, L the largest. A realistic batch contains WP1-WP5 plus WP7; WP6 and WP8 can be a second batch if D1-D3 change scope.

## Evidence the batch will produce

Before/after sheets for every WP (browser, same camera, same flags), the full regression re-run, a new performance table with the same 9 cameras plus the throttled profile, an updated asset register (any new source with its licence verified from the files), updated defect list with each item closed, deferred or accepted, and a short owner checklist.

## Explicit non-goals

No new quests, NPCs, combat or dragon controller; no increase in animal counts; no deployment or commit; no paid asset without your authorisation; no change to the 24 buildings; no edit of production modules without D3.

## Risks to the plan

Cliff work (WP3) is the only item that can change the walk mask and therefore every route test: it is scheduled early so the suite catches problems before polish piles on. The shader work (WP2) interacts with the existing tone-mapping patch and the baked AO attribute: it must be tested with `?tm=aces` and the default. Low-end measurement depends on a second device that I cannot provide myself.
