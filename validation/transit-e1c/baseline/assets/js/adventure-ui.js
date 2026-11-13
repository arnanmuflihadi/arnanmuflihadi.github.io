// Native dialogs and ordinary buttons. No renderer or gameplay assets in this module.
export function createAdventureUI(host,{world,onClose,onStudy,onLeave}){
  const hud=host.querySelector('[data-adventure-hud]');
  const story=document.createElement('button');story.className='atlas-story-card';story.dataset.questJournal='';story.innerHTML='<small>OPTIONAL FIELD STORY · FICTION</small><strong>The Lost Survey Signal</strong><span data-objective>Meet Sari at the south plaza.</span>';hud.append(story);
  const health=document.createElement('section');health.className='atlas-encounter-health';health.hidden=true;health.setAttribute('aria-label','Optional encounter health');health.innerHTML='<label>Your health <span data-player-health>100</span><progress data-player-bar max="100" value="100"></progress></label><label>Mosskeeper <span data-enemy-health>96</span><progress data-enemy-bar max="96" value="96"></progress></label><p data-enemy-intent></p>';hud.append(health);
  const actions=document.createElement('div');actions.className='atlas-combat-actions';actions.hidden=true;actions.setAttribute('aria-label','Encounter controls');actions.innerHTML='<button data-combat-action="attack">Attack <small>J · combo</small></button><button data-combat-action="dodge">Dodge <small>C</small></button><button data-combat-action="guard" aria-pressed="false">Guard <small>Hold K</small></button>';hud.append(actions);
  const jump=document.createElement('button');jump.dataset.combatAction='jump';jump.innerHTML='<kbd>Space</kbd><span>Jump</span>';hud.querySelector('[data-atlas-help]').before(jump);
  const announcer=document.createElement('p');announcer.className='sr-only';announcer.setAttribute('role','status');hud.append(announcer);
  const dialog=document.createElement('dialog');dialog.className='experience-panel atlas-dialogue';dialog.setAttribute('aria-labelledby','atlas-dialogue-title');dialog.dataset.lenisPrevent='';document.body.append(dialog);
  dialog.addEventListener('keydown',event=>{if(event.key===' '&&!event.target.closest('input,textarea,[contenteditable=true]'))event.preventDefault();});
  let current=null,lastPhase=null,lastHealth=100;
  dialog.addEventListener('close',()=>{world()?.speakTo(null);onClose();});
  function close(){if(dialog.open)dialog.close();}
  async function recover(){await world()?.requestAdventureAction('retry');close();}
  dialog.addEventListener('cancel',event=>{if(current?.kind==='defeat'){event.preventDefault();recover();}});
  function show(interaction){
    if(interaction.kind==='journal'&&world()?.getAdventureSnapshot()?.playerHealth===0)interaction={kind:'defeat'};
    current=interaction;const research=world()?.getAdventureSnapshot()?.kind==='research';
    const copy=research?world()?.getDialogue(interaction):interaction.kind==='journal'?{speaker:'Optional field story · Fiction',title:'The Lost Survey Signal',text:world()?.getAdventureSnapshot()?.objective||'Meet Sari at the south plaza. Look for the gold marker on the conceptual map.',actions:[{id:'close',label:'Keep exploring'},{id:'leave',label:'Read the atlas'}]}:world()?.getDialogue(interaction);
    if(!copy)return;world()?.setPaused(true);world()?.speakTo(interaction.id||null);
    dialog.replaceChildren();const closeButton=document.createElement('button');closeButton.textContent=interaction.kind==='defeat'?'Recover at the yard entrance':'Close conversation';closeButton.onclick=interaction.kind==='defeat'?recover:close;dialog.append(closeButton);
    const speaker=document.createElement('p');speaker.className='research-kicker';speaker.textContent=copy.speaker;
    const title=document.createElement('h2');title.id='atlas-dialogue-title';title.textContent=copy.title;
    const text=document.createElement('p');text.textContent=copy.text;dialog.append(speaker,title,text);
    const choices=document.createElement('div');choices.className='atlas-dialogue-choices';dialog.append(choices);
    for(const option of copy.actions){
      const button=document.createElement('button');button.textContent=option.label;button.dataset.storyAction=option.id;choices.append(button);
      button.onclick=async()=>{
        if(option.id==='close'){close();return;}
        if(option.id==='research'||option.id==='limitations'){show({...current,topic:option.id});return;}
        if(option.id.startsWith('answer:')){await world()?.requestAdventureAction(`transit:${option.id}`);show({...current,topic:option.id.slice(7)});return;}
        if(option.id==='leave'){close();onLeave();return;}
        if(option.id==='study'){close();onStudy(option.projectId);return;}
        if(option.id.startsWith('transit:')){await world()?.requestAdventureAction(option.id);if(option.id.startsWith('transit:scenario:'))current={...current,topic:option.id.slice(-1)};if(dialog.open)show(current);return;}
        button.disabled=true;button.textContent=option.id==='accept'?'Preparing the encounter…':'One moment…';
        try{await world().requestAdventureAction(option.id);if(option.id==='retry'){close();return;}if(dialog.open)show(current);}
        catch{const error=document.createElement('p');error.setAttribute('role','alert');error.textContent='The optional encounter could not load. You can keep exploring or read every study normally.';dialog.append(error);button.disabled=false;button.textContent=option.label;}
      };
    }
    if(!dialog.open)dialog.showModal();closeButton.focus({preventScroll:true});
  }
  story.onclick=()=>show({kind:'journal'});
  return{dialog,close,show,update(info){
    story.hidden=!info;if(!info){health.hidden=true;actions.hidden=true;return;}if(info.kind==='research'){health.hidden=true;actions.hidden=true;story.querySelector('small').textContent='FIELD NOTE · FICTION';story.querySelector('strong').textContent='Beyond the Station';story.querySelector('[data-objective]').textContent=info.objective;if(info.objective!==lastPhase){announcer.textContent=info.objective;lastPhase=info.objective;}return;}const phase=info.save.phase;
    story.querySelector('[data-objective]').textContent=info.objective+(info.marker?` · ${info.markerDistance}\u00a0m`:'');
    story.dataset.phase=phase;health.hidden=!info.inEncounter;actions.hidden=!info.inEncounter;
    health.querySelector('[data-player-health]').textContent=String(info.playerHealth);health.querySelector('[data-player-bar]').value=info.playerHealth;
    health.querySelector('[data-enemy-health]').textContent=String(info.enemyHealth);health.querySelector('[data-enemy-bar]').value=info.enemyHealth;health.querySelector('[data-enemy-intent]').textContent=info.enemyIntent;
    if(phase!==lastPhase){announcer.textContent=info.objective;lastPhase=phase;}
    else if(info.playerHealth<lastHealth&&info.playerHealth%5===0)announcer.textContent=`Health ${info.playerHealth}. ${info.enemyIntent}.`;
    else if(info.playerHealth>lastHealth&&lastHealth===0)announcer.textContent='Recovered at the yard entrance with full health.';
    lastHealth=info.playerHealth;
  }};
}
