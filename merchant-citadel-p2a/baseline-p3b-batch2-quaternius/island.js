// Merchant Citadel P3-B batch 1: the floating island in the isolated preview (no production module is touched).
//   - walkable support: island-terrain.bin (int16 cm, 0.5 m grid, bilinear) combined with the town's own 0.2 m grid (max where the town authored a surface)
//   - collision: terrain-aware blocked/slide (rim margin and steepness from island-mask.bin) plus the town's solid proxies; replaces the game's blocked(), whose hard +-105 m limit
//     cannot hold an island that reaches 136 m (the game module itself is NOT edited: the preview passes its own collision object, as the controller allows)
//   - visuals: the exported GLB (terrain top, cliffs, underside, Tea Stack, bridge, water) + instanced vegetation, rocks and quay props
import { createLandingScan } from './island-landing.js';
import { loadFlora } from './flora.js';

export async function loadIsland(T, { townHeightAt, params, scene, say = () => {} }) {
  const get = (u, kind = 'json') => fetch(u).then((r) => { if (!r.ok) throw new Error(u + ' ' + r.status); return r[kind](); });
  const [meta, tBuf, mBuf, inst] = await Promise.all([get('data/island-terrain.json'), get('data/island-terrain.bin', 'arrayBuffer'), get('data/island-mask.bin', 'arrayBuffer'), get('data/island-instances.json')]);
  const H = new Int16Array(tBuf), MK = new Uint8Array(mBuf), { x0, n0, cell, nx, nn } = meta, NOSUP = meta.nosup_height_m, MISSING = meta.nosup_sentinel;

  // ---------------------------------------------------------------------------------------------- support
  function terrainAt(x, n) {
    const fx = (x - x0) / cell, fn = (n - n0) / cell, i = Math.floor(fx), j = Math.floor(fn);
    if (i < 0 || j < 0 || i >= nx - 1 || j >= nn - 1) return NOSUP;
    const k = j * nx + i, a = H[k], b = H[k + 1], c = H[k + nx], d = H[k + nx + 1];
    if (a === MISSING && b === MISSING && c === MISSING && d === MISSING) return NOSUP;
    let av = 0, cnt = 0; for (const v of [a, b, c, d]) if (v !== MISSING) { av += v; cnt++; } av /= cnt;
    const tx = fx - i, tn = fn - j, A = a === MISSING ? av : a, B = b === MISSING ? av : b, C = c === MISSING ? av : c, D = d === MISSING ? av : d;
    return ((A * (1 - tx) + B * tx) * (1 - tn) + (C * (1 - tx) + D * tx) * tn) * 0.01;
  }
  const heightAt = (x, z) => { const t = terrainAt(x, -z), w = townHeightAt(x, z); return w > 0.005 ? Math.max(t, w) : t; };
  const maskAt = (x, n) => { const i = Math.round((x - x0) / cell), j = Math.round((n - n0) / cell); return i < 0 || j < 0 || i >= nx || j >= nn ? 0 : MK[j * nx + i]; };
  const walkable = (x, z) => (maskAt(x, -z) & 5) !== 0, comfortable = (x, z) => (maskAt(x, -z) & 6) !== 0;

  // ---------------------------------------------------------------------------------------------- collision (same obstacle rule as the game's collision.js, terrain mask instead of the +-105 box)
  function blocked(x, z, obstacles, radius = 0.34) {
    if (!walkable(x, z)) return true;
    for (let q = 0; q < obstacles.length; q++) {
      const o = obstacles[q]; if (o.cameraOnly) continue; const dx = x - o.x, dz = z - o.z;
      if (o.oriented) { const c = Math.cos(o.oriented.rotation), s = Math.sin(o.oriented.rotation); if (Math.abs(dx * c - dz * s) < o.oriented.w / 2 + radius && Math.abs(dx * s + dz * c) < o.oriented.d / 2 + radius) return true; }
      else if (Math.abs(dx) < o.w / 2 + radius && Math.abs(dz) < o.d / 2 + radius) return true;
    }
    return false;
  }
  function slide(p, dx, dz, obstacles) {
    const n = Math.max(1, Math.ceil(Math.max(Math.abs(dx), Math.abs(dz)) / 0.1));
    for (let i = 0; i < n; i++) { if (!blocked(p.x + dx / n, p.z, obstacles)) p.x += dx / n; if (!blocked(p.x, p.z + dz / n, obstacles)) p.z += dz / n; }
  }
  // collision proxies of the island's own solids: tree trunks, large rocks, quay props, bridge rails
  const obstacles = [];
  const floraOn = params.get('flora') !== '0';                       // P3-B batch 2: third-party flora replaces the procedural trees, shrubs, rocks and tea hedges
  if (!floraOn) for (const t of inst.tree_trunks) obstacles.push({ src: 'P3B:trunk', group: 'post', x: t.x, z: -t.n, w: 0.5, d: 0.5, h: 3.4 });
  if (!floraOn) for (const r of inst.big_rocks) obstacles.push({ src: 'P3B:rock', group: 'prop', x: r.x, z: -r.n, w: r.r * 1.5, d: r.r * 1.5, h: 1.2 });
  for (const p of inst.prop_solids) obstacles.push({ src: p.src, group: p.src.includes('beacon') || p.src.includes('crane') ? 'wall' : (p.src.includes('counting_stone') ? 'post' : 'prop'), x: p.x, z: -p.n, w: p.w, d: p.d, h: p.h });
  { const b = inst.bridge, ax = b.b[0] - b.a[0], az = -(b.b[1] - b.a[1]), L = Math.hypot(ax, az), rot = Math.atan2(-az, ax), nxn = -az / L, nzn = ax / L;
    for (const sgn of [-1, 1]) obstacles.push({ src: 'P3B:bridge-rail', group: 'prop', x: (b.a[0] + b.b[0]) / 2 + nxn * sgn * (b.width / 2 - 0.05), z: -(b.a[1] + b.b[1]) / 2 + nzn * sgn * (b.width / 2 - 0.05), w: L, d: 0.12, h: 1.1, oriented: { rotation: rot, w: L, d: 0.12 } }); }

  // ---------------------------------------------------------------------------------------------- visuals
  say('loading the island (GLB)…');
  const loader = new T.GLTFLoader(); const t0 = performance.now();
  const gltf = await loader.loadAsync(params.get('islandglb') || 'models/merchant-citadel-p3b-island.glb'); const loadMs = performance.now() - t0;
  const group = new T.Group(); group.name = 'ISLAND'; scene.add(group);
  const nodes = {}; gltf.scene.children.forEach((c) => { nodes[c.name] = c; });
  const time = { value: 0 };
  const NOISE = `float h21(vec2 p){ p=fract(p*vec2(123.34,456.21)); p+=dot(p,p+45.32); return fract(p.x*p.y); }
float vn(vec2 p){ vec2 i=floor(p), f=fract(p); f=f*f*(3.-2.*f); return mix(mix(h21(i),h21(i+vec2(1.,0.)),f.x),mix(h21(i+vec2(0.,1.)),h21(i+vec2(1.,1.)),f.x),f.y); }
float fbm3(vec3 p){ return vn(p.xy*1.0+p.z*0.37)*0.5 + vn(p.zy*2.3+p.x*0.21)*0.3 + vn(p.xz*5.1+p.y*0.5)*0.2; }`;
  const detail = (shader) => {                                          // procedural albedo detail and micro-relief for terrain materials: no texture memory
    shader.uniforms.uTime = time;
    shader.vertexShader = shader.vertexShader.replace('#include <common>', 'attribute float matId;\nvarying float vMat;\nvarying vec3 vWP;\n#include <common>').replace('#include <begin_vertex>', '#include <begin_vertex>\nvMat = matId; vWP = (modelMatrix * vec4(position, 1.0)).xyz;');
    shader.fragmentShader = shader.fragmentShader.replace('#include <common>', 'varying float vMat;\nvarying vec3 vWP;\n' + NOISE + '\n#include <common>')
      .replace('#include <color_fragment>', `#include <color_fragment>
{ float cls = floor(vMat + 0.5); vec3 wp = vWP;
  if (cls < 0.5) { float n = vn(wp.xz*0.9)*0.5 + vn(wp.xz*3.7)*0.3 + vn(wp.xz*13.0)*0.2; diffuseColor.rgb *= 0.80 + 0.40*n; }
  else if (cls < 1.5) { float n = vn(wp.xz*6.0)*0.6 + vn(wp.xz*22.0)*0.4; diffuseColor.rgb *= 0.84 + 0.30*n; }
  else if (cls < 2.5) { vec2 q = wp.xz / vec2(1.3, 0.65); float row = floor(q.y); q.x += 0.5*mod(row, 2.0); vec2 c = fract(q), id = floor(q);
    float edge = min(min(c.x, 1.0-c.x)*1.3, min(c.y, 1.0-c.y)*0.65); float joint = smoothstep(0.0, 0.03, edge); float tint = 0.84 + 0.26*h21(id);
    diffuseColor.rgb *= tint * (0.50 + 0.50*joint) * (0.92 + 0.16*vn(wp.xz*6.0)); }
  else if (cls < 3.5) { float n = fbm3(wp*0.55); float m = vn(vec2(wp.y*2.3 + n*3.0, 0.5)); diffuseColor.rgb *= 0.78 + 0.34*n + 0.12*(m-0.5); }
  else { float rows = 0.5 + 0.5*sin(wp.x*1.9 + wp.z*0.7); diffuseColor.rgb *= 0.88 + 0.16*vn(wp.xz*4.0) - 0.05*rows; } }`)
      .replace('#include <normal_fragment_maps>', `#include <normal_fragment_maps>
{ float cls2 = floor(vMat + 0.5); float amt = cls2 > 2.5 && cls2 < 3.5 ? 0.35 : (cls2 > 1.5 && cls2 < 2.5 ? 0.05 : 0.10);
  vec3 p = vWP * 1.7; float e = 0.07; float c0 = fbm3(p);
  vec3 g = vec3(fbm3(p + vec3(e,0.,0.)) - c0, fbm3(p + vec3(0.,e,0.)) - c0, fbm3(p + vec3(0.,0.,e)) - c0) / e;
  vec3 gv = (viewMatrix * vec4(g, 0.0)).xyz; normal = normalize(normal - amt * (gv - dot(gv, normal) * normal)); }`);
  };
  const waterShader = (fall) => (shader) => {
    shader.uniforms.uTime = time;
    shader.vertexShader = shader.vertexShader.replace('#include <common>', 'varying vec2 vWUv;\n#include <common>').replace('#include <begin_vertex>', '#include <begin_vertex>\nvWUv = uv;');
    shader.fragmentShader = shader.fragmentShader.replace('#include <common>', 'varying vec2 vWUv;\nuniform float uTime;\n#include <common>')
      .replace('#include <color_fragment>', `#include <color_fragment>
{ float s = ${fall ? 'vWUv.y*2.0 + uTime*2.4' : 'vWUv.y*3.0 - uTime*0.9'}; float st = 0.5 + 0.5*sin(s*6.2831 + sin(vWUv.x*9.0)*1.7); st = st*st; float edge = smoothstep(0.0, 0.2, vWUv.x) * smoothstep(1.0, 0.8, vWUv.x);
  diffuseColor.rgb = mix(diffuseColor.rgb, vec3(0.93,0.97,1.0), ${fall ? '0.55 + 0.4*st' : '0.22*st + 0.15*(1.0-edge)'}); diffuseColor.a *= ${fall ? '0.88' : '0.9'} * (0.6 + 0.4*edge); }`);
  };
  const statics = ['ISL_TOP', 'ISL_CLIFF', 'STACK_TOP', 'STACK_CLIFF', 'ISL_ROOTS', 'ISL_DEBRIS', 'BRIDGE'];
  const matsDone = new Set();
  const tune = (o) => {
    if (!o.isMesh) return; const g = o.geometry; if (g.attributes._matid && !g.attributes.matId) g.setAttribute('matId', g.attributes._matid);
    if (!g.attributes.matId) g.setAttribute('matId', new T.Float32BufferAttribute(new Float32Array(g.attributes.position.count).fill(3), 1));
    for (const m of [].concat(o.material)) if (!matsDone.has(m) && (m.name === 'MI_P3B_Top' || m.name === 'MI_P3B_Rock')) { matsDone.add(m); m.userData.extraCompile = detail; }
    o.castShadow = false; o.receiveShadow = true;
  };
  for (const nm of statics) { const o = nodes[nm]; if (!o) { console.warn('island node missing', nm); continue; } o.traverse(tune); group.add(o); }
  for (const nm of ['WATER_STREAM', 'WATER_FALL']) {
    const o = nodes[nm]; if (!o) continue; const fall = nm === 'WATER_FALL';
    o.traverse((c) => { if (!c.isMesh) return; c.material = c.material.clone(); const m = c.material; m.transparent = true; m.depthWrite = false; m.side = T.DoubleSide; m.userData.extraCompile = waterShader(fall); m.roughness = 0.25; c.castShadow = false; c.receiveShadow = false; c.renderOrder = 2; }); group.add(o);
  }
  // instanced vegetation, rocks and quay props
  const M4 = new T.Object3D().matrix.constructor, tmp = new T.Object3D(), instanced = {};
  const protoMesh = (name) => { let mesh = null; const n = nodes['PROTO_' + name]; if (n) n.traverse((c) => { if (c.isMesh && !mesh) mesh = c; }); return mesh; };
  function addInstances(proto, list, { cast = true, yOff = 0, scaleMul = 1, shadowRecv = true } = {}) {
    const src = protoMesh(proto); if (!src || !list.length) return;
    const im = new T.InstancedMesh(src.geometry, src.material, list.length);
    list.forEach(([x, n, z, yaw, s], i) => { tmp.position.set(x, z + yOff, -n); tmp.rotation.set(0, yaw, 0); tmp.scale.setScalar(s * scaleMul); tmp.updateMatrix(); im.setMatrixAt(i, tmp.matrix); });
    im.name = 'I_' + proto; im.castShadow = cast; im.receiveShadow = shadowRecv; im.frustumCulled = true; im.computeBoundingSphere && im.computeBoundingSphere(); group.add(im); instanced[proto] = im;
  }
  const V = inst.vegetation;
  if (!floraOn) { addInstances('tree_round', V.tree_round); addInstances('tree_tall', V.tree_tall); addInstances('palm', V.palm); addInstances('shrub', V.shrub, { cast: false }); addInstances('tea', V.tea, { cast: false });
  ['rock_a', 'rock_b', 'rock_c'].forEach((r, k) => addInstances(r, V.rock.filter((_, i) => i % 3 === k).map(([x, n, z, yaw, s]) => [x, n, z - 0.12 * s, yaw, s * 0.9]), { cast: false })); }
  const byProto = {}; for (const p of inst.quay_props) (byProto[p.proto] ||= []).push([p.x, p.n, p.z, p.yaw, p.s]); for (const [k, l] of Object.entries(byProto)) addInstances(k, l, { cast: true });
  // low cloud deck below the island: Gobkit Cloud 001-003 (CC0, 48 triangles each, flat shaded) when present, else the batch 1 procedural puffs
  { const rng = (() => { let q = 7; return () => (q = (q * 16807) % 2147483647) / 2147483647; })(), geos = [];
    for (const k of ['Cloud001', 'Cloud002', 'Cloud003']) { try { const g = await loader.loadAsync('assets-p3b2/env/' + k + '.glb'); let m = null; g.scene.traverse((o) => { if (o.isMesh && !m) m = o; }); if (m) { m.updateMatrixWorld(true); const geo = m.geometry.clone(); geo.applyMatrix4(m.matrixWorld); geo.computeBoundingBox(); const bb = geo.boundingBox, w = bb.max.x - bb.min.x; geo.translate(-(bb.min.x + bb.max.x) / 2, -(bb.min.y + bb.max.y) / 2, -(bb.min.z + bb.max.z) / 2); geo.scale(1 / w, 1 / w, 1 / w); geos.push(geo); } } catch (e) { /* fall back below */ } }
    if (geos.length) { const mat = new T.MeshStandardMaterial({ color: 0xffffff, roughness: 1, metalness: 0, emissive: 0xfff4e6, emissiveIntensity: 0.9, flatShading: true }); const per = [[], [], []];
      for (let i = 0; i < 60; i++) { const a = rng() * Math.PI * 2, r = 170 + rng() * 560; per[i % geos.length].push([Math.cos(a) * r + 20, Math.sin(a) * r + 40, -90 - rng() * 150, rng() * 6.28, 38 + rng() * 70]); }
      per.forEach((list, k) => { if (!geos[k] || !list.length) return; const im = new T.InstancedMesh(geos[k], mat, list.length); list.forEach(([x, n, z, yaw, w], i) => { tmp.position.set(x, z, -n); tmp.rotation.set(0, yaw, 0); tmp.scale.set(w, w * (0.8 + rng() * 0.5), w * 0.8); tmp.updateMatrix(); im.setMatrixAt(i, tmp.matrix); }); im.name = 'CLOUDS_' + k; im.frustumCulled = false; group.add(im); instanced['cloud' + k] = im; }); }
    else { const src = protoMesh('cloud'); if (src) { const list = []; for (let i = 0; i < 46; i++) { const a = rng() * Math.PI * 2, r = 190 + rng() * 520; list.push([Math.cos(a) * r + 20, Math.sin(a) * r + 40, -95 - rng() * 130, rng() * 6, 0.7 + rng() * 1.6]); }
      const mat = new T.MeshStandardMaterial({ color: 0xffffff, roughness: 1, metalness: 0, transparent: true, opacity: 0.93, depthWrite: false }); const im = new T.InstancedMesh(src.geometry, mat, list.length); list.forEach(([x, n, z, yaw, s], i) => { tmp.position.set(x, z, -n); tmp.rotation.set(0, yaw, 0); tmp.scale.set(s * 1.5, s * 1.0, s * 1.2); tmp.updateMatrix(); im.setMatrixAt(i, tmp.matrix); }); im.name = 'CLOUDS'; im.frustumCulled = false; group.add(im); instanced.cloud = im; } } }

  const flora = floraOn ? await loadFlora(T, { group, params, say }) : null; if (flora) obstacles.push(...flora.obstacles);

  // ---------------------------------------------------------------------------------------------- Cloudfall presentation (batch 2): layered mist, foam at the lip, spray at the cliff base. Procedural, unlit, no textures files.
  const fx = (() => {
    const sprites = [], foam = []; const wf = nodes.WATER_FALL; if (!wf) return { update() {}, sprites, foam };
    let mnY = 1e9, mxY = -1e9, cx = 0, cz = 0, cnt = 0, xs = [0, 0]; wf.updateMatrixWorld(true);
    wf.traverse((o) => { if (!o.isMesh) return; const p = o.geometry.attributes.position; for (let i = 0; i < p.count; i++) { const y = p.getY(i); mnY = Math.min(mnY, y); mxY = Math.max(mxY, y); cx += p.getX(i); cz += p.getZ(i); cnt++; } });
    cx /= cnt; cz /= cnt; const ctx = document.createElement('canvas'); ctx.width = ctx.height = 64; const g = ctx.getContext('2d'), gr = g.createRadialGradient(32, 32, 2, 32, 32, 31); gr.addColorStop(0, 'rgba(255,255,255,0.9)'); gr.addColorStop(0.5, 'rgba(255,255,255,0.35)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, 64, 64);
    const tex = new T.CanvasTexture(ctx); tex.colorSpace = T.SRGBColorSpace; const mat = new T.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false, opacity: 0.55, fog: false });
    const geo = new T.PlaneGeometry(1, 1); let seed = 5; const rn = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
    for (let i = 0; i < 46; i++) { const u = rn(), m = new T.Mesh(geo, mat); const y = mxY - (mxY - mnY) * (i < 30 ? u : 0.88 + 0.12 * rn()); const s = i < 30 ? 2.2 + 3.2 * (1 - u) : 6 + 7 * rn(); m.scale.set(s, s, 1); m.userData = { y0: y, x0: cx + (rn() - 0.5) * 3, z0: cz + (rn() - 0.5) * 3, ph: rn() * 6.28, sp: 0.2 + 0.4 * rn(), s }; m.renderOrder = 3; m.frustumCulled = false; group.add(m); sprites.push(m); }
    // foam at the lip: short white streaks lying on the water surface
    const fm = new T.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.6, depthWrite: false }); const fg = new T.PlaneGeometry(1, 1);
    for (let i = 0; i < 9; i++) { const m = new T.Mesh(fg, fm); m.rotation.x = -Math.PI / 2; m.scale.set(0.9 + rn(), 0.18 + 0.15 * rn(), 1); m.position.set(cx + (rn() - 0.5) * 3.2 - 1.2, mxY + 0.14, cz + (rn() - 0.5) * 2.0); m.userData = { ph: rn() * 6.28, x0: m.position.x }; m.renderOrder = 3; group.add(m); foam.push(m); }
    return { sprites, foam, update(t, camera) { for (const m of sprites) { const d = m.userData; m.position.set(d.x0 + Math.sin(t * d.sp + d.ph) * 0.8, d.y0 + Math.sin(t * d.sp * 1.7 + d.ph) * 0.6, d.z0 + Math.cos(t * d.sp + d.ph) * 0.8); m.quaternion.copy(camera.quaternion); }
      for (const m of foam) { m.position.x = m.userData.x0 + Math.sin(t * 1.2 + m.userData.ph) * 0.35; m.material.opacity = 0.45 + 0.2 * Math.sin(t * 3 + m.userData.ph); } } };
  })();
  const bounds = meta.derived_bounds.controller_bounds_m;
  const api = { meta, inst, H, MK, terrainAt, heightAt, maskAt, walkable, comfortable, collision: { blocked, slide }, obstacles, group, nodes, instanced, bounds, loadMs, NOSUP,
    flora, isSafe: (x, z) => comfortable(x, z), minY: -30, maxY: 80, tick(t, camera) { time.value = t; if (camera) { if (flora) flora.update(camera.position, t); fx.update(t, camera); } },
    stats() { let tris = 0, inst_tris = 0; group.traverse((o) => { if (!o.isMesh) return; const g = o.geometry, tcount = (g.index ? g.index.count : g.attributes.position.count) / 3; if (o.isInstancedMesh) inst_tris += tcount * o.count; else tris += tcount; }); return { static_triangles: tris, instanced_triangles_submitted: inst_tris, instanced_meshes: Object.keys(instanced).length }; } };
  api.landing = createLandingScan(api);
  return api;
}
