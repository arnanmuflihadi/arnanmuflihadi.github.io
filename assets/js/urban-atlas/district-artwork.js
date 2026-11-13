import * as T from '../vendor/three-atlas.module.js?v=16';
export function createDistrictArtwork({anisotropy=4}={}){
  const textures=new Set(),displays=new Map(),signs=new Map();
  function texture(canvas,name){const map=new T.CanvasTexture(canvas);map.name=name;map.colorSpace=T.SRGBColorSpace;map.magFilter=T.LinearFilter;map.generateMipmaps=true;map.anisotropy=Math.min(8,anisotropy);textures.add(map);return map;}
  function sign(title,subtitle='',width=8,height=.5){
    const key=[title,subtitle,width,height].join('|');if(signs.has(key))return signs.get(key);
    const c=document.createElement('canvas');c.width=2048;c.height=Math.max(96,Math.round(c.width*height/width));const p=c.getContext('2d');p.fillStyle='#203e36';p.fillRect(0,0,c.width,c.height);p.textAlign='center';p.fillStyle='#fff1cb';
    let size=Math.round(c.height*(subtitle?.58:.7));p.font='700 '+size+'px Arial';const measured=p.measureText?.(title)?.width||title.length*size*.62;if(measured>c.width*.9){size=Math.floor(size*c.width*.9/measured);p.font='700 '+size+'px Arial';}p.fillText(title,c.width/2,c.height*(subtitle?.62:.77));
    if(subtitle){p.font='600 '+Math.round(c.height*.16)+'px Arial';p.fillStyle='#e0ddbd';p.fillText(subtitle,c.width/2,c.height*.89);}const map=texture(c,'Original district sign: '+title);signs.set(key,map);return map;
  }
  function display(style){if(displays.has(style))return displays.get(style);
    const c=document.createElement('canvas');c.width=768;c.height=512;const p=c.getContext('2d');p.fillStyle='#bba88b';p.fillRect(0,0,768,512);p.fillStyle='#746b57';p.fillRect(0,374,768,138);p.fillStyle='#d2c0a0';p.fillRect(42,24,684,335);p.fillStyle='#554f43';
    if(style==='books'){for(const y of[156,288]){p.fillRect(54,y,660,13);for(let i=0;i<22;i++){p.fillStyle=['#667e73','#8b5e45','#c7ad72','#897a61'][i%4];p.fillRect(65+i*29,y-85+(i%3)*9,18+(i%3)*3,85-(i%3)*9);}}p.fillStyle='#586653';p.fillRect(475,315,185,62);}
    else if(style==='cafe'){p.fillStyle='#8a6748';p.fillRect(50,286,668,90);p.fillStyle='#455b54';p.fillRect(83,192,120,95);p.fillStyle='#d3b179';p.fillRect(102,211,80,36);for(let i=0;i<7;i++){p.fillStyle='#dbbd88';p.fillRect(255+i*54,260,34,25);p.fillStyle='#6c7161';p.fillRect(253+i*54,251,38,7);}p.fillStyle='#4d6056';for(const x of[235,580]){p.fillRect(x,365,8,95);p.fillRect(x-52,359,112,10);p.fillRect(x-46,407,7,52);p.fillRect(x+41,407,7,52);}}
    else{for(const x of[90,315,545]){p.fillStyle='#807b60';p.fillRect(x,110,130,8);p.fillRect(x,278,130,8);p.fillStyle='#a9694b';p.fillRect(x+35,219,62,56);p.fillStyle='#536e51';p.beginPath();p.ellipse(x+65,186,44,40,0,0,Math.PI*2);p.fill();p.fillStyle='#758f6b';p.beginPath();p.ellipse(x+75,155,25,47,.3,0,Math.PI*2);p.fill();}}
    p.fillStyle='#354c4340';p.fillRect(0,0,27,512);p.fillRect(741,0,27,512);p.fillRect(0,0,768,18);const result=texture(c,'Original painted shop-room silhouette: '+style);displays.set(style,result);return result;
  }
  return{sign,display,dispose(){textures.forEach(t=>t.dispose());}};
}
