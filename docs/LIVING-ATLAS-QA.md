# Living Urban Atlas — Phase 1–2 QA

Executed 31 October 2026 against the static site on localhost, on branch
`codex/jakarta-experience`. No deployment or later-phase systems.

## Automated checks

- `node --test tests/*.test.mjs`: **28 passed**. Covers actual skinned assets,
  animation mixing, movement/collision, camera obstruction, route roundtrips,
  storage validation, all three shared landmark approaches, camera compositions,
  six existing research destinations, scenery checksums and embedded glTF data.
- Node syntax checks passed for **31** authored modules, conversion/build scripts
  and tests. The browser also loaded the actual vendored renderer successfully.
- Local `href`/`src` scan across all public top-level HTML routes found **no missing
  local targets**. All six project routes and registry map destinations exist.
- Tracked and untracked authored text checked for whitespace errors.
- `node scripts/audit-static-site.mjs`: **fails with 58 inherited findings**.
  Its output is byte-identical to running the same audit on untouched source
  commit `dffaf125c1999615852772093f04255f5ebb48e4`. The audit was not weakened.
  Findings concern inherited footer/transition conventions, eager map embeds,
  missing older hero masters/derivatives and old static-story hooks. This is an
  outstanding repository release gate, not a passing check.

## Real browser checks

Used the Codex in-app Chromium browser, with native input and actual Three.js
rendering. Inspected desktop 1280×720 and a narrow 390×844 viewport override.
Temporary viewport overrides were reset. Images below are actual captures,
visually opened and inspected, not mockups or generated reference images.

| Check | Observed result |
| --- | --- |
| Home arrival | Semantic headings, research links and real Jakarta geometry visible. Character-ready attribute false before control. |
| Scroll storytelling | Arrival→Transit changed the composition and selected project without replacing the scene. |
| First activation | The explorer loaded into the existing district; no second world, game page or duplicate header. |
| Shared scene identity | Editorial and adventure UUID both `5e9440fa-bedb-4ffe-b61d-1ad4ed649e35`, renderer count 1. See captured JSON. |
| Character animation | Held W and Shift+W; observed Walk/Run, advancing clip time and changing world position. Run was faster. |
| Collision | Running into the station stopped at approximately x −23, z −10.91, with feet on the raised platform at y .52. Actual layout substep checks also pass. |
| Research inspection | E at the station opened the same Transit dialog used by editorial inspection. Scores/caveats and case/map links were present. |
| Complete case study | Followed the Transit case-study link; the existing research page loaded without errors. Its Living atlas link returned to Home with Transit still selected. |
| Resume | After returning to editorial, resuming retained x −23.000, z −3.928 exactly in the recorded transition check; scene UUID stayed unchanged. |
| Back/Forward | Restored editorial/adventure modes. On Work, Back restored the MBR study dialog and Forward restored exploration. |
| Work | All six chapters available; MBR inspection and safe landmark activation reached x 0, z −25. Return restored that research context. |
| Mobile | Header switch, menu, chapter, minimap and direction controls remained reachable. Held touch forward changed z −3.928→−5.617. |
| Mobile menu/focus | Fixed scroll restoration; selected Transit URL remained stable. Escape closed the menu, and returning to editorial restored main/footer/skip-link accessibility. |
| Reduced motion | Guide checkbox persisted; snaps editorial camera and suppresses extra environmental motion, while walking remains usable. Restored normal preference afterward. |
| Rendering failure | Separate temporary localhost fixture returned 503 for the renderer module. Poster/HTML remained, control disabled, study dialog and case/map links still available. |
| JavaScript logs | No warnings/errors in normal Home/Work scenarios. The failure fixture produced the deliberately induced load error. |

The rendering-failure fixture was outside the repository and does not alter
production assets. Context-loss reload messaging is implemented, but forced GPU
context loss and automatic GPU recovery were not tested or claimed. Data Saver's
conditional branch is implemented but no OS/browser network preference was
changed for this validation. No physical mobile-device or cross-browser coverage,
Lighthouse score, or hardware performance guarantee is claimed.

## Captured evidence

- [Arrival, before explorer loading](living-atlas-review/editorial-arrival.jpg)
- [Transit editorial composition](living-atlas-review/editorial-transit.jpg)
- [Same district under character control](living-atlas-review/gameplay-transit.jpg)
- [Captured shared-scene attributes](living-atlas-review/shared-scene.json)
- [Work neighbourhood composition](living-atlas-review/work-neighbourhood.jpg)
- [Mobile editorial](living-atlas-review/mobile-editorial.jpg)
- [Mobile character control](living-atlas-review/mobile-gameplay.jpg)
- [Renderer unavailable fallback](living-atlas-review/rendering-fallback.jpg)

## Scope boundary

Only Jakarta is constructed. The other research remains readable with explicit
region availability labels. No NPCs, combat, quests, train/bus travel, gliding or
additional regions were added. Human visual approval of this milestone remains
the gate before expanding those systems.
