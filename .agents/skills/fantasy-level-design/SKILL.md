---
name: fantasy-level-design
description: "Plan or review 3D adventure-game layouts for AR(N)AN: floating-island settlements, fantasy towns, building and landmark placement, plazas, streets, skyports, world composition and player navigation. Use before changing settlement layouts; not for asset-only modeling or ordinary portfolio copy edits."
---

# Fantasy level design

Design a coherent, navigable tropical modern-fantasy RPG hub. Establish connected public space and a player journey before distributing finished architecture.

## Scope and project context

Read the latest user brief, repository `AGENTS.md` and approval/evidence record. Determine whether the task authorizes planning, blockout, implementation or a read-only review. A dry-run produces findings and proposed checks, not changes to the level.

Read [references/project-context.md](references/project-context.md) for current project files, destinations and preserved systems. Consult [references/reference-map.md](references/reference-map.md) only when a concrete design question needs an external implementation reference.

The first island is a compact RPG hub. Its primary destinations are the skyport, town square, market street, Atlas Guild and highland lookout. The MRT station is optional. Keep real Jakarta transit research accessible through the portfolio. Judge the fictional layout by gameplay, sightlines and the actual controller, rather than imposing real-world urban-planning or TOD standards.

## Workflow

1. Inspect the current terrain mesh/support, elevations, slopes, walkable boundaries and protected surfaces. Measure available buildable space; do not assume a flat site or flatten approved terrain.
2. Locate spawn, primary destinations, landmarks, scenic viewpoints and existing circulation. Distinguish approved placements from reservations and asset demonstrations.
3. Describe the player journey: arrival, orientation, first destination, choices, discoveries and return. Establish a spatial hierarchy with a readable public center.
4. Draw a primary route, optional loops and exploration areas. Check route visibility, elevation changes, dead ends and expected traversal time with the current movement settings.
5. Cluster buildings around the square and connected streets. Face entrances toward usable public space; reserve approach, turning and canopy clearance. Do not scatter unrelated buildings along dirt trails or reinstate rejected Jakarta layouts automatically.
6. Define continuous urban paving, thresholds, steps/ramps and transitions into natural trails. Retain natural terrain where it supports the journey; distinguish settlement streets from wilderness paths.
7. If construction is authorized, make a reversible blockout before detailed construction. Keep placement data and temporary geometry separable from approved terrain and production content. Primitives are appropriate for blockouts, not a substitute for the final architectural asset foundation.
8. Traverse it with the actual third-person controller: walk, run, jump, turn, approach entrances and return to spawn. Check support, collisions, camera clearance, path obstruction and inaccessible destinations.
9. Inspect player-eye-height, third-person and aerial compositions using reproducible camera presets. Check landmark visibility, enclosure, skyline hierarchy and the relationship between frontages and public spaces.
10. Correct layout and navigation defects before placing final architecture. Use `game-visual-qa` for visual evidence; repeat the relevant routes and cameras after meaningful corrections.

## Handoff and owner gate

For an authorized layout phase, deliver:

- Gameplay route diagram with primary/optional routes and elevation constraints.
- Reversible settlement blockout and landmark placement plan with footprints, entrance directions and connected public spaces.
- Actual player traversal checks and reproducible screenshots, with camera/quality settings.
- Known layout defects and the specific phase awaiting owner approval.

For a read-only review, deliver the diagnosis and proposed blockout/checks; mark unbuilt or untested outputs explicitly. Preserve existing terrain, working gameplay/camera systems, GLB pipeline, collision support, research integration, licenses and prior evidence.

Complete authorized corrections before handoff. Stop at the requested phase boundary and keep owner approval pending until explicitly supplied. Technical passes and internal visual observations cannot grant human approval or authorize the next settlement phase.
