# P2-A correction report (closeout)

Baseline: P1.4 layout D and the P2-A slice as delivered (preserved unchanged in `merchant-citadel-p2a/baseline-p2a/`: P2-A GLB, scene data, `p2a.js`, `p2a-tests.js`, evidence, SHA-256 list). The pipeline (Blender → one kit GLB → three.js with the game's own controller, camera, character and collision modules) is unchanged; no asset research, planning or Blender conversion was restarted.

## 1. Corrections to my own P2-A statements

Three conclusions in the P2-A package were wrong. They are corrected here and in the P2-A documents.

| P2-A statement | What is true | How it was found |
|---|---|---|
| "The B04–B05 alley is 1.34 m wide" (a trail-width violation) | 1.34 m is the gap between the **roof-eave envelopes**. The walls are 3.0 m apart at the A11 turret and 4.0 m elsewhere. The real problem was a street centre 0.5 m off the junction node N03 and eaves nearly touching overhead | recomputing from the collision proxies before changing anything |
| "The ~23-point lighting error is structural: no AO, ACES instead of Neutral" | The preview's sun was **mirrored** (light from the north-east instead of the south-west). Correcting it took the error from ≈ 23–26 to 9 points. AO and Neutral are still improvements but not the main cause | the hall front stayed dull at any AO strength |
| Frame times "GPU-synchronised with `gl.finish()`: 0.6–2.4 ms" | `finish()` does not wait for the GPU in Chromium. With a read-back the same frames cost 3.5–6.4 ms (about 5x) | a SwiftShader (software) run took ~1 s per frame while reporting 1.5 ms |

## 2. Circulation (details: [02](02-pedestrian-network-spec.md))

| Issue | Fix | Result (real controller, both directions) |
|---|---|---|
| N16–N17: N17 0.55 m from a veranda post | **N17 → (36.16, 62.24)**, the centre of the 1.49 m clear gap; post layout kept | N16⇄N17 pass; 360° turn in place at N17 without moving; oblique approaches from SSW and SSE pass; clearance 0.30 m each side |
| B04–B05 cross street | **B04 moved 1.2 m south**: walls 4.2 m apart at the turret, street centred on n 19.9 (N03 at 20), eaves 2.54 m apart. Open, permeable, not closed | west and east cross streets walked both ways, 0 stuck |
| Market cross blocks the straight line | **Cross kept** (it is the market's landmark, on the Hall's axis). 3.85 m clear each side; N29/N30 centred at x = ±2.9; edges as polylines | spine walk and run pass with the camera at ≥ 12.3 m; the straight line through the cross is documented as blocked |
| Whole network | all 34 slice edges walked in both directions; 28 nodes standability-tested | **34/34 pass, 28/28 standable, 0 stuck** |

## 3. Camera (details: [03](03-camera-validation.md))

Cloth, signs and pennants stay out of camera collision (re-confirmed with the corrected routes). New, evidence-based: thin posts (0.4–0.5 m, including the 4 m market-cross post) are ignored by the camera (spine walk 3.64 → 12.25 m, pops 15 → 0). Severe compression in the four critical spots is handled by a preview-side **character fade**, which takes the share of time the character covers more than a quarter of the screen from 37–64 % to 0–0.8 %. **The production camera and controller are not modified** (hashes identical).

## 4. Visual parity (details: [04](04-lighting-and-materials.md))

Sun direction corrected, Khronos Neutral tone mapping injected, baked per-vertex AO (indirect light only), bluer sky, darker stand-in ground. Judged on matched Blender/browser views: the Exchange Hall, street and court now read like the Blender renders; remaining differences listed honestly in 04.

## 5. Performance (details: [05](05-performance.md))

Re-measured with a method that really waits for the GPU. Apple M4 Pro: 3.0–5.9 ms per frame at 720p, 12.6 ms at 4K; 335 draw calls (123 merged); 308.5k triangles drawn with the hall after module LOD (418k before; 347k → 240k kit triangles, GLB 21.3 → 17.4 MB). A software-rendered run (SwiftShader) gives ~1 s per frame and is a stress bound only. **No lower-end hardware was available; that limitation is explicit.**

## 6. Exchange Hall (details: [06](06-p2b-batch1-proposal.md))

The grey stand-in is gone: the hall is five reusable modules (main hall, two wings, porch, tower) exported in the kit with seals, dormers, banners and lanterns, with 23 collision proxies, tested stairs and porch access, camera cases and matched views.

## 7. Defects and limits that remain

* One machine only for performance; lower-end hardware unmeasured.
* No human playtest; all routes are simulated at 60 Hz.
* Baked AO is on the heavy side and soft on large faces; the sky, ground and horizon are stand-ins.
* The fade is a preview feature: not tested on the first island.
* Owner approval pending (see 07).
