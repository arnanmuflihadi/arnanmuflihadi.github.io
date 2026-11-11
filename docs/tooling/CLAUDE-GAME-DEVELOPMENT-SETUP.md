# Claude Code game-development setup — AR(N)AN Urban Atlas

Set up 2026-11-11 by Claude Code (Opus 5.5). Tooling only: no game code, asset, GLB, `.blend`, terrain, camera, NPC or quest was changed, nothing was committed or deployed.

## 1. Inventory found before installation

| Item | State at audit |
| --- | --- |
| Game code | Lives **uncommitted** in this folder on branch `codex/floating-atlas-r0` (~106 modified/untracked entries: `assets/js/rpg`, `floating-atlas`, `tests/`, `validation/`, `.agents/`, `AGENTS.md`). Claude worktree sessions branch from the last commit and **cannot see the game**. |
| Project `CLAUDE.md`, `.claude/skills/`, `.mcp.json` | None. |
| Global `~/.claude/skills` | `context7-mcp`, `resume-tailoring` (untouched). |
| Codex project skills (`.agents/skills/`) | `game-visual-qa`, `fantasy-level-design`, `blender-environment-art`. Claude Code discovers skills from `~/.claude/skills`, `.claude/skills` and plugins, not `.agents/skills`, so these were not available to Claude. They are kept unchanged and referenced by the new Claude skills. |
| Claude plugins | Superpowers, frontend-design, engineering/PM/academic packs, ui-ux-pro-max. No game-development plugin. |
| Claude MCP servers | Only `context7`. No Blender or Playwright MCP. |
| Codex MCP | `blender` = `uvx mcp-for-blender` (safe mode, telemetry off, port 9876); `node_repl` browser. |
| Blender | `/Applications/Blender.app` running with the MCP add-on listening on `127.0.0.1:9876`. |
| Browser tooling | Desktop-app built-in browser, Claude in Chrome; Playwright Chromium builds cached in `~/Library/Caches/ms-playwright`. No `package.json` / `node_modules` in the project. |
| Test & evidence tools | `node --test tests/*.test.mjs` (33 files), `scripts/audit-static-site.mjs`, `scripts/serve-pages-preview.mjs`, `scripts/record-*.mjs`, town-review "View …/Walk …" presets in the game. |

## 2. Installed and verified

