# 05 — Terrain construction strategy, requirements, risks and the P3-B handoff

Everything here is a proposal for P3-B. **No production terrain exists and none was built.** Numbers marked *estimate* are not measurements.

## 1. Construction strategy (preliminary)

1. **One authoritative height function.** Keep the shape file's approach: the top surface is an analytic function of plan position (flat pad, hall shelf, crag benches, tea benches, quay), not a hand-sculpt. Export it once as a height grid for the game (section 3) and build the visible mesh from the same grid. The town pad (x −34…44, n −20…73.2) and the shelf are exact constants, so buildings and paving cannot drift.
2. **Top mesh.** A regular grid (not the massing's polar fan, which produces the sawtooth risers visible in `v5b`): about 2 m cells in open ground, 1 m along paths, bench risers and the pad boundary, cut to the rim outline. *Estimate:* 12–20 k triangles.
3. **Cliffs.** A band 23 m high and 678 m long. Build from 4–6 reusable rock-strata modules (ledge, recess, buttress, notch corner) with a tiling banded-rock material, plus 3 hero pieces (Cloudfall notch, quay prow, crag face). *Estimate:* 15–25 k triangles.
4. **Underside.** Seen only from the air and from other islands: one low-detail keel mesh with baked vertex colour, 30–40 hanging roots as instances of 3 meshes. *Estimate:* 6–10 k triangles.
5. **Tea Stack, bridge, pavilion, quay stair, beacon, retaining walls, rails.** Small authored pieces; the pavilion, rails, stair and walls can reuse registered Quaternius modules (to be checked against the asset inventory first).
6. **Vegetation.** 80–150 trees from 3–4 meshes as `InstancedMesh`, shrubs and tea rows as instanced strips, grass by material only (no blades) in the first pass. *Estimate:* 20–40 k submitted triangles.
7. **Water.** One stream ribbon and one waterfall sheet with a scrolling unlit material; a mist card at the lip. No reflections, no refraction in the first pass.
8. **Sky.** A cloud deck below the island (cards or a few instanced shapes); the first island as a distant silhouette if both are ever shown together (owner decision).
9. **Order of work.** Height grid and collision first (grey terrain, playable) → cliffs and underside → hall shelf and quay stair (fixes C4) → vegetation and water → dressing of quay and green.

## 2. Assets and materials required

| Need | Source to check first | Note |
|---|---|---|
| Banded rock (cream / ochre / red), dark keel rock | none in the kit; a tiling material must be authored or sourced CC0 | the island's signature; 2 materials |
| Grass, meadow, packed-earth trail, tea soil | first island's terrain materials if the owner allows reuse; otherwise authored flat colour with vertex-colour variation | 4 materials, no new textures needed for a first pass |
| Trees (broadleaf, conifer), shrubs, tea bush | registered packs (`ASSET_MANIFEST.md`, Quaternius) before anything new | **asset-first check not yet done for vegetation** |
| Rails, stairs, retaining walls, pavilion parts | Quaternius Medieval Village modules already in the kit | reuse |
| Quay dressing (crane, cargo, bollards) | `CUS-Hoist` and the existing goods | reuse |
| Water, mist | authored material | — |

No asset was searched for, downloaded, purchased or generated in this phase. AI asset generation is not proposed.

## 3. Collision and camera interface requirements

Facts read from the code: the controller takes `heightAt(x, z)`, `collision {blocked, slide}`, `bounds`, `minY`/`maxY`, `recoveryPoint` and `isSafe`; the camera's `clearDistance` also uses `heightAt`. The preview's height field is **uint8 centimetres over x −36…50, n −12…100**, so it can only hold 0…2.55 m.

| Requirement | Why |
|---|---|
| New support grid: signed 16-bit centimetres (or float32), covering at least x −90…125, n −85…140, 0.5 m cells for terrain plus the existing 0.2 m grid kept for the paved town and stairs | the island spans −8.7…+23.7 m and 178 × 216 m; uint8 cannot hold negative or tall values |
| `bounds` ≥ 145 (the preview uses 130; the rim reaches n 136) or a rim-shaped bound | the square bound would cut the crag |
| `isSafe(x, z)`: inside the rim by ≥ 1.5 m and not on a bench riser or cliff; `recoveryPoint` per district | falling off the island must return the player to a sensible place; today `isSafe` is always true in the preview |
| `minY` below the lowest walkable level (−9 m) with a fall-recovery threshold, e.g. −30 m | benches and quay are below 0 |
| Rim, bench-end and quay-edge rails as body proxies; bench risers (1.7 m) need no proxy (too high to step, and falls down a riser are safe) | edge safety |
| Camera: terrain participates through `heightAt`; add camera-transparent rule A (02) to the proxy data; test the crag stair foot, the bank behind the tea house and the promenade | new tight spots are expected |
| Stack bridge: narrow walkway with rails; decide fall behaviour | only optional route with a real fall |
| Terrain under buildings stays at −0.02 m (pad) and the hall shelf at 1.9 m under the podium deck | avoids z-fighting with paving (0.01) and the deck (2.01) |

## 4. Performance and optimisation risks

**There is no valid frame-time baseline.** Batch 5's timings were taken on a loaded machine and must not be used; nothing was measured in this phase (it produced no browser content). The town alone is 588,064 unique triangles, up to 687 k submitted in an aerial view, and about 98 MB of textures (estimate).

| Risk | Why it matters here | Mitigation to design in |
|---|---|---|
| **Dragon-flight and distant views draw everything** | from the air the whole town (687 k) plus the island is in the frustum; cell merging does not help | a far LOD of the town (merged, decimated roofs-and-walls shell or an impostor) swapped by distance; measure before choosing |
| Terrain + cliffs + underside | *estimate* 35–55 k triangles: under 10 % of the town | grid LOD for the top is unnecessary at this size; keep the underside separate so it can be culled from street level |
| Vegetation | instancing keeps calls low, but 150 trees × shadows is real cost | 3–4 meshes, 150–300 triangles each, no shadows beyond ~60 m, tea rows as strips |
| Shadows | the shadowed area grows from the town's extent to an island twice as long, at the same shadow-map size | fit the cascade to the player's surroundings; the underside and far cliffs receive no shadow |
| Water | transparency and overdraw at the Cloudfall | unlit scrolling material, one sheet, mist as one card |
| Draw distance and fog | an island in open sky has no natural far clip | height-and-distance haze toward the cloud deck (also sells scale) |
| Texture memory | two more tiling rock materials on top of ~98 MB | 1024² maximum, shared across cliffs and underside |
| Collision grid memory | 430 × 450 int16 cells ≈ 0.4 MB | negligible |

**Tests required before integration:** (1) a valid frame-time run of the 24-building town on a quiet machine; (2) the same with grey terrain, at street level and from two flight cameras (`v6`, `v6b` positions); (3) one lower-end device; (4) the far-LOD decision measured, not assumed.

## 5. P3-B handoff (what to build, in order, with acceptance checks)

| Step | Build | Done when |
|---|---|---|
| B0 | Apply C1–C3 and C5 of doc 02 (if approved) | spins at the hall door, B10 eave and lane corners ≥ 2.7 m; doors reachable; gap closed |
| B1 | Height grid + collision + safe-ground predicate from `p3a_island_shape.py` (key `S`), grey top mesh, in the isolated preview | every existing network edge still passes (65/65); the player walks quay → stair → gateway, court → benches → lookout, hall → crag summit, and cannot leave the island; fall recovery works |
| B2 | Hall shelf, quay stair, retaining banks | podium east/west/north drops gone (02's walk tests end at y ≥ 1.9); stair risers ≤ 0.42 m |
| B3 | Cliffs, underside, Tea Stack, roots | silhouette matches `v1`, `v2`, `v6` cameras in the browser; counts reported |
| B4 | Vegetation, stream, Cloudfall, tea rows | matched Blender / browser views for the eight `v*` cameras; landing discs still clear |
| B5 | Rails, quay and green dressing, trails | camera spins at the listed tight spots; edge walk tests |
| B6 | Measurement | the four tests of section 4; human playtest checklist |

Inputs for P3-B: `blender/p3a_island_shape.py` (the design as code: outline, height function, benches, features, landing discs, trails), `blender/p3a_island_blender.py` (massing and the camera set), `blender/p3a_plan.py`, `evidence/island-measurements.json`, `p2e-batch5/terrain-interface.json`. The massing .blend with the town (102 MB) is in the ignored workspace `.asset-inspection/merchant-citadel-p1/p3a/final/` and can be regenerated with one command (README).

## 6. Open decisions for the owner

1. Concept choice (S recommended; A or B remain available as code).
2. Corrections C1–C5.
3. Size: 178 × 216 m is what the composition asked for; a 15 % smaller version is possible by shortening the quay and the green.
4. The Tea Stack bridge: build it as optional exploration, or keep the stack unreachable scenery.
5. Bank or retaining wall 1 m behind B15, B16 and the tea house.
6. Whether terrain materials and trees may be reused from the first island's library.
