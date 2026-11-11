import * as T from'../vendor/three-atlas.module.js?v=16';

export function distantIslandGeometry(profile=0){
 const p=[],c=[],idx=[],n=22,stone=new T.Color('#627d87'),grass=new T.Color('#6c9084');
 const shape=(a)=>1+.17*Math.sin(a*3+profile)+.1*Math.cos(a*5-profile*.7);
 for(let r=0;r<4;r++)for(let i=0;i<n;i++){
  const a=i/n*Math.PI*2,s=shape(a),scale=[1,1.05,.63,.05][r],stretch=profile%2?1.45:.95;
  const y=r===0?2+3*Math.sin(a*2+profile)+2*Math.cos(a*3):[-1,-9,-25,-43][r]+Math.sin(a*3+profile)*2;
  p.push(Math.cos(a)*25*s*scale*stretch-3*r,y,Math.sin(a)*22*s*scale/stretch+1.5*r);
  const col=(r===0?grass:stone).clone().multiplyScalar(.92+.1*Math.sin(a*3+r));c.push(col.r,col.g,col.b);
 }
 const peak=p.length/3;p.push(-3,profile%2?16:9,-3);c.push(grass.r,grass.g,grass.b);
 for(let i=0;i<n;i++)idx.push(peak,(i+1)%n,i);
 for(let r=0;r<3;r++)for(let i=0;i<n;i++){const a=r*n+i,b=r*n+(i+1)%n;idx.push(a,b,a+n,b,b+n,a+n);}
 const tip=p.length/3;p.push(-9,-47,4.5);c.push(stone.r,stone.g,stone.b);for(let i=0;i<n;i++)idx.push(3*n+i,3*n+(i+1)%n,tip);
 const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(p,3));g.setAttribute('color',new T.Float32BufferAttribute(c,3));g.setIndex(idx);g.computeVertexNormals();return g;
}

export function createAtmosphere({scene,b,ownedMaterials}){
 const skyMat=new T.ShaderMaterial({
  side:T.BackSide,depthWrite:false,toneMapped:false,
  uniforms:{zenith:{value:new T.Color('#3274ae')},horizon:{value:new T.Color('#8bb0c0')},lowerSky:{value:new T.Color('#5989a8')}},
  vertexShader:'varying vec3 p;void main(){p=position;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',
  fragmentShader:`varying vec3 p;uniform vec3 zenith;uniform vec3 horizon;uniform vec3 lowerSky;
  void main(){vec3 d=normalize(p);float h=d.y;
   vec3 col=mix(horizon,zenith,smoothstep(-.02,.78,h));
   if(h<0.)col=mix(horizon,lowerSky,smoothstep(0.,.72,-h));
   float sunlight=pow(max(0.,dot(d,normalize(vec3(-.55,.70,.45)))),24.);
   col+=vec3(.055,.035,.012)*sunlight;
   gl_FragColor=vec4(col,1.);
   #include <colorspace_fragment>
  }`
 });
 ownedMaterials.add(skyMat);const sky=b.mesh(new T.SphereGeometry(1000,32,20),skyMat);sky.name='Painterly blue sky / horizon and lower atmosphere';sky.castShadow=sky.receiveShadow=false;
 const material=new T.ShaderMaterial({
  transparent:true,depthWrite:false,side:T.DoubleSide,toneMapped:false,
  uniforms:{lit:{value:new T.Color('#f1e7ce')},shade:{value:new T.Color('#7d9eaf')},haze:{value:new T.Color('#8bb0c0')}},
  vertexShader:`varying vec2 uvp;varying float seed;varying float distanceFog;
   void main(){uvp=uv;vec4 p=vec4(position,1.);seed=0.;
   #ifdef USE_INSTANCING
    p=instanceMatrix*p;seed=sin(instanceMatrix[3].x*.037+instanceMatrix[3].z*.013)*3.14;
   #endif
   vec4 mv=modelViewMatrix*p;distanceFog=clamp((-mv.z-130.)/650.,0.,.8);gl_Position=projectionMatrix*mv;}`,
  fragmentShader:`varying vec2 uvp;varying float seed;varying float distanceFog;uniform vec3 lit;uniform vec3 shade;uniform vec3 haze;
   void main(){vec2 p=(uvp-.5)*2.;float s=sin(seed),a=0.;
    a=max(a,1.-length((p-vec2(-.48,-.10))/vec2(.50,.30+.06*s)));
    a=max(a,1.-length((p-vec2(-.13,.12+.08*s))/vec2(.49,.60)));
    a=max(a,1.-length((p-vec2(.31,.03))/vec2(.52,.43-.06*s)));
    a=max(a,1.-length((p-vec2(.64,-.13))/vec2(.35,.25)));
    float edge=sin(p.x*13.+seed)*sin(p.y*8.+seed)*.035+sin(p.x*23.-p.y*7.+seed)*.015;
    float alpha=smoothstep(.005,.22,a+edge)*(.86-distanceFog*.18);
    vec3 col=mix(shade,lit,smoothstep(-.58,.5,p.y)*.78+a*.22);col=mix(col,haze,distanceFog*.45);
    gl_FragColor=vec4(col,alpha);
    #include <colorspace_fragment>
   }`
 });ownedMaterials.add(material);
 const geo=new T.PlaneGeometry(1,1);b.owned.add(geo);const defs=[];
 for(const[x,y,z,w]of[[-165,-62,70,115],[140,-70,125,130],[-70,-92,-150,155],[170,-48,-110,110],[-225,40,-170,125],[150,62,-290,135],[-245,30,165,140],[220,-26,-5,105],[-95,95,-280,95],[245,90,145,130]])for(let i=0;i<3;i++)defs.push({x:x+(i-1)*w*.31,y:y+Math.sin(i*2+x)*w*.045,z:z+i*8,w:w*(.65+i%2*.2),h:w*(.32+i%2*.04),phase:i+x});
 for(const[x,z]of[[-430,-400],[200,-500],[500,70],[-450,230]])defs.push({x,y:30,z,w:250,h:28,phase:x});
 const clouds=new T.InstancedMesh(geo,material,defs.length);clouds.name='Layered cloud banks / varied puffs and horizon wisps';clouds.castShadow=clouds.receiveShadow=false;clouds.frustumCulled=false;scene.add(clouds);const dummy=new T.Object3D();
 return{cloudCount:defs.length,update(time,reduced,camera){if(!camera)return;for(let i=0;i<defs.length;i++){const d=defs[i];dummy.position.set(d.x+(reduced?0:Math.sin(time*.009+d.phase)*4),d.y,d.z);dummy.quaternion.copy(camera.quaternion);dummy.scale.set(d.w,d.h,1);dummy.updateMatrix();clouds.setMatrixAt(i,dummy.matrix);}clouds.instanceMatrix.needsUpdate=true;}};
}
