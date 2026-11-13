# 07 — Remaining construction backlog, risks and limitations

## 1. Construction backlog

| Item | State | Note |
|---|---|---|
| **B15 Terrace Tower House West** (assay office, A11, at (−18, 67)) | **not built — the next planned step** | surrogate in the 24-building estimate (`?town24=1`); P1.4 gives it the guild seal at 8.0 m |
| **B16 Terrace Tower House East** (chart maker, A11m, at (18, 67)) | **not built — the next planned step** | surrogate; mirror of B15 |
| Ground, vegetation, sky | **stand-ins** (flat green plane, no trees: the preview skips vegetation) | the quarter's edges (south of B13, east of the porters' path, north of the tea lane) are unexplained open ground until real scenery exists; a fence line at the path and the lane is all there is |
| Floating-island terrain, transport, NPCs, quests, combat, dragon flight | out of scope | |
| Interiors | none; doors do not open | |
| Leaf sign for E05 | redraw | reads as a heart at 4–6 m (02) |
| B13 south wall and E04 north wall | plain | seen from the open ground at the quarter's edge |
| Tea lane north side | a three-segment fence only | no building frontage opposite E05; a low garden wall or stalls would enclose the lane |
| Sightlines from the bazaar's south entrance to B13's roof | not checked | |
| Paving tint | cooler in the browser than in Blender in shade | residual from batch 3 |
| P1.4 envelopes for B13, E04, E05 | not recomputed (placement is verified against the Blender-built nodes) | |

## 2. Technical backlog

| Item | Note |
|---|---|
| Lower-end device measurement | **none was available; nothing estimated** |
| Quantised vertex data: a 4-component padded layout | not tested; the 3-component one costs +1.3 to +2.9 ms here (05) |
| Decode-at-load in the game's loader | new game code; owner decision |
| Meshopt / Draco / KTX2 | no decoders in the vendored three; nothing installed |
| `InstancedMesh` for repeated whole buildings | analysed (≤ 10.7 % of placed triangles), not built |
| Distance LOD for roofs and props; lazy load per district | open for the town |
| Mouse-rotated camera round the new corners, gamepad, touch | untested |
| The character fade on the first island | untested; the fade remains provisional |

## 3. Risks

| Risk | Level | Note |
|---|---|---|
| **Performance on target hardware unknown** | **high** | one GPU, shared machine, ±10–15 % run to run |
| Town triangles | medium | 516k unique, worst measured view 575k (cells) / 613k (scene-wide) with 22 buildings + 2 surrogates; B15 and B16 (A11 and its mirror, 28k each) add about 56k unique |
| GLB size | medium | 40.8 MB raw, 13.2 MB gzipped (9.2 MB with quantisation and WebP) |
| E05 is a deviation (two floors) | low | one-line revert: base `A03c` → `A04b` in `HALL_VARIANTS` and the extras |
| Closed fences (slot, pocket) | low–medium | they stop the player from entering two pinch points; a player may find the fences arbitrary |
| Camera: lane canyon (2.8 m minima, roofs 10–12 m) | medium | measured, not judged; playtest case |
| Camera: E04 strongroom side and the path gate (1.1–1.8 m) | medium | measured; playtest case |
| The low-prop camera rule is preview-only and differs from the island's camera | low | switch `?lowprops=0`; the island's code is untouched |
| Fade at 0.15 in ring-walk stress tests | medium | provisional system |
| Human playtest not done | **high** | everything above is automated or scripted |
| Tea-green accent | low | owner's call |

## 4. Corrections made to earlier deliverables

* Batch 3 doc 03 labelled the 45 m row "new default" while the shipped default is 30 m: the two tables and a note in that file were corrected.
* The hall-camera test's screen-coverage fractions depended on the browser pane's aspect ratio (an earlier run showed 14–46 % where a fixed 16:9 viewport shows 0–1 %): fixed to 1280 x 720; no earlier batch's numbers were re-derived.
* `mergeByGroup` could not handle interleaved attributes (found by the quantised GLB); fixed.
* The `geoBytes` helper of the tests did not count interleaved buffers; fixed.
* A buried chimney on E04's strongroom wing (below the roof, invisible, 130 triangles) was found while writing 01 and removed; the GLB was re-exported and the results that depend on geometry (placement, scale) re-run; navigation, camera and performance results were measured on the kit before that change (no collision proxy and no visible geometry differ).
