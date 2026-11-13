# R0-D1A — Dragon mount integration plan

Planning audit: 10 November 2026. **Implementation is not authorized by this document.**

## 1. Recommendation and decision

**Conditional GO for reuse; NO-GO for integrating the current jade export. Recommend Option B, narrowly scoped to export fidelity, rider fit and missing animations.** The original dragon has usable organic geometry, four legs, articulated wings, a long neck/tail and a substantial rig. Do not start another asset search or full creature redesign.

The decisive finding is a **pose mismatch between the untouched source and jade derivative**, beyond the color change. At the same normalized wing-cycle phase (6/25), CPU evaluation through the project's GLTFLoader gives:

| Metres, unscaled, Three.js Y-up | Original source | Jade derivative |
|---|---:|---:|
| Torso region extent, width × height × depth | 0.251 × 0.360 × 0.527 | 0.251 × 0.518 × 0.325 |
| Head-region centre, Y / Z | 1.387 / −0.111 | 1.331 / −1.641 |

Regions use vertices with at least 65% weight on the relevant torso/head bones. This is primarily an **orientation/pose issue, not proof of changed anatomy**: a 78.95° X-axis correction about the pelvis aligns the wing-clip head position within 0.04 mm at five sampled phases. The head-turn clip instead needs approximately 0°, so one constant asset rotation is not a validated fix across states. The import/export cause remains undiagnosed. The saved Blender scene also shows the upright torso; it is not the sole fidelity reference. Earlier checks missed this drift.

First restore source-pose fidelity while retaining the approved jade texture. Then test a **roughly 3× uniformly scaled candidate** with the actual explorer, without assuming it fits. Prefer a grounded, crouching boarding pose on the open portion of the existing deck: site **Option C**, a future localized landing-bay adaptation. Both asset and site recommendations remain conditional on D1B visual/clearance approval.

## 2. Verified asset and animation inventory

Files under [validation/stylized-dragon-review](../../validation/stylized-dragon-review/README.md) exist. The unchanged original is 5,641,080 bytes; jade GLB is **4,675,680 bytes**. Jade SHA-256: `104c2f73158ed381ae0f2e99d43492f8c0de256d5a1a7dceaf82bf5e7d5b5a19`. The editable `.blend` exists and was inspected through live Blender MCP 5.2.3 LTS; no save was performed.

Both GLBs contain **57,936 triangles, two render primitives and one 99-joint skin**. The body is skinned; the eye mesh follows the head hierarchy without its own skin. No morph targets. Jade has two opaque, double-sided PBR materials, three embedded 1024² PNG images (color, normal, packed surface map), and four texture definitions, including a duplicate reference to the color image. No transmission or external image URI. Body roughness factor is 0.876, metalness zero; eyes are glossier.

| Clip | Source duration → jade playback duration | Source → jade channels | Actual content / reuse |
|---|---|---:|---|
| `Wing flaps` | 1.041667 → 1.083333 s | 80 → 297 | Wings plus body, legs and tail motion. Best cruise/hover basis. Endpoint rotations match; velocity/visual seam remains unreviewed. |
| `head turn` | 3.708333 → 3.750000 s | 130 → 297 | Neck/head glance; not a grounded idle or boarding animation. Endpoint rotations match. |
| `head turn/wing flaps` | 3.708333 → 3.750000 s | 197 → 297 | Combined action; wing-base endpoints differ by **72.9°**. Do not repeat as a seamless cruise loop. |

Jade keys begin at 0.041667 s; Three.js clip duration includes that initial hold. Each jade clip targets all 99 joints with translation/rotation/scale tracks; most are constant. Same-rig crossfades are possible with the existing AnimationMixer, but full-body head-turn tracks would compete with flight. Leave them unused initially; a later optional neck-only track filter can preserve the original clips. Hip bob is pose motion, not a transport trajectory.

Fresh checks: GLB metadata/binary inspection; CPU GLTFLoader/AnimationMixer pose sampling; live Blender mesh, bone and frame inspection with the original frame restored. CPU loader inspection removed textures **only in memory**: it proves parsing/deformation, not browser materials or performance. Browser control is available again, but the jade asset has no verified browser review; that check belongs to D1B. No gameplay or regression suites were rerun for this document-only phase.

## 3. Dragon / player / skyport fit

The controller uses a **1.9 m explorer**, 0.34 m horizontal collision radius and 0.42 m maximum ground step. The separate 1.65 m reference-camera height is not the character's body height.

