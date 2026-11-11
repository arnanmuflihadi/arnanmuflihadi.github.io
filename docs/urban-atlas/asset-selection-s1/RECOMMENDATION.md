# S1 — Architecture acquisition and comparison

**Decision: no inspected ready-made building kit meets the concept.** Keep the verified component library; use limited custom Blender modeling for the missing architectural language after owner approval. These renders are asset inspection evidence, not an approved town or finished façades. S2 has not started.

## Recommended system

| Role | Recommendation | Limits |
|---|---|---|
| Primary component pack | Existing Kenney Modular Buildings 2.1 | 108 actual local GLBs, CC0. Useful windows, doors and structural pieces; do not repeat its rectangular whole-building defaults. |
| Secondary component source | Quaternius Ultimate Buildings, A1 balcony and A2 columns | Only four sample FBXs acquired. Reuse selected geometry after repair, not the Western houses intact. |
| Roof/opening complement | Existing Kenney Building Kit | 79 actual local GLBs, CC0; no redownload. Does not supply a finished tropical roof family. |
| Props | Existing Downtown City planter/street details | CC0 Standard files already verified. No additional prop pack needed for selection. |
| Nature | Existing Quaternius Stylized Nature tree and fern | Keep existing textures/geometry; future species choice should preserve tropical identity. No replacement landscape. |
| Materials | Controlled original mineral paving; retained source atlases | No new PBR downloads necessary for this comparison. Future warm plaster, timber, terracotta, teal glazing and dark metal need distinct values and roughness. |

Use a shared 3 m floor module as a later design target; keep openings approximately human-scale and coordinate balcony depth, canopy height and roof thickness across variants. The intended design language is warm plaster over a darker stone base, shaded glazed commercial ground floors, timber or dark-metal balcony frames, and related terracotta hip/swept roofs. Vary roof height and frontage rhythm while keeping window proportions related. Guild fantasy accents should concentrate in a memorable crown and canopy, rather than repeated ornament everywhere.

Missing components requiring limited custom Blender work: genuinely open/glazed retail frontage, continuous shaded arcade, accessible thresholds, deep tropical eaves, usable balconies, hip/swept roof corners and one distinctive Guild silhouette. Existing licensed meshes should supply useful details. None of this production work was undertaken in S1.

## Actual comparison evidence

Open [asset-comparison.blend](../../../validation/asset-selection-s1/asset-comparison.blend), active scene **S1 Asset Comparison**. Other prior validation scenes were preserved. Collections: Buildings, Streets, Landscape, Props, Collision References, Labels and Cameras. Collision References is intentionally empty: these are inspection bays, not playable terrain or collision-certified town plots.

| Bay | Imported file | Dimensions W×D×H, metres | Triangles | Finding |
|---|---|---|---:|---|
| A1 | 2Story_Balcony.fbx | 5.18×6.08×7.07 | 4,210 | Real cornice/balcony geometry; dark diagonal/gap visible at balcony, tiny closed glazing and Western decorative quoins. Parts only. |
| A2 | 2Story_Columns.fbx | 5.18×5.97×6.64 | 3,620 | Porch depth useful; closed frontage, tall door and small windows need redesign. Parts only. |
| A3 | 1Story_GableRoof.fbx | 5.05×5.71×4.86 | 1,684 | Gable treatment visible; weak shop identity. Reject complete building. |
| A4 | 2Story_RoundRoof.fbx | 5.07×5.10×6.96 | 2,714 | Barrel roof provides contrast; blank upper wall fails storefront quality. Reject complete building. |
| G0 | Existing transit-kingdom.glb / AtlasResearchCentre | 13.45×12.47×18.20 | 20,112 | Existing 16-mesh Guild reference. Canopy silhouette useful; excessive repeated floor bands. Not a new selected external landmark. |

Four storefront **candidates**, not four accepted shop designs. Their common 2.4× source scale preserves relative kit proportions; Blender metric units, Z-up, fronts toward −Y, bases at Z=0 within floating-point tolerance. Human gauges are 1.80 m, pedestrian camera eye is 1.65 m. Door dimensions/accessibility remain unsuitable or unverified; scale normalization does not grant architectural approval. Native source UVs and the original 32×32 light atlas were restored; no invented high-detail façade overlay.

