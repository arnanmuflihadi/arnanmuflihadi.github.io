# 03 — Visual quality and comparison with the P1.4 concept

**Status of the judgement:** provisional internal observation by the executor. It is not owner approval. Numbers are supporting only: a numeric match has already hidden two real defects in earlier phases (white banners, a mirrored sun), so every claim below was checked on the images.

## 1. One geometry in every view

All seven required views were rendered from **the same assembly**: Blender from `p2a_world_scene.py` (the same kit scripts, same positions, same signs as separate placed objects) and Three.js from the GLB exported by `p2a_kit_export.py`; same cameras, same field of view, same explorer position (Blender shows the cyan capsule at the explorer's position). The sheets are in [`visuals/comparison/`](visuals/comparison) (Blender left, browser right); the stills are in `visuals/blender/` and `visuals/browser/`.

| Required view | Sheet |
|---|---|
| Elevated overall bazaar | [cmp-p3-bazaar-aerial](visuals/comparison/cmp-p3-bazaar-aerial.jpg) |
| Central aisle at eye height | [cmp-p3-aisle-eye](visuals/comparison/cmp-p3-aisle-eye.jpg) |
| Gameplay camera (follow camera; the browser still is the live camera) | [cmp-p3-gameplay](visuals/comparison/cmp-p3-gameplay.jpg) |
| Western Hall entrance | [cmp-p3-west-entrance](visuals/comparison/cmp-p3-west-entrance.jpg) |
| Eastern Hall entrance | [cmp-p3-east-entrance](visuals/comparison/cmp-p3-east-entrance.jpg) |
| Interior / covered passage | [west](visuals/comparison/cmp-p3-west-interior.jpg), [east](visuals/comparison/cmp-p3-east-interior.jpg) |
| Street level toward the Exchange Hall | [cmp-p3-axis-to-hall](visuals/comparison/cmp-p3-axis-to-hall.jpg) |
| Surrounding shops | [east shops B14/E06](visuals/comparison/cmp-p3-shops-east.jpg), [potter E07](visuals/comparison/cmp-p3-shop-e07.jpg) |

## 2. Against the approved concept (before / after)

[ba-view-c-central-bazaar](visuals/before-after/ba-view-c-central-bazaar.jpg) and [ba-view-c2-bazaar-eye](visuals/before-after/ba-view-c2-bazaar-eye.jpg): columns = **P1.4 concept (the approved Blender image) | Blender of the closeout slice (halls missing) | Blender after batch 2 | Three.js after batch 2**.

* **Faithful:** the two halls stand where the concept puts them, at the same size, with the same terracotta-on-timber roofs, the same striped rows in front, the market cross between, and the Exchange Hall at the end of the axis. Palette and materials are the P1.4 ones (blue and burgundy cloth, red-brick accents, cream plaster, dark civic roof tile).
* **Better than the concept:** the concept's two halls are one repeated shape; they are now two buildings (section 2 of `01`): an open produce arcade with blue awnings and a windowed shop-hall with burgundy awnings, a red-brick threshold at each entrance, per-building trade signs, and coherent merchandise zones. The brick thresholds and the colour tie to the neighbouring rows make the district read as planned.
* **Not a brightness change:** the lighting is identical to the closeout (sun direction from the Blender light, Neutral tone mapping, same exposure); the improvement is in the architecture. The two views of the same halls differ only by the buildings.
* **Mean luma Blender / browser** (support only): aerial 109/112, aisle 131/136, gameplay 108/112, west entrance 118/116, east entrance 112/120, west interior 75/84, east interior 77/85, axis 121/126, shops 126/128, potter 102/113.

## 3. Ambient occlusion: does the lighter bake help?

P2-B asked whether a lighter bake improves consistency. Three bakes of the same kit were compared at matched mixes ([sheet](visuals/ab/ao-bake-A-B-C.jpg)):

| Bake | Strength / floor | Vertices clamped at the floor | Mean AO | Shader mix | Look |
|---|---|---|---|---|---|
| A (closeout) | 0.9 / 0.2 | **56 %** | 0.41 | 0.45 | reference |
| B | 0.6 / 0.2 | 42 % | 0.47 | 0.70 | same |
| **C (adopted)** | **0.4 / 0.3** | **0.8 %** | 0.62 | **0.80** | same |

**Finding:** to the eye the three are indistinguishable at the matched mixes, so the lighter bake does **not** make the pictures look better. Technically it is better: the closeout bake had more than half of all vertices pinned at its floor value (flat dark zones with no gradient), now almost none, so the AO is a real gradient that can be tuned in the shader (`?ao=`) without re-baking. C is the final bake (`p2a_kit_export.py` defaults 0.4/0.3, mix 0.8 in `p2a.js`).

## 4. Lighting and pipeline retained

Sun direction `(0.441, −0.616, −0.653)` (the Blender light in three axes), Neutral tone mapping, baked `_AO` into indirect light only, sky gradient and exposure from the closeout; shadow frustum now fitted to the built area. Shadow map: see 05 ([1024 / 2048 / 4096 crops](visuals/ab/shadow-map-1024-2048-4096.jpg): 1024 visibly soft, 2048 and 4096 close; **2048 is the default**).

## 5. Remaining visual issues (honest list)

1. **Paving and ground:** the browser paving reads lighter and bluer than the Blender cobbles; the ground and sky around the district are stand-ins (flat green plane, gradient sky).
2. **Hall roof undersides:** the interior shows large plain brown roof surfaces; the east hall reads well because of the cloth wall and rug, the west hall's interior is sparse at the north end (bench, hay) and could take one more story element.
3. **Perimeter shops** (B14, E06, E07) stand on thin paving with grass behind; their lanes need the surrounding districts' paving and the east lane's vegetation (not in scope).
4. **Interior floor:** the hall floor is the court brick tile; the red-brick threshold stops at the arcade line.
5. **Hall doors/windows do not open.** No interiors beyond the arcades.
6. **Repetition left:** both halls share the roof, posts and seal by design; the three shops share two archetypes (A04 twice, A04b once) differing only by sign, turn and position.
7. **Vertex AO is soft on large faces** (a roof or wall plane takes a gradient between its corner values).
