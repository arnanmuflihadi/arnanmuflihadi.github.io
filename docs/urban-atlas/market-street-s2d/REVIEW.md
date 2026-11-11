# S2-D — isolated Market Street integration proof

Technical evidence is ready. **Do not deploy this placement.** S2-C's conditional architectural approval is preserved; it does not approve the terrain fit or production integration. No production file, approved Blender source, source archive or license was changed.

Open [the isolated preview](../../../validation/market-street-s2d/index.html) through the existing local preview server. [Visual gallery](index.html). The default is authored transmission glass; the cheaper alpha-glass button is a clearly labeled comparison, not the delivered material.

## Export and preservation

- [Independent editable Blender master](../../../validation/market-street-s2d/market-street-export.blend): 6,033,566 bytes; saved, reopened and inspected through live Blender MCP. `S2C Market Street` retains its 947 objects; `S2D Optimized Export` contains 69 objects including its root. Originals S2-A/B/C remain byte-identical.
- [Optimized GLB](../../../validation/market-street-s2d/market-street-optimized.glb): **10,007,904 bytes**, 170,709 triangles including instances; 126,543 unique stored triangles; 21 glTF meshes / 107 render primitives / 37 material definitions / five embedded PNGs. Three.js creates 59 material variants for differing mesh attributes. Four distinct buildings load successfully.
- Native convert/join batches static geometry by building and public-realm role. Linked landscape geometry exports with `EXT_mesh_gpu_instancing`: seven canopy trees, twenty street ferns and shared palm components. All architectural triangles, roof detail, transforms and material identities are retained. No decimation or new asset acquisition.
- Delivery changes fern foliage from alpha blending to a 0.4 cutout. Glass transmission remains 0.96. The binary geometry/image chunk is identical to the live-MCP export; only material JSON changes. All five images decode, UV-dependent materials render, and there are no missing textures or browser errors.
- Coordinate conversion: Blender `(u,v,h)` → exported local Three.js `(u,h,-v)` → island `(36+u,18.6+h,44-v)`. One translation, no second axis conversion. Building counts and bounds are in the capture JSONs. Loaded geometry arrays occupy **9,637,842 measured ArrayBuffer bytes**, excluding image/GPU/driver memory.

## Matched visual inspection

[Street comparison](street-comparison.jpg) and [aerial comparison](aerial-comparison.jpg) place unchanged approved Blender captures beside actual browser screenshots. Cameras and 3:2 framing match; full source images are linked in the gallery. Browser drawing buffer: 1800×1200, DPR 1, antialiasing on, ACES exposure 1, PCFSoft shadows at 2048. Actual captured CSS image: 1265×843. Camera near/far: 0.12/1000 m; the existing follow-camera pose is reused during traversal. The preview's far plane is larger than the production follow camera's 460 m, and is unchanged across performance comparisons.

Arrival and detail cameras are 1.65 m above the lower terrace; opposite view is 1.65 m above the upper apron. Skyport camera uses the provisional deck Y=17.15, not the current natural ground. Each screenshot has a matching JSON with camera position, quaternion, lens/FOV, mode and settings.

The four silhouettes, roof tiles, timber frames, balconies, signage, paving and glazing survive export. Browser rendering has softer contact shading, warmer highlights and less tonal depth than the Blender render; Cycles GI/AgX does not transfer. No AO/postprocessing is used to conceal geometry. Island directional/hemisphere lights remain those from R0-A3; a small 256×128 gradient reflection environment is added for imported PBR materials. Original terrain, clouds, rocks, waterfall and vegetation remain in place. No geometry masking or vegetation removal is applied.

At player height the real forest replaces the art scene's blank sky termination. It is a green backdrop, but obscures the future square/Guild direction. This is not a finished landmark vista. [Island views and exposed foundations](island-evidence.jpg) show that limitation.

## Measured rendering costs

