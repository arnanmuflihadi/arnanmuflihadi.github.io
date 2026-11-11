import test from 'node:test';
import assert from 'node:assert/strict';
import {restoreDiscovery,nearestDiscovery} from '../assets/js/floating-atlas/wilderness.js';
const height=()=>32, free=()=>false, at={x:-80,y:32,z:5};
test('discovery saves reject invalid data and deduplicate recognized discoveries',()=>{
 assert.deepEqual(restoreDiscovery({version:1,realm:'transit',visited:['cloudbreak']}).visited,[]);
 assert.deepEqual(restoreDiscovery({type:'transit-discoveries',version:1,realm:'transit',visited:['cloudbreak','cloudbreak','unknown','crown-ridge']}).visited,['cloudbreak','crown-ridge']);
});
test('observation requires grounded nearby player, matching elevation and a clear destination',()=>{
 assert.equal(nearestDiscovery(at,true,height,[],free)?.id,'cloudbreak');
 assert.equal(nearestDiscovery({...at,x:-75},true,height,[],free),null);
 assert.equal(nearestDiscovery({...at,y:40},true,height,[],free),null);
 assert.equal(nearestDiscovery(at,false,height,[],free),null);
 assert.equal(nearestDiscovery(at,true,height,[],()=>true),null);
 assert.equal(nearestDiscovery({...at,x:-81},true,height,[],x=>x > -80.7 && x < -80.4),null,'an intervening obstacle blocks interaction');
});
