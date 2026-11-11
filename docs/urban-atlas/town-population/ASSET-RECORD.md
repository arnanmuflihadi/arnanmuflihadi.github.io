# Transit Kingdom — CC0 environment props

New selection: **16 actual Kenney models** plus the **existing Quaternius fern**, reused without redownloading. No new building, speculative model or paid asset. Native Blender editing was unnecessary: this phase selects existing meshes, normalizes metric transforms and places cached imports in the existing game.

| Source | Verified rights and actual files |
|---|---|
| [Kenney Furniture Kit](https://kenney.nl/assets/furniture-kit) | Official live page CC0. Downloaded through “Continue without donating”; retained ZIP 5,130,729 bytes. Bundled `furniture/License.txt` says Furniture Kit **2.0**, while the web update label says 1.0. Actual bundled notice governs recorded edition. Nine chosen GLBs, with real mesh geometry and material factors. |
| [Kenney Food Kit](https://kenney.nl/assets/food-kit) | Official page and bundled `food/License.txt` both CC0; edition 2.0. Retained ZIP 4,606,270 bytes; seven selected GLBs and their referenced `Textures/colormap.png` verified. Atlas embedded into the delivery GLB. |
| [Quaternius Stylized Nature MegaKit](https://quaternius.com/packs/stylizednaturemegakit.html) | Existing verified free Standard `Fern_1.gltf` derivative, `assets/game/scenery/fern.glb`; source hash/rights remain in the existing scenery source manifest and retained `stylized-nature-megakit-LICENSE.txt`. Three additional placements reuse the already-loaded geometry/material. No Pro/paid preview assets assumed available. |

[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) permits modification and redistribution, including raw delivery assets in a public repository. Attribution is optional; Kenney and Quaternius are credited. No ownership is claimed over their original models.

The local library was inspected first: existing project-authored café sets/benches and verified Quaternius planters/vegetation are retained. No local dedicated food/furniture pack existed. Only the two missing prop packs were acquired. Fantasy Props MegaKit was evaluated on its official page: the free Standard subset is not the entire pictured pack. No files from it, Poly Haven or paid editions are used.

Archives and original extracted files stay unchanged under `source-assets/town-population/`. Selection paths, file/archive/license SHA256, source URLs, per-model geometry and normalized dimensions: [sources.json](../../../assets/game/town-population/sources.json). Counts/use: [ASSET-INVENTORY.csv](ASSET-INVENTORY.csv). Authoring step: [prepare.mjs](../../../validation/town-population/prepare.mjs), using the already-installed glTF tools; no dependency installation.

Delivery: `assets/game/town-population/props.glb`, **117,052 bytes**, 16 model roots, eight shared materials, one embedded food atlas. Furniture receives a restrained timber, jade and foliage palette; no transmission, new lighting, postprocessing or alpha vegetation shader is introduced. The reused fern retains its existing alpha material. An indoor floor-lamp candidate was rejected after the first in-game visual pass and is not included in the delivered model library.
