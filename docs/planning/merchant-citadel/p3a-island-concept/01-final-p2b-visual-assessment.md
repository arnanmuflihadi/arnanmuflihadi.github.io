# 01 — Independent final P2-B visual assessment (the town as a game environment)

**Role taken:** environment art direction review. **Evidence looked at for this review:** 13 of the 14 matched Blender / Three.js pairs of batch 5 (`p2e-batch5/visuals/comparison/`; `c04` was seen only in the quantisation difference sheet), the live preview through the game's real controller and camera (section 02's tests and seven new captures), and the Blender assembly of the 24 buildings. Scores are provisional internal observations, **not approval**. Images named `cmp-*` are batch 5's; images named `v*` are the new Blender massing renders of this phase (island concept, not the browser).

## 1. Verdict in one paragraph

The town works where the player actually stands. Merchant Street aims at the Exchange Hall and its clock tower (`cmp-t03`), the bazaar is lively and legible (`cmp-t04`), and the Civic Terrace is a proper formal court (`cmp-t08`, `cmp-t09`). What makes it look unfinished is almost entirely **what is not there**: no ground but a flat green plane, no backdrop behind the hall, no threshold at the arrival, no edge, no panorama at the tea lookout. Of the weaknesses I rank highest, five are landscape, one is camera rules, one is dressing, and none requires rebuilding a building.

## 2. Weaknesses ranked by effect on the experience

| # | Weakness (what the player notices) | Evidence | Cause | Fixed by | Label |
|---|---|---|---|---|---|
| 1 | **The hall has nothing behind it.** The town's landmark stands against empty sky at the edge of a lawn; from the air it is one roof mass among several | `cmp-c01`, `cmp-t01`, `cmp-t09` | 5 missing landscape | the island: a crag and trees behind the hall (`v4`, `v4b`) | VISUAL-DEFECT |
| 2 | **The arrival has no threshold.** The player starts on a wide cobble field between two near-identical gabled houses; nothing says "you have arrived" | `cmp-t02` | 5 missing landscape, 2 placement (E01/E02 are the same volume) | the island: a lower quay and a 3 m stair up to the gateway (`v3`); the twin gables stay | VISUAL-DEFECT |
| 3 | **The tea lookout looks at a lawn.** The district named for its view has no view | `cmp-t07`, `cmp-t10` | 5 missing landscape | the island: descending tea benches, stream, cliff, Tea Stack (`v5`) | VISUAL-DEFECT |
| 4 | **Camera collapses at low eaves and at the hall porch** (0.77–0.84 m, character faded to 0.14) | 02, `evidence/p3a-eave-*.jpg` | 6 camera (proxy rules), not geometry | two proxy rules and an opened rail (02); no building changes | CONFIRMED-TECH |
| 5 | **The forecourt rail fences off the landmark's doors** | `cmp-t09`, `evidence/p3a-rail-v0-at-rail.jpg` | 6 camera workaround of batch 5 | open the three centre bays (02) | VISUAL-DEFECT |
| 6 | **B15 and B16 read as the same house at eye level.** Batch 5 wrote that they read as two trades; in the door views the stone base, timber frame and corner quoins are the same and the balance and map board are too small to carry it | `cmp-c02`, `cmp-c03` | 1 architecture (shared A11 base), 7 storytelling | dressing only: larger hanging signs, different banner colour per house (burgundy/gold assay, blue chart), a visible chart table. Not a rebuild | VISUAL-DEFECT |
| 7 | **Open backs.** The west row, the warehouse south side and the tea lane face flat ground | `cmp-t05`, `cmp-t10`, `v9` | 5 missing landscape | the island: garden walls, hedges, the Caravan Green, tea benches | VISUAL-DEFECT |
| 8 | Repeated volumes (A04 ×3, A03 ×2) visible from the air | `cmp-t01` | 2 placement / asset reuse | leave; trees and terrain break the pattern from the air | PREFERENCE |
| 9 | Paving slightly cool in shade in the browser | batch 5 doc 01 | 4 lighting (preview rig) | lighting pass in P3, with the terrain's bounce colour | APPROVED-LIMIT (batch 5) |
| 10 | Wide, even cobble fields (arrival court, terrace) | `cmp-t02`, `cmp-t08` | 3 materials / 7 storytelling | later polish: paving bands, drains, carts, planters | PREFERENCE |

**Genuinely needs an architectural (kit) change:** none. **Needs proxy/config changes:** 4, 5. **Needs dressing:** 6. **Solved by the island:** 1, 2, 3, 7 and most of 8.

## 3. Rubric (provisional, 1–5; browser evidence unless stated)

| Domain | Score | One line of evidence |
|---|---|---|
| World composition | 2.5 today → the island is the fix | strong street-level axis (`cmp-t03`), but no silhouette, depth or backdrop (`cmp-t01`, `cmp-c01`) |
| Architecture | 4 | coherent kit, good roofs and shopfronts, hall reads as the landmark (`cmp-t08`); twin tower houses (`cmp-c02/c03`) |
| Environment | 1.5 | flat plane, no vegetation, no cliffs or water (every image) |
| Character and camera | 3 | normal routes fine (12.9 m on lanes), collapses at eaves and porch until the rules in 02 are applied |
| Rendering | 3.5 | consistent materials and AO, Blender and browser agree within 2–8 luma; cool shade; **frame rate not validly measured** |
| Gameplay readability | 3 | the hall guides the player up the axis; side districts lack pull (no visible reward from the street) |

Average 2.9; two domains below 3. That is a statement about the **environment being absent**, not about the 24 buildings.

## 4. What I did not verify

No human played it. No valid frame-time measurement exists (batch 5's was invalid). The island images are Blender massing, so everything the island is said to fix is `UNVERIFIED` in the browser until P3-B builds it.
