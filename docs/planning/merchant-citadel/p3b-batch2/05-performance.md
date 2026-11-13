# 05 — Performance (measured)

Method as batch 1: in-engine, 1280 x 720, DPR 1, shadows on, `render()` + 1x1 read-back so GPU completion is included, 20 warm-up + 120 timed frames per case, each case with layers switched on/off. Machine: this Mac (12 cores), browser pane, shared with other apps; load average about 5.6 during this run (the previous Gobkit run: 2.95, batch 1: 6.5). **This table was re-measured after the Quaternius animal swap** (the Gobkit table is in `evidence/superseded-gobkit/p3b2-perf.json`; evidence of this run: `evidence/validation-quaternius/p3b2q-perf.json`). Treat differences under about 1 ms as noise, and note the machine was busier than for the Gobkit run, so a part of the 0.3-1.4 ms rise is load, not animals (the crag bench went from 10.7 to 11.7 ms and its wildlife-hidden figure from 7.6 to 8.4 ms).

| Case | all on p50 / p95 (ms) | calls | triangles | flora hidden p50 | wildlife hidden p50 | town only p50 (triangles) |
|---|---|---|---|---|---|---|
| street: arrival court (gameplay camera) | 9.5 / 10 | 644 | 1035k | 8.6 | 8.3 | 6.4 (690k) |
| street: Exchange Hall forecourt | 6.9 / 7.6 | 294 | 523k | 5.9 | 5.5 | 4.3 (139k) |
| Caravan Green meadow (gameplay camera, animals around) | 6 / 7.4 | 255 | 517k | 5.5 | 5 | 3.3 (38k) |
| Counting Crag bench (gameplay camera) | 11.7 / 12.8 | 649 | 1291k | 8.3 | 8.4 | 6.1 (686k) |
| tea terraces promenade (gameplay camera) | 6.3 / 7.3 | 268 | 626k | 5.6 | 5.1 | 3.3 (22k) |
| aerial: whole island | 7.2 / 9.2 | 530 | 990k | 6.5 | 7.1 | 5.6 (690k) |
| flight: south-west approach | 6.4 / 7.4 | 517 | 873k | 6.2 | 6.5 | 5.6 (690k) |
| flight: east approach | 7.4 / 9.4 | 530 | 981k | 6.3 | 7.3 | 5.6 (690k) |
| town with vegetation (low aerial) | 8.8 / 9.4 | 610 | 1029k | 7.9 | 7.9 | 6 (690k) |

Worst case: the crag bench (11.7 ms, 1.3 M triangles). Wildlife adds about 0-1.2 ms (skinned-mesh draw calls, 59 visible agents; 0 where none are in view: flight and aerial cameras); flora adds about 0.2-3.4 ms.

## CPU, memory, load

| Item | Value |
|---|---|
| Whole simulation step per frame at the Green (character, camera, wildlife, flora re-bucket) | 0.34 ms |
| Wildlife update per frame | 0.188 ms: 65 agents, 36 simulated and 31 mixers updated that frame, 59 visible (distance LOD: full rate < 32 m, every 3rd frame < 70 m, every 8th beyond with mixers frozen, hidden > 130 m) |
| Flora re-bucketing | 0.046 ms each; 464 instances drawn (390 L0, 74 L1), 346k flora triangles in that view |
| Flora textures | 12 textures, about 35 MB GPU estimate; renderer holds 222 textures, 512 geometries |
| Load | island GLB 3.2 MB (12 ms), flora GLB 10.9 MB (50 ms), 13 Quaternius animal GLBs 2.3 MB + swallowtail 0.4 MB on disk (30 ms for the 14 species) |

## What the numbers do and do not say

* Skinned animals are cloned per agent (no GPU animation instancing). 65 agents is cheap here; hundreds would not be, and nothing here tests that.
* Culling: instanced flora is re-bucketed by distance, not by frustum (spatial cells are backlog); animals have `frustumCulled = false` on their skinned meshes and rely on the distance LOD.
* Not measured: a lower-end GPU or integrated graphics, a phone, memory beyond the texture estimate, flight views with a dragon, shadow cost beyond the town's frustum (trees outside it are unshadowed), sustained thermals.
* Batch 1 was timed at load 6.5 and this run at load 3: do not compare the two to the millisecond.
