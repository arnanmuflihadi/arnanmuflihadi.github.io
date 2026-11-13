# 01 — District construction: B13, E04, E05 and the connected quarter

Coordinates: plan metres, x east, n north (Three.js z = −n). Heights are metres above the ground. "Local" means the building's own frame (front at −y). All images referred to are in [visuals/](visuals).

## 1. What the district is for

Before this batch the east side of the town was an empty lane: a paved strip at x 14–18, a paved court nobody could use, grass where B13, E04 and E05 belong, and a dead-end tea lane with no frontage ([before](visuals/before-after/ba-p5-east-aerial.jpg)). The design question was not "where do three more buildings go" but "what does a merchant walk through between the market and the lookout". The answer built here has three layers that are meant to read differently on foot:

| Layer | Character | Parts |
|---|---|---|
| **Public shopping street** | paved, enclosed by shopfronts, awnings and signs | the merchant street's east frontage (B07–B09, B14, E06, existing), the **tea lane** (E05's gallery and tables, the lookout beyond) |
| **Trade lane (Jalur Gudang)** | working lane, stone ground floors, goods at the doors | the 4 m warehouse lane x 14–18, **B13's lane gable** (two doors, guild seal, loading sign), **E04's lane front** (guild frontage: seal, two burgundy standards, coin sign) |
| **Service court and porters' path** | service-oriented: red-brick thresholds, loading station, wagon, lamps, fences | the **court** x 18–32, n 16–24 (B13's loading canopy south, E04's tally loggia north-west), the **porters' path** x 32–34 (n 18–48) bending to x 30–32 (n 48–52) |

The three layers meet at one place: **E05 stands where the service route meets the scenic one.** Its front (balcony gallery, tea tables) faces the tea lane; its west door opens on the bazaar's east market lane; its **east door is the end of the porters' path**, where the lookout terrace begins. That is the transition from busy market to quieter scenic district that the brief asked for, built into the plan rather than painted on a facade.

## 2. Composition review

| Criterion | What was built and measured |
|---|---|
| **Street enclosure** | The lane has an 8 m long two-storey gable (B13, 14 m of wall behind it) on one side and B07/B09 (their eaves reach x 13.9) on the other, so 4.6 m between facades; the court has a two-storey wall on each long side with 4.9 m clear between the lean-to edges (n 17.56 to 22.44), a deliberately intimate proportion for a service yard; the porters' path is 2 m of paving between the backs of E04, B14, E06 and a fence on its east edge. The tea lane's north side was open ground: a fence (x 23–27, n 60.4) now gives it a side. |
| **Architectural continuity** | Same module family (Quaternius Medieval Village walls, windows, doors, roofs), same stone ground floors and timber upper floors as the existing district, **dark civic roof tile** on B13 and E04 as on the Exchange Hall and the market halls (guild buildings), terracotta on E05 as on the shops. One accent added: sage green (`#6F7F55`) on E05's awnings, the tea route's colour. |
| **Warehouse access** | Doors on two sides: the lane gable (two doors) and the court side (double loading door under the hoist hatch, a window, a side door); the south wall has windows and the wagon. Goods station under a 6 m lean-to roof on two posts. |
| **Shopfront orientation** | B13 and E04 face the lane (P1.4), E05 faces the tea lane (north) as in P1.4. E04's *working* side faces the court (loggia), its *civic* side the lane. |
| **Service-yard proportions** | Court 14 x 8 m with a 2 m red-brick loading apron; the canopy posts stand 0.55 m inside the apron edge. The wagon (P1.4) stays in the middle; B13's own wagon moved to the south side. |
| **Relationship to the bazaar** | The lane enters the bazaar's south-east corner at N14 (unchanged); E05 joins the bazaar's north-east corner and the east market lane through its west door. |
| **Secondary loops** | `loop_exploration_east`: bazaar → lane → court → east opening → porters' path → gate → E05's east door → lookout terrace → tea lane → bazaar's north-east corner → east market lane → bazaar (70.6 s walking, 0.4 % of the time with the camera under 3 m). Both directions walked. A second loop through the cross street, court and lane (42.8 s). |
| **Tea Lookout approach** | Two routes now: the P1.4 tea lane (public) and the porters' path (service). E05 is a landmark on both; the lookout terrace is reached through a 2 m gate in its south fence (the P1.4 fence segment was removed there). |
| **Landmark visibility** | E05's balcony and gable are visible from the bazaar's north-east corner ([view](visuals/comparison/cmp-p5-bazaar-ne.jpg)); B13's dark roof, the hoist jib and E04's loggia read in the lane and court views and the quarter aerials ([aerial](visuals/before-after/ba-p5-quarter-sw.jpg)). Not checked: sightlines from the bazaar's south entrance and from the market halls' interiors. |
| **Player-scale composition** | All routes walked with the real controller; hoist, canopy, loggia and gallery are at 2.6–3.0 m, above the 1.9 m body. |

