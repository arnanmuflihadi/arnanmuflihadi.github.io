# S2-B: Kopi Awan optimization and modules

S2-A visual direction was explicitly approved by the owner in the S2-B request. That original file is unchanged. This independent S2-B derivative awaits review; no S2-C work, street construction or production game changes were made.

## Deliverables

- [Independent modular Blender master](../../../validation/storefront-s2b/kopi-awan-modular.blend)
- [Optimized LOD0 GLB](../../../validation/storefront-s2b/kopi-awan-optimized.glb)
- [Distant LOD1 GLB](../../../validation/storefront-s2b/kopi-awan-lod1.glb)
- [Swappable roof B GLB](../../../validation/storefront-s2b/kopi-awan-roof-b.glb)
- [Blender/browser comparison gallery](index.html)
- [Isolated live Three.js preview](../../../validation/storefront-s2b/index.html) served at `http://127.0.0.1:4173/validation/storefront-s2b/index.html`
- [Geometry cost summary, export checks and preservation hashes](geometry-costs.json), [per-object costs](geometry-by-object.csv), [module sockets](module-sockets.json)

## Geometry and delivery cost

| Component | Original evaluated triangles | Optimized LOD0 triangles |
|---|---:|---:|
| Building shell | 5,064 | 2,736 |
| Shopfront and doors | 4,212 | 1,716 |
| Windows | 3,732 | 1,684 |
| Balcony | 5,400 | 2,200 |
| Roof A | 17,128 | **17,128, unchanged** |
| Timber structures | 2,592 | 1,056 |
| Sun screens | 1,836 | 748 |
| Decorative props | 1,908 | 1,460 |
| Interior staging | 5,068 | 3,148 |
| Planters, soil and ferns | 4,768 | 4,000 |
| **Complete exported asset** | **51,708** | **35,876** |

The earlier 46,940-triangle figure counted the building without planters. On that same basis the optimized building is 31,876 triangles, a 32.1% reduction. Including planters, the reduction is 30.6%. Presentation ground, scale mannequin, cameras and lights are excluded from GLBs.

The most expensive individual source items were tile courses (4,816 triangles), arrayed beveled balcony decking (3,348), and arrayed sun-screen blades (1,404). Cost reductions target small bevel cross sections rather than arbitrary silhouette decimation. Roof A geometry and modifiers remain intact in the editable master. Native convert/join preserves its exported appearance.

| Export | Triangles | GLB bytes | glTF module meshes | Render primitives |
|---|---:|---:|---:|---:|
| LOD0 / roof A | 35,876 | 2,477,572 | 10 | 46 |
| LOD1 / roof A | 11,938 | 803,596 | 10 | 42 |
| Roof B only | 3,456 | 155,004 | 1 | 6 |

LOD1 removes the individual roof tile courses, retains the curved roof silhouette and ridge/edge treatment, removes tiny bevels, and dissolves coplanar detail. It reduces total triangles by 66.7% versus LOD0. It is intended for distance, not a substitute for the approved close-view asset. It remains manually selectable in the isolated preview; no production LOD integration occurred.

The editable source contains 270 asset objects organized into reusable components. Delivery consolidates these into 10 module meshes; multiple materials become separate glTF primitives. **Ten module meshes does not mean ten draw calls.** The GLB contains 18 material definitions; GLTFLoader creates 19 runtime materials where geometry requires separate variants. Two PNG images are embedded: 256×256 fern leaves and a 512×512 Kenney palette. No external textures or decoder dependency is required.

## Modular organization

The master opens in **S2B Editable Modules**. Collections separate Building shell, Shopfront and doors, Windows, Balcony, Roof A, Timber structures, Sun screens, Planters and Decorative props, with Interior as an auxiliary component and Roof B as a separately editable alternate. Existing presentation Streets, Props, Cameras and empty Collision References remain separate.

Socket origins use metres and Blender Z-up: shell at `(0,0,0)`, shopfront at `(0,-3.55,0.24)`, balcony at `(0,-2.85,3.5)`, roof at `(0,0.5,6.45)`, screen at `(1.26,-3.14,4.08)`. Other shared assemblies use the building ground datum. Editable child meshes retain useful source modifiers and transforms; delivered meshes have applied rotation/scale and unit node scales. Native export performs the supported glTF Y-up conversion once. Final browser bounds for roof A are approximately X `-4.37..4.37`, Y `0..8.812`, Z `-5.72..5.260`, including foliage and overhangs.

Source wall/opening meshes, arrays, bevels and roof surfaces remain editable. Batched export scenes are derivatives, not replacements for these collections. Future variations should exchange components at the sockets, keep the 3.5 m upper-floor datum and 6.45 m roof interface, and adapt opening widths deliberately. This is a reusable assembly, not an automatic arbitrary-width building generator. No additional complete building was created.

## Roof study

[Actual side-by-side Blender render](../../../validation/storefront-s2b/roof-a-b-comparison.png):

- **A:** approved lifted-corner hip, individual tile courses, raised ventilated ridge and brass crest. Default for Kopi Awan.
- **B:** contemporary limasan-inspired four-sided hip with straighter deep protective eaves, stronger upper pitch, a shallow skirt and lower ridge treatment. Its roof-only geometry is 3,456 triangles and it uses the same palette and socket. It is a study, not a claim of historical vernacular reconstruction or owner approval.

