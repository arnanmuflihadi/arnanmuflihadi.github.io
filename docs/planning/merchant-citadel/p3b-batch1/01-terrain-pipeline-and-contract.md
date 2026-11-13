# 01 — Terrain pipeline, heightfield contract and bounds

## Inspection result (what was reused, what was not)

| Component | Finding | Decision |
|---|---|---|
| `player-controller.js`, `camera.js`, `character.js`, `input.js`, vendored three | take `heightAt`, `collision {blocked, slide}`, `bounds`, `minY/maxY`, `recoveryPoint`, `isSafe` as options | **reused unchanged** (SHA-256 of all six production files verified OK) |
| `floating-atlas/collision.js` `blocked()` | hard limit `|x| > 105 or |z| > 105` → returns blocked | **cannot hold the island** (rim to n 136, stack to x 122.6): the preview passes its own collision object with the same obstacle rule and a terrain mask instead of the box. The game module is not edited |
| Controller `bounds` | one symmetric number | derived from all geometry: ceil(136.25) + 10 = **147 m** (P2-B preview used 130 < rim n 136) |
| Preview heightfield | uint8 cm, 0–2.55 m, x −36…50, n −12…100 | kept as the **town layer** (0.2 m, authored paving/steps/terrace/podium); combined with the island grid by `max` where the town authored a surface |
| Dragon free flight | not in this branch (`travelConfig.implemented = false`; only `skyport-boarding.js` loads `dragon.glb`) | interface requirements documented, terrain tested independently (04) |
| Spatial-cell merging | merges the 24-building town only | unchanged; the island is **not** merged (instanced + 7 static meshes) |

## One authoritative definition

`source/p3b_model.py` (numpy only) is the only place that says what the island is: two rim outlines, the height function (pad, hall shelf, crag benches, tea contours, quay, clearings, graded paths, stream bed, rim lip), the optional bridge, vegetation rules. Everything below is generated from it:

```
p3b_model.py ─┬─ p3b_export_runtime.py ─ island-terrain.json/.bin, island-mask.bin   (walkable support, bounds)
              ├─ p3b_geo.py + p3b_props.py ─ p3b_blender_build.py ─ merchant-citadel-p3b-island.glb, island-instances.json
              └─ p3b_blender_render.py ─ Blender reference views (imports the exported GLB, never the model directly)
```
Rebuild everything: `bash docs/planning/merchant-citadel/p3b-batch1/source/build_all.sh` (≈ 3 min, mostly vegetation placement).

## Runtime formats

| File | Content |
|---|---|
| `data/island-terrain.json` | grid spec (x −90.0 … 131.0, n −89.0 … 144.5, cell 0.5, 443 × 468), `nosup` sentinel, extents, derived bounds, slope limits, bridge |
| `data/island-terrain.bin` | **int16 centimetres**, 414,648 B (−32768 = no support); covers −8.7 … +23.6 m with 1 cm precision (the old uint8 format could not hold either) |
| `data/island-mask.bin` | uint8: bit0 walkable (supported, ≥ 1.2 m inside the rim, slope ≤ 0.9, or bridge deck within its own slope), bit1 comfortable (slope ≤ 0.6, ≥ 2.5 m inside; used by `isSafe`), bit2 authored by the town grid |
| `models/merchant-citadel-p3b-island.glb` | 3.23 MB; 98.7 k static triangles + 16 instanced prototypes; vertex colours (linear) + a `_matid` attribute per vertex |
| `data/island-instances.json` | 584 trees, shrubs, rocks and tea hedges, 40 quay and landscape props, collision proxies, paths, clearings, water, fall |

Interpolation: bilinear on the 0.5 m grid; a cell with a missing corner uses the mean of its valid corners; heights over town paving are `max(island, town grid)`. Lookup cost on a mixed sample: ~0.02 µs per call (400 k calls in 7.9 ms; part of the sample is outside the grid, so treat as an upper bound on speed).

## Authoritative bounds (all geometry, detached stack included)

| | x (m) | n (m) |
|---|---|---|
| Main landmass | −81.6 … 97.3 (178.9) | −80.6 … 136.2 (216.9) |
| Tea Stack | 100.3 … 122.6 | 32.8 … 56.0 |
| **Complete** | **−81.6 … 122.6 (204.2)** | −80.6 … 136.2 |

Supported area 26,214 m²; walkable 23,840 m²; comfortable 22,046 m²; rim 690 + 82 m. The grid adds an 8 m margin; the controller bound is 147 m; `maxY` 80, `minY` −30 (lowest walkable ground is −8.7 m, the quay −3.0 m). Camera `far` is 2500 m in the preview.

## Does the rendered ground equal the physical ground?

The visible top mesh (constrained Delaunay, adaptive 2 / 1 / 0.5 m, 59.7 k triangles) was compared with the bilinear physical surface at 30,641 random walkable points (`evidence/terrain-export-stats.json`): **mean 3.2 mm, median 0.7 mm, p95 1.4 cm, p99 3.2 cm, max 0.85 m; 0.05 % of points differ by more than 20 cm**. The maximum is at the hidden vertical step under the Exchange Hall podium (terrain 0 → 1.9 m inside 0.6 m beneath the stairs; the stairs and deck are authored by the town grid). Continuity of the grid: no seam (largest change over 1 cm is 4.2 cm at the steepest walls).

## Deviations from P3-A, with reasons

* **Quay stair → graded ramp** (14 m wide, 0.25 slope, −3.0 → 0 m, n −24 … −36): a 0.3 m stair cannot be both a 1 m-resolution mesh and a heightfield without a mismatch; the ramp is physically and visually the same object. Stair detailing is backlog.
* Shelf bank starts 1.1 m north of B15/B16 and 0.9 m north of the tea house (unchanged from P3-A; batch 5 asked 6 m). It is a 2 m bank, walkable, with the camera tested at its foot (2.79 m).
* The cliff/underside shell is built from the rim polyline (690 points), not the P3-A polar fan; the top is a triangulation, so no sawtooth risers.
