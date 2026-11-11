import { projectById } from './project-registry.js';
export function readRoute(url) {
  const params = new URL(url).searchParams;
  return {experience:params.get('experience') === 'rpg' ? 'rpg' : 'professional', activeProject:projectById(params.get('project'))?.id || null};
}
export function routeUrl(url, state) {
  const next = new URL(url);
  next.searchParams.delete('experience'); next.searchParams.delete('project');
  if (state.experience === 'rpg') next.searchParams.set('experience','rpg');
  if (projectById(state.activeProject)) next.searchParams.set('project',state.activeProject);
  return next;
}
export function createState(route, saved = {}) {
  const position = saved?.playerPosition;
  const safePosition = position && Number.isFinite(position.x) && Number.isFinite(position.z) && Math.abs(position.x)<31 && Math.abs(position.z)<31 ? {x:position.x,z:position.z} : null;
  const visited = ['transit','cbd'].filter(id => saved?.missionProgress?.[id] === true);
  return {...route,activeDistrict:'jakarta',gameReady:false,playerPosition:safePosition,panelOpen:false,missionProgress:Object.fromEntries(visited.map(id=>[id,true]))};
}
