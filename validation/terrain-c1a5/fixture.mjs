import {fixture as baseline}from'../town-s2g/fixture.mjs';
import {integrateTown}from'../../assets/js/floating-atlas/town-integration.js';
export async function fixture(){const f=await baseline();f.town.dispose();const town=await integrateTown(f.world,{terrainStudy:true});return{...f,town,dispose(){town.dispose();f.world.dispose();}};}
