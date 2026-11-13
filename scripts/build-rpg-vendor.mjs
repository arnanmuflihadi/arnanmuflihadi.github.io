#!/usr/bin/env node
// One-time static vendor build. Runtime deployment does not require npm.
import {readFile,writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
const flag=process.argv.indexOf('--deps');
if(flag<0)throw new Error('Use --deps /absolute/path/to/node_modules');
const deps=resolve(process.argv[flag+1]);
for(const [name,version] of [['three','0.180.0'],['esbuild','0.25.10']]){
 const pkg=JSON.parse(await readFile(resolve(deps,name,'package.json'),'utf8'));
 if(pkg.version!==version)throw new Error(`Expected ${name}@${version}`);
}
const {build}=await import(pathToFileURL(resolve(deps,'esbuild/lib/main.js')));
await build({stdin:{contents:"export {Scene,PerspectiveCamera,WebGLRenderer,Group,Mesh,BoxGeometry,SphereGeometry,CylinderGeometry,PlaneGeometry,CanvasTexture,SRGBColorSpace,ACESFilmicToneMapping,MeshStandardMaterial,MeshBasicMaterial,HemisphereLight,DirectionalLight,Color,Fog,Vector3,Raycaster,InstancedMesh,Object3D} from 'three'",resolveDir:deps},bundle:true,minify:true,format:'esm',outfile:'assets/js/vendor/three-rpg.module.js',banner:{js:'/*! Three.js r180, MIT. Isolated RPG renderer. See THREE-LICENSE.txt. */'}});

// Remove insignificant trailing whitespace in bundled shader template strings.
const output='assets/js/vendor/three-rpg.module.js';
await writeFile(output,(await readFile(output,'utf8')).replace(/[ \t]+$/gm,''));