| Measured source geometry / accepted site | Result and implication |
|---|---|
| Source wing cycle, 26 keyed samples | Maximum span **3.654 m**; cycle-union envelope **3.654 × 3.016 × 1.828 m** (width/height/depth). A union is not a simultaneous pose or continuous collision proof. |
| Candidate scale 3×, calculated | Span **10.96 m**; union **10.96 × 9.05 × 5.48 m**. Torso approximately **0.75 m wide / 1.58 m long**. Promising for one rider, unverified with the explorer's pelvis, knees and boots. |
| Dorsal torso / tail, source | Torso region reaches about Y=0.687; at 3× its top is about **2.06 m above the asset origin**. Tail reaches about **2.32 m below origin** while feet reach roughly origin height. A flight pose would drive the tail into a landing deck. |
| Deck / datum | Diameter **13 m**, centre world X/Z **(13.339, 67.479)**, town-local `(u,v)=(0,−7)`, nominal datum **15.095 m**. Paving follows ground, not one horizontal plane. |
| Canopy / portal | **9.2 × 4.1 m**, lowest fascia **2.595 m**, portal width **6.12 m**. Neither flapping wings nor a mounted rider may be assumed to clear it. |
| Spawn / guards / C3.1 | Spawn `(0,−10)`. Closed perimeter guards are about 1.24 m visually / 1.30 m in collision. Pylons at `u=±3.55,v=−10.5`, height 2.2 m; beacon at `u=−4.6,v=−8.3`, height 5.2 m. All must enter the swept-volume check. |

Dimensions come from the actual GLBs, [site survey](../../validation/skyport-r0c3/site-survey.json), accepted integration modules and a fresh CPU survey using the RESET-FINAL terrain sampler. A source bone's name/transform is not itself a measured seat surface. Candidate seat location: dorsal spine behind the wing roots, provisionally associated with `spine_02`; final offset and rider visibility require actual poses.

## 4. Visual concerns and minimum improvements

The source silhouette has a restrained head and articulated limbs, but its slim torso, long neck and hanging tail need a passenger-scale check. The jade export's pose distortion currently makes this assessment misleading. **Recover fidelity before changing proportions.** Only consider localized torso thickening if the recovered model fails rider fit at a sensible overall scale.

After fit approval, retain jade, add a lighter underside, darker membranes and limited horn/claw contrast through the existing atlas/PBR palette. No new transmission shader or large textures. These changes can improve readability but cannot fix rider support, pose or tail contact. A compact saddle/harness, grounded crouch with folded wings and a curled tail are functional requirements for later authoring.

Existing evidence: [jade side](../../validation/stylized-dragon-review/jade-side.png), [wing frame](../../validation/stylized-dragon-review/jade-flight-frame12.png), [accepted skyport aerial](../../validation/skyport-r0c3-1/01-aerial-after.png). These are prior images; the studio renders do not establish browser fidelity. No human artistic score is assigned.

## 5. Boarding and landing arrangement

| Site option | Evidence / decision |
|---|---|
| **A — nearby natural pad** | Local 6 × 8 m probe centred `(0,−18)` has **19 of 221 samples outside the island**, with valid ground 13.790–14.865 m. A lateral probe `(10,−8)` stays on-island but spans **0.867 m**, median grade 11.9%, maximum 28.4%; it also requires a route around the closed deck perimeter. More grading/circulation work than justified initially. |
| **B — hover beside deck** | Requires rail-crossing/gate design plus a moving boarding target. Unproven saddle alignment, wing/pylon clearance and fall recovery. Reject for the first slice. |
| **C — future localized open-deck bay: recommended** | Test a **4 × 4 m stance reservation centred `(0,−10)`**, outside the canopy. All 81 half-metre samples remain on-island; current walking support **14.947–15.131 m**. It reuses existing ground-supported paving and town access. This reservation is not proof that the full creature fits. |

For C, keep closed guards, canopy, settlement and original spawn. The player must first vacate the spawn/landing reservation and reach a checked waiting point before approach is allowed. Board a stationary crouched dragon entirely inside the guard line; take off vertically clear of pylons before departing outward. Do not walk a mounted dragon beneath the canopy. A localized surface/detail adjustment is only a future proposal if measured foot contact requires it; no deck extension is assumed.

**D1B failure gate:** if the recovered dragon, tail, rider and complete wing sweep cannot fit without changing the canopy, opening guards or disrupting the civic route, do not force C or shrink the rider. Stop with the measured conflict for an owner site decision.

## 6. Minimum gameplay architecture

