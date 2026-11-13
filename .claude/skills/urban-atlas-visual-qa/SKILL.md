---
name: urban-atlas-visual-qa
description: "Visual QA for the AR(N)AN Urban Atlas Three.js RPG in a real browser: island composition, tropical-modern architecture, vegetation/terrain/waterfalls, character-to-building scale, third-person camera framing, lighting/materials, NPC and landmark readability. Use after building or changing any 3D environment, building, landmark, NPC placement or camera behaviour, and before calling such work done or high-quality. Not for portfolio text pages or pure logic changes."
---

# Urban Atlas visual QA

Judge what the real browser renders while a player moves through it. This skill supersedes the Codex `game-visual-qa` skill for Claude sessions and reuses its evidence notes: [browser-evidence.md](../../../.agents/skills/game-visual-qa/references/browser-evidence.md). Use `threejs-qa-release` only for its canvas-pixel/release checks and `threejs-debug-profiler` only for measured performance; do not run another QA orchestrator alongside this one.

## Art direction (the bar)

80 % contemporary Indonesian tropical architecture and landscape, 20 % restrained fantasy. Polished stylized RPG, not photoreal and not toy-like. Deep overhanging roofs (limasan/joglo-derived, terracotta or timber), raised plinths, verandas, timber screens, lime plaster, volcanic stone; dense layered tropical planting; a few floating-island and sky-port fantasy elements. Exploration readability in the spirit of Breath of the Wild / Skyward Sword — clear landmarks, silhouettes and sightlines — without copying their assets or designs.

## Fixed gameplay camera and scale (measured from code)

| Item | Value | Source |
| --- | --- | --- |
| Follow camera | FOV 60°, distance 11.8 m, +6.6 m above smoothed player, looks at player +1.25 m; pulls in to ≥0.8 m when blocked, then lifts | `assets/js/urban-atlas/camera.js` |
| Locomotion | walk 2.1 m/s, run 4.6 m/s | `assets/js/urban-atlas/player-controller.js` |
| Jump / step | launch 6.2 m/s, gravity 16.5 → apex ≈1.17 m; max step 0.42 m; body height 1.9 m | same |
| Eye height for pedestrian views | 1.65 m above actual support | existing evidence convention |

Judge from this camera first. Aerial and close-up views are supporting evidence, never the only evidence.

## Evidence rules

- Capture the real local game: `node scripts/serve-pages-preview.mjs --root . --port 4173`, then `http://127.0.0.1:4173/index.html?experience=adventure&dev-town=s2f&...`. Town/skyport/wildlife layers only load on localhost **with `dev-town=s2f`** plus their own flags; record the exact URL.
- Tools: Playwright MCP (`.mcp.json`, headed, 1280×720) or the desktop app's built-in browser. Movement must be real keyboard input (e.g. `browser_run_code_unsafe` → `page.keyboard.down('KeyW')`, wait, `up`). The town-review panel's "View …"/"Walk …" buttons are the approved reproducible cameras/routes — prefer them to ad-hoc framing.
- Read console errors every capture. Save evidence into the current phase folder under `validation/<phase>/`; `.playwright-mcp/` is scratch only. Never overwrite approved evidence — use new filenames.
- A Blender render, a GLB viewer, source code or a mockup is never "the browser render". Say which one an image is.
- Passing tests, a clean console or a pixel metric never establishes visual quality.

## Workflow (per substantial environment feature)

1. Capture the actual browser game at the feature, flags recorded.
2. Player-height view (1.65 m eye, or the gameplay camera standing at the feature).
3. Elevated composition view (aerial or "View island/oblique" preset).
4. Active movement: walk up to, around, into and away from the feature with the real controller; capture at least one frame mid-movement.
5. Compare against the approved baseline at the matched camera, resolution, quality and lighting.
6. List the **three largest visually meaningful defects**, each with an image reference.
7. Fix only defects inside the authorised scope; leave the rest listed.
8. Re-capture the same views after the fix and show before/after side by side.

Stop after two correction loops on the same defect and report the blocker instead of iterating further.

## Finding labels (use exactly one per finding)

`CONFIRMED-TECH` reproducible technical defect (clipping, floating, z-fighting, missing texture, blocked route, console error) · `VISUAL-DEFECT` meaningful quality problem a player would notice · `PREFERENCE` subjective design taste · `APPROVED-LIMIT` previously accepted limitation (cite the record) · `UNVERIFIED` not yet observed in the browser.

## Rubric (score 1–5 per domain, provisional internal observation)

| Domain | 1 | 3 | 5 |
| --- | --- | --- | --- |
| World composition — island silhouette, depth layers, skyline, landmark hierarchy | flat, no focal point | readable but generic | strong silhouette, clear primary + secondary landmarks |
| Architecture — proportions, tropical-modern cohesion, roofs, plinths, terrain/path integration | primitive boxes, floating or sunk | believable, some generic parts | authored, grounded, culturally coherent |
| Environment — vegetation variety/density, terrain materials, cliffs/water, path readability, storytelling | sparse or tiled repetition | varied, some seams | layered, purposeful, tells a story |
| Character & camera — scale vs doors/eaves, framing, obstruction, visibility while moving, intersections | scale wrong or camera blocked | acceptable with lapses | always readable, nothing clips |
| Rendering — materials, shadows, lighting, atmosphere, readability at 1280×720 | flat/noisy/missing maps | coherent | cohesive mood, clean contact shadows |
| Gameplay readability — NPC discoverability, interaction prompts, guidance, landmark purpose | player gets lost | findable with effort | player is guided without UI help |

Report each score with one line of image-backed evidence. Unobserved domains are `UNVERIFIED`, not scored. Owner target: average ≥4, no domain <3. Owner approval stays **pending** until the owner says otherwise.

## Proportion and clearance checks (measure, don't eyeball)

- Doors ≥2.1 m clear height and ≥1.0 m wide; eaves/canopies over walkways ≥2.4 m; storeys 3.0–3.6 m.
- Steps ≤0.42 m rise or the player cannot climb; ledges meant to be jumped ≤1.1 m.
- Walkable trails ≥1.5 m, settlement streets ≥3 m; no gap the camera's 0.8 m minimum cannot frame.
- Buildings sit on support: no visible gap or >5 cm float at the plinth; no roof or prop intersections at player height.
- Character 1.9 m must read as human against doors, benches and railings in the gameplay camera.

## Scope and rollback

Work only inside the authorised feature and phase. Before editing, confirm a baseline checkpoint exists (commit, tag or copied files with SHA-256). Preserve approved terrain, controller, camera, renderer lifecycle, GLB cache, licenses and prior evidence (`tests/helpers/production-preservation.mjs`). Each fix must be revertible by removing its flag or restoring the listed files.

## Report (keep it short)

URL + flags · images (before/after pairs) · rubric table · top three defects with labels and status · console/test results actually run · what remains `UNVERIFIED` · owner approval: pending.
