# R0-D1C — mount feasibility

**NO-GO for straightforward reuse as a grounded rideable mount at the unchanged skyport.** The bounded static trial failed. This is not proof that a specialist could never rebuild its deformation system. Further pose work stopped; owner approval is required for any next phase.

## Rig audit

Terra inspected the original GLB mechanically; Sol performed live Blender tests and final judgment. One 99-joint skin, 39,778 body vertices, maximum four influences. Weight sums: 0.999999866–1.000000119. Vertex counts with one/two/three/four influences: 18,148/12,236/4,582/4,812. Separate eye mesh is unskinned and parented through the hierarchy.

Each wing has a weighted root, wrist and three finger controls: wingbase.L_026/R_039 → wingwrist.L_027/R_040 → wingfinger01/02/03. Weighted vertex counts L/R: root 950/873, wrist 986/990, fingers 1028/1030, 1413/1423, 1529/1538. Finger heads share an exported location; synthetic end bones are not trustworthy anatomical fingertip targets. FK rotation exists, but convincing folded deformation is not supplied.

Tail chain: hips.001_053 → hips.004_054 → hips.003_055 → hips.002_056, with 1083/656/522/700 influenced vertices. Four limbs have shoulder/forearm/hand and thigh/shin/foot/toe articulation. No operating IK constraints or anatomical limits survive in the imported dragon; IK-named bones alone are not a functional IK rig.

| Original clip | Duration | Channels | Movement |
|---|---:|---:|---|
| Wing flaps | 1.041667 s | 80 | Wings and body/tail |
| head turn | 3.708333 s | 130 | Head; wing tracks single-key static |
| head turn/wing flaps | 3.708333 s | 197 | Head, wings, tail/body |

No authored grounded/folded/boarding/riding/landing state is established. Original actions remain in the isolated derivative, muted for static inspection; no new keyframes. D1B fidelity tests were not repeated.

## Bounded trial

Only **3×** was tested. One standing/FK trial, bilateral root/wrist folding and one finger-fan closure were attempted, with a curved tail and actual 1.9 m explorer. No second scale or repeated rescue iterations followed the unacceptable fold. Shrinking does not resolve membrane deformation and reduces rider capacity.

Context consists of unchanged imported C3/C3.1 geometry, plus exact development-game deck/guard triangles extracted read-only by `node validation/dragon-mount-d1c/context.mjs`. `deck-guards.ply` retains triangles at town-local v≤0. Coordinates are town-local u/v/Z, with 15.095 m datum subtracted; deck slope is preserved. Dragon root is at u=0,v=-12 to test the outward area away from the canopy, not a changed game spawn. Context uses neutral review materials; production materials are unchanged.

| Check | Result |
|---|---|
| Posed bounds | 4.490 m wide × 6.555 m long × 4.472 m high |
| Foot support | **FAIL:** front soles float 0.180/0.182 m; rear soles 0.077/0.072 m above actual deck |
| Support penetration | 636 evaluated vertices below raycast support; maximum 0.400 m; wing tips visibly penetrate floor |
| Site surface intersections | 222 triangle pairs against combined deck/guards; 148 against C3 weathered-bronze batch |
| Folding | **FAIL:** broad membrane sheets collapse downward rather than tucking convincingly |
| Pelvis | (0,-10.9,1.70), nearest dragon surface 0.187 m away |
| Knees | Approximately ±0.464 m lateral, Z=1.658 m |
| Ankles | Approximately ±0.525 m lateral, Z=1.220 m |
| Rider clearance | **FAIL:** 182 intersecting triangle pairs with legs, 142 with boots |
| Saddle | Not built; measured back Z≈1.501 m leaves ≈0.199 m to pelvis, but no valid leg/stirrup envelope |

BVH overlap counts are intersecting evaluated surface pairs, not penetration depths or counts of distinct obstacles. Knee/ankle distances of ~0.085/0.047 m are unsigned joint-to-surface distances and do not prove mesh clearance. Foot gaps use minimum vertices weighted to hand/foot groups (>0.25), raycast against game-derived support. Obstacle batches do not individually isolate every canopy, pylon, wind-standard and guard conflict. No zero-hit result establishes boarding/departure clearance. The failed fold and rider fit already fail the gate.

## Actual Blender evidence

Four Cycles renders, 1280×800, 16 denoised samples, common lighting. They depict **failed trials**, not approved poses:

1. `01-grounded-side.png`: attempted grounded stance; soles remain unsupported.
2. `02-folded-front.png`: failed fold; camera Z=1.65 m.
3. `03-seated-rider-side.png`: real explorer; independent foot controls placed at lower-leg ends, residual clipping visible.
4. `04-skyport-overhead.png`: unchanged skyport context and failed footprint.

Camera objects and measurements are embedded in `dragon-static-feasibility.blend`; main numerical results are in `measurements.json`. Inspection cameras are orthographic, not simulated gameplay. Wings conceal much of the rider/legs. An approximate static follow-offset centre ray is stored in the Blender scene; it is not a third-person camera-clearance pass. No gameplay, continuous flight sweep, browser performance or successful all-feet-supported/seated pose is claimed.

## Three blockers and next step

1. Current membrane deformation did not produce a credible compact fold in this bounded trial.
2. Rider legs/boots intersect the dragon and wings mask the riding posture.
3. Tested stance lacks foot contact and intersects unchanged site geometry.

**Cheapest credible next step, subject to owner approval:** inspect one alternative licensed rigged dragon with demonstrated grounded idle, bilateral folding, flight and landing, and a clear rider-back envelope. Verify actual animations and a 1.9 m rider before integration. Retain Stan's dragon as a flying creature/reference. Repairing it needs a specialist membrane/weight and mount-fit study, not simply a saddle or animation-state hookup. No search or next phase started.

## Preservation, license and rollback

All task writes are isolated here; no production game, terrain, controller, skyport or integration file edited. Source hash checks match prior records:

- Original GLB SHA-256: `427e832bb466b7eba096ffc056b9cac6897edc7c4b3fa182003c2deec3c5ac57`.
- D1B jade SHA-256: `4c9e49cb54d56a68b242cd94e383842204a046f7e65ea8759f1139acc6ce9dbe`.

Source: [Stylized Dragon by Stan](https://sketchfab.com/3d-models/stylized-dragon-97d00c182fa24fa4838493c41ad8e52c), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Changes: prior approved jade image replacement; isolated D1C static pose/root placement. Preserve attribution and modification notice. Skyport retains existing project-original/Kenney CC0 provenance; explorer retains repository provenance. No new assets acquired.

Rollback: close the derivative and reopen the original master. `live-workspace-before.blend` preserves the live workspace before testing. Removing this validation directory removes this phase; no runtime rollback is necessary. Stop for owner decision.
