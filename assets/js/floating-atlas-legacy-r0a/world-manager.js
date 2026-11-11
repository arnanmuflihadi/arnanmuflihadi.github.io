import{worldId}from'./plan.js?v=63';
import{createFloatingWorld}from'./scene.js?v=63';
export function createWorldManager({load=createFloatingWorld}={}){
 let current=null,pending=null,abort=null,disposed=false,generation=0;
 return{async load(id=worldId,options={}){if(disposed)throw Error('World manager disposed');if(id!==worldId)throw Error('This realm is not constructed');if(current)return current;if(!pending){const controller=new AbortController(),ticket=++generation;abort=controller;pending=load({...options,signal:controller.signal}).then(world=>{if(disposed||controller.signal.aborted||ticket!==generation){world.dispose();throw Error('World load cancelled');}current=world;return world;}).catch(error=>{if(ticket===generation)pending=null;throw error;});}return pending;},get current(){return current;},unload(){generation++;abort?.abort();current?.dispose();current=null;pending=null;},dispose(){if(disposed)return;disposed=true;generation++;abort?.abort();current?.dispose();current=null;pending=null;}};
}
