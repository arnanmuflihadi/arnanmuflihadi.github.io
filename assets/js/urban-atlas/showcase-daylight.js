import * as T from '../vendor/three-atlas.module.js?v=16';

export const daylightPreset=Object.freeze({id:'neutral-stylized-daytime',hemisphere:2.05,sun:2.15,exposure:1,shadowMap:2048,normalBias:.012,fogNear:90,fogFar:200,postprocessing:false});

export function createShowcaseDaylight(scene){
  const width=2,height=128,pixels=new Uint8Array(width*height*4),horizon=new T.Color('#e6e9e2'),zenith=new T.Color('#acc9df');
  for(let y=0;y<height;y++){const t=y/(height-1),c=horizon.clone().lerp(zenith,Math.pow(t,.7));for(let x=0;x<width;x++){const i=(y*width+x)*4;pixels[i]=Math.round(c.r*255);pixels[i+1]=Math.round(c.g*255);pixels[i+2]=Math.round(c.b*255);pixels[i+3]=255;}}
  const sky=new T.DataTexture(pixels,width,height);sky.name='Project-authored neutral daytime sky';sky.magFilter=T.LinearFilter;sky.minFilter=T.LinearFilter;sky.needsUpdate=true;scene.background=sky;scene.fog=new T.Fog('#d6e1de',daylightPreset.fogNear,daylightPreset.fogFar);
  const fill=new T.HemisphereLight('#eaf2fc','#8a8d80',daylightPreset.hemisphere),sun=new T.DirectionalLight('#fff1df',daylightPreset.sun);sun.position.set(-24,36,25);sun.castShadow=true;sun.shadow.mapSize.set(daylightPreset.shadowMap,daylightPreset.shadowMap);sun.shadow.normalBias=daylightPreset.normalBias;sun.shadow.bias=-.00007;sun.shadow.radius=4;Object.assign(sun.shadow.camera,{left:-34,right:34,top:34,bottom:-34,near:1,far:100});scene.add(fill,sun);
  return {preset:daylightPreset,textureBytes:pixels.byteLength,dispose(){sky.dispose();sun.shadow.dispose();fill.removeFromParent();sun.removeFromParent();}};
}
