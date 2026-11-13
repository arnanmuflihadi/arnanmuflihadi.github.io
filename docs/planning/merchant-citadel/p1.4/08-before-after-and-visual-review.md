# 08 - Before/after comparison and visual quality review

Pairs from the same cameras and light: [A aerial](visuals/before-after-a-hero-aerial.jpg), [B merchant street](visuals/before-after-b-merchant-street-gameplay.jpg), [B2 street at eye height](visuals/before-after-b2-merchant-street-eye.jpg),
[C bazaar](visuals/before-after-c-central-bazaar.jpg), [D Exchange Hall](visuals/before-after-d-exchange-hall.jpg), [E service court](visuals/before-after-e-secondary-service-court.jpg), [E2 artisan lane](visuals/before-after-e2-secondary-artisan-lane.jpg), [F tea route](visuals/before-after-f-tea-lookout.jpg).

## What changed, measured

| Measure | P1.3 | P1.4 |
|---|---|---|
| Permanent buildings | 22 | **24** |
| Building archetypes in use | 11 | 14 |
| Vertical accents on the skyline (towers, turrets) | 1 | 4 (hall tower and three turrets) |
| Levels | 2 (ground, podium +1) | 3 (ground, terrace +1, podium +2) |
| Highest point above the bazaar | 22.8 m | 26.8 m |
| Bazaar: free stalls / awning rows | 12 / 0 | 4 / 4 (16 bays) |
| Bazaar edge enclosed / active | 38% / 20% | 46% / 29% |
| All tested edges enclosed / active | 51% / 35% | 55% / 35% |
| Buildings off the grid | 0 | 6 (6 to 18 degrees) |
| Developed envelope | 70.5 x 98 m | 72.5 x 98 m |
| Triangles, unoptimised | 915,026 | 968,466 (+6%) |
| Camera: directions fully clear / share of all samples clear | 48 of 92 / 79% | 35 of 84 / 79% |

## View by view

| View | Changed in form | Not changed, or weaker |
|---|---|---|
| Aerial | Turrets at the junction and both terrace corners; awning rows draw a street through the bazaar; the terrace reads as a platform before the hall; the inn closes the west edge | Still an open field around the town; lanes as P1.3 |
| Merchant street | Tower house on the junction corner; paving seal; pennant line; cloth awnings; the hall sits visibly higher at the end | Street walls are where they were |
| Bazaar | A market street instead of scattered stalls; pennants; tower houses and steps close the north side | Plaza floor is one tile; awning cloth is flat-coloured |
| Exchange Hall | Terrace, steps, standards, taller tower with four seals, dormers | The hall's walls are unchanged |
| Secondary | Workshops turned 6 degrees | Otherwise as P1.3. **This is the area P1.4 improved least** |
| Tea lookout | Tea house turned to the view; lamp; rearranged tables | No level change, no view until terrain exists |

**Changing only light or colour would not count as redesign, and P1.4 did not change either:** light, palette and materials are those of P1.3.

## Visual quality review (internal, provisional; not an approval)

Scores are 1-5 for the nine criteria of the brief.

| Output | Composition | Reference interpretation | Cohesion | Spatial hierarchy | Architectural quality | Atmosphere | Gameplay readability | Constructibility | Performance feasibility | Mean |
|---|---|---|---|---|---|---|---|---|---|---|
| A Hero aerial | 4 | 4 | 4 | 4 | 4 | 3.5 | 4 | 4 | 3 | **3.83** |
| B Merchant street (gameplay camera and eye height) | 4 | 3.5 | 4 | 4 | 4 | 4 | 4 | 4 | 3 | **3.83** |
| C Central bazaar | 4.5 | 4 | 3.5 | 4.5 | 4 | 4.5 | 4 | 4 | 3 | **4.00** |
| D Exchange Hall and civic terrace | 4 | 3.5 | 4 | 4.5 | 4 | 3.5 | 4 | 4 | 3 | **3.83** |
| E Secondary street (service court, artisan lane) | 3.5 | 3 | 4 | 4 | 3.5 | 3.5 | 3.5 | 4 | 3.5 | **3.61** |
| F Tea lookout | 3.5 | 3.5 | 4 | 3.5 | 3.5 | 3.5 | 4 | 4 | 4 | **3.72** |

- **A Hero aerial.** Reads as one cluster with four tower and turret points, awning rows marking the market street and a raised terrace before the hall. Weak: the town still stands in an open field, and the bazaar's west and east edges are only half built (46% enclosed).
- **B Merchant street (gameplay camera and eye height).** Junction tower house, paving seal, pennant line, cloth awnings and the hall on its terrace as the destination. Weak: the 6.6 m camera still shows more roof than shopfront on the nearest buildings; the frontage itself is unchanged from P1.3 (71% enclosed).
- **C Central bazaar.** Three clear layers: goods and striped awning rows, the two halls, then tower houses and the hall. A 10 m market street with a cross-passage is immediately legible. Weak: the awning cloth is flat-coloured custom geometry beside hand-painted kit textures; the plaza floor is still one cobble tile.
- **D Exchange Hall and civic terrace.** Hierarchy now comes from level (terrace +1 m, podium +2 m), a 12 m flight of steps, guild standards, a taller tower with a seal on each face and dormers. Weak: still assembled from house modules, so the stone-and-timber detail is that of a large house; R08 and R09 could not be located, so their specifics were not studied.
- **E Secondary street (service court, artisan lane).** Unchanged in form from P1.3 except two workshops turned 6 degrees. Honest position: P1.4 put its effort into the bazaar, hall and street; the secondary quarters gained least. R10 images were not viewed.
- **F Tea lookout.** Tea house turned 18 degrees to face the lookout corner, veranda on posts, lamp on the lane, laid tables, red tree. Weak against R11: no wrap-around deck or level change, and without terrain there is nothing to look out over yet.

**Mean of the six outputs: 3.81 / 5.** The target is a human-reviewed 4 / 5; this internal figure is below it and is not a claim of approval.
The lowest column is performance feasibility: every image is a Blender render and the triangle count rose again.

## Where it is still generic, and the root cause

1. **Secondary quarters.** Root cause: they are built from the two plainest archetypes (workshop, warehouse) with no form of their own. More dressing would not fix that; a distinct workshop type (open-fronted, with a lean-to) would.
2. **Exchange Hall walls.** Root cause: the kit has no civic-scale module (tall windows, stone arcade). Level and tower compensate; a small set of custom civic modules would be the real fix.
3. **Cloth and painted texture side by side.** Root cause: custom cloth is untextured.
4. **No terrain.** Root cause: phase order (town first). The lookout and the aerial both wait on it.
