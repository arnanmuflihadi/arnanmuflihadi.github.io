# R0-C1C asset record

No assets, packs, textures, dependencies or tools were acquired. Approved masters and GLBs remain byte-identical; see [preservation](../../../validation/circulation-c1c/preservation.json).

The independent `validation/circulation-c1c/circulation-design.blend` derives from the approved C1B export master. Project-original C1A fountain, pavilion, furniture and jointed paving retain their design and dimensions. New geometry is limited to circulation steps, terrain-scribed gravel/stone transitions and necessary guards. Four buildings, foundation-hybrid GLB, market GLB, terrain, ridge and waterfall are preserved.

Selected existing town props are relocated in this derivative: nine-part obstructing bench, planter bed and one Quaternius tree, two ginger flowers and their seven leaf meshes. Wayfinding signs reuse original project geometry at 65% scale. The source market archive is never edited. The runtime filters only selected indexed triangles and moves the town tree's two existing instance components; disabling the proposal restores originals.

The town tree is the already licensed Quaternius shared canopy component; all upstream CC0 license files and source attribution remain under the [S2-C record](../market-street-s2c/ASSET-RECORD.md) and [C1A record](../town-square-r0c1a/ASSET-RECORD.md). Original project work is not assigned an invented third-party license. Fountain/pavilion provenance remains in the [C1B record](../town-square-c1b/ASSET-RECORD.md).

Blender coordinates are `(u,v,h)=(X−36,44−Z,Y−18.6)` metres. Supported glTF Y-up conversion is followed by one translation `(36,18.6,44)` in Three.js. Exports contain no texture references. Editable native collections and separate material-batched export collections are retained. The compact runtime metadata contains actual guard bounds; the full circulation inventory is a separate review-only JSON.

Blender MCP was genuinely used to inspect, edit, export, save and render the derivative. Browser bronze and closed-stone shadow treatment reuse C1B/S2-G conventions; no lighting or approved glass change is made. Glass B remains the development baseline, with A/C comparisons intact.
