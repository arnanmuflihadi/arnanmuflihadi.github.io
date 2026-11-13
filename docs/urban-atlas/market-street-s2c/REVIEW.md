# S2-C: Modern Tropical Market Street

One 36 m environment-art vertical slice, authored and rendered through live Blender MCP. **S2-B was approved as the starting system; S2-C awaits human visual approval.** No S2-D work, new town district, Guild building, NPC gameplay, production export or integration occurred.

## Saved project and evidence

- [Native S2-C project](../../../validation/market-street-s2c/market-street.blend), active scene **S2C Market Street**.
- [Four-view gallery and top-down plan](index.html).
- [Arrival / first market landing](../../../validation/market-street-s2c/01-arrival.png).
- [Opposite pedestrian perspective](../../../validation/market-street-s2c/02-opposite.png).
- [Complete elevated view](../../../validation/market-street-s2c/03-elevated.png).
- [Paving, entrance, balcony and planting detail](../../../validation/market-street-s2c/04-detail.png).
- [Actual top-down render](../../../validation/market-street-s2c/05-plan.png).
- [Existing LOD1 distance check](../../../validation/market-street-s2c/06-distance-check.png), same four placements, distant Kopi Awan swapped only in the separate **S2C Distance Check** scene. Main scene retains LOD0.

The four architectural renders are 1800×1200. The plan is 1500×1600. All are real Cycles images, with 48–64 samples and denoising; the optional distance test uses 32 samples. Cameras, metre-space transforms, materials and object costs are in [metrics.json](../../../validation/market-street-s2c/metrics.json). No AI illustration substitutes for this evidence.

## Four related storefronts

| Building | Reused system | Authored difference |
|---|---|---|
| **Kopi Awan** | Approved complete LOD0 assembly, roof A, original café name, glazing, timber balcony and source materials | Positioned on the first west landing; two outdoor café tables/chair pairs connect it to the public realm. The source building was not remodeled. |
| **Lembaran** | Window/door frames, shell/floor system, balcony, timber structure, planters, roof B | Approximately 5.9 m frontage, ochre plaster, three differently spaced upper windows, compact screen, shaded frontage and perpendicular bookshop blade. Only shallow visible book displays are staged. |
| **Rupa Rimba** | Ground-floor shell/openings, door/frame parts, lower ceiling slab, roof B | Approximately 8 m single-storey atelier; roof B lowered to a ventilated lower roof, recessed/open display bays, timber terrace screens, pottery counter and a different massing/height. No complete interior built. |
| **Serambi** | Two-storey frame/window family, balcony parts, roof A | Approximately 8 m corner frontage; actual chamfered ground-floor entrance/glazing, fitted square-facing return, wraparound terrace and signs addressing both street and square opening. |

Original S2-A and S2-B files remain unchanged. Geometry and materials are shared where appropriate; the variants are selectively edited component assemblies, not four buildings modeled from scratch. Full transmission glass is retained only for Kopi Awan. Other storefronts use cheaper alpha/opaque PBR glass or open display bays.

## Street, terrain and destinations

The measured source is `assets/js/town-layout/plan.js`, revision **R0-B1.5-composition-repair.3**, plus the actual triangulated terrain sampler. The provisional market has opposing frontages around game X=36, running from Z=40 toward Z=12 and the square. This slice extends that reference to Z=44..8.

Art-local Blender `(u,v,h)` maps to game `(36+u,18.6+h,44-v)`. The 36 m public route rises 4 m. Two opposing shop pairs occupy two terraces, with the lower artisan shop balancing the taller corner shop. The original route's ramped profile is interpreted as broad stair flights/landings for this isolated art study. Maximum local vertical departure from the provisional street profile is approximately **0.80 m**; the production route was not changed.

The original plan's small M1–M8 envelopes are consolidated into four larger art footprints, not blindly populated or permanently replaced. Final proposed shop-floor game elevations are 20.043 m, 20.234 m, 21.960 m and 21.960 m. The latter two differ from the source street at their final centres by approximately −0.09 m and −0.23 m. [Final site/terrain survey](../../../validation/market-street-s2c/final-site-survey.json) records those comparisons and 0.5 m terrain sampling.

Natural ground lies substantially below the provisional street floors: sampled support/fill depth ranges reach **about 7.4 m** at the west atelier footprint. The scene therefore includes local proposed graded pads, continuous retaining skirts, planted returns and threshold landings. These are art-scene support proposals, not structural or production-terrain approval. Production integration needs a dedicated terrain/retaining/collision review rather than simply dropping these buildings onto the existing ground.

The public realm includes continuous laid paving, three broad stair flights, café furniture, two benches, integrated and street planters, tropical trees/palms, ginger/broadleaf planting, restrained lamps and wayfinding. A short measured landscape/path connection continues toward the existing arrival direction; it is context, not another street or island.