Apple M4 Pro through ANGLE/Metal, Chrome 156, same resolution/shadows/exposure in all runs. Each performance sample contains 360 real animation-frame intervals while the existing animated explorer/controller walks, using actual frame delta. CPU times cover renderer submission, not GPU completion. GPU time and GPU byte usage were not measured. JS heap snapshots are recorded in the raw JSON; garbage collection makes them unsuitable for attributing memory savings to glass.

| Scene / glass | Walking calls, all passes | Walking triangles, all passes | rAF median / p95 | Render CPU median / p95 |
|---|---:|---:|---:|---:|
| Isolated art, authored | 366 | 542,733 | 5.6 / 11.2 ms | 1.2 / 1.5 ms |
| Actual island, authored | 508–510 | 4,056,613–4,056,949 | 11.1 / 16.7 ms | 2.1 / 2.4 ms |
| Actual island, explicit alpha study | 339–340 | 2,672,362–2,672,530 | 5.6 / 11.3 ms | 0.9 / 1.1 ms |

Fixed arrival without the character: 321 calls / 512,127 triangles in isolated art; island 455 calls, observed as 145 shadow-target + 151 transmission-target + 159 canvas draws. The alpha study uses 305 fixed-frame calls and removes the transmission target. These are observed WebGL draw functions grouped by bound framebuffer, not assumed pass counts. Walking includes character geometry and changing visibility. The island loads roughly 1.44 million triangles before view/pass culling. Counts differ between resource inventory and submitted frames by design.

Five decoded asset images: one 512² and four 256². Isolated renderer texture count was 11 after character loading; island 17, including render targets/environment and other scene textures. The GLB compresses to 2,005,093 bytes with gzip in a file test, **but this preview served the 10 MB uncompressed GLB**. No compressed-transfer benefit is included in the timings. Model-cache reuse returns the same loaded asset with one request. Lower-power/mobile hardware is not tested.

## Terrain fit

Study grading is visible only in isolated-art mode. The island overlay hides all three proposed grading meshes and uses the exact unchanged terrain sampler. 990 building-footprint samples at 0.5 m spacing reproduce the S2-C support discrepancy.

| Building | Floor Y | Natural ground range | Floor-to-ground support needed |
|---|---:|---:|---:|
| Kopi Awan | 20.043 | 14.093–17.359 | 2.684–5.950 m |
| Lembaran | 20.234 | 15.924–20.026 | 0.208–4.310 m |
| Rupa Rimba | 21.960 | 14.577–21.390 | 0.570–7.383 m |
| Serambi | 21.960 | 15.606–21.026 | 0.934–6.354 m |

The floor is 0.24 m above each building's lowest base geometry, so the maximum visibly open gap below Rupa Rimba's base is about 7.14 m. The **7.38 m floor/support discrepancy is real**, not an axis conversion error. Current shallow skirts and pads do not solve it. A future approved design needs terrain-responsive structural plinths/stilts/retaining terraces, or local plot/floor adjustment; simply dropping this GLB into production is unsuitable. No terrain flattening is proposed as an automatic fix.

Nearest natural island boundary across sampled plot corners is 20.07–39.01 m; none of the plots lies beyond terrain support. Zero existing trunk/rock collision boxes intersect the four core footprints. This does not certify every foliage leaf: visible vegetation is retained and requires a final interface review. The main fall hazards are exposed terrace/plot edges and the raised route ends, not an absent island surface.

## Controller study and route proposal

Uses the existing `createCharacter`, player controller, animation clips, movement speeds, jump physics and follow-camera algorithm in this isolated preview. Supports come from the **actual exported upward triangles**, plus natural terrain in island mode. Existing slide/blocked logic uses building footprint proxies and original island tree/rock colliders; camera clearance additionally raycasts actual imported meshes. These are central-route tests, not complete production door/prop collision coverage.

