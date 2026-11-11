# Preserved Phase 2 Jakarta district

R0 replaces the environment, not the portfolio or its research. The Phase 2
district remains a documented legacy implementation in `assets/js/urban-atlas/`.
It is not assembled alongside the floating island on Home or Work.

Preserved environment modules include `scene.js`, `architecture.js`,
`environment.js`, `district-plan.js`, `district-ground.js`, `district-assets.js`,
`district-artwork.js`, `district-review.js` and the former `entry.js`.
Their source, assets, collision tests and captured Phase 2 evidence remain.

The legacy development preview is `urban-atlas.html` (noindex). The approved
architecture regression gallery remains `asset-showcase.html`. These explicit
review pages are not the production Home/Work environment. Home/Work now import
`floating-atlas/entry.js`, whose only constructed world is Transit Kingdom.

R0 reuses the approved `model-library.js`, `architecture-design-system.js`,
geometry helpers, input, animation, rig and dialogue infrastructure. The old
character, player controller and camera receive optional world dependencies;
their existing defaults remain unchanged. All original 67 tests remain in the
suite and pass, including all 16 asset/architecture/character regressions.

Preservation evidence:

- `docs/PHASE-2-DISTRICT.md`: old design, audit classification and measurements.
- `docs/district-review/`: eight old comparison pairs, gameplay and source records.
- `docs/floating-review/legacy-module-hashes.json`: module preservation inventory.
- `assets/game/scenery/architecture-enhancements.json`: original approved-component
  snapshot, unchanged and historically unscored.
- `assets/game/scenery/architecture-source.json`, `source.json`, `verification.json`
  and the existing CC0 notices: original provenance and archive verification.

Branch: `codex/floating-atlas-r0`, created from the existing checkout. Pre-existing
uncommitted work was preserved. No blanket commit, reset, clean, push or deployment
was performed. The installed Command Line Tools Git binary works directly; the
Xcode license was not accepted or changed.
