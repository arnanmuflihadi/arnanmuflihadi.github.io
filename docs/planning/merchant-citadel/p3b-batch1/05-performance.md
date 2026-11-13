# 05 — Performance (measured; not a pass/fail claim)

Method (`p3b-tests.js` `testPerf`): in-engine, 1280 × 720, DPR 1, shadows on (2048 map fitted to the town), render() timed on the CPU side and **to GPU completion** with a 1 × 1 read-back (vsync cannot hide it), 30 warm-up + 180 timed frames per case. Machine: this Mac (12 cores), browser pane, **shared with other applications (load average ≈ 6.5)**. Two full runs were made (this table is the second, on the final build; the first, on the previous build, gave 6.8–9.7 ms) and the same cases moved by up to ≈ 2 ms between runs, so read differences under 2 ms as noise. The batch 5 timings stay invalid and unused.

| Case | Frame to GPU complete p50 / p95 (ms) | Draw calls | Triangles submitted | With island hidden p50 (ms) / triangles |
|---|---|---|---|---|
| Street level, arrival court (gameplay camera) | 7.3 / 10.9 | 380 | 812 k | 6.6 / 539 k |
| Street level, Exchange Hall forecourt | 8.8 / 12.0 | 393 | 831 k | 7.3 / 614 k |
| Tea lookout (gameplay camera) | 7.7 / 9.2 | 116 | 312 k | 6.8 / 135 k |
| Aerial, whole island | 7.0 / 10.8 | 462 | 868 k | 6.9 / 690 k |
| Flight south-west (dragon approach) | 7.5 / 9.8 | 462 | 868 k | — |
| Flight east | 7.9 / 9.9 | 462 | 868 k | — |
| Side profile with underside | 7.1 / 9.2 | 462 | 868 k | — |

Shadows off (aerial): p50 7.4 ms against 7.0 ms with shadows: within noise.

## Island budget (counted)

Static: top 59.7 k, cliff + underside 30.4 k, stack 3.5 k, roots 0.8 k, debris 3.8 k, water 0.2 k, bridge 0.3 k = **98.7 k triangles** in 7 meshes. Instanced: 87 round trees, 36 tall trees, 77 palms, 185 shrubs, 48 rocks, 151 tea hedges, 40 props and 46 clouds ≈ **79 k submitted triangles** (island `stats()`). Textures: **0 added** (vertex colours and procedural shader detail); GLB 3.23 MB. Draw calls added: 143–150 depending on the view.

## What this does and does not show

* The island adds 0.1–1.5 ms (p50, one run) and up to **276 k submitted triangles** at the arrival court because the cliffs and the tea terraces are in the frustum. The aerial/flight cases draw the **whole** 588 k-triangle town plus the island (868 k) in ≈ 7–8 ms on this GPU: **no far LOD has been built and none was needed on this machine**; that says nothing about a lower-end device.
* Not measured: a lower-end GPU or integrated graphics, a phone, sustained thermal behaviour, memory, load time over a network, the dragon's own animation/cost, shadow cost with the island in the shadow frustum (the frustum still fits only the town; the island beyond it is unshadowed), 4K or DPR 2.
* The first-frame cost of the island's new shader programs is covered by the preview's prewarm.
