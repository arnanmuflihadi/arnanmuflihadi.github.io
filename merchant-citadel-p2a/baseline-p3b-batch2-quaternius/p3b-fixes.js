// Merchant Citadel P3-B batch 1: targeted town corrections identified in P3-A, applied preview-side behind flags (the kit GLB and scene.json are NOT edited).
// ?fixes=0 switches all of them off (P2-B batch 5 behaviour); individual flags: rail, porch, eaves, gap, signs.
// Each is data or a small load-time edit so that it can be reverted by flag and re-done properly in the Blender kit later.
export const FIX_DATA = {
  rail: { removeBays: [-2, 0, 2], cutBox: { x: [-3.05, 3.05], y: [1.8, 3.4], z: [-75.5, -74.9] }, alignProxies: { front: { x: [-4, 4], n: 75.2 }, sides: { x: [-5, 5], mesh_x: 6.0, n: 77.55, d: 2.7 } }, note: 'the three centre bays of the forecourt balustrade are cut out of the dressing geometry and their three proxies removed; the end bays and the side returns stay. MEASURED: the balustrade mesh stands at n 75.1-75.3 (front) and x +-6 (returns) while the batch 5 proxies stood at n 76.2 and x +-5: a 1.0 m visual/collision mismatch (CONFIRMED-TECH, pre-existing); the remaining proxies are moved onto the mesh' },
  gates: { list: [{ name: 'Tea Lookout east gate', removeProxy: { x: 42, n: 57 }, cutBox: { x: [41.7, 42.3], y: [-0.1, 1.45], z: [-58.05, -55.95] } }], note: 'the Tea Lookout terrace fence (x 42, n 54-60) has no opening: one 2 m bay (n 56-58) is cut out of the dressing and its proxy removed so the terrace connects to the Tea promenade' },
  porch: { note: 'the six camera-only roof bands of the porch of B01 (x 0, n 80.4, minY 4.22 .. 8.945) are camera-transparent: the camera no longer collapses against the porch roof; the body is unaffected' },
  eaves: { maxMinY: 3.2, note: 'camera-only roof bands that start below 3.2 m are camera-transparent (P3-A rule A). Walls, upper roof bands and every body proxy remain' },
  gap: { note: 'the enterable 2.7 m strip between B10 and B11 (n 14.3..17.0) is closed at both mouths with stacked crates and barrels (instanced custom props) and two solid proxies', props: [['crate', -17.9, 15.1, 0.2, 1], ['crate', -17.9, 16.2, -0.1, 1], ['barrel', -18.1, 15.65, 0, 1], ['crate', -24.1, 15.1, 0.1, 1], ['crate', -24.1, 16.2, 0.0, 1], ['crate', -24.1, 15.65, 0.0, 1.0, 0.8], ['barrel', -23.6, 15.65, 0, 1]], solids: [{ x: -17.95, n: 15.65, w: 1.1, d: 2.7, h: 1.7 }, { x: -24.1, n: 15.65, w: 1.1, d: 2.7, h: 1.7 }] },
  signs: { note: 'B15 (assay office) and B16 (cartographer): a second, projecting sign on the side of the tower facing the terrace and the street, and three banners each (burgundy for the assay office, blue for the cartographer)',
    add: [['B15_sign1', 'SIGN_CUS-Sign_Coin_burgundy_x1p4', -14.35, 3.5, -64.6, 90, 1.5], ['B15_banner1', 'SIGN_FP-Banner_1_at_burgundy', -14.35, 1.4, -66.2, 90, 1.0], ['B15_banner2', 'SIGN_FP-Banner_1_at_burgundy', -17.2, 1.7, -62.95, 0, 1.0], ['B15_banner3', 'SIGN_FP-Banner_1_at_burgundy', -20.6, 1.7, -62.95, 0, 1.0],
      ['B16_sign1', 'SIGN_CUS-Sign_Compass_wood_x1p4', 14.35, 3.5, -64.6, -90, 1.5], ['B16_banner1', 'SIGN_FP-Banner_1_at_blue', 14.35, 1.4, -66.2, -90, 1.0], ['B16_banner2', 'SIGN_FP-Banner_1_at_blue', 17.2, 1.7, -62.95, 0, 1.0], ['B16_banner3', 'SIGN_FP-Banner_1_at_blue', 20.6, 1.7, -62.95, 0, 1.0]] },
};

export function fixFlags(params) {
  const all = params.get('fixes') !== '0', f = (k) => all && params.get(k) !== '0';
  return { rail: f('rail'), gates: f('gates'), porch: f('porch'), eaves: f('eaves'), gap: f('gap'), signs: f('signs') };
}

