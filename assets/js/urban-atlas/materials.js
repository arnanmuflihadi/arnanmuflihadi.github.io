import * as T from '../vendor/three-atlas.module.js?v=16';
export const palette = {
  plaster: '#f2dfb7', ivory: '#fff0cf', stone: '#d5c5a3', sand: '#c6b58c',
  terra: '#b7654c', roof: '#914e3f', teal: '#377f80', glass: '#4f9291',
  glassLight: '#8eb9a4', timber: '#77543c', dark: '#294d48', road: '#576a69',
  grass: '#8eac72', leaf: '#578361', leafLight: '#80a26b', leafDark: '#36654f',
};
export function createMaterials() {
  const ramp = new T.DataTexture(new Uint8Array([98, 133, 189, 236, 255]), 5, 1, T.RedFormat);
  ramp.minFilter = ramp.magFilter = T.LinearFilter; ramp.needsUpdate = true;
  const cache = new Map();
  const toon = (color, options = {}) => {
    const key = color + JSON.stringify(options);
    if (!cache.has(key)) {
      const material = new T.MeshToonMaterial({ color, gradientMap: ramp, ...options });
      // Broad, restrained pigment washes add surface variation without textures.
      material.onBeforeCompile = shader => {
        shader.vertexShader = 'varying vec3 vAtlasWorld;\n' + shader.vertexShader;
        shader.vertexShader = shader.vertexShader.replace('#include <begin_vertex>', `#include <begin_vertex>
          vec4 atlasPosition = vec4(transformed, 1.0);
          #ifdef USE_INSTANCING
            atlasPosition = instanceMatrix * atlasPosition;
          #endif
          vAtlasWorld = (modelMatrix * atlasPosition).xyz;`);
        shader.fragmentShader = 'varying vec3 vAtlasWorld;\n' + shader.fragmentShader;
        shader.fragmentShader = shader.fragmentShader.replace('#include <color_fragment>', `#include <color_fragment>
          float pigment = sin(vAtlasWorld.x * .72 + sin(vAtlasWorld.z * .41)) * sin(vAtlasWorld.y * .65 + vAtlasWorld.z * .17);
          diffuseColor.rgb *= .96 + .025 * pigment + .04 * clamp(vAtlasWorld.y / 18.0, 0.0, 1.0);`);
      };
      if ([palette.leaf, palette.leafLight, palette.leafDark].includes(color)) material.userData.noReceiveShadow = true;
      material.customProgramCacheKey = () => 'atlas-pigment-wash-v1';
      cache.set(key, material);
    }
    return cache.get(key);
  };
  return { toon, ramp, cache, dispose() { ramp.dispose(); cache.forEach(m => m.dispose()); } };
}