## 3. The three buildings

### B13 — Guild Warehouse (variant `A07w` of P1.4 A07; position unchanged (25.5, 12), turned −90°)

8 x 14 m, two floors (stone ground floor), dark round-tile roof, ridge along the long axis, 37,194 triangles in 24 primitives. Local frame: front (lane gable) y = −7, north long wall (court) x = −4.

* **Loading front (north wall, court side):** ground `S o o S s o S` (two round doors side by side forming the loading doors, pier, window, side door, pier); upper floor `P T D T P T P` with a **hoist hatch** (wood-grid door) above the loading doors. **Custom `CUS-Hoist`**: wall plate, 2.3 m beam, diagonal brace, iron pulley, rope and hook, with a crate half way up the rope, placed at the hatch at 5.0 m (below the eave). **Canopy:** a 6 m lean-to of three `MV-Roof_Wooden_2x1` modules at 2.6 m on two posts. **Tally station** under it: `FP-Table_Large`, scales, ledger stack, sacks, two barrels, two wall lanterns.
* **Lane gable:** two ground doors, the guild seal at 8.3 m (P1.4), a **new burgundy crate sign** (`CUS-Sign_Crate_burgundy`), crates, a barrel and a sack at the corners.
* **South wall:** windows as P1.4, the wagon moved 0.8 m (to (21.3, 5.6)); P1.4's vines removed (they stood on the canopy side).
* Deviations from P1.4: north-wall openings, canopy, hoist, tally station, sign; P1.4's five crates and barrels at (27–30.4, 17.3) removed (they stood where the canopy is and overlapped the tally table by 0.4 m).

### E04 — Merchant Counting House (variant `A05c` of P1.4 A05; position unchanged (22.5, 28), turned −90°)

8 x 8 m main block (two floors, stone ground, dark tile) plus a **strongroom wing**: 6 x 4 m, one floor, stone with barred windows only, own dark roof ridge running north-south, attached to the east gable (local (0, 6)); 31,628 triangles in 22 primitives.

* **Identity from function:** a *tally loggia* on the court (south) side — a 4-module lean-to on three posts over the stone wall and the court door, with a tally table, scales, ledger stack, bench and sacks — because a counting house in a trading quarter weighs and records at the door; a *strongroom* wing because the same house stores what it records; guild frontage on the lane: the seal at 8.25 m, **two** burgundy standards (P1.4 had one), the burgundy coin sign (as P1.4).
* Deviations: wing, loggia, second standard; the P1.4 right-hand coin sign was removed (it would pass through the loggia roof); P1.4's crate at (20.0, 23.2) removed (inside the loggia now) and the tree at (30.5, 31.5) is outside the preview's dressing (vegetation is out of scope) but would also have stood on the wing.

### E05 — Tea Route Merchant House (variant `A03cT`; position unchanged (25.5, 53.5), turned 180°)

**Deviation from P1.4, decided on evidence: two floors, not one.** P1.4 gives E05 the archetype A04b (6 x 4 m, single storey, 6.7 m). At the corner where the bazaar's east frontage (B14, E06: both single-storey) meets the tea lane that leaves the lane with one low shop and nothing to mark the entrance to the scenic district ([before](visuals/before-after/ba-p5-tea-entrance.jpg)). E05 is built as an 8 x 4 m two-storey house (the A03c shallow house walls and roof, 9.7 m high, ridge east-west, gable to the bazaar). It adds 16.3k triangles over the P1.4 contract (24,606 against 8,278).

