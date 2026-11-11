# Telaga Awan C1B — sources and export

Project-original fountain, jade basin, pavilion, pavers, furniture, planting, retaining walls, civic walk and guards are reused from the approved [C1A master](../../../validation/town-square-r0c1a/town-square-design.blend). No external asset, image, texture, pack or dependency was acquired.

The export contains only the square and its existing civic/highland connections. Market Street, the island and reference vegetation are excluded. Their upstream [C1A record](../town-square-r0c1a/ASSET-RECORD.md), CC0 source records, licenses and approved files remain unchanged. Original project geometry is not assigned an invented third-party license.

The independent [Blender derivative](../../../validation/town-square-c1b/town-square-export.blend) retains editable modular collections plus a separate material-batched export collection. [Export manifest](../../../validation/town-square-c1b/export-manifest.json) records component costs, real collision bounds, original floor elevations, fitted route and source cameras.

Native coordinates are `(u,v,h)=(X−36,44−Z,Y−18.6)` metres. The supported glTF Y-up export is translated `(36,18.6,44)` once in Three.js. No additional axis conversion or scale normalization is applied at runtime.

Optimization preserves 300 paver joints and their top arrises while removing redundant underside bevels. Closed stair/deck winding is corrected. A local civic-walk bow of at most 0.75 m clears the preserved market-ramp rail. The highland path is fitted to accepted C1A.5 ground with terrain-contact skirts. Existing support toes are resurveyed; floor elevations and market geometry remain unchanged.

Twelve authored PBR materials export without external texture references. The browser uses a square-only bronze material clone (metalness 0.28, roughness 0.42, emissive fill 0.14) for the existing renderer, which has no matching Blender studio environment. Closed stone uses the existing S2-G back-face shadow technique to suppress self-shadow stripes. These material clones add no lighting pass. The GLB retains its authored bronze parameters. Existing Market Street Glass A/B/C materials are preserved; C1A.5/C1B development measurements use B.

Approved masters/GLBs and prior evidence are protected by the C1B [hash checkpoint](../../../validation/town-square-c1b/before-hashes.json). The derivative and GLB were created and inspected through the live Blender MCP connection.
