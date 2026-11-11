# S2-G asset preservation

No source-model edits, downloads, new textures, new architecture or replacement GLBs. Blender MCP inspection confirmed the existing `validation/market-street-s2e/site-interface.blend`, unit scale 1, in Blender 5.2.3 LTS. It was not saved or edited.

All approved Blender files, source archives, GLBs, licenses, building coordinates, terrain and gameplay sources remain preserved. Original component rights and attribution remain in the [S2-C](../market-street-s2c/ASSET-RECORD.md), [S2-D](../market-street-s2d/ASSET-RECORD.md), [S2-E](../market-street-s2e/ASSET-RECORD.md) and [S2-F](../town-s2f/ASSET-RECORD.md) records.

The unchanged town body payload is 11,084,692 bytes: market 10,007,904; interfaces 527,172; hybrid foundations 543,452; invisible support reference 6,164. The exact-terrain reference is not loaded.

Only runtime copies change:

- Four original tree placements, one palm with all ten fronds, and seven individual small plants are moved onto existing natural ground. Paired trunk/crown transforms stay together; the four tree collision proxies follow their trees. No entire instancing batch is hidden or reduced.
- Ninety-one individual grass blades out of 28,063 are excluded where they cross the town's actual walking surfaces or enclosed building footprint. Four chunks receive filtered near/far index buffers; the original geometry and attributes remain intact. The existing terrain and LOD selection continue to run.
- Solid town paving/base materials use back-face shadow casting to reduce surface shadow banding. Source colors, roughness and global lighting are retained; thin foliage and glazing do not receive that policy.
- Optional B glazing uses one shared MeshStandardMaterial with low-opacity tint, front-face rendering and depth-write disabled. C reuses it for 424 glass triangles and retains the original physical material for 132 café-front triangles. A retains the original material and geometry references. No image textures are added.

`validation/town-s2g/clearance-ledger.json` identifies every changed instance/blade, original and revised coordinates, and purpose. `preservation.json` records the final byte comparison against the S2-F checkpoint. Approval of these runtime corrections does not authorize replacing glass A or public deployment.
