# P2-B readiness recommendation, decisions and risks

## Recommendation

**Proceed to P2-B conditionally.** The P1.4 architecture reproduces at playable scale: scale and placement are exact, materials and palette carry over, the real controller walks every route and both stair flights,
and the camera behaves except at four places that are geometry decisions rather than engine problems. The conditions are owner decisions, not more engineering research:

1. Owner reviews the slice visually (preview URL below, plus `visuals/comparison/`) and accepts or rejects the lighting gap: no ambient occlusion and ACES instead of Neutral. If the flatter finish is not acceptable, P2-B must first add baked vertex AO to the kit (no new engine dependency) or authorise a post-processing change to the vendored three build.
2. Owner decides the three plan corrections (N17 position, the 1.34 m B04–B05 alley, the market-cross bypass) so P2-B builds the corrected plan.
3. A performance check on a lower-end device (or the intended minimum spec) is run before the whole-town budget in 02 is fixed.

If any of 1–3 is refused, P2-B should not start. Nothing in P2-A authorises P2-B.

## Decisions taken in P2-A (reversible)

| Decision | Basis |
|---|---|
| Cloth, signs, pennants do not collide with the camera; roofs/balconies/jetties/overhangs/arches do | 01, measured |
| Texture tier policy (92 MB) | 02 |
| One kit GLB, merge by material per district for static architecture | 02 |
| Lighting sun 2.2 / environment 1.1 / exposure 0.7 / ACES | 03 |
| Height field from real stair geometry as shared `heightAt` | 01 |
| Slice code is isolated (`merchant-citadel-p2a/`), imports unmodified game modules read-only | scope |

## Risks

| Risk | Level | Note |
|---|---|---|
| Visual finish without AO is flatter than the concept | **medium** | owner call; vertex AO bake is the cheap fix |
| Whole-town budgets are extrapolated from 8 of 24 buildings | medium | re-measure after the first district |
| Performance measured on one fast GPU, one viewport, DPR 1 | medium | see 02 |
| Camera in porches and against facades (tea-house veranda 0.5–2.8 m, hall steps 2.9 m) | medium | needs a design rule (fade/porch camera) in P2-B, not a proxy change |
| Narrow gaps (1.34 m alley) generate camera pops and stuck states | low–medium | fix in plan |
| Exchange Hall is a stand-in; camera and stair test against the real hall remain untested | medium | P2-B first item |
| Tests are simulated routes, no human playtest, no touch input | medium | do a 10-minute human walk before approval |
| Hidden-pane timer throttling made early timing runs unreliable; the final measurements ran with the pane visible and use synchronous timing | low | recorded in `performance.json` |
| Material cache and shader warm-up absent (spikes 22–34 ms at first use) | low | P2-B task |

## What failed or is unverified (plainly)

* A banner colour bug and an unlinked-material bug were found **only** by looking at the comparison sheet; the numeric luma comparison did not catch them. Both are fixed and re-verified. After the fix the GLB was audited: every glTF material that is not a flat custom (`CUS_*`) colour has a base-colour texture except `MI_WindowGlass` and `TMP_interior_core` (flat by design), and `MI_Banner@burgundy` was the only tinted variant on the failing path. A per-material screenshot audit was not done.
* Browser look does not match Blender in AO and tone mapping; reduced, not removed.
* No A/B of 512 px vs 1024 px normal maps.
* `renderer.info` does not expose the shadow-pass draw calls in this build; shadow cost is known only from frame time.
* Early test runs (first calibration, first route set) were superseded by the final runs listed in `evidence/`; files from superseded runs were overwritten or removed. `autotest-calibrate.json` is the first, narrower grid.

## How to run

```bash
node merchant-citadel-p2a/server.mjs --port 4180
```

Open `http://127.0.0.1:4180/merchant-citadel-p2a/index.html` (WASD/arrows, Shift runs, Space jumps; buttons teleport to spawn, junction, market, steps, inn, tea house; toggles for shadows, cloth/sign camera collision and collision proxies).
Automated tests: append `?autotest=scale|routes|cause|platform|views|perf` (writes JSON/PNG into `merchant-citadel-p2a/evidence/`). The server serves the repository root read-only and writes only into that evidence folder.
`window.P2A` exposes the scene, controller, camera, `camGroups`, `teleport`, `setMerged`.

## Rebuilding the GLB and parity renders

```bash
BLENDER=/Applications/Blender.app/Contents/MacOS/Blender
python3 docs/planning/merchant-citadel/p2a/blender/p2a_data.py        # writes merchant-citadel-p2a/data/scene.json
$BLENDER --background --factory-startup --disable-autoexec --python docs/planning/merchant-citadel/p2a/blender/p2a_kit_export.py -- <inspection_dir> <out_dir> merchant-citadel-p2a/data/scene.json
$BLENDER --background --factory-startup --disable-autoexec --python docs/planning/merchant-citadel/p2a/blender/p2a_world_scene.py -- <inspection_dir> <out_dir> merchant-citadel-p2a/data/scene.json merchant-citadel-p2a/data
python3 -I docs/planning/merchant-citadel/p2a/blender/p2a_compare.py <blender_renders> merchant-citadel-p2a/evidence <out_dir>
```

`<inspection_dir>` is the git-ignored `.asset-inspection/merchant-citadel-p1/` holding the extracted licensed packs; the two source `.blend` files are written there and are **not** in the review zip (85 MB and 95 MB, third-party textures embedded).