Actual Blender MCP imports, scene queries, camera edits, saves and renders were used. The three saved images were visually inspected. The detail camera was widened to include the parapet; source defects were retained for honest assessment.

- [Aerial architectural contact sheet](../../../validation/asset-selection-s1/01-aerial-contact-sheet.png), 1600×1000.
- [Pedestrian storefront comparison](../../../validation/asset-selection-s1/02-pedestrian-storefronts.png), 1600×800, eye Z=1.65 m.
- [Façade / roof detail](../../../validation/asset-selection-s1/03-facade-roof-detail.png), 1280×960.

Fixed camera transforms/lenses: [scene-metrics.json](../../../validation/asset-selection-s1/scene-metrics.json). All views use the same neutral world fill, large soft area light, Cycles 24 samples and denoising. No fog or atmospheric concealment. The pedestrian camera compares all four bays, rather than depicting an implemented street. Two roof treatments are gable and barrel, plus flat parapet variants. No optional 30 m streetscape was built because these complete buildings are not strong enough.

## Resource and preservation checks

- 4 new imported FBX meshes: **12,228 triangles**, **396,304 source bytes**; original atlas **3,212 bytes**. One new pack sampled; no entire catalog/archive downloaded.
- Total comparison: **37 mesh objects, 46,184 triangles, 23 materials**, including reused Guild, vegetation, planter, display paving and scale gauges. There are 9 imported visible asset instances: four buildings, Guild, two trees, fern, planter. Primitive geometry is confined to display bases and human gauges.
- 17 used image datablocks, all populated and packed. Some are duplicate source images from reused instances; this is a comparison scene, not a delivery-optimized GLB. Source texture resolution is 32px, 256px or 1024×256 signage. No missing-image datablocks detected.
- `node --test tests/*.test.mjs`: **106 passed, 0 failed, 0 skipped**. [Actual output](../../../validation/asset-selection-s1/regression-results.txt).
- **1,260 baseline files unchanged**, including game JS/CSS/assets, source assets and root HTML. Both Kenney archive hashes and license hashes still match the existing manifest. [Preservation check](../../../validation/asset-selection-s1/preservation-check.json).
- No website integration, export replacement or gameplay change. Browser draw calls, walking timing, collision traversal and browser material transfer are **NOT TESTED for these candidates**. Blender triangles are not browser draw calls or a performance guarantee. Prior dirty/untracked repository work was preserved.
- Native file reopened successfully through live Blender MCP: active `S1 Asset Comparison`, 52 total scene objects. A separate background Blender launch exited 139 before its inspection completed; this check failed, while live imports/rendering/save/reopen succeeded. The launch warning/crash output is retained in `validation/asset-selection-s1/reopen-check.txt`.

## Licensing and selection records

[All 63 source entries](ASSET-CATALOG.md), [ranked shortlist](ASSET-SHORTLIST.csv), [acquisition provenance / SHA256](../../../validation/asset-selection-s1/acquisition-manifest.json). Six scores are provisional internal candidate assessments; visual score averages concept fit, richness and coherence only. They are not human approval.

All acquired/reused external comparison meshes are CC0 with retained source records. Source model archives were not changed. The Guild is existing project-authored work using the previously documented CC0 components. Original provenance remains in ASSET_MANIFEST.md and architecture/scenery source manifests. No per-asset clearance is inferred from a marketplace catalog. Reodesuxz source redistribution restrictions prevent raw public GitHub acquisition in this workflow. Andrew Jepson’s CC BY4.0 diorama is reference only; not imported. Kenney Fantasy Town ZIP returned HTTP403; not acquired. No paid services or purchases used.

**Owner visual approval pending.** The defensible outcome is a small verified parts shortlist plus specific custom-modeling requirements, not a claim that these generic source buildings achieve the premium concept. Stop before S2.
