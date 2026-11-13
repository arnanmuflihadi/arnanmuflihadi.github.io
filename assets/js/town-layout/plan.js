import{groundHeight,terrainSample}from'../floating-atlas/terrain.js?v=73';
import{routes as trails}from'../floating-atlas/plan.js?v=73';

export const revision='R0-B1.5-composition-repair.3';
const line=(id,width,points,kind='paved')=>({id,width,points,kind});
const sample=(x,z)=>[x,z,groundHeight(x,z)+.10];
const ridge=trails.find(r=>r.id==='ridge').points;
const back=[...trails.find(r=>r.id==='overlook').points,...trails.find(r=>r.id==='return').points.slice(1)];
const natural=p=>p.map(([x,z])=>sample(x,z));
export const destinations=Object.freeze({skyport:[27,60],market:[36,36],square:[36,10],guild:[40,.8],lookout:[-45,-49]});
// Shared terrace stations make frontages, paving and thresholds one continuous section.
export const streetLevel=z=>{const stations=[[60,17.15],[52,17.4],[47,18],[43,18.8],[40,19.1],[33,20.2],[26,21.4],[19,22.6],[0,22.6]];for(let i=1;i<stations.length;i++){const a=stations[i-1],b=stations[i];if(z>=b[0])return a[1]+(b[1]-a[1])*Math.max(0,Math.min(1,(a[0]-z)/(a[0]-b[0])));}return 22.6;};
const commercial=(id,x,z,w,d,h,face,roof='gable')=>({id,name:'Commercial planning envelope '+id,x,z,w,d,h,y:streetLevel(z),face,roof,publicPoint:[36,z]});
export const selected={
 id:'A',name:'Central Plaza Hub / composition repair',square:{x:36,z:10,w:24,d:14,y:22.6,clear:[30,5,37,15],focal:[33,9]},
 skyport:{x:27,z:60,r:9,y:17.15},
 streets:[
  line('arrival',7,[[27,60,17.15],[30,52,17.4],[34,47,18],[36,43,18.8],[36,40,19.1]]),
  line('market',8,[[36,40,19.1],[36,33,20.2],[36,26,21.4],[36,19,22.6],[36,12,22.6]]),
  line('guild',4,[[36,12,22.6],[40,14,22.6],[40,9,23.35],[40,5,24.2],[40,.8,25.2]]),
  line('east-frontage',2.5,[[39.3,40,19.1],[39.3,33,20.2],[39.3,26,21.4],[39.3,19,22.6]]),
  line('garden-loop',2.4,[[30,52,17.4],[26,49,17.35],[22,42,17.9],[16,36,18.4],[12,29,18.8],[11,22,19.4],[8,17,20.5],[8,12,20.6],[14,12,20.6],[18,16,21.3],[22,16,22.6],[24,16,22.6],[30,14,22.6]],'secondary'),
  line('ridge-connector',3,[[30,14,22.6],[24,16,22.6],[22,16,22.6],[18,16,21.3],[14,12,20.6],[3,12,20.6],...natural([[-5,5]])],'trail'),
  line('highland',2.6,natural(ridge),'trail'),
  line('scenic-return',2.5,natural(back),'trail'),
  line('west-frontage',2.5,[[32.7,40,19.1],[32.7,33,20.2],[32.7,26,21.4],[32.7,19,22.6]])
 ],
 lots:[
  commercial('M1',27.5,40,5,5.4,5.8,'east','terrace'),
  commercial('M2',43.5,40,5.5,5.4,6.6,'west'),
  commercial('M3',28.5,33,5.5,5.8,7.4,'east'),
  commercial('M4',43.5,33,5.5,5.8,5.8,'west','terrace'),
  commercial('M5',28.5,26,5.5,5.8,6.2,'east','terrace'),
  commercial('M6',43.5,26,5.5,5.8,8.4,'west'),
  commercial('M7',28.5,19,5.5,5.4,7.4,'east'),
  commercial('M8',43.5,19,5.5,5.4,6.2,'west','terrace'),
  {id:'M9',name:'North square envelope',x:28,z:-2,w:5,d:6,h:6.4,y:23.7,face:'south',roof:'gable',publicPoint:[28,5]},
  {id:'M10',name:'Trail gate envelope',x:22,z:8,w:5,d:7,h:5.8,y:22.6,face:'east',roof:'terrace',publicPoint:[29,8]},
  {id:'G',name:'Atlas Guild / civic hall and observatory massing',x:40,z:-4,w:10,d:8,h:16.3,y:25.2,face:'south',publicPoint:[40,9]}
 ]
};
export const entryOf=l=>l.face==='east'?[l.x+l.w/2+.8,l.z]:l.face==='west'?[l.x-l.w/2-.8,l.z]:[l.x,l.z+l.d/2+.8];
export const thresholdLinks=selected.lots.filter(l=>l.id!=='G').map(l=>line('threshold-'+l.id,3,[[...l.publicPoint,l.publicPoint[1]>16?streetLevel(l.publicPoint[1]):22.6],[...entryOf(l),l.y]]));
export function surveyPlot(l,spacing=.5){const heights=[];let unsafe=0;const nx=Math.ceil(l.w/spacing),nz=Math.ceil(l.d/spacing);for(let i=0;i<=nx;i++)for(let j=0;j<=nz;j++){const x=l.x-l.w/2+i*l.w/nx,z=l.z-l.d/2+j*l.d/nz,s=terrainSample(x,z);heights.push(s.height);if(s.height<0||s.fraction>=.93)unsafe++;}const min=Math.min(...heights),max=Math.max(...heights);return{id:l.id,samples:heights.length,spacing,groundRange:[min,max],floor:l.y,minimumFloorClearance:l.y-max,maximumFoundationHeight:l.y-min+.15,foundationBottom:min-.15,unsafeSamples:unsafe};}
export const alternatives=[selected,
 {id:'B',name:'Terraced Hillside Town',square:{x:30,z:-8,w:20,d:17,y:27.5},skyport:selected.skyport,
  streets:[line('arrival',5,[[27,60],[39,36],[36,15],[30,-8]]),line('guild',4,[[30,-8],[38,-30]]),line('loop',3,[[30,-8],[11,22],[32,44],[39,36]])],
  lots:[{x:17,z:0,w:10,d:9},{x:43,z:1,w:10,d:9},{x:18,z:-15,w:10,d:9},{x:45,z:-14,w:10,d:9},{x:38,z:-30,w:14,d:13}]},
 {id:'C',name:'Curved Market Loop',square:{x:32,z:17,w:18,d:17,y:22.3},skyport:selected.skyport,
  streets:[line('arrival',5,[[27,60],[32,44],[39,36],[43,24],[32,17]]),line('guild',4,[[32,17],[38,-18]]),line('loop',3,[[32,17],[18,12],[11,22],[16,36],[32,44],[39,36],[43,24],[32,17]])],
  lots:[{x:23,z:34,w:9,d:8},{x:48,z:33,w:9,d:8},{x:46,z:15,w:9,d:8},{x:16,z:5,w:9,d:8},{x:7,z:28,w:9,d:8},{x:38,z:-18,w:14,d:13}]}
];
export function densify(points,spacing=.4){
 const out=[];for(let i=1;i<points.length;i++){const a=points[i-1],b=points[i],n=Math.ceil(Math.hypot(b[0]-a[0],b[1]-a[1])/spacing);for(let j=0;j<n;j++){const t=j/n;out.push([a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t,a[2]===undefined?undefined:a[2]+(b[2]-a[2])*t]);}}out.push(points.at(-1));return out;
}
export function routeSurvey(points,{authored=false,width=0}={}){
 const p=densify(points),heights=p.map(v=>authored?v[2]:groundHeight(v[0],v[1]));let length=0,ascent=0,descent=0,maxGrade=0,unsafe=0;
 for(let i=0;i<p.length;i++){if(terrainSample(p[i][0],p[i][1]).fraction>.93)unsafe++;if(i){const d=Math.hypot(p[i][0]-p[i-1][0],p[i][1]-p[i-1][1]),rise=heights[i]-heights[i-1];length+=Math.hypot(d,rise);ascent+=Math.max(0,rise);descent+=Math.max(0,-rise);maxGrade=Math.max(maxGrade,Math.abs(rise)/Math.max(.001,d));}}
 return{length,ascent,descent,elevation:[Math.min(...heights),Math.max(...heights)],maxGrade,unsafeSamples:unsafe,samples:p.length,width,walkSeconds:length/2.1,runSeconds:length/4.6};
}
export function surveyAlternative(plan){
 let low=Infinity,high=-Infinity,steep=0,count=0;const slopeDelta=.5;
 for(const s of [plan.square,...plan.lots])for(let x=s.x-s.w/2;x<=s.x+s.w/2;x+=1)for(let z=s.z-s.d/2;z<=s.z+s.d/2;z+=1){const h=groundHeight(x,z),slope=Math.hypot((groundHeight(x+slopeDelta,z)-groundHeight(x-slopeDelta,z))/(2*slopeDelta),(groundHeight(x,z+slopeDelta)-groundHeight(x,z-slopeDelta))/(2*slopeDelta));low=Math.min(low,h);high=Math.max(high,h);if(slope>.35)steep++;count++;}
 const urban=plan.streets.filter(r=>r.kind!=='trail'),xs=plan.lots.flatMap(l=>[l.x-l.w/2,l.x+l.w/2]),zs=plan.lots.flatMap(l=>[l.z-l.d/2,l.z+l.d/2]);xs.push(plan.square.x-plan.square.w/2,plan.square.x+plan.square.w/2);zs.push(plan.square.z-plan.square.d/2,plan.square.z+plan.square.d/2);
 return{id:plan.id,name:plan.name,terrainRange:[low,high],steepFootprintPercent:100*steep/count,slopeThreshold:.35,footprintSamples:count,coreBounds:[Math.min(...xs),Math.min(...zs),Math.max(...xs),Math.max(...zs)],coreArea:(Math.max(...xs)-Math.min(...xs))*(Math.max(...zs)-Math.min(...zs)),routes:urban.map(r=>({id:r.id,...routeSurvey(r.points)}))};
}
export const journeyRoutes={
 'skyport-market':{name:'Skyport → Market Street',points:selected.streets[0].points},
 'market-square':{name:'Market Street → Town Square',points:selected.streets[1].points},
 'square-guild':{name:'Town Square → Atlas Guild',points:selected.streets[2].points},
 'square-lookout':{name:'Town Square → Highland Lookout',points:[[36,12,22.6],...selected.streets[5].points,...selected.streets[6].points.slice(1)]},
 'return-loop':{name:'Highland → Cloudbreak → Town return',points:[...selected.streets[7].points,...selected.streets[5].points.slice().reverse().slice(1),[36,12,22.6]]},
 'garden-loop':{name:'Optional meadow return to Skyport',points:[...selected.streets[4].points].reverse().concat([[27,60,17.15]])}
};
journeyRoutes['skyport-lookout']={name:'Continuous arrival → market → square → Guild → highland',points:[...journeyRoutes['skyport-market'].points,...journeyRoutes['market-square'].points.slice(1),...journeyRoutes['square-guild'].points.slice(1),...journeyRoutes['square-guild'].points.slice().reverse().slice(1),...journeyRoutes['square-lookout'].points.slice(1)]};
journeyRoutes['entrance-circuit']={name:'Market frontage and square entrance circuit',points:selected.lots.filter(l=>l.id!=='G').flatMap(l=>[[...l.publicPoint,l.publicPoint[1]>16?streetLevel(l.publicPoint[1]):22.6],[...entryOf(l),l.y],[...l.publicPoint,l.publicPoint[1]>16?streetLevel(l.publicPoint[1]):22.6]]).filter((p,i,a)=>!i||Math.hypot(p[0]-a[i-1][0],p[1]-a[i-1][1])>.01)};
