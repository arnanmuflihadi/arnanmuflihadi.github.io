# Reference-to-implementation record

Inspected 2 November 2026. Sky Isles and Leonardo Sato were inspected first.
No repositories were cloned. Selected source was read through GitHub; no code,
model, texture, sound, branding or recognizable composition was copied.

| Reference / inspected source | Technique and intended use | Code rights | Asset rights / decision |
| --- | --- | --- | --- |
| [Sky Isles: `src/world/islands.js`](https://github.com/stas4000/sky-isles/blob/main/src/world/islands.js), [`clouds.js`](https://github.com/stas4000/sky-isles/blob/main/src/world/clouds.js) | Separate vegetated top and layered underside; cloud banks at multiple altitudes for depth. Our continuous chiseled mesh and analytic cloud shader are independently written. Circular platforms, copied palette, gliding and jump pads rejected. | Root [LICENSE](https://github.com/stas4000/sky-isles/blob/main/LICENSE) verified MIT, Stanislav Sorokin, 2026. | README says zero binary assets and procedural generation. No reference assets imported. Existing Quaternius plants used instead. |
| [Leonardo Sato: `src/scene/ProceduralGrass.ts`](https://github.com/satoLG/portfolio/blob/main/src/scene/ProceduralGrass.ts), [`SkyboxShader.ts`](https://github.com/satoLG/portfolio/blob/main/src/shaders/SkyboxShader.ts) | Batch real blade geometry; move tips with a wind uniform; interpolate horizon/zenith by altitude. Our six-vertex tapered blades, distribution, wind expression and daylight shader are original. | README claims MIT; root directory has no LICENSE file. Treat reuse rights as unconfirmed and copy no code. | No separate model/texture license verified. No assets imported. No ocean, PWA, physics engine or postprocessing migration. |
| [Mehmet: README](https://github.com/xenitV1/mehmet-3d-portfolio/blob/main/README.md), [`js/engine/registry.js`](https://github.com/xenitV1/mehmet-3d-portfolio/blob/main/js/engine/registry.js), [`interaction.js`](https://github.com/xenitV1/mehmet-3d-portfolio/blob/main/js/engine/interaction.js) | Keep collision and content triggers separate. Existing atlas registry, guide and research panels already meet this need; retain them. Village architecture belongs to a later phase and is not reproduced. | No LICENSE file in root; GitHub license metadata is null. No reuse permitted on the evidence inspected. | No asset permission established; nothing imported. |
| [Platform of Things: README](https://github.com/rexchoppers/platform-of-things/blob/master/README.md), [`src/core/SceneManager.ts`](https://github.com/rexchoppers/platform-of-things/blob/master/src/core/SceneManager.ts) | One renderer/camera owner, DPR control and world-specific atmosphere. Retain current world-manager lifecycle; future transitions remain disabled. | Root [LICENSE](https://github.com/rexchoppers/platform-of-things/blob/master/LICENSE) verified MIT, Rexchoppers, 2026. | [CREDITS](https://github.com/rexchoppers/platform-of-things/blob/master/CREDITS.md) distinguishes music CC BY-ND and logos under various licenses/trademark restrictions. They are not blanket MIT assets. Nothing imported. |
| [Bruno Simon: readme](https://github.com/brunosimon/folio-2025/blob/main/readme.md), [`Fog.js`](https://github.com/brunosimon/folio-2025/blob/main/sources/Game/Fog.js), [`Quality.js`](https://github.com/brunosimon/folio-2025/blob/main/sources/Game/Quality.js), [`ResourcesLoader.js`](https://github.com/brunosimon/folio-2025/blob/main/sources/Game/ResourcesLoader.js) | Coordinate fog/background colors, explicit quality changes and cached resources. Retain atlas cache/quality controls; tune atmospheric distance to this island. | Root [license.md](https://github.com/brunosimon/folio-2025/blob/main/license.md) verified MIT, Bruno Simon, 2025. | Separate model/music/texture rights not established by the selected files. No assets imported. No TSL/WebGPU migration or driving mechanics. |

## Assets actually shipped

The active landscape requests only the existing `canopy-tree.glb` and `fern.glb`,
from Quaternius Stylized Nature MegaKit, CC0, with the original source record,
license text and hashes retained. Existing player, jump and Nadia GLBs stay under
their previously recorded Quaternius CC0 provenance. The architecture library
and all of its source licenses stay on disk, but are absent from active loading.
Terrain, rock formations, palms, grass, trails, stream, clouds and sky are
project-authored. No new third-party files or dependencies were downloaded.
