import test from 'node:test';
import assert from 'node:assert/strict';
import {placements} from '../assets/js/floating-atlas/town-population.js';

test('square chairs face their table and tabletop items use their supporting surface',()=>{
 const chairs=placements.filter(p=>p.id==='chair'&&p.v===22.6).sort((a,b)=>a.u-b.u);
 assert.equal(chairs.length,2);
 assert.equal(chairs[0].turn,Math.PI/2);
 assert.equal(chairs[1].turn,-Math.PI/2);
 for(const p of placements.filter(p=>['cup-saucer','cup-coffee','plate','croissant','coconut-half'].includes(p.id))){
  assert.ok(p.support,`${p.id} needs its table as a height reference`);
  assert.ok(placements.some(table=>table.id==='tableRound'&&table.u===p.support[0]&&table.v===p.support[1]));
 }
});
