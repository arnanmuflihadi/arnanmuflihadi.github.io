// Merchant Citadel P2-B: loader-side production helpers for the isolated preview (no game module is touched).
//  - dedupeMaterials: one material object per distinct (name, colour, constants, textures, flags)
//  - mergeByGroup: static merge of placed meshes by (group x material) with world transforms baked, frustum culling kept
//  - fitSunShadow: orthographic shadow frustum fitted to the scene's bounding box in light space
// The game's vendored three build is a curated subset, so everything is written against the exports that exist (see p2a.js).

const texKey = (t) => (t ? ((t.source && t.source.uuid) || (t.image && t.image.uuid) || t.uuid) : '-');

export function materialKey(m) {
  return [m.name.split('.')[0], m.type, m.color ? m.color.getHex() : '-', m.emissive ? m.emissive.getHex() : '-', m.roughness, m.metalness, m.side, m.transparent, m.opacity, m.alphaTest, m.vertexColors,
    m.envMapIntensity, texKey(m.map), texKey(m.normalMap), texKey(m.roughnessMap), texKey(m.metalnessMap), texKey(m.aoMap), texKey(m.emissiveMap), texKey(m.alphaMap)].join('|');
}

/** Replace duplicate material objects (same key) by the first one seen; returns {before, after, saved}. */
export function dedupeMaterials(root) {
  const canon = new Map(), seen = new Set(); let before = 0;
  root.traverse((o) => {
    if (!o.isMesh) return;
    const list = [].concat(o.material), out = list.map((m) => {
      if (!seen.has(m)) { seen.add(m); before++; }
      const k = materialKey(m); if (!canon.has(k)) canon.set(k, m); return canon.get(k);
    });
    o.material = Array.isArray(o.material) ? out : out[0];
  });
  return { before, after: canon.size, saved: before - canon.size, canon };
}

