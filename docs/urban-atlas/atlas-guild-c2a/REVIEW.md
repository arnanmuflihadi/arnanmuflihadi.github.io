# R0-C2A — Atlas Guild site and architectural design

**One isolated concept for owner visual approval. The production game is unchanged. No Guild GLB, deployment, playable integration or detailed interior was created.**

[Native Blender scene](../../../validation/atlas-guild-c2a/atlas-guild-design.blend) · [Four-view gallery](index.html) · [Measured scene record](../../../validation/atlas-guild-c2a/site-plan.json) · [Source record](ASSET-RECORD.md)

## Selected concept

A compact, stepped tropical research hall uses the existing warm plaster, timber, blue-green glazing and terracotta palette. A curved timber portal and glazed fanlight distinguish the entrance; an octagonal observation lantern establishes the long-range silhouette. The doors carry physical **ATLAS GUILD / BALAI RISET / AKSES TRANSIT** lettering. This identifies the future transit-research gateway; no research interaction is implemented.

The supplied floating-town concept boards inform the roof language and material family. Actual island capacity supports a small Guild outpost, rather than the large multi-wing research centre shown in the boards. No generated illustration is used as evidence.

## Site decision

The original `(44,−8)` reservation is a route boundary, not a ready-made entrance. Its ground is **Y23.535 m**, with a steep surrounding cross-slope. A conventional 14 × 12 m candidate spans **9.35 m** of ground elevation. The initial shallower placement also crossed the approved final approach.

The selected hall therefore occupies the **western contour-side gap**, with a short branch from the existing route at **(40,−4)**. The existing path to `(44,−8)` remains untouched. No market, square, fountain, pavilion, highland branch, mature tree or terrain vertex is moved. One small fern is proposed for replanting in the isolated scene.

| Measurement | Selected design |
|---|---:|
| Structural support envelope | X30.50–38.10 / Z−8.80–−4.20 m |
| Footprint | 7.60 × 4.60 m, **34.88 m²** after a 0.08 m² corner chamfer |
| Entrance / lower floor | **Y24.20 m**, door at `(34.10,−4.20)` |
| Rear reading-room floor | **Y25.60 m** |
| Entrance terrace | **7.51 m²**, about 1.65 m deep |
| Main roof ridge / curved portal peak | Y29.88 / Y31.40 m |
| Lantern top | **Y39.85 m**, 15.65 m above entrance floor |
| Door opening | 2.30 m wide × 2.70 m high |
| Final approach | **6.40 m**, versus 5.90 m direct separation |
| Stone approach / stair | 2.74 m approach; **7 × 178.6 mm** risers over 1.96 m |
| Approach width / stair width | 1.20–1.80 m / **2.30 m** |

The terrain-fitted approach has a **34.51% maximum measured centre grade**. It is a steep game-environment proposal, with no step-free-access claim. The full court-to-Guild route is approximately **31.89 m in plan**: the retained court route to `(40,−4)`, then the 6.40 m branch. The existing seven-step proposal is geometry only, not a traversal result.

## Terrain support and preservation

The hall uses two terrain-scribed stone tiers rather than a single deep platform. Over the surveyed envelopes, floor-to-ground gaps are **0.32–1.66 m** below the lower hall, **0.33–2.10 m** below the rear hall, and **1.33–2.40 m** below the small terrace. Footing corners embed 0.18 m; the maximum floor-to-bottom depth is therefore approximately **2.58 m**. These are environment-art support proposals, not certified structural designs.

Floor rims and wall finishes project up to 0.13 m beyond the structural envelope. The conservative support envelopes remain **1.48 m** and **1.24 m** from the approved route centreline for the hall and terrace respectively. This is a plan-clearance measurement, not proof of collision clearance. The new branch joins at the existing route; its final collider and camera behavior remain untested.

A rear-west eave initially intersected a retained tree. A clipped roof corner and matching 0.4 m body chamfer remove that conflict; the measured roof/affected-tree intersection count is now **zero**. All mature trees remain in place. The highland branch stays west of the square.

Forty-two native terrain samples agree with the current accepted game sampler to **0.0000162 m** maximum error. All **1,087 checkpointed source/assets/evidence files remain byte-identical**. [Verification](../../../validation/atlas-guild-c2a/verification.json), [preservation](../../../validation/atlas-guild-c2a/preservation.json).

## Actual Blender evidence

All four final PNGs are **1440 × 960**, rendered through live Blender MCP using Blender 5.2.3 LTS / Cycles, 48 samples with denoising. Camera poses and lens settings are recorded in `site-plan.json`.

1. [Guild from Telaga Awan](../../../validation/atlas-guild-c2a/01-guild-from-square.png): camera Y23.45, **1.65 m above the court floor**.
2. [Entrance and forecourt](../../../validation/atlas-guild-c2a/02-entrance.png): elevated architectural inspection with the human reference, doorway, landing and stair visible.
3. [Guild in the existing town](../../../validation/atlas-guild-c2a/03-town-context.png): all four approved market buildings, square and natural context retained.
4. [Measured site plan](../../../validation/atlas-guild-c2a/04-measured-plan.png): **60 m orthographic width**, north up, 10 m scale, dimensions and route annotations.

Native scene rays from both the square and Market Street reach the entrance glazing, curved fanlight and observation lantern before other objects. This supports landmark visibility in the native scene; it does not establish final browser appearance. No additional game overlay was necessary because the exact terrain and accepted town geometry are present in the Blender scene.

Visual QA corrected the shop-like initial portal, detached ladder-like lantern base, doorway planter obstruction, coincident terrace faces, folded approach surface and tree/eave collision. The final composition remains subject to human review. No internal score grants approval.

## Geometry and technical scope

The actual evaluated Guild/site concept contains **12,253 triangles** and reuses **17 material identities**, with **zero image-texture nodes** in those Guild materials. Terrain, existing town, human reference and plan annotations are excluded from this total. Roof shells and architectural parts remain editable in organized collections. Most visible complexity is in timber, glazing, signage and rails.

GLB size, browser draw calls, frame timing, browser glass/shadow appearance, new-route player traversal and operational research interaction are **NOT TESTED**: this phase intentionally has no export or integration. Future preparation must apply transforms, batch compatible parts, optimize lettering and validate the renderer's material transfer without assuming Cycles parity.

The six existing circulation preservation regressions were freshly rerun and pass:

```
node --test tests/circulation-c1c.test.mjs
node validation/atlas-guild-c2a/verify.mjs
```

[Regression log](../../../validation/atlas-guild-c2a/regression.log). These tests protect the accepted town/controller; they do not certify the proposed Guild route. No whole-game suite or unrelated optimization was run.

## Remaining review issues

1. **Approach:** the 34.5% stone branch is steep. Controller traversal, guards and camera clearance need an authorized isolated integration test; no playable claim is made.
2. **Proportions and capacity:** the compact hall, shallow terrace and tall 15.65 m lantern are intentional site trade-offs. Owner approval is needed before adding architectural detail or interior circulation.
3. **Rendering:** native context trees use render-only material clones. Browser lighting, glass, materials, export cost and performance remain unverified.

**STOP for visual approval before detailed modeling or integration. No public deployment.**
