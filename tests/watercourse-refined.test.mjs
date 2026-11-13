import test from 'node:test';
import assert from 'node:assert/strict';
import {channelGeometry,watercourseFixEnabled} from '../assets/js/floating-atlas/waterfall.js';
import {groundHeight} from '../assets/js/floating-atlas/terrain.js';

test('refined stream is local opt-in and follows the sampled banks continuously',()=>{
 assert.equal(watercourseFixEnabled('http://localhost:4202/?watercourse=refined'),true);
 assert.equal(watercourseFixEnabled('https://example.com/?watercourse=refined'),false);
 assert.equal(watercourseFixEnabled('http://localhost:4202/'),false);
 const g=channelGeometry(true);
 try{const p=g.getAttribute('position');assert.equal(p.count,322);
  for(let i=0;i<p.count;i++){
   const x=p.getX(i),z=p.getZ(i),ground=groundHeight(x,z);
   if(ground>0)assert.ok(Math.abs(p.getY(i)-ground-.075)<.001);
   if(i>=2)assert.ok(Math.hypot(x-p.getX(i-2),z-p.getZ(i-2))<1);
  }
 }finally{g.dispose();}
});
