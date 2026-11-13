import {writeFileSync}from'node:fs';
import{fixture}from'../terrain-c1a5/fixture.mjs';
const f=await fixture(),a=f.world.terrain.geometry.attributes.position;
writeFileSync(new URL('terrain-vertices.json',import.meta.url),JSON.stringify(Array.from({length:a.count},(_,i)=>[a.getX(i)-36,44-a.getZ(i),a.getY(i)-18.6])));
writeFileSync(new URL('terrain-updates.json',import.meta.url),JSON.stringify(f.town.terrain.changed.map(r=>[r.index,r.x-36,44-r.z,r.after-18.6])));console.log(a.count);f.dispose();
