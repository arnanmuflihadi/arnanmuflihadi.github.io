#!/usr/bin/env node
// Asset authoring only. All runtime files remain local, self-contained GLBs.
import{resolve}from'node:path';import{pathToFileURL}from'node:url';
import{readFile,writeFile,mkdir,copyFile}from'node:fs/promises';import{createHash}from'node:crypto';
const arg=n=>{const i=process.argv.indexOf(n);if(i<0)throw Error(`Required ${n}`);return resolve(process.argv[i+1]);};
const deps=arg('--deps'),source=arg('--source');
for(const name of ['core','functions']){const pkg=JSON.parse(await readFile(resolve(deps,`@gltf-transform/${name}/package.json`),'utf8'));if(pkg.version!=='4.2.1')throw Error(`Expected @gltf-transform/${name}@4.2.1`);}
const{NodeIO}=await import(pathToFileURL(resolve(deps,'@gltf-transform/core/dist/index.modern.js')));
const{dedup,prune}=await import(pathToFileURL(resolve(deps,'@gltf-transform/functions/dist/functions.modern.js')));
const hash=b=>createHash('sha256').update(b).digest('hex'),io=new NodeIO();
const sourcePins={'Casual.gltf':'55c654d09a2a5ff6e3bd6158d4a1b462f181cd6f1e12a0f5e9d959f9c3abc438','Adventurer.gltf':'21f7a61afb6bd6cef6961490c367594e3c2fc01ec1f041662131172ce763063e','MushroomKing.gltf':'ccf27e126b881d80a2046c3ab96ddd94eb996837480e783142009ecd6629a3a4'};
const specifications=[
 {id:'city-resident',file:'Casual.gltf',page:'https://quaternius.com/packs/ultimatemodularcharacters.html',clips:{Idle_Neutral:'Idle',Walk:'Walk',Run:'Run',Wave:'Wave',Interact:'Interact'}},
 {id:'explorer-actions',file:'Adventurer.gltf',page:'https://quaternius.com/packs/ultimatemodularcharacters.html',clips:{Punch_Left:'Attack1',Punch_Right:'Attack2',Roll:'Dodge',HitRecieve:'Hit',Death:'Defeat',Idle_Sword:'Guard'},animationOnly:true},
 {id:'mosskeeper',file:'MushroomKing.gltf',page:'https://quaternius.com/packs/ultimatemonsters.html',clips:{Idle:'Idle',Walk:'Walk',Run:'Run',Punch:'Attack',HitReact:'Hit',Death:'Defeat'}},
];
await mkdir('assets/game/phase3',{recursive:true});const models=[];
for(const spec of specifications){
 const path=resolve(source,spec.file),bytes=await readFile(path),doc=await io.read(path),root=doc.getRoot();
 if(hash(bytes)!==sourcePins[spec.file])throw Error('Source differs from the reviewed file: '+spec.file);
 for(const animation of [...root.listAnimations()]){
  const name=spec.clips[animation.getName()];if(!name){animation.dispose();continue;}animation.setName(name);
  for(const c of animation.listChannels())if(c.getTargetNode()?.getName()==='Root'&&c.getTargetPath()==='translation'){
   const output=c.getSampler().getOutput(),a=output.getArray().slice();for(let i=0;i<a.length;i+=3){a[i]=a[0];a[i+2]=a[2];}output.setArray(a);
  }
 }
 if(root.listAnimations().length!==Object.keys(spec.clips).length)throw Error('Missing authored clips: '+spec.id);
 if(spec.animationOnly){root.listMeshes().forEach(m=>m.dispose());root.listSkins().forEach(s=>s.dispose());}
 for(const m of root.listMaterials())m.setMetallicFactor(0).setRoughnessFactor(.9);
 await doc.transform(dedup(),prune({keepLeaves:true}));
 const output=`assets/game/phase3/${spec.id}.glb`;await io.write(output,doc);const result=await readFile(output);
 models.push({id:spec.id,source:spec.page,sourceFile:spec.file,author:'Quaternius',license:'CC0-1.0',sourceSha256:hash(bytes),outputSha256:hash(result),bytes:result.length,animationOnly:Boolean(spec.animationOnly),clips:spec.clips,changes:['Retain selected authored clips and original matching rig; rename actions','Hold animated horizontal Root translation constant where present; retain authored body motion','Matte nonmetallic materials; deduplicate/prune; embed all buffers and images']});
}
await copyFile(resolve(source,'License.txt'),'assets/game/phase3/CC0-Monsters.txt');
await copyFile('assets/game/characters/urban-explorer/CC0-Quaternius.txt','assets/game/phase3/CC0-Characters.txt');
await writeFile('assets/game/phase3/source.json',JSON.stringify({models},null,2)+'\n');console.log(models.map(m=>({id:m.id,bytes:m.bytes,clips:m.clips})));
