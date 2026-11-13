# 06 — Known defects, risks and roadmap

## Visible defects (`VISUAL-DEFECT` unless marked)

1. **Animals are small in the gameplay frame** (`VISUAL-DEFECT`): after the swap to the Quaternius animals (D1 resolved: closer in style to flora and architecture, natural size) a cat, chick, pug, fox or songbird is a few pixels at the 11.8 m follow camera. `?wscale=1.3` previews larger animals; the default stays natural. Horses, cows and llamas read well.
2. **Thinner ecology** (`PREFERENCE`): 13 species / 65 agents, no deer, hare, goat or waterbirds; the pack roster limits it. The 12-animal Drive pack or another source would restore variety.
3. **Flight and idle quality**: flight uses real clips but the songbird is tiny and its wing motion subtle; fox, chick and songbird idle are held frames of a walk/flap cycle; no turn-in-place, eat or sleep clips; llamas do not graze.
4. **Foot sliding** is not measured (`UNVERIFIED`).
5. **Clouds** (Gobkit, faceted) read as ice shards from some angles. **Cloudfall** is still one thin sheet; the fall is a white strip with a mist blob, no volume.
6. **Soft vertex-colour paths and bench edges** from batch 1 remain (blurry path borders); the soil rows between tea bushes are smeared stains from some angles.
7. **Tea rows are `Bush_Common`** (a decorative bush), not tea.
8. **Cliff and underside** remain the batch 1 procedural shell with shader noise; Pro-only cliff meshes were not available; ledge rocks are a partial answer. The crag is still partly a smooth dome.
9. **Tea-house veranda** camera (1.49 m) still unsolved.
10. Quaternius leaf cards show as faceted cards when close; tints are one multiplier per family (no per-instance colour variation).
11. The Sky Quay is lightly dressed (planting is intentionally absent; props unchanged).

## Technical risks

* Population scale: per-agent skinned clones will not scale to many islands with hundreds of animals; plan GPU animation instancing or impostors beyond ~150 m before populating further (65 agents here).
* Flora is distance-bucketed on the CPU every 0.4 s (cheap here: 0.03-0.07 ms) but is not spatially partitioned; larger islands need cells.
* 10.9 MB flora GLB (PNG textures); WebP/KTX2 would cut it (untested).
* Shadows: frustum still fits only the town; trees and animals elsewhere get none.
* Tint multipliers are a fix for a shader mismatch; the proper route is a stylised leaf material.
* No lower-end device measured; worst case 10.7 ms at 720p on this machine.
* The preview-side collision and the load-time town corrections from batch 1 still have to be moved into production.

## Roadmap for further islands

1. Keep one authoritative model per island (terrain model -> GLB + grid + mask), then `scatter` (flora + habitats) as a separate, seeded step: both scripts are island-agnostic except the constants at the top.
2. Species library: a per-island habitat file (`habitats` block of `island-flora.json`) already carries species, home points, perches and keep-outs; the species table and state machines are reusable as is.
3. Next quality steps in order of visual return: (a) stylised leaf/ground shader to drop the tint hack and add wind; (b) a real waterfall volume and stream depth; (c) path/decal layer instead of vertex-colour paths; (d) cliff meshes (Pro tier or a custom set) and a better underside; (e) animal clip coverage (eat, sleep, turn) and a size decision for small animals; (f) cell-based culling and animation instancing; (g) dragon-aware flocking once the controller exists.
