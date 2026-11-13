// Merchant Citadel P3-B batch 1: browser measurements for the island. Runs inside the preview page against the real controller, camera and loaded terrain.
// Results are POSTed to server.mjs (merchant-citadel-p2a/evidence/). Scripted input, not a human playtest.
export function installIslandTests(P) {
  const { T, scene, renderer, camera, character, input, follow } = P, isl = P.isl;
  const mc = new MessageChannel(); const sleep = () => new Promise((r) => { mc.port1.onmessage = () => r(); mc.port2.postMessage(0); });
  const save = async (name, data) => { const body = data instanceof Blob ? data : typeof data === 'string' ? data : JSON.stringify(data, null, 1); await fetch('/__save?name=' + encodeURIComponent(name), { method: 'POST', body }); };
  const r3 = (v) => (v == null ? null : Math.round(v * 1000) / 1000), pct = (a, p) => { if (!a.length) return null; const s = [...a].sort((x, y) => x - y); return s[Math.min(s.length - 1, Math.floor(p * s.length))]; };
  const DT = 1 / 60, syncPx = new Uint8Array(4), hardSync = () => { const g = renderer.getContext(); g.readPixels(0, 0, 1, 1, g.RGBA, g.UNSIGNED_BYTE, syncPx); };
  const pos = () => character.root.position;

  // ---------------------------------------------------------------------------------------------- free-camera captures (matched to the Blender views by p3b_views.json)
  let views = null;
  async function loadViews() { return (views ||= await fetch('data/p3b-views.json').then((r) => r.json())); }
  function setCam(p, look, fov) {                                              // p, look in plan frame (x, n, z_up) -> three (x, z_up, -n)
    P.sim.frozenCamera = true; camera.position.set(p[0], p[2], -p[1]); camera.fov = fov || 50; camera.near = 0.3; camera.far = 4000; camera.updateProjectionMatrix(); camera.lookAt(look[0], look[2], -look[1]); camera.updateMatrixWorld(true);
  }
  async function blob(w, h, q = 0.9) {
    renderer.userSize = true; renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); P.render(); const c = renderer.domElement;
    const b = await new Promise((r) => c.toBlob(r, 'image/jpeg', q)); renderer.userSize = false; P.resize(); return b;
  }
  async function viewShot(name, { w = 1600, h = 900, tag = 'b' } = {}) {
    const v = (await loadViews())[name]; if (!v) throw new Error('no view ' + name); const [p, look, fov, ortho, who] = v;
    const hid = []; let fig = null;
    if (who) { fig = character.root; hid.push(fig.visible); fig.visible = true; const wz = P.heightAt(who[0], -who[1]); character.root.position.set(who[0], wz, -who[1]); }
    else { hid.push(character.root.visible); character.root.visible = false; }
    if (ortho) { const f = 2 * Math.atan((ortho / 2) / (p[2] - look[2])) * 180 / Math.PI; camera.up.set(0, 0, -1); setCam(p, look, f); }      // top view: north up
    else { camera.up.set(0, 1, 0); setCam(p, look, fov); }
    const b = await blob(w, h); await save(`p3b-${tag}-${name}.jpg`, b); character.root.visible = true; camera.up.set(0, 1, 0); P.sim.frozenCamera = false; return name;
  }
  async function viewShots(names, opts) { for (const n of names) { await viewShot(n, opts); await sleep(); P.say('shot ' + n); } return names; }

  // ---------------------------------------------------------------------------------------------- walking with the real controller
  function walk(label, pts, { run = false, maxSeconds = 240, turnRate = 2.6, keepCamera = true, sample = 6 } = {}) {
    const [x0, n0] = pts[0], [x1, n1] = pts[1] || pts[0];
    P.teleport(x0, -n0, Math.atan2(-(x1 - x0), (n1 - n0))); for (let i = 0; i < 40; i++) P.stepSim(DT);
    const rec = { y: [], cam: [], speed: [], grounded: [], phase: [] }; let t = 0, stuck = 0, stuckAt = [], maxUp = 0, prevY = pos().y, minCam = 99, minSupport = 99, falls = 0, recovered = 0, prevSafeDist = 0, maxStepDown = 0, fadeMin = 1, camHits = 0;
    const origin = new T.Vector3(); input.keys.clear(); let wi = 1;
    for (let wp = 1; wp < pts.length; wp++) {
      const [tx, tn] = pts[wp]; let best = Infinity, lastProg = t;
      while (t < maxSeconds) {
        const p = pos(), dx = tx - p.x, dz = -tn - p.z, dist = Math.hypot(dx, dz); if (dist < 0.5) break;
        if (dist < best - 0.05) { best = dist; lastProg = t; } if (t - lastProg > 2.5) { stuck++; stuckAt.push({ wp, at: [r3(p.x), r3(-p.z)], target: [tx, tn], y: r3(p.y) }); break; }
        const want = Math.atan2(-dx, -dz), diff = Math.atan2(Math.sin(want - input.yaw), Math.cos(want - input.yaw)); input.yaw += Math.max(-turnRate * DT, Math.min(turnRate * DT, diff));
        input.keys.add('w'); if (run) input.keys.add('shift'); else input.keys.delete('shift');
        const px = p.x, pz = p.z, py = p.y; P.stepSim(DT); t += DT; const q = pos();
        if (Math.hypot(q.x - px, q.z - pz) > 3) recovered++;                                        // teleported: fall recovery
        maxUp = Math.max(maxUp, q.y - py); maxStepDown = Math.max(maxStepDown, py - q.y); if (q.y < -30) falls++;
        origin.set(q.x, q.y + 1.25, q.z); const cd = camera.position.distanceTo(origin); minCam = Math.min(minCam, cd); fadeMin = Math.min(fadeMin, P.fade.alpha);
        if (Math.round(t * 60) % sample === 0) { rec.y.push(r3(q.y)); rec.cam.push(r3(cd)); rec.speed.push(r3(P.sim.motion?.speed ?? 0)); rec.phase.push(P.sim.motion?.phase); }
      }
    }
    input.keys.clear(); const end = pos(), last = pts[pts.length - 1];
    const cams = rec.cam; const meanSpeed = rec.speed.reduce((a, b) => a + b, 0) / Math.max(1, rec.speed.length);
    return { label, seconds: r3(t), stuck, stuck_at: stuckAt, end: [r3(end.x), r3(-end.z), r3(end.y)], target: last, end_error_m: r3(Math.hypot(end.x - last[0], -end.z - last[1])), max_step_up_m: r3(maxUp), max_step_down_m: r3(maxStepDown), recovered_by_fall_recovery: recovered, minimum_camera_m: r3(minCam), camera_p05_m: r3(pct(cams, 0.05)), share_camera_below_3m: r3(cams.filter((v) => v < 3).length / Math.max(1, cams.length)), min_fade_alpha: r3(fadeMin), min_y: r3(Math.min(...rec.y)), max_y: r3(Math.max(...rec.y)), mean_speed: r3(meanSpeed), phases: [...new Set(rec.phase)], series: rec };
  }

  // ---------------------------------------------------------------------------------------------- routes of the landscape (plan frame x, n)
  const ROUTES = {
    quay_to_arrival_court: [[0, -60], [0, -44], [0, -36], [0, -24], [0, -16]],
    arrival_court_to_quay: [[0, -16], [0, -24], [0, -36], [0, -44], [0, -60]],
    arrival_court_to_merchant_street: [[0, -16], [0, 2], [0, 19.9], [0, 37.5]],
    street_to_civic_terrace: [[0, 37.5], [0, 45.5], [2.9, 49], [0, 52.5], [0, 59.4], [0, 67], [0, 72], [0, 75]],
    hall_doors_and_forecourt: [[0, 74], [0, 77.4], [0, 79.3], [0, 77.4], [0, 74]],
    hall_to_crag_stair_foot: () => reach([0, 75], [18, 84]).waypoints,
    crag_ascent: [[18, 84], [34, 88], [20, 95], [36, 101], [22, 107], [34, 111], [37.6, 113.8]],
    crag_descent: [[37.6, 113.8], [34, 111], [22, 107], [36, 101], [20, 95], [34, 88], [18, 84]],
    hall_to_shoulder_table: [[-10, 80], [-16, 84], [-24, 94], [-30, 104], [-36, 112]],
    tea_house_to_overlook: [[36.16, 62.24], [36, 57], [42, 57], [50, 57.5], [60, 55.5], [70, 53], [80, 54]],
    overlook_back_to_lookout: [[80, 54], [70, 53], [60, 55.5], [50, 57.5], [42, 57], [36, 57]],
    service_court_to_lower_benches: [[33, 20], [44, 18], [52, 24], [58, 36], [60, 48], [60, 54]],
    benches_back_to_court: [[60, 54], [60, 48], [58, 36], [52, 24], [44, 18], [33, 20]],
    arrival_court_to_caravan_green: [[0, -16], [-7, -11], [-16, -4], [-26, 5], [-35, 12], [-46, 16], [-50, 18]],
    caravan_green_to_arrival_court: [[-50, 18], [-46, 16], [-35, 12], [-26, 5], [-16, -4], [-7, -11], [0, -16]],
    bridge_to_tea_stack: [[86, 46.4], [93, 46], [97, 45.8], [101.4, 45.55], [108, 45.2], [111, 45]],
    bridge_back: [[111, 45], [108, 45.2], [101.4, 45.55], [97, 45.8], [93, 46], [86, 46.4]],
  };
  async function testRoutes(names = Object.keys(ROUTES), opt = {}) {
    const out = []; for (const n of names) { const pts = typeof ROUTES[n] === 'function' ? ROUTES[n]() : ROUTES[n]; const r = walk(n, pts, opt); out.push(r); await sleep(); P.say('route ' + n); }
    await save('p3b-routes' + (opt.tag || '') + '.json', out); return out.map(({ series, ...r }) => r);
  }


  // ---------------------------------------------------------------------------------------------- reachability: A* over the real blocked() and support heights (what the controller can actually do)
  function reach(from, to, { cell = 0.5, maxStep = 0.38, bounds = [-95, 130, -90, 145], run = false } = {}) {
    const [xa, xb, na, nb] = bounds, W = Math.ceil((xb - xa) / cell), Hh = Math.ceil((nb - na) / cell), idx = (i, j) => j * W + i, cx = (i) => xa + (i + 0.5) * cell, cn = (j) => na + (j + 0.5) * cell;
    const si = Math.floor((from[0] - xa) / cell), sj = Math.floor((from[1] - na) / cell), ei = Math.floor((to[0] - xa) / cell), ej = Math.floor((to[1] - na) / cell);
    const g = new Float32Array(W * Hh).fill(Infinity), from_ = new Int32Array(W * Hh).fill(-1), closed = new Uint8Array(W * Hh); const heap = [];
    const push = (f, id) => { heap.push([f, id]); let k = heap.length - 1; while (k > 0) { const p = (k - 1) >> 1; if (heap[p][0] <= heap[k][0]) break; [heap[p], heap[k]] = [heap[k], heap[p]]; k = p; } };
    const pop = () => { const top = heap[0], last = heap.pop(); if (heap.length) { heap[0] = last; let k = 0; for (;;) { let l = 2 * k + 1, r = l + 1, m = k; if (l < heap.length && heap[l][0] < heap[m][0]) m = l; if (r < heap.length && heap[r][0] < heap[m][0]) m = r; if (m === k) break; [heap[m], heap[k]] = [heap[k], heap[m]]; k = m; } } return top; };
    const free = (i, j) => i >= 0 && j >= 0 && i < W && j < Hh && !P.blocked(cx(i), -cn(j), P.walkObs);
    const h = (i, j) => Math.hypot(i - ei, j - ej) * cell; g[idx(si, sj)] = 0; push(h(si, sj), idx(si, sj)); let found = false, expanded = 0;
    while (heap.length) {
      const [, id] = pop(); if (closed[id]) continue; closed[id] = 1; expanded++; const i = id % W, j = (id / W) | 0; if (Math.abs(i - ei) <= 1 && Math.abs(j - ej) <= 1) { found = true; from_[idx(ei, ej)] = id; break; }
      const hy = P.heightAt(cx(i), -cn(j));
      for (let di = -1; di <= 1; di++) for (let dj = -1; dj <= 1; dj++) { if (!di && !dj) continue; const a = i + di, b = j + dj; if (!free(a, b)) continue; if (di && dj && (!free(i + di, j) || !free(i, j + dj))) continue;
        const ny = P.heightAt(cx(a), -cn(b)); if (ny < -50 || Math.abs(ny - hy) > maxStep) continue; const nid = idx(a, b), cost = g[id] + (di && dj ? 1.4142 : 1) * cell; if (cost < g[nid]) { g[nid] = cost; from_[nid] = id; push(cost + h(a, b), nid); } }
    }
    if (!found) return { found: false, expanded };
    const path = []; let id = idx(ei, ej); path.push([to[0], to[1]]); id = from_[id]; while (id >= 0 && id !== idx(si, sj)) { path.push([cx(id % W), cn((id / W) | 0)]); id = from_[id]; } path.push([from[0], from[1]]); path.reverse();
    let len = 0; for (let k = 1; k < path.length; k++) len += Math.hypot(path[k][0] - path[k - 1][0], path[k][1] - path[k - 1][1]);
    const simp = [path[0]]; let acc = 0; for (let k = 1; k < path.length - 1; k++) { acc += Math.hypot(path[k][0] - path[k - 1][0], path[k][1] - path[k - 1][1]); if (acc >= 3.0) { simp.push(path[k]); acc = 0; } } simp.push(path[path.length - 1]);
    return { found: true, length_m: r3(len), walk_s: r3(len / 2.1), run_s: r3(len / 4.6), expanded, waypoints: simp.map(([x, n]) => [r3(x), r3(n)]) };
  }
  const ACCESS = { 'arrival court -> Exchange Hall podium': [[0, -16], [0, 75]], 'arrival court -> Caravan Green': [[0, -16], [-50, 18]], 'Exchange Hall -> crag stair foot': [[0, 75], [18, 84]], 'quay -> arrival court': [[5, -52], [0, -16]], 'Exchange Hall -> crag summit (beside the Counting Stone)': [[0, 75], [38, 114]], 'Exchange Hall -> Shoulder Table': [[0, 75], [-36, 112]], 'tea house veranda -> Cloudfall overlook': [[36.16, 62.24], [80, 54]], 'service court -> lower benches': [[33, 20], [60, 54]], 'overlook -> Tea Stack (bridge)': [[80, 54], [111, 45]], 'tea lookout -> Caravan Green (whole town)': [[36, 57], [-50, 18]], 'quay -> Tea Stack': [[5, -52], [111, 45]] };
  async function testAccess() { const out = {}; for (const [k, [a, b]] of Object.entries(ACCESS)) { const t = performance.now(); out[k] = { from: a, to: b, ...reach(a, b, /Stack/.test(k) ? { cell: 0.25 } : {}), ms: Math.round(performance.now() - t) }; await sleep(); } await save('p3b-access.json', out); return out; }

  // ---------------------------------------------------------------------------------------------- edges, steep ground, fall recovery
  async function testEdges() {
    const out = { edge_walks: [], steep_walks: [], fall_recovery: [], rim_margin: null };
    // push the explorer toward the rim from several bearings: they must stop on the island with y near the support height, never airborne below
    const starts = [[-50, 18, 180], [-50, 18, 225], [5, -52, 270], [5, -52, 0], [20, -60, 315], [40, 116, 80], [-36, 112, 120], [80, 54, 0], [111, 45, 0], [5, 100, 90], [-60, 60, 180]];
    for (const [sx, sn, deg] of starts) {
      P.teleport(sx, -sn, 0); for (let i = 0; i < 30; i++) P.stepSim(DT); const a = deg * Math.PI / 180; input.keys.clear(); input.keys.add('w'); input.keys.add('shift'); let minY = 1e9, recov = 0, t = 0;
      input.yaw = Math.atan2(-Math.cos(a), Math.sin(a)) + Math.PI;           // face the bearing (plan angle a from +x toward +n) : forward = (-sin yaw, -cos yaw) in (x, z)
      input.yaw = Math.atan2(-Math.cos(a), Math.sin(a));
      for (let i = 0; i < 60 * 12; i++) { const p0 = pos().clone(); input.yaw = Math.atan2(-Math.cos(a), Math.sin(a)); P.stepSim(DT); t += DT; const q = pos(); minY = Math.min(minY, q.y); if (Math.hypot(q.x - p0.x, q.z - p0.z) > 3) recov++; }
      input.keys.clear(); const q = pos(); out.edge_walks.push({ start: [sx, sn], bearing: deg, end: [r3(q.x), r3(-q.z)], y: r3(q.y), support: r3(P.heightAt(q.x, q.z)), min_y: r3(minY), on_island: P.heightAt(q.x, q.z) > -50, walkable_cell: isl.walkable(q.x, q.z), distance_travelled: r3(Math.hypot(q.x - sx, -q.z - sn)), recoveries: recov });
    }
    // steep ground: walk straight at the tea riser and the crag face
    for (const [label, a, b] of [['tea riser, outward', [54, 46], [62, 46]], ['crag face, northward', [30, 98], [30, 118]], ['quay retaining wall, southward from the court', [-14, -22], [-14, -40]], ['hall shelf bank, northward (west of the terrace)', [-30, 70], [-30, 82]]]) {
      const r = walk(label, [a, b], { maxSeconds: 20 }); out.steep_walks.push({ label, start: a, target: b, end: r.end, stuck: r.stuck, max_step_up_m: r.max_step_up_m, min_y: r.min_y, max_y: r.max_y });
    }
    // fall recovery: put the character in the void, step, expect to land back on the last safe ground; and a long fall from the Tea Stack side
    for (const [label, sx, sn] of [['void south of the quay', 5, -110], ['void east of the stack', 150, 45], ['void under the crag', 40, 150], ['inside the rim lip (blocked cell)', -81, 18]]) {
      P.teleport(5, 52, 0); for (let i = 0; i < 20; i++) P.stepSim(DT); const safeBefore = [r3(pos().x), r3(-pos().z)];
      character.root.position.set(sx, -60, -sn); let steps = 0; const y0 = pos().y; while (steps < 120 && pos().y < -40) { P.stepSim(DT); steps++; }
      for (let i = 0; i < 30; i++) P.stepSim(DT); const q = pos(); out.fall_recovery.push({ label, from: [sx, sn], steps_to_recover: steps, end: [r3(q.x), r3(-q.z), r3(q.y)], expected_near: safeBefore, back_on_support: P.heightAt(q.x, q.z) > -50 && Math.abs(q.y - P.heightAt(q.x, q.z)) < 0.05, grounded: character.movement ? true : null });
    }
    // a jump toward the edge of the quay cannot leave the island: jump + sprint at the prow
    P.teleport(5, 70, 0); input.keys.clear(); let left = false; for (let i = 0; i < 60 * 6; i++) { input.yaw = Math.PI; input.keys.add('w'); input.keys.add('shift'); P.stepSim(DT, i % 40 === 0); if (P.heightAt(pos().x, pos().z) < -50 && pos().y < -3) left = true; } input.keys.clear();
    out.jump_at_prow = { left_island: left, end: [r3(pos().x), r3(-pos().z), r3(pos().y)] };
    await save('p3b-edges.json', out); return out;
  }

  // ---------------------------------------------------------------------------------------------- rendered vs physical ground (character feet against the visible mesh)
  async function testSupport() {
    const out = { grid: { nx: isl.meta.nx, nn: isl.meta.nn, cell: isl.meta.cell, bytes_terrain: isl.H.byteLength, bytes_mask: isl.MK.byteLength, range_m: isl.meta.height_range_m, precision_m: 0.01 }, bounds: { controller: isl.bounds, extents: isl.meta.extents, derived: isl.meta.derived_bounds }, interpolation: [], lookup_cost: null };
    // bilinear continuity: height must be continuous across grid lines (no step larger than the local gradient allows)
    let maxJump = 0; for (let k = 0; k < 20000; k++) { const x = -60 + Math.random() * 150, n = -60 + Math.random() * 180, a = isl.terrainAt(x, n), b = isl.terrainAt(x + 0.01, n); if (a > -50 && b > -50) maxJump = Math.max(maxJump, Math.abs(a - b)); }
    out.continuity = { samples: 20000, max_height_change_over_1cm_m: r3(maxJump), note: 'steepest riser is about 1.4 m per m, so 1.4 cm per cm is expected; a larger value would be a seam' };
    // town layer agreement: heights over authored paving come from the town grid
    const town = []; for (const [x, n] of [[0, 2], [0, 40], [0, 59], [0, 67], [0, 75], [0, 85], [-13, 49], [13, 49], [36, 57], [36.16, 62.24], [0, 77.4]]) town.push({ at: [x, n], island_terrain: r3(isl.terrainAt(x, n)), town_grid: r3(P.townHeightAt(x, -n)), used: r3(P.heightAt(x, -n)) });
    out.town_layer = town;
    // lookup cost
    const t0 = performance.now(); let s = 0; for (let k = 0; k < 400000; k++) s += P.heightAt(-60 + (k % 200) * 0.7, -(k % 311) * 0.5); out.lookup_cost = { heightAt_calls: 400000, ms: r3(performance.now() - t0), per_call_us: r3((performance.now() - t0) / 400), checksum: r3(s) };
    await save('p3b-support.json', out); return out;
  }

  // ---------------------------------------------------------------------------------------------- landing compatibility (dragon model measured, surfaces scanned, no whitelist)
  async function measureDragon() {
    const loader = new T.GLTFLoader(); const g = await loader.loadAsync('../assets/game/skyport/boarding/dragon.glb'); g.scene.updateMatrixWorld(true);
    const box = new T.Box3().setFromObject(g.scene), size = box.getSize(new T.Vector3()); const clips = g.animations.map((a) => ({ name: a.name, s: r3(a.duration) }));
    const sc = g.scene.scale.x, rec = { bounds_bind_pose_m: [r3(size.x), r3(size.y), r3(size.z)], scale: sc, animations: clips.slice(0, 40) };
    // pose-evaluated bounds for the idle flight clip, if the mixer is available
    try { const mixer = new T.AnimationMixer(g.scene); const clip = g.animations.find((a) => a.name === 'Flying_Idle'); if (clip) { const act = mixer.clipAction(clip); act.play(); let wmax = 0, lmax = 0; for (let t = 0; t < clip.duration; t += clip.duration / 12) { mixer.setTime(t); g.scene.updateMatrixWorld(true); g.scene.traverse((o) => { if (o.isSkinnedMesh) o.skeleton.update(); }); const b = new T.Box3().setFromObject(g.scene, true).getSize(new T.Vector3()); wmax = Math.max(wmax, b.x, b.z); lmax = Math.max(lmax, b.z); } rec.idle_flight_max_extent_m = r3(wmax); } } catch (e) { rec.pose_error = String(e); }
    return rec;
  }
  async function testLanding() {
    const dr = await measureDragon(); const span = Math.max(dr.idle_flight_max_extent_m || 0, ...dr.bounds_bind_pose_m);
    const dragonRadius = r3(span / 2); const out = { dragon: dr, dragon_footprint_radius_used_m: dragonRadius, criteria: null, scan: null, examples: [], note: 'criteria are this phase proposal (no dragon controller in this branch); eligibility is computed from the loaded terrain, not from a list of places' };
    const solids = P.obstacles.filter((o) => !o.cameraOnly);
    const crit = { radius: Math.max(dragonRadius, 3), edgeClear: 4, obstacleClear: 1.0, maxRange: 0.5, maxSlope: 0.18, obstacles: solids, approachRange: 40, approachClear: 3.0, glide: 0.10, dismountDist: 3.0 }; out.criteria = { ...crit, obstacles: solids.length + ' solids' };
    const t0 = performance.now(); const hits = isl.landing.scan(crit, { step: 2 }); out.scan = { cells_eligible_at_2m_step: hits.length, ms: r3(performance.now() - t0) };
    // cluster the hits into surfaces (greedy, 6 m apart) and report each cluster's best cell
    const cl = []; for (const h of hits.sort((a, b) => b.rim_distance - a.rim_distance)) { if (!cl.some((c) => Math.hypot(c.x - h.x, c.n - h.n) < 7)) cl.push({ ...h, count: 1 }); else cl.find((c) => Math.hypot(c.x - h.x, c.n - h.n) < 7).count++; }
    out.surfaces = cl.map((c) => ({ at: [r3(c.x), r3(c.n)], z: r3(c.z), cells: c.count, range_m: r3(c.range), slope: r3(c.slope), rim_m: r3(c.rim_distance), nearest_solid_m: r3(c.obstacle_clearance), approach_bearings_deg: c.approach_bearings }));
    for (const [name, x, n, r] of [['Caravan Green', -50, 18, 14], ['Sky Quay', 5, -52, 11], ['Shoulder Table', -36, 112, 6], ['Hall lawn west', -32.5, 85, 7.5]]) {
      const lg = isl.landing.largestAt(x, n, crit, 30); const ev = isl.landing.evaluate(x, n, { ...crit, radius: crit.radius });
      out.examples.push({ name, centre: [x, n], p3a_radius: r, dragon_radius_test: ev ? { eligible: ev.eligible, range_m: r3(ev.range), slope: r3(ev.slope), rim_m: r3(ev.rim_distance), nearest_solid_m: r3(ev.obstacle_clearance), nearest: ev.obstacle, approach_deg: ev.approach_bearings, dismount: ev.dismount } : null, largest_eligible_radius_at_centre_m: lg.radius });
    }
    await save('p3b-landing.json', out); return out;
  }

  // ---------------------------------------------------------------------------------------------- camera against landscape (yaw sweeps at spots)
  async function testCameraSpots() {
    const spots = [['quay centre', 5, -52], ['ramp head', 0, -26], ['ramp middle', 0, -31], ['ramp foot', 0, -36], ['crag stair foot', 18, 84], ['crag stair, first switchback', 34, 88], ['crag mid', 20, 95], ['crag upper', 36, 101], ['crag summit stone', 40, 116], ['shoulder table', -36, 112], ['hall lawn west', -32.5, 85], ['east of hall (shelf)', 20, 82], ['behind hall (shelf)', 0, 93], ['tea promenade start', 42, 57], ['tea promenade middle', 60, 55.5], ['cloudfall overlook', 80, 54], ['porters loop bend', 52, 24], ['lower benches', 60, 48], ['caravan green', -50, 18], ['artisan gate path', -36, 20], ['bridge middle', 98, 45.9], ['tea stack top', 111, 45], ['east of the hall podium edge', 15.5, 82], ['bank behind tea house', 36, 74.5]];
    const out = []; for (const [label, x, n] of spots) {
      P.teleport(x, -n, 0); for (let i = 0; i < 40; i++) P.stepSim(DT); const ds = [], al = []; const origin = new T.Vector3();
      for (let k = 0; k < 24; k++) { input.yaw = k * Math.PI / 12; for (let i = 0; i < 30; i++) P.stepSim(DT); const p = pos(); origin.set(p.x, p.y + 1.25, p.z); ds.push(camera.position.distanceTo(origin)); al.push(P.fade.alpha); }
      out.push({ label, at: [x, n], support: r3(P.heightAt(x, -n)), min_camera_m: r3(Math.min(...ds)), share_below_3m: r3(ds.filter((d) => d < 3).length / ds.length), min_alpha: r3(Math.min(...al)) }); await sleep();
    }
    await save('p3b-camera-spots.json', out); return out;
  }

  // ---------------------------------------------------------------------------------------------- performance (valid in-engine timing: CPU submit and GPU-complete via read-back)
  function loadInfo() { return { cores: navigator.hardwareConcurrency, dpr: devicePixelRatio, ua: navigator.userAgent.slice(0, 120) }; }
  async function measure(label, setup, { w = 1280, h = 720, frames = 180, warm = 30, shadows = true } = {}) {
    P.setShadows(shadows); renderer.userSize = true; renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); setup(); if (P.isl) P.isl.tick(0);
    for (let i = 0; i < warm; i++) { P.render(); hardSync(); }
    const cpu = [], gpu = []; let info = null;
    for (let i = 0; i < frames; i++) { const t0 = performance.now(); P.render(); const t1 = performance.now(); hardSync(); const t2 = performance.now(); cpu.push(t1 - t0); gpu.push(t2 - t0); if (i === frames - 1) { const r = renderer.info.render; info = { calls: r.calls, triangles: r.triangles, geometries: renderer.info.memory.geometries, textures: renderer.info.memory.textures }; } if (i % 20 === 19) await sleep(); }
    renderer.userSize = false; P.resize(); P.sim.frozenCamera = false;
    return { label, w, h, shadows, frames, cpu_submit_ms: { p50: r3(pct(cpu, 0.5)), p95: r3(pct(cpu, 0.95)) }, frame_complete_ms: { p50: r3(pct(gpu, 0.5)), p95: r3(pct(gpu, 0.95)), max: r3(Math.max(...gpu)) }, implied_fps_p50: r3(1000 / pct(gpu, 0.5)), ...info };
  }
  async function testPerf(tag = '') {
    const out = { when: new Date().toISOString(), machine: loadInfo(), note: 'frame_complete = render() + 1x1 read-back (forces GPU completion; not vsync-limited). Run on a shared desktop: the load average is recorded by the caller.', cases: [] };
    const sets = {
      'street level, arrival court (gameplay camera)': () => { P.sim.frozenCamera = false; P.teleport(0, -16, 0); for (let i = 0; i < 60; i++) P.stepSim(DT); },
      'street level, Exchange Hall forecourt': () => { P.sim.frozenCamera = false; P.teleport(0, -75.4, Math.PI); for (let i = 0; i < 60; i++) P.stepSim(DT); },
      'tea lookout (gameplay camera)': () => { P.sim.frozenCamera = false; P.teleport(36, -57, -Math.PI / 2); for (let i = 0; i < 60; i++) P.stepSim(DT); },
      'aerial: whole island (v1)': async () => {}, 'flight: dragon approach south-west (v6)': async () => {}, 'flight: dragon approach east (v6b)': async () => {}, 'underside from below (v2b side south)': async () => {},
    };
    const vv = await loadViews(); const viewSet = (name) => () => { const [p, look, fov] = vv[name]; setCam(p, look, fov); };
    const list = [['street level, arrival court (gameplay camera)', sets['street level, arrival court (gameplay camera)']], ['street level, Exchange Hall forecourt', sets['street level, Exchange Hall forecourt']], ['tea lookout (gameplay camera)', sets['tea lookout (gameplay camera)']],
      ['aerial: whole island (v1)', viewSet('v1-aerial')], ['flight: dragon approach south-west (v6)', viewSet('v6-dragon-approach')], ['flight: dragon approach east (v6b)', viewSet('v6b-dragon-approach-east')], ['side profile south (v2b)', viewSet('v2b-side-south')]];
    for (const [label, fn] of list) { out.cases.push(await measure(label, fn)); P.say('perf ' + label); await sleep(); }
    // island off (town only) at the same cameras for the delta
    if (isl) { isl.group.visible = false; for (const [label, fn] of list.slice(0, 3).concat([list[3]])) { const m = await measure(label + ' [island hidden]', fn); out.cases.push(m); await sleep(); } isl.group.visible = true; }
    out.shadows_off = [await measure('aerial: whole island (v1), shadows off', viewSet('v1-aerial'), { shadows: false })];
    P.setShadows(true); await save('p3b-perf' + tag + '.json', out); return out;
  }

  P.island = { reach, testAccess, ACCESS, viewShot, viewShots, walk, testRoutes, testEdges, testSupport, testLanding, testCameraSpots, testPerf, measure, setCam, ROUTES, blob, save, sleep, measureDragon };
}
