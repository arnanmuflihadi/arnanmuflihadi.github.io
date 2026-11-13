# Construction dependencies, risks and the human approval checkpoint

## 1. Dependencies

```
owner approval of the corrected slice ─┬─► P2-B batch 1 (hall + court, built here)  ─► approval
                                       └─► decisions (below) ─► batch 2 (D3 Pasar Awan) ─► later districts
lower-end performance measurement ─────────► whole-town budgets fixed ─► any batch beyond 2
loader: material cache + shader pre-warm ──► batch 2 (stutter, 86 → ~60 materials)
AO bake strength decision (0.6 suggested) ─► kit re-export (≈ 4 min, scripted) ─► visual re-check
cafe-pack + Avramania goods re-link/atlas ─► A02 market halls (CONDITIONAL in P1.4)
real-hardware camera/fade review ──────────► any move of the fade toward the first island
```

| Dependency | Status |
|---|---|
| Blender 5.2.3 LTS, the extracted licensed packs in `.asset-inspection/merchant-citadel-p1/extracted` | available (git-ignored workspace; rebuild needs it) |
| Vendored three build (46 exports): no post-processing, ACES only | unchanged; worked around with per-material shader injection |
| First-island controller/camera/character/collision modules | read-only, hashes unchanged |
| Terrain/support contract for the floating island (P1.4 doc 11) | not touched; island not built |
| Quaternius MegaKits (CC0), Syntaxes of Play cafe (CC0 on page only), Avramania (CC0, AI-built packs rejected) | licence register in P1/P1.2; the cafe-pack condition remains for batch 2 |

## 2. Risks (updated from P2-A)

| Risk | Level | Change since P2-A | Mitigation / owner |
|---|---|---|---|
| Frame cost on low-end hardware unknown | **high** | still unmeasured; the slice is cheap on an M4 Pro (3.0–5.9 ms at 720p, 12.6 ms at 4K) and unusable in software (~1 s) | measure on the target minimum device before fixing the town budget |
| Whole-town triangle count | medium | slice with hall now 308k drawn (418k before module LOD); P1.4 full-town projection 532k; the two LOD substitutions already took −31 % of kit triangles | per-district merge; further P1.4 substitutions (window boxes, doors, crates, barrels) only if measured |
| Performance reporting methodology | fixed | P2-A timings under-reported ~5x (finish()) | read-back sync in all tests; P2-A files labelled |
| Lighting fidelity | **reduced** | mirrored sun found and fixed; MAE 9 vs 23–26; AO and Neutral in | owner judges the images; AO strength tuning (0.6 bake) |
| AO is soft on large faces and heavy in the bake | low | new | bake at 0.6 and mix higher; or subdivide key facades |
| Character fade is a preview feature | medium | new | review in motion; implement as a switchable camera-distance rule if adopted; never tested on the island |
| Hall interior and doors | low | decorative doors | an interior would be a new phase |
| Narrow spots (tea-house veranda gap 1.49 m, 0.30 m side clearance) | low | corrected, tight by design | keep the rule: no new narrowing; widen by dropping one post if the owner wants |
| Conditional assets (cafe pack, Avramania goods) for batch 2 | medium | unchanged | atlas and re-link in batch 2 with licence rows |
| Material count/stutter | medium | 86 objects for ~60 names; 225–280 ms first-frame compile | loader cache and shader pre-warm |
| Tests are simulated, no human playtest | medium | unchanged | 10-minute human walk (checklist below) |
| Final-kit verification | low | After the module LOD the scale, routes (23 x 8 camera modes), network (34 edges), camera cases, camera cause, platform, camera shots and performance tests were all re-run on the final kit (`evidence/`) | none |
| Source `.blend` files (85/95 MB, third-party textures) are outside the zip | low | unchanged | they are in `.asset-inspection/…/p2a/` |
| Concurrent work in this workspace | low | nothing committed; only two new untracked folders | owner commits/tags when ready |

## 3. Human visual approval checkpoint

**Preview:** `node merchant-citadel-p2a/server.mjs --port 4180`, then open `http://127.0.0.1:4180/merchant-citadel-p2a/index.html`. WASD/arrows move, Shift runs, Space jumps, Q/R turn the camera. Buttons teleport to arrival, junction corner, awning rows, terrace steps, inn balcony, tea house. Flags: `?fade=0` (no character fade), `?postsblock=1` (P2-A camera behaviour), `?ao=0` (no baked AO), `?tm=aces` (P2-A tone mapping), `?shadows=0`, `?sun=` `?env=` `?exp=`.

**Please look at, in this order:**
1. The walk from arrival up the market street to the Exchange Hall steps (the corrected spine, the cross, the awning rows, the hall appearing at the end of the street).
2. The Exchange Hall from the court, the porch, the tower, and from the aerial view; compare with `visuals/comparison/cmp-view-d-exchange-court.jpg` and `cmp-p2b-hall-*.jpg`.
3. The west cross street between the turret house (B04) and the bakery (B05); the market cross and the passage either side.
4. The tea house: walk N16 → veranda gap and back; stand on the veranda and turn the camera (character fade).
5. Before/after sheets in `visuals/before-after/`.

**Decisions requested:**
| # | Decision | Recommendation |
|---|---|---|
| 1 | Approve the corrected P2-A slice (circulation, camera rules, lighting) as the baseline for P2-B? | yes, if the images read as the P1.4 concept |
| 2 | Approve the Exchange Hall (batch 1) as built? | yes / or list artistic corrections |
| 3 | Accept the character fade as the camera-compression solution (preview-side)? | yes for the preview; not for the island without review |
| 4 | Authorise batch 2 = D3 Pasar Awan completion (B02, B03, B14, E06, E07)? | after 5 and the measurement below |
| 5 | A lower-end device / minimum spec to measure on before the town budget is fixed | needed |
| 6 | AO: keep 0.45 mix on a 0.9 bake, or re-bake at 0.6 and retune? | re-bake in batch 2 |

**Not approved by anything in this package:** the whole town, other districts, the floating island, NPCs/quests, any commit, merge or deploy. Technical validation (tests, numbers) is not artistic approval.
