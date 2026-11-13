# 04 — Rendering and performance of the real 24-building scene

**Headline, stated plainly: the deterministic costs (draw calls, triangles, memory, file size, load) are measured and valid. The frame-time measurements of this batch are NOT valid for conclusions, and I make no claim about frames per second.** No lower-end hardware was available; nothing was estimated or simulated (no SwiftShader substitute).

## 1. What was measured, and on what

Scene: 24 real buildings, no surrogates, 66 instances, 54 kit nodes, shadows on/off, 1280 × 720, Apple M4 Pro, Claude desktop in-app Chromium 156, one machine. Method: 22 camera views (the batch 4 set plus the Civic Terrace views), 3 to 5 repetitions, 1×1 `readPixels` sync per view. Runs: `merge-cells-b5-24.json` (3 reps, all strategies), `-r2` (5 reps), `-B`, plus two replays of the **batch 4 scene** under today's conditions (`merge-cells-b5-replay-b4-A`, `-A2`).

## 2. Deterministic numbers (valid; they do not depend on load)

Mean over the 22 views, shadows off:

| Strategy | draw calls / view | submitted triangles / view | meshes | resident geometry | GL geometries |
|---|---|---|---|---|---|
| unmerged | 424.5 | 392,750 | 734 | 40.8 MB | 1,001 |
| district | 202.9 | 490,553 | 288 | 51.5 MB | 1,286 |
| 45 m cells | 213.5 | 508,625 | 285 | 51.5 MB | 1,568 |
| **30 m cells (default)** | 252.3 | 451,770 | 376 | 51.5 MB | 1,568 |
| 20 m cells | 329.3 | 413,644 | 532 | 51.7 MB | 2,097 |
| scene-wide (diagnostic) | 118.5 | 672,678 | 102 | 51.5 MB | 2,196 |

Per camera (calls / submitted triangles), showing that culling depends on the view, not on one aerial:

| View | unmerged | 30 m cells | scene-wide |
|---|---|---|---|
| t01 town aerial | 800 / 687k | 429 / 687k | 141 / 687k |
| t02 southern arrival | 725 / 650k | 388 / 664k | 139 / 685k |
| p3 bazaar aerial | 542 / 483k | 305 / 601k | 123 / 682k |
| p3 aisle at eye height | 339 / 368k | 220 / 417k | 114 / 676k |
| t07 tea route | 116 / 112k | 108 / 153k | 108 / 656k |
| t08 civic terrace | 132 / 155k | 107 / 218k | 100 / 666k |
| t09 hall approach | 105 / 103k | 81 / 137k | 89 / 639k |
| c01 terrace aerial | 412 / 412k | 233 / 440k | 115 / 676k |
| c02 assay office | 99 / 105k | 98 / 200k | 92 / 646k |
| p5 court from lane | 87 / 106k | 101 / 193k | 90 / 653k |

Reading: unmerged culling is best for triangles in street-level views (103–155 k at the terrace) but costs 100–800 calls; scene-wide merging fixes calls near 100–140 but submits 640–690 k triangles in **every** view, including the closest; 30 m cells sit between (81–429 calls, 137–688 k). Worst unmerged view 800 calls and 687,384 triangles (aerial). Unique triangles in the kit 588,064; placed triangles in the 24 buildings 547,307.

Memory and load: 40.8 MB of geometry unmerged (51.5 MB with merged copies), 79 textures ≈ 98 MB GPU with mips (estimate from sizes, not a GPU readout), 98 materials, 74–76 programs, GLB 46.5 MB raw / 14.5 MB gzip, parse and build 280–390 ms and shader prewarm 660–700 ms in these runs (also affected by load). Heap 177–344 MB in the three runs (varies with what else the page held).

Compared with batch 4's 22 buildings + 2 surrogates: GLB 40.8 → 46.5 MB (+13.9 %), unique triangles 516,528 → 588,064 (+13.8 %), worst aerial 575 k (cells) → 687 k (unmerged), consistent with the +56–70 k of B15/B16 and with batch 4 counting surrogates only for the 24-building estimate.

## 3. Frame times: why they are not valid

| Observation | Value |
|---|---|
| Same configuration (unmerged, shadows off), median synced frame time across repetitions | between **5.6 ms and 26.4 ms** within one run (`range` in `merge-cells-b5-24-r2.json`) |
| Medians for one configuration in three runs | 18.0 / 21.2 / 21.8 ms (unmerged), 16.4 / 14.8 / 14.1 ms (30 m cells), 10.5 / 9.7 / 10.1 ms (scene-wide) |
| Replay of the **batch 4 scene**, which batch 4 measured at 8.05–8.79 ms unmerged | 6.9–17.5 ms |
| Machine at the time | iCloudDriveCore syncing the worktree at up to ~97 % CPU, ChatGPT Codex helpers at 30–50 %, a Virtualization process, WindowServer 65 %, load average 4.8–8 |
| Odd results | unmerged with shadows (9.7) faster than without (18.0) in one run |

Because the replay of the old scene shows the same scatter, the spread comes from the machine and not from the new buildings. **I did not repeat the run on a quiet machine** (it was still loaded when I last checked). The numbers are kept in `evidence/` for completeness and must not be quoted as performance. The last frame times I would call valid are batch 4's (22 buildings, shadows off: 8.05–8.79 ms unmerged, 7.31–7.56 ms in 30 m cells; `p2d-batch4/05-optimisation-assessment.md`), and the 24-building scene has 13.8 % more unique triangles, which does not by itself say what the frame time is.

What the noisy data can still say, as direction only: per-view GPU readback times (the `mean_view_ms` column) stayed between about 4.8 and 10.5 ms for every strategy; shadows added roughly 1–3 ms per view in the pairs of the first run; no strategy was stably better, which agrees with batch 4's finding that district, cells and unmerged are within the run-to-run spread of one another on this GPU.

## 4. Recommendation

Keep 30 m cells as the default (calls drop to ~60 % of unmerged without the every-view triangle cost of scene-wide merging); keep the unmerged mode as the baseline. **Required before any claim:** repeat `?autotest=mergecells&modes=none,district,cell30,scene&reps=5` on a quiet machine, and on at least one lower-end device (an integrated-GPU laptop, a phone) to find out whether 588 k unique triangles and ~98 MB of textures are affordable. Texture memory (KTX2) and distance LOD for roofs and props are the likely levers if they are not.

## 5. Still not measured

Other GPUs and browsers, battery and thermal state, long-session memory growth, first-load time over a real network, the effect of the stand-in ground and sky being replaced by real terrain and vegetation.