Reuse `skyport-boarding.js`, the shared model cache, existing actor/animator and entry-loop ownership hooks. D1 currently scales a Quaternius dragon to 5.2 m, keeps the explorer stationary, locks input, switches two clips and moves the creature between two points over a 6.8 s sequence. Its outbound endpoint `(4,−37)` lies **outside terrain support** (island fraction 1.081); it is not a landing site. Reuse cancellation/lifecycle hooks and the outbound corridor as a route seed, not as a finished transport route.

| State | Minimum motion source / requirement |
|---|---|
| Idle / Hover | Existing `Wing flaps` for airborne waiting; **new folded-wing, tail-clear crouch/hold** for ground boarding. |
| Approach | Existing flight loop plus one guided root path; check deck occupancy and swept geometry. |
| Board | **New explorer boarding action**, stable dragon hold and measured seat/pelvis alignment. No jump-to-saddle claim. |
| Takeoff | **New dragon crouch-to-flight transition**, synchronized with controlled lift; rider seated action. |
| Cruise | Existing wing loop, guided route, small wrapper-bank/turn easing; preserve source tail motion. |
| Landing | Guided descent plus **new fold/foot-contact/tail-clear landing transition**. Reversal of takeoff is only a candidate to inspect. |
| Dismount | **New explorer dismount action**; reuse/reverse boarding only if contact and timing actually work. Validate ground, then resume the original controller. |

Use one activity coordinator in the existing update loop, not another movement engine. Load before input takeover; require grounded explorer, empty bay, valid destination and no open research panel. Use `world.library.get` and bundled `cloneSkeleton`; the static library `instantiate` explicitly rejects skinned models. Keep cached source data immutable and reuse one mixer per active rig.

Keep `ExplorerMovementRoot` in world coordinates. During riding, suspend its physics and drive its world pose from a bone-attached seat marker with the rider pelvis offset accounted for. Tick the existing animator separately: D1's present active-state branch skips `character.update`, which would otherwise freeze rider animation. Add authored rider clips through the existing animator; Idle/Walk/Run and jump clips are not seated/boarding actions.

One existing camera gets explicit ownership during boarding/flight, then `follow.handoff()` resumes ground follow. Frame rider, head and wings with bounded bank/FOV changes; preserve ACES/exposure and collision clearance. A **single same-island round trip returning to the departure bay** is the smallest safe destination scope. Do not infer free-flight safety from this guided path.

On successful dismount, sample current town support and clear obstacles before settling the explorer. Escape, visibility loss, pause, editorial switch, teardown and load failure must have one idempotent restore path: detach/restore actor pose, clear input, reset animation/controller, restore camera and return to the saved safe departure point when airborne. Reduced motion retains D1's explicit skip/safe return. No invisible floor, mid-air controller resume or altered physics. Guild/research interactions remain gated out during the activity and functional afterwards; editorial research stays independently accessible.

## 7. Performance and licensing

The dragon is **12.7× D1's 4,562 triangles**, or about 34% of the S2-D street asset's 170,709 triangles; this is asset geometry, not a frame-time forecast. Its GLB is about 4.68 MB versus D1's 0.261 MB. Two opaque batches avoid transmission, but skinning, double-sided wings and shadows add work. Three 1K RGBA textures imply approximately **12 MiB decoded / 16 MiB with mipmaps**, an estimate rather than measured GPU memory.

Historical M4 Pro D1 evidence, 1280 × 656, DPR 1, standard shadows, 600 samples:

| | Preview off | Old preview on |
|---|---:|---:|
| rAF median / p95 | 5.5 / 6.3 ms | 5.6 / 6.0 ms |
| All-pass calls / triangles | 409 / 2,607,520 | 411 / 2,616,644 |

For jade alone, **estimate** two color draws and two shadow draws / 115,872 submitted triangles if both meshes enter one shadow pass. Actual pass visibility and costs must be measured. Start with one LOD0 hero, two materials and no new rendering dependency; target ≤4 incremental calls in that matched pass configuration and investigate a >10% median/p95 increase. Do not silently lower quality to pass. Set conservative animated bounds from sampled poses, avoid per-frame full vertex scans, and pause idle offscreen pose work without pausing transport progression. Add a distant LOD only if distance/performance evidence warrants it. No mobile/integrated-GPU readiness claim; those remain untested.

