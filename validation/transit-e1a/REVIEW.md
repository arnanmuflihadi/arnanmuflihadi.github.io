# R0-E1A review

Local development flag: `?experience=adventure&dev-town=s2f&town-layout=reset-final&town-props=cc0&town-guild=r0c2&town-skyport=r0c3&town-skyport-polish=r0c3-1&town-story=r0e1`. No deployment. This is objective 1 of 3; the remaining objectives are not implemented.

Nadia uses the existing resident and cached source; Lembaran's two scenarios read the shared transit registry. Acceptance, viewing both scenarios, recording the comparison and returning to movement were exercised in the actual browser. The explorer reached Nadia and Lembaran, the comparison offered recording only after both choices, and 1/3 persisted after reload and Adventure/Professional switching. The existing review harness completed forward and reverse routes using the original controller. At the Guild, the authentic transit panel opened and closed. Nadia's decline and Escape were exercised. Invalid saves, duplicate events and public/flag dependencies were checked by focused tests. The flag-off browser view had no story card; its observed asset inventory did not contain the quest module. One resident was reported in each mode.

## Evidence and limitations

- [Nadia in the town](evidence/04-nadia-in-town.jpg), [briefing](evidence/01-nadia-briefing.jpg), [both-scenario comparison](evidence/02-network-comparison.jpg), [1/3 journal](evidence/03-journal-one-of-three.jpg). Some views retain the local review panel. Nadia's view shows the skyport canopy obscuring the upper camera view: this needs visual correction/review before calling the camera clearance fully acceptable.
- The developer review rail reported PASS for the full forward and reverse walk. The separate NPC and counter interactions were reached through real keyboard movement; this is not a single uninterrupted recorded run. Touch controls, complete camera coverage, invalid-save injection in the live browser, and network-request inspection across every navigation path remain unverified.
- Relevant tests: `node --test tests/transit-quest.test.mjs tests/living-atlas.test.mjs tests/floating-atlas.test.mjs tests/atlas-guild.test.mjs tests/experience.test.mjs` — 24 passed, 0 failed.
- M4 Pro, 1280×656, DPR 1, Glass B, same 2 s warmup / 12 s camera rail: story off 16.6/22.3 ms median/p95, on 11.1/17.0 ms; both 338–417 all-pass draw calls and 2,545,684–2,624,244 submitted triangles. Separate walking samples: off 16.4/22.2 ms, on 11.1/16.7 ms. These runs had variable system load and do not demonstrate a performance improvement; no GPU timing or mobile measurement was made. Benchmarks preceded the final lazy-loading and label-only adjustments.

## Changed files and rollback

Changed: `assets/js/floating-atlas/entry.js`, `assets/js/floating-atlas/guide.js`, `assets/js/adventure-ui.js`, `assets/js/living-atlas-controller.js`. Added: `assets/js/floating-atlas/transit-quest.js`, `tests/transit-quest.test.mjs`, and this validation directory. No binary assets or accepted terrain/building data were changed.

Remove `town-story=r0e1` from the URL for normal local behavior. Exact copies of the four prior integration files plus the unchanged CSS are in `baseline/`; `shasum -a 256 -c validation/transit-e1a/baseline/SHA256SUMS` verifies them. To roll back code, copy those four files to their original paths and remove the two newly added quest/test files; preserve all unrelated untracked and modified work.
