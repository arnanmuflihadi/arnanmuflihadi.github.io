# R0-D2 Gate B · isolated dragon study

**Status: incomplete visual and animation study; not ready for Gate C.** The custom model does not yet match the approved concept's organic anatomy or painterly finish. The wing spars still read as rigid tubes, the head and saddle are too simple, and several joints are visibly assembled from separate forms. The four rendered views should be judged as a study, not a finished creature.

## Files

- `dragon-master.blend` — editable Blender copy containing scene `R0-D2 | Dragon study`, 54 separately editable meshes and an 18-bone armature. Because Blender saved a copy of the open document, the copy also contains the pre-existing C3.1 scene; the approved original file was not saved over. The 1.65 m mannequin and ground belong to a separate reference collection and are excluded from GLB.
- `dragon-batched.glb` — 392,804 bytes, 10,442 triangles, seven material primitives, one skin, 18 joints, no externally referenced texture images. Batching was performed on temporary duplicates; the editable master retains components.
- `01-three-quarter.png`, `02-side.png`, `03-front.png`, `04-flight.png` — actual Blender Cycles renders, not concept art. `05-browser-flight.png` — real isolated Three.js asset viewer. `index.html` is an independent review page; it does not modify or load into the production game.
- `build_dragon.py`, `refine_dragon.py`, `export_dragon.py`, `verify-export.mjs` and `export-inventory.json` document the authored geometry and checks. New geometry and materials were created for this project; no external creature model or texture was imported.

## What works, and what does not

The model has four legs, two independently weighted wings, a long tail and a saddle shape. Its rest-pose span is approximately 9.2 m and nose-to-tail length approximately 7.5 m, measured in Blender. The mannequin is a scale reference, not the actual explorer or proof of a usable saddle.

Five named skeletal animation studies export: Idle_Hover, Takeoff_Preparation, Wing_Powered_Flight, Gentle_Bank and Approach_Landing. The browser loads and plays them. They demonstrate changing wing rotations, but they are basic cycles: they do **not** demonstrate convincing takeoff, trajectory, landing, leg placement, rider motion or tail follow-through. Boarding and dismount clips were not created. No landing location, skyport clearance, guard crossing, rider contact or gameplay route has been validated.

## Checks

- `node validation/skyport-r0d2-gate-b/verify-export.mjs` passed structural GLB, skin, weight attributes, flight-channel variation and triangle-count checks.
- `node --test tests/skyport-boarding.test.mjs`: 2 passed; D1 is preserved.
- Actual isolated browser viewer: seven draw calls and 10,442 submitted triangles in its displayed camera; this is not a matched game benchmark and does not include a representative island or shadow pass. No mobile test or frame-time comparison is claimed.
- Live Blender MCP used for authoring, inspection, export and four renders. `dragon-master.blend` was saved as a copy. A separate headless Blender reopen attempt crashed in this environment, so independent reopen verification is not claimed.

## Preservation and rollback

No production source, existing asset, game layout, character controller or renderer was changed. No R0-D2 gameplay integration was performed. The prior D1 toggle remains unchanged. To remove this study, delete only the `validation/skyport-r0d2-gate-b/` directory after preserving any desired evidence; original C3.1 and D1 files are not part of it.

Owner visual review is pending. Gate C is not approved or started.
