# Blender environment-art setup

2026-11-02. Setup only; production website and town were not edited.

## Installed configuration

- Local macOS 27.2 (26B123), Darwin arm64; not a remote container.
- Blender **5.2.3 LTS**, official Apple Silicon DMG, installed at `/Applications/Blender.app`.
  Homebrew exists but `brew install --cask blender` failed on the unaccepted Xcode
  license. No license was accepted automatically. The official DMG was used instead.
- Existing uv/uvx **0.11.15**, reused at `/Users/arnanmuflihadi/.local/bin/uvx`.
- Existing Codex CLI **0.144.1**; MCP for Blender package **2.2.6** from PyPI.
- Add-on installed by `uvx mcp-for-blender install-addon`, with explicit Blender
  5.2 directory: `~/Library/Application Support/Blender/5.2/scripts/addons/blender_mcp.py`.
  Enabled using Blender's preferences API and saved; a separate Blender process
  confirms that preference persists.
- Codex stdio server `blender`: absolute uvx path above, argument `mcp-for-blender`.
  Environment: `BLENDER_HOST=localhost`, `BLENDER_PORT=9876`,
  `BLENDER_MCP_SAFE_MODE=1`, `DISABLE_TELEMETRY=true`. Installed source implements
  safe mode. No paid generation services or external asset packs were configured.
- Config backup: `/Users/arnanmuflihadi/.codex/config.toml.blender-backup-20261102-163903`.
  Existing server entries were preserved. `codex mcp list` confirms registration.
- Skill: `.agents/skills/blender-environment-art/SKILL.md`; official skill validator
  passes. Existing fantasy-level-design and game-visual-qa skills are preserved.

Sources reviewed: [MCP README](https://github.com/ahujasid/mcp-for-blender),
[Homebrew cask](https://formulae.brew.sh/cask/blender),
[official downloaded DMG](https://download.blender.org/release/Blender5.2/blender-5.2.3-macos-arm64.dmg).

## Acceptance results

| Check | Result | Evidence / limit |
|---|---|---|
| Blender installed and launches | PASS | Headless verified; native app inventory now confirms Blender is running |
| Blender Python works | PASS | bpy reports 5.2.3 LTS; created and rendered test scene |
| MCP server registered | PASS | `codex mcp get blender` and `codex mcp list` |
| Add-on enabled | PASS | Saved preferences; confirmed in separate Blender process |
| Codex communicates with live Blender MCP | PASS | Live status and scene queries; protocol 15, matching add-on 1.8 |
| Codex modifies objects through MCP | PASS | Created scene, materials, camera and cube; moved cube to (-3.5, -2, 0.5) Blender coordinates |
| Codex retrieves scene image through MCP | PASS | `look` camera/material and viewport/solid images returned successfully |
| Skill discoverable | PASS | Correct repository discovery path and validated YAML; new-session activation pending |
| Test .blend saved | PASS | Live MCP saved mcp-validation.blend; independently reopened |
| Test GLB exported | PASS | Live MCP active-scene export; Three.js loader parses 10 meshes, 15,516 bytes |
| Existing website untouched | PASS | SHA-256 comparison of assets, source assets, root HTML and existing skills |

After Codex restarted and Blender opened, the local server became available on
127.0.0.1:9876. Initial connection attempts failed during startup; subsequent live
MCP status, scene, execution and image calls succeeded. Telemetry consent is false;
all asset libraries and generation providers report off. Native computer capture
still has ScreenCaptureKit error -3811, but Blender MCP viewport capture works.
No manual panel action or additional restart is currently required.

## Test artifacts

All paths below are under
`/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/blender-setup/`:

- `validation.blend` — native test project, metre scale, named collections.
- `validation.glb` — Y-up glTF export; 12 m ground, 3.3 m structure, 1.8 m reference.
- `validation-render.png` — actual offline Blender render, not MCP evidence.
- `create_validation.py` — reproducible offline scene creation.
- `glb-verification.json`, `preservation.json`, `mcp-list.txt` — verification records.

The final **live MCP** proof is separate from those initial offline artifacts:

- `mcp-validation.blend` — MCP-created scene; original default scene preserved.
- `mcp-validation.glb` — corrected active-scene-only export, 10 meshes / 15,516 bytes.
- `mcp-validation-render.png` — actual Cycles render executed through MCP.
- `mcp-viewport.png` — actual solid viewport image retrieved through MCP `look`.
- `mcp-verification.json` — existing Three.js loader verification; 12 × 3.5 × 12 m
  bounds, correctly converted moved-cube location (-3.5, 0.5, 2) in glTF Y-up.

The scene contains a ground, simple plaster structure, real 1.6 × 2.2 m door opening,
shading roof, materials, scale marker, camera and light. Original custom geometry;
no downloaded models or attribution obligations added. Blender Z-up → glTF Y-up
conversion is applied once. GLB bounds are x/z ±6 m, y −0.2 to 3.3 m; the ground
slab extends below zero intentionally. No in-browser render verification is claimed.

## Reopen the verified workflow

1. Blender MCP tools are available; the live tests are complete.
2. Open mcp-validation.blend after preserving any unsaved work.
3. In Blender: Edit → Preferences → Add-ons → confirm **Interface: MCP for Blender**.
4. Hover the 3D Viewport, press **N**, choose **MCP for Blender**. Check port 9876;
   use **Connect to MCP server / Start MCP Server** if not running. Keep local access.
5. In Codex invoke `get_addon_status`, `get_scene_info` and `look` to inspect it.
   Use `execute_blender_code` for authorized edits in isolated review files.

Useful terminal commands:

```sh
/opt/homebrew/bin/codex mcp list
/Users/arnanmuflihadi/.local/bin/uvx mcp-for-blender --help
/Applications/Blender.app/Contents/MacOS/Blender --background --python validation/blender-setup/create_validation.py
```

Do not run a second stdio server alongside Codex unnecessarily. Do not begin town
production or modify the Three.js website during this remaining setup verification.
