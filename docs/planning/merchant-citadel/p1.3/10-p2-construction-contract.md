# 10 - P2 construction contract for the selected P1.3 layout (not started; needs explicit authorisation)

P2 builds the archetypes as reusable assemblies and proves one of them in the real Three.js scene. It does not assemble the town (P3) or build terrain (P4).
This contract replaces `../p1/12-p2-construction-contract.md` where they differ; the per-archetype module lists, material strategy, collision notes and acceptance criteria in `../p1/08` still apply.

## Roster

| ID | Purpose | Instances | Used by | Footprint (m) | Height (m) | Module instances / ids | Triangles each | Verified sources | Readiness |
|---|---|---|---|---|---|---|---|---|---|
| A01 | Exchange Hall: civic landmark | 1 | B01 | 28 x 16 | 22.8 | 348 / 28 | 87,904 | custom (seal / sign), Quaternius Fantasy Props, Quaternius Medieval Village | READY |
| A02 | Covered market hall (two dressing kits) | 2 | B02, B03 | 8 x 12 | 9.0 | 61 / 27 | 42,176 | Avramania, custom (seal / sign), Quaternius Fantasy Props, Quaternius Medieval Village, Syntaxes of Play Medieval Cafe | CONDITIONAL |
| A03 | Jettied two-storey shophouse, gable to street | 2 | B07, B09 | 6 x 8 | 10.9 | 59 / 21 | 19,238 | Avramania, custom (seal / sign), Quaternius Fantasy Props, Quaternius Medieval Village | CONDITIONAL |
| A03b | Two-storey shophouse, eaves to street | 2 | B05, E03 | 8 x 6 | 10.9 | 63 / 22 | 19,454 | Avramania, custom (seal / sign), Quaternius Fantasy Props, Quaternius Medieval Village | READY |
| A03c | Shallow two-storey merchant house (8 x 4 m) for plots that back onto a lane - **new in P1.3** | 1 | E02 | 8 x 4 | 9.7 | 56 / 21 | 16,288 | Avramania, custom (seal / sign), Quaternius Fantasy Props, Quaternius Medieval Village | READY |
| A04 | Single-storey shop, gable to street | 2 | B06, B14 | 4 x 6 | 6.7 | 25 / 14 | 8,200 | custom (seal / sign), Quaternius Fantasy Props, Quaternius Medieval Village | READY |
| A04b | Single-storey shop, eaves to street | 4 | B08, B11, E01, E05 | 6 x 4 | 6.7 | 25 / 13 | 8,134 | custom (seal / sign), Quaternius Fantasy Props, Quaternius Medieval Village | READY |
| A05 | Stone-based corner building with two fronts | 4 | B04, B15, B16, E04 | 8 x 8 | 12.0 | 68 / 21 | 37,334 | Avramania, custom (seal / sign), Quaternius Fantasy Props, Quaternius Medieval Village | READY |
| A06 | Stone workshop | 2 | B10, B12 | 6 x 6 | 7.9 | 32 / 16 | 30,692 | custom (seal / sign), Quaternius Fantasy Props, Quaternius Medieval Village | READY |
| A07 | Guild warehouse | 1 | B13 | 8 x 14 | 12.0 | 80 / 22 | 42,321 | custom (seal / sign), Quaternius Fantasy Props, Quaternius Medieval Village | READY |
| A08 | Tea house with veranda | 1 | B17 | 6 x 6 | 10.9 | 65 / 21 | 20,976 | Avramania, custom (seal / sign), Quaternius Fantasy Props, Quaternius Medieval Village | CONDITIONAL |

Structures: split gateway (READY), market cross (READY). Stall kits: five kinds, 12 stalls (READY; three kinds depend on the cafe and Avramania packs).

**What P1.3 adds to the P2 work:** one variant (A03c, from modules already verified), a per-building "additions" list (seal, banner, vine, goods) so reused archetypes differ, and nothing else.
No new download, no new custom mesh, no new material.

## Sequence

1. Scale scene: 2 m grid, 3 m storey, 1.9 m explorer.
2. Materials: bake the colour grade into copies of the base-colour textures; merge duplicates only where the node set-up is identical; cloth and dark-roof instances; seal and sign meshes. Convert the used cafe-pack models to GLB once.
3. Shared wall, window, door, roof and signage sub-assemblies.
4. A04, A04b (six instances between them). 5. A03b, **A03c**, A03. 6. A05 (four instances), A06.
7. A02, gateway, market cross. 8. A01. 9. A07, A08.
10. Apply the substitutions below; join static meshes per building by material.
11. One archetype exported and loaded in the real scene; measurements recorded; stop for approval.