* **Gallery:** a balcony on four posts over the lane in the pattern of the merchants' inn (wood floor tiles, straight rails with returns), so the ground floor becomes a 1.9 m deep covered tasting gallery: two tables with cloth and stools, a menu stand, jar baskets, herb bundles hanging from the underside, a potted plant, lanterns. Red-brick gallery strip in the paving. The gallery posts stand at n 57.4, so the lane centre node N41 moved from n 58 to n 59 (0.6 m would have been too close).
* **Three doors, three audiences:** front door under the gallery (tea lane), **west door** on the bazaar's east market lane (two sage awnings, a leaf-sprig sign), **east door** for porters, facing the lookout terrace, with sacks, a chest and a ladder against the wall.
* **Custom:** `CUS-Awning_tea` (sage green, a palette extension), `CUS-Sign_Leaf_wood` (two-leaf sprig; replaces the cup that P1.4's schedule gave E05, which belongs to the tea house).
* **Slot between E05 and E06:** the 2.2 m gap is closed by two fences (see 03); E05 therefore has no ring walk.

## 4. Other changes in the quarter

| Change | Reason (evidence) |
|---|---|
| **Porters' path** x 32–34, n 18–48 and x 30–32, n 48–52 (cobble), fence along its east edge (x 35, n 25–51), three lamp posts at x 34.4 | closes the second exploration loop; the P1.4 plan had no east-side route from the court to the lookout |
| Red-brick loading apron (24–32, 16–18), loggia floor (18–26, 22–24), gallery strip (22–30, 54–58) | the red brick marks thresholds, as at the market halls (batch 2) |
| Terrace furniture moved east (bench 1.6 m, table, cloth, two stools, mug, platter 2.8 m), P1.4 lantern post (30.6, 51.4) and fence segment (31, 52) removed | the porters' path reaches E05's east door through that gap; the table stood in front of the door (network test) |
| Fences closing the E05–E06 slot ((23.3, 50.3), (29.3, 50.4)) and a dead-end pocket behind B14 ((19.4, 37.3)) | camera and autopilot evidence in 03 |
| Fence on the tea lane's north edge (x 23–27, n 60.4); a fence at the court's south-east corner (32, 17) | enclosure |
| District rule: new district D7 (x ≥ 14, n < 37), D8 extended to E05, D1 narrowed to x < 14 | merge and culling groups follow the built districts |
| Paving rows, preview data: `p2a_data.py` | [production-config.json](production-config.json) |

## 5. Custom versus downloaded geometry

Downloaded and placed as authored (Quaternius Medieval Village and Fantasy Props, Avramania, Syntaxes of Play): all walls, windows, doors, roofs, balconies, posts, lanterns, wagon, crates, barrels, sacks, scales, tables, stools, jars. **Material variants (not new geometry):** the dark civic roof tile on `MV-Roof_RoundTiles_4x6` and `_8x8` (the dark grade of batch 1), burgundy banner cloth. **Custom, authored here:** `CUS-Hoist`, `CUS-Awning_tea`, `CUS-Sign_Leaf_wood`, `CUS-Sign_Crate_burgundy` (an existing glyph on a new field), plus the lean-to roofs, loggia and gallery which are *assemblies* of downloaded modules. The strongroom wing is an assembly of downloaded wall and roof modules. No AI-generated geometry; no new asset pack ([06](06-assets-licence-registry.md)).

## 6. Corrections found while building (each measured)

| Found by | Defect | Correction |
|---|---|---|
| network test, first run | lantern posts of the new path stood **in** the path (x 33) | moved to x 34.4 |
| network test | the P1.4 terrace bench and table stood in the new gate / E05's east door | moved east, gate shifted to x 30–32 |
| district test | autopilot stuck near the loading-bay node (turn-around next to the wagon's corner) | node N48 moved 0.4 m away; the later camera finding explains the wagon |
| first renders | P1.4 crates overlapped the tally table | removed, replaced by the loading station |
| compression test | slot between E05 and E06: camera 0.52 m, median 1.13 m | closed by fences; a first closure left a sliver at the south-west corner (flood-fill check), second position verified |
| E05 block circuit | autopilot jammed in the 1.8 m pocket behind B14 | closed by a fence |
| real-keyboard session | camera 0.5 m for 0.2 s next to a wagon (phantom camera hit on an oriented prop's AABB) | low-prop camera rule |
| hall-camera test | screen-coverage fractions depended on the browser pane's aspect ratio | test fixed to 1280 x 720; earlier numbers discarded |
