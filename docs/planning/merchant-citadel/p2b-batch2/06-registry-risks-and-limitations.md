# 06 — Registry, dependencies, risks and remaining limitations

## 1. Registry and configuration

* [asset-registry.csv](asset-registry.csv) / [.json](asset-registry.json): 36 kit nodes (status P2-A, P2-B batch 1, **P2-B batch 2**), triangles, vertices, primitives, materials, baked AO, sources and licence notes, collision groups.
* [asset-provenance.csv](asset-provenance.csv) / [.json](asset-provenance.json): 134 downloaded models resolved to source files and hashes; 14 custom items listed separately.
* [production-config.json](production-config.json): texture tiers, module LOD, AO bake and mix, metals, lighting, collision/camera rules (open-arcade roof shell, merchandise footprints, thin posts, fade), network rules, loader features and switches, loader to-do.
* [pedestrian-network-batch2.json](pedestrian-network-batch2.json) and CSVs.

## 2. Construction dependencies

| Dependency | State |
|---|---|
| Blender 5.2.3 LTS, extracted licensed packs in `.asset-inspection/merchant-citadel-p1/extracted` (git-ignored) | required to rebuild; not in the zip |
| Vendored three build (46 exports): ACES only, no post-processing, no render targets | worked around by per-material shader injection; unchanged |
| First-island controller, camera, character, collision | read-only imports; SHA-256 unchanged |
| Syntaxes of Play licence page copy | **owed** (24 models depend on it) |
| Remaining districts (D1, D4, D6, D7, E05) | not built; the district assignment (`district_at`) and per-district nodes are ready for them |
| Exchange Hall (batch 1) | untouched |

## 3. Risks

| Risk | Level | Note |
|---|---|---|
| **Lower-end device performance unknown** | **high** | single GPU, shared machine, ±30 % run-to-run; the slice with two halls is 7–13 ms per frame at 720p on an M4 Pro (merged / unmerged, shadows off/on); software rendering is ~1 s per frame. A target minimum spec and a measurement on it are needed before the town budget is fixed |
| Town triangle count | medium–high | 428k in the worst slice view with 14 of 24 buildings; extrapolation 700–800k vs the P1.4 projection 532k; needs the remaining P1.4 substitutions and cell merging |
| GLB size | medium | 27.0 MB raw, 9.1 MB gzipped, for the slice alone; the town would be about 2x. Quantisation and a lazy load per district are the remedies; not implemented |
| Licence evidence for the cafe pack | medium | CC0 stated on the creator's page only; a dated page copy must be kept |
| Fade not tested on the island; smoothing leaves 2–4 % of turn-in-place time with the character > 25 % of the screen at three squeezed spots | medium | preview-side only |
| East hall is a closed shop-hall, not P1.4's open arcade | low | deliberate, evidence in 01; one-line revert |
| Hall interiors are arcades only; doors do not open | low | no interiors in scope |
| Human playtest not done; autopilot only | medium | guided checklist in 07 |
| Merchandise density: the West hall's north end is sparse, merchandise zones depend on the SoP counters | low | content pass later |
| Merge groups per district are coarse for a town | medium | use ~30 m cells |
| Shared-machine timing noise | low | medians of 3 and paired runs reported |

## 4. Corrections made to earlier deliverables during this batch

Vertex-colour export (stall goods in P2-A and the closeout showed white), per-building signs (B07 showed B09's sign), fade flicker (opacity jumped 0.75 per frame), perf test hygiene (a stray second browser tab rendering the preview in the background slowed an earlier measurement run; found and closed, all numbers in 05 are from clean runs interleaved with the closeout replay).

## 5. Remaining visual and technical issues

See 03 section 5 (visual) and the limits above. Technical: stand-in ground and sky; no distance LOD; no mesh quantisation; `renderer.info` omits the shadow pass; software-renderer run not repeated for this kit; the closeout's absolute frame times were taken at a quieter moment than this batch's.

## 6. Not done (scope)

Remaining districts, the floating island, NPCs, quests, combat, dragon travel, first-island changes, any commit, merge or deploy.
