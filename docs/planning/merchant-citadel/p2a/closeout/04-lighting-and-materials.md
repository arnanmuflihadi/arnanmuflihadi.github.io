# Lighting and material improvements (P2-A closeout)

Matched views: [`visuals/comparison/`](visuals/comparison) (Blender left, browser right, same camera) and [`visuals/before-after/`](visuals/before-after) (Blender | P2-A browser | closeout browser). Judgement below is by looking at those images; the numbers are supporting, not proof.

## 1. The biggest error was not what I said it was

P2-A reported a residual lighting error of about 23 luma points and attributed it to the missing ambient occlusion and ACES tone mapping ("structural"). **That was wrong.** The preview's sun was **mirrored**: `sunDir = (-0.55, -0.75, 0.38)` makes the light travel west and south (from the north-east) while the Blender light (rotation 52°, 0°, −34°) travels east and north (from the south-west): rotated 180° about the vertical. South-facing fronts, the Exchange Hall's front among them, were in shade in the browser and lit in Blender. Street views hid it because shadows still fell across the street.
Found while comparing the hall: its front stayed dull whatever the AO strength. Fixed to `(0.441, −0.616, −0.653)`, computed from the Blender Euler angles in three axes.
Effect (same five-to-six views, same scoring): best mean absolute luma error **≈ 23–26 → 9.0**, bias −1.7, warmth error 16. The earlier "structural" gap was mostly this. AO and tone mapping are still worth having (below) but they were not the main cause.

## 2. What was changed and how each was judged

| Item | Change | Visible effect | Cost |
|---|---|---|---|
| **Sun direction and colour** | Direction as above; colour (1.0, 0.95, 0.86) like Blender; intensity 4.2 | Facades, shadows and the hall now read like the Blender render. Largest single improvement | none |
| **Tone mapping: Khronos PBR Neutral** | The vendored three build exports only ACES. Neutral is injected per material (`onBeforeCompile`, `renderer.toneMapping = 0`), same function as the Blender view transform, exposure 0.75 | Plaster and cloth keep their hue in highlights instead of ACES's desaturation | one fragment function replaces ACES; no extra program |
| **Baked vertex AO** | Blender ray-casts 40 cosine-weighted rays (2.6 m) per vertex against the node plus a ground plane at its lowest point; stored as glTF custom attribute `_AO`; the shader multiplies it into **indirect** light only (`mix(1, ao, 0.45)`) | contact darkening under eaves, porch, balcony and window recesses; wall bases darken toward the ground | +1.7 MB in the GLB (428,675 vertices x 4 bytes); 1 varying and 1 attribute; no extra draw calls |
| **Environment** | Sky gradient made bluer (zenith #5f97dc, horizon #ece4d6) and intensity 2.0 | cooler shadows like the Blender sky fill | none |
| **Shadow resolution** | Kept 4096 (see 05: no measurable difference on this GPU; 2048 recommended elsewhere) | | |
| **Ground** | Stand-in plane darkened to #5f7a45 | no longer a bright mint plane | none |
| **Shared-material AO bug** | Paving tiles share the stone material of the buildings; a tile without baked AO read 0 and went black. Every mesh now gets an `aoBaked` attribute (1.0 where nothing was baked) | the black paving seen in an intermediate capture is gone | none |

Not done: material-level contact darkening beyond the baked AO (a height-based ground gradient was considered and left out because the baked ground plane gives the same effect without a shader term); screen-space AO (needs render targets the vendored build does not export).

## 3. AO strength: chosen by eye, and a limit

The bake uses strength 0.9 and a 0.2 floor; the preview mixes it at **0.45**. At 0.75 the hall facade was visibly darker than Blender's (compared on the hall tower view); at 0 the hall looked flatter. Vertex AO is interpolated across large faces, so a big roof or wall plane takes a gradient between its corner values: it is a soft effect, not a crease shadow. Mean baked value is 0.34–0.53 per node, i.e. the bake is on the heavy side; a lower bake strength (0.6) and a higher shader mix would give the same look with more headroom. That is a P2-B tuning item.

## 4. Numbers (supporting only)

Mean luma, Blender / browser, closeout: aerial 124/120, inn 134/140, junction 126/127, tea 162/161, terrace 149/150, hall aerial 126/127, hall porch 133/129, hall tower 162/158, B 99/107, B2 114/117, C2 154/157, D hall court 157/156, F 160/158, G 149/155. P2-A browser values were off by up to 40 (aerial 89 vs 126 in the first capture).
Calibration grid (sun 3.4–6.0, environment 1.0–2.0, exposure 0.6–0.9, 36 settings, six views): best sun 4.2 / env 2.0 / exp 0.75, MAE 9.02, bias −1.69, warmth MAE 16.2 (`evidence/calibration.json`). The chosen values are that optimum; AO and the final sky were set afterwards by eye.
**These numbers do not establish fidelity.** In P2-A a 23-point match hid a white-banner export bug and, as section 1 shows, a mirrored light. Both were found by looking.

## 5. What still differs (honest list)

* Sky: the browser sky is more saturated at the zenith; the Blender sky is paler there.
* Ground and horizon are stand-ins in both renders but differently coloured (flat green vs hazy).
* Paving reads slightly lighter and bluer in the browser; the paving seal is paler.
* No soft contact shadow under the character (Blender's stand-in capsule has none either).
* Roof moss/streaks: Blender's roof reads a little more weathered; the browser roof is flatter because the roof albedo is the 512/1024 px kit texture.
* Normal-map detail on brick/cobble is 512 px (1024 px for the three brick materials) so grazing paving is softer than in Blender.

## 6. Materials

* The banner fix of the first closeout step (Mix-node bypass) stays; the export now aborts if a baked material loses its base-colour link.
* No texture-tier or constants change was needed for the hall; its materials are the kit's existing ones (the tier-1 stone, plaster, wood, roof tiles). The hall added 4 signature-merged materials (56 → 60 in the Blender report) and 3 texture images (69 → 72).
* Rules for P2-B (see 06): bake AO at 0.6 strength, keep the tier policy, add a loader material cache, pre-warm shaders.
