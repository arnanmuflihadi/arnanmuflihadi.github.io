# 13 - Risk and feasibility register (P1.2)

## Not verified

- **Nothing was loaded in Three.js.** All renders are Blender EEVEE. Browser appearance, frame rate, real collision and real camera behaviour are untested.
- The walkability and camera checks use ray casts against render geometry with constants copied from the project. They are evidence about the layout, not a run of the game.
- The colour grade and cloth colours were judged under Blender's light and tone mapping only.
- General browsing of OpenGameArt and the itch.io 3D tag was not carried out beyond the named candidates.

## Licensing and provenance

| Item | State | Action |
|---|---|---|
| Syntaxes of Play cafe pack | CC0 stated on the page; no licence file in the archive | Save a dated copy of the page with the P2 assets |
| Avramania Food & Market, Village Builder | CC0 in the archive; ReadMe states no AI-generated meshes | Owner to confirm that script-built models made with an AI coding assistant are acceptable |
| Avramania Props, Interiors, Nature | Contain unidentified AI-generated meshes | Not used. Do not add them later without an owner decision |
| Quaternius, Kenney | Unchanged | - |

## Geometry and assembly

| Item | Risk | Mitigation |
|---|---|---|
| Jetty windows surface-mounted on `Overhang_Plaster_Short` | Z-fighting or a visible frame gap in the engine | Check on the first A03 export; if needed cut an opening or offset the insert 1 cm |
| Porch roof runs through the hall's upper wall into the main roof | Hidden inside the walls in Blender; overlapping roof surfaces could flicker at the junction | Inspect the junction in the engine; trim the hidden half of the porch roof on export |
| Cafe pack FBX | Texture paths do not resolve; materials come from the pack's `.blend` by name | Convert once to GLB with materials embedded and record the conversion |
| Same-named Quaternius materials differ by mesh | Merging them by name turned lantern metal black in this revision (the importer adds a vertex-colour multiply only where the mesh has vertex colours) | Merge materials only where the node set-up is identical |
| Custom seal and signs | 10 small meshes to author | One seal mesh and one sign mesh with a pictogram atlas |

## Performance

| Risk | Likelihood | Mitigation |
|---|---|---|
| Triangle load too high in the browser | Medium | 847,312 now; substitutions in 12 project 461,419; measure one archetype early in P2 |
| Material and texture count | Medium to high | 53 materials now; atlas the cafe pack; bake the grade into shared textures |
| Small goods are heavy | Medium | Avramania cabbage 1,448 and flower box 1,330 triangles each; simplify or merge per stall |
| Lanterns, piers and trees | Medium | Still the three largest contributors (12) |

## Design

| Risk | Likelihood | Mitigation |
|---|---|---|
| Owner prefers the approved P1.1 seal or colours | Open | P1.1 is preserved in `visuals/p1.1/`; either set can be built |
| Mixed shading styles noticed in play | Medium | Keep other publishers to small goods; drop the Avramania stall if it jars |
| Town reads as standing in a field | Certain until P4 | Terrain and island edge are P4; the support zone is defined in 10 |
| Engine collision differs from the ray test | Medium | Repeat sections B and F of 09 in the engine |

## Resolved or reduced since P1.1

| P1.1 limitation | State |
|---|---|
| Only two stall models | Reduced: five stall kinds from three sources |
| Shops identified only by red banners | Resolved: pictogram trade signs |
| Hall built from house parts with a flat front | Reduced: entrance porch, dark roofs |
| Overhang / jetty modules unassembled | Resolved: assembled on A03 and rendered |
| Stall counter height set by eye | Resolved: flat tops measured on the meshes (0.83, 0.96, 1.15 m) |

## Differences from the supplied concept images (unchanged)

European half-timber and stone, not Indonesian-tropical; 17 buildings and 12 stalls rather than 21 and 12; straight streets on a 2 m grid; a stone-based hall with a porch and crossing tower rather than a multi-tier roof.

## Housekeeping

- Downloads, extracted files, tiles, the P1.0 and P1.1 comparison sets and the blockout `.blend` are in `.asset-inspection/merchant-citadel-p1/` (about 1.5 GB, ignored by Git).
- No production file, earlier asset, island-1 content or game code was changed. No GLB was exported. Nothing was committed or deployed.
