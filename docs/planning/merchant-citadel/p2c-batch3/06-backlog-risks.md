# 06 — Remaining construction backlog, dependencies and risks

## 1. Backlog, in the order I would take it

| # | Item | What it needs | Notes |
|---|---|---|---|
| 1 | **E05** tea-route merchant house (D8) | A04b variant, one building | extends the east bazaar edge (B14, E06); smallest step, reuses the pipeline |
| 2 | **B13 warehouse, E04 counting house** (D7 Jalur Gudang, service court N33) | A07 (42k triangles) and A05 variants, court paving, the east lane (x 14-18) | an east counterpart of the artisan lane; node N33 and the E-side lane edges are already in the data |
| 3 | **B15, B16 terrace tower houses** (D4 Pelataran Bursa) | A11 / A11m variants on the civic terrace | belong with the Exchange Hall court; the terrace camera cases of P2-A apply |
| 4 | Ground, vegetation, sky | the preview still has a flat green plane and a gradient sky; the P1.4 vegetation (Quaternius Stylized Nature trees, bushes, ferns, rocks) is excluded from the slice | the paving edges and the lane's west side read unfinished until this exists |
| 5 | Lane's east side | the backs of B04-B06 are plain plaster; a fence, climbers or lamp brackets would complete the lane | small, uses existing modules |
| 6 | Interiors | doors are closed in every shop | not in scope so far |
| 7 | Mesh quantisation in the kit exporter; a GPU texture format | a quantising GLB writer and, for KTX2, the loader and transcoder in the vendored three build (a dependency decision) | see 03 |
| 8 | Town-scale rendering check | all 24 real buildings in 30 m cells, per-cell shadow plan, instancing for heavy repeated props | the five surrogates are a stand-in |
| 9 | A named minimum device and a measurement on it | hardware | still open |

## 2. Risks

| Risk | Level | Note |
|---|---|---|
| **No lower-end hardware measured** | **high** | one GPU, shared machine, differences under 1 ms are noise; the call/triangle columns are the only device-independent evidence |
| Triangle budget | medium | 24-building scene submits 606k triangles when all in view (439k average with 30 m cells) vs the 532k projection; depends on the five real buildings matching the surrogates |
| GLB size | medium | 33.4 MB raw / 11.0 MB gzipped for 19 buildings; quantisation estimated at -13 MB, not built |
| Texture memory | medium | about 95 MB estimated with mips; only GPU-compressed formats reduce it, and they need a loader decision |
| Workyard camera | low-medium | 1.07 m camera, character faded to 0.15 for 29 % of the approach; revisit when its north side is built |
| Wall-hugging play in the lane | low | ring walks at 0.12 m wall clearance fade the character for 29-52 % of the time; ordinary lane walking 0-4.6 % |
| Fade untested on the first island, and 14 % opacity not judged in real time | medium | preview-side only |
| Paving still cool in shade | low | reduced, measured, not eliminated; the lighting would have to change to remove it, which was not done |
| Syntaxes of Play | low | page copy now kept; the archive still has no licence file |
| Placement check for non-90° buildings (B10, B12, E01) is a bound | low | the node boxes match Blender to 0.01 cm; positions come from the same data |
| Human playtest not done | medium | checklist in 07 |

## 3. What this batch did not touch

The Exchange Hall, both market halls' structure, B14/E06/E07, the Bazaar's network and collision, the production controller/camera/character, the first island, terrain, NPCs, quests, combat, dragon travel. Nothing committed, merged or deployed.
