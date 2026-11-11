#!/usr/bin/env node
/** Official Quaternius Adventurer -> self-contained, animation-trimmed GLB.
 * node scripts/prepare-atlas-character.mjs --source /path/Adventurer.gltf --deps /path/node_modules
 * Temporary dependencies: @gltf-transform/core@4.2.1 @gltf-transform/functions@4.2.1
 */
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const arg=name=>{const i=process.argv.indexOf(name);if(i<0)throw new Error(`Required ${name}`);return resolve(process.argv[i+1]);};
const source=arg('--source'),deps=arg('--deps');
const sha=bytes=>createHash('sha256').update(bytes).digest('hex');
const sourceBytes=await readFile(source);
if(sha(sourceBytes)!=='21f7a61afb6bd6cef6961490c367594e3c2fc01ec1f041662131172ce763063e')throw new Error('Source differs from the reviewed Quaternius Adventurer.gltf');
for(const name of ['core','functions']){
 const pkg=JSON.parse(await readFile(resolve(deps,`@gltf-transform/${name}/package.json`),'utf8'));
 if(pkg.version!=='4.2.1')throw new Error(`Expected @gltf-transform/${name}@4.2.1`);
}
const {NodeIO}=await import(pathToFileURL(resolve(deps,'@gltf-transform/core/dist/index.modern.js')));
const {dedup,prune}=await import(pathToFileURL(resolve(deps,'@gltf-transform/functions/dist/functions.modern.js')));
const io=new NodeIO(),doc=await io.read(source),root=doc.getRoot();
const required=new Map([['Idle_Neutral','Idle'],['Walk','Walk'],['Run','Run']]);
for(const animation of [...root.listAnimations()]){
 const name=required.get(animation.getName());if(!name){animation.dispose();continue;}
 animation.setName(name);
 // Root displacement is removed on horizontal axes; skeleton and vertical gait remain.
 for(const channel of animation.listChannels())if(channel.getTargetNode()?.getName()==='Root'&&channel.getTargetPath()==='translation'){
   const accessor=channel.getSampler().getOutput(),array=accessor.getArray().slice();
   for(let i=0;i<array.length;i+=3){array[i]=array[0];array[i+2]=array[2];}
   accessor.setArray(array);
 }
}
if(root.listAnimations().length!==3)throw new Error('Missing source locomotion clips');
const palette={Green:'#3d6370',LightGreen:'#819276',Brown:'#767065',Brown2:'#59594e',Gold:'#b5a47a',Grey:'#c5beac',Black:'#353d40',Hair:'#433c35',Eyebrows:'#433c35'};
const linear=v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4;
for(const material of root.listMaterials()){
 if(palette[material.getName()]){const hex=palette[material.getName()].slice(1);material.setBaseColorFactor([0,2,4].map(i=>linear(parseInt(hex.slice(i,i+2),16)/255)).concat(1));}
 material.setMetallicFactor(0).setRoughnessFactor(.9);
}
await doc.transform(dedup(),prune({keepLeaves:true}));
const output='assets/game/characters/urban-explorer/urban-explorer.glb';await io.write(output,doc);
const manifest={source:'https://quaternius.com/packs/ultimatemodularcharacters.html',sourceFile:'Individual Characters/glTF/Adventurer.gltf',sourceDownload:'https://drive.google.com/uc?export=download&id=1fzSq1Rr037f7QkfXPWEAzmbLMNx-FpPA',author:'Quaternius',license:'CC0-1.0',licenseUrl:'https://creativecommons.org/publicdomain/zero/1.0/',sourceSha256:sha(sourceBytes),outputSha256:sha(await readFile(output)),changes:['Keep matching Idle_Neutral, Walk and Run; rename idle to Idle','Remove horizontal Root translation to produce in-place locomotion','Recolor clothing, boots, hair and backpack; preserve skin, geometry, bind poses and weights','Set nonmetallic rough materials; deduplicate and prune unused animation data'],animations:root.listAnimations().map(a=>a.getName()),skins:root.listSkins().map(s=>({name:s.getName(),joints:s.listJoints().length}))};
await writeFile('assets/game/characters/urban-explorer/source.json',JSON.stringify(manifest,null,2)+'\n');console.log(manifest);
