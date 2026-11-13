# 08 — Remaining backlog, risks and limitations

## 1. Construction backlog

| Item | State |
|---|---|
| B15, B16 | **built** (this batch); 24 of 24 buildings are real |
| Ground, vegetation, sky | **stand-ins** (flat green plane, gradient sky, no trees); the whole next phase |
| Floating-island terrain, transport, NPCs, quests, combat, dragon flight | out of scope |
| Interiors | none; doors do not open; the hall's doors are now behind a rail |
| E04 north wall, B10/B12 west walls | plain when seen from open ground |
| Tea lane north side | fence only, no frontage opposite E05 |
| Repeated whole buildings (A04 ×3, A03/A04b/A10p/A10c) | visible from the aerial; variation by roof grade only |
| Paving tint in shade | still cooler in the browser than in Blender (preview lighting rig) |
| Leaf sign for E05 | redrawn; not confirmed by a human at 4–6 m |
| Exchange Hall dominance in the aerial | not dominant from height (t01); dominant at street level (t03, t08) |

## 2. Technical backlog

| Item | Note |
|---|---|
| **Frame-time measurement on a quiet machine and on lower-end hardware** | **not done**; this batch's timings are invalid (04) |
| Texture memory (~98 MB estimated with mips) | KTX2 / Basis not tested |
| Meshopt / Draco | not tested (no decoders in the vendored three) |
| Decode-at-load in the game's loader | new game code, owner decision; timing not re-measured for the 24-building kit |
| 4-component padded quantised layout | not tested |
| Distance LOD for roofs and props; lazy load per district | open |
| Mouse-rotated camera round corners, gamepad, touch | untested |
| Character fade on the first island | untested; the fade remains provisional |
| B10–B11 gap (0.75 m) and the B10/B12 canyon (camera 0.84 m in ring walks) | open; decision needed (03) |
| Tea veranda and east-court stress sequences (opacity 0.25 and 0.43) | open, not acceptable as a final state |
| Registry polish | `new_in_batch4` column name kept; dressing nodes modified in batch 5 keep their original status |

## 3. Risks

| Risk | Level | Note |
|---|---|---|
| **Performance on target hardware unknown** | **high** | one GPU, and this batch's timings are invalid |
| **Human playtest not done** | **high** | everything is scripted or automated |
| Town triangles | medium | 588 k unique, worst measured view 687 k submitted (unmerged aerial and scene-wide) |
| Texture memory | medium | ~98 MB with mips (an estimate) |
| GLB size | medium | 46.5 MB raw, 14.5 MB gzip (10.3 MB with quantisation and WebP) |
| Hall doors closed by the forecourt rail | low | reversible (01) |
| Camera canyons: west row, east court, tea veranda | medium | measured, not judged |
| Low-prop camera rule is preview-only and differs from the island's camera | low | `?lowprops=0` |
| Fade at 0.25–0.43 in stress sequences | medium | provisional system |
| Syntaxes of Play licence is a page statement | low | batch 3 capture stands |
| Tea-green accent | low | owner's call |
| Quantised kit: c04 close-up 35.7 dB | low | not the default |

## 4. Corrections made to earlier deliverables in this batch

* Batch 4's platform aggregation (7 runs, 0 passes) was an aggregation bug, now replaced by explicit criteria (03).
* A buried chimney on E04's wing was removed.
* The batch 4 `?town24=1` surrogate mode is now a no-op because B15/B16 are real; batch 4 numbers that included surrogates are not comparable one-to-one with this batch's.
* Batch 4's doc 05 says "40 % of primitives with tiling UVs: 221 of 551"; the final kit has 241 of 602 (same 40 %).
