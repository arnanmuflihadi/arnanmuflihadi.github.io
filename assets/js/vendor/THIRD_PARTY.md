# Local browser libraries

| Library | Version | Source | License | SHA-256 |
| --- | --- | --- | --- | --- |
| GSAP | 3.13.0 | jsDelivr npm mirror | Standard GSAP license | `96c01b81f44a3290e2b4532f55e2c9534b2adc43273a19f3756b2cb41f0fd0b6` |
| ScrollTrigger | 3.13.0 | jsDelivr npm mirror | Standard GSAP license | `308219390e5e3b84cda0c481e70caa9820883ae10bda44e6e9a149a81aac4b3f` |
| Lenis | 1.3.23 | jsDelivr npm mirror | MIT | `1375bb5f82062a5ba4ccb2ec5b420ee41578abf4ec04673a6bcfa6714b95f885` |
| Three.js home subset | 0.180.0 | npm registry; curated local IIFE build | MIT, `THREE-LICENSE.txt` | `cec9da7ff6f46d2ad9f97893c3d35dfeb97beb11bc4389b22b78040df69b1baa` |

The Three.js subset loads on Home, Work, About and News. It supports the original
procedural analyst and contextual spatial models, not downloaded models.
The map adds shape extrusion, a curved route, and node rings to that same build.
No controls, model loaders,
post-processing, physics, or new animation scheduler are included. Reproduce
with `scripts/build-hero-3d.mjs`; its temporary build tools are not deployed.

## Jakarta RPG renderer

`three-rpg.module.js` is a separate, lazy-loaded ES-module build of Three.js
0.180.0 from the npm registry, licensed under MIT (`THREE-LICENSE.txt`).
SHA-256: `4c4cecf61de6492c8cf43c7780d9c2a0d898ba7a43d8da767fc8d06cb733dbe3`.
Rebuild with `scripts/build-rpg-vendor.mjs --deps <temporary node_modules>` using
`three@0.180.0` and `esbuild@0.25.10`. It exposes perspective cameras, raycasting,
instancing, and canvas sign textures; the original hero subset remains unchanged.
No external controls, physics, model, texture, or asset libraries are required.
The second renderer module is requested only after explicit 3D activation or an
RPG deep link; all game geometry, signage, and character animation are original.

## Current Living Urban Atlas runtime

Home and Work use `three-atlas.module.js`: Three.js 0.180.0, GLTFLoader,
AnimationMixer, loop modes and the official SkeletonUtils clone helper. All are
from the pinned `three@0.180.0` npm package under MIT (`THREE-LICENSE.txt`).
SHA-256: `e8fdf00ae6ebc1d0f005da87ce61ab171637c8f3119298742e68dcb7a9c70a01`.
Reproduce with `scripts/build-atlas-vendor.mjs --deps <temporary node_modules>`,
using esbuild 0.25.10. Authored runtime modules use consistent `?v=22` URLs;
the unchanged vendor retains its shared `?v=16` URL. Character and scenery models are separately
licensed; their original notices and per-file manifests live under `assets/game/`.

The home-subset and early RPG descriptions above are historical. Home/Work no
longer import those older renderers. About/News keep their decorative hero subset;
the early RPG module remains retained development work.

## Current repair assets

`assets/game/scenery/architecture-library.glb` contains eleven selected glTF
templates from Quaternius Downtown City MegaKit Standard, CC0-1.0. The original
Standard license is retained as `downtown-city-megakit-LICENSE.txt`; filenames,
source/output hashes, conversions and footprints are in `architecture-source.json`.
The street pass adds `Prop_Drain.gltf` and `Prop_ManholeCover.gltf` and uses
`Sidewalk_NoCurb_3m.gltf` for level interior paving. It adds no texture images.
Roof eaves, balcony rails, cycle stands, signs and café tables are project-authored
geometry rather than downloaded models. No Nintendo assets, fonts or glyphs are used.

`assets/game/characters/urban-explorer/jump-animations.glb` contains three
retargeted clips from Quaternius Universal Animation Library Standard, CC0-1.0.
The original license is `jump-LICENSE.txt`; source/target/output hashes and the
retargeting procedure are recorded in `jump-source.json`. No library mannequin
mesh or texture is delivered. The explorer and resident model notices remain
beside their existing manifests.

## Isolated Phase 1 asset review

`asset-showcase.html` reuses the verified CC0 scenery files listed in
[`ASSET_MANIFEST.md`](../../../ASSET_MANIFEST.md). Official free Standard city and
nature archives were downloaded again on 1 November 2026. Fourteen selected glTF
files, all referenced buffers/images and both included licenses were checked;
archive and dependency digests are in `assets/game/scenery/verification.json`.
The runtime palette disables Downtown's engine-specific vertex-color wear masks,
uses warm masonry and matte mineral trim, and keeps muted opaque glass.
Kenney Commercial was evaluated but no Kenney model is imported: its official
archive returned HTTP 403 during this review. Paid Quaternius Pro/Source assets
are not included. The showcase uses the unchanged Three.js vendor URL `?v=16`.

Phase 1.5 retains those same GLBs and notices. The original architectural layers,
procedural mineral/glass textures, fictional canopy lettering and direct browser
captures are project-authored additions. `architecture-enhancements.json` records
their source relationship and generator digest. No architectural reference photo,
model, shader or font was downloaded from the reference practices. Imported source
geometry remains CC0; added project work is identified separately in the manifest.
