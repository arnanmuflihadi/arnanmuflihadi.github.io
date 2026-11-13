# AR(N)AN Urban Atlas — Claude Code instructions

@AGENTS.md

In Claude sessions, `AGENTS.md`'s `fantasy-level-design` means **`urban-atlas-level-design`** and `game-visual-qa` means **`urban-atlas-visual-qa`** (both in `.claude/skills/`). Toolkit details, versions and rollback: [docs/tooling/CLAUDE-GAME-DEVELOPMENT-SETUP.md](docs/tooling/CLAUDE-GAME-DEVELOPMENT-SETUP.md).

## Operating standard: Inspect → Build → Playtest → Visual Review → Fix → Deliver

- When implementation is requested, implement. Do not open a new planning phase, master plan or design document for a scoped change; a 5-line route/intent note in the report is enough.
- Every environment task ends with a visible, playable improvement (a reachable landmark, an explorable settlement, a working NPC interaction, a functioning discovery) — tests and docs are supporting evidence, not the deliverable.
- Before editing: make a safe baseline checkpoint (the game is largely uncommitted — ask the owner to commit/tag, or copy the touched files with SHA-256 into the phase's `validation/` folder).
- Build in small increments behind a localhost flag; playtest each in the real browser; fix defects found in the same session.
- Small, safe, in-scope corrections: just do them. Escalate destructive actions, terrain/controller/camera rewrites, new dependencies, or moving to the next phase.
- Preserve approved assets, terrain, controller, camera, renderer lifecycle, GLB cache, licenses and evidence. Never overwrite existing evidence files.
- Final report: short. What changed, URL + flags, screenshots, checks actually run, unresolved defects stated plainly, owner approval pending.

## Skill routing (load the minimum; one coordinator = these instructions)

| Task | Skills |
| --- | --- |
| Build or extend an island / environment | `urban-atlas-level-design` → `threejs-aaa-graphics-builder` (narrow refs only) → `urban-atlas-visual-qa` |
| NPC, quest or interaction | `threejs-gameplay-systems` → targeted `urban-atlas-visual-qa` (gameplay readability domain) |
| Unique Blender building or prop | asset-first check (inventory below) → `blender-image-to-3d` → `urban-atlas-visual-qa` in the real Three.js scene |
| Camera or movement problem | `threejs-gameplay-systems` + `threejs-debug-profiler` → focused QA of the affected route |
| Game UI / HUD / dialogue / journal | `threejs-game-ui-designer` → `urban-atlas-visual-qa` (desktop + 390×844) |
| Slow rendering / WebGL error | `threejs-debug-profiler` only |
| Release-style canvas or bundle check | `threejs-qa-release` (current-view mode; Urban Atlas has no `__THREE_GAME_TEST_HOOKS__`) |

Never load every game skill for one task. Never run two QA or director workflows at once. Read a skill's reference files only when its table says the task needs them.

## Hard rules for the installed third-party skills

- **Never run `threejs-gameplay-systems/scripts/create_threejs_game.py`** or any scaffold over this project. This is an existing no-bundler static site (`assets/js/vendor/three-*.module.js`); do not add Vite, TypeScript, npm packages or a new engine.
- Do not use AI asset generation (Tripo, Gemini, ElevenLabs, Blender MCP `generate_3d`, paid `import_asset`) unless the owner explicitly asks. The generator skills are intentionally not installed.
- The 10-category scorecard in `threejs-aaa-graphics-builder` is optional context; the acceptance rubric is the one in `urban-atlas-visual-qa`.

## Running and checking

- Preview: `node scripts/serve-pages-preview.mjs --root . --port 4173`. Town layers need localhost **and `dev-town=s2f`**, e.g. `http://127.0.0.1:4173/index.html?experience=adventure&dev-town=s2f&town-layout=reset-final&town-props=cc0&town-guild=r0c2&town-skyport=r0c3&town-review=1`.
- Browser: Playwright MCP (`.mcp.json`) or the desktop app's built-in browser. Blender: `blender` MCP in `.mcp.json` (Blender add-on on port 9876, safe mode on).
- Tests: `node --test tests/*.test.mjs`. Note `terrain-c1a5`, `circulation-c1c` and `town-square-c1b` rewrite evidence JSON under `validation/` — run the suite in a copy, or only when refreshing that evidence is authorized. Static audit: `node scripts/audit-static-site.mjs` (compare with the recorded baseline; 58 inherited findings as of 2026-11-11).
- Asset inventory before modelling anything: `node docs/tooling/glb-inventory.mjs assets/game`, plus `ASSET_MANIFEST.md` and each folder's `source*.json`.
