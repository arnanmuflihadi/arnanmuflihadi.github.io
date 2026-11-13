# Jakarta vertical slice — QA record

> Historical implementation record. The current Home/Work integration, assets
> and validation are documented in [Living Atlas](LIVING-ATLAS.md) and
> [Phase 1–2 QA](LIVING-ATLAS-QA.md). Earlier mission UI and separate game entry
> described here are not part of the current public experience.

Date: 31 October 2026 (Asia/Jakarta).
Source baseline: `dffaf125c1999615852772093f04255f5ebb48e4`.

## Executed checks

- Seven Node tests pass: six-project registry/routes and map destinations; URL
  roundtrips including project-path hosting, unrelated queries and hashes; invalid
  route/storage handling; collision tunnelling/sliding/bounds; reachability of
  both landmarks; walking/sprinting/stopping; camera obstruction avoidance.
- Syntax checks pass for all 14 authored/modified JavaScript source/build files.
- `git diff --check` passes. New files also checked for whitespace errors.
- `node scripts/audit-static-site.mjs` fails with 58 inherited issues. Running it
  on the untouched downloaded source produces byte-identical output and exit
  status. No additional audit failures were introduced. The inherited gate still
  needs attention before a full production release.

## Real browser checks

Used the Codex in-app Chromium browser against a Python static server. No browser
substitute or screenshot mockup was used. Inspected 1280×720 desktop and 390×844
narrow viewports; restored the original viewport after responsive testing.

- Ordinary Home and Work visits retain the original professional content and
  expose an opt-in experience switch. The renderer is imported dynamically only
  inside the activation path; the project drawer requires no game renderer.
- Walked from spawn to the station using held WASD inputs. E opened the transit
  drawer, and the scenario controls changed the displayed mean from 29.67 to
  37.55. Recording the finding changed mission progress to 1/2.
- Walked across the district to the business plaza, interacted, inspected its
  DBSCAN explanation and recorded its finding. The mission reached completion.
- Held forward movement against the business building. The player stopped at
  z=7.920 and remained at that boundary under another second of forward input.
- Dragging the canvas rotated the third-person camera. Narrow-screen testing
  revealed a close-obstruction framing issue; the camera now switches to an
  overhead view when a wall would otherwise push it inside the character.
- Returned to professional mode and verified the selected study received focus.
  Resumed the game and verified the previous player coordinates were retained.
- Back restored the transit project and Forward restored CBD in the shared drawer.
- From Work, selected transit in the professional navigator, then used Explore
  this project in 3D. It focused x=-13, z=-2 without a document navigation.
- Direct RPG deep links initialized the world correctly. Direct case-study links
  remain normal HTML routes. An explicit project deep link focuses its landmark.
- At 390×844, verified the responsive HUD and full-width scrollable drawer. Held
  the backward touch button for 700 ms; player z changed from 11.000 to 14.186.
  This tests pointer events at mobile size, not physical touchscreen hardware.
- M hid the minimap. Escape closed the research modal without pausing gameplay.
  Native modal semantics provide focus containment; close restores the opener.
- Theme switching worked in professional mode; restored the initial theme.
- Direct-load background inertness was rechecked after fixing the shell conflict.
- No blocking JS errors were observed. Three.js reports an expected multiple-
  instance warning when the isolated RPG module follows the existing hero subset.
  These builds do not share game objects; decorative renderers pause in RPG mode.

## Performance and limitations

Pixel ratio is capped at 1.7 desktop / 1.25 compact. Shadows default off below
700 px, with a working quality toggle. Trees use instancing; geometry/materials
are reused. Only one RPG RAF loop is scheduled; it stops in professional mode and
when the document is hidden. Browser-context loss and initialization failures
show an error with a persistent Return to Portfolio route.

The HUD exposes a `data-fps` diagnostic sampled over two seconds of wall time.
A short desktop sample reported 180 FPS before final art changes; this is a local
observation, not a representative benchmark or a mobile-performance guarantee.
Physical iOS/Android testing, extended frame-time profiling, forced GPU context
loss, forced unsupported-WebGL, and OS reduced-motion emulation remain unverified.
The reduced-motion path disables limb/marker animation and camera interpolation;
it is covered by source inspection and the player test, not an OS-level test.

Collision is intentionally simple and the world is small. Camera obstruction is
pragmatic, including a near-wall overhead fallback. The research visualizations
are an aggregate comparison and a labeled illustrative clustering diagram, not
full GIS layer rendering. Existing analytical map tools remain linked separately.
No future regions, NPCs, traffic, jumping or geographic accuracy are implied.
