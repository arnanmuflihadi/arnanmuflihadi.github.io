# 01 — Asset research, verification and licences

Downloads were made only from the sources the brief named, into an ignored workspace (`.asset-inspection/merchant-citadel-p1/p3b2/`), inspected as data (`source/p3b2_inspect.py` parses glTF JSON and buffers; nothing downloaded was executed), and only then copied into the preview. **No asset was purchased, no paid tier used, no AI generation used.** Full per-file register: `evidence/asset-register-batch2.csv` (145 rows: source, URL, file, licence, role, triangles, bones, clips, status). Inspection data: `evidence/inspect-*.json`.

## What each source actually gave

| Source | Result | Licence as found |
|---|---|---|
| **Quaternius Stylized Nature MegaKit** (itch.io, free **Standard** tier, 104 MB zip) | **Used.** The pack's own `License_Standard.txt` says the free version holds **68 of 116 models** (the itch page says 81, the site says 116): 5 common trees, 5 pines, 5 twisted trees, 5 dead trees, bushes (plain and flowering), ferns, plants, clovers, flowers, 4 grass types, mushrooms, 3 medium rocks, pebbles, path stones, petals. No cliffs, no large rocks, no cattails (Pro only). glTF + textures (2048 px). | CC0 1.0 |
| **Gobkit free animals** (`gobkit.com/api/free` manifest, direct GLB) | **Retired (owner decision D1): only the Swallowtail butterfly is still used.** First version of this batch. 381 free CC0 models in the manifest. 36 animals were downloaded; 27 species/entries are used. Rigged (16-bone skeleton), named clips `idle`, `walk`, `attack`, `dead` (1.208 s, 24 fps, looping except `dead`); the insect packs add 23 clips including `fly` and `perch`. **No bird has a flight clip.** Authored facing +Z. Raw bounds differ by four orders of magnitude (0.04 to 460 units): every model is normalised at load from its posed bounds. | CC0 1.0 |
| **Gobkit nature kit** (41 static GLB) | 3 cloud models used (cloud deck). The rest **rejected**: 3-70 triangles per tree/rock/cliff, far simpler than the Quaternius flora (the brief warns against mixing). | CC0 1.0 |
| **Quaternius animals via OpenGameArt** (Farm Animals, Animal Pack Vol.2, Animals Pack: see [08](08-animal-source-change.md)) | **Used for all animals except the butterfly** (13 species: cow, horse, llama, pig, pug, sheep/lamb, cat, dog, red fox, chick, songbird, eagle). Converted from the `.blend` files (FBX loses clips). CC0 1.0 (farm pack: `License.txt` in the zip; the other two per the OpenGameArt pages). | CC0 1.0 |
| **Quaternius Ultimate Animated Animals / Farm Animal Pack / Ultimate Crops** (Google Drive versions) | **Not obtained.** The pages link to Google Drive folders that could not be fetched non-interactively (no file names or direct downloads reachable without the browser sign-in flow). Gobkit supplies animated animals instead; no crop models were needed (Bush_Common is used as the tea-row plant, see 02). | CC0 per the pack pages (not verified from files) |
| **KayKit Forest, Kenney Nature Kit, Poly Haven, OpenGameArt, itch tags, Sketchfab, Poly Pizza** | **Not downloaded or evaluated.** Quaternius flora (compatible with the Quaternius architecture of the town) and Gobkit fauna covered the brief; I did not want a third style. | n/a |
| Visual references V01-V03 | studied only through their pages' descriptions where reachable; nothing copied. | n/a |

## Verification notes that changed decisions

* `Leaves_TwistedTree.png` (used by twisted trees and every bush) is **pure white**: it is a mask whose colour came from vertex colours and the pack's Pro shader. With the plain PBR material it rendered white; a documented albedo multiplier makes it green. `_C` variants are red. The tint table lives in `merchant-citadel-p2a/flora.js` (browser) and `source/p3b2_blender_render.py` (Blender) so both renders agree.
* The Quaternius leaf textures are pastel and designed for a toon shader; under this scene's lighting they blow out. Same multiplier table (leaf 0.50-0.62, rock warm 0.92/0.80/0.66, bark 0.85).
* Texture memory: 2048 px textures were downscaled (bark/rock 1024, leaf/flower 512, grass 256) and normal maps dropped: 12 textures, about **35 MB GPU estimate** (with mips) against several times that at the shipped sizes (not measured).
* Tree triangle counts (3.2-10 k) are heavy for a browser: trees carry an L1 level made by collapse decimation (about 33 %, twisted 20 %), see `evidence/` flora stats: CommonTree_1 6,265 -> 2,067; Pine_1 3,947 -> 1,302; TwistedTree_2 9,134 -> 1,826.
* (Gobkit stage, now retired) Animal rigs: 24 of 36 have named bones (`Head`, `LeftHand`, `RightHand`, ...), **12 have obfuscated bone names** (BrahmaChicken, Budgie, Eland, Frigatebird, Goldenpheasant, Kingfisher, MerinoRam, Mouflon, Pigeon, Puffin, SebrightBantam, SkullDeer). Procedural head-down grazing and wing flapping are therefore impossible on those: they are perch/walk/idle only and never fly.
* (Gobkit stage, now retired) Style: the animals were **chibi toys** (large heads, tiny limbs), clearly different from the realistic-stylised Quaternius flora and the architecture. This is a `PREFERENCE` call for you (see 06). Apparent size is boosted (ground x1.35, birds x1.5, butterflies x1.7) because at the follow camera's 11.8 m true-scale animals disappear.

## What is custom

All earlier custom geometry (terrain, cliffs, props) from batch 1. New in batch 2: the Cloudfall mist/foam effects (procedural), terrain detail shader, scatter and habitat layout code, animal state machines, procedural wing/head offsets. No third-party code was added.

## Inspection sheets (Blender)

`visuals/inspection/flora-sheet.png` (33 flora models from the exported library), `visuals/inspection/fauna-rest-pose-sheet.png` (all 36 downloaded animals at rest pose, normalised to 1.2 m). Animation checks in the browser: `visuals/animation-sheets/` (ground species idle + two walk poses, birds with flap phases, butterfly fly/perch, `p3b2-flaptest.jpg`: wing bone axes).

## Update after the animal source change

The asset register (`evidence/asset-register-batch2.csv`) marks the 36 Gobkit animals `replaced` (Swallowtail `used`) and lists the Quaternius animals with clips and statuses. The animal rigs in use: farm animals + pug have named bones (`Neck`, `Head`, ...); cat, dog, fox, chick, songbird and eagle have generic bone names, so no head-pitch grazing is possible on them. Apparent-size boost removed (natural size, `?wscale` review knob).
