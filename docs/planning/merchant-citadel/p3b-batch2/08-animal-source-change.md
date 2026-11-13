# 08 — Animal source change (decision D1): done, Quaternius-only

Owner decisions: **change the animal source** (the Gobkit animals read as chibi toys next to the flora and architecture), then **Quaternius only** (a smaller but coherent ecology). Implemented in this batch; the system, layout, validation, captures and documents were redone. Gobkit animals are retired (files removed from the preview; old evidence kept under `superseded-gobkit/`), only the Gobkit **Swallowtail** butterfly stays because no Quaternius butterfly exists.

## Sources

| Pack | Animals used | Licence evidence |
|---|---|---|
| Farm Animals ([OpenGameArt](https://opengameart.org/content/lowpoly-animated-farm-animal-pack)) | Cow, Horse, Llama, Pig, Pug, Sheep (+ Lamb = the sheep rig scaled) | `License.txt` in the zip: CC0 1.0 |
| Animal Pack Vol.2 ([OpenGameArt](https://opengameart.org/content/animated-animales-low-poly)) | Cat, Dog, Eagle | CC0 per the page (no file in the zip) |
| Animals Pack ([OpenGameArt](https://opengameart.org/content/5-low-poly-animals)) | Red Fox, Chick, small blue bird | CC0 per the page (no file in the zip) |

The 12-animal "Ultimate Animated Animals" and "Farm Animal Pack" on Google Drive were not fetchable; these older packs were used instead. Unused downloads (Zebra, Wolf, Piranha, Fish, Whale) were removed from the preview assets.

## Conversion findings (kept from the research step; `evidence/inspect-quaternius-animals.json`)

* FBX loses actions; the `.blend` files keep Death/Idle/Jump/Run/Walk/WalkSlow on the farm animals. Converter: `source/p3b2_blend_to_glb.py`.
* Diffuse BSDF colours are dropped by the glTF exporter and the farm animals carry an all-white vertex-colour layer; the converter rebuilds Principled materials and removes the layer.
* Eagle: `Flying` clip, 1,532 triangles. Songbird: flap action. Fox and chick: one walk cycle. Cat/Dog: Idle + Walking.

## What changed in the code

`wildlife.js` (species table, clip alias layer, natural size, real flight clips, per-animal wall margin, `?wscale`), `p3b2_scatter.py` (habitats; flora, trunks, perches and keep-outs verified identical to the previous data), `p3b2-tests.js` (species lists, new capture helpers `portrait`, `encounter`, `strip`). Old habitat data: `evidence/island-flora-gobkit-habitats.json`, `evidence/scatter-report-gobkit.json`.

## Fixes found while doing it

* The demo helper removed a real agent from the simulation on every call (`splice(-1)`); fixed (affected only inspection runs).
* Grazing head pitch had the wrong sign on these rigs (head went up); fixed and checked per species in `visuals/quaternius/animation-sheets/p3b-q-graze-pose-check.jpg`; llamas do not graze.
* A fixed 0.28 m wall margin was too small for horses and cows; now per animal.
* Birds in the tea terraces and Cloudfall had a single shared perch (no rock/tree perches there); pools widened to nearby roofs, stream boulders and trees.

## Honest limits

* Natural size makes small animals read as specks at the 11.8 m follow camera (cat, chick, pug, songbird, fox; see `visuals/quaternius/gameplay/*-close.jpg` vs the standard shots). `?wscale=1.3` is provided so you can judge a larger scale; it is not the default.
* The songbird is tiny and fast: the flight GIF mostly shows the landscape (`strip-bird-flight.jpg`); its flight cycle is validated numerically and in the portrait.
* Ecological variety is lower (13 species, 65 agents vs 27 species, 83). Deer, hare, goat, birds of prey other than the eagle etc. would need the Drive pack or another source.
* Foot sliding is not measured (clip rate follows speed by estimate); the fox/chick/songbird idle is a held frame of the walk/flap cycle.
