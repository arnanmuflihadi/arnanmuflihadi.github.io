import{writeFileSync,readFileSync}from'node:fs';
import{groundHeight,terrainSample,terrainInfo,segmentPoint}from'../../assets/js/floating-atlas/terrain.js';
const source=JSON.parse(readFileSync(new URL('../market-street-s2c/final-site-survey.json',import.meta.url))),boundary=terrainInfo.boundary;
const plots=source.buildingSamples.map(p=>{const[x,floor,z]=p.gameCenter,[w,d]=p.bodyFootprint;let minCliff=Infinity,maxFraction=0;for(const xx of[x-w/2,x,x+w/2])for(const zz of[z-d/2,z,z+d/2]){maxFraction=Math.max(maxFraction,terrainSample(xx,zz).fraction);for(let i=0;i<boundary.length;i++)minCliff=Math.min(minCliff,segmentPoint(xx,zz,boundary[i],boundary[(i+1)%boundary.length]).distance);}return{id:p.id,gameCenter:p.gameCenter,bodyFootprint:p.bodyFootprint,floorToTerrain:p.proposedGroundSupportBelowFloor,nearestBoundaryHorizontalMetres:minCliff,maxTerrainFraction:maxFraction};});
const sections=[];for(let z=60;z>=0;z-=.25)sections.push({x:36,z,terrainY:groundHeight(36,z)});
writeFileSync(new URL('terrain-detail.json',import.meta.url),JSON.stringify({mapping:'game (36+u,18.6+h,44-v)',source:'unchanged R0-A3 exact triangulated support sampler',plots,centreline:sections},null,2)+'\n');
console.log(plots.map(p=>({id:p.id,nearestCliff:p.nearestBoundaryHorizontalMetres,terrainFraction:p.maxTerrainFraction})));
