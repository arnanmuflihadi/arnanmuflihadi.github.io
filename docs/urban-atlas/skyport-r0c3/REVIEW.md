# Pelabuhan Awan / R0-C3

**Complete local integration. Owner visual approval pending. No public deployment.** [Play locally](../../../index.html?experience=adventure&dev-town=s2f&town-layout=reset-final&town-props=cc0&town-guild=r0c2&town-skyport=r0c3&build=skyport-c3-final) · [Matched screenshots](index.html) · [Blender master](../../../validation/skyport-r0c3/pelabuhan-awan.blend) · [Optimized GLB](../../../assets/game/skyport/pelabuhan-awan.glb).

The low double-wing clay canopy, forked timber piers, two-sided jade sign and flush windrose turn the existing arrival disk into an identifiable tropical skyport. The original 13 m deck, guard arrangement, spawn and continuous town approach remain. Four actual local Kenney CC0 models supply eight waiting/cargo/lantern placements; existing pavilion shoes/piers and six architectural material definitions are reused. Only the distinctive canopy/connecting structure, sign and inlays are custom authored. [Selected sources and licenses](ASSET-RECORD.md).

## Fit and playability

Centre world **(13.33941, 67.47880)**, local **(u,v)=(0,−7)**, datum **15.095 m**, rotation **35°**. Canopy **9.2 × 4.1 m**, highest roof **4.55 m above datum**. No deck extension, new stairs, terrain edits or vegetation changes. The existing deck follows measured ground; it is not an unsupported aerial slab. Boarding markings identify a future reservation, not functioning flight or a verified dragon-sized landing system.

Portal clear width **6.12 m**; lowest fascia clearance **2.595 m**. Four footing contacts range from **7.24 mm embedded to 3.13 mm above** the existing sloped paving, with no meaningful exposed foundation gap. Exact measured terrain/support is retained. Grounded shoes, ten movement proxies and sampled visible roof/fascia head-stop references use the existing controller. Camera clearance uses actual imported mesh rays, excluding these local movement proxies from the legacy axis-aligned sweep. No hidden floor or altered movement/camera physics.

**Seven live original-explorer checks pass:** uninterrupted arrival → Market Street → Telaga Awan → Guild (**42.163 m**), complete reverse (**42.160 m**), canopy passage, pier collision, both guards, and jump/landing (**1/1**). Elevation **15.040 → 16.050 m**; existing Guild steps remain. Main-route camera separation stays at least **3.158 m forward / 2.511 m reverse**; close guard probes pull the original camera inward to approximately **1.57 m**. [Live results](../../../validation/skyport-r0c3/live-evidence.json).

Nine CPU controller/support cases also pass, including full routes at **20/60 Hz**, measured footing contact and exact rollback. The existing Guild research button opens the authentic transit panel; closing it retains adventure mode, player position and scene. [Controller/fit](../../../validation/skyport-r0c3/controller.json) · [Research interaction](../../../validation/skyport-r0c3/research-interaction.json).

## Measured browser cost

Delivery **731,580 bytes**, **14,600 triangles**, **eight indexed static batches/materials**, **zero textures/transmission**. Native raw GLB **876,340 bytes**. Source collections/modifiers remain editable; export batches have baked transforms and one supported axis conversion. No decimation of roof silhouette. Cold request **731,880 transfer bytes / 2.5 ms** on the local server; one extra cached GLB, **10 files versus nine** without the flag. Off/on toggles reuse the same cache.

| Same 12-second camera rail + 2-second warmup | Skyport OFF | Skyport ON |
|---|---:|---:|
| rAF median / p95 | 5.60 / 11.20 ms | 5.60 / 11.20 ms |
| CPU submission median / p95 | 1.00 / 1.30 ms | 1.00 / 1.30 ms |
| All-pass draw calls | 327–396 | 335–412 |
| Submitted triangles | 2,530,358–2,593,700 | 2,544,958–2,622,900 |
| Samples | 1,706 | 1,709 |

Apple M4 Pro / ANGLE Metal; standard shadows, exposure **0.96**, approved Glass **B**, DPR **1**, game buffer **1280 × 656**. Same cameras/settings; no simultaneous Blender render. These are rAF/CPU timings, not GPU timings or mobile claims. Active-walking costs are recorded separately in the live evidence. No new texture request, transmission pass, console warning/error or missing texture. [Raw performance and resource inventory](../../../validation/skyport-r0c3/performance.json).

## Evidence, preservation and rollback

Five matched before/after pairs plus actual third-person gameplay: [whole island](../../../validation/skyport-r0c3/01-island-after.png), [skyport aerial](../../../validation/skyport-r0c3/02-aerial-after.png), [spawn](../../../validation/skyport-r0c3/03-arrival-after.png), [town approach](../../../validation/skyport-r0c3/04-town-route-after.png), [market return](../../../validation/skyport-r0c3/05-market-return-after.png), [explorer](../../../validation/skyport-r0c3/06-gameplay.png). Camera/FOV/settings accompany every image. Pedestrian views are **1.65 m above actual support**. [Visual observations and corrections](VISUAL-QA.md).

**24 relevant regression tests pass, none skipped**: skyport flag/GLB, Guild, character, town integration/stabilization/population and all six research studies. [Executed results](../../../validation/skyport-r0c3/regression.log). Approved Guild/code/GLB, four shops, fountain/pavilion, terrain, forest, original props, character/camera and project registry remain unchanged against the checkpoint. [Preservation hashes](../../../validation/skyport-r0c3/preservation.json).

Fresh browser checks confirm **zero skyport requests without its flag**, with the Guild and 42 props retained. A fresh default `project=mbr` load has only the original five landscape/character GLBs, one renderer and the authentic MBR panel; switching to editorial and opening the complete index preserves all six study links. [Disabled load](../../../validation/skyport-r0c3/disabled-load.json) · [Default load](../../../validation/skyport-r0c3/default-load.json) · [Portfolio navigation](../../../validation/skyport-r0c3/portfolio-check.json).

Remove **`town-skyport=r0c3`** and reload to restore the accepted populated town and Guild without any skyport request. Local Skyport off removes its root/colliders exactly while retaining cache. Town off restores the original landscape and removes all development layers; Town on restores them with the **same scene and one renderer**, without extra requests. [Live rollback](../../../validation/skyport-r0c3/rollback-live.json).

Verified pre-implementation checkpoint **`codex/guild-town-baseline` / `5e71477a39220d12808e24e38851e9d3cfabc04e`**. Exact entry/review/manifest backups are under `validation/skyport-r0c3/baseline/`; preserve unrelated working-tree changes when restoring. A local no-store server avoids inherited preview module caching: `python3 validation/skyport-r0c3/serve.py`, port **4176**, loopback only. Existing preview servers are untouched.

Remaining limitations: **(1)** owner artistic approval is pending; **(2)** travel/creature boarding is intentionally inactive; **(3)** mobile hardware and GPU timings are untested. No critical technical blocker was observed. Stop at R0-C3.