/** Remove the triangles of the dressing meshes whose three vertices lie inside the cut box (world == local for DRESSING nodes). Returns the number removed. */
export function cutDressing(world, box, key = 'rail') {
  let removed = 0;
  world.traverse((o) => {
    if (!o.isMesh) return; let a = o, ok = false; while (a) { if (/^DRESSING/.test(a.name)) ok = true; a = a.parent; } if (!ok) return;
    const g = o.geometry; if (!g.index) return; g.userData.p3bCuts ||= {}; if (g.userData.p3bCuts[key]) return; g.userData.p3bCuts[key] = true; const p = g.attributes.position, idx = g.index.array, keep = []; const inb = (i) => { const x = p.getX(i), y = p.getY(i), z = p.getZ(i); return x >= box.x[0] && x <= box.x[1] && y >= box.y[0] && y <= box.y[1] && z >= box.z[0] && z <= box.z[1]; };
    for (let t = 0; t < idx.length; t += 3) { if (inb(idx[t]) && inb(idx[t + 1]) && inb(idx[t + 2])) removed++; else keep.push(idx[t], idx[t + 1], idx[t + 2]); }
    if (keep.length !== idx.length) { const Arr = idx.constructor; g.setIndex(new g.index.constructor(new Arr(keep), 1)); g.computeBoundingSphere(); }
  });
  return removed;
}

/** Open a gate in town dressing: cut the bay's triangles and remove its proxy. */
export function openGates(world, obstacles) {
  const out = []; for (const g of FIX_DATA.gates.list) { const tri = cutDressing(world, g.cutBox, g.name); let px = 0; for (let i = obstacles.length - 1; i >= 0; i--) { const o = obstacles[i]; if (o.src === 'dressing' && o.x === g.removeProxy.x && -o.z === g.removeProxy.n) { obstacles.splice(i, 1); px++; } } out.push({ gate: g.name, triangles: tri, proxies: px }); }
  return out;
}

/** Remove the proxies of the rail bays. */
export function removeRailProxies(obstacles, bays) {
  let n = 0, moved = 0; for (let i = obstacles.length - 1; i >= 0; i--) { const o = obstacles[i]; if (o.src === 'PORCH_RAIL' && o.z === -76.2 && bays.includes(o.x)) { obstacles.splice(i, 1); n++; } }
  const a = FIX_DATA.rail.alignProxies; for (const o of obstacles) { if (o.src !== 'PORCH_RAIL') continue; if (o.z === -76.2 && a.front.x.includes(o.x)) { o.z = -a.front.n; moved++; } else if (o.z === -77.2 && a.sides.x.includes(o.x)) { o.x = Math.sign(o.x) * a.sides.mesh_x; o.z = -a.sides.n; o.d = a.sides.d; moved++; } }
  return { removed: n, moved };
}

/** Camera filter predicate: true = the camera ignores this proxy because of a correction. */
export function cameraTransparent(o, flags) {
  if (!o.cameraOnly || o.group !== 'roof') return false;
  if (flags.porch && o.src === 'B01' && o.x === 0 && o.z === -80.4) return true;
  if (flags.eaves && o.minY !== undefined && o.minY < FIX_DATA.eaves.maxMinY) return true;
  return false;
}

/** Place the extra signs and banners (clones of existing kit nodes). */
export function addSigns(T, kit, world, placed, add) {
  let n = 0; for (const [id, node, x, y, z, ry, s] of add) { const src = kit[node]; if (!src) { console.warn('p3b sign node missing', node); continue; } const o = src.clone(true); o.name = id; o.position.set(x, y, z); o.rotation.y = ry * Math.PI / 180; o.scale.multiplyScalar(s); o.userData.district = 'D3'; world.add(o); placed.push(o); n++; }
  return n;
}

/** Close the B10-B11 strip: instanced crates / barrels (island prototypes) and solid proxies. */
export function addGapProps(T, isl, scene, obstacles) {
  if (!isl) return 0; let n = 0; const tmp = new T.Object3D();
  const by = {}; for (const [proto, x, nn, yaw, s, sy] of FIX_DATA.gap.props) (by[proto] ||= []).push([x, nn, yaw, s, sy || 1]);
  for (const [proto, list] of Object.entries(by)) { let src = null; const node = isl.nodes['PROTO_' + proto]; if (node) node.traverse((c) => { if (c.isMesh && !src) src = c; }); if (!src) continue;
    const im = new T.InstancedMesh(src.geometry, src.material, list.length); list.forEach(([x, nn, yaw, s, sy], i) => { tmp.position.set(x, 0 - 0.02, -nn); tmp.rotation.set(0, yaw, 0); tmp.scale.set(s, s * sy, s); tmp.updateMatrix(); im.setMatrixAt(i, tmp.matrix); });
    im.name = 'GAP_' + proto; im.castShadow = true; im.receiveShadow = true; scene.add(im); n += list.length; }
  for (const s of FIX_DATA.gap.solids) obstacles.push({ src: 'P3B:gap-closure', group: 'prop', x: s.x, z: -s.n, w: s.w, d: s.d, h: s.h });
  return n;
}
