// Merchant Citadel P3-B batch 2: third-party flora (Quaternius Stylized Nature MegaKit Standard, CC0) as distance-managed instanced sets.
// One InstancedMesh per (prototype primitive, LOD). Every ~0.4 s (or when the camera moved 3 m) the instances are re-bucketed by distance: L0 near, L1 (decimated trees) mid,
// nothing beyond the prototype's cull range. Small ground cover is only drawn near the camera; rocks are always drawn. Trees cast shadows at L0 only.
export async function loadFlora(T, { group, params, isl, say = () => {} }) {
  const get = (u) => fetch(u).then((r) => { if (!r.ok) throw new Error(u + ' ' + r.status); return r.json(); });
  const data = await get('data/island-flora.json');
  say('loading flora (GLB)…'); const t0 = performance.now();
  const gltf = await new T.GLTFLoader().loadAsync(params.get('floraglb') || 'assets-p3b2/flora.glb'); const loadMs = performance.now() - t0;
  const nodes = {}; gltf.scene.children.forEach((c) => { nodes[c.name] = c; });
  const prims = (name) => { const n = nodes['F_' + name]; const out = []; if (!n) return out; n.updateMatrixWorld(true); n.traverse((c) => { if (c.isMesh) out.push(c); }); return out; };
  const tmp = new T.Object3D(), mats = new Set();
  // cull ranges (m) per prototype family: [L0 range, L1 range (trees), draw cap]
  const RANGE = (name) => /^(CommonTree|Pine|TwistedTree|DeadTree)/.test(name) ? [36, 460] : /^(Bush|Fern|Plant|Mushroom)/.test(name) ? [60, 0] : /^Rock_Medium/.test(name) ? [1e9, 0] : /^(Flower_._Group)/.test(name) ? [24, 0] : /^(Flower|Clover|Grass|Pebble|RockPath)/.test(name) ? [32, 0] : [50, 0];
  // third-party leaf/rock textures are pastel and designed for a toon shader; this scene's lighting (env 2.0, sun 4.2) blows them out, so each family gets a documented albedo multiplier
  const TINT = [[/^Leaves_NormalTree/, [0.50, 0.56, 0.40]], [/^Leaves_TwistedTree/, [0.30, 0.47, 0.19]], [/^Leaves_Pine/, [0.85, 0.88, 0.80]], [/^Leaves(\.|$)/, [0.62, 0.70, 0.52]], [/^Flowers/, [0.82, 0.82, 0.82]], [/^Grass/, [0.62, 0.70, 0.50]], [/^Rocks/, [0.92, 0.80, 0.66]], [/^PathRocks/, [0.90, 0.80, 0.68]], [/^Bark/, [0.85, 0.80, 0.75]]];
  // foliage near the lens dithers away (camera standing in a grove must not be blinded by leaf cards): fully visible beyond 3.4 m, gone inside 1.0 m
  const nearFade = (shader) => { shader.fragmentShader = shader.fragmentShader.replace('#include <alphatest_fragment>', '{ float nd = length(vViewPosition); float nk = smoothstep(1.0, 3.4, nd); float nt = fract(52.9829189 * fract(dot(gl_FragCoord.xy, vec2(0.06711056, 0.00583715)))); if (nk < nt) discard; }\n#include <alphatest_fragment>'); };
  const sets = [];
  for (const [name, list] of Object.entries(data.instances)) {
    const p0 = prims(name + '_L0'), p1 = prims(name + '_L1'); if (!p0.length) { console.warn('flora prototype missing', name); continue; }
    const [r0, r1] = RANGE(name), isTree = /^(CommonTree|Pine|TwistedTree|DeadTree)/.test(name), pos = list;
    const make = (ps, tag) => ps.map((src) => { const im = new T.InstancedMesh(src.geometry, src.material, pos.length); im.name = 'FL_' + name + tag; im.count = 0; im.frustumCulled = false; im.castShadow = isTree && tag === '_L0'; im.receiveShadow = true;
      const m = src.material; if (!mats.has(m)) { mats.add(m); m.side = T.DoubleSide; if (m.alphaTest === 0 && m.map && /Leaves|Leaf|Flowers|Grass/.test(m.name)) m.alphaTest = 0.5; m.roughness = Math.max(m.roughness ?? 0.9, 0.85); m.metalness = 0; const t = TINT.find(([re]) => re.test(m.name)); if (t) m.color.setRGB(...t[1]); m.userData.extraCompile = nearFade; } group.add(im); return im; });
    sets.push({ name, pos, r0, r1, a0: make(p0, '_L0'), a1: p1.length ? make(p1, '_L1') : [], m: new T.Object3D().matrix.constructor });
  }
  // ledge rocks (cliff outcrops): always drawn, three variants
  const ledgeSets = [];
  { const ls = data.ledge_rocks || []; ['Rock_Medium_1', 'Rock_Medium_2', 'Rock_Medium_3'].forEach((nm, k) => { const list = ls.filter((_, i) => i % 4 === 0 && (i / 4 | 0) % 3 === k); const ps = prims(nm + '_L0'); if (!ps.length || !list.length) return;
      ps.forEach((src) => { const im = new T.InstancedMesh(src.geometry, src.material, list.length); list.forEach(([x, n, z, yaw, s], i) => { tmp.position.set(x, z, -n); tmp.rotation.set(0.25 * Math.sin(i), yaw, 0.2 * Math.cos(i)); tmp.scale.setScalar(s * 0.55); tmp.updateMatrix(); im.setMatrixAt(i, tmp.matrix); }); im.name = 'FL_ledge_' + nm; im.receiveShadow = true; im.frustumCulled = false; group.add(im); ledgeSets.push(im); }); }); }
  const stats = { drawn: 0, l0: 0, l1: 0, updates: 0, ms: 0 }; let last = -1e9, lx = 1e9, lz = 1e9;
  function update(cam, t) {
    const dx = cam.x - lx, dz = cam.z - lz; if (t - last < 0.4 && dx * dx + dz * dz < 9) return; last = t; lx = cam.x; lz = cam.z; const c0 = performance.now(); let n0 = 0, n1 = 0;
    for (const s of sets) {
      const r0s = s.r0 * s.r0, r1s = s.r1 * s.r1; let c = 0, d = 0;
      for (let i = 0; i < s.pos.length; i++) { const [x, n, z, yaw, sc] = s.pos[i], ex = x - cam.x, ez = -n - cam.z, d2 = ex * ex + ez * ez;
        if (d2 < r0s) { tmp.position.set(x, z, -n); tmp.rotation.set(0, yaw, 0); tmp.scale.setScalar(sc); tmp.updateMatrix(); for (const im of s.a0) im.setMatrixAt(c, tmp.matrix); c++; }
        else if (s.a1.length && d2 < r1s) { tmp.position.set(x, z, -n); tmp.rotation.set(0, yaw, 0); tmp.scale.setScalar(sc); tmp.updateMatrix(); for (const im of s.a1) im.setMatrixAt(d, tmp.matrix); d++; } }
      for (const im of s.a0) { im.count = c; im.instanceMatrix.needsUpdate = true; } for (const im of s.a1) { im.count = d; im.instanceMatrix.needsUpdate = true; } n0 += c; n1 += d;
    }
    stats.l0 = n0; stats.l1 = n1; stats.drawn = n0 + n1; stats.updates++; stats.ms += performance.now() - c0;
  }
  // collision proxies (trunks and big boulders replace the batch 1 procedural ones)
  const obstacles = []; for (const t of data.trunks) obstacles.push({ src: 'P3B2:trunk', group: 'post', x: t.x, z: -t.n, w: t.r * 2, d: t.r * 2, h: 3.4 });
  for (const r of data.rocks_solid) obstacles.push({ src: 'P3B2:rock', group: 'prop', x: r.x, z: -r.n, w: r.r * 1.5, d: r.r * 1.5, h: 1.3 });
  const tri = (ps) => ps.reduce((a, g) => a + (g.geometry.index ? g.geometry.index.count : g.geometry.attributes.position.count) / 3, 0);
  const info = () => { const o = {}; for (const s of sets) o[s.name] = { instances: s.pos.length, l0_tris_each: tri(prims(s.name + '_L0')), l1_tris_each: s.a1.length ? tri(prims(s.name + '_L1')) : 0 }; return o; };
  return { data, sets, ledgeSets, update, stats, obstacles, loadMs, info, nodes, perches: data.perches, habitats: data.habitats, keepouts: data.keepouts, materials: mats,
    triangles(cam) { let t = 0; for (const s of sets) { for (const im of s.a0) t += im.count * (im.geometry.index ? im.geometry.index.count : im.geometry.attributes.position.count) / 3; for (const im of s.a1) t += im.count * (im.geometry.index ? im.geometry.index.count : im.geometry.attributes.position.count) / 3; } for (const im of ledgeSets) t += im.count * (im.geometry.index ? im.geometry.index.count : im.geometry.attributes.position.count) / 3; return t; } };
}
