# Urban Atlas — asset provenance

The district architecture, vegetation, landscape, signs, sky and street furniture
remain original parametric assets authored in this project. No Nintendo content,
commercial asset packs or generated images are used.

## Imported explorer character

The former procedural figure has been replaced with Quaternius’s **Adventurer**
from the [Ultimate Modular Men pack](https://quaternius.com/packs/ultimatemodularcharacters.html).
It is a real imported humanoid skinned mesh with 62 joints and matching animations,
not reconstructed primitive geometry. See `assets/game/characters/urban-explorer/`:

- `urban-explorer.glb`: self-contained derivative; 10,202 triangles and three clips.
- `CC0-Quaternius.txt`: original downloaded **CC0 1.0** license notice.
- `source.json`: original download URL, source/output checksums and modifications.

Clothing, hair, footwear and pack colors were adapted to the city palette. Skin,
geometry, skeleton hierarchy, inverse bind matrices and skin weights are preserved.
Only the matching Idle_Neutral, Walk and Run clips are retained; no retargeting.
Original embedded standard materials remain in use, with nonmetallic roughness.
The source is material-colored and has no raster textures or normal maps.

Reproduce the asset with `scripts/prepare-atlas-character.mjs`; source and dependency
instructions are in `docs/CHARACTER-OVERHAUL.md`. The earlier Stage 1 review captures
record the superseded procedural character and remain as historical artifacts.

## Original environment

- `geometry.js`: chamfered footprints, closed roof shells, gables, arcades, fronds.
- `architecture.js`: tropical-modern station, office landmark, shops and pavilion.
- `environment.js`: landscape, paving, rain garden, sculpture, foliage and sky.
- `materials.js`: shared environment toon materials and procedural pigment wash.
- Signage uses locally drawn canvas textures with browser system fonts.

## Renderer and loader

`three-atlas.module.js` locally bundles **Three.js 0.180.0**, including its official
GLTFLoader and AnimationMixer, from the npm registry, under **MIT**. Keep
`assets/js/vendor/THREE-LICENSE.txt`. All parts share the same Three.js runtime.

SHA-256: `d4814cb06247e46f5b3d01251cf95489c42247641ee081236de7caf50c55e662`.

Rebuild with `scripts/build-atlas-vendor.mjs --deps <node_modules>` using temporary
`three@0.180.0` and `esbuild@0.25.10`. No npm dependencies are required at runtime.
