# 01 — District selection and construction

## 1. What was left, and why this district

Built before this batch: 14 of the 24 P1.4 buildings (B01-B09, B14, B17, E03, E06, E07). Unbuilt: **B10, B11, B12** (D6 Lorong Lentera, artisan lane), **E01, E02** (D1 Gerbang Niaga, south gateway), **E05** (D8 tea lane), **B13, E04** (D7 Jalur Gudang, warehouse lane), **B15, B16** (D4 Pelataran Bursa, terrace tower houses).

| Candidate | Adjoins the existing market? | Decision |
|---|---|---|
| D6 B10, B11, B12 | The lane runs behind the west shop row (B04-B06) and meets the commercial street through the cross street at the junction; B11 closes that cross street (the P1.4 vista) | **Built** |
| D1 E01, E02 | They stand at the south end of the commercial street, where the player spawns; without them the street begins in an empty field | **Built** (completes the street's first view and its frontage from the court to the bazaar) |
| D8 E05 | Continues the east bazaar edge (B14, E06) but is a one-building extension of a finished edge | Left; backlog |
| D7 B13, E04 | A warehouse lane and a service court (A07, 42k triangles plus the court): a district of its own, not an extension of the artisan connections | Left; backlog |
| D4 B15, B16 | Tower houses on the civic terrace; they belong with the Exchange Hall's court | Left; backlog |

Nothing was built to raise the count: each of the five touches the lane, the cross street or the street's first view.

## 2. The five buildings

| Building | Kit node | Position (x, n), turn | Triangles | Architectural device added to the P1.4 archetype |
|---|---|---|---|---|
| B10 smithy | `A06s` (A06) | (-21.5, 11), 84° | 21,688 | **open forge bay**: three Roof_Wooden lean-to modules on the south wall, posts, anvil, quench trough, whetstone, coal sacks, tool rack with hammer and pick; its east end rests on the lane-entrance post of the P1.4 dressing |
| B11 potter's shop | `A04bP` (A04b) | (-20.5, 20), 90° | 12,435 | gold-and-cream cloth awning (the market rows are blue and burgundy), **brick kiln with a flue behind the shop** (a 2 × 2 m box of three scaled brick wall modules, a brick-tile cap, a chimney), rows of vases at the door, jar shelf, clay trough |
| B12 joiner | `A06j` (A06) | (-21.5, 29), 96° | 16,062 | different wall system (plaster and half-timber on a stone-free wood-corner shell instead of the smithy's stone), **open drying shed** over the workyard with three wood piles, ladder, cart wheel, bench with axe, wheelbarrow of offcuts, chopping block |
| E01 outfitter | `A04bO` (A04b) | (-12, -1), 78° | 12,090 | burgundy awnings, tool rack with a rope coil, barrels, bags, a basket, a signpost at the court's edge |
| E02 carrier's office | `A03cC` (A03c) | (12, -2), -90° | 15,862 | stacked crates and hay at the door's left, a hitching rail on its right; the P1.4 court dressing already supplies the cargo wagon and crates five metres out, so the office adds only its own load |

Per-building signs are the P1.4 trade signs (hammer, jar, hammer, crate, scroll) placed as separate nodes; all five buildings keep their P1.4 doors, windows, roofs and chimney shapes. **Disclosure:** the kiln, the lean-to roofs, the awning colour and the arrangement of goods are compositions made in this batch from verified downloaded modules (Quaternius Medieval Village and Fantasy Props, Avramania, one Syntaxes of Play basket) plus the project's own custom awning and sign geometry; no new third-party model was introduced beyond the 25 listed in 05.

## 3. How the district strengthens the town

* **Continuous frontage and enclosure.** The artisan lane is now a 2.9-4.4 m street between the west row's backs (x ≈ -14.1) and three workshop fronts (x ≈ -18.5 to -16.3 with goods); looking north from the lane's south end the player sees a smithy, a potter and a joiner in sequence ([lane view](visuals/comparison/cmp-p4-lane-north.jpg)).
* **A composed vista.** From the junction the cross street ends on the potter's gold awning and vases ([cross-street view](visuals/comparison/cmp-p4-cross-vista.jpg)); this was a blank field before.
* **District identity.** The lane is red brick (P1.4), stone-and-timber trades, one lean-to per workshop (south for the smithy, north for the joiner: the two bays are not mirror images), a kiln stack rising behind the potter; the gateway shops use cloth colours and goods of travellers and carriers.
* **Gameplay scale.** The party gap between the smithy and the potter stays 3 m clear, the same between the potter and the joiner; all door nodes are reachable (04).
* **Visual continuity with the Bazaar.** Same kit, roofs, materials, AO bake and lighting; the lane's red brick meets the bazaar's court brick at the artisan workyard.

## 4. Corrections made on the way (each found by a test or an image)

| Finding | Evidence | Fix |
|---|---|---|
| The smithy's forge bay on its north side narrowed the potter gap to 1.2 m and blocked the planned alley | district route test: the circumnavigation of B11 failed | bay moved to the south side (mirrored), the gap is 3 m again |
| The potter's kiln first stood between the potter and the joiner and left 1.0 m | same test | kiln moved behind the shop |
| The joiner's drying shed overlapped three P1.4 workyard props (workbench, anvil log, barrel) | 4 solid overlaps in the first district test | the three duplicates are dropped from the dressing (the well stays); recorded in `scene.json` corrections |
| My first carrier's office added a second wagon beside the court's own wagon, and its crate and rail stood in front of the door | rendered view | wagon and door-line items removed |
| `FP-Pot_1` rendered as a translucent blue bowl | rendered view | replaced by `AV-mdvl_interiors_pot_01` |
| Door nodes placed by hand sat 0.2-1.2 m from the free centre | network test: 5 edges failed | nodes moved to the point of maximum clearance on the proxies (1.29-1.38 m) |
| Heavy small props (barrel 2,348, basket 2,200, sack 1,529, rope coil, rope, anvil log 3,808, fruit basket 3,646, wheelbarrow) | kit report | module LOD to 600-1,400 triangles each, not visible at play distance |

## 5. Limits, plainly

* The ground is still the preview's flat stand-in; the lane's east side is the plain backs of B04-B06; there is no vegetation.
* B10, B12 and E01 stand at 78-96°, so their placement check is a bounding-box bound, not a 0.5 cm match (B11 and E02, at 90° multiples, match to 0.05 cm); the nodes' own boxes match Blender to 0.01 cm.
* The variants exceed the P1.4 schedule envelopes: B10 by 0.6 m to the south (the bay), B11 by 1.3 m to the west (the kiln), E01 by 1.4 m to the south (barrels, signpost), E02 by 2.0 m into the court (hitching rail). `expected-envelopes.json` records both.
* Interiors: none (closed doors), as for the other shops.
