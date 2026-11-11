---
name: urban-atlas-level-design
description: "Lightweight level design for the AR(N)AN Urban Atlas floating-island RPG: placing or changing landmarks, settlements, trails, forest/highland/waterfall areas, NPC and discovery locations, exploration rewards and routes on Transit Kingdom or a new island. Use before and while building such spaces in Three.js. Not for asset-only modelling, UI, or portfolio pages."
---

# Urban Atlas level design

**Core rule: a location is not complete until the real player can reach it, interact with its intended content, and return safely** — verified with the actual controller in the browser, not from an aerial screenshot or a plan.

This replaces the Codex `fantasy-level-design` skill for Claude sessions; its project notes remain valid: [project-context.md](../../../.agents/skills/fantasy-level-design/references/project-context.md). Pair with `urban-atlas-visual-qa` for evidence and `threejs-gameplay-systems` only for controller/interaction code.

## Player metrics (design every dimension in these units)

Walk 2.1 m/s · run 4.6 m/s · max step 0.42 m · jump apex ≈1.17 m · body 1.9 m · camera 11.8 m behind / +6.6 m, minimum pull-in 0.8 m, FOV 60° (`assets/js/urban-atlas/player-controller.js`, `camera.js`). Trails ≥1.5 m, streets ≥3 m, doors ≥2.1 m. A 100 m trail is ~48 s walking / ~22 s running — keep main destinations within 30–60 s of a landmark sightline.

## Workflow (small, build-first)

1. **Inspect** the real support surface and existing routes: `assets/js/floating-atlas/terrain.js`, `support.js`, `plan.js`, `collision.js`. Measure slopes and edges; never flatten approved terrain.
2. **Write a 5-line route note** (in the task report, not a new document): arrival → orientation landmark → main destination → optional loop / reward → return. Name one main landmark and 1–3 secondary ones, and what the player sees from arrival.
3. **Block out reversibly** behind a localhost flag or isolated module (same pattern as `town-*=` flags gated by `dev-town=s2f`). Primitives are fine for blockout only.
4. **Walk it** with real keyboard input (Playwright MCP `browser_run_code_unsafe` holding keys, or the review panel's "Walk …" routes): reach it, interact (prompt appears, NPC/research panel opens), turn around, return to spawn. Include one run and one jump where the route needs them.
5. **Check** support/collision (no falling through, no invisible walls on the path), camera obstruction in tight spaces, edge safety near cliffs, and that the destination is visible or signposted from the previous node.
6. **Fix** navigation defects before adding detail; then hand visual judgement to `urban-atlas-visual-qa`.

## Design checklist (only what applies)

- **Floating-island composition** — readable island silhouette; landmark on a high or edge point; cliffs and underside visible from approaches.
- **Trail hierarchy** — paved settlement street › packed trail › faint path; width, material and edging tell the player which is primary.
- **Safe exploration** — rails, vegetation or terrain lips along drop-offs on main routes; optional risky edges clearly optional.
- **Landmarks** — main landmark visible from arrival; secondary landmarks frame each fork; nothing important hidden behind the camera's default yaw.
- **Forest / highland / waterfall** — trail approaches the waterfall with a viewpoint and a reachable pool/ledge; highland gives a look-back view to the settlement; forest density opens at decision points.
- **Environmental storytelling & rewards** — each optional loop ends in something: a vista, NPC, research marker, discovery item or shortcut home.
- **Readability** — at the gameplay camera the next destination or its cue is on screen at each fork.

## Done means

Reached, interacted and returned in the real browser (state the URL, flags and route); route note in the report; defects listed honestly. No large plans, no new design documents for small changes, and no next phase without owner authorization (`AGENTS.md`).
