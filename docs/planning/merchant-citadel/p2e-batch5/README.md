# Merchant Citadel — P2-B Batch 5: Civic Terrace completion and whole-town validation

**Status: delivered for human review. Not approved. Nothing committed, deployed or integrated into the game.** Executor: Claude Sonnet 5.5. Date 2026-11-13.

## In one paragraph

The last two buildings (B15 Merchant Assay Office, B16 Cartographer) are built, so the preview now holds all **24 real buildings with no surrogates** on the Civic Terrace composition around the unchanged Exchange Hall. Navigation, collision, camera and fade were re-run on the whole scene (network 65/65, routes 45/45, solids 271/271, platform 7/7 with explicit criteria), the descent-from-the-hall compression and the terrace-edge walk-off were fixed, a whole-town Blender and browser set was produced, and the town-to-terrain contract was derived. **Frame-time measurements were taken on a heavily loaded machine and are not valid; no lower-end hardware was available**, so no performance claim is made beyond draw calls, triangles, memory and file size.

## Documents

| File | Content |
|---|---|
| [01](01-civic-terrace-and-final-assemblies.md) | B15, B16, terrace composition, forecourt rail, final fixes |
| [02](02-visual-quality-whole-town.md) | whole-town visual review and consistency |
| [03](03-camera-collision-navigation.md) | navigation, collision, camera, fade; corrected platform reporting |
| [04](04-rendering-and-performance.md) | 24-building rendering costs; why the frame times are invalid |
| [05](05-optimisation-and-file-size.md) | GLB variants, quantisation, WebP, decode-at-load |
| [06](06-assets-licence-registry.md) | provenance, licences, registry |
| [07](07-terrain-interface-contract.md) | what the built town requires of the terrain |
| [08](08-backlog-risks.md) | backlog, risks, corrections |
| [09](09-guided-playtest-checklist.md) | what a human should try |
| [10](10-final-p2b-construction-review.md) | **final review: complete / provisional / needs judgement** |

Data: [production-config.json](production-config.json), [asset-registry](asset-registry.json), [asset-provenance](asset-provenance.json), [terrain-interface.json](terrain-interface.json), [pedestrian-network-batch5.json](pedestrian-network-batch5.json) with nodes and edges CSVs. `evidence/` holds every test result and `visuals/` every image (blender, browser, comparison pairs, before/after sheets, real-key camera shots).

## Run it

```bash
node merchant-citadel-p2a/server.mjs --port 4180
```

`http://127.0.0.1:4180/merchant-citadel-p2a/index.html` (see 09 for controls and switches). Scripts: `docs/planning/merchant-citadel/p2a/blender/` (`p2a_data.py`, `p2a_bazaar.py`, `p2a_kit_export.py`, `p2a_world_scene.py`, `p2a_registry.py`, `p2a_provenance.py`, `p2e_terrain_interface.py`, `p2a_quantize_glb.py`, `p2a_webp_variant.py`).

## Key numbers

24 buildings · 66 instances · 54 kit nodes · 588,064 unique triangles · GLB 46,517,600 B (14.5 MB gzip, SHA-256 prefix `9288a67693af`) · 30 m cells: 252 draw calls and 452 k submitted triangles per view on average, worst unmerged view 800 calls / 687 k triangles · textures ≈ 98 MB GPU estimate · hall tower 26.79 m vs tower houses 15.79 m.
