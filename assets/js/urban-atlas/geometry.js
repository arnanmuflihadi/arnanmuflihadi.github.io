import * as T from '../vendor/three-atlas.module.js?v=16';
// Authored, reusable architectural geometry. All dimensions use conceptual metres.
export function footprint(width, depth, cut = .7) {
  const x = width / 2, z = depth / 2, s = new T.Shape();
  s.moveTo(-x + cut, -z); s.lineTo(x - cut, -z); s.lineTo(x, -z + cut);
  s.lineTo(x, z - cut); s.lineTo(x - cut, z); s.lineTo(-x + cut, z);
  s.lineTo(-x, z - cut); s.lineTo(-x, -z + cut); s.closePath();
  return s;
}
export function extrudedPlan(width, depth, height, cut = .5) {
  const g = new T.ExtrudeGeometry(footprint(width, depth, cut), { depth: height, bevelEnabled: false, steps: 1 });
  g.rotateX(-Math.PI / 2); return g;
}
export function shellRoof(width, depth, rise = 1.6, thickness = .22) {
  const vertices = [], indices = [], n = 32;
  for (let side = 0; side < 2; side++) for (let j = 0; j <= 1; j++) for (let i = 0; i <= n; i++) {
    const u = i / n * 2 - 1;
    // Soft vault with subtly lifted eaves; no borrowed game geometry.
    const y = rise * (1 - u * u) + .22 * Math.pow(Math.abs(u), 8) - side * thickness;
    vertices.push(u * width / 2, y, (j - .5) * depth);
  }
  const row = n + 1, layer = row * 2;
  for (let i = 0; i < n; i++) {
    indices.push(i, i + row, i + 1, i + 1, i + row, i + row + 1);
    const k = i + layer; indices.push(k, k + 1, k + row, k + 1, k + row + 1, k + row);
    for (const j of [0, 1]) { const a = i + j * row; if(j===0)indices.push(a, a + 1, a + layer, a + 1, a + layer + 1, a + layer); else indices.push(a, a + layer, a + 1, a + 1, a + layer, a + layer + 1); }
  }
  for (const i of [0, n]) { if(i===0)indices.push(i, i + layer, i + row, i + layer, i + row + layer, i + row); else indices.push(i, i + row, i + layer, i + layer, i + row, i + row + layer); }
  const g = new T.BufferGeometry(); g.setAttribute('position', new T.Float32BufferAttribute(vertices, 3)); g.setIndex(indices); g.computeVertexNormals(); return g;
}
export function gableRoof(width, depth, rise) {
  const shape = new T.Shape(); shape.moveTo(-width / 2, 0); shape.lineTo(0, rise); shape.lineTo(width / 2, 0); shape.lineTo(width / 2, -.18); shape.lineTo(-width / 2, -.18); shape.closePath();
  const g = new T.ExtrudeGeometry(shape, { depth, bevelEnabled: false }); g.translate(0, 0, -depth / 2); return g;
}
export function archFrame(width, height, thickness = .24, depth = .35) {
  const s = new T.Shape(), radius = width / 2, spring = height - radius;
  s.moveTo(-radius - thickness, 0); s.lineTo(-radius - thickness, spring);
  s.absarc(0, spring, radius + thickness, Math.PI, 0, true);
  s.lineTo(radius + thickness, 0); s.lineTo(radius, 0); s.lineTo(radius, spring);
  s.absarc(0, spring, radius, 0, Math.PI, false); s.lineTo(-radius, 0); s.closePath();
  return new T.ExtrudeGeometry(s, { depth, bevelEnabled: false, curveSegments: 16 });
}
export function leafRibbon(length = 3.5) {
  const pos = [], idx = [], n = 12;
  for (let i = 0; i <= n; i++) {
    const t = i / n, w = Math.sin(t * Math.PI) * .42, y = Math.sin(t * Math.PI) * .45 - t * t * 1.25;
    pos.push(-w, y, t * length, w, y, t * length);
    if (i < n) { const k = i * 2; idx.push(k, k + 2, k + 1, k + 1, k + 2, k + 3); }
  }
  const g = new T.BufferGeometry(); g.setAttribute('position', new T.Float32BufferAttribute(pos, 3)); g.setIndex(idx); g.computeVertexNormals(); return g;
}
export function createBuilder(scene, materials) {
  const cube = new T.BoxGeometry(1, 1, 1), sphere = new T.SphereGeometry(1, 14, 10), cylinder = new T.CylinderGeometry(1, 1, 1, 10);
  let channel='default',offset=new T.Vector3();
  const batches = new Map(), owned = new Set([cube, sphere, cylinder]);
  function instance(geometry, material, x, y, z, sx = 1, sy = 1, sz = 1, ry = 0, rz = 0, rx = 0) {
    const key = geometry.uuid + material.uuid + channel;
    if (!batches.has(key)) batches.set(key, { geometry, material, channel, transforms: [] });
    const dummy = new T.Object3D(); dummy.position.set(x+offset.x,y+offset.y,z+offset.z); dummy.scale.set(sx, sy, sz); dummy.rotation.set(rx, ry, rz); dummy.updateMatrix(); batches.get(key).transforms.push(dummy.matrix.clone());
  }
  function mesh(geometry, color, x = 0, y = 0, z = 0, ry = 0) {
    owned.add(geometry); const m = new T.Mesh(geometry, typeof color === 'string' ? materials.toon(color) : color); m.position.set(x+offset.x,y+offset.y,z+offset.z); m.rotation.y = ry; m.castShadow = m.receiveShadow = true; m.userData.atlasGroup=channel;scene.add(m); return m;
  }
  const box = (x, y, z, w, h, d, color, ry = 0, rz = 0, rx = 0) => instance(cube, materials.toon(color), x, y, z, w, h, d, ry, rz, rx);
  const ball = (x, y, z, w, h, d, color) => instance(sphere, materials.toon(color), x, y, z, w, h, d);
  const column = (x, y, z, r, h, color, rz = 0) => instance(cylinder, materials.toon(color), x, y, z, r, h, r, 0, rz);
  return { box, ball, column, mesh, instance, sphere, owned, translated(x,y,z,fn){const previous=offset;offset=offset.clone().add(new T.Vector3(x,y,z));try{return fn();}finally{offset=previous;}},inGroup(name,fn){const previous=channel;channel=name;try{return fn();}finally{channel=previous;}},
    flush() { batches.forEach(({geometry, material, transforms, channel:group}) => { const m = new T.InstancedMesh(geometry, material, transforms.length); transforms.forEach((matrix, i) => m.setMatrixAt(i, matrix)); m.castShadow = true; m.receiveShadow = !material.userData.noReceiveShadow; m.computeBoundingSphere();m.userData.atlasGroup=group; scene.add(m); }); batches.clear(); },
  };
}

export function accessRamp(width,run,rise){
  const w=width/2, g=new T.BufferGeometry();
  g.setAttribute('position',new T.Float32BufferAttribute([-w,0,0,w,0,0,-w,rise,-run,w,rise,-run,-w,-.1,0,w,-.1,0,-w,-.1,-run,w,-.1,-run],3));
  g.setIndex([0,1,2,1,3,2,4,6,5,5,6,7,0,4,1,1,4,5,2,3,6,3,7,6,0,2,4,2,6,4,1,5,3,3,5,7]);
  g.computeVertexNormals();return g;
}
