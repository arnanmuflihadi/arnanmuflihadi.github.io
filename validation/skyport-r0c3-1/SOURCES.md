# C3.1 selected provenance

No downloads, external asset search, installations or new textures.

- Original C3 source: `validation/skyport-r0c3/pelabuhan-awan.blend` and `assets/game/skyport/pelabuhan-awan.glb`, retained unchanged. Their SHA256 is recorded in [baseline.json](baseline.json).
- Reused actual meshes: C3 `Reused pavilion timber pier`, `Reused pavilion stone shoe`, and `Kenney / canopy lantern / lampSquareCeiling`. Timber/shoes are project-authored civic components. The fixture derives from [Kenney Furniture Kit](https://kenney.nl/assets/furniture-kit), `source-assets/town-population/furniture/Models/GLTF format/lampSquareCeiling.glb`, **CC0-1.0**, retained [license](../../source-assets/town-population/furniture/License.txt). Modification and redistribution are permitted; attribution is optional; Kenney remains credited. Exact original source hashes remain in [C3 sources](../skyport-r0c3/sources.json).
- Reused material definitions: C1 oiled timber, C1 weathered bronze and C3 jade enamel. The detail GLB has three material slots; runtime maps them to the actual existing C3 material objects. Zero additional runtime definitions or textures.
- New project-authored geometry: paired closed docking eyes/cleats, compact beacon cap and static wind sleeve, four north-aligned bronze inlay ticks. No invented external license is assigned to original work. No rope asset was available locally; rope detail was omitted.

The independent [Blender derivative](pelabuhan-awan-polish.blend) retains the base as context and separate editable additions/export collections. Only new detail geometry is exported to [skyport-details.glb](skyport-details.glb); no C3 base mesh is re-exported or replaced. Identity transforms, metres, supported Blender Z-up to glTF Y-up conversion and the existing C3 root transform are preserved.