The square opening occupies local V≈30..36, overlapping the original square reservation centred at `(0,34)`. The tree/benches are offset from the central route. The Guild reservation lies beyond the slice at local `(4,48)`. Its direction remains open and signed; **no Guild model or architectural stand-in was built**. Neither the full Town Square nor Market Street's remaining buildings were constructed.

## Pedestrian checks

- Central intended clear corridor: **6 m** inside the 10.4 m paved realm.
- Stair flights: 6 risers at 17.38 cm / 40 cm tread; 11 at 17.43 cm / 32.73 cm tread; 4 at 16 cm / 50 cm tread.
- One shallow approximately 19 cm threshold landing serves Lembaran; the other main thresholds meet their terrace levels.
- A conservative world-AABB test at 145 stations found **zero architecture, prop, planter or plant bounds obstructing the central corridor below 2.1 m**. [Actual result](../../../validation/market-street-s2c/circulation-check.json).
- Arrival eye is 1.65 m above the first market landing; opposite eye is 1.65 m above the upper gathering apron; the detail eye is 1.65 m above the café landing.

This is not a controller, camera-clearance or physics traversal test. There is no authored game collision mesh in this phase. Stair/support conversion and a step-free alternative remain future integration decisions. Passing geometric checks does not prove artistic approval or game walkability.

## Geometry and material costs

| Part | Evaluated triangles | Editable geometry objects |
|---|---:|---:|
| Kopi Awan, including its original planters | 35,876 | 10 batched assemblies |
| Lembaran | 19,710 | 193 |
| Rupa Rimba | 12,012 | 117 |
| Serambi | 33,926 | 247 |
| Public realm, terrain patch, furniture and vegetation | 69,185 | 361 |
| **Total visible main scene** | **170,709** | **928** |

There are **38 used materials**, **5 packed populated images** and **690 raw geometry datablocks**. Trees, ferns and repeated source pieces share geometry/materials. Packed image payload totals approximately 324 KB; decoded dimensions are one 512×512 palette and four 256×256 images. Source textures and actual licenses remain intact.

Editable per-object material slots total **989 potential unbatched render primitives**. This is a Blender authoring inventory, **not measured Three.js draw calls**. Grouping static surfaces by material could reduce this substantially; the theoretical per-building material sets are 18/21/16/18, plus 22 public-realm materials. Those lower bounds do not account for module retention, alpha sorting, shadows or glass passes. The native authoring scene should not be integrated unbatched.

A rough future uncompressed GLB budget is **10–14 MB**, inferred from S2-B's measured bytes/triangle plus this scene's images and geometry. It is an estimate, not an exported file measurement. Attribute splitting, static batching, foliage instancing and delivery compression will change it. **No S2-C GLB was exported.** Browser draw calls, GPU timing, actual export bytes and walking performance are intentionally untested.

The optional distance check reuses the already approved Kopi Awan LOD1 at the same far placement, saving **23,938 triangles** in that alternative view (main scene remains full detail). Its flatter roof surface is visible on close inspection; a game-camera switching threshold needs later review. No new LOD generation or repeated S2-B optimization was performed.

## Visual QA and concept comparison

The original generated floating-town reference was available in S1's `references/` directory and inspected. The slice adopts its warm plaster/timber/terracotta family, protective eaves, planted balconies, shaded shopfronts and pedestrian scale. It does **not** claim to reproduce the illustrated full town, atmosphere or landmark richness. The view edges deliberately stop at the isolated scene; no distant district or Guild is disguised in the background.

The first actual renders exposed three major defects: inactive-scene socket transforms put copied roofs at the wrong height; natural-ground interpolation intersected stair edges; and per-face grass variation created a checker pattern. Source transforms were evaluated before copying, continuous support skirts/ground clearance corrected the paving interface, and grass changed to broad tonal zones. Initial images are retained as diagnostic evidence, not delivery views.

Subsequent pedestrian inspection removed upper-storey sill remnants from the lower atelier roof, fitted the Serambi corner return, refined the palms and brought the square marker into view. Final context images add the arrival landscape connection; the detail camera was lowered to include the actual entrance/paving relationship. These are internal visual observations only. No numerical human-quality score or automatic approval is awarded.

## Preservation and limits

[Validation record](../../../validation/market-street-s2c/validation.json) confirms all **1,310 protected starting files unchanged**, including S2-A/S2-B projects/exports and production assets/pages. The five required images plus the optional distance image decode successfully, and used images are packed. No full-game regression suite ran during this isolated Blender authoring phase.

Known limits: this remains an editable art scene with a high unbatched object count; foliage LOD and alpha sorting need delivery work. The local retaining/fill proposal needs integration review. Existing scenery at the open view boundaries is a partial context patch, not the finished floating-island backdrop. Palm leaves are intentionally lightweight geometry and remain subject to visual review. Interiors are shallow staging, doors static, and the Guild only a future directional reservation. Blender sky/PBR appearance will require separate browser verification after an approved export phase.

**Stop for human visual approval before S2-D.**
