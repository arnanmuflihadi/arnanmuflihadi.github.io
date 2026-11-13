# 10 — Final P2-B architectural construction review

**This is a package for human review, not an approval.** I do not self-approve any acceptance item. "Complete" below means built and checked by the tests named; it does not mean approved.

## Acceptance gate

| Gate item | State | Basis |
|---|---|---|
| 24 real buildings | **met** (24 real, 0 surrogates, 66 instances) | `scene-census.json` read from the live Three.js scene |
| B15 and B16 integrated | **met** | placement within 1.1 cm of Blender, collision 271/271, routes pass |
| The Exchange Hall remains dominant | **met at street and terrace level; not at aerial height** | hall tower 26.79 m vs tower houses 15.79 m; t03, t08 vs t01 |
| Routes traversable | **met in scripted tests** | network 65/65 both ways, district 45/45, stairs 7/7, real-key session 17/17 |
| Camera documented and usable | **partly met** | measured and documented (03); severe cases remain in the west row, veranda and east court; human judgement needed |
| GLB integrity verified | **met** | `glb-structural-inspection.json`; merged geometry integrity float |
| Full-town performance measured | **partly met** | draw calls, triangles, memory, size measured; **frame times invalid** (loaded machine); no lower-end device |
| Visual consistency reasonable | **provisional** | my reading of 14 matched pairs (6 examined closely); style approval is the owner's |
| Limitations documented | **met** | 03, 04, 08 |

## What is complete, provisional, or needs human judgement

**Complete (built and checked by tests):**
B15/B16 assemblies and the 24-building kit; Blender build scripts; GLB 46,517,600 B (SHA-256 prefix 9288a67693af) with float fallback and three variants; asset registry and provenance (170 downloaded, 23 custom, no new pack); authoritative `scene.json`; whole-town matched Blender and Three.js set (14 pairs, 14 before/after sheets); Civic Terrace before/after; complete navigation and collision test set; corrected platform reporting with explicit criteria (7/7); terrace edge protection; forecourt rail fixing the descent compression; terrain-interface contract; backlog.

**Provisional:**
* Visual consistency and hall hierarchy (my reading).
* Camera and fade analysis: cause attribution is measured, acceptability is not decided; fade system untested on the first island.
* Draw-call and triangle counts per view (deterministic, but only the views I chose).
* Optimisation findings: float-versus-quantised sizes and visual diffs are measured; the **frame-time effect on the 24-building kit was not re-measured** and batch 4's results are carried over.
* Paving tint (improved, not matched).

**Needs human judgement:**
1. Does the town look right (style, repetition, flat stand-in ground)?
2. Is the forecourt rail acceptable, given it closes the hall's doors?
3. Are the 0.84 m camera cases in the west row, 0.25 and 0.43 opacity at the tea veranda and east court, and the 0.75 m B10–B11 gap acceptable, or should the geometry change?
4. Tea-green accent and E05's two floors (deviation from P1.4).
5. Whether to open the terrace's south edge (a 1 m drop) or add a rail.

**Not done, and I say so:** a valid frame-time benchmark; any measurement on lower-end hardware; Meshopt, Draco or KTX2; a human playtest; mouse-rotated camera, gamepad or touch tests; integration into the game (nothing was integrated, committed or deployed).

## Boundaries kept

Production controller, camera, character, input, collision and the vendored three build are byte-identical (SHA-256 in `evidence/production-code-sha256.txt`); nothing was committed, deployed or integrated; no terrain, quests, NPCs, combat or dragon work; no paid, AI-generated or newly downloaded asset; the batch 4 kit and evidence were preserved (`merchant-citadel-p2a/baseline-batch4/`).

## Recommendation

After your review, the next phase I would propose is **whole-town environmental polish and floating-island landscape design**, starting from `07-terrain-interface-contract.md`, **and** a valid performance run on a quiet machine plus at least one lower-end device before more triangles are added. I stop here, as instructed, and will not begin that phase without approval.
