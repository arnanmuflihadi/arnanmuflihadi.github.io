# 02 — Whole-town visual review (Blender and browser on the same geometry)

## Method

Fourteen cameras (ten town views t01–t10, four terrace close-ups c01–c04), defined once in `scene.json` and rendered twice from the same GLB-equivalent geometry: Blender Eevee (the P1.4 look) in `visuals/blender/`, the Three.js preview with the game's real controller, camera and character in `visuals/browser/`. `visuals/comparison/` pairs them with mean luma; `visuals/before-after/` is a 2 × 2 sheet per view (batch 4 state vs batch 5 state, both renderers; 14 sheets); `visuals/before/` holds the batch 4 renders. Camera positions are in `scene.json` → `views`. The scores below are my provisional reading, **not an approval**.

## Views and what I saw (looked at in the matched pairs)

| View | Reading | Open point |
|---|---|---|
| t01 town aerial | the town reads as one compact settlement with a clear axis to the hall; roof colours are varied enough; the hall's tower is visible at the head of the axis but the hall is **not dominant from this height** (it is a similar-size roof mass to its neighbours) | owner judgement: is aerial dominance wanted, or is street-level dominance enough? |
| t02 southern arrival | (not looked at one by one in this write-up; see the contact sheet) | human check |
| t03 Merchant Street | **strong at street level**: the hall and its clock tower sit at the end of the street axis, framed by bunting and awnings, so the hall *is* dominant from the player's viewpoint | — |
| t04 Central Bazaar | (not looked at one by one in this write-up) | human check |
| t05 Artisan Lane | brick lane, stone corner, bench and barrel props, roof grades vary; reads as a working lane | the alley between B10/B11/B12 is tight (03); the green ground strip beside the lane is a stand-in |
| t06 Warehouse District | stone walls with doors, shutters, hoist, workbench with scales; the plain-wall complaint is addressed at this distance | north face of E04 not shown by this camera |
| t07 Tea Route | tea-house veranda, ivy and a fence give a distinct, quieter identity | **flat green ground and a bare fence dominate the lower half of the frame**; the leaf sign is not visible from this camera, needs a human look at 4–6 m |
| t08 Civic Terrace | **strongest view**: the hall stands at the head of the terrace, tower houses and banners frame it, the seal paving marks the centre | — |
| t09 hall approach | (not looked at one by one in this write-up; podium, steps and rail shown in c04 and t08) | rail closes the doors (01) |
| t10 lookout to terrace | (not looked at one by one in this write-up) | human check |

In Blender versus browser mean luma differs by 2–8 of 255 on the pairs I checked (t08 140 vs 138, t01 120 vs 117, t06 102 vs 105, t07 111 vs 109, t05 123 vs 116, t03 104 vs 112). Differences: the browser's character (a real model) versus Blender's marker, the sky gradient, and cooler paving in shade (01).

## Consistency of the town's visual language (provisional)

* **Consistent:** one palette (burgundy, blue, gold, terracotta, cream plus the tea-green accent on E05), one pack family, one baked-AO look, signs as flat pictograms, banners as the civic marker.
* **Varied on purpose:** three roof grades (terracotta, dark civic, weathered), three wall mixes, ridge directions.
* **Weaker:** (a) repeated whole buildings (A04 ×3 etc., 10.7 % of placed triangles in batch 4) are recognisable from the aerial; (b) the ground, sky and vegetation are stand-ins, so the town floats on flat green; (c) paving is slightly cool in shade in the browser; (d) there are no interiors.
* **Not judged by me:** whether the style is "good". That is the owner's.

## Limits

In this write-up I looked closely at the matched pairs for t01, t03, t05, t06, t07 and t08; the rest are marked above. A look at every pair by a human is part of the review. No lower-quality renderer, no other GPU.
