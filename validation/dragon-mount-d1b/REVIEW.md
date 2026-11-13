# R0-D1B — Dragon fidelity and fit review

**Result: fidelity PASS; rider fit FAIL for the trial marker; skyport clearance CONDITIONAL for a future grounded pose and FAIL for the current flight pose. Owner review pending.** D1B's full success criteria are not met. No game integration is authorized or implemented.

## Source fidelity

`dragon-jade-source-faithful.glb` is 6,363,084 bytes, SHA-256 `4c9e49cb54d56a68b242cd94e383842204a046f7e65ea8759f1139acc6ce9dbe`. It preserves the complete original binary payload and appends the already-approved jade PNG. Original nodes, meshes, skins, accessors, animation definitions and inverse-bind data remain unchanged; the embedded color PNG is byte-identical to the earlier jade derivative. The GLB retains Stan's CC BY 4.0 source/license metadata and a change notice. The original and earlier jade files remain unchanged.

`node validation/dragon-mount-d1b/verify.mjs` loads both source and derivative through the bundled Three.js GLTFLoader and AnimationMixer. At 21 corresponding phases in each of the three original clips, all 99 bone world positions matched exactly, maximum quaternion angle difference was 0.000000067 radians, and every 97th skinned vertex matched exactly. All clip durations match the source. This is sampled equivalence, not a proof for every possible interpolation time. Browser rendering showed the source and jade models in the same .25 s wing pose; the source is partly obscured by the site geometry in the comparison image.

The derivative has 57,936 triangles, two primitives/materials, one skin and three embedded 1K images. The model loads with textures in the browser; only a static animation frame was rendered there. Continuous playback was tested by the CPU AnimationMixer samples, not visually reviewed as motion.

## Rider and scale

3× uniform scale remains a **provisional candidate only**. The actual 1.9 m explorer is visible next to the dragon in `scale-on.png`; at that scale the measured source wing span reaches approximately 10.96 m and the torso is approximately 0.75 m wide. A static mockup aligns the explorer's Hips to a temporary marker at dragon-root local `(0, 0.72, -0.62)`; with the tested skyport placement this is world `(13.993, 17.220, 68.413)` m. No saddle or animation was authored. The manually adjusted static legs and seat point visibly intersect or disappear into the wing/root region. Pelvis, knee and boot clearances and third-person sightlines are **not validated**; do not use this marker as a final seat location. Test a different seat location and a properly authored seated pose before approving scale or proportions.

## Skyport clearance

The existing deck is 13 m wide, the fascia is 2.595 m above datum, and the proposed stance reservation is 4 × 4 m around the existing spawn. The reservation does not contain the full dragon: the sampled source wing envelope at 3× is approximately 10.96 m wide. The current animation contains no folded/crouching pose, so its grounded footprint and foot contacts cannot be measured as a real landing pose.

`node validation/dragon-mount-d1b/clearance.mjs` samples 26 flight frames and every third body vertex against the existing C3/C3.1 object collision boxes. It found **89 sampled vertices inside the wind-standard collider and 65 inside canopy-pier colliders**. These are volume-sampling findings, not exact continuous triangle/triangle collision counts. The lowest sampled dragon point was Y=12.741 m against deck datum 15.095 m: **2.354 m below datum**. The underlying hanging tail must be curled or repositioned before any landing test. Absence of a hit on other guards/pylons is not proof of clearance. A safe waiting point and the vertical departure corridor remain untested. The fixed spawn must be vacated before any future landing attempt.

Minimum next authoring, subject to owner approval: grounded crouch and foot contact; bilateral wing-root/wrist/finger folding; raised/curled tail; a correctly positioned seated rider with knees/boots clear; board/dismount and ground-to-flight/landing transitions. Then repeat a continuous swept-geometry/camera/guard check. Do not modify the skyport or treat the current flight pose as a landing pose.

## Browser evidence and cost

The isolated localhost review uses the existing world construction, GLTFLoader/cache, player model, skyport assets and Three.js renderer conventions. It does **not** add the dragon to the production game or include boarding gameplay. The exported PNGs are real browser-rendered canvas frames, 1364 × 1209, DPR 1, ACES exposure 0.96, standard shadows:

- `compare-on.png`: source and corrected jade at the same wing phase and scale, with site occlusion.
- `scale-on.png`: actual standing explorer and dragon.
- `rider-on.png`, `rear-on.png`: temporary static rider placement; visibly unapproved.
- `site-on.png`: skyport placement; `overhead-on.png`: overhead view. The overhead has no dimension annotation; the measured bounds are in `clearance.json`.

Matched site camera, same browser/settings, 200 rAF intervals following 30 warm-up frames:

| | Dragon hidden | Dragon visible |
|---|---:|---:|
| Calls | 184 | 186 |
| Submitted triangles | 1,307,506 | 1,365,442 |
| rAF median / p95 | 5.5 / 6.1 ms | 5.6 / 6.5 ms |

Delta: **2 calls and 57,936 submitted triangles** in this displayed configuration. These are frame intervals, not GPU timings; the sampled renderer counter does not establish separate shadow-pass cost. Both configurations preloaded the dragon, so this is not a network/cache benchmark. The jade is quite dark in the skyport's existing lighting. No mobile, animated-flight, full gameplay, texture-memory or camera-collision performance claim is made.

## Rollback and provenance

Delete or remove the `validation/dragon-mount-d1b/` review directory after retaining evidence; no production integration was changed. To view locally, run `python3 validation/dragon-mount-d1b/serve.py` from the repository root and open `http://127.0.0.1:4177/validation/dragon-mount-d1b/index.html`. The server binds localhost; its capture endpoint only accepts the six named PNGs in this directory.

Source: [Stylized Dragon by Stan](https://sketchfab.com/3d-models/stylized-dragon-97d00c182fa24fa4838493c41ad8e52c), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Modification: original red color image replaced with the project's jade recolor. Preserve source attribution, license link and modification notice in any derivative distribution.
