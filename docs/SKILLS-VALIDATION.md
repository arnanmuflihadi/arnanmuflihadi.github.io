# AR(N)AN game development skills — installation validation

Installed 2 November 2026 in the current working tree. This was a workflow-only task; no settlement phase was started.

## Installation and discovery

- `.agents/skills/fantasy-level-design/SKILL.md`: connected RPG-hub planning, terrain-aware placement, reversible blockout and actual-controller traversal.
- `.agents/skills/game-visual-qa/SKILL.md`: actual browser visual review, matched evidence, provisional rubric, regressions and measured rendering costs.
- Both have UI metadata in `agents/openai.yaml`, explicit implicit-invocation permission and linked focused references. Neither installs executable scripts, dependencies or third-party skill code.
- No repository `AGENTS.md` or local skills existed beforehand. The new `AGENTS.md` routes layout work and 3D phase submissions to these skills, preserves game/research systems, makes the MRT optional, requires evidence and keeps owner approval/phase boundaries explicit.
- Reused the built-in skill-creator initializer and validator, skill-installer guidance, and existing project camera/evidence/test workflows. No duplicate QA helper was added. Existing global skills were not edited.

The files follow the [official Agent Skills specification](https://learn.chatgpt.com/docs/build-skills). Both passed the bundled `quick_validate.py`; YAML UI policy/default prompts, reference resolution and absence of executables/symlinks were also checked.

The installed desktop Codex CLI **0.166.0-alpha.5.1** was queried through `skills/list` with the repository cwd and `forceReload=true`. It returned each requested name exactly once, **scope `repo`, enabled `true`**, with the expected paths/UI descriptions and **zero repository errors**. No model turn was started by that registry query.

## Read-only behavioral dry-run

The skill-creator's independent forward-testing procedure was used with two ordinary example requests and the new skill metadata. The evaluator had the raw R0-B1 images and site record, without a supplied expected diagnosis.

| Example task | Skill selected | Observed result |
|---|---|---|
| Review whether the current placements form a compact hub serving skyport, square, market, Guild and lookout | `fantasy-level-design` | The four buildings are dispersed across natural trails. No shared town square or continuous market street is established; proposed research access remains unresolved. Suggested the skyport → square → market/Guild journey and optional lookout loop as planning checks, keeping the MRT optional. |
| Assess visual coherence between buildings and surrounding ground | `game-visual-qa` | The commercial building's isolated paved apron meets a dirt trail abruptly. Modern facades and natural ground do not yet form a continuous urban streetscape. The deep canopy also darkens the frontage. |

Evidence read: `docs/architecture-r0b1-review/final-ensemble.jpg`, `final-commercial.jpg`, `final-commercial-eye.jpg`, and `assets/game/architecture-r0b1/site-feasibility.json`.

These are settlement-readiness findings, not a reversal of approval for the natural terrain. No blockout or building changes were made. Actual traversal, calibrated camera height, fresh rendering costs and gameplay regressions were not exercised by this screenshot-only dry-run. Historical R0-B1 results were not presented as newly executed tests. Owner approval remains pending.

## Scope and limitations

SHA-256 comparison confirms all **1,623 pre-existing project files** in the installation baseline are unchanged. Repository additions are limited to the two skill packages, `AGENTS.md` and this note. Prior screenshots and approved evidence are preserved.

Discovery and two representative routing cases were verified; future implicit selection still depends on the request and available context. The skills are available on the next turn. If a selector has not refreshed, the official guide recommends restarting Codex. No R0-B1.5 or R0-B2 implementation is authorized by this installation.