The browser switches A/B on the same exported building. With B visible, the complete asset has 22,204 visible triangles. Roof B is hidden in the main editable scene by default; the **S2B Roof A-B Study** scene displays both roof components on neutral trays. Neither tray is a new building.

## Actual browser validation

The isolated preview imports the existing bundled `three-atlas.module.js` and existing promise-cached `createModelLibrary`. It calls `get()` to retain authored glTF materials and physical scale; the production loader's scenery palette and automatic height normalization are not applied. Existing loader/cache source was not changed.

Browser evidence records the actual drawing buffer, camera, view, device, bounds, texture sizes, visible geometry, cache counts and renderer counters. The preview uses WebGL2 on **ANGLE Metal / Apple M4 Pro**, DPR 1. Street/detail buffers are 1500×1200; elevated is 1500×1500. Saved canvas-region screenshots are 1349 CSS pixels wide, with matching aspect ratios. Blender images are 1500 pixels wide. The gallery displays them at equal CSS sizes.

Camera positions/targets and perspective match after conversion from Blender `(x,y,z)` to Three.js `(x,z,-y)`. Street eye height is nominally 1.65 m. Blender daylight uses Cycles world/area fill; Three.js uses hemispheric fill, sun and a soft front fill with ACES tone mapping. **Lighting, reflections and global illumination are not identical.** Blender's ground joints and scale reference are presentation objects, omitted from the game GLB. Roof silhouettes, openings and material hierarchy can be compared fairly without claiming pixel-identical shading.

Verified in the browser: correct upright orientation, metre scale, grounded base, complete roof, visible glazing/interior, shadows, both embedded images, no missing textures, successful LOD selection and roof exchange. Console warnings/errors recorded at the final export check were empty. No production terrain collision, player traversal or doorway interaction is claimed for this isolated asset preview.

The elevated LOD0 counter is **140 calls and 107,632 submitted triangles across all render passes** in this preview. These include shadow and glass transmission passes and the ground, not just the 35,876 asset triangles. View-specific counters are saved in the browser JSON files. LOD1's counters remain materially affected by glass despite its large geometry reduction. Cached resource inventories can include hidden alternatives; visible geometry and submitted triangles are reported separately.

Moving-camera samples, 240 measured frame intervals each:

| Export | Median rAF interval | 95th percentile | Median CPU submission | 95th percentile CPU |
|---|---:|---:|---:|---:|
| LOD0 | 5.6 ms | 6.2 ms | 0.5 ms | 0.8 ms |
| LOD1 | 5.5 ms | 6.1 ms | 0.5 ms | 0.7 ms |

These are local warm-cache orbit observations on this browser/renderer, not GPU timings, player-walking tests or whole-district performance. DPR, glass passes, shadow settings and the number of buildings matter. [LOD0 timing record](../../../validation/storefront-s2b/performance-lod0.json), [LOD1 record](../../../validation/storefront-s2b/performance-lod1.json).

## Corrections and checks

Live browser inspection caught and corrected a doubled module-parent offset and a camera-axis mismatch before final screenshots. Native join also left the render UV layer unselected for plants: it was explicitly assigned, and the imported foliage material simplified to direct image-color/alpha PBR. The texture, silhouette and source license were retained. Final Blender plant rendering was checked after correction.

An initial custom mesh-repacking path interrupted Blender. The successful deliverable uses native Blender conversion/join/export operators instead; editable work was recovered from the independent saved copy. This is not a claim that the failed path succeeded.

GLB checks passed: header lengths/version, one active scene per file, embedded decodable images, triangle indices, normals, unit node scales and successful browser loading. **20 existing architecture/character regressions passed, zero failures or skips.** [Actual output](../../../validation/storefront-s2b/regression-results.txt). Hash verification confirms **1,261 starting files unchanged**, including the approved S2-A `.blend`, production assets, source packs and website pages. Approved S2-A SHA256 is recorded in `geometry-costs.json`.

The independent master was reopened successfully through live Blender MCP with **S2B Editable Modules** active and all five S2-B edit/export/study scenes present. Preview JavaScript and Blender helper syntax checks passed.

## Source rights and remaining limits

No new pack or paid service was used. Kenney Modular Buildings window frames and Quaternius Stylized Nature ferns retain the existing CC0 provenance in [S2-A attribution](../storefront-s2a/ATTRIBUTION.md) and [source hashes](../storefront-s2a/source-components.json). Building geometry, materials and alternate roof are original project work. Original archives/licenses and approved S2-A project remain unchanged.

Keep A for the approved hero storefront and review B as a quieter, less costly roof option. For future variants, change signs, glazing divisions, terrace screens and roof selection while retaining floor/roof sockets. Consider an opaque/alpha glass alternative and material atlasing if many buildings share a view; transmission currently adds significant passes. Evaluate LOD1 by projected size in the eventual game camera, not an untested fixed distance. Interior access, door animation, collision proxies, automatic LOD and whole-town budgets remain integration work for a later approved phase.

**STOP: S2-B awaits owner review before S2-C.**
