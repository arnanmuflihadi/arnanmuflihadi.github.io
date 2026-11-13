# Atlas Guild R0-C2: source record

No new asset research, downloads, software installation or paid services.

The new editable `validation/atlas-guild-r0c2/atlas-guild.blend` derives from the existing new-town study `validation/atlas-guild-reset/atlas-guild.blend`, itself derived from `validation/atlas-guild-c2a/atlas-guild-design.blend`. Both reference files remain unchanged. The old C2A site coordinates, circulation and foundations are not used in the game.

Reused C2A work: research-hall walls, timber portal/trusses, sun screens, glazing, warm plaster/stone/timber materials, terracotta vocabulary, door hardware and observation-lantern components. R0-C2 compresses and broadens the lantern neck, integrates the lantern into the roof mass, replaces the old tree-cut main roof with a complete limasan roof, and adds actual editable secondary lettering and a restrained survey-compass inlay. New roof, label and emblem are project-authored Blender geometry. No external license is invented for project-original work.

Placement uses the accepted RESET-FINAL reservation only: local `(u,v)=(0,32)`, world centre `(-9.0300701, 35.5318714)`, datum **15.48 m**, Y rotation **35°** after one standard Blender Z-up to glTF Y-up conversion. The shallow plinth, direct landing and three risers fit the unchanged measured terrain. Native context is a read-only reference snapshot, not exported as a replacement landscape.

Upstream rights: [C2A component record](../atlas-guild-c2a/ASSET-RECORD.md), [S2-C components](../market-street-s2c/ASSET-RECORD.md), and the existing root `ASSET_MANIFEST.md` preserve the Kenney/Quaternius CC0 notices and source archives. The 17 CC0 prop types / 42 placements remain exactly as recorded in [population provenance](../town-population/ASSET-RECORD.md). No new font or image file is delivered; labels are mesh geometry. The native architectural scale figure is not exported as a character or NPC.

Delivery: `assets/game/atlas-guild/atlas-guild.glb`, **1,527,656 bytes**, **14,697 triangles**, **16 static geometry/material batches**, **16 materials**, **zero textures**. Authored blue-green glass uses no transmission. Native raw export is retained independently at `validation/atlas-guild-r0c2/atlas-guild.glb` (1,734,020 bytes). Existing glTF tools index identical vertices and deduplicate/prune unused resources without decimating silhouettes or altering normals, material identities or visible walkable extras.

[Export sizes and SHA256](../../../validation/atlas-guild-r0c2/export-metrics.json) · [Source checkpoint hashes](../../../validation/atlas-guild-r0c2/checkpoint.json). Native authoring/export/optimization scripts stay beside the validation file; live Blender MCP was used to modify, inspect, save, render and export the model. Browser appearance is checked separately from Cycles.