/** Static merge: every non-instanced mesh under `root` goes into one mesh per (groupOf(mesh) x material x attribute set). */
export function mergeByGroup(T, root, groupOf, { name = 'MERGED', cull = true, cellSize = 0, quantize = false } = {}) {
  const buckets = new Map(); root.updateMatrixWorld(true); const out = new T.Group(); out.name = name;
  const add = (o, grp) => {
    const key = grp + '|' + o.material.uuid + '|' + Object.keys(o.geometry.attributes).join(',');
    if (!buckets.has(key)) buckets.set(key, { group: grp, material: o.material, list: [] }); buckets.get(key).list.push(o);
  };
  root.traverse((o) => {
    if (!o.isMesh) return;
    if (o.isInstancedMesh) { const c = o.clone(); c.applyMatrix4(o.parent.matrixWorld); out.add(c); return; }
    if (!cellSize) { add(o, groupOf(o)); return; }
    if (!o.geometry.boundingSphere) o.geometry.computeBoundingSphere();
    const c = o.geometry.boundingSphere.center.clone().applyMatrix4(o.matrixWorld), r = o.geometry.boundingSphere.radius * Math.max(o.matrixWorld.getMaxScaleOnAxis(), 1e-6);
    const cx0 = Math.floor((c.x - r) / cellSize), cx1 = Math.floor((c.x + r) / cellSize), cz0 = Math.floor((c.z - r) / cellSize), cz1 = Math.floor((c.z + r) / cellSize);
    if (cx0 === cx1 && cz0 === cz1) { add(o, `c${cx0}_${cz0}`); return; }                       // wholly inside one cell
    if (r * 2 <= cellSize * 0.6) { add(o, `c${Math.floor(c.x / cellSize)}_${Math.floor(c.z / cellSize)}`); return; }   // a building: kept whole in the cell of its centre
    for (const piece of splitMeshByCell(T, o, cellSize)) add(piece, piece.userData.cell);       // ground, paving, district dressing: triangles go to the cell of their centroid
  });
  const NM = new T.Object3D().normalMatrix.constructor, v = new T.Vector3(), nm = new NM(); let triangles = 0;
  for (const { group, material, list } of buckets.values()) {
    const names = Object.keys(list[0].geometry.attributes); let vc = 0, ic = 0;
    for (const o of list) { vc += o.geometry.attributes.position.count; ic += o.geometry.index ? o.geometry.index.count : o.geometry.attributes.position.count; }
    const arrays = {}; for (const n of names) arrays[n] = new Float32Array(vc * list[0].geometry.attributes[n].itemSize); const index = new Uint32Array(ic); let vo = 0, io = 0;
    for (const o of list) {
      const g = o.geometry, pc = g.attributes.position.count; nm.getNormalMatrix(o.matrixWorld);
      for (const n of names) {
        const a = g.attributes[n], dst = arrays[n], sz = a.itemSize;
        for (let i = 0; i < pc; i++) {
          if (n === 'position') { v.fromBufferAttribute(a, i).applyMatrix4(o.matrixWorld); dst[(vo + i) * 3] = v.x; dst[(vo + i) * 3 + 1] = v.y; dst[(vo + i) * 3 + 2] = v.z; }
          else if (n === 'normal') { v.fromBufferAttribute(a, i).applyNormalMatrix(nm).normalize(); dst[(vo + i) * 3] = v.x; dst[(vo + i) * 3 + 1] = v.y; dst[(vo + i) * 3 + 2] = v.z; }
          else for (let k = 0; k < sz; k++) dst[(vo + i) * sz + k] = a.getComponent(i, k);
        }
      }
      if (g.index) for (let i = 0; i < g.index.count; i++) index[io + i] = g.index.getX(i) + vo; else for (let i = 0; i < pc; i++) index[io + i] = vo + i;
      vo += pc; io += g.index ? g.index.count : pc;
    }
    const geo = new T.BufferGeometry(); let qk = 0, qc = null;
    if (quantize) {                                                                  // P2-B batch 4: re-quantise the merged geometry (Int16 positions relative to the bucket centre with a power-of-two mesh scale, Int8 normals, Uint16 uv when they fit in [0, 1], Uint8 colour and AO)
      const BA = Object.getPrototypeOf(T.Float32BufferAttribute), pos = arrays.position;           // the generic BufferAttribute class (the curated build does not export it, but Float32BufferAttribute extends it)
       let mn = [1e9, 1e9, 1e9], mx = [-1e9, -1e9, -1e9];
      for (let i = 0; i < pos.length; i += 3) for (let k = 0; k < 3; k++) { if (pos[i + k] < mn[k]) mn[k] = pos[i + k]; if (pos[i + k] > mx[k]) mx[k] = pos[i + k]; }
      qc = [(mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2, (mn[2] + mx[2]) / 2]; const half = Math.max(mx[0] - mn[0], mx[1] - mn[1], mx[2] - mn[2]) / 2 + 1e-6; qk = Math.min(13, Math.floor(Math.log2(32767 / half)));
      const q = new Int16Array(pos.length), sc = 2 ** qk; for (let i = 0; i < pos.length; i += 3) for (let k = 0; k < 3; k++) q[i + k] = Math.round((pos[i + k] - qc[k]) * sc);
      geo.setAttribute('position', new BA(q, 3, false));
      for (const n of names) {
        if (n === 'position') continue; const a = arrays[n], isz = list[0].geometry.attributes[n].itemSize; let out, norm = false;
        if (n === 'normal') { out = new Int8Array(a.length); for (let i = 0; i < a.length; i++) out[i] = Math.max(-127, Math.min(127, Math.round(a[i] * 127))); norm = true; }
        else if (n === 'uv' && a.every((v) => v >= 0 && v <= 1)) { out = new Uint16Array(a.length); for (let i = 0; i < a.length; i++) out[i] = Math.round(a[i] * 65535); norm = true; }
        else if (n === 'color' || n === 'aoBaked' || n === '_ao') { out = new Uint8Array(a.length); for (let i = 0; i < a.length; i++) out[i] = Math.max(0, Math.min(255, Math.round(a[i] * 255))); norm = true; }
        else out = a;
        geo.setAttribute(n, new BA(out, isz, norm));
      }
    } else for (const n of names) { const A0 = list[0].geometry.attributes[n]; geo.setAttribute(n, A0.isInterleavedBufferAttribute ? new T.Float32BufferAttribute(arrays[n], A0.itemSize) : new A0.constructor(arrays[n], A0.itemSize)); }
    geo.setIndex(new (list[0].geometry.index.constructor)(index, 1)); geo.computeBoundingSphere(); geo.computeBoundingBox();
    const m = new T.Mesh(geo, material); if (quantize) { m.position.set(qc[0], qc[1], qc[2]); m.scale.setScalar(2 ** -qk); } m.name = `${name}_${group}_${material.name}`; m.castShadow = true; m.receiveShadow = true; m.frustumCulled = cull; m.userData.group = group; out.add(m); triangles += ic / 3;
  }
  out.userData.stats = { meshes: out.children.length, buckets: buckets.size, triangles };
  return out;
}

/** Fit the sun's orthographic shadow camera to the bounding box `box` (three Box3) in light space. */
export function fitSunShadow(T, sun, box, margin = 4) {
  const f = sun.target.position.clone().sub(sun.position).normalize(), up = new T.Vector3(0, 1, 0);
  const r = new T.Vector3().crossVectors(f, up).normalize(), u = new T.Vector3().crossVectors(r, f).normalize();
  let x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9, z0 = 1e9, z1 = -1e9; const c = new T.Vector3();
  for (let i = 0; i < 8; i++) {
    c.set(i & 1 ? box.max.x : box.min.x, i & 2 ? box.max.y : box.min.y, i & 4 ? box.max.z : box.min.z).sub(sun.position);
    const a = c.dot(r), b = c.dot(u), d = c.dot(f); x0 = Math.min(x0, a); x1 = Math.max(x1, a); y0 = Math.min(y0, b); y1 = Math.max(y1, b); z0 = Math.min(z0, d); z1 = Math.max(z1, d);
  }
  const s = sun.shadow.camera; s.left = x0 - margin; s.right = x1 + margin; s.bottom = y0 - margin; s.top = y1 + margin; s.near = Math.max(0.5, z0 - margin); s.far = z1 + margin; s.updateProjectionMatrix();
  return { width: x1 - x0 + 2 * margin, height: y1 - y0 + 2 * margin, depth: z1 - z0 + 2 * margin };
}


/** Split one large mesh into pseudo-meshes (geometry + matrixWorld + material) by the cell of each triangle's centroid in world space. */
export function splitMeshByCell(T, o, size) {
  const g = o.geometry, pos = g.attributes.position, n = pos.count, idx = g.index, m = o.matrixWorld, v = new T.Vector3();
  const wx = new Float32Array(n), wz = new Float32Array(n);
  for (let i = 0; i < n; i++) { v.fromBufferAttribute(pos, i).applyMatrix4(m); wx[i] = v.x; wz[i] = v.z; }
  const tris = idx ? idx.count / 3 : n / 3, cells = new Map();
  for (let t = 0; t < tris; t++) {
    const a = idx ? idx.getX(t * 3) : t * 3, b = idx ? idx.getX(t * 3 + 1) : t * 3 + 1, c = idx ? idx.getX(t * 3 + 2) : t * 3 + 2;
    const key = `c${Math.floor((wx[a] + wx[b] + wx[c]) / 3 / size)}_${Math.floor((wz[a] + wz[b] + wz[c]) / 3 / size)}`;
    if (!cells.has(key)) cells.set(key, []); cells.get(key).push(a, b, c);
  }
  const names = Object.keys(g.attributes), out = [];
  for (const [key, list] of cells) {
    const remap = new Map(), src = []; const index = new Uint32Array(list.length);
    for (let k = 0; k < list.length; k++) { let j = remap.get(list[k]); if (j === undefined) { j = src.length; remap.set(list[k], j); src.push(list[k]); } index[k] = j; }
    const ng = new T.BufferGeometry();
    for (const nm of names) {
      const A = g.attributes[nm], sz = A.itemSize, arr = new Float32Array(src.length * sz);
      for (let i = 0; i < src.length; i++) for (let k = 0; k < sz; k++) arr[i * sz + k] = A.getComponent(src[i], k);
      ng.setAttribute(nm, new T.Float32BufferAttribute(arr, sz));
    }
    if (!g.index) throw new Error('splitMeshByCell: source geometry must be indexed'); ng.setIndex(new g.index.constructor(index, 1));          // the curated three build exports no BufferAttribute: reuse the source index class
    out.push({ isMesh: true, geometry: ng, matrixWorld: m, material: o.material, userData: { cell: key } });
  }
  return out;
}


/** Decode-at-load: turn KHR_mesh_quantization attributes back into Float32 (positions multiplied by the node's power-of-two scale, which is reset to 1). Keeps the smaller download, renders like the float kit. */
export function dequantizeKit(T, sceneRoot) {
  let attrs = 0, ms = performance.now();
  sceneRoot.children.forEach((node) => {
    const s = node.scale.x; if (s === 1) return; let any = false;
    node.traverse((o) => {
      if (!o.isMesh) return; const g = o.geometry; if (g.userData.dequantized) return; g.userData.dequantized = true; any = true;
      for (const [name, a] of Object.entries(g.attributes)) {
        if (!a.isInterleavedBufferAttribute && a.array instanceof Float32Array) continue;
        const sz = a.itemSize, out = new Float32Array(a.count * sz); for (let i = 0; i < a.count; i++) for (let k = 0; k < sz; k++) out[i * sz + k] = a.getComponent(i, k) * (name === 'position' ? s : 1);
        g.setAttribute(name, new T.Float32BufferAttribute(out, sz)); attrs++;
      }
      g.computeBoundingSphere(); g.computeBoundingBox();
    });
    if (any) node.scale.setScalar(1);
  });
  return { attributes_converted: attrs, ms: performance.now() - ms };
}
