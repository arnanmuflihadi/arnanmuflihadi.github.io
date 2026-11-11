# R0-D1 · skyport flight preview

**Status:** Local development preview; owner visual approval pending. The explorer stays on the deck while a dragon performs a departure preview; boarding and travel are not implemented. The selected cartoon dragon reads as a small flying creature more than a credible passenger mount. The larger Dragon_Evolved from the same pack was also inspected in the live scene; it remained cartoonish and was not retained. Its proportions and connection to the terminal need human review before this can be considered a satisfying boarding experience.

[Open the local preview](http://127.0.0.1:4176/index.html?experience=adventure&dev-town=s2f&town-layout=reset-final&town-props=cc0&town-guild=r0c2&town-skyport=r0c3&town-skyport-polish=r0c3-1&skyport-demo=r0d1). At the spawn, press E or use **Request skyport flight preview**. Escape cancels; reduced-motion mode uses an immediate return. No player transport or destination is implied.

## Asset and implementation

- `Dragon.gltf`, Quaternius, [Ultimate Monsters](https://quaternius.com/packs/ultimatemonsters.html), [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Creator distributes individual glTF files in the pack's public Drive folder. Source preserved as `Dragon-source.gltf` here; GLB conversion uses its embedded texture and geometry.
- Delivery: `assets/game/skyport/boarding/dragon.glb`, **261,004 bytes**, 4,562 triangles, one skinned mesh, one material and one embedded texture. `Flying_Idle` and `Fast_Flying` are real skeletal clips. The remaining source clips are retained in the file. SHA-256: `b0ab4a6d431ee86692c28128da6266e499bb25931cf699a186e138a4c9f16530`.
- `assets/js/floating-atlas/skyport-boarding.js` uses the shared model cache, world, camera and explorer. `entry.js` wires the opt-in flag, interaction, update and cleanup. No movement physics or town geometry changed. The model does not add collision or walking support.

## Browser evidence

All PNGs are real frames from the existing game. `01-arrival.png`, `02-cinematic-near.png`, `03-departure.png`, `04-departure-distant.png` form a timed interaction sequence. `05-restored-player.png` shows the returned explorer. `06-skyport-aerial.png`, `07-island.png`, and `08-boarding-edge.png` are existing fixed-camera views. `09-baseline-skyport-aerial.png` is the matching camera with the flag disabled.

- Forward and reverse controller walks: **PASS**, 42.2 m each, including the Guild approach. Skyport jump: **PASS**, one jump and one landing. See `route-forward.json`, `route-reverse.json` and `route-jump.json` for sampled traces and camera distances.
- At the Guild the actual E interaction opened **Transit accessibility in DKI Jakarta**; closing the panel returned to exploration. At the skyport, E triggered the preview; Escape restored the original player coordinates and controls. Reduced motion returned to idle in under one second without the cinematic camera movement.
- Flag-off local run made no `dragon.glb` request. The enabled run requested it once. The scene reported one renderer. No warnings or errors were recorded in the saved route and performance evidence. An initial temporary implementation error was corrected before this evidence.
- Existing scoped tests: 24 passed; new boarding flag/GLB checks: 2 passed. These tests do not establish artistic approval. Visibility-change cancellation and an actual network failure were not independently exercised in the browser.

## Rendering costs

Same `skyportaerial` camera, viewport 1280 × 656, pixel ratio 1, standard quality, shadows enabled, after warmup, 600 frame samples per configuration on the available local Apple Silicon desktop. Numbers are animation-frame intervals, not GPU timings. Different timing samples are not a controlled laboratory benchmark.

| | C3.1 baseline | R0-D1 enabled |
|---|---:|---:|
| Median frame interval | 5.5 ms | 5.6 ms |
| p95 frame interval | 6.3 ms | 6.0 ms |
| All-pass draw calls | 409 | 411 |
| All-pass submitted triangles | 2,607,520 | 2,616,644 |

The 9,124 submitted-triangle increase includes both visible and shadow passes. `performance-on.json` and `performance-off.json` contain settings, counters and resource records. No mobile device was tested.

## Rollback

Remove `skyport-demo=r0d1` from the URL or use the prior C3.1 development URL. The dragon is not requested and no new interaction is installed without this flag and the prerequisite local flags. The default/public site remains unchanged. For code rollback, remove the boarding import/catalog/initialization/update/interaction/cleanup hooks in `entry.js`, then remove `skyport-boarding.js`, the dragon GLB and this validation directory; leave the pre-existing C3.1 files intact. No public deployment was performed.
