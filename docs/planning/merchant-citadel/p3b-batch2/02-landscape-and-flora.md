# 02 — Landscape: what was replaced, how the scenery is laid out

## Pipeline (all reproducible: `source/build_all.sh`)

`p3b2_prepare_flora.py` (resize textures, keep alpha masks) -> `p3b2_flora_build.py` (Blender: import the 33 selected models, L1 decimation for trees, export `merchant-citadel-p2a/assets-p3b2/flora.glb`, 10.9 MB) -> `p3b2_scatter.py` (deterministic, seed 20261113, ~4 s: distance fields on the batch 1 terrain grid, writes `data/island-flora.json`: 1,651 instances, 83 trunk proxies, 121 cliff-ledge rocks, habitats, perches, keep-outs). Batch 1 terrain, heightfield and walk mask are **unchanged**; only the vertex colours of the top mesh changed (tea rows). The old procedural trees, shrubs, rocks and tea hedges are off by default (`?flora=0` restores them).

## Placement rules (from the scatter, not hand-placed)

Trees in noise-modulated groves per zone (west wood, south-west and south-east groves, Green edges, crag pines and dead trees, hall rear, shoulder grove) with species mixtures; no tall trees inside the Tea Lookout view wedge; hero twisted trees frame the lookout and the Cloudfall overlook. Everything respects: rim >= 3 m, town solids >= 3-4 m, pedestrian routes >= 1.5-2.5 m, authored paths, stream, dragon-landing keep-outs, slope, and the walk mask. Understory (bushes, ferns, large plants, mushrooms) clusters around trees; meadow flowers/clover/grass are patch-noise driven and never grow through the quay paving.

| Zone / feature | What it got |
|---|---|
| **Tea terraces** | 6 contour benches: two rows of pruned `Bush_Common` (scale 0.42-0.56, stand-in for tea plants, **not botanically tea**) with a clover/short-grass strip between, flowers at bench ends; soil colour only in the planting rows (baked into vertex colours with the same contour wobble as the rows); the batch 1 sausage rows are gone. |
| **Counting Crag** | boulder fields (Rock_Medium x3, scale 0.9-3.0, 61/58/54 instances) on benches and foot, pines and dead trees on the flanks, 121 ledge outcrops half-buried in the cliff strata from the real shell rings. Pro-only cliff meshes were not available: the cliff itself is still the batch 1 shell. |
| **Paths** | pebbles and a few stepping stones (RockPath) on alternating sides; ferns and big plants along the stream. |
| **Cloudfall** | 46 soft mist sprites along and below the 24 m fall, foam streaks at the lip (procedural, no texture file), ferns/plants and rocks on the banks. The fall is still one animated white sheet. |
| **Sky Quay** | unchanged props; the first scatter grew weeds through the paving, fixed (nothing spawns at n < -26). |
| **Sky** | Gobkit clouds replace the flat white ovals (still faceted, see 06). |
| **Terrain shader** | grass/earth/paving/rock detail from batch 1 kept. |

## Camera in the groves

Standing in a grove put the follow camera inside leaf cards. Foliage materials now dither away inside 3.4 m of the lens (fully gone at 1.0 m): measured effect: the player-height encounters in `visuals/gameplay/` are readable. Trunks stay camera-transparent posts as before.

## Distance management

`flora.js` re-buckets instances by camera distance every 0.4 s or 3 m: trees L0 < 36 m, L1 out to 460 m; bushes/ferns < 60 m; flowers/clover/grass/pebbles 24-32 m; rocks always. Re-bucketing costs 0.025-0.067 ms each. At the Green about 390 L0 + 74 L1 instances are drawn (347 k flora triangles in that view).
