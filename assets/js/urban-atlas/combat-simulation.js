import{slide,blocked}from'./collision.js?v=22';
import{questPlaces}from'./quest-state.js?v=22';
export const combatTuning=Object.freeze({playerHealth:100,enemyHealth:96,reach:2.8,attackDuration:.62,hitAt:.24,dodgeDuration:.58,dodgeCooldown:.9,windup:.85,enemyDamage:24});
const distance=(a,b)=>Math.hypot(a.x-b.x,a.z-b.z);
export const inServiceYard=p=>p.x<-10.3&&p.x>-29&&p.z>34.7&&p.z<43.7;
export function facesPoint(position,yaw,target,threshold=.2){const dx=target.x-position.x,dz=target.z-position.z,d=Math.hypot(dx,dz);return d<.001||(Math.sin(yaw)*dx+Math.cos(yaw)*dz)/d>=threshold;}
export function unobstructed(a,b,obstacles){const n=Math.max(1,Math.ceil(distance(a,b)/.15));for(let i=1;i<n;i++)if(blocked(a.x+(b.x-a.x)*i/n,a.z+(b.z-a.z)*i/n,obstacles,.04))return false;return true;}
// Pure, deterministic simulation. Animation and UI observe this state; neither owns damage.
export function createCombatSimulation(obstacles=[]){
  const home=questPlaces.guardian;
  const player={health:100,state:'free',elapsed:0,combo:1,queued:false,hit:false,cooldown:0,dodge:{x:0,z:1},lastDamage:10};
  const enemy={x:home.x,z:home.z,yaw:0,health:96,state:'Idle',elapsed:0,hit:false,patrol:0};
  let defeatedEvent=false;
  function enemyState(state){enemy.state=state;enemy.elapsed=0;enemy.hit=false;}
  function playerState(state){player.state=state;player.elapsed=0;player.hit=false;}
  function hurtPlayer(amount,p,facing,guarding){
    if(player.state==='defeated'||(player.state==='dodge'&&player.elapsed>=.04&&player.elapsed<.48))return false;
    const guarded=guarding&&facesPoint(p,facing,enemy,.15);player.health=Math.max(0,player.health-(guarded?5:amount));player.lastDamage=0;
    if(player.health===0)playerState('defeated');else if(!guarded){playerState('hit');player.queued=false;}
    return true;
  }
  function moveEnemy(goal,speed,dt,p){
    const dx=goal.x-enemy.x,dz=goal.z-enemy.z,d=Math.hypot(dx,dz);if(d<.04)return;
    enemy.yaw=Math.atan2(dx,dz);const step=Math.min(speed*dt,d);
    if(p&&distance(enemy,p)<1.4&&d<2)return;
    slide(enemy,dx/d*step,dz/d*step,obstacles);
  }
  return{player,enemy,
    restoreDefeated(){enemy.health=0;enemyState('Defeated');defeatedEvent=true;},
    reset(){Object.assign(player,{health:100,state:'free',elapsed:0,combo:1,queued:false,hit:false,cooldown:0,lastDamage:10});Object.assign(enemy,{x:home.x,z:home.z,health:96,patrol:0});enemyState('Idle');defeatedEvent=false;},
    step(dt,{position,facing=0,attack=false,dodge=false,guard=false,direction={x:0,z:0},enabled=true}={}){
      const events=[],delta={x:0,z:0};dt=Math.max(0,Math.min(.05,dt));
      player.elapsed+=dt;player.cooldown=Math.max(0,player.cooldown-dt);player.lastDamage+=dt;enemy.elapsed+=dt;
      const inside=enabled&&inServiceYard(position),alive=player.health>0;
      if(!inside&&alive&&player.lastDamage>3)player.health=Math.min(100,player.health+12*dt);
      if(player.state==='hit'&&player.elapsed>.32)playerState('free');
      if(player.state==='dodge'){
        if(player.elapsed<combatTuning.dodgeDuration){const speed=5.5;delta.x=player.dodge.x*speed*dt;delta.z=player.dodge.z*speed*dt;}
        else playerState('free');
      }
      if(inside&&alive&&dodge&&player.cooldown===0&&player.state!=='hit'){
        let dx=direction.x,dz=direction.z;if(Math.hypot(dx,dz)<.1){dx=position.x-enemy.x;dz=position.z-enemy.z;}
        const length=Math.hypot(dx,dz)||1;player.dodge={x:dx/length,z:dz/length};player.cooldown=combatTuning.dodgeCooldown;player.queued=false;playerState('dodge');events.push('dodge');
      }
      if(inside&&alive&&attack){
        if(['free','guard'].includes(player.state)){player.combo=1;player.queued=false;playerState('attack');events.push('attack');}
        else if(player.state==='attack'&&player.combo===1&&player.elapsed>.1)player.queued=true;
      }
      if(player.state==='attack'){
        if(!player.hit&&player.elapsed>=combatTuning.hitAt){
          player.hit=true;
          if(inside&&enemy.health>0&&distance(position,enemy)<combatTuning.reach&&facesPoint(position,facing,enemy,.15)&&unobstructed(position,enemy,obstacles)){
            enemy.health=Math.max(0,enemy.health-(player.combo===1?26:34));events.push('enemy-hit');
            enemyState(enemy.health===0?'Defeated':'Hit');
          }
        }
        if(player.elapsed>=combatTuning.attackDuration){
          if(player.queued&&inside){player.combo=2;player.queued=false;playerState('attack');events.push('combo');}
          else playerState('free');
        }
      }
      if(['free','guard'].includes(player.state))player.state=inside&&guard?'guard':'free';
      if(enemy.health>0){
        if(!inside||!alive){if(!['Return','Idle','Patrol'].includes(enemy.state))enemyState('Return');}
        else if(['Idle','Patrol','Return'].includes(enemy.state)&&distance(position,enemy)<10&&unobstructed(position,enemy,obstacles))enemyState('Detect');
        switch(enemy.state){
          case'Idle':if(enemy.elapsed>2)enemyState('Patrol');break;
          case'Patrol':{const goal={x:home.x+Math.sin(enemy.patrol)*1.6,z:home.z+Math.cos(enemy.patrol)*1.2};moveEnemy(goal,.65,dt);if(enemy.elapsed>2.4){enemy.patrol+=1.8;enemyState('Idle');}break;}
          case'Detect':enemy.yaw=Math.atan2(position.x-enemy.x,position.z-enemy.z);if(enemy.elapsed>.4)enemyState('Chase');break;
          case'Chase':if(distance(position,home)>10)enemyState('Return');else if(distance(position,enemy)<2.3){enemy.yaw=Math.atan2(position.x-enemy.x,position.z-enemy.z);enemyState('Attack');}else moveEnemy(position,1.65,dt,position);break;
          case'Attack':
            if(!enemy.hit&&enemy.elapsed>=combatTuning.windup){enemy.hit=true;events.push('enemy-swing');if(distance(position,enemy)<2.7&&facesPoint(enemy,enemy.yaw,position,.25)&&unobstructed(enemy,position,obstacles)&&hurtPlayer(combatTuning.enemyDamage,position,facing,player.state==='guard'))events.push(player.state==='guard'?'blocked':'player-hit');}
            if(enemy.elapsed>1.15)enemyState('Recover');break;
          case'Recover':if(enemy.elapsed>1.15)enemyState('Chase');break;
          case'Hit':if(enemy.elapsed>.36)enemyState('Chase');break;
          case'Return':moveEnemy(home,1.4,dt);if(distance(enemy,home)<.1)enemyState('Idle');break;
        }
      }else if(!defeatedEvent){defeatedEvent=true;events.push('enemy-defeated');}
      if(player.state==='defeated'&&!player.hit){player.hit=true;events.push('player-defeated');}
      return{events,delta,inside,allowMove:['free','guard'].includes(player.state),pose:({attack:'Attack'+player.combo,dodge:'Dodge',hit:'Hit',defeated:'Defeat',guard:'Guard'})[player.state]||null};
    },
  };
}
