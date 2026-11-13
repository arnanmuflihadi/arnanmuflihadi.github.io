export const questPhases=Object.freeze(['available','searching','device-ready','returning','complete']);
export const questPlaces=Object.freeze({researcher:{x:4,z:25},entrance:{x:-9.5,z:37},guardian:{x:-20,z:39},device:{x:-23,z:40}});
export function createQuestState(saved){return{version:1,phase:saved?.version===1&&questPhases.includes(saved.phase)?saved.phase:'available'};}
export function advanceQuest(state,event){
  const transitions={available:{accept:'searching'},searching:{defeat:'device-ready'},'device-ready':{collect:'returning'},returning:{report:'complete'}};
  return{version:1,phase:transitions[state.phase]?.[event]||state.phase};
}
export function questObjective(state){return({
  available:'Meet Sari by the south plaza for an optional story.',
  searching:'Find the mosskeeper in the old service yard, southwest of the plaza.',
  'device-ready':'Retrieve the survey receiver beside the old service-yard wall.',
  returning:'Return the receiver to Sari at the south plaza.',
  complete:'Receiver returned. Thank you for exploring the district.',
})[state.phase];}
export function questMarker(state){return state.phase==='complete'?null:state.phase==='searching'?questPlaces.entrance:state.phase==='device-ready'?questPlaces.device:questPlaces.researcher;}
