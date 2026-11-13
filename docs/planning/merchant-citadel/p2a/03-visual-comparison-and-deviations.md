# P2-A visual comparison and deviations from P1.4

> **Correction (2026-11-12, P2-A closeout):** the lighting gap described in section 2 as structural (no AO, ACES vs Neutral) was mostly a **mirrored sun direction** in the preview; corrected and re-measured in [closeout/04-lighting-and-materials.md](closeout/04-lighting-and-materials.md).


**Status of the judgement:** the comparison below is a provisional internal observation by the executor. It is not owner approval of the artistic result.

## 1. What was compared

Ten cameras defined in `scene.json`: five P1.4 views that fall inside the slice (B, B2, C2, F, G) and five new slice cameras (aerial, junction, inn, terrace, tea house).
Left: the P1.4-style Blender render of the **same assembled slice** (Eevee, ambient occlusion, Khronos Neutral view transform, `renders/` in `visuals/blender/`).
Right: the preview page at the same position, look-at and vertical FOV (`visuals/browser/`), with the game's real explorer instead of the cyan stand-in capsule.
Side-by-side sheets: [`visuals/comparison/`](visuals/comparison). Mean-luma pairs (Blender / browser): aerial 126/135, inn 134/154, junction 135/139, tea 162/175, terrace 161/164, B 102/114, B2 116/123, C2 159/173, F 160/175, G 149/164.

Key sheets: [junction](visuals/comparison/cmp-p2a-junction.jpg) · [inn](visuals/comparison/cmp-p2a-inn.jpg) · [terrace](visuals/comparison/cmp-p2a-terrace.jpg) · [market street B](visuals/comparison/cmp-view-b-merchant-street.jpg) · [bazaar C2](visuals/comparison/cmp-view-c2-bazaar-eye.jpg) · [aerial](visuals/comparison/cmp-p2a-aerial.jpg).
In-game follow-camera view: [live follow camera](visuals/browser/shot-live-follow-camera-street.jpg).

## 2. Verdict

Geometry, scale, placement, materials and palette match: the same buildings stand in the same places at the same size (0.5 cm placement error), roof tile, plaster, timber, stone and cloth read as the Blender versions,
signs, lanterns, bunting and the striped awnings carry over. In my judgement the slice is **not materially worse in architecture or material language** than the concept. It is **somewhat worse in lighting finish**:

| Difference | Browser vs Blender | Cause | Corrected? |
|---|---|---|---|
| No ambient occlusion: contact darkening under eaves, at wall bases, inside the porch is absent; the browser reads flatter and 3–20 luma points brighter | visible in every view | the vendored three build has no post-processing/SSAO (`three-atlas.module.js`, 46 exports) and adding it is a new dependency | **No.** Mitigation: a lower sun (2.2) and exposure (0.7) lowered the average error; baked vertex AO in the kit is a P2-B option |
| Tone mapping: ACES vs Khronos Neutral | browser slightly more contrasty/desaturated highlights; sky paler | only ACES exists in the vendored build | No. Colour error is small; documented |
| Sky and ground are stand-ins | pale equirect sky, green plane; the Blender haze/sky is bluer | out of slice scope | Ground lightened (0x7d9660) after the first capture was far too dark (luma 89 vs 126) |
| Burgundy banner on the terrace flagpoles rendered **white** | found in the comparison | export bug: `bypass()` rewired only a Mix node's float output, so the baked burgundy texture was disconnected | **Fixed** in `p2a_kit_export.py`, GLB re-exported, banners verified burgundy |
| Black lanterns / grey-black cafe counters | first browser capture | metals without an environment, and cafe-pack metallic maps that glTF cannot carry | **Fixed**: equirect environment lighting; metal/roughness constants for non-ORM materials (documented in 04) |
| Paving seal looks lighter and pinker | B, C2 | lighter ground bounce / no AO | Not corrected, cosmetic |
| Cloth under direct sun looks slightly flatter | terrace awnings | no AO / sheen | Not corrected |

A lighting grid search (sun x environment x exposure over five views, mean absolute luma and warmth error against the Blender renders) bottomed out at ≈ 23.5 luma points of mean absolute error regardless of settings, which is the structural AO/tone-mapping gap, not a settings problem.
Chosen: sun 2.2, environment 1.1, exposure 0.7 (bias +9.7 luma). The saved result of the first, narrower grid is `evidence/autotest-calibrate.json`; the wider grid was run interactively and its numbers are quoted here from the session log, not stored as a file.

## 3. Deviations from P1.4 and their causes

| # | Deviation | Cause / reason | Effect |
|---|---|---|---|
| D1 | Slice contains 8 of 24 buildings (B04–B09, E03, B17), 4 stall rows, the market cross, the terrace and podium stairs, 2 arches, 674 paving tiles, 87 dressing pieces | the brief's one segment + corner + inn + tea house + hall approach | scope only |
| D2 | **Exchange Hall is a grey stand-in box (26 x 7 x 8 m + 4 m tower)** | hall construction is P2-B; the stair test needed a destination | visible in every view toward the north; the camera runs inside it when descending |
| D3 | Textures re-encoded: tier 1 base 1024 / ORM 512 / normal 512, tier 2 half | 828 MB → 92 MB; GLB 15.2 MB | no visible loss found; normal-map softness not isolated |
| D4 | Colour grade and cloth tints **baked into base textures** (Hue/Sat and multiply nodes) | glTF has no Hue/Sat node | identical colour; variants cost an extra texture each |
| D5 | Non-Quaternius metal/specular maps replaced by constants (metallic 0.5 for listed metals, else 0; roughness floor 0.6 when < 0.2) | glTF has one metallic-roughness texture; cafe-pack specular maps were read as metal and rendered black | lanterns and counters visible; less sparkle than Blender |
| D6 | One UV set and one colour attribute per mesh; vertex-colour multiply kept as COLOR_0 | UV1/UV2 and duplicate colour layers were 60 % of the file | none visible |
| D7 | Lighting: sun + equirect IBL + ACES; no AO, no SSAO | vendored build limits (see section 2) | flatter finish |
| D8 | Character is the game's real explorer (1.9 m), not the P1.4 capsule | brief: use the actual controller | none |
| D9 | Camera collision: **cloth awnings, signs and pennants are not obstacles**; roofs are stepped bands; jetties/balconies/overhangs/arches are camera-only boxes | measured in 01 | camera may pass through cloth |
| D10 | Proposed plan edits from the tests: N17 → (36.16, 62.30); B04–B05 alley 1.34 m to be closed or ≥ 2.0 m; spine route bypasses the market cross | 01 | not applied to P1.4 files; owner decision |
| D11 | Walkable height field is **sampled from the real stair geometry** (0.2 m cells, uint8 cm) rather than analytic planes | needed so the controller's step logic is tested on real treads | max riser 0.22 m |

## 4. Custom vs downloaded geometry

Downloaded, CC0, verified in P1.2 and reused unchanged in shape: the Quaternius MegaKit modules (`MV-*` walls, roofs, stairs, floors, balconies, props) and the dressing props listed in `../p1.4/03-asset-inventory-update.md`
(licences and hashes in `../p1/03`, `../p1/04`). Custom (authored for this project, not downloaded): `CUS-Awning_*`, `CUS-Bunting_*`, `CUS-PavingSeal`, `CUS-Seal_NiagaAwan`, the hanging `CUS-Sign_*` boards and the guild cross emblem (flat-colour materials `CUS_*`).
No asset in this slice comes from the first island, and no AI generation was used.