## Performance estimate (Blender measurements; no browser figure exists)

| | P1.2 | P1.3 |
|---|---|---|
| Buildings | 17 | 22 |
| Instances | 2,184 | 2,443 |
| Downloaded models used | 139 | 140 |
| Triangles, unoptimised (measured) | 847,312 | **915,026** (+8%) |
| Distinct materials | 53 | 53 |
| Paving tiles | 700 | 725 |
| After the substitutions below (projection) | 461,419 | **515,072** |

Triangles by category:

| Category | P1.2 | P1.3 | Change |
|---|---|---|---|
| architecture modules | 327,590 | 406,044 | +78,454 |
| goods, furniture and street props | 198,063 | 222,578 | +24,515 |
| lanterns | 124,168 | 132,634 | +8,466 |
| vegetation | 170,091 | 124,506 | -45,585 |
| stall bases | 16,856 | 16,856 | +0 |
| custom seal and signs | 7,200 | 8,964 | +1,764 |
| paving | 3,344 | 3,444 | +100 |

Five buildings added 67,714 triangles, about 13,542 each, because every building repeats the same modules: geometry is reused, not multiplied in kind.
Largest contributors and the substitution proposed for each (targets are for simplified meshes that P2 must produce and measure):

| Component | Instances | Triangles each | Total now | Target each | Saving |
|---|---|---|---|---|---|
| `MV-Corner_Exterior_Brick` | 38 | 3,102 | 117,876 | 300 | 106,476 |
| `FP-Lantern_Wall` | 47 | 2,822 | 132,634 | 600 | 104,434 |
| `SN-CommonTree_3` | 21 | 3,505 | 73,605 | 1,500 | 42,105 |
| `AV-mdvl_village_window_box_01` | 20 | 1,330 | 26,600 | 400 | 18,600 |
| `SN-CommonTree_1` | 3 | 6,265 | 18,795 | 1,500 | 14,295 |
| `FP-Crate_Wooden` | 10 | 1,576 | 15,760 | 230 | 13,460 |
| `MV-Door_8_Round` | 17 | 1,142 | 19,414 | 400 | 12,614 |
| `FP-Barrel` | 22 | 824 | 18,128 | 300 | 11,528 |
| `SN-Bush_Common_Flowers` | 12 | 1,368 | 16,416 | 500 | 10,416 |
| `FP-FarmCrate_Apple` | 3 | 4,028 | 12,084 | 600 | 10,284 |
| `FP-Bag` | 14 | 858 | 12,012 | 300 | 7,812 |
| `FP-Barrel_Apples` | 4 | 2,480 | 9,920 | 700 | 7,120 |

| Lever | Effect |
|---|---|
| Instancing | 2,443 instances draw from 156 meshes. Repeated modules (wall bays, windows, posts, lanterns, tiles) are candidates for `InstancedMesh`; the brick pier is placed 38 times and the lantern 47 |
| Static merge | Alternatively merge each building by material: about 53 materials town-wide, so the number of batches depends on materials, not on the building count. The five new buildings add to existing batches |
| LOD and visibility | The compact layout hides more: from any street the far districts are behind two-storey rows. Backdrop trees and far roofs can drop to a lower level beyond about 40 m. To be measured, not assumed |
| Collision | 56 box proxies for buildings (P1.2: 51); posts and stalls extra. No mesh colliders |
| Paving | 725 tiles could be one plane per surface (23 surfaces) |

The earlier figure of about 350,000 triangles is not reached by substitutions alone (515,072). The remaining levers are fewer or lower-detail backdrop trees and lower-detail wall and roof modules; each should be decided on a browser measurement.

## Measurable P2 verification steps

| Step | Measure | Pass condition (proposed, to be agreed) |
|---|---|---|
| 1 | Triangles per archetype GLB (`docs/tooling/glb-inventory.mjs`) | At or below the agreed budget |
| 2 | Distinct materials and textures in the exported set | At or below 53; no texture above 2048 px |
| 3 | One archetype in the real page: `renderer.info.render.triangles` and `.calls` at three fixed cameras against the island-1 baseline | Recorded; increase within budget |
| 4 | Scale and orientation: door 2.1 m, storey 3.0 m, +y up, front on +z | Within 1 cm |
| 5 | Controller on the hall stairs, through a hall arch, and along a 4 m lane | No sticking |
| 6 | Follow camera at the corners and door exits listed in 08 | Behaves acceptably with the game's collision set; recorded |
| 7 | Frame time over a fixed 60 s walk at 1280 x 720 | Recorded with hardware noted |

**Browser performance has not been validated.**
