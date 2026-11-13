# 11 - Visual QA report: approved P1.1 and P1.2 compared

Reviewed: the four ASSET-BACKED BLENDER BLOCKOUT views of each revision from the same cameras, the archetype sheets and roof plans. These are
Blender EEVEE renders, **not browser renders**. Scores are internal and provisional. The ten criteria are those of the owner's brief; P1.1 was
re-scored on them (its own report used nine different criteria and averaged 3.78).

Side by side: [A aerial](visuals/before-after-a-aerial.png), [B merchant street](visuals/before-after-b-merchant-street.png), [C bazaar](visuals/before-after-c-central-bazaar.png), [D Exchange Hall](visuals/before-after-d-exchange-court.png).

| Criterion | P1.1 | P1.2 | What changed, and why the score is what it is |
|---|---|---|---|
| Architectural coherence | 4 | 4 | One building kit throughout. New publishers appear only as goods and furniture. Held at 4: the Avramania stall and goods are flat-shaded and read as a different hand at close range. |
| Commercial identity | 3 | 4 | Every shop now has a trade sign with a pictogram, a canopy or a jetty, and goods by the door; the two halls sell different things; guild offices are marked. In P1.1 shops were told apart only by long red banners. |
| Building proportions | 4 | 4 | Unchanged modules and heights. The jetty adds 1.12 m of overhang at 3 m and reads correctly beside the 1.9 m figure. The hall was not enlarged. |
| Landmark hierarchy | 4 | 4 | The hall gains a gabled entrance porch with the seal, darker roofs and burgundy banners, and is the visible end of the street from the gate. Held at 4: at the gameplay camera on the street the top of the tower is still out of frame. |
| Bazaar quality | 3 | 4 | Five stall kinds instead of two, counters and tables stocked with bread, cheese, fish, pottery and books, goods stacked at the hall corners, two halls with different trades. Held at 4: from above the plaza is still a large even field of cobble. |
| Spatial readability | 4 | 4 | Plan unchanged and still validated. The darker civic roofs and the porch make the destination easier to pick out; the lanes are as before. |
| Player-scale compatibility | 4 | 4 | Re-measured: 38 of 38 built edges walkable, nothing hanging below 2.18 m, camera clear on the axis. Held at 4 until tested in the engine. |
| Asset constructibility | 4 | 4 | Every visible component is a downloaded model, a disclosed variant or a disclosed custom item. Held at 4, not raised: there are now three publishers, an FBX pack that needs its materials re-linked, and windows mounted on the jetty face. |
| Visual polish | 3 | 3.5 | Colour grade to the palette, afternoon light, sky gradient and a quieter ground lift the images clearly. Not a 4: no terrain or backdrop, the cobble tile still repeats, and none of it has been seen in the game's renderer. |
| Production efficiency | 3 | 3 | Modular system kept, no new building type, 0 new downloads for architecture. But triangles rose from 779,806 to 847,312, materials from 29 to 53, and there are 10 custom meshes to author. The plan in 12 projects 461,419 triangles; nothing is measured in a browser. |

**Average 3.60 to 3.85 out of 5. The 4 / 5 target is not reached and is not claimed.** No criterion is at 5. The two below 4 cannot be raised inside a
Blender blockout: polish needs terrain, a backdrop and the game's lighting; efficiency needs the P2 substitutions made and measured. **Human approval is pending.**

Part of the visible improvement is presentation: the P1.2 views use warmer light and a different tone mapping than the P1.1 views. To judge
the design changes alone, compare shapes and content (jetties, porch, signs, goods), not brightness.

## View by view

| View | Works | Weak, and the root cause |
|---|---|---|
| A - The Trading Town | Roof hierarchy now reads: dark hall, halls, warehouse and lodges against lighter shops; porch marks the hall | The town still sits in an open field ringed by trees. Root cause: no terrain or island edge exists yet (P4), not a lack of props |
| B - The Merchant's Walk | Signs, canopies, jetties and flower boxes at eye level; porch and tower seal as the destination; clear centre | The camera's height shows more roof than shopfront on the near buildings. Root cause: the documented camera sits 6.6 m up in a 10 m wide street |
| C - The Bazaar of Awan | Five stall kinds, stocked counters, market cross, hall goods visible, hall dominant | Plaza surface is uniform. Root cause: one cobble tile; a paving pattern or a second tile is a P2 or P3 material task |
| D - The Exchange | Porch gives the entrance a hierarchy the flat front lacked; banners and seal in the guild colours | Court is plain by design; the lamp posts are still stretched house posts |

## Unresolved (largest first)

1. **Not seen in the game.** Lighting, colour grade, scale and motion are unverified in Three.js.
2. **Blockout finish.** Temporary ground, no backdrop, repeating cobble.
3. **Mixed shading styles at close range.** The Avramania stall and goods are flat-shaded; the cafe pack is semi-realistic; Quaternius is hand-painted.
4. **Tower top at the street camera** is cropped, as in P1.1.
5. **Jetty windows** are mounted on the face of a module that has no opening; fine in Blender, to be checked for flicker in the engine.
6. **Seal and sign pictograms** are first proposals and need the owner's eye.
7. **Chimneys have no flashing piece**; dormer cheeks sink slightly into the tiles (unchanged).
