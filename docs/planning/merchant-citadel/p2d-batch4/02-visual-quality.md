# 02 — Visual quality, matched renders and before/after

**These are provisional internal observations by the executor, not an approval.** Passing tests and matching images do not grant artistic approval (AGENTS.md); the owner decides. Images are in [visuals/](visuals): `blender/` and `browser/` (the 18 cameras, final), `comparison/` (Blender after | Three.js after), `before-after/` (2 x 2: Blender before | after on top, Three.js before | after below, same camera in all four), `before/` (the individual before images), `camera/` (real-keyboard screenshots).

## 1. How the pairs are made

* **Three.js:** the in-app browser (Chromium 156, ANGLE/Metal), the production GLB, the game's real controller and camera, 1280 x 720, Neutral tone mapping, baked vertex AO, shadows on, `?autotest=views&shot=final`.
* **Blender:** the source assembly of the same `scene.json` (`p2a_world_scene.py`: original P1.4 materials, afternoon presentation light, Eevee), the same camera positions, look-at points and fields of view (`scene.json["views"]`, 15 new cameras `p5-*`).
* **Before:** the batch 3 scene and GLB with the same cameras (`scene-before.json`, `baseline-batch3/`), so the "before" is the real previous state with an empty site, not a plan diagram.

## 2. What was compared

| Check | Observation |
|---|---|
| **Roof and façade alignment** | In the pairs looked at closely (court from the lane and from the east, loading bay, counting front and loggia, tea entrance and tea lane, quarter and route aerials, gameplay camera: 12 of 15) the three buildings agree in massing, roof pitch, gable positions, dormers, balcony, lean-to roofs, hoist and loggia between Blender and the browser; no module is displaced or missing in either. One visible difference: Blender shows a pale fascia board along B13's eave in the gameplay view where the browser shows tile and timber. The kit's nodes match their Blender bounding boxes to 0.005 cm and the placements to under 3 cm (03). |
| **Material consistency** | Same textures and colour grade as the existing district (stone ground floors, timber, plaster, terracotta, the dark civic tile on B13/E04). One accent added (sage awnings). **Known residual:** the browser's cobble and hall floors read cooler (bluer) than Blender's in shade, a lighting difference (sky ambient on up-facing surfaces) that batch 3 reduced but did not remove; see `cmp-p5-tea-lane-east.jpg`. |
| **Scale** | Doors and openings 2.1–2.4 m, loggia and gallery posts about 2.6 m, hoist 5 m, canopy 2.6 m; with the 1.9 m character the loggia and gallery read as walk-under spaces in the browser shots (`shot-real-keys-b4-loggia`, `-e05-front`). |
| **Light direction** | Shadows fall the same way in both renderers in the pairs looked at; the Blender sun is warmer and the sky a gradient, the browser's a flat blue with a flat green ground (stand-ins in both). |
| **Signage** | B13's crate sign, E04's coin sign, E05's leaf sign read at 4–6 m. **The leaf sprig reads closer to a heart than to a leaf at that distance** (`cmp-p5-tea-entrance.jpg`); the pictogram is a candidate for redraw (see 07). |
| **Proportions** | B13 is a long low-slung two-storey hall whose dark roof is the largest single plane of the quarter; E04 is the shorter, richer building (loggia, wing, standards); E05 is the tallest of the east frontage's corner. |
| **Visible seams** | None seen in the 12 pairs looked at closely at 1280 px. Not checked: the other three pairs at full size, close range from every angle, a free camera. |
| **Gameplay camera composition** | `p5-quarter-gameplay` (the follow camera 11.8 m behind and 6.6 m up) looks up the lane: B13's dark-tile roof fills the right third, the shops' roofs the left, and the lane reads as a narrow canyon (4.6 m between facades under roofs 10–12 m high) with a strip of sky; the court and path are not visible from there, they are discovered by turning in. Whether that canyon is attractive or oppressive is a playtest question (08). |
| **Luma** | Mean luma of the 15 pairs: Blender 110.9, browser 110.4; mean absolute per-pixel luma difference 16.9 (of 255), dominated by sky and ground. A numeric match hid a white-banner export defect in P2-A, so the pairs were looked at, not only measured. |

## 3. Before → after

| View | Before | After |
|---|---|---|
| [court from the lane](visuals/before-after/ba-p5-court-from-lane.jpg) | grass and sky | loading bays and tally table on one side, loggia and scales on the other, hoist and a crate in the air |
| [quarter from the south-west](visuals/before-after/ba-p5-quarter-sw.jpg) | an empty plot east of the lane | B13, E04 and E05 closing the lane's east side, the court between them |
| [tea entrance](visuals/before-after/ba-p5-tea-entrance.jpg) | one low shop's site and an empty lane | E05's gallery, tables and sage awning on the lane |
| [route aerial](visuals/before-after/ba-p5-route-aerial.jpg) | a dead-end lane to the lookout terrace | the porters' path with fence and lamps joining the terrace |

The other eleven sheets (`ba-p5-*.jpg`) are the same cameras at eye height and in the follow camera.

## 4. What the images do not settle

Whether the three buildings feel like the same town as the Central Bazaar at walking speed; whether E05's second storey is the right call (it is a deviation, 01); whether the dark roof of B13 is too dominant from the lane; the paving tint. These are the owner's calls.
