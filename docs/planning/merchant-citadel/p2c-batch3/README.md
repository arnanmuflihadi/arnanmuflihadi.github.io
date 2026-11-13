# Merchant Citadel — P2-B batch 3: Lorong Lentera, the south gateway, Western Hall polish, scalable rendering

**Status: PENDING HUMAN VISUAL AND TECHNICAL REVIEW.** 2026-11-12. Nothing is committed, pushed or deployed. The first island, the production controller/camera/character/collision modules (SHA-256 re-checked), the Exchange Hall, both market halls' structure and B14/E06/E07 are as accepted. No NPCs, quests, combat or dragon travel. Five of the 24 P1.4 buildings are still unbuilt (listed in 06); no further district is started.

## What was done

| Request | Result | Doc |
|---|---|---|
| Next connected district | **Lorong Lentera (D6) and the south gateway (D1): B10 smithy, B11 potter's shop, B12 joiner, E01 outfitter, E02 carrier's office.** Five of the ten buildings that were still missing; 19 of 24 now stand. Each is a variant of its P1.4 archetype with one added architectural device and its own working set, not a prefab repeat | [01](01-district-construction.md) |
| Selective Bazaar polish | Western Hall: guild seal on both inner gables, four pier lanterns, two more herb hangers, scales; no floor props added (the aisle stays clear). Paving warmed twice against measured Blender colours; the blue is reduced, not removed | [02](02-bazaar-polish-and-paving.md) |
| Scalable rendering | Unmerged vs district vs scene-wide vs 20/30/45/60 m cells, on a 24-building scene, shadows off/on, 3 interleaved repeats, draw calls, submitted triangles, frame time, CPU submit time, resident geometry. Default is now 30 m cells. WebP textures verified in the engine; geometry quantisation sized, not built | [03](03-rendering-merge-and-compression.md) |
| Gameplay QA | Network 38 nodes / 48 edges pass; 17/17 district routes; 104/104 solids; 360° sweeps; fade traces; one scripted real-keyboard session in the live page. **No human playtest** | [04](04-circulation-camera-collision.md) |
| Licence evidence | Syntaxes of Play CC0 page captured with date and hash; register updated (158 downloaded assets, 25 new, none unresolved) | [05](05-assets-licence-registry.md) |
| Backlog | [06](06-backlog-risks.md) | |

## Evidence

* Matched Blender | Three.js sheets for 16 views: [visuals/comparison](visuals/comparison); before/after (batch-2 kit vs batch 3 in the same engine and cameras): [visuals/before-after](visuals/before-after).
* Paving A/B/C: [visuals/paving](visuals/paving). Scripted real-key session stills: [visuals/camera](visuals/camera).
* Records: [asset-registry.csv](asset-registry.csv) (44 nodes), [asset-provenance.csv](asset-provenance.csv), [pedestrian-network-batch3.json](pedestrian-network-batch3.json), [production-config.json](production-config.json), [evidence/](evidence).

## Headline numbers

* Kit: 420,575 triangles (batch 2: 336,528), GLB 33.4 MB raw / 11.0 MB gzipped (27.0 / 9.1), 75 textures, ~95 MB estimated GPU texture memory, structural inspection ok.
* Circulation: the new door nodes keep 1.29-1.38 m beyond the body radius; lane walks never compress the camera (12.9 m); 3 m alleys compress it to 0.78 m with the character fade holding effective screen coverage over 25 % to 2.4-3.7 % of a 360° turn (raw 49-65 %).
* Rendering (Apple M4 Pro, 1280×720, 24-building scene with 5 surrogates): unmerged 8.7 / 13.8 ms (shadows off / on), 411 calls; 30 m cells 7.4 / 11.1 ms, 238 calls; district 7.3 / 10.5 ms, 204 calls; scene-wide 6.3 / 9.5 ms, 110 calls but 606k triangles in every view.

## Not done / not verified

Human playtest; any lower-end device (still none measured); the five remaining buildings; mesh quantisation and KTX2/Meshopt/Draco in the engine (decoders are not in the vendored three build; the npm tool that would have produced them was not permitted to run); ground, vegetation and sky are still stand-ins; the surrogate town is a performance stand-in, not a measurement of the finished town.

## Rebuild and run

```bash
python3 docs/planning/merchant-citadel/p2a/blender/p2a_data.py          # scene.json (buildings, collision, network, views)
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --disable-autoexec \
  --python docs/planning/merchant-citadel/p2a/blender/p2a_kit_export.py -- <inspection_dir> <out_dir> merchant-citadel-p2a/data/scene.json
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --disable-autoexec \
  --python docs/planning/merchant-citadel/p2a/blender/p2a_world_scene.py -- <inspection_dir> <out_dir> merchant-citadel-p2a/data/scene.json merchant-citadel-p2a/data <view names>
node merchant-citadel-p2a/server.mjs --port 4180     # then ?autotest=network|district|merch|hallcam|fademotion|scale|views|mergecells
```
The extracted licensed packs (`.asset-inspection/merchant-citadel-p1/extracted`) and the `.blend` sources are not in the review package. Batch 3 script changes: `p2a_bazaar.py` (five district variants, hall polish), `p2a_data.py` (buildings, district rule, nodes, dropped dressing), `p2a_kit_export.py` (paving warm, module LOD), `p2a_registry.py`, `p2a_provenance.py`, `p2a_webp_variant.py` (new).

## Review package

`../merchant-citadel-p2c-batch3-review.zip`: this folder, the Blender scripts, `merchant-citadel-p2a/` (final GLB, data, code, JSON evidence). Left out for size: evidence PNGs (the report images are under `visuals/`), the WebP variant GLB (`p2a_webp_variant.py` rebuilds it), the batch-2 baseline GLB used for the before images, the AO test GLBs, `.blend` files.
