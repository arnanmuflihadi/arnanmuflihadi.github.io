# 02 — Selective Central Bazaar polish and the paving colour

Scope kept narrow: the Western Hall's interior and the browser's paving colour. No structure of either hall, no shop, no network edge of the Bazaar was changed.

## 1. Western Hall (`A02p`)

Finding (batch 2, confirmed on the interior view): the north gable was a blank cream triangle, the aisle ends were dim and the roof underside a large plain brown surface; the hall read as sparse although its goods are correct.

Added, using verified models only (no new third-party model):

| Addition | Source | Why |
|---|---|---|
| Guild seal on the **inside** of both gables (scale 1.3) | custom `CUS-Seal_NiagaAwan` (already on the outside) | gives the plain gable its identity; first placement sat 0.1 m inside the wall and showed only the diamond, moved to 5.78 m and checked |
| Four wall lanterns on the inner piers (at 4.0 m and -2.0 m along the hall, both sides) | Quaternius `FP-Lantern_Wall`, module LOD 700 triangles | light cue at the aisle's quarter points |
| Two more herb hangers over the produce tables | Syntaxes of Play `SY-herb-drying-hanger` | continues the overhead story |
| Scales on the north bench | Avramania `AV-mdvl_food_scales_01` | an interaction cue at the aisle's end |

No floor props were added: the aisle stays clear (the hall's camera and collision results are unchanged, see 04). Net triangle change is -1.4k (A02p 52,909 to 51,485): the additions are small and the module LOD of the fruit basket (3,646 to 1,300) and wheelbarrow more than pays for them. Before/after: [ba-p3-west-interior](visuals/before-after/ba-p3-west-interior.jpg).

Honest judgement (provisional, mine): the seal and lanterns lift the interior's vertical zone, but the hall remains plain brown overhead and the north end is still modest; a further step would be cloth or hanging goods across the tie beams, which was not taken to avoid scattering.

## 2. Paving: why the browser read blue, what was done

**Cause (measured, not assumed).** The same camera in Blender and in the browser:

| View | Blender | Browser before | Browser after batch 3 |
|---|---|---|---|
| Hall floor (RGB mean, lower left) | 101, 106, 111 | 83, 106, 129 | 98, 107, 116 |
| Sunlit cobble, arrival court (RGB mean) | 157, 150, 143 | 150, 153, 160 | 163, 152, 146 |

The baked paving textures are not blue (cobble mean 134, 127, 119; hall brick 153, 143, 133). The browser's blue comes from the image-based sky light (blue zenith, intensity 2.0) landing almost alone on up-facing, shaded floors, stronger than in the Blender render. A first runtime tint test ([A/B/C sheet](visuals/paving/paving-warm-A-B-C.jpg), cobble only) made the sunlit cobble neutral but left the hall floor teal even at multipliers of 1.5 / 0.7, which showed the tint had to be matched per material to the Blender colours.

**Change.** The warm multipliers are baked into the two stone-paving base-colour textures at export (`PAVING_WARM` in `p2a_kit_export.py`): `MI_UnevenBrick` (1.03, 0.96, 0.84), `MI_Brick` (1.31, 1.00, 0.80) in linear albedo, derived as Blender/browser colour ratios in two passes. The sky light, tone mapping and exposure were **not** changed (the batch-2 finding stands: a brighter or recoloured sky would not be an architectural improvement). The stone walls that use `MI_UnevenBrick` warm slightly with the paving.

**Residual.** Blue minus red is now 18 (hall) and -17 (cobble) against 10 and -14 in Blender; the hall floor still reads cool in shade, which is the lighting. Runtime tuning switches remain (`?warm=`, `?warmb=`). Not judged: the owner's eye on the result, which is the real test.
