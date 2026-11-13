# S2-F asset use

No models, materials, textures or licenses were replaced; no downloads or installations. Existing assets are loaded through the shared model library using one cached GLTFLoader. The same library also supplies the existing island vegetation.

| File under validation/ | File bytes | Visible triangles |
|---|---:|---:|
| market-street-s2d/market-street-optimized.glb | 10,007,904 | 170,709 |
| market-street-s2e/common-interface.glb | 527,172 | 8,404 |
| market-street-s2e/foundation-hybrid.glb | 543,452 | 7,248 |
| market-street-s2e/support-reference.glb | 6,164 | 0 (100 support-only triangles) |

Asset totals are potential geometry, not camera-specific submitted triangle counters. All render passes are counted in the performance evidence. Source grading meshes remain hidden as in S2-D/E. The exact-terrain-reference export is never loaded into the game.

All roots retain translation **(36, 18.6, 44)**, unit scale and original Y-up GLB orientation. Building transforms and authored physical-glass transmission remain unchanged. Only the four documented imported showcase canopy placements are adjusted at runtime using the S2-E manifest. Original island vegetation and terrain remain byte- and matrix-identical.

Sources, terms and attribution are preserved in [S2-C](../market-street-s2c/ASSET-RECORD.md), [S2-D](../market-street-s2d/ASSET-RECORD.md), and [S2-E](../market-street-s2e/ASSET-RECORD.md). These cover original AR(N)AN geometry, licensed CC0 Kenney window components, and Quaternius canopy/fern components. No source archives were edited. See `validation/town-s2f/preservation.json` and the regression results for byte checks.