| Test | Result | Evidence |
|---|---|---|
| Isolated stairs uphill/downhill | PASS | About 33.81 m / 16.17 s each; no jump required; max riser 0.174286 m |
| Island stairs uphill | PASS | Same controller reaches upper apron on actual mesh support |
| Raw natural-ground skyport approach | FAIL | Stops near `(31.235,16.208,52.000)` at raised garden-path start |
| Square exit / return | FAIL as a two-way connection | Exit reaches terrain after 0.891 m support drop and a fall/landing; return blocks at Z≈8 |
| Jump on the street | PASS | One actual jump/landing, 1.086 m peak foot clearance above current support |
| Proposed provisional-deck connector → upper apron | PASS, isolated proposal | 53.33 m / 25.47 s; later repeat recorded max actual foot rise 0.1863 m, foot drop 0.0120 m; no large support transitions in repeat |

Existing limits: capsule radius 0.34 m, height 1.9 m, max snap step 0.42 m, walk 2.1 m/s, run 4.6 m/s. The three flights have 6/11/4 risers, heights 0.17381/0.17429/0.16 m, treads 0.4/0.32727/0.5 m. The entire street rises 4 m over 36 m; it is stair-based, not a step-free route.

**Feasible controller-compatible proposal:** a 3 m nominal-width, 8.544 m bridge/ramp from provisional skyport `(27,17.15,60)` to existing garden-path `(30,17.412,52)`, rise 0.262 m, grade 3.07%. Centreline terrain clearance is 1.07–1.24 m; it needs supports and edge protection. It continues along the existing 10 m / 1.2 m-rise garden path and the verified stairs. This starts on a **future deck reservation**, not a currently built skyport or the lower natural ground. Only a labeled planning ribbon is built in the preview. No skyport architecture is added.

A 5 mm centreline scan of that combined route samples 10,712 points: largest up-step 0.174286 m, down-step 0.0115 m, no change over the 0.42 m controller threshold. One earlier traversal recorded a brief point-support fallback to terrain despite only a small actual foot dip; it was not reproduced in the repeat or dense scan. Use a continuous/welded collision deck at interfaces, then retest variable frame rates before production. Central-route overhead rays found no obstruction within 30 m. The follow camera remained roughly 12.85 m from the player's feet on the proposed journey; that number is camera distance, not a wall-clearance measurement.

A separately recorded 29.39 m, 4.76% natural-ground garden-boardwalk alternative also traversed successfully, but is not the recommended dominant route: it detours from the provisional arrival axis. Its evidence is retained and labeled separately.

## Three remaining critical defects / integration recommendation

1. **Terrain/building support:** up to 7.38 m below floor level remains unresolved; exposed bases and edges need an approved structural/site response.
2. **Two-way connections and collision:** raw arrival blocks, square return blocks, and the current square edge drops 0.89 m. The isolated skyport connector demonstrates feasibility, but production needs supported landings/ramps, guarded edges, welded support seams and actual door/furniture collision proxies.
3. **Destination composition:** the forest closes the square/Guild axis. A later approved composition pass must establish a readable public-space connection and framed landmark/scenic view. No Guild or additional buildings were constructed.

Recommend preserving this export as the architectural source and authorizing a small terrain/support-and-interface design proof before any production deployment. Review the explicit alpha-glass comparison as a performance option; do not silently substitute it. Browser visual approval remains pending.

## Verification records

43 existing regression tests passed: 27 asset/character/floating-landscape/town tests plus 16 experience/portfolio tests. [Focused output](../../../validation/market-street-s2d/regression-results.txt), [portfolio output](../../../validation/market-street-s2d/portfolio-regression-results.txt). These protect existing systems; they do not approve S2-D art.

[Artifact verification](../../../validation/market-street-s2d/validation.json) checks all **1,353 protected files unchanged**, GLB geometry totals, binary preservation, embedded image decoding and screenshot integrity. [Terrain detail](../../../validation/market-street-s2d/terrain-detail.json), [raw traversal](../../../validation/market-street-s2d/skyport-deck-proposal-result.json), [repeat/seam diagnosis](../../../validation/market-street-s2d/connector-seam-diagnosis.json), [5 mm scan](../../../validation/market-street-s2d/support-seam-scan.json). Live Blender MCP export, native reopen and actual viewport inspection succeeded. **STOP at S2-D; owner approval is required for deployment.**
