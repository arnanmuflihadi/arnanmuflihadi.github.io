// Merchant Citadel P3-B batch 1: the floating island in the isolated preview (no production module is touched).
//   - walkable support: island-terrain.bin (int16 cm, 0.5 m grid, bilinear) combined with the town's own 0.2 m grid (max where the town authored a surface)
//   - collision: terrain-aware blocked/slide (rim margin and steepness from island-mask.bin) plus the town's solid proxies; replaces the game's blocked(), whose hard +-105 m limit
//     cannot hold an island that reaches 136 m (the game module itself is NOT edited: the preview passes its own collision object, as the controller allows)
//   - visuals: the exported GLB (terrain top, cliffs, underside, Tea Stack, bridge, water) + instanced vegetation, rocks and quay props
import { createLandingScan } from './island-landing.js';
import { loadFlora } from './flora.js';

export async function loadIsland(T, { townHeightAt, params, scene, say = () => {} }) {
  const get = (u, kind = 'json') => fetch(u).then((r) => { if (!r.ok) throw new Error(u + ' ' + r.status); return r[kind](); });
  const [meta, tBuf, mBuf, inst, gmMeta, gmR, gmG] = await Promise.all([get('data/island-terrain.json'), get('data/island-terrain.bin', 'arrayBuffer'), get('data/island-mask.bin', 'arrayBuffer'), get('data/island-instances.json'), get('data/groundmap.json'), get('data/groundmap-r.bin', 'arrayBuffer'), get('data/groundmap-g.bin', 'arrayBuffer')]);
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
  // P3-B batch 3 ground map (0.3 m cells, two RedFormat textures, 1.15 MB): R = signed distance to the nearest path edge, G = tea planting-row soil weight; the shader draws crisp paths and soil strips from it
  const gmTex = (buf) => { const t = new T.DataTexture(new Uint8Array(buf), gmMeta.nx, gmMeta.nn, T.RedFormat); t.minFilter = T.LinearFilter; t.magFilter = T.LinearFilter; t.generateMipmaps = false; t.needsUpdate = true; return t; };
  const GM = { r: { value: gmTex(gmR) }, g: { value: gmTex(gmG) }, spec: { value: { x: gmMeta.x0, y: gmMeta.n0, z: gmMeta.cell, w: 0 } }, size: { value: { x: gmMeta.nx, y: gmMeta.nn } }, on: { value: params.get('gmap') === '0' ? 0 : 1 } };
  const NOISE = `float h21(vec2 p){ p=fract(p*vec2(123.34,456.21)); p+=dot(p,p+45.32); return fract(p.x*p.y); }
float vn(vec2 p){ vec2 i=floor(p), f=fract(p); f=f*f*(3.-2.*f); return mix(mix(h21(i),h21(i+vec2(1.,0.)),f.x),mix(h21(i+vec2(0.,1.)),h21(i+vec2(1.,1.)),f.x),f.y); }
float fbm3(vec3 p){ return vn(p.xy*1.0+p.z*0.37)*0.5 + vn(p.zy*2.3+p.x*0.21)*0.3 + vn(p.xz*5.1+p.y*0.5)*0.2; }`;
  const detail = (shader) => {                                          // procedural albedo detail and micro-relief for terrain materials: no texture memory
    shader.uniforms.uTime = time; shader.uniforms.uGmR = GM.r; shader.uniforms.uGmG = GM.g; shader.uniforms.uGm = GM.spec; shader.uniforms.uGmSize = GM.size; shader.uniforms.uGmOn = GM.on;
    shader.vertexShader = shader.vertexShader.replace('#include <common>', 'attribute float matId;\nvarying float vMat;\nvarying vec3 vWP;\n#include <common>').replace('#include <begin_vertex>', '#include <begin_vertex>\nvMat = matId; vWP = (modelMatrix * vec4(position, 1.0)).xyz;');
    shader.fragmentShader = shader.fragmentShader.replace('#include <common>', 'varying float vMat;\nvarying vec3 vWP;\nuniform sampler2D uGmR;\nuniform sampler2D uGmG;\nuniform vec4 uGm;\nuniform vec2 uGmSize;\nuniform float uGmOn;\n' + NOISE + '\n#include <common>')
      .replace('#include <color_fragment>', `#include <color_fragment>
{ float cls = floor(vMat + 0.5); vec3 wp = vWP;
  if (cls < 0.5) { float n = vn(wp.xz*0.9)*0.5 + vn(wp.xz*3.7)*0.3 + vn(wp.xz*13.0)*0.2; diffuseColor.rgb *= 0.80 + 0.40*n; }
  else if (cls < 1.5) { float n = vn(wp.xz*6.0)*0.6 + vn(wp.xz*22.0)*0.4; diffuseColor.rgb *= 0.84 + 0.30*n; }
  else if (cls < 2.5) { vec2 q = wp.xz / vec2(1.3, 0.65); float row = floor(q.y); q.x += 0.5*mod(row, 2.0); vec2 c = fract(q), id = floor(q);
    float edge = min(min(c.x, 1.0-c.x)*1.3, min(c.y, 1.0-c.y)*0.65); float joint = smoothstep(0.0, 0.03, edge); float tint = 0.84 + 0.26*h21(id);
    diffuseColor.rgb *= tint * (0.50 + 0.50*joint) * (0.92 + 0.16*vn(wp.xz*6.0)); }
  else if (cls < 3.5) { float n = fbm3(wp*0.55); float m = vn(vec2(wp.y*2.3 + n*3.0, 0.5)); diffuseColor.rgb *= 0.78 + 0.34*n + 0.12*(m-0.5); }
  else { float rows = 0.5 + 0.5*sin(wp.x*1.9 + wp.z*0.7); diffuseColor.rgb *= 0.88 + 0.16*vn(wp.xz*4.0) - 0.05*rows; }
  if (uGmOn > 0.5 && (cls < 1.5 || cls > 3.5)) {                       // ground map: crisp earth paths (signed distance) and tea soil strips
    vec2 guv = vec2(((wp.x - uGm.x)/uGm.z + 0.5)/uGmSize.x, ((-wp.z - uGm.y)/uGm.z + 0.5)/uGmSize.y);
    float pd = texture2D(uGmR, guv).r*3.0 - 1.0; float sw = texture2D(uGmG, guv).r;
    float nE = vn(wp.xz*6.0)*0.6 + vn(wp.xz*22.0)*0.4; float nB = vn(wp.xz*2.1);
    vec3 earth = pow(vec3(0.66,0.55,0.38), vec3(2.2)) * (0.80 + 0.34*nE) * (1.0 - 0.10*smoothstep(-0.6, -1.0, pd));   // packed earth, a little darker in the centre line
    float edge = pd + (nB - 0.5)*0.10;                                                              // edge wobble of a few cm so the border is crisp but not ruler-straight
    float pm = 1.0 - smoothstep(0.03, 0.10, edge);
    float rim = smoothstep(0.50, 0.14, pd) * smoothstep(0.02, 0.14, pd) * (0.4 + 0.6*vn(wp.xz*9.0));  // trodden fringe just outside the edge: drier grass
    diffuseColor.rgb = mix(diffuseColor.rgb, diffuseColor.rgb*0.78 + vec3(0.08,0.07,0.02), 0.65*rim);
    diffuseColor.rgb = mix(diffuseColor.rgb, earth, pm);
    float soil = smoothstep(0.30, 0.62, sw) * (1.0 - pm);
    diffuseColor.rgb = mix(diffuseColor.rgb, pow(vec3(0.45,0.28,0.18), vec3(2.2)) * (0.80 + 0.30*nE) * 0.9, 0.78*soil); } }`)
      .replace('#include <normal_fragment_maps>', `#include <normal_fragment_maps>
{ float cls2 = floor(vMat + 0.5); float amt = cls2 > 2.5 && cls2 < 3.5 ? 0.35 : (cls2 > 1.5 && cls2 < 2.5 ? 0.05 : 0.10);
  vec3 p = vWP * 1.7; float e = 0.07; float c0 = fbm3(p);
  vec3 g = vec3(fbm3(p + vec3(e,0.,0.)) - c0, fbm3(p + vec3(0.,e,0.)) - c0, fbm3(p + vec3(0.,0.,e)) - c0) / e;
  vec3 gv = (viewMatrix * vec4(g, 0.0)).xyz; normal = normalize(normal - amt * (gv - dot(gv, normal) * normal)); }`);
  };
  // P3-B batch 3 (crag pass): rock faces of the terrain mesh get crisp strata in the shader (world-height bedding with noise warp, dark bedding lines, vertical joints) instead of the vertex-colour smears
  const detailTop = (shader) => {
    detail(shader); shader.uniforms.uStrata = { value: params.get('strata') === '0' ? 0 : 1 };
    shader.fragmentShader = shader.fragmentShader.replace('varying float vMat;', 'varying float vMat;\nuniform float uStrata;').replace('else if (cls < 3.5) { float n = fbm3(wp*0.55);', `else if (cls < 3.5 && uStrata > 0.5) {
    float wr = vn(wp.xz*0.30)*2.4 + vn(wp.xz*1.2)*0.7; float u = (wp.y + wr) * 0.66; float k = floor(u), f = u - k;
    vec3 pA = pow(vec3(0.66,0.56,0.40), vec3(2.2)), pB = pow(vec3(0.52,0.34,0.23), vec3(2.2)), pC = pow(vec3(0.44,0.39,0.33), vec3(2.2)), pD = pow(vec3(0.72,0.64,0.47), vec3(2.2));
    float s0 = mod(k, 4.0), s1 = mod(k + 1.0, 4.0); vec3 c0 = s0 < 0.5 ? pA : s0 < 1.5 ? pB : s0 < 2.5 ? pD : pC; vec3 c1 = s1 < 0.5 ? pA : s1 < 1.5 ? pB : s1 < 2.5 ? pD : pC;
    vec3 rock = mix(c0, c1, smoothstep(0.88, 1.0, f)); rock = mix(rock, pA, 0.28); rock *= 1.0 - 0.28*smoothstep(0.0, 0.05, f)*(1.0 - smoothstep(0.05, 0.14, f));
    float jt = vn(vec2(wp.x*1.7 + wp.z*1.3, wp.y*0.22)); rock *= 1.0 - 0.30*smoothstep(0.52, 0.56, jt)*(1.0 - smoothstep(0.56, 0.62, jt));
    float gr = vn(wp.xz*5.0 + wp.y*0.7)*0.6 + vn(wp.xz*18.0)*0.4; diffuseColor.rgb = rock * (0.82 + 0.36*gr); }
  else if (cls < 3.5) { float n = fbm3(wp*0.55);`);
  };
  const waterShader = (fall, sp = 1, ph = 0, bright = 0) => (shader) => {
    shader.uniforms.uTime = time;
    shader.vertexShader = shader.vertexShader.replace('#include <common>', 'varying vec2 vWUv;\n#include <common>').replace('#include <begin_vertex>', '#include <begin_vertex>\nvWUv = uv;');
    shader.fragmentShader = shader.fragmentShader.replace('#include <common>', 'varying vec2 vWUv;\nuniform float uTime;\n#include <common>')
      .replace('#include <color_fragment>', `#include <color_fragment>
{ float s = ${fall ? `vWUv.y*2.0 + uTime*2.4*${sp.toFixed(3)} + ${ph.toFixed(3)}` : 'vWUv.y*3.0 - uTime*0.9'}; float st = 0.5 + 0.5*sin(s*6.2831 + sin(vWUv.x*9.0)*1.7); st = st*st; float edge = smoothstep(0.0, 0.2, vWUv.x) * smoothstep(1.0, 0.8, vWUv.x);
  diffuseColor.rgb = mix(diffuseColor.rgb, vec3(0.93,0.97,1.0), ${fall ? `0.55 + 0.4*st + ${bright.toFixed(2)}*(1.0-edge)` : '0.22*st + 0.15*(1.0-edge)'}); diffuseColor.a *= ${fall ? '0.88' : '0.9'} * (0.6 + 0.4*edge); }`);
  };
  const statics = ['ISL_TOP', 'ISL_CLIFF', 'ISL_HEROES', 'ISL_CRAG', 'STACK_TOP', 'STACK_CLIFF', 'ISL_ROOTS', 'ISL_DEBRIS', 'BRIDGE'];
  const matsDone = new Set();
  const tune = (o) => {
    if (!o.isMesh) return; const g = o.geometry; if (g.attributes._matid && !g.attributes.matId) g.setAttribute('matId', g.attributes._matid);
    if (!g.attributes.matId) g.setAttribute('matId', new T.Float32BufferAttribute(new Float32Array(g.attributes.position.count).fill(3), 1));
    for (const m of [].concat(o.material)) if (!matsDone.has(m) && (m.name === 'MI_P3B_Top' || m.name === 'MI_P3B_Rock')) { matsDone.add(m); m.userData.extraCompile = m.name === 'MI_P3B_Top' ? detailTop : detail; }
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
  if (params.get('cloud') === 'cards') { const rng = (() => { let q = 7; return () => (q = (q * 16807) % 2147483647) / 2147483647; })(), geos = [];
    for (const k of ['Cloud001', 'Cloud002', 'Cloud003']) { try { const g = await loader.loadAsync('assets-p3b2/env/' + k + '.glb'); let m = null; g.scene.traverse((o) => { if (o.isMesh && !m) m = o; }); if (m) { m.updateMatrixWorld(true); const geo = m.geometry.clone(); geo.applyMatrix4(m.matrixWorld); geo.computeBoundingBox(); const bb = geo.boundingBox, w = bb.max.x - bb.min.x; geo.translate(-(bb.min.x + bb.max.x) / 2, -(bb.min.y + bb.max.y) / 2, -(bb.min.z + bb.max.z) / 2); geo.scale(1 / w, 1 / w, 1 / w); geos.push(geo); } } catch (e) { /* fall back below */ } }
    if (geos.length) { const mat = new T.MeshStandardMaterial({ color: 0xffffff, roughness: 1, metalness: 0, emissive: 0xfff4e6, emissiveIntensity: 0.9, flatShading: true }); const per = [[], [], []];
      for (let i = 0; i < 60; i++) { const a = rng() * Math.PI * 2, r = 170 + rng() * 560; per[i % geos.length].push([Math.cos(a) * r + 20, Math.sin(a) * r + 40, -90 - rng() * 150, rng() * 6.28, 38 + rng() * 70]); }
      per.forEach((list, k) => { if (!geos[k] || !list.length) return; const im = new T.InstancedMesh(geos[k], mat, list.length); list.forEach(([x, n, z, yaw, w], i) => { tmp.position.set(x, z, -n); tmp.rotation.set(0, yaw, 0); tmp.scale.set(w, w * (0.8 + rng() * 0.5), w * 0.8); tmp.updateMatrix(); im.setMatrixAt(i, tmp.matrix); }); im.name = 'CLOUDS_' + k; im.frustumCulled = false; group.add(im); instanced['cloud' + k] = im; }); }
    else { const src = protoMesh('cloud'); if (src) { const list = []; for (let i = 0; i < 46; i++) { const a = rng() * Math.PI * 2, r = 190 + rng() * 520; list.push([Math.cos(a) * r + 20, Math.sin(a) * r + 40, -95 - rng() * 130, rng() * 6, 0.7 + rng() * 1.6]); }
      const mat = new T.MeshStandardMaterial({ color: 0xffffff, roughness: 1, metalness: 0, transparent: true, opacity: 0.93, depthWrite: false }); const im = new T.InstancedMesh(src.geometry, mat, list.length); list.forEach(([x, n, z, yaw, s], i) => { tmp.position.set(x, z, -n); tmp.rotation.set(0, yaw, 0); tmp.scale.set(s * 1.5, s * 1.0, s * 1.2); tmp.updateMatrix(); im.setMatrixAt(i, tmp.matrix); }); im.name = 'CLOUDS'; im.frustumCulled = false; group.add(im); instanced.cloud = im; } } }

  // P3-B batch 3 WP4: soft cumulus puffs (one 256x128 canvas texture, one instanced draw, yaw-billboarded) replace the faceted Gobkit cloud cards; `?cloud=cards` brings the old ones back
  const softClouds = (() => { if (params.get('cloud') === 'cards') return null; const cv = document.createElement('canvas'); cv.width = 256; cv.height = 128; const g = cv.getContext('2d'); g.filter = 'blur(5px)';
    const gr = g.createLinearGradient(0, 20, 0, 118); gr.addColorStop(0, '#ffffff'); gr.addColorStop(0.55, '#f3f7fb'); gr.addColorStop(1, '#c9d6e6'); g.fillStyle = gr;
    for (const [x, y, r] of [[60, 84, 30], [96, 66, 38], [136, 58, 42], [176, 70, 36], [206, 86, 26], [128, 88, 40], [84, 92, 28], [170, 94, 30]]) { g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fill(); }
    const tex = new T.CanvasTexture(cv); tex.colorSpace = T.SRGBColorSpace; const mat = new T.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false, opacity: 0.96, fog: false });
    const rng = (() => { let q = 11; return () => (q = (q * 16807) % 2147483647) / 2147483647; })(), list = []; for (let i = 0; i < 80; i++) { const a = rng() * Math.PI * 2, r = 170 + rng() * 560, w = 70 + rng() * 150; list.push({ x: Math.cos(a) * r + 20, n: Math.sin(a) * r + 40, z: -90 - rng() * 150, w, h: w * (0.42 + 0.12 * rng()), flip: rng() < 0.5 ? -1 : 1 }); }
    const im = new T.InstancedMesh(new T.PlaneGeometry(1, 1), mat, list.length); im.name = 'CLOUDS_SOFT'; im.frustumCulled = false; im.renderOrder = 0; group.add(im);
    return { im, list, update(camera) { for (let i = 0; i < list.length; i++) { const c = list[i]; tmp.position.set(c.x, c.z, -c.n); tmp.rotation.set(0, Math.atan2(camera.position.x - c.x, camera.position.z + c.n), 0); tmp.scale.set(c.w * c.flip, c.h, 1); tmp.updateMatrix(); im.setMatrixAt(i, tmp.matrix); } im.instanceMatrix.needsUpdate = true; } }; })();
  const flora = floraOn ? await loadFlora(T, { group, params, time, say }) : null; if (flora) obstacles.push(...flora.obstacles);

  // ---------------------------------------------------------------------------------------------- Cloudfall presentation (batch 2): layered mist, foam at the lip, spray at the cliff base. Procedural, unlit, no textures files.
  const fx = (() => {
    const sprites = [], foam = []; const wf = nodes.WATER_FALL; if (!wf) return { update() {}, sprites, foam };
    let mnY = 1e9, mxY = -1e9, cx = 0, cz = 0, cnt = 0, xs = [0, 0]; wf.updateMatrixWorld(true);
    wf.traverse((o) => { if (!o.isMesh) return; const p = o.geometry.attributes.position; for (let i = 0; i < p.count; i++) { const y = p.getY(i); mnY = Math.min(mnY, y); mxY = Math.max(mxY, y); cx += p.getX(i); cz += p.getZ(i); cnt++; } });
    cx /= cnt; cz /= cnt;
    // P3-B batch 3 WP4: three layered falling sheets (main, a narrow fast front sheet, two thin side strands) built from the main ribbon's own vertices, plus falling spray quads
    let fallGeo = null; wf.traverse((o) => { if (o.isMesh && !fallGeo) fallGeo = o; });
    const layers = []; const layered = params.get('fall') !== 'plain';
    if (layered && fallGeo) {
      const P = fallGeo.geometry.attributes.position, UV = fallGeo.geometry.attributes.uv, rows = P.count / 2, L = [], Rr = []; for (let k = 0; k < rows; k++) { L.push([P.getX(k), P.getY(k), P.getZ(k)]); Rr.push([P.getX(rows + k), P.getY(rows + k), P.getZ(rows + k)]); }
      const sheet = (wScale, wShift, outX, sp, ph, bright, op) => { const pos = new Float32Array(rows * 2 * 3), uv = new Float32Array(rows * 2 * 2);
        for (let k = 0; k < rows; k++) { const c = [0, 1, 2].map((i) => (L[k][i] + Rr[k][i]) / 2), h = [0, 1, 2].map((i) => (L[k][i] - Rr[k][i]) / 2); const sway = 0.12 * Math.sin(k * 1.7 + ph * 3);
          for (let i = 0; i < 3; i++) { pos[k * 3 + i] = c[i] + h[i] * (wShift + wScale) + (i === 0 ? outX + sway : 0); pos[(rows + k) * 3 + i] = c[i] + h[i] * (wShift - wScale) + (i === 0 ? outX + sway : 0); }
          uv[k * 2] = 0; uv[k * 2 + 1] = UV.getY(k); uv[(rows + k) * 2] = 1; uv[(rows + k) * 2 + 1] = UV.getY(k); }
        const g = new T.BufferGeometry(); g.setAttribute('position', new T.Float32BufferAttribute(pos, 3)); g.setAttribute('uv', new T.Float32BufferAttribute(uv, 2)); g.setIndex(Array.from(fallGeo.geometry.index.array)); g.computeVertexNormals();
        const m = fallGeo.material.clone(); m.userData.extraCompile = waterShader(true, sp, ph, bright); m.opacity = op; const mesh = new T.Mesh(g, m); mesh.renderOrder = 2; mesh.frustumCulled = false; group.add(mesh); layers.push(mesh); return mesh; };
      sheet(0.78, 0, 0.34, 1.45, 0.37, 0.16, 0.92); sheet(0.2, 1.0, 0.2, 0.8, 1.9, 0.05, 0.85); sheet(0.2, -1.0, 0.2, 1.1, 3.1, 0.05, 0.85); sheet(0.35, 0.2, 0.55, 1.9, 4.4, 0.2, 0.7);
    }
    const spray = []; if (layered && fallGeo) { const sg = new T.PlaneGeometry(1, 1); const sc = document.createElement('canvas'); sc.width = sc.height = 32; const sx = sc.getContext('2d'), sgr = sx.createRadialGradient(16, 16, 1, 16, 16, 15); sgr.addColorStop(0, 'rgba(255,255,255,0.95)'); sgr.addColorStop(1, 'rgba(255,255,255,0)'); sx.fillStyle = sgr; sx.fillRect(0, 0, 32, 32);
      const st = new T.CanvasTexture(sc); st.colorSpace = T.SRGBColorSpace; const sm = new T.MeshBasicMaterial({ map: st, transparent: true, depthWrite: false, opacity: 0.8, fog: false }); const P = fallGeo.geometry.attributes.position, rows = P.count / 2;
      const prof = []; for (let k = 0; k < rows; k++) prof.push([(P.getX(k) + P.getX(rows + k)) / 2, (P.getY(k) + P.getY(rows + k)) / 2, (P.getZ(k) + P.getZ(rows + k)) / 2, Math.abs(P.getZ(k) - P.getZ(rows + k)) / 2]);
      let sd = 17; const r2 = () => (sd = (sd * 16807) % 2147483647) / 2147483647;
      const im = new T.InstancedMesh(sg, sm, 150); im.renderOrder = 3; im.frustumCulled = false; im.name = 'FALL_SPRAY'; group.add(im);
      for (let i = 0; i < 150; i++) spray.push({ t0: r2(), sp: 0.16 + 0.22 * r2(), lat: (r2() - 0.5) * 2.0, out: 0.2 + 1.1 * r2(), sz: 0.3 + 0.55 * r2(), prof }); spray.im = im; }
    const ctx = document.createElement('canvas'); ctx.width = ctx.height = 64; const g = ctx.getContext('2d'), gr = g.createRadialGradient(32, 32, 2, 32, 32, 31); gr.addColorStop(0, 'rgba(255,255,255,0.9)'); gr.addColorStop(0.5, 'rgba(255,255,255,0.35)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, 64, 64);
    const tex = new T.CanvasTexture(ctx); tex.colorSpace = T.SRGBColorSpace; const mat = new T.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false, opacity: 0.55, fog: false });
    const geo = new T.PlaneGeometry(1, 1); let seed = 5; const rn = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
    for (let i = 0; i < 46; i++) { const u = rn(), m = new T.Mesh(geo, mat); const y = mxY - (mxY - mnY) * (i < 30 ? u : 0.88 + 0.12 * rn()); const s = i < 30 ? 2.2 + 3.2 * (1 - u) : 6 + 7 * rn(); m.scale.set(s, s, 1); m.userData = { y0: y, x0: cx + (rn() - 0.5) * 3, z0: cz + (rn() - 0.5) * 3, ph: rn() * 6.28, sp: 0.2 + 0.4 * rn(), s }; m.renderOrder = 3; m.frustumCulled = false; group.add(m); sprites.push(m); }
    // foam at the lip: short white streaks lying on the water surface
    const fm = new T.MeshBasicMaterial({ map: tex, transparent: true, opacity: 0.55, depthWrite: false });   // soft blobs instead of hard planks
    const fg = new T.PlaneGeometry(1, 1);
    for (let i = 0; i < 16; i++) { const m = new T.Mesh(fg, fm); m.rotation.x = -Math.PI / 2; m.scale.set(1.3 + 1.4 * rn(), 0.5 + 0.4 * rn(), 1); m.position.set(cx + (rn() - 0.5) * 3.2 - 1.2, mxY + 0.14, cz + (rn() - 0.5) * 2.0); m.userData = { ph: rn() * 6.28, x0: m.position.x }; m.renderOrder = 3; group.add(m); foam.push(m); }
    return { sprites, foam, layers, spray, update(t, camera) {
      if (spray.im) { for (let i = 0; i < spray.length; i++) { const d = spray[i], pr = d.prof, ph0 = (((t * d.sp + d.t0) % 1) + 1) % 1, ph = Number.isFinite(ph0) ? ph0 : d.t0, f = ph * (pr.length - 1), k = Math.min(pr.length - 2, Math.floor(f)), a = f - k; const gx = pr[k][0] + (pr[k + 1][0] - pr[k][0]) * a, gy = pr[k][1] + (pr[k + 1][1] - pr[k][1]) * a, gz = pr[k][2] + (pr[k + 1][2] - pr[k][2]) * a, hw = pr[k][3];
          tmp.position.set(gx + d.out * (0.4 + 2.2 * ph * ph), gy, gz + d.lat * hw * (1 + 0.7 * ph)); const sz = d.sz * (0.6 + 2.2 * ph) * Math.min(1, ph * 8) * (1 - 0.55 * ph); tmp.scale.set(sz, sz, 1); tmp.quaternion.copy(camera.quaternion); tmp.updateMatrix(); spray.im.setMatrixAt(i, tmp.matrix); } spray.im.instanceMatrix.needsUpdate = true; }
      for (const m of sprites) { const d = m.userData; m.position.set(d.x0 + Math.sin(t * d.sp + d.ph) * 0.8, d.y0 + Math.sin(t * d.sp * 1.7 + d.ph) * 0.6, d.z0 + Math.cos(t * d.sp + d.ph) * 0.8); m.quaternion.copy(camera.quaternion); }
      for (const m of foam) { m.position.x = m.userData.x0 + Math.sin(t * 1.2 + m.userData.ph) * 0.35; m.material.opacity = 0.45 + 0.2 * Math.sin(t * 3 + m.userData.ph); } } };
  })();
  const bounds = meta.derived_bounds.controller_bounds_m;
  const api = { meta, inst, H, MK, terrainAt, heightAt, maskAt, walkable, comfortable, collision: { blocked, slide }, obstacles, group, nodes, instanced, bounds, loadMs, NOSUP,
    flora, isSafe: (x, z) => comfortable(x, z), minY: -30, maxY: 80, tick(t, camera) { time.value = t; if (camera) { if (flora) flora.update(camera.position, t); fx.update(t, camera); if (softClouds) softClouds.update(camera); } },
    stats() { let tris = 0, inst_tris = 0; group.traverse((o) => { if (!o.isMesh) return; const g = o.geometry, tcount = (g.index ? g.index.count : g.attributes.position.count) / 3; if (o.isInstancedMesh) inst_tris += tcount * o.count; else tris += tcount; }); return { static_triangles: tris, instanced_triangles_submitted: inst_tris, instanced_meshes: Object.keys(instanced).length }; } };
  api.landing = createLandingScan(api);
  return api;
}
