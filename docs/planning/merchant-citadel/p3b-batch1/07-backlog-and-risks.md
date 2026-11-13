# 07 — Remaining polish backlog, defects and risks

## Defects seen in the browser (`VISUAL-DEFECT` unless stated; images in `visuals/gameplay/`, `visuals/compare/`)

1. **Soft, blurry path and bench edges**: colour lives in vertex colours on a 2 m lattice, so path borders and the quay-court seam smear (`gameplay-contact-sheet`, rows 2 and 4). Needs a splat/decal layer or a finer colour mesh near paths.
2. **Large brown tea benches and crag flanks read as bare mud**: the laterite colour dominates, there is little ground cover; the tea rows are clean green sausages. Ground-cover, soil variation and row structure are polish work.
3. **Crag reads as a smooth dome from the summit approach** (row 3 right): rock detail is shader noise only, no hero rock formations; the stone marker is not visible from the approach. The Counting Crag is a backdrop at the hall, not yet a landmark up close.
4. **Cliff faces look like stretched noise from player distance** (no real strata geometry at < 20 m); the hanging roots and underside are good from afar, thin from below.
5. **Sky Quay is bigger than its dressing**: crane, beacon, props only at the edges (intentionally open for landing). No berths, retaining-wall detail, ropes or cargo story.
6. Procedural clouds are flat ovals from some angles; underside has no vegetation or waterfalls other than the Cloudfall (24 m, drops to the cliff base, no mist).
7. `CONFIRMED-TECH`: the camera is 2.79 m from the player at the crag upper bench, summit and the podium-shelf bank; the tea-house veranda stays at 1.49 m.
8. No shadows beyond the town's shadow frustum: trees and cliffs outside it receive none.

## Not done (and why)

Stair detailing of the arrival ramp; texture/trim sheets; vegetation LOD or wind; grass; water reflection, mist, sound; second bridge or rails along bench ends and the overlook (blocked by the walkability mask, so there are no visible rails); far LOD of the town; per-district recovery points; terrain streaming (the island is 3.2 MB and loaded whole); applying the corrections to the kit GLB and `scene.json` instead of at load time; checking other dressing rows for proxy/mesh offsets.

## Risks

| Risk | Status |
|---|---|
| Performance on lower-end hardware | **untested**; 868 k triangles submitted in flight views, 812 k at the arrival court; no far LOD |
| Physics is preview-side | the game's `blocked()` cannot be used for an island this large; a production integration needs the same terrain-aware collision and `bounds` ≥ 147 |
| Invisible rim / slope walls | walkability blocks steep ground and the rim margin instead of rails; if falling off must be possible somewhere, that needs designing |
| Camera tight spots at the crag and shelf bank | measured 2.79–2.9 m |
| Landing criteria are this phase's | the real system is absent; Caravan Green is eligible but with only 6 m free at its centre once dressed |
| Vertex-colour terrain | colours cannot be repainted without rebuilding; no baked AO on the island |
| One browser, one GPU, one machine under load | all measurements |
