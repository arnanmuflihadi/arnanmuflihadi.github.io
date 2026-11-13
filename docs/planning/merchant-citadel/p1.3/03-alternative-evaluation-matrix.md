# 03 - Alternative evaluation matrix

Numbers come from `asset-evidence/alternatives-metrics.json` (nominal footprints) and `asset-evidence/massing-ray-tests.json` (massing geometry).
They compare layouts on equal terms; the selected layout was then built with the real assets and re-measured (08).

| Measure | P1.2 baseline | A - Refined (18) | B - Compact (22) | C - Expanded (24) |
|---|---|---|---|---|
| Buildings (new) | 17 (0) | 18 (1) | 22 (5) | 24 (7) |
| New assets to download | 0 | 0 | 0 | 0 |
| Archetypes (incl. variants) | 10 | 10 | 11 | 11 |
| Developed footprint (m) | 74.5 x 98 | 70.5 x 98 | 70.5 x 98 | 70.5 x 98 |
| Terrain support zone (m) | 94.5 x 134 | 90.5 x 134 | 90.5 x 134 | 90.5 x 134 |
| Market configuration | 2 halls, 12 stalls, open edges | 2 halls, 12 stalls, corner houses and registry on the edge | as A plus a perimeter shop and the tea route house | as B plus two more edge shops |
| Primary route (m) | 76.8 | 76.8 | 76.8 | 76.8 |
| Walking graph: nodes / edges / loops | 31 / 39 / 9 | 35 / 45 / 11 | 37 / 47 / 11 | 37 / 47 / 11 |
| Network length (m) | 437.4 | 463.6 | 452.7 | 452.7 |
| Lane width, merchant street clear width | 4 m, 8 m | 4 m, 8 m | 4 m, 8 m | 4 m, 8 m |
| Wall enclosure / active frontage, all tested edges | **28% / 22%** | **33% / 26%** | **51% / 35%** | **54% / 38%** |
| Hall tower visible from (of 15 tested points, massing) | 8 | 6 | 7 | 7 |
| Camera: travel directions fully clear (massing ray test) | 50 of 76 (65%) | 57 of 88 (64%) | 52 of 92 (56%) | 51 of 92 (55%) |
| Camera: mean clear share on secondary routes | 69% | 77% | 69% | 68% |
| Triangles, unoptimised (estimate from archetype counts) | 847,312 | 855,446 | 954,752 | 971,086 |
| Triangles after the P1.2 substitutions (projection) | 474,949 | 480,861 | 539,065 | 550,955 |
| Building collision proxies (boxes) | 51 | 52 | 56 | 58 |
| Materials / draw-call implication | 53 materials | same 53 | same 53: new buildings reuse existing materials, so batches grow in size, not number, if merged by material per district | same |

## Enclosure by place (wall / active)

| Place | P1.2 | A | B | C |
|---|---|---|---|---|
| Merchant street | 73% / 73% | 71% / 71% | 71% / 71% | 71% / 71% |
| Artisan lane | 30% / 30% | 30% / 30% | 62% / 30% | 62% / 30% |
| Warehouse lane | 20% / 20% | 14% / 14% | 46% / 26% | 46% / 26% |
| Bazaar perimeter | 16% / 0% | 24% / 8% | 38% / 20% | 45% / 27% |
| Arrival court sides | 0% / 0% | 19% / 19% | 44% / 44% | 44% / 44% |
| Civic court sides | 58% / 58% | 75% / 58% | 83% / 67% | 83% / 67% |
| **All tested edges** | **28% / 22%** | **33% / 26%** | **51% / 35%** | **54% / 38%** |

## Reading the matrix

| Criterion | A | B | C |
|---|---|---|---|
| Visual enclosure | Small gain (28 to 33%). Lanes still one-sided | **Large gain (28 to 51%).** Lanes two-sided, arrival and bazaar edged | Slightly more than B (54%) |
| Navigation | Cross street added, but 12 m of it runs between fences | Cross street, pocket court, service court, workyard: loops pass frontages | Same network as B |
| Secondary districts | Warehouse still behind a back court | Warehouse and counting house share a court on the lane; tea house one lane from the bazaar | Same as B |
| Camera | Best of the three (more open ground) | About the same as P1.2 in the massing test | Slightly worse than B: two more buildings on the hall-side lanes |
| Asset reuse | 1 building reused | 5 buildings from existing archetypes, one new shallow variant from verified modules | 7 buildings |
| Performance | +8,134 triangles | +107,440 | +123,774 |

## Selection: B, 22 buildings

- **A does not solve the problem.** Relocation alone lifts enclosure by 5 points; the lanes and bazaar edges stay open. This answers the brief's question directly: moving buildings is not enough.
- **B is where the town changes character.** Enclosure rises from 28% to 51% and active frontage from 22% to 35%, every district gains an edge, and each added building has a named spatial job.
- **C buys little.** Two more buildings add 3 points of enclosure, all on the bazaar edge, cost about 16,334 triangles, narrow the hall-side lanes visually and slightly worsen the camera test. E06 would also stand on the corner where the tea lane leaves, crowding the one quiet route.
- **Not chosen because it is the middle option.** If the owner wants a busier bazaar edge later, E07 (west edge) is the better of C's two additions and can be added without moving anything; that would make 23.

The count of 22 is appropriate because it is the smallest number at which the lanes, the arrival court and the bazaar all have built edges; below it one of those stays open, above it the gain per building falls sharply.
