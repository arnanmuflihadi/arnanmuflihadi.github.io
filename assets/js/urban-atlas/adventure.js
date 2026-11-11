import {researchConversation} from './npc-registry.js?v=22';
import * as T from '../vendor/three-atlas.module.js?v=16';
import{createQuestState,advanceQuest,questPlaces,questMarker,questObjective}from'./quest-state.js?v=22';
import{createCombatSimulation,inServiceYard}from'./combat-simulation.js?v=22';
import{createRiggedActor,disposeAsset}from'./rigged-actor.js?v=22';
import{slide,separateFromPeople}from'./collision.js?v=40';
import{groundHeight}from'./layout.js?v=40';
const url=id=>new URL(`../../game/phase3/${id}.glb`,import.meta.url).href;
export function createAdventure({scene,character,input,obstacles,life,yard,saved,explorationOnly=false,onEvent=()=>{}}){
  let quest=createQuestState(saved),monster=null,loading=null,disposed=false,time=0,assets=[],lastPose=null,defeatNotice=null;
  const combat=createCombatSimulation(obstacles),empty={keys:new Set(),touch:new Set(),yaw:0};
  if(['device-ready','returning','complete'].includes(quest.phase))combat.restoreDefeated();
  const change=event=>{quest=advanceQuest(quest,event);onEvent('quest-change');};
  async function loadEncounter(){
    if(monster)return;if(loading)return loading;
    loading=(async()=>{
      const loader=new T.GLTFLoader(),results=await Promise.allSettled([loader.loadAsync(url('explorer-actions')),loader.loadAsync(url('mosskeeper'))]);
      const loaded=results.filter(r=>r.status==='fulfilled').map(r=>r.value);
      if(disposed||loaded.length!==2){loaded.forEach(disposeAsset);throw Error('Encounter assets unavailable');}
      assets=loaded;character.animator.addClips(assets[0].animations);
      monster=createRiggedActor(scene,assets[1],{...questPlaces.guardian,height:2.5,clone:false});
      if(combat.enemy.health===0)monster.root.visible=false;
    })().catch(error=>{loading=null;throw error;});return loading;
  }
  function getInteraction(){
    const p=character.root.position,npc=life()?.nearest(p);
    if(npc)return{kind:'npc',id:npc.id,label:`Talk to ${npc.name} · ${npc.role}`,name:npc.name,role:npc.role,study:npc.study};
    if(explorationOnly)return null;
    if(quest.phase==='device-ready'&&Math.hypot(p.x-questPlaces.device.x,p.z-questPlaces.device.z)<2.4)return{kind:'device',id:'receiver',label:'Retrieve survey receiver'};
    if(quest.phase==='available'&&Math.hypot(p.x-questPlaces.entrance.x,p.z-questPlaces.entrance.z)<2.4)return{kind:'yard',id:'yard',label:'Read service-yard notice'};
    return null;
  }
  function dialogue(interaction){
    if(interaction.kind==='npc'&&interaction.id!=='sari')return researchConversation(interaction.id,interaction.topic);
    if(interaction.kind==='defeat')return{speaker:'Old service yard',title:'Take a breath.',text:'The mosskeeper caught you. Retry from the yard entrance with full health, or return to the atlas. Your research and project selection are unaffected.',actions:[{id:'retry',label:'Recover at the yard entrance'},{id:'leave',label:'Read the atlas'}]};
    if(interaction.kind==='device')return{speaker:'The Lost Survey Signal · Fiction',title:'Receiver recovered.',text:'The little receiver is still blinking. Bring it back to Sari at the south plaza to finish this optional story.',actions:[{id:'close',label:'Return to Sari'}]};
    if(interaction.kind==='yard')return{speaker:'Optional story · Fiction',title:'The old service yard',text:'An overgrown maintenance court, beyond the everyday station and shops. Sari at the south plaza knows why a survey receiver was left here. You can ignore this story and read every study normally.',actions:[{id:'close',label:'Keep exploring'}]};
    if(interaction.id==='sari'){
      const copy={available:['The Lost Survey Signal','I am checking a receiver left in the old service yard, southwest of this plaza. A curious mosskeeper has settled beside it. Would you retrieve it? This is a fictional side story; it is unrelated to the research findings.','accept','I’ll find the receiver'],searching:['Follow the small signal','Go southwest, behind Studio Kota, to the old service yard. The mosskeeper signals before each strike. J attacks, C rolls, K guards. You can leave the yard whenever you like.','close','Continue exploring'],'device-ready':['A signal in the moss','The guardian has settled down. The receiver is beside the back wall of the service yard. Bring it here when you have it.','close','Find the receiver'],returning:['You found the receiver.','Thank you. Returning the receiver will finish our little field story. The actual research is always available through the atlas.','report','Return the receiver'],complete:['A small field story, complete.','The receiver is back and the district is yours to explore. If you are curious about urban morphology, the study explains both its evidence and its limits.','close','Keep exploring']}[quest.phase];
      return{speaker:'Sari · Field researcher · Fiction',title:copy[0],text:copy[1],actions:[{id:copy[2],label:copy[3]},{id:'study',projectId:'mbr',label:'Read the urban morphology study'}]};
    }

  }
  return{combat,loadEncounter,getInteraction,dialogue,getSave:()=>({...quest}),
    async request(action){
      if(explorationOnly)return null;
      if(action==='accept'&&quest.phase==='available'){await loadEncounter();change('accept');}
      else if(action==='collect'&&getInteraction()?.kind==='device')change('collect');
      else if(action==='report'&&quest.phase==='returning'&&getInteraction()?.id==='sari')change('report');
      else if(action==='retry'){combat.reset();defeatNotice=null;character.root.position.set(questPlaces.entrance.x,.06,questPlaces.entrance.z);character.reset();lastPose=null;}
      return this.snapshot();
    },
    begin(){if(explorationOnly)return;if(['searching','device-ready'].includes(quest.phase))loadEncounter().catch(()=>onEvent('encounter-error'));if(combat.player.health===0)onEvent('defeat');},
    stop(){input.clear();character.reset();defeatNotice=null;if(combat.player.state!=='defeated')combat.player.state='free';combat.player.queued=false;lastPose=null;},
    update(dt,reduced){
      time+=dt;const p=character.root.position,commands=input.consumeActions(),active=Boolean(monster)&&quest.phase==='searching';
      const has=k=>input.keys.has(k)||input.touch.has(k),mx=Number(has('d')||has('arrowright'))-Number(has('a')||has('arrowleft')),mz=Number(has('s')||has('arrowdown'))-Number(has('w')||has('arrowup'));
      const direction={x:mx*Math.cos(input.yaw)+mz*Math.sin(input.yaw),z:-mx*Math.sin(input.yaw)+mz*Math.cos(input.yaw)};
      if(active&&combat.player.health>0&&inServiceYard(p)&&(commands.has('attack')||has('k')||playerAction()))character.root.rotation.y=Math.atan2(combat.enemy.x-p.x,combat.enemy.z-p.z);
      const canAct=character.movement.grounded&&character.movement.phase==='grounded';
      const result=combat.step(dt,{position:p,facing:character.root.rotation.y,attack:commands.has('attack')&&canAct,dodge:commands.has('dodge')&&canAct,guard:has('k')&&canAct,direction,enabled:active});
      if(result.events.includes('dodge'))character.root.rotation.y=Math.atan2(combat.player.dodge.x,combat.player.dodge.z);
      slide(p,result.delta.x,result.delta.z,obstacles);
      if(active&&combat.enemy.health>0){const dx=p.x-combat.enemy.x,dz=p.z-combat.enemy.z,d=Math.hypot(dx,dz);if(d>.001&&d<1.25)slide(p,dx/d*(1.25-d),dz/d*(1.25-d),obstacles);}
      if(result.pose!==lastPose){character.animator.setOverride(result.pose,{duration:result.pose?.startsWith('Attack')?.62:result.pose==='Dodge'?.58:result.pose==='Hit'?.32:result.pose==='Defeat'?1.1:1.5,loop:result.pose==='Guard'});lastPose=result.pose;}
      const people=life()?.people||[];separateFromPeople(p,people.map(n=>n.actor.root.position),obstacles);const solids=people.map(n=>({x:n.actor.root.position.x,z:n.actor.root.position.z,w:.6,d:.6,h:1.9}));
      empty.yaw=input.yaw;const motion=character.update(dt,result.allowMove?input:empty,solids.length?obstacles.concat(solids):obstacles,reduced,{jump:commands.has('jump')&&combat.player.health>0&&combat.player.state==='free'});
      if(monster){
        const e=combat.enemy,old=monster.root.position.clone();monster.root.position.set(e.x,groundHeight(e.x,e.z),e.z);monster.root.rotation.y=e.yaw;
        const pose=e.state==='Defeated'?'Defeat':e.state==='Hit'?'Hit':e.state==='Attack'&&e.elapsed>=.5?'Attack':null;
        monster.animator.setOverride(pose,{duration:pose==='Attack'?.65:pose==='Hit'?.36:1.3});monster.animator.update(dt,Math.hypot(old.x-e.x,old.z-e.z)/Math.max(.001,dt));
        monster.root.visible=e.health>0||e.elapsed<2;
      }
      yard.update(combat.enemy,quest.phase,time,reduced);
      if(result.events.includes('enemy-defeated')&&quest.phase==='searching')change('defeat');
      if(result.events.includes('player-defeated'))defeatNotice=1.1;
      if(defeatNotice!==null){defeatNotice-=dt;if(defeatNotice<=0){defeatNotice=null;onEvent('defeat');}}
      return motion;
      function playerAction(){return ['attack','guard'].includes(combat.player.state);}
    },
    snapshot(){if(explorationOnly)return null;const p=character.root.position,e=combat.enemy,marker=questMarker(quest);return{save:{...quest},objective:questObjective(quest),marker,markerDistance:marker?Math.round(Math.hypot(p.x-marker.x,p.z-marker.z)):0,inEncounter:Boolean(monster)&&quest.phase==='searching'&&inServiceYard(p),playerHealth:Math.ceil(combat.player.health),playerState:combat.player.state,enemyHealth:e.health,enemyState:e.state,enemyIntent:e.state==='Attack'?(e.elapsed<.85?'Readying a strike':'Striking'):e.state==='Recover'?'Recovering':e.state,ready:Boolean(monster)};},
    dispose(){disposed=true;monster?.dispose();assets.forEach(disposeAsset);},
  };
}
