---
name: blender-environment-art
description: "Use for Blender-based 3D environment creation, architectural asset assembly, material editing, scene inspection, and game-ready GLB export for AR(N)AN Urban Atlas."
---

# Blender environment art

Blender is the authoritative environment-art workspace. Inspect the current .blend and live MCP connection before editing; registration alone does not prove connectivity. Preserve originals and save reviewable versions.

- Reuse verified licensed architectural assets before generating complex geometry. Record source URLs, filenames, licenses and attribution requirements alongside exports.
- Preserve metre scale and coordinate alignment. Blender is Z-up; export glTF with its supported Y-up conversion. Inspect the exported bounds, ground origin and orientation in Three.js rather than applying conversion twice.
- Separate Buildings, Streets, Landscape, Props and Collision References into collections. Collision references must be distinguishable from visible export geometry.
- Work on small reviewable sections. Prioritize composition, entrances, connected public space and architectural coherence over object count. Reuse $fantasy-level-design for settlement planning.
- Use actual Blender MCP scene inspection, geometry queries and viewport/render tools. If unavailable, mark the connection unverified and record restart/manual steps; standalone bpy success is not MCP verification.
- Render aerial, pedestrian-height (1.65 m above support) and architectural-detail views. Reuse $game-visual-qa for browser inspection; distinguish technical checks from owner visual approval.
- Export optimized GLB with intentional transforms, normals, material slots and texture sizes. Check geometry, scale, orientation, ground alignment, collision references and missing textures after export.
- Blender shaders, lighting and renders do not transfer identically to the browser. Verify the actual GLB in an isolated Three.js validation scene before production integration.
- Never modify the production Three.js game without explicit approval. Setup authorization does not authorize town production. Preserve terrain, gameplay, existing skills, manifests and source licenses.