| Capability | Location | Source @ commit | Verification |
| --- | --- | --- | --- |
| `threejs-gameplay-systems` | `~/.claude/skills/` | [majidmanzarpour/threejs-game-skills](https://github.com/majidmanzarpour/threejs-game-skills) @ `8286774b22a2566bf894dbc825825c16921866af` (MIT) | Files byte-identical to source (`diff -rq`); Claude Code listed it as an invocable skill in the installing session. |
| `threejs-aaa-graphics-builder` | same | same | same |
| `threejs-game-ui-designer` | same | same | same |
| `threejs-debug-profiler` | same | same | same |
| `threejs-qa-release` | same | same | same; inspector needs `playwright` resolvable and only works in current-view mode here (no `__THREE_GAME_TEST_HOOKS__`). |
| `blender-image-to-3d` | same | [majidmanzarpour/blender-game-skills](https://github.com/majidmanzarpour/blender-game-skills) @ `f0ef29385a03de139957e6f700b801cdc00b7e29` (MIT) | Byte-identical; discovered live. Scripts reviewed: bpy/Pillow only, no network or deletion calls. Not run (no modelling during setup). |
| `urban-atlas-visual-qa` (new) | `.claude/skills/` | Project-local, 77 lines | Frontmatter valid; discovered live by Claude Code (listed as invocable skills in the installing session). |
| `urban-atlas-level-design` (new) | `.claude/skills/` | Project-local, 37 lines | Same as above (discovered live). |
| Project instructions | `CLAUDE.md` | New; imports `@AGENTS.md` | Routing and build-first standard (section 9). |
| Playwright MCP | `.mcp.json` → `npx -y @playwright/mcp@0.0.85 --isolated --viewport-size 1280x720` | [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) 0.0.85 (Apache-2.0) | MCP handshake + real game run (section 6). |
| Blender MCP | `.mcp.json` → `uvx mcp-for-blender==2.2.7`, safe mode, telemetry off | [ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp) 2.2.7 (same package Codex uses) | MCP handshake + read-only scene query (section 5). |
| GLB inventory tool | `docs/tooling/glb-inventory.mjs` | New, read-only | Ran on `assets/game`; triangle counts match `ASSET_MANIFEST.md` (77,876 / 14,697 / 14,600). |

Installed by copying the pinned skill folders (`rsync`), **not** with the upstream `install.sh` (it installs all nine skills including paid generators) or `npx skills`. Each installed folder carries `LICENSE.upstream`; `~/.claude/skills/.urban-atlas-installed-skills` records the commits.

## 3. Evaluated and not installed

| Candidate | Decision and reason |
| --- | --- |
| `threejs-game-director` | Excluded: a second coordinator. It requires reading all five production skills for broad work, keeps going "until the bar is met" (conflicts with `AGENTS.md` phase stops), and its credential probe sources your shell profiles. `CLAUDE.md` routing replaces it. Installed siblings reference director files only for excluded features: credential probe, asset recovery, and evidence-manifest state mode. |
| `threejs-3d-generator`, `threejs-image-generator`, `threejs-audio-generator` | Excluded: they need Tripo / Gemini / ElevenLabs keys and paid credits. |
| awesome-gamedev-agent-skills @ `dcf3bbbb` (Apache-2.0, 78 skills) | None installed. `level-design` overlaps the project skill; its metrics-first, critical-path and blockout principles were absorbed. `game-feel` is covered by `threejs-gameplay-systems/references/game-feel.md`, which is Three.js-specific. `camera-systems` is Godot/Unity code, and spring-arm pull-in already exists in `camera.js`. `rpg` is mostly stats/XP; quest events already exist. `performance-optimization` overlaps `threejs-debug-profiler`. The `threejs-*` web skills overlap the graphics skill and the existing loader. All Unity, Unreal, Godot, Phaser, multiplayer and monetization skills were excluded. |
| Xyloforge/claude-game-skills @ `6ee94d9f` (MIT) | Excluded: `game-detail-bar` is a 624-line multi-genre checklist (expensive on every invocation); `game-asset-pipeline` targets 2D sprites and image generation. |
| shipshitgames/skills @ `e4d7d2cf` (MIT) | Excluded: tied to `@shipshitgames/engine`. Techniques adopted from `playwright-game-testing`: real-gesture clicks, held keys, and in-rAF or `preserveDrawingBuffer` canvas capture. |
| Bulugulu/game-qa @ `41c54cc4` (MIT) | Excluded: a six-skill multi-agent QA framework whose bootstrap copies a TS runner and adapter into the project. Its pass/soft-pass/fail/unverified labelling informed the finding labels in `urban-atlas-visual-qa`. |
| Codex `game-visual-qa`, `fantasy-level-design` | Not copied or symlinked into Claude, to avoid competing QA and level skills. The Claude skills link to their reference files. |
| Codex `blender-environment-art` | Not ported: its rules (preserve originals, Z-up → Y-up once, verify GLB in Three.js) are covered by `blender-image-to-3d` plus the visual-QA rule. Codex keeps using it. |

## 4. Exact sources

Fetched 2026-11-11 by shallow `git clone`; nothing from them was executed. Commits are as listed in sections 2–3. The MCP servers resolve to `@playwright/mcp@0.0.85` (reports Playwright 1.66.0-alpha-2026-11-09) and `mcp-for-blender==2.2.7` (reports server 1.30.0).

## 5. Blender MCP verification (2026-11-11, actual)

The MCP stdio handshake against the `.mcp.json` entry listed 9 tools: `get_addon_status`, `disable_telemetry`, `get_scene_info`, `execute_blender_code`, `record_trajectory_feedback`, `look`, `generate_3d`, `search_assets`, `import_asset`. Read-only `get_scene_info` returned the open scene: 19 objects, 2 armatures, 4 cameras, including the "Pelabuhan / C1 …" skyport meshes and `D1C_Camera` from the dragon-mount feasibility study. Nothing was modified or saved. `generate_3d` and paid `import_asset` are barred by `CLAUDE.md` unless you ask for them.

## 6. Browser MCP verification (2026-11-11, actual)

Preview: `node scripts/serve-pages-preview.mjs --root . --port 4173`.

- Plain adventure URL (`project=transit`): real WebGL forest-trail render with the explorer; zero console errors or warnings.
- `…?experience=adventure&dev-town=s2f&town-layout=reset-final&town-props=cc0&town-guild=r0c2&town-skyport=r0c3&town-review=1`: skyport spawn rendered. After a real click and holding `KeyW` for 2.5 s (`browser_run_code_unsafe`), the explorer walked to the Pelabuhan Awan gate with the camera following (51 % of pixels changed). At 390×844 the layout rendered with touch controls. Zero console errors or warnings. Contact sheet: [playwright-smoke-2026-11-11.png](playwright-smoke-2026-11-11.png).
- **Unverified observation:** the URL with the full stack (`…&town-skyport-polish=r0c3-1&wilderness=r0f1&wildlife=r0f2&nature=r0f2`) stayed blank white after 12 s, with no console errors and a timed-out wait and click. Not investigated (tooling task). Retest it before relying on that flag combination.
- Not exercised in the smoke test: NPC dialogue, a full walking route with collision, or before/after comparison. The tools for these (`browser_click`, held keys, review-panel "Walk …" presets, screenshots) were shown to work.
- The headed browser uses the real GPU. Headless Chromium falls back to software WebGL, so do not use headless captures for performance numbers.
- Screenshots go to `.playwright-mcp/` under the session's working directory. Treat it as scratch and copy evidence into `validation/<phase>/`. Consider adding `.playwright-mcp/` to `.gitignore`; that file was left untouched.

## 7. Asset-first discovery workflow

1. Check the local library first: `node docs/tooling/glb-inventory.mjs assets/game`, `ASSET_MANIFEST.md`, each folder's `source*.json` / `LICENSE.txt`, and the archives in `source-assets/`.
2. If nothing fits, look for CC0 sources in this order: Quaternius, Kenney, Poly Haven (models and textures), then Poly Pizza (check each item's licence: CC0 vs CC-BY). Sketchfab and itch.io only with an explicit per-item licence that allows redistribution in a public web build. Never ripped or proprietary game assets, no purchases without your approval, and no whole-collection downloads.
3. Record per asset: name, creator/source URL, licence and attribution terms, local file, triangles/textures/clips (from the inventory tool), intended use, and style fit. Store it in that asset folder's `source.json`, following the existing pattern.
4. Use Blender (`blender-image-to-3d`) only when no licensed asset fits, and verify the exported GLB in the real Three.js scene.

Current inventory (read-only measurement, 2026-11-11):

| File | KB | Tris | Mat/Tex | Clips | Source / licence | Use / style fit |
| --- | ---: | ---: | --- | --- | --- | --- |
| `architecture-r0b1/components.glb` | 75 | 804 | 3/2 | open, close | Kenney Modular Buildings + Building Kit, CC0 | modular doors/windows; neutral, needs tropical dressing |
| `architecture-r0b1/transit-kingdom.glb` | 5,904 | 77,876 | 24/12 | — | Project-original (Blender) + Kenney CC0 parts | R0-B1 architecture prototypes |
| `atlas-guild/atlas-guild.glb` | 1,492 | 14,697 | 16/0 | — | Project-original Blender derivative ([record](../urban-atlas/atlas-guild-r0c2/ASSET-RECORD.md)) | civic landmark; on-style |
| `skyport/pelabuhan-awan.glb` | 714 | 14,600 | 8/0 | — | Project-original + Kenney Furniture Kit CC0 ([record](../urban-atlas/skyport-r0c3/ASSET-RECORD.md)) | skyport landmark; on-style |
| `skyport/boarding/dragon.glb` | 255 | 4,562 | 1/1 | Flying_Idle, Fast_Flying +6 | Quaternius Ultimate Monsters, CC0 | anatomy judged insufficient for riding (validation/dragon-*) |
| `characters/urban-explorer/urban-explorer.glb` | 1,544 | 10,202 | 10/0 | Idle, Walk, Run | Quaternius Ultimate Modular Characters, CC0 | player |
| `characters/urban-explorer/jump-animations.glb` | 261 | 0 | — | JumpStart/Air/Land | Quaternius Universal Animation Library, CC0 | player jump |
| `phase3/city-resident.glb` | 1,159 | 5,776 | 9/0 | Idle, Interact, Run, Walk, Wave | Quaternius Modular Characters, CC0 | NPC base |
| `phase3/mosskeeper.glb` | 487 | 6,044 | 1/1 | Idle, Walk, Run, Attack, Hit, Defeat | Quaternius Ultimate Monsters, CC0 | creature |
| `phase3/explorer-actions.glb` | 609 | 0 | — | Attack1/2, Guard, Dodge, Hit, Defeat | Quaternius, CC0 | combat clips |
| `scenery/architecture-library.glb` | 5,254 | 90,100 | 12/19 | — | Quaternius Downtown City MegaKit (free), CC0 | urban kit; contemporary, heavy |
| `scenery/city-building.glb` | 2,548 | 18,344 | 10/19 | — | Quaternius Downtown City MegaKit, CC0 | generic city; weak tropical fit |
| `scenery/canopy-tree.glb`, `fern.glb` | 702 / 102 | 6,265 / 288 | 2/3, 1/1 | — | Quaternius Stylized Nature MegaKit, CC0 | vegetation |
| `scenery/city-planter.glb` | 444 | 118 | 2/6 | — | Quaternius Downtown City MegaKit, CC0 | street prop |
| `nature-r0f2/*.gltf` (3) | 41 | 600 | 1–2 each | — | Quaternius Ultimate Stylized Nature, CC0 | bushes/flowers |
| `town-population/props.glb` | 114 | 1,850 | 8/1 | — | Kenney Furniture + Food kits, CC0 (16 props) | market/town props |
| `wildlife-r0f2/{cow,deer,fox}.gltf` | ~3,000 each | 1,848–2,450 | 5–7/0 | Idle, Eating, Gallop … (12–13) | Quaternius, CC0 | ambient wildlife; large embedded animation buffers |

## 8. Visual QA workflow and rubric

Defined in `.claude/skills/urban-atlas-visual-qa/SKILL.md`:

- **Evidence:** a real browser with the URL and flags recorded, real keyboard movement, and console errors read.
- **Workflow:** player-height view, elevated view, mid-movement frame, matched baseline, top three defects, scoped fix, matched re-capture. At most two correction loops per defect.
- **Finding labels:** `CONFIRMED-TECH`, `VISUAL-DEFECT`, `PREFERENCE`, `APPROVED-LIMIT`, `UNVERIFIED`.
- **Rubric:** 1–5 in six domains (world composition, architecture, environment, character & camera, rendering, gameplay readability), with anchored 1/3/5 descriptions. Owner target is an average of at least 4 with no domain below 3. Scores are always provisional, and owner approval stays pending.
- **Measured checks:** doors at least 2.1 m, eaves at least 2.4 m, steps at most 0.42 m, trails at least 1.5 m and streets at least 3 m, no plinth float above 5 cm, and character-scale readability at FOV 60° and 11.8 m.

## 9. Task-to-skill routing

| Task | Load |
| --- | --- |
| New island / environment | `urban-atlas-level-design` → `threejs-aaa-graphics-builder` → `urban-atlas-visual-qa` |
| NPC / quest interaction | `threejs-gameplay-systems` → targeted `urban-atlas-visual-qa` |
| Unique Blender building | inventory check → `blender-image-to-3d` → `urban-atlas-visual-qa` in Three.js |
| Camera problem | `threejs-gameplay-systems` + `threejs-debug-profiler` → focused route QA |
| Game UI | `threejs-game-ui-designer` → `urban-atlas-visual-qa` (desktop + 390×844) |
| Slow rendering | `threejs-debug-profiler` only |
| Release / canvas check | `threejs-qa-release` (current-view mode) |

The coordinator is `CLAUDE.md` itself: always loaded and costing nothing to invoke. No director skill and no parallel QA orchestrators.

## 10. Configuration changes and rollback

| Change | Rollback |
| --- | --- |
| `~/.claude/skills/{threejs-gameplay-systems,threejs-aaa-graphics-builder,threejs-game-ui-designer,threejs-debug-profiler,threejs-qa-release,blender-image-to-3d}` and `~/.claude/skills/.urban-atlas-installed-skills` added | `rm -rf` those seven paths |
| `.mcp.json` (new) | delete it |
| `CLAUDE.md` (new) | delete it |
| `.claude/skills/urban-atlas-visual-qa/`, `.claude/skills/urban-atlas-level-design/` (new) | delete them |
| `docs/tooling/` (this file, `glb-inventory.mjs`, smoke contact sheet) | delete the folder |

No existing file was edited. `~/.claude/settings.json`, `~/.codex/config.toml`, `AGENTS.md`, `.agents/skills/`, `.gitignore` and all game files are unchanged. No npm, pip or other dependency was added to the project. Upgrading a skill means re-cloning at a new commit, reviewing the diff, and replacing the folder.

## 11. Known limitations and security notes

- **Biggest risk: the game is uncommitted.** One bad edit or `git checkout` could lose weeks of work, and Claude worktree sessions start without the game. Commit or tag a baseline before the next build session.
- **Baseline checks**, run on an isolated copy because three tests rewrite `validation/*/height-verification.json` and `controller-routes.json`:
  - Tests: 146/148 pass. Two **inherited** failures (`architecture-r0b1.test.mjs:42`, `town-layout.test.mjs:20`) come from `tests/helpers/production-preservation.mjs`. `assets/js/floating-atlas/entry.js` (modified 06:18, before this session) no longer matches the S2-F authorization hash, and `terrain.js`, `experience-controller.js` and `living-atlas-controller.js` also differ from `production-baseline.json`. These look like out-of-date preservation records after the authorized F1/F2 passes; for the owner to reconcile.
  - Static audit: 58 findings, the same count as the recorded `docs/town-composition-review/static-audit.txt` (inherited).
- Project skills were discovered live; routing (choosing the right specialists) was not exercised in a fresh session because the `claude` CLI OAuth session had expired.
- Project MCP servers in `.mcp.json` must be approved the first time a session starts in this folder. They load only in new sessions.
- `browser_run_code_unsafe` runs arbitrary Playwright code; use it only against the local preview.
- `threejs-qa-release`'s inspector needs `playwright` resolvable from the project. The project has no `package.json`; use `npx -p playwright@<ver> node …` or Playwright MCP instead of adding a dependency.
- Blender MCP safe mode restricts `execute_blender_code` imports to bpy/bmesh/mathutils-type modules. Keep it on.

## 12. Recommended minimum setup for Island 2

1. Commit or tag the current Transit Kingdom state, then start Island 2 work in a session on this folder or on a worktree from that commit.
2. Load `urban-atlas-level-design`. Write a 5-line route note, then build a flag-gated blockout reachable from the skyport.
3. Dress the island from the inventory first: Quaternius/Kenney CC0 and existing project-original buildings. Use `blender-image-to-3d` only for a signature landmark that nothing fits.
4. Load `threejs-aaa-graphics-builder` only for its `technical-art.md` budgets and `authoring-recipes.md` lighting notes.
5. Close every increment with `urban-atlas-visual-qa`: Playwright MCP, real walking, six-domain rubric, top three fixes in the same session.
6. Use `threejs-debug-profiler` when frame time or draw calls regress, and run the regression suite in a copy.
