import{fixture}from'./fixture.mjs';import{blocked}from'../../assets/js/floating-atlas/collision.js?v=73';
const f=await fixture();for(let i=-1;i<=12;i++){const t=i/10,x=36-1.5*t,z=-1.8*t,y=f.town.heightAt(x,z);console.log(JSON.stringify({x,z,y,square:f.town.square.support(x,z),blocks:f.world.obstacles.filter(o=>y+1.9>o.minY&&y<o.h-.05&&blocked(x,z,[o])).map(o=>o.square||o)}));}f.dispose();
