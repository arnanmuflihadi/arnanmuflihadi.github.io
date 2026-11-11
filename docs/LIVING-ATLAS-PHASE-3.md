# Phase 3 — living city and one optional encounter

Historical milestone. Current guide identities, jump controls, architecture and
loading behavior are documented in [the repair report](LIVING-ATLAS-REPAIR.md).

Continue the shared Jakarta scene on `codex/jakarta-experience`, preserving the
existing uncommitted work and static portfolio. User requested the next phase
after reviewing Phase 1–2. No Bandung or transport work belongs to this phase.

## Implementation plan

1. Reuse the verified Quaternius humanoid rig and its matching authored actions.
   Import one actual animated CC0 monster, with source and checksum records.
   Keep combat clips and the creature outside the initial editorial bundle.
2. Populate purposeful public-space routes with several independently animated
   civilians and a researcher. Use obstacle-aware waypoints, waiting, interaction
   facing, and distance-based update budgets. Share geometry, not skeleton state.
3. Add a native dialogue panel and an optional Lost Survey Signal quest: speak to
   the researcher, investigate the old rain-garden service yard, overcome one
   fictional guardian, retrieve the device, and report back. Research remains
   available regardless of quest status.
4. Add light-attack combo, dodge, guard, health, directional/range/line-of-sight
   hits, wind-up telegraphs, recovery and defeat/retry. Keep the encounter in a
   clearly marked overgrown service yard away from ordinary station/shop use.
5. Preserve exploration/editorial state, pause all simulation for dialogs and the
   shared menu, and keep keyboard/touch controls and reduced motion usable.
6. Test the actual complete quest, defensive actions, defeat/recovery, NPC routes,
   history/reading regressions, mobile layout and real animation. Capture and
   inspect browser evidence; keep inherited static-audit results explicit.

## Implemented systems

The same Jakarta scene now contains Sari (researcher), Bima (commuter), Ayu
(neighbourhood reader), Raka (station attendant) and Nara (shopkeeper). Short
authored routes have obstacle checks, separation from other people, waiting and
independent animation. Raka follows the station ramp. Nara stands on the actual
raised shop threshold. Distant residents animate at lower update rates. Five
instances share geometry but have independent cloned skeletons and shirt colors.

Sari offers **The Lost Survey Signal**. Its explicit state progression is:
available → searching → device ready → returning → complete. The southwest
maintenance yard, its sign, the mosskeeper, receiver and quest dialogue are
fictional. Each resident can also open related research, including before the
quest is accepted. No research result or case-study access depends on combat.

The mosskeeper has Idle, Patrol, Detect, Chase, Attack, Hit, Recover, Return and
Defeated states. The strike has an amber ground warning and a delayed damage
window. Player attacks check range, direction and line of sight; each swing hits
once. A second press queues the second punch. Dodge has a cooldown and a timed
invulnerability window. Guard requires facing the attacker and reduces damage.
Leaving the yard leashes the guardian and allows recovery. Defeat offers a full
retry outside the encounter boundary or a return to reading. Dismissing defeat
with Escape also recovers safely.

The explorer's collision root owns all movement. Matching Quaternius punch,
roll, hit and defeat clips animate the existing skeleton; the author's sword-idle
clip supplies the unarmed guard stance. A bounded skinned-geometry floor check
keeps rolls and defeat poses above paving during crossfades. It runs only during those actions and
for 0.18 seconds of settling; it never moves the collision root. The defeat pose plays
before recovery choices pause the world. Player movement also respects civilian
collision footprints.

## Runtime and data

| Module | Ownership |
| --- | --- |
| `city-life.js` | Civilian profiles, routes, local avoidance and animation budgets. |
| `rigged-actor.js` | Skeleton-safe cloning, material variants and resource disposal. |
| `quest-state.js` | Validated quest state and ordered transitions; no research mutation. |
| `combat-simulation.js` | Deterministic health, attacks, timing, defenses and AI. |
| `adventure.js` | Scene actors, optional asset loading, interactions and story orchestration. |
| `service-yard.js` | Designed maintenance court, receiver and strike warning. |
| `adventure-ui.js` | Native dialogue, journal and compact encounter controls. |

The NPC GLB streams progressively with the city. Explorer actions and the monster
load only on quest acceptance, or when resuming an unfinished quest in adventure
mode. Mode changes reuse all actors, quest state and scene identity. Dialogs,
menus and hidden-page states pause simulation. The existing session record keeps
player coordinates and a validated quest phase; a full document reload restarts
civilian schedules and encounter health. In-document mode switches retain health.
All runtime imports share a versioned URL set so cached older exports cannot
break a new scene controller. Nearby canopy leaves cut away around the follow
camera; the same trees remain fully visible in editorial compositions.

## Imported assets

Actual, locally delivered CC0 models from Quaternius:

| File under `assets/game/phase3/` | Original source | Delivery size |
| --- | --- | --- |
| `city-resident.glb` | Casual; [Ultimate Modular Characters](https://quaternius.com/packs/ultimatemodularcharacters.html) | 1,186,388 B |
| `explorer-actions.glb` | Adventurer actions from the same pack, animation-only | 623,948 B |
| `mosskeeper.glb` | MushroomKing; [Ultimate Monsters](https://quaternius.com/packs/ultimatemonsters.html) | 499,044 B |

These files were downloaded/prepared and rendered, not substituted with primitive
characters. The monster's original 43-joint rig and embedded atlas are retained.
The humanoid uses the matching 62-joint rig. Source and output checksums, selected
clip names and edits are in `source.json`, alongside both original CC0 notices.
The monster folder's supplied notice retains its original “Ultimate Platformer
Pack” header; the official monster pack page separately identifies its CC0 license.

Reproduce with `scripts/prepare-atlas-phase3.mjs --source <source directory>
--deps <temporary node_modules>`, using pinned glTF-Transform core/functions 4.2.1.
Source hashes are checked before conversion. Temporary authoring tools and full
vendor sources are not runtime dependencies or part of the delivered site.

## Validation and boundary

The focused suite now has **36 passing tests**, including real rig/action binding,
independent skeletons, actual collision routes, attack timing, defenses, safe
recovery and deformed roll clearance. The complete quest was exercised in the
real browser: Sari → yard → guardian defeat → pickup → return → completion.
The two-hit combo reduced enemy health from 96 to 36; two combos defeated it.
Held guard reduced strikes to five damage. Defeat and the full-health retry were
also exercised. Native touch walking, guard, combo and dodge were tested in a
390×844 viewport, with readable research available before quest acceptance.

Browser screenshots were captured and visually inspected. Final QA and image
evidence are returned with the implementation in chat. The unchanged static audit
still reports the same 58 inherited findings as the untouched source. No physical
mobile-device, Safari/Firefox, hardware performance or automatic GPU recovery
coverage is claimed. Only Phase 3 is added; Bandung, transport and gliding remain
outside this work. No commit, push or deployment was performed.
