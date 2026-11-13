# Reusable asset, material and collision construction rules (proven in P2-A)

Each rule is something the slice needed or something that broke once. File names refer to `docs/planning/merchant-citadel/p2a/blender/` and `merchant-citadel-p2a/`.

## Coordinates and orientation
1. Plan: x = east, n = north. three.js: (x, elevation, −n). Blender: rotation about Z by θ ↔ three `rotation.y = θ`. glTF front is **+z**; Blender (x, y, z) → glTF (x, z, −y). Verify with a front-projecting part (turret, balcony, veranda): its bounds centre must be at z > 0 (scale test does this).
2. Every kit node is exported at the origin with **rotation, scale and location applied** (`transform_apply` before `origin_set`); placement sets only position and `rotation.y`. A baked rotation survives placement and silently double-rotates (it did for four nodes).
3. Node roots are named `ROOT_<name>` to avoid `.001` clashes with joined objects.

## Geometry
4. One GLB for the kit (all archetypes), embedded textures, so each texture uploads once. Merge **per archetype per material**; do not join across archetypes (placement needs them separate).
5. One UV set and one colour attribute per mesh (`export_vertex_color="MATERIAL"`, `export_all_vertex_colors=False`); extra UV/colour layers were 60 % of the file.
6. Paving: three 2 x 2 m tile meshes placed with `InstancedMesh`; keep tile top at +0.01 so the height field and the visual agree.
7. Repeated small pieces stay instances or become one merged mesh per (district x material); never one mesh per piece.

## Materials and textures
8. **Signature-merge** materials (same textures + constants) before export; keep a loader cache so identical names do not create duplicate three materials (68 objects for 55 names in P2-A).
9. Tier policy: tier 1 (visible at street scale: brick, wood, plaster, roof, stone) base 1024 / ORM 512 / normal 512; tier 2 half of that. Results: 92 MB vs 828 MB.
10. Colour grade (Hue/Sat) and flat cloth tints are **baked into the base texture** in linear space (sRGB↔linear conversion) and the node removed. After baking, assert the base colour is still linked: `bypass()` must rewire **all** outputs of a Mix node (ShaderNodeMix has float, vector and colour results). The original code linked only the first, which turned the burgundy banner white; the export now fails loudly if a base colour is unlinked.
11. glTF carries one metallic-roughness texture (G roughness, B metallic). Packs whose metal/specular maps do not fit it get **constants**: metallic 0.5 for listed metals, 0 otherwise; roughness floor 0.6 if the source is < 0.2. Never ship an unlit metal without an environment map.
12. Metal needs an environment: the scene uses a generated equirect sky as `scene.environment` (intensity 1.1) plus one sun (2.2) at exposure 0.7 with ACES; without the environment lanterns render black.
13. Cloth materials use `DoubleSide`; alpha-cutout leaves (`MI_Vine`) use `alphaTest 0.5`, no blending.
14. Shadows: one directional light, 4096 map, `bias −0.0004`, `normalBias 0.03`; cost ≈ 2x frame time and ~20 extra shader programs.

## Collision proxies (same record format as the first island: `{x, z, w, d, h, minY, cameraOnly, oriented:{rotation,w,d}}`)
15. Walkable solids: walls, posts, counters, benches, balustrades, props. Posts of a veranda or colonnade need ≥ 1.5 m clear between them (0.68 m body + margin); the tea-house veranda has 1.49 m.
16. **Roofs are stepped `cameraOnly` bands** (top and `minY`), one per roof tier, never one box over the whole building; jetties, balconies, overhangs and arches are `cameraOnly` boxes with `minY` so the player walks under them.
17. **Cloth awnings, signs and pennants are not camera obstacles** (measured: cloth pulls the camera to 1.2–3.2 m; pennants to 3.3 m with 4–6 pops per walk). Tag them with `group: 'cloth' | 'sign' | 'pennant'` so the decision stays switchable (`P2A.camGroups`).
18. Walking ignores y for solids; the airborne head check uses `minY`. A trail between two walls is ≥ 1.5 m (the 1.34 m B04–B05 alley failed this).
19. Raised ground: ray-cast the real stair/floor geometry into a 0.2 m height field and use it as `heightAt` for **both** the controller and the camera ground test; risers ≤ 0.22 m (controller step 0.42 m). Flat tiles are analytic (+0.01).
20. Expect the unobstructed camera at 12.92 m (13.20 m minus the 0.28 m `clearDistance` padding), and compression to 3 m or less when a player stands against a facade facing away from it (porch, hall steps). That is geometry, not a bug: provide a door, portico or camera-fade rule where the design wants a player there.

## Verification (run before scaling)
21. Scale/placement test against the Blender envelopes (≤ 5 cm); orientation test; `transforms_clean` empty.
22. Route set with the real controller incl. a straight-line and a corner-cutting route per space; camera mode comparison A–E; per-obstacle camera-ray attribution (`autotest=cause`).
23. Parity renders from the same cameras in Blender and the browser; compare mean luma/warmth **and look at them**: the numeric match (23 luma points MAE) did not catch the white banners.
24. Measure counts (calls, triangles, textures, programs) and time separately; state hardware; never quote an fps without the machine.
