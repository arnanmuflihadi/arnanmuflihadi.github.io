import {projectById} from './project-registry.js?v=22';
export function readAtlasRoute(value){
  const url=new URL(value),p=url.searchParams;
  const activeProject=projectById(p.get('project'))?.id||null;
  return {mode:['adventure','rpg'].includes(p.get('experience'))?'adventure':'editorial',activeProject,panelOpen:Boolean(activeProject&&p.get('panel')==='study')};
}
export function atlasRoute(value,state){
  const url=new URL(value);for(const key of ['experience','project','panel'])url.searchParams.delete(key);
  if(state.mode==='adventure')url.searchParams.set('experience','adventure');
  if(projectById(state.activeProject))url.searchParams.set('project',state.activeProject);
  if(state.panelOpen&&state.activeProject)url.searchParams.set('panel','study');
  return url;
}
export function createAtlasState(route,saved={}){
  const p=saved?.playerPosition,valid=p&&Number.isFinite(p.x)&&Number.isFinite(p.z)&&Math.abs(p.x)<44&&Math.abs(p.z)<44;
  return {...route,activeDistrict:'jakarta',cameraMode:route.mode==='adventure'?'follow':'cinematic',playerPosition:valid?{x:p.x,z:p.z}:null,selectedLandmark:projectById(route.activeProject)?.landmarkId||null,worldReady:false,characterReady:false,travelState:'idle'};
}
