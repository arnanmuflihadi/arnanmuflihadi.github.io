# R0-E1C review

Local review only; no deployment. URL: http://127.0.0.1:4188/index.html?experience=adventure&project=transit&dev-town=s2f&town-layout=reset-final&town-props=cc0&town-guild=r0c2&town-skyport=r0c3&town-skyport-polish=r0c3-1&town-story=r0e1

## Changes

The research journal now lists all three objectives and their active/completed states. Dialogue width was reduced on desktop, the completion heading identifies the quest, and the idle interaction prompt names the current objective. The existing follow camera receives a smoothly blended shorter distance near Nadia, without altering normal flag-off settings; no terrain, buildings, character assets, research values or controller physics were changed.

## Browser evidence and acceptance

The final build was walked continuously from skyport to Nadia, Lembaran, Telaga Awan and the Guild using the real explorer, without reloads or review controls. Both scenarios, 1/3, wrong-answer retry, correct interpretation, 2/3, actual study, filing, 3/3 and movement after closure were observed. The timestamped [trace](playthrough-trace.json) is a sequence of observed checkpoints, not a video or a frame-by-frame recording. The study was also opened before accepting. Separate browser checks confirmed 1/3 and 3/3 after reload, journal Escape and Space without unintended jump, and one Nadia / one renderer. Prior E1B evidence covers Professional Mode, full-case-study navigation and Back; these were not all repeated in E1C.

Actual screenshots: [arrival](evidence/arrival.jpg), [Nadia before](evidence/nadia-before.jpg), [Nadia after](evidence/nadia-after.jpg), [dialogue](evidence/nadia-dialogue.jpg), [comparison](evidence/comparison.jpg), [journal](evidence/journal.jpg), [square](evidence/square.jpg), [Guild study](evidence/guild-study.jpg), [completion](evidence/quest-complete.jpg), [after completion](evidence/after-completion.jpg), [whole island](evidence/island.jpg). The island uses the existing `island-review=aerial` fixed camera; no `town-review` overlay appears. The journal and Nadia-after images precede the final research-only CSS scoping adjustment; the completion image and trace are from the final gameplay run.

**Visual gate not passed:** the canopy still obscures the upper portion of Nadia's view despite the local adjustment. A tight Guild approach briefly placed the camera inside the character, although moving restored the view. Those defects need a bounded follow-up and owner review; no claim of production readiness or artistic approval is made. The full six links, all interaction angles, a novice timed playthrough, and resource growth across repeated modal openings were not individually validated. Partial-save and completed-save reload were verified. The [phone-size journal](evidence/phone-journal.jpg) and an emulated on-screen walking control were checked at 390×844; no physical mobile device was tested.

## Checks and performance

`node --test tests/transit-quest.test.mjs tests/living-atlas.test.mjs tests/floating-atlas.test.mjs tests/atlas-guild.test.mjs tests/experience.test.mjs tests/atlas-character.test.mjs tests/skyport.test.mjs tests/skyport-polish.test.mjs tests/town-s2g.test.mjs`: 37 passed, 0 failed. Browser logs for the playthrough showed no errors or warnings. The disabled story view showed no quest module in the observed asset inventory.

Matched camera rail, M4 Pro, 1280×656 DPR 1, Glass B and standard shadows, 2 s warmup / 12 s sample: story off 16.7/27.8 ms median/p95, story on 16.7/22.3 ms. Both showed 338–417 all-pass draw calls and 2,545,684–2,624,244 submitted triangles. CPU submission median/p95: off 1.7/3.1 ms, on 1.0/1.2 ms. Load and display scheduling varied; these numbers do not establish an improvement or GPU cost. Active-walking samples were separately measured: off 22.2/33.0 ms, on 22.0/27.7 ms, from different actual walks, not a controlled identical walking comparison. [Raw rail data](performance.json). The rail measurements preceded the final research-only CSS scoping and startup-label cleanup.

## Changed files and rollback

Changed: `assets/js/urban-atlas/camera.js`, `assets/js/floating-atlas/entry.js`, `assets/js/living-atlas-controller.js`, `assets/js/adventure-ui.js`, `assets/css/atlas-adventure.css`. No new binary assets. Removing `town-story=r0e1` disables the story and its local camera adjustment. For a full code rollback, restore the matching paths from `baseline/`; verify the checkpoint with `shasum -a 256 -c validation/transit-e1c/baseline/SHA256SUMS`. Preserve unrelated dirty and untracked work.
