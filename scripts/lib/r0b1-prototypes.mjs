import{createForms}from'./r0b1-forms.mjs';

export function designPrototypes(T,palette){
 const f=createForms(T,palette),{plate,panel,beam,source,pane,rail,planter,bench,stairs,shell,circularDeck,sign}=f,roots=[];
 function fins(x,y,z,n,spacing,height,rotation=0){for(let i=0;i<n;i++)panel('Climate shading fin',x+(i-(n-1)/2)*spacing,y,z,.08,height,.62,'bronze',rotation);}
 function display(x,z){plate('Shop display timber counter',x,.82,z,1.7,.65,.1,'timber','detail',.05);for(let j=0;j<4;j++)panel('Displayed book or sample',x-.55+j*.34,.93,z,.23,.3+j%2*.1,.08,j%2?'terracotta':'forest');}
 function doorPair(x,y,z,rotation=0){f.group('Recessed public entry',x,y,z,rotation,()=>{source('A-door',-1.03,0,0,-1.15,'bronze');source('A-door',1.03,0,0,1.15,'bronze');pane('Entry side transom',0,2.42,0,2.7,.45);sign('Entry wayfinding','MASUK',0,2.67,.03,1.05,.2);});}
 function upperWindows(y,frontZ,centres,finish,rotation=0){for(const x of centres){source('B-window-wall',x,y,frontZ,rotation,finish);plate('Deep window head shade',x,y+2.45,frontZ+.28,4.16,.75,.08,'concrete','detail',.05);}}

 const a=f.root('RuangNiaga');roots.push(a);
 plate('Commercial stone terrace',0,0,.3,14.8,10.6,.2,'stone','walk',.7);
 for(const x of[-6.6,-.1,6.4])source('B-column',x,.25,4.1,0,'bronze');
 for(const centre of[-3.3,3.3]){
  source('B-portal',centre,.25,2.65,0,'terracotta',1.1);pane('Layered shop display glazing',centre-.66,.48,2.54,1.92,1.95);source('A-door',centre+1.47,.25,2.05,-Math.PI/2,'bronze');
  panel('Shop interior back wall',centre,0,1.1,5.4,3.15,.18,'plaster');display(centre-.7,1.85);sign('Shop tenant sign',centre<0?'PUSTAKA / RUANG':'KOPI / RUANG',centre,2.96,2.88,3.6,.42);
 }
 panel('Commercial rear ground wall',0,.25,-3.7,13.4,2.94,.28,'terracotta');for(const side of[-1,1])panel('Commercial ground side',side*6.65,.25,-.5,6.4,2.94,.28,'terracotta',Math.PI/2);
 plate('Arcade timber soffit',0,3.18,3.25,14.2,3.6,.08,'timber','detail',.24);plate('Arcade canopy fascia',0,3.32,.1,14.5,10.4,.17,'concrete','walk',.5);
 upperWindows(3.61,3.72,[-4.25,0,4.25],'plaster');upperWindows(3.61,-3.7,[-4.25,0,4.25],'plaster',Math.PI);
 for(const[z,rotation]of[[3.59,0],[-3.57,Math.PI]])panel('Continuous mineral infill behind commercial modules',0,3.49,z,13.3,2.98,.22,'plaster',rotation,[-4.25,0,4.25].map(x=>[x,.87,2.8,1.1]));
 for(const side of[-1,1])panel('Commercial upper side return',side*6.17,3.49,0,7.5,2.98,.22,'terracotta',Math.PI/2,[[0,.87,2.8,1.1]]);
 for(const side of[-1,1]){f.group('Commercial side upper',side*6.3,0,0,side>0?Math.PI/2:-Math.PI/2,()=>{source('B-window-wall',0,3.61,0,0,'terracotta');source('A-window',0,7.01,-.03,0,'bronze');pane('Side window inner glass',0,7.15,-.12,1.63,1.98);});}
 plate('Commercial second terrace',0,6.4,0,13.8,8.7,.18,'concrete','walk',.55);upperWindows(6.82,2.9,[.3,4.55],'terracotta');upperWindows(6.82,-3.65,[.3,4.55],'plaster',Math.PI);
 for(const[z,rotation,finish]of[[2.77,0,'terracotta'],[-3.52,Math.PI,'plaster']])panel('Setback facade continuous infill',2.2,6.64,z,8.6,2.98,.22,finish,rotation,[.3,4.55].map(x=>[rotation?2.2-x:x-2.2,.93,2.8,1.1]));
 panel('Setback west wall',-1.85,6.64,-.4,6.6,2.96,.24,'terracotta',-Math.PI/2,[[0,0,1.25,2.45]]);source('A-door',-2.01,6.64,-.4,-Math.PI/2,'bronze');
 panel('Setback east wall',6.5,6.64,-.4,6.6,2.96,.24,'plaster',Math.PI/2,[[-1.35,.42,1.72,2.13],[1.35,.42,1.72,2.13]]);for(const z of[-1.75,.95]){source('A-window',6.66,7.0,z,Math.PI/2,'bronze');pane('Recessed east terrace glass',6.45,7.14,z,1.65,1.99,Math.PI/2);}
 rail('Setback west terrace edge',[-6.5,6.64,-3.6],[-6.5,6.64,3.9]);rail('Setback terrace south edge',[-6.5,6.64,3.9],[-2.15,6.64,3.9]);
 panel('Commercial east ground wall relief',6.82,.38,-.5,6.25,2.6,.14,'terracotta',Math.PI/2,[[-1.5,.6,1.8,1.6],[1.5,.6,1.8,1.6]]);for(const z of[-2,1])pane('Commercial ground side recessed window',6.91,.98,z,1.8,1.6,Math.PI/2);
 plate('Commercial planted roof',2.2,9.6,-.35,9.3,7.7,.2,'concrete','walk',.6);panel('Commercial roof parapet front',2.2,9.85,3.48,9.0,.68,.22,'terracotta');panel('Commercial roof parapet back',2.2,9.85,-4.0,9.0,.68,.22,'terracotta');
 planter('Western setback terrace',-4.55,6.64,2.8,3.1,.8);planter('Upper front integrated garden',2.1,9.85,3.25,4.9,.65);planter('Arcade corner planting',-6.25,.25,3.85,1.35,1.25);
 for(let j=0;j<6;j++)beam('Roof pergola timber',[-1.9+j*1.18,10.55,-2.8],[-1.9+j*1.18,10.55,2.4],.075,'timber');for(const x of[-1.8,4.0])for(const z of[-2.8,2.4])beam('Pergola structural post',[x,9.85,z],[x,10.6,z],.055,'bronze');
 fins(-5.5,3.7,4.0,3,.36,2.3);fins(5.85,6.9,3.25,3,.33,2.2);bench('Arcade bench',.0,.25,4.35);sign('Commercial architectural name','RUANG NIAGA',0,3.49,5.37,5.5,.58);
 a.userData={id:'commercial',name:'Ruang Niaga',entry:[4.13,.25,5.6],entryDirection:[0,0,1],floorDatum:.25,canopyClearance:2.93,design:'Three-storey stepped commercial arcade with planted west terrace'};

 const b=f.root('AtlasResearchCentre');roots.push(b);
 plate('Research stone podium',0,0,0,13.4,11.4,.25,'stone','walk',1.2);
 for(let floor=0;floor<4;floor++){
  const y=.3+floor*3.6,w=floor===3?9.5:12.4,xx=floor===3?1.5:0;plate('Research floor plate',xx,floor*3.6,0,w,10.6,.23,'concrete','walk',.65);
  for(const side of[-1,1]){const x=side*(floor===3?4.1:5.8);panel('Research side plaster wing',x,y,-.2,9.5,3.3,.28,'sage',Math.PI/2,[[0,.35,1.7,2.7]]);f.group('Research side source window',x,0,-.2,side>0?Math.PI/2:-Math.PI/2,()=>{source('A-window-tall',0,y+.22,.04,0,'bronze');pane('Research recessed side glazing',0,y+.36,-.16,1.64,2.72);});}
  panel('Research rear facade',xx,y,-4.8,w-.5,3.3,.3,'plaster',0,[[-2.8,.4,1.65,2.55],[2.7,.4,1.65,2.55]]);
  for(const x of[-2.8,2.7]){source('A-window',x,y+.55,-4.98,Math.PI,'bronze');pane('Research rear glass',x,y+.69,-4.86,1.64,1.99,Math.PI);}
  if(floor>0){const centres=floor===3?[-1.6,2.2,5.25]:[-4.25,-.2,4.0];panel('Research recessed front mineral facade',xx,y,4.32,w-.1,3.3,.3,'sage',0,centres.map(x=>[x-xx,.2,1.75,2.84]));for(const x of centres){source('A-window-tall',x,y+.12,4.56,0,'bronze');pane('Research deep front glass',x,y+.26,4.30,1.64,2.7);}for(let j=0;j<4;j++)panel('Research horizontal shade blade',xx,y+.24+j*.79,4.93,w-.15,.065,.42,'bronze');}
 }
 for(const x of[-5.6,-2.8,2.8,5.6])beam('Research vertical bronze blade',[x,.28,4.95],[x,14.18,4.95],.085,'bronze','column');
 for(const side of[-1,1])panel('Research public entry pier',side*4.35,.3,4.6,2.5,3.15,.45,'sage');doorPair(0,.3,4.7);pane('Research public atrium glass',0,3.0,4.65,5.3,.65);
 shell('Research entrance canopy',0,3.3,5.2,8.2,3.1,(u,v)=>.12+.24*Math.sin(u*Math.PI)+v*.16,'concrete','timber');sign('Research public identity','ATLAS / PUSAT RISET',0,3.6,6.52,5.8,.5);
 planter('Research vertical garden base',-5.4,.3,4.18,1.1,1.2);for(let floor=1;floor<4;floor++)planter('Research planted facade slot',-4.95,.3+floor*3.6,4.18,1.35,.75);
 plate('Public reception counter',-3.6,.3,.8,2.5,.9,.72,'sage','detail',.18);plate('Reception timber worktop',-3.6,1.06,.8,2.6,1.0,.07,'timber','detail',.12);bench('Public research lobby seating',3.8,.3,.8,Math.PI/2);sign('Research visitor information','ATLAS / INFORMASI',-3.6,2.1,-1.2,2.7,.45);
 plate('Research roof observation terrace',1.0,14.4,0,10.7,10.4,.23,'concrete','walk',1.5);for(const z of[-4.7,4.7])rail('Research roof edge',[-3.8,14.68,z],[5.8,14.68,z],1.1);rail('Research west roof edge',[-3.8,14.68,-4.7],[-3.8,14.68,4.7],1.1);rail('Research east roof edge',[5.8,14.68,-4.7],[5.8,14.68,4.7],1.1);
 circularDeck('Observation instrument dais',1.7,14.68,-.3,2.6,'forest');shell('Research observation sail',1.6,17.35,-.7,7.5,5.9,(u,v)=>.5*Math.sin(u*Math.PI)+.35*v,'concrete','timber',(u,v)=>[(u-.5)*7.5*(.65+.35*Math.sin(v*Math.PI)),(v-.5)*5.9]);
 for(const x of[-.5,3.8])beam('Observation shade support',[x,14.72,-2.8],[x,17.75,-2.6],.08,'bronze','column');beam('Research instrument pedestal',[1.6,14.98,-.3],[1.6,16.1,-.3],.15,'bronze');beam('Research telescope housing',[1.6,16.08,-.3],[2.6,16.48,-1.25],.16,'forest');planter('Research roof garden',-2.4,14.68,2.65,2.0,2.1);bench('Research observation bench',4.3,14.68,1.4,Math.PI/2);
 b.userData={id:'research',name:'Atlas Research Centre',entry:[0,.3,6.5],entryDirection:[0,0,1],floorDatum:.3,canopyClearance:2.98,design:'Four-storey stepped research pavilion with observation sail and deep vertical facade shading'};

 const c=f.root('StasiunAntara');roots.push(c);
 for(const x of[-7.4,7.4])for(const z of[-3.2,3.2]){source('B-column',x,0,z,0,'forest',1.45);for(const dx of[-1,1])beam('Branching transit support',[x,4.35,z],[x+dx*1.0,5.28,z],.15,'bronze','column');}
 plate('Elevated platform structural slab',0,5.4,0,22.2,10.0,.3,'concrete','walk',.7);plate('Platform tactile boarding strip',0,5.75,1.8,21.1,.28,.018,'terracotta','detail',.02);
 for(const zz of[-.72,.72])panel('Rail steel running section',0,5.76,zz,21.9,.14,.09,'bronze');for(let i=0;i<19;i++)plate('Rail timber sleeper',-10.35+i*1.15,5.72,0,.16,2.1,.055,'timber','detail',.025);
 for(const side of[-1,1])shell('Split butterfly transit roof',0,8.85,side*2.8,24.4,4.5,(u,v)=>.08+Math.pow(v-.5,2)*.6+.65*Math.pow((u-.5)*2,2)+(side>0?v:1-v)*.65,'concrete','timber',(u,v)=>[(u-.5)*24.4*(.94+.06*Math.sin(v*Math.PI)),(v-.5)*4.5]);
 for(let i=0;i<8;i++){const xx=-10.5+i*3;for(const side of[-1,1]){beam('Canopy rib inner',[xx,8.67,side*.65],[xx,8.88,side*2.6],.065,'bronze');beam('Canopy rib outer',[xx,8.88,side*2.6],[xx,9.35,side*4.65],.065,'bronze');}for(const zz of[-3.6,3.6])beam('Canopy slender post',[xx,5.75,zz],[xx,9.1,zz],.055,'bronze','column');}
 for(const zz of[-4.6,4.6]){if(zz<0)rail('Platform safety edge',[-10.7,5.75,zz],[10.7,5.75,zz],1.1);else for(const[a,b]of[[-10.7,-10.15],[-7.25,4.75]])rail('Platform edge with access openings',[a,5.75,zz],[b,5.75,zz],1.1);for(const x of zz<0?[-8,-4,0,4,8]:[-4,0]){pane('Passenger wind screen',x,6.0,zz,3.5,1.65);beam('Wind screen sill',[x-1.75,6.0,zz],[x+1.75,6.0,zz],.03);}}
 stairs('Station stair lower flight',-8.7,0,10.2);plate('Station lower landing',-10.05,1.63,5.7,5.4,2.4,.15,'concrete','walk',.18);stairs('Station stair middle flight',-11.4,1.8,5.7,2.4,12,.15,.28,Math.PI);plate('Station middle landing',-10.05,3.43,10.15,5.4,2.6,.15,'concrete','walk',.18);stairs('Station stair upper flight',-8.7,3.6,10.2);plate('Station upper landing',-8.7,5.4,5.65,2.6,2.4,.3,'concrete','walk',.18);
 rail('Lower switchback landing guard',[-12.7,1.8,4.55],[-7.35,1.8,4.55]);rail('Middle switchback landing guard',[-12.7,3.6,11.25],[-7.35,3.6,11.25]);for(const x of[-12.3,-7.8]){beam('Stair landing support',[x,0,5.65],[x,1.8,5.65],.11,'bronze','column');beam('Stair landing support',[x,0,10.15],[x,3.6,10.15],.11,'bronze','column');}
 for(const xx of[-9.98,-7.42]){beam('Stair handrail rising',[xx,.95,10.2],[xx,2.75,6.84],.045);beam('Stair top handrail',[xx,4.55,10.2],[xx,6.35,6.84],.045);}for(const xx of[-12.68,-10.12])beam('Middle flight handrail',[xx,2.75,5.7],[xx,4.55,9.06],.045);
 f.group('Transit lift and ticket entrance',7.7,0,5.2,0,()=>{panel('Lift rear wall',0,0,-1.2,2.6,8.5,.22,'forest');for(const x of[-1.2,1.2])panel('Lift side',x,0,0,2.6,8.5,.16,'forest',Math.PI/2);for(const y of[0,5.75]){source('A-door',0,y,1.2,0,'bronze');pane('Lift door glass',0,y+.12,1.08,1.03,2.16);}pane('Lift upper glazing',0,2.45,1.18,2.3,3.1);plate('Lift cap',0,8.5,0,3.0,3.0,.2,'concrete','detail',.3);});
 plate('Lift upper exit and bridge interface',7.7,5.4,6.25,5.8,4.3,.3,'concrete','walk',.35);rail('Lift exit apron outer guard',[4.8,5.75,8.3],[10.6,5.75,8.3]);for(const x of[4.8,10.6])rail('Lift exit side protection',[x,5.75,4.7],[x,5.75,8.3]);
 bench('Platform shaded bench',1.8,5.75,3.4);bench('Platform shaded bench',-3.0,5.75,3.4);planter('Station platform end garden',9.8,5.75,3.4,1.25,1.6);sign('Transit name fascia','STASIUN ANTARA',0,8.18,5.1,7.5,.64);sign('Transit platform wayfinding','01 / PERON · ATLAS',0,7.5,3.8,3.4,.5);sign('Transit access sign','MASUK / LIFT',7.7,2.9,6.5,2.4,.36);
 c.userData={id:'station',name:'Stasiun Antara',entry:[-8.7,0,10.5],entryDirection:[0,0,1],floorDatum:0,platformDatum:5.75,canopyClearance:2.9,design:'Elevated open transit viaduct, split butterfly canopy, railway bed, three-flight stair and lift core'};

 const d=f.root('PelabuhanAwan');roots.push(d);
 plate('Skyport terminal foundation',-1.8,0,-3.6,17.8,10.8,.23,'stone','walk',1.4);circularDeck('Dragon landing apron',2.0,0,6.1,6.3,'stone');plate('Boarding bridge',2,0,1.2,5.4,5.8,.23,'concrete','walk',.4);circularDeck('Landing deck inset',2.0,.001,6.1,5.7,'forest');
 for(const x of[-7.5,4.8])for(const z of[-7.2,-.8]){source('B-column',x,.28,z,0,'bronze',1.8);beam('Skyport branching roof support',[x,5.4,z],[x+1.0,7.1,z+.6],.13,'bronze','column');}
 for(const x of[-7.0,3.8])panel('Terminal service wing wall',x,.28,-4.1,6.5,3.25,.28,'plaster',Math.PI/2);panel('Terminal rear wall',-1.8,.28,-7.6,12.7,3.25,.26,'forest',0,[[-.5,0,2.7,2.6]]);
 doorPair(-2.3,.28,-7.85,Math.PI);for(const x of[-5.4,-1.8]){source('A-window-tall',x,.52,-.77,0,'bronze');pane('Terminal boarding lounge glass',x,.67,-.94,1.65,2.68);}doorPair(2,.28,-.77);
 plate('Terminal upper observation floor',-3.2,3.55,-4.4,9.8,6.7,.2,'concrete','walk',.8);for(const zz of[-7.1,-1.5])rail('Skyport upper observation edge',[-7.5,3.8,zz],[1.25,3.8,zz],1.1);
 stairs('Skyport observation stair lower',-8.5,.28,-1.4,1.6,12,.145,.28);plate('Observation stair switchback',-7.55,1.9,-5.2,3.6,1.8,.1,'concrete','walk',.1);stairs('Skyport observation stair upper',-6.6,2.02,-5.2,1.6,12,.145,.28,Math.PI);for(const x of[-9.35,-7.65])beam('Observation stair lower handrail',[x,1.28,-1.4],[x,3.02,-4.76],.035);for(const x of[-7.45,-5.75])beam('Observation stair upper handrail',[x,3.02,-5.2],[x,4.76,-1.84],.035);rail('Observation stair landing guard',[-9.3,2.02,-6.0],[-5.8,2.02,-6.0]);
 shell('Swept modern skyport wing',-1.0,6.15,-3.25,22.5,12.5,(u,v)=>.3+1.35*Math.sin(u*Math.PI)+.8*Math.sin(v*Math.PI)+.5*u,'concrete','timber',(u,v)=>[(u-.5)*22.5*(.65+.35*Math.sin(v*Math.PI)),(v-.5)*12.5+1.8*Math.pow(u,2)]);
 for(let i=0;i<8;i++){const xx=-8.0+i*2.2;beam('Skyport wing roof rib',[xx,6.0,-7.2],[xx+.5,7.6,-3.1],.085,'bronze');beam('Skyport wing roof rib',[xx+.5,7.6,-3.1],[xx+1.2,6.55,1.45],.085,'bronze');}
 for(let i=0;i<18;i++){const a=-2.72+i/18*5.44,x=2+Math.sin(a)*6.12,z=6.1+Math.cos(a)*6.12,next=a+5.44/18;rail('Landing apron perimeter',[x,.28,z],[2+Math.sin(next)*6.12,.28,6.1+Math.cos(next)*6.12],1.1);}
 for(const x of[-.5,4.5])rail('Protected boarding interface',[x,.28,.3],[x,.28,3.0],1.1);bench('Terminal waiting bench',-4.4,.28,-3.6);bench('Terminal waiting bench',.4,.28,-3.6);planter('Skyport roofside garden',-7.1,3.8,-4.0,1.25,4.3);planter('Boarding garden',-3.1,.28,.1,2.3,1.2);
 sign('Skyport northern entrance name','PELABUHAN AWAN',-1.8,3.7,-8.02,6.2,.64,Math.PI);sign('Skyport boarding wayfinding','01 / BOARDING',1.25,2.95,.0,3.5,.46);const landingSign=sign('Landing apron identifier','01',2,.31,6.1,3.2,3.2);landingSign.rotation.x=-Math.PI/2;
 beam('Skyport navigation mast',[6.9,.28,2.1],[6.9,5.1,2.1],.07,'bronze','column');for(let i=0;i<3;i++)beam('Navigation wind vane',[6.9,4.3+i*.25,2.1],[7.8+i*.25,4.3+i*.25,2.1],.04,'terracotta');
 d.userData={id:'skyport',name:'Pelabuhan Awan',entry:[-2.3,.28,-8.2],entryDirection:[0,0,-1],floorDatum:.28,landingDatum:.28,canopyClearance:3.0,design:'Contemporary cloud-facing terminal with swept wing roof and protected circular landing apron'};
 return{roots,materials:f.materials,sources:f.sources};
}
