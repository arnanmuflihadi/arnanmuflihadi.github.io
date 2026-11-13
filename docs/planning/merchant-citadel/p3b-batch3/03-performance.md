# 03 — Performance (measured)

Method as batch 2: 1280 x 720, DPR 1, shadows on, `render()` + 1x1 read-back, 20 warm-up + 120 timed frames, layers toggled. Load average about 5.6 (same as the Quaternius-stage run). Evidence: `evidence/validation/p3b3-perf.json`. Differences under about 1 ms are within the noise of this shared machine (repeated runs of the same case moved by up to 0.4 ms).

| Case | all on p50 / p95 (ms) | calls | triangles | batch 2 stage p50 |
|---|---|---|---|---|
| street: arrival court | 10.7 / 11.6 | 652 | 1056k | 9.5 |
| street: Exchange Hall forecourt | 8.0 / 9.1 | 303 | 545k | 6.9 |
| Caravan Green meadow | 6.8 / 7.9 | 262 | 538k | 6.0 |
| Counting Crag bench | 12.2 / 13.3 | 660 | 1315k | 11.7 |
| tea terraces promenade | 7.4 / 8.5 | 279 | 647k | 6.3 |
| aerial: whole island | 7.7 / 9.6 | 539 | 1011k | 7.2 |
| flight: south-west approach | 7.0 / 7.8 | 526 | 894k | 6.4 |
| flight: east approach | 7.9 / 9.9 | 539 | 1002k | 7.4 |
| town with vegetation (low aerial) | 9.3 / 10.1 | 618 | 1050k | 8.8 |

Rise of 0.5-1.4 ms in gameplay cameras (island GLB +23.7 k hero-mass triangles, ground-map sampling, fall layers, blobs, foliage shader). **Foliage A/B** (`?wind=0&ivar=0&grade=0` versus default, same session): Green 7.2 vs 7.2-7.4, tea promenade 6.7 vs 7.3-7.7, arrival 9.8 vs 10.5: the shader work costs 0-1.0 ms, **missing the 0.5 ms target** at the tea promenade and the arrival court. Draw calls: +8 at the arrival camera (fall layers, spray, clouds, blobs, hero masses). CPU: step 0.44 ms per frame, wildlife 0.22 ms (65 agents), flora re-bucket 0.08 ms. Memory: ground map 1.15 MB (2 textures), flora textures about 35 MB as before; renderer 227 textures / 517 geometries; island GLB 6.1 MB (was 3.2; flat-shaded hero masses duplicate vertices), flora GLB 10.9 MB unchanged. Not measured: low-end GPU, phone, thermal behaviour.

## After the crag + Cloudfall pass

Re-measured (`evidence/validation/p3b3b-perf.json`, load about 5): arrival court 10.9 / 11.7 ms, Exchange Hall forecourt 7.5, Caravan Green 7.2, **Counting Crag bench 12.5 / 13.7**, tea promenade 7.6, aerial 7.9, SW approach 7.0, east approach 8.6, low aerial 9.5 (p50 / p95 where given); triangles up to 1.45 M at the crag bench (was 1.32 M: +7.4 k outcrops, +scree and trees); calls 660 at the arrival camera; wildlife 0.18 ms per frame; island GLB 6.9 MB, flora data 100 kB. Differences of this size are within the noise of this shared machine.
