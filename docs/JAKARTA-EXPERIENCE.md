# AR(N)AN — Jakarta vertical slice

> Historical implementation record. The current Home/Work integration, assets
> and validation are documented in [Living Atlas](LIVING-ATLAS.md) and
> [Phase 1–2 QA](LIVING-ATLAS-QA.md). Earlier mission UI and separate game entry
> described here are not part of the current public experience.

## Audit and integration decisions

Imported the existing public repository at the commit recorded by `git rev-parse
HEAD`. Preserved every original route, case study, map document, CV, and deployment
workflow. The workspace was initially an empty Git repository; source history was
attached and work is on `codex/jakarta-experience`, without a new commit or push.

The site is static HTML/CSS/JS. `site-shell.js` owns navigation and page curtains;
`motion.js` owns GSAP, ScrollTrigger, Lenis and decorative 3D. The original curated
Three.js IIFE lacks PerspectiveCamera, Raycaster and InstancedMesh. An isolated,
483 KiB-class, locally vendored ES module supplies these only after 3D activation.
It does not overwrite or assume game APIs in the original hero subset.

The shared motion layer pauses its ambient renderers and Lenis during gameplay.
The shell respects game background inertness, including on direct deep links and
pageshow. New styles inherit the existing typography, theme and editorial tokens.
Existing HTML changes only attach versioned enhancement assets and update versions
of the two changed shared scripts. Research text and analytical embeds are intact.

## File map

- `assets/js/project-registry.js`: six verified project summaries, routes,
  encounter availability, research caveats, scenarios and map links.
- `assets/js/experience-state.js`: pure URL serialization and validated state.
- `assets/js/experience-controller.js`: global switch, project navigator, native
  modal research drawer, URL history, persistence and lazy game lifecycle.
- `assets/css/experience.css`: professional enhancement, drawer and responsive HUD.
- `assets/js/rpg/`: world/district configuration, original procedural character,
  input, collision, follow camera, minimap and render-loop coordinator.
- `assets/js/vendor/three-rpg.module.js`: pinned MIT renderer module.
- `scripts/build-rpg-vendor.mjs`: reproducible one-time vendor build.
- `tests/experience.test.mjs`: registry, state, navigation and gameplay tests.

## Experience behavior

Home and Work offer the same registry-driven research navigator. Inspect a project
and choose **Explore this project in 3D** to focus its landmark without navigating.
Return to Portfolio highlights and focuses the selected study. Resuming retains the
safe player position. An explicit project-focus action relocates to that landmark.
All pages have a 3D entry control; case studies pass their implemented encounter to
Home. Those cross-document links retain conventional navigation.

`?experience=rpg&project=transit` and `?experience=rpg&project=cbd` are shareable on
Home or Work. `?project=cbd` opens the same drawer in professional mode. Back and
Forward restore experience and selected project. Other query parameters and hashes
are preserved. Mission progress, selection and a validated player position persist
in sessionStorage. Explicit mode choices are recorded in localStorage, but never
auto-start the game: a fresh ordinary URL always defaults to professional mode.
A saved position is checked against current world collisions before use.

## Controls

- WASD / arrows: camera-relative walk; Shift: sprint.
- Drag the canvas: orbit the follow camera; vertical drag changes elevation.
- E or the interaction button: inspect a nearby landmark.
- M: toggle minimap; Escape: pause/resume or close a modal.
- Pause, Controls, Shadows and Return to Portfolio are conventional buttons.
- Narrow screens and coarse pointers show hold-to-walk direction buttons.

Approach the station and business plaza, open their findings, and record each note.
Both notes produce a real completion state. Research access is never mission-gated.

## Running and deployment

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Open `http://127.0.0.1:4173/`. No npm install or build is needed. Relative imports
and assets support GitHub Pages project paths. The existing Pages workflow is
unchanged. Review the branch before merging to main; nothing has been published.

To intentionally regenerate the vendor module:

```sh
npm install --prefix /tmp/arnan-rpg-build --ignore-scripts three@0.180.0 esbuild@0.25.10
node scripts/build-rpg-vendor.mjs --deps /tmp/arnan-rpg-build/node_modules
```

Update its checksum in `assets/js/vendor/THIRD_PARTY.md` afterward.

## Evidence and boundaries

Transit figures were verified against `project-transit.html`: 261 villages,
60-minute threshold, mean scores 29.67 / 37.55, and the reported 26.6% modeled
uplift. The comparison uses these documented aggregate scores. It does not pretend
to be a geographical scenario map. Full map tools are explicit outbound links.

The CBD encounter follows `project-cbd.html`: 91,940 OSM commercial POIs, adaptive
DBSCAN, haversine distances and the largest-cluster provincial CBD interpretation.
Its diagram is explicitly illustrative; it does not invent point-level results.

The district and minimap are conceptual geography, not geospatial measurements.
Ground is flat; collision is horizontal circle-versus-expanded-box with bounded
substeps and wall sliding. Camera obstruction uses mesh raycasting. There is no
jumping, terrain physics, downloaded model animation or NPC simulation.

## Validation

Run `node --test tests/experience.test.mjs`, JavaScript syntax checks,
`git diff --check`, and `node scripts/audit-static-site.mjs`.

The supplied static audit fails on the untouched source too: canonical footer
requirements, transition placement, existing iframe policy and older approved-art
requirements. Before/after output was compared exactly; this change adds no audit
failures. Do not treat this pre-existing release gate as passing.

Browser verification and remaining limits are recorded in `JAKARTA-QA.md`.

## Licensing and expansion

All new scenery, character geometry, signs and diagrams are authored in code for
this project. Three.js is MIT; original vendor licensing records are retained.
Temporary npm dependencies and browser tooling are outside the repository.

Next priorities: (1) test on physical iOS/Android and profile slower GPUs;
(2) improve character/architecture art and camera usability; (3) add West Java as
another district configuration with the same registry and interaction contracts;
(4) add Bandung; (5) load compact, source-backed GIS layers only on request.
