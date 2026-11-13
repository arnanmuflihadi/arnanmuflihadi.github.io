import * as T from '../vendor/three-atlas.module.js?v=16';

export const sites=Object.freeze([{id:'cloudbreak',x:-80,z:5,radius:1.8,title:'Cloudbreak Overlook',text:'Clouds gather beneath the island while the forest trail winds back toward town. This observation is part of the fictional world.'}]);
export function restoreDiscovery(value){const valid=value?.type==='transit-discoveries'&&value.version===1&&value.realm==='transit';return {type:'transit-discoveries',version:1,realm:'transit',visited:valid&&Array.isArray(value.visited)?sites.map(s=>s.id).filter(id=>value.visited.includes(id)):[]};}
export function nearestDiscovery(position,grounded,heightAt,obstacles,blocked){if(!position||!grounded)return null;return sites.find(s=>Math.hypot(position.x-s.x,position.z-s.z)<s.radius&&Math.abs(position.y-heightAt(s.x,s.z))<.8&&!blocked(s.x,s.z,obstacles))||null;}
export function createWilderness(world,heightAt){
 const root=new T.Group();root.name='Cloudbreak observation / local review';
 const stone=new T.MeshStandardMaterial({color:'#a89470',roughness:1}),bronze=new T.MeshStandardMaterial({color:'#8a6c40',roughness:.8,metalness:.25});
 const geometry=new T.CylinderGeometry(.65,.7,.12,12),ringGeometry=new T.TorusGeometry(.48,.035,5,24);
 const marker=new T.Group(),disc=new T.Mesh(geometry,stone),ring=new T.Mesh(ringGeometry,bronze);ring.rotation.x=-Math.PI/2;ring.position.y=.075;marker.add(disc,ring);marker.position.set(-80,heightAt(-80,5)+.07,5);root.add(marker);world.scene.add(root);
 return{dispose(){root.removeFromParent();geometry.dispose();ringGeometry.dispose();stone.dispose();bronze.dispose();}};
}
