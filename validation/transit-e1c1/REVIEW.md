# R0-E1C.1 camera investigation — incomplete

No camera or game files were changed. The original source files are checkpointed in `baseline/` (verify with `shasum -a 256 -c validation/transit-e1c1/baseline/SHA256SUMS`).

In the live game, the [Nadia approach](evidence/nadia-before.jpg) showed the skyport overhang across the top of the view; player `(10.518, 15.189, 63.701)`, camera `(12.317, 18.336, 66.291)`, FOV 60°, 1364×1145 viewport. At a [Guild-side pavilion approach](evidence/guild-before.jpg), the roof filled the top of the view with the player beside a pavilion post; player `(-3.131, 15.515, 37.969)`, camera `(-0.891, 18.238, 36.979)`, FOV 60°. This does not establish that the camera entered the player mesh or identify a Guild-door collision.

Code inspection found a plausible close-range failure: the follow camera permits 0.5 m from its target when an expanded obstacle contains the ray origin, but the actual obstructing proxy at the reported Guild pose has not been verified. Roof rendering around the view frustum also needs direct inspection; center-ray clearance alone is insufficient. No speculative collision filtering or camera rewrite was applied. There are no after images, six matched pairs, completed traversal, or measured overhead; both reported defects remain unresolved and this phase has not passed.

Focused regression command: `node --test tests/atlas-character.test.mjs tests/atlas-guild.test.mjs tests/transit-quest.test.mjs tests/experience.test.mjs` — 17 passed, 0 failed; see `test-results.txt`. These tests do not prove camera visual clearance.

Preview: http://127.0.0.1:4188/index.html?experience=adventure&project=transit&dev-town=s2f&town-layout=reset-final&town-props=cc0&town-guild=r0c2&town-skyport=r0c3&town-skyport-polish=r0c3-1&town-story=r0e1. Owner review remains pending; no deployment.
