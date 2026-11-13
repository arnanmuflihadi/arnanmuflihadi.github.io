# Stylized Dragon · isolated jade recolor

**Status:** ready for a preliminary owner color/model review, not approved for gameplay integration. This is a recolor of a downloaded model, not a complete rideable mount.

## Source and attribution

[Stylized Dragon](https://sketchfab.com/3d-models/stylized-dragon-97d00c182fa24fa4838493c41ad8e52c) by [Stan (@Stas_SayHallo)](https://sketchfab.com/Stas_SayHallo), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The downloaded GLB identifies the author, source and license in `asset.extras`. **Changes:** the red body texture was recolored muted jade/teal; the model was exported again from Blender. Preserve this credit, license link and change notice when distributing the derivative. The creator describes the model as made while following a CG Cookie course; the listing does not independently establish the full rights chain.

## Files and inspection

- `stylized-dragon-stan-original.glb`: unchanged Sketchfab 1k-texture download, 5,641,080 bytes; SHA-256 `427e832bb466b7eba096ffc056b9cac6897edc7c4b3fa182003c2deec3c5ac57`.
- `stylized-dragon-jade-review.blend`: editable Blender scene with packed textures, rig, animation tracks, camera and studio lights.
- `stylized-dragon-jade.glb`: isolated derivative, 4,675,680 bytes; SHA-256 `104c2f73158ed381ae0f2e99d43492f8c0de256d5a1a7dceaf82bf5e7d5b5a19`. Attribution and change notice are included in glTF asset metadata.
- `original-three-quarter.png` and `jade-three-quarter.png`: actual Blender renders using the same camera, pose and lighting. `jade-front.png`, `jade-side.png` and `jade-flight-frame12.png` provide additional views. These are studio renders, not browser or in-game screenshots.

The exported GLB contains 57,936 triangles, two mesh primitives, two materials, three embedded images and a skin with 99 joints. It retains the named `Wing flaps`, `head turn`, and `head turn/wing flaps` clips. Blender MCP reimported the derivative and showed a different evaluated wing span at frames 1 and 12; this verifies deformation, not animation quality or gameplay suitability. A structural GLB check passed for the embedded images, skin, clips and attribution. The exporter warned that multiple image nodes share a texture sampler; the browser appearance remains to be checked.

## Remaining limitations

No saddle, rider, boarding, landing or dismount animation has been added. The source's rest-pose body is only about 3 m long in the imported scene; rider scale and skyport clearances are untested. Its 57,936 triangles are substantially above the earlier 4,562-triangle preview, and runtime draw calls and frame times are unmeasured. Browser visual verification was not possible because local browser use is disabled in the current Work settings. This palette is predominantly teal; a separate warm-stone underside was not authored.

The original game and R0-D1 preview were not changed. Gate C integration and production deployment remain unauthorized. The isolated files can be removed without changing the existing game.
