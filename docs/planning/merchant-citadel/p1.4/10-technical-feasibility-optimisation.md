# 10 - Technical feasibility and optimisation assessment

All figures are Blender measurements of the blockout. **No browser measurement exists; no frame rate is claimed.**

| | P1.3 | P1.4 |
|---|---|---|
| Buildings | 22 | 24 |
| Instances | 2,443 | 2,736 |
| Distinct meshes | 156 | 159 |
| Triangles, unoptimised | 915,026 | **968,466** (+6%) |
| Distinct materials | 53 | 59 |
| Paving tiles | 725 | 737 |
| After the substitutions below (projection) | 515,072 | **532,062** |

| Category | P1.3 | P1.4 | Change |
|---|---|---|---|
| architecture modules | 406,044 | 492,573 | +86,529 |
| goods, furniture and street props | 222,578 | 206,807 | -15,771 |
| lanterns | 132,634 | 129,812 | -2,822 |
| vegetation | 124,506 | 117,382 | -7,124 |
| custom elements | 8,964 | 12,120 | +3,156 |
| stall bases | 16,856 | 6,184 | -10,672 |
| paving | 3,444 | 3,588 | +144 |

The increase is mostly architecture: two more buildings, three turrets, a taller tower, the inn's larger roof and the terrace's stair and skirt modules. The custom cloth, pennants and paving seals together are 12,120 triangles.

## Largest contributors and proposed substitutions (targets are for meshes P2 must make and measure)

| Component | Instances | Triangles each | Total now | Target each | Saving |
|---|---|---|---|---|---|
| `MV-Corner_Exterior_Brick` | 51 | 3,102 | 158,202 | 300 | 142,902 |
| `FP-Lantern_Wall` | 46 | 2,822 | 129,812 | 600 | 102,212 |
| `SN-CommonTree_3` | 21 | 3,505 | 73,605 | 1,500 | 42,105 |
| `AV-mdvl_village_window_box_01` | 17 | 1,330 | 22,610 | 400 | 15,810 |
| `SN-CommonTree_1` | 3 | 6,265 | 18,795 | 1,500 | 14,295 |
| `FP-FarmCrate_Apple` | 4 | 4,028 | 16,112 | 600 | 13,712 |
| `MV-Door_8_Round` | 16 | 1,142 | 18,272 | 400 | 11,872 |
| `FP-Crate_Wooden` | 8 | 1,576 | 12,608 | 230 | 10,768 |
| `FP-Barrel` | 19 | 824 | 15,656 | 300 | 9,956 |
| `MV-Balcony_Simple_Straight` | 10 | 1,120 | 11,200 | 132 | 9,880 |
| `SN-Bush_Common_Flowers` | 9 | 1,368 | 12,312 | 500 | 7,812 |
| `AV-mdvl_food_cabbage_01` | 6 | 1,448 | 8,688 | 300 | 6,888 |

## Assessment by topic

| Topic | Assessment |
|---|---|
| Geometry | 968,466 now; 532,062 projected. The earlier 350,000 figure is not reached by substitutions; reaching it needs lower-detail wall and roof modules or fewer backdrop trees, decided on a browser measurement |
| Materials | 59 distinct (+6 against P1.3: flat cloth, pennant and paving colours). The cafe pack's textured materials should be atlased; custom flat colours can share one palette texture |
| Draw calls | Depends on materials, not on building count, if each district is merged by material; repeated modules (wall bays, windows, piers, lanterns, awning bays) suit `InstancedMesh` |
| Texture memory | Unchanged from P1.2: architecture and nature up to 2048 px, props up to 4096 px (to be downscaled), cafe pack with normal and roughness maps |
| Visibility | The terrace and the denser bazaar hide more of the far town from any one street; a distance-based level for backdrop trees and far roofs is plausible. To be measured |
| Collision | Box proxies only: about 92 boxes for buildings, rows and terrace; steps as treads or ramp proxies |
| Level of detail | Three candidates carry most of the load: lanterns, brick piers, trees |
| Two-sided cloth | Awnings and pennants are single-surface and must render double-sided; alpha is not needed |

**Credible path:** substitutions, instancing of repeated modules, per-district static merge, one LOD step for trees and far roofs. **Unproven** until one archetype is measured in the real page (12).
