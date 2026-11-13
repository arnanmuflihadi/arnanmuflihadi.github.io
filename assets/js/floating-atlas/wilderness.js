import * as T from '../vendor/three-atlas.module.js?v=16';

export const sites=Object.freeze([{id:'cloudbreak',x:-80,z:5,radius:1.8,title:'Cloudbreak Overlook',text:'Clouds gather beneath the island while the forest trail winds back toward town. This observation is part of the fictional world.'},{id:'crown-ridge',x:-43.04,z:-48.2,radius:1.2,title:'Crown Ridge',text:'From the ridge, the forest gives way to the roofs of town. The winding trail leads back down through the valley. This observation belongs to the fictional world.'}]);
export function restoreDiscovery(value){const valid=value?.type==='transit-discoveries'&&value.version===1&&value.realm==='transit';return {type:'transit-discoveries',version:1,realm:'transit',visited:valid&&Array.isArray(value.visited)?sites.map(s=>s.id).filter(id=>value.visited.includes(id)):[]};}
export function nearestDiscovery(position,grounded,heightAt,obstacles,blocked){if(!position||!grounded)return null;return sites.find(s=>Math.hypot(position.x-s.x,position.z-s.z)<s.radius&&Math.abs(position.y-heightAt(s.x,s.z))<.8&&!blocked(s.x,s.z,obstacles)&&Array.from({length:5},(_,i)=>{const t=(i+1)/6;return !blocked(position.x+(s.x-position.x)*t,position.z+(s.z-position.z)*t,obstacles);}).every(Boolean))||null;}
export function createWilderness(world,heightAt){
 const root=new T.Group();root.name='Wilderness observations / local review';
 const stone=new T.MeshStandardMaterial({color:'#9d9076',roughness:1}),bronze=new T.MeshStandardMaterial({color:'#987949',roughness:.78,metalness:.18});
 const postGeometry=new T.BoxGeometry(.18,.75,.18),plaqueGeometry=new T.BoxGeometry(.68,.32,.08),inlayGeometry=new T.BoxGeometry(.42,.035,.095),ridgeGeometry=new T.CylinderGeometry(.09,.16,.8,4),capGeometry=new T.ConeGeometry(.22,.25,4);
 const post=new T.Group(),shaft=new T.Mesh(postGeometry,stone),plaque=new T.Mesh(plaqueGeometry,stone),inlay=new T.Mesh(inlayGeometry,bronze);shaft.position.y=.38;plaque.position.y=.78;inlay.position.set(0,.78,.01);post.add(shaft,plaque,inlay);post.rotation.y=-.65;post.position.set(-78.5,heightAt(-78.5,6.2),6.2);root.add(post);
 const ridge=new T.Group(),ridgeStone=new T.Mesh(ridgeGeometry,stone),ridgeCap=new T.Mesh(capGeometry,bronze);ridgeStone.position.y=.4;ridgeCap.position.y=.9;ridge.add(ridgeStone,ridgeCap);ridge.position.set(-41.8,heightAt(-41.8,-47.1),-47.1);ridge.rotation.y=.55;root.add(ridge);world.scene.add(root);
 return{dispose(){root.removeFromParent();for(const g of [postGeometry,plaqueGeometry,inlayGeometry,ridgeGeometry,capGeometry])g.dispose();stone.dispose();bronze.dispose();}};
}
