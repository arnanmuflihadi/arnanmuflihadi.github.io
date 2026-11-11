import{readFileSync,writeFileSync}from'node:fs';import{fixture}from'../circulation-c1c/fixture.mjs';
const all=JSON.parse(readFileSync('validation/reset-a/comparison.json')),f=await fixture(),out={};
for(const[k,r]of Object.entries(all)){
 const arrival=k==='A'?[[27,57],[38,58],[46,49],r.entry]:[[27,57],[27,65],[22,67],r.entry];
 const sq=r.program.find(p=>p.id==='square').polygon,exit=k==='A'?sq[0].map((v,i)=>(v+sq[3][i])/2):sq[2];const branch=k==='A'?[exit,[12,11],[-5,5]]:[exit,[12,25],[-5,5]];
 const lines={arrival,core:r.primaryCoreRoute,optionalHighland:branch};if(k==='B')lines.optionalTrailReturn=[r.entry,[26,49],[22,42],[16,36],[12,29],[11,22],[6,15],[-5,5]];out[k]={};
 for(const[name,line]of Object.entries(lines)){let distance=0,rows=[];for(let i=1;i<line.length;i++){const a=line[i-1],b=line[i],len=Math.hypot(a[0]-b[0],a[1]-b[1]),n=Math.ceil(len/.25);for(let j=0;j<n;j++){const t=j/n,x=a[0]+(b[0]-a[0])*t,z=a[1]+(b[1]-a[1])*t;rows.push({s:distance+t*len,x,z,y:f.world.groundHeight(x,z)});}distance+=len;}const[x,z]=line.at(-1);rows.push({s:distance,x,z,y:f.world.groundHeight(x,z)});out[k][name]={line,rows,length:distance};}
}
writeFileSync('validation/reset-a/profiles.json',JSON.stringify(out));console.log(JSON.stringify(Object.fromEntries(Object.entries(out).map(([k,r])=>[k,Object.fromEntries(Object.entries(r).map(([n,p])=>[n,{length:p.length,groundRange:[Math.min(...p.rows.map(q=>q.y)),Math.max(...p.rows.map(q=>q.y))]}]))]))));f.dispose();