[Stan's Stylized Dragon](https://sketchfab.com/3d-models/stylized-dragon-97d00c182fa24fa4838493c41ad8e52c) is identified as **CC BY 4.0 in the actual original GLB metadata**. Preserve author/title/source, [license link](https://creativecommons.org/licenses/by/4.0/) and recolor/rig/animation modification notices in files, manifest and eventual visible credits. Public distribution is compatible with those terms. Keep both source files unchanged. No new search or purchase is justified.

## 8. Strategy decision matrix

Planning estimates: **5 = most favorable**, including easier integration, lower effort and better token efficiency. These are potential/feasibility judgments, not owner visual scores; C is largely unknown.

| Criterion | A: material/scale only | B: targeted mesh/animation recovery | C: replace asset |
|---|---:|---:|---:|
| Visual potential | 3 | 4 | 3, unknown |
| Rider compatibility | 2 | 4 | 2, unknown |
| Animation reuse | 3 | 4 | 2, unknown |
| Integration ease | 4 | 3 | 2 |
| Performance potential | 3 | 3 | 3, unknown |
| License suitability | 5 | 5 | 2, unverified |
| Development effort | 5 | 3 | 1 |
| Token efficiency | 4 | 4 | 1 |

**Select B:** recover the original pose/clip data, retain the jade atlas and rig, then author only functional mount additions. A could produce a quick scale demo but cannot resolve the present export mismatch or land convincingly. C would repeat acquisition and still leaves rider/site integration. Reconsider C only if source rig fidelity cannot be retained, usable rider support requires a creature redesign, or the model cannot meet a measured rendering budget. No search begins automatically.

## 9. Future gated roadmap

All paths below are proposed future change boundaries, not current authorization. Keep the D1 preview and approved game assets available independently. Effort is ordered **fit session → several animation sessions → integration/QA sessions**; transition authoring is the dominant uncertainty.

| Phase | Scope, reuse and minimum deliverable | Acceptance / evidence / rollback / owner gate |
|---|---|---|
| **D1B — fidelity and fit** | Independent `validation/dragon-mount-d1b/` derivative and minimal localhost review hooks in the existing `reconstruction-review.js`/`entry.js` only if approved. Reuse original rig/GLB and exact jade atlas; compare sequentially through the shared loader. No saddle or new clips. | Source-equivalent poses, actual explorer fit and source-to-browser materials; cycle-sampled deck/canopy/pylon/tail envelopes. Browser side, three-quarter and skyport/rider views with fixed scale/cameras. Restore review flag to zero new requests and original scene. **Owner approves creature scale and boarding bay.** |
| **D1C — contact and animation** | Separate editable Blender/export derivative; compact saddle/seat marker, crouch/tail clearance, takeoff/landing transitions and explorer board/ride/dismount clips. Reuse rigs, source cruise and existing animator; no route yet. | Visible pelvis/hand/boot contact, no wing-root intersections or ground clipping, synchronized transitions and safe cancel at each state in the same-world review hook. Export/reimport proof and matched browser close views. Remove prototype flag/owned clones to rollback. **Owner approves contact and motion.** |
| **D1D — one guided round trip** | Extend the existing boarding coordinator and minimal entry/catalog hooks behind an explicit localhost/default-off mount flag, mutually exclusive with D1. Reuse camera, input, support, cache and outward route seed. | Real explorer boards, flies, lands, dismounts and resumes walking; complete civic route and Guild research still work. Browser departure/cruise/landing plus continuous trace; cancel, hidden tab, pause, failure and reduced-motion cases. Flag removal restores old D1 or no dragon. **Owner accepts playable transport.** |
| **D1E — focused polish and cost** | Only demonstrated material, timing, bounds/shadow/LOD defects; relevant asset/boarding files and current QA harness. | Matched off/on rAF/draw/triangle/network measurements, no missing textures, relevant boarding/skyport/character/Guild/portfolio regressions, one scene/renderer, warm-cache and fresh flag-off checks. Fixed-camera before/after and active rider evidence. Preserve D1D checkpoint. **Owner visual approval; no deployment implied.** |

## 10. Exactly what to do first in D1B

1. Open the **original and jade GLBs sequentially with the real browser loader**, at the same wing-cycle phases and camera. Confirm the measured pose discrepancy before any modeling.
2. Test a source-faithful derivative that reuses the exact approved jade image **without changing original nodes, inverse bind matrices or animation tracks**. Prefer replacing only that embedded image over another unrestricted rig round trip; inspect any later Blender re-export against this baseline.
3. Compare one uniform 3× candidate with the actual 1.9 m explorer and a temporary seat-position marker. Measure torso/wing-root/rider clearance, back orientation, source tail drop and prospective crouch boarding height. Correct scale before considering local proportions.
4. Inspect the proposed 4 × 4 m bay against the whole animated envelope and actual C3.1 meshes/guards, using the updated terrain/support. Record needed folded-wing/tail poses and any localized surface conflict; do not modify the skyport in this fit check. Capture only the decisive fixed views and return for approval.

**Hard stop: D1A delivered. No dragon, animation, saddle, skyport or production implementation was performed.**
