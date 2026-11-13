#!/usr/bin/env node
// Shared editorial/adventure renderer; authoring dependencies never ship at runtime.
import { readFile, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
const index = process.argv.indexOf('--deps');
if (index < 0) throw new Error('Pass --deps /absolute/path/to/node_modules');
const deps = resolve(process.argv[index + 1]);
for (const [name, version] of [['three', '0.180.0'], ['esbuild', '0.25.10']]) {
  if (JSON.parse(await readFile(resolve(deps, name, 'package.json'), 'utf8')).version !== version) throw new Error(`Expected ${name}@${version}`);
}
const { build } = await import(pathToFileURL(resolve(deps, 'esbuild/lib/main.js')));
const names = `Scene PerspectiveCamera WebGLRenderer Group Mesh BoxGeometry SphereGeometry CylinderGeometry PlaneGeometry ConeGeometry TorusGeometry LatheGeometry ExtrudeGeometry Shape BufferGeometry Float32BufferAttribute Vector2 Vector3 Color Fog ShaderMaterial MeshToonMaterial MeshBasicMaterial MeshStandardMaterial HemisphereLight DirectionalLight AmbientLight CanvasTexture DataTexture RedFormat LinearFilter SRGBColorSpace ACESFilmicToneMapping PCFSoftShadowMap Raycaster InstancedMesh Object3D DoubleSide BackSide MathUtils AnimationMixer Box3 LoopRepeat LoopOnce`;
const output = 'assets/js/vendor/three-atlas.module.js';
await build({ stdin: { contents: `export { ${names.split(' ').join(',')} } from 'three'; export { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js'; export { clone as cloneSkeleton } from 'three/addons/utils/SkeletonUtils.js';`, resolveDir: deps }, bundle: true, minify: true, format: 'esm', outfile: output, banner: { js: '/*! Three.js 0.180.0 | MIT | Living Urban Atlas | See THREE-LICENSE.txt */' } });
await writeFile(output, (await readFile(output, 'utf8')).replace(/[ \t]+$/gm, ''));
