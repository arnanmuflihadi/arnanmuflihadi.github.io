# 01 — Civic Terrace completion: B15, B16 and the Exchange Hall forecourt

All geometry here is an assembly of modules from the registered CC0 packs plus a few custom flat-colour props (disclosed in 06). Everything is in the isolated preview `merchant-citadel-p2a/`; nothing is in the game.

## 1. What was built

| | B15 Merchant Assay Office | B16 Cartographer (chart maker) |
|---|---|---|
| Position (plan) | west of the stairs, (−18, 67) | east of the stairs, (18, 67) |
| P1.4 base | A11 (tower house) | A11m, **redesigned**, not mirrored |
| Kit node / triangles | `A11a` / 31,804 | `A11c` / 34,578 |
| Envelope (x, n) | −23.32…−12.17, 61.29…72.08 | 12.00…23.25, 61.29…71.98 |
| Top above ground | 15.79 m | 15.79 m |
| Walls | stone-and-plaster mix with stone base courses on all four faces | timber-frame upper floor over plaster on the front and left faces |
| Roof | dark civic tile on body and turret (the Guild grade) | terracotta, ridge turned 90° from B15 |
| Distinct features | gold-pan **assay balance** (custom `CUS-AssayBalance`) over the door, workbench with scales, coin and book stacks, chest, two burgundy banners, two chimneys | upper-floor **balcony** over the terrace side, **map board** (custom `CUS-MapBoard`: parchment, routes, way-stations, compass disc), book stand, scroll, compass sign (`CUS-Sign_Compass_wood`) |

B15 and B16 share the tower-house massing (hence the same 15.79 m top and the 11 × 10.8 m footprint) and differ in material, roof grade, ridge direction, silhouette and props; side by side they read as two trades, not one mirrored house.

**Hierarchy.** The Exchange Hall tower is 26.79 m, the tower houses 15.79 m (the hall's tower is 11 m taller). Hierarchy is carried by height, the podium and stairs, the clock-seal tower, the porch and the forecourt rail, not by tower-house height. The tower houses stand 4 m south of the hall's front line (their north walls at n 72.1, the hall's at n 76.3), either side of the stairs, so they frame the approach (t08, c01, c04 in `visuals/`).

## 2. Civic Terrace composition review (the hall unchanged)

Defects measured in the batch 4 state and what was done:

| Finding | Fix | Evidence |
|---|---|---|
| Player could walk off the terrace edge (platform test: body centre reached the edge, 7 runs 0 passes in the old aggregation) | two terrace-edge wall proxies at x = ±13.95, n 62–74, h 1.0, body only | `platform-test.json` |
| Descending from the hall steps pulled the camera to ~0.4 m (opacity floor) | forecourt rail at n 76.2 (five `MV-Balcony_Cross_Straight` bays, side returns) with matching proxies | `compression-cause.json`, `fade-motion.json` (porch-steps min camera 2.95 m, min opacity 0.83) |

**Consequence the owner must decide on:** the rail also closes the hall's doors to the player (the hall has no interior in any batch, so no loss today). It is dressing plus proxies in `p2a_data.py` and reversible in one edit. The first attempt, rails at the porch posts, did not fix the compression and was discarded.

Other terrace-level changes: nodes N60 (−19.0, 60.8) and N61 (19.0, 60.8) at the tower-house doors, edges N23–N60 and N24–N61, plaza rectangles for the two towers in the paving data.

## 3. Final small fixes from the whole-town review (measured defects only)

| Item | Action | Result |
|---|---|---|
| Cool paving in shade | baked warm albedo multipliers on the two brick materials (`PAVING_WARM`) | blue-minus-red on the lane fell 18.7 → 14.9 (lane), 15.9 → 12.4 (court), 23.7 → 21.2 (tea lane); **still cooler than Blender in shade**: the cause is the preview lighting rig (environment intensity), not the material (`paving-tint-before-after.json`) |
| E05 leaf sign read as a heart | redrawn as a pointed leaf on a stem | confirm in `visuals/browser/` t07; human check at 4–6 m |
| Plain warehouse walls (B13 south, E04 north) | ivy, open shutters, barrel, ladder, lanterns on B13; ivy, shutter, lantern on E04 | visible in t06 |
| Roof repetition | dark / weathered roof grades on B10, B12, B11, E02 | visible in t05, t01 |
| Buried chimney on E04's wing (batch 4) | removed | — |

## 4. Counts, read from the final GLB and the live Three.js scene

* 24 real buildings, 0 surrogates, 66 placed instances, 54 kit nodes, 547,307 triangles in the 24 buildings, 588,064 unique triangles in the kit (`scene-census.json`, `glb-structural-inspection.json`).
* Placement against the Blender build: 24 of 24 within 1.1 cm (B15 1.03 cm, B16 0.05 cm); orientation checks 3 of 3 (`autotest-scale.json`, rerun on the final kit).
* Geometry in the page: 602 geometries, 98 materials, 79 textures (97.98 MB GPU estimate with mips), load 389 ms in that run.
