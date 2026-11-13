import * as T from'../vendor/three-atlas.module.js?v=16';
export function createAtmosphere({scene,b,ownedMaterials}){
 const skyMat=new T.ShaderMaterial({side:T.BackSide,depthWrite:false,toneMapped:false,vertexShader:'varying vec3 p;void main(){p=position;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',fragmentShader:`varying vec3 p;void main(){vec3 d=normalize(p);float h=d.y;vec3 col=mix(vec3(.83,.88,.81),vec3(.18,.44,.61),pow(max(h,0.),.45));col=mix(col,vec3(.69,.80,.81),clamp(-h*.9,0.,.65));float sun=pow(max(0.,dot(d,normalize(vec3(-.55,.70,.45)))),90.);col+=vec3(.15,.11,.045)*sun;gl_FragColor=vec4(col,1.);
#include <colorspace_fragment>
}`});ownedMaterials.add(skyMat);const sky=b.mesh(new T.SphereGeometry(1000,32,20),skyMat);sky.name='Daylight sky / altitude gradient';sky.castShadow=sky.receiveShadow=false;
 const material=new T.ShaderMaterial({transparent:true,depthWrite:false,side:T.DoubleSide,toneMapped:false,uniforms:{},vertexShader:'varying vec2 uvp;void main(){uvp=uv;vec4 p=vec4(position,1.);\n#ifdef USE_INSTANCING\np=instanceMatrix*p;\n#endif\ngl_Position=projectionMatrix*modelViewMatrix*p;}',fragmentShader:`varying vec2 uvp;void main(){vec2 p=(uvp-.5)*2.;float a=0.;a=max(a,1.-length((p-vec2(-.48,-.05))/vec2(.52,.38)));a=max(a,1.-length((p-vec2(-.13,.12))/vec2(.57,.64)));a=max(a,1.-length((p-vec2(.30,.05))/vec2(.55,.48)));a=max(a,1.-length((p-vec2(.65,-.1))/vec2(.35,.28)));a=smoothstep(0.,.22,a);vec3 col=mix(vec3(.66,.78,.79),vec3(.98,.96,.85),smoothstep(-.55,.5,p.y));gl_FragColor=vec4(col,a*.88);
#include <colorspace_fragment>
}`});ownedMaterials.add(material);
 const geo=new T.PlaneGeometry(1,1);b.owned.add(geo);const defs=[];
 for(const[x,y,z,w]of[[-165,-65,70,125],[130,-76,115,145],[-65,-87,-150,160],[150,-54,-85,100],[-210,36,-160,135],[130,54,-240,125],[-240,25,160,140],[200,-25,-5,100],[-100,83,-250,105],[220,76,130,140]])for(let i=0;i<4;i++)defs.push({x:x+(i-1.5)*w*.21,y:y+Math.sin(i*2)*w*.045,z:z+i*6,w:w*(.7+i%2*.15),h:w*.4,phase:i+x});
 const clouds=new T.InstancedMesh(geo,material,defs.length);clouds.name='Layered cloud banks';clouds.castShadow=clouds.receiveShadow=false;clouds.frustumCulled=false;scene.add(clouds);const dummy=new T.Object3D();
 return{cloudCount:defs.length,update(time,reduced,camera){if(!camera)return;for(let i=0;i<defs.length;i++){const d=defs[i];dummy.position.set(d.x+(reduced?0:Math.sin(time*.009+d.phase)*4),d.y,d.z);dummy.quaternion.copy(camera.quaternion);dummy.scale.set(d.w,d.h,1);dummy.updateMatrix();clouds.setMatrixAt(i,dummy.matrix);}clouds.instanceMatrix.needsUpdate=true;}};
}
