// Merchant Citadel P2-A: automated measurements. Runs inside the preview page against the real controller and camera.
// Results are POSTed to server.mjs, which writes them to merchant-citadel-p2a/evidence/.
export function installTests(P) {
  const { T, scene, renderer, camera, follow, character, input, sceneData, hf, heightAt } = P;
  // A hidden Browser pane throttles timers to about 1 Hz and stops requestAnimationFrame, so the tests never wait on either:
  // they yield through a MessageChannel and time work with synchronous, GPU-synced loops.
  const mc = new MessageChannel(); const sleep = () => new Promise((r) => { mc.port1.onmessage = () => r(); mc.port2.postMessage(0); });
  const save = async (name, data) => { const body = data instanceof Blob ? data : typeof data === 'string' ? data : JSON.stringify(data, null, 1); await fetch('/__save?name=' + encodeURIComponent(name), { method: 'POST', body }); };
  // gl.finish() does NOT wait for the GPU in Chromium (measured: 1.6 ms with it vs 10.8 ms with a read-back for the same frame on an M4 Pro).
  // A 1x1 readPixels after the draw forces completion, so every GPU-inclusive timing below uses it. (The P2-A figures used finish() and under-reported.)
  const syncPx = new Uint8Array(4); const hardSync = () => { const g = renderer.getContext(); g.readPixels(0, 0, 1, 1, g.RGBA, g.UNSIGNED_BYTE, syncPx); };
  const N = (k) => sceneData.nodes[k];
  const pct = (a, p) => { if (!a.length) return null; const s = [...a].sort((x, y) => x - y); return s[Math.min(s.length - 1, Math.floor(p * s.length))]; };
  const r3 = (v) => (v == null ? null : Math.round(v * 1000) / 1000);
  // A-E are the P2-A modes (thin posts block the camera); F is the closeout default (thin posts ignored) and the mode every other test runs in.
  const MODES = { 'A solids and roofs (P2-A)': { postsBlock: true }, 'B plus cloth': { postsBlock: true, cloth: true }, 'C plus cloth, signs, pennants': { postsBlock: true, cloth: true, sign: true, pennant: true }, 'D signs only': { postsBlock: true, sign: true }, 'E pennants only': { postsBlock: true, pennant: true }, 'F thin posts ignored (default)': {}, 'G default plus cloth': { cloth: true }, 'H default plus pennants': { pennant: true } };
  const setMode = (m) => { Object.assign(P.camGroups, { cloth: false, sign: false, pennant: false, balcony: true, roof: true, overhang: true, arch: true }, m); P.camOff.clear(); if (!m.postsBlock) P.camOff.add('post'); P.refreshObstacles(); };

  // ---------------------------------------------------------------------------------------------- geometry of the proxies (for clearance measurements)
  function distToObstacle(px, pz, o) {                                  // distance from a point to the footprint edge of a solid proxy
    let dx = px - o.x, dz = pz - o.z, w = o.w, d = o.d;
    if (o.oriented) { const c = Math.cos(o.oriented.rotation), s = Math.sin(o.oriented.rotation); [dx, dz] = [dx * c - dz * s, dx * s + dz * c]; w = o.oriented.w; d = o.oriented.d; }
    const ex = Math.max(Math.abs(dx) - w / 2, 0), ez = Math.max(Math.abs(dz) - d / 2, 0);
    return Math.hypot(ex, ez);
  }
  const solids = () => P.obstacles.filter((o) => !o.cameraOnly);
  const sideClearance = (px, pz) => { let best = 99, who = null; for (const o of solids()) { const d = distToObstacle(px, pz, o) - 0.34; if (d < best) { best = d; who = o.src + ':' + o.group; } } return [best, who]; };

  // ---------------------------------------------------------------------------------------------- route runner (real controller, real camera, fixed 60 Hz steps)
  const DT = 1 / 60;
  const origin = new T.Vector3();
  const camDist = () => { const p = character.root.position; origin.set(p.x, p.y + 1.25, p.z); return camera.position.distanceTo(origin); };
  const FULL = Math.hypot(11.8, 6.6 - 1.25 + 0.19 * 3);              // unobstructed follow distance for pitch 0.19
  function turnStats(pts) {
    let over60 = 0, total = 0;
    for (let i = 1; i + 1 < pts.length; i++) {
      const a = Math.atan2(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]), b = Math.atan2(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]);
      const d = Math.abs(Math.atan2(Math.sin(b - a), Math.cos(b - a))) * 180 / Math.PI; total += d; if (d > 60) over60++;
    }
    return { over60, total: Math.round(total) };
  }
  function runRoute(label, pts, { run = false, maxSeconds = 90, mode = {}, turnRate = 2.4, startYaw = null } = {}) {
    setMode(mode);
    const [x0, n0] = pts[0], [x1, n1] = pts[1];
    P.teleport(x0, -n0, startYaw ?? Math.atan2(-(x1 - x0), -(-(n1 - n0))));
    for (let i = 0; i < 40; i++) P.stepSim(DT);                    // let the camera settle behind the player
    const rec = { t: [], d: [], y: [], speed: [], n: [], x: [], phase: [], side: [], alpha: [] };
    let t = 0, stuck = 0, stuckWaypoints = [], prevD = camDist(), pops = 0, maxCamSpeed = 0, prevCam = camera.position.clone(), maxStepUp = 0, prevY = character.root.position.y, minSide = [99, null, null];
    input.keys.clear();
    for (let wp = 1; wp < pts.length; wp++) {
      const [tx, tn] = pts[wp]; let best = Infinity, lastProgress = t;
      while (t < maxSeconds) {
        const p = character.root.position, dx = tx - p.x, dz = -tn - p.z, dist = Math.hypot(dx, dz);
        if (dist < 0.45) break;
        if (dist < best - 0.05) { best = dist; lastProgress = t; }
        if (t - lastProgress > 2.0) { stuck++; stuckWaypoints.push({ wp, at: [r3(p.x), r3(-p.z)], target: [tx, tn] }); break; }
        const want = Math.atan2(-dx, -dz); let diff = Math.atan2(Math.sin(want - input.yaw), Math.cos(want - input.yaw));
        input.yaw += Math.max(-turnRate * DT, Math.min(turnRate * DT, diff));
        input.keys.add('w'); if (run) input.keys.add('shift'); else input.keys.delete('shift');
        P.stepSim(DT); t += DT;
        const cd = camDist(), dd = cd - prevD; if (Math.abs(dd) > 0.5) pops++; prevD = cd;
        const cs = camera.position.distanceTo(prevCam) / DT; if (cs > maxCamSpeed) maxCamSpeed = cs; prevCam.copy(camera.position);
        const up = p.y - prevY; if (up > maxStepUp) maxStepUp = up; prevY = p.y;
        if (Math.round(t * 60) % 6 === 0) {
          rec.t.push(r3(t)); rec.d.push(r3(cd)); rec.y.push(r3(p.y)); rec.speed.push(r3(P.sim.motion?.speed ?? 0)); rec.n.push(r3(-p.z)); rec.x.push(r3(p.x)); rec.phase.push(P.sim.motion?.phase); rec.alpha.push(r3(P.fade.alpha));
          const [sc, who] = sideClearance(p.x, p.z); rec.side.push(r3(sc)); if (sc < minSide[0]) minSide = [sc, [r3(p.x), r3(-p.z)], who];
        }
      }
    }
    input.keys.clear();
    const turns = turnStats(pts);
    const d = rec.d;
    return { label, mode: Object.entries(mode).filter(([, v]) => v).map(([k]) => k).join('+') || 'solids and roofs', seconds: r3(t), samples: d.length, full_distance: r3(FULL), min_distance: r3(Math.min(...d)), p05: r3(pct(d, 0.05)), median: r3(pct(d, 0.5)),
      share_below_6m: r3(d.filter((v) => v < 6).length / d.length), share_below_3m: r3(d.filter((v) => v < 3).length / d.length), pops_over_0_5m: pops, max_camera_speed_mps: r3(maxCamSpeed), stuck, stuck_waypoints: stuckWaypoints,
      turns_over_60: turns.over60, total_turn_deg: turns.total, max_step_up_m: r3(maxStepUp), min_side_clearance_m: r3(minSide[0]), min_side_at: minSide[1], min_side_with: minSide[2], end: [r3(character.root.position.x), r3(-character.root.position.z), r3(character.root.position.y)], min_alpha: Math.min(...rec.alpha), share_faded_below_0_9: r3(rec.alpha.filter((v) => v < 0.9).length / rec.alpha.length), series: rec };
  }
  const via = (...keys) => keys.map((k) => [N(k)[0], N(k)[1]]);
  const ROUTES = {
    street_axis_straight_through_cross: { pts: [[0, 2], [0, 22], [0, 40], [0, 58]] },            // documents the cross as a solid on the axis (P2-A finding; the network routes round it)
    street_axis: { pts: [[0, 2], [0, 19.9], [0, 37.5], [0, 45.5], [2.9, 49], [0, 52.5], [0, 59.4]] },     // the P1.4 primary spine as corrected: N04 N05 N29 N27 N06
    street_axis_run: { pts: [[0, 2], [0, 19.9], [0, 37.5], [0, 45.5], [2.9, 49], [0, 52.5], [0, 59.4]], run: true },
    street_axis_west_of_cross: { pts: [[0, 37.5], [0, 45.5], [-2.9, 49], [0, 52.5], [0, 59.4]] },
    junction_west_cross_street: { pts: [[0, 10], [0, 19.9], [-14, 19.9], [0, 19.9], [0, 30]] },        // corrected 4.2 m street between the moved B04 and B05
    junction_east_cross_street: { pts: [[0, 10], [0, 19.9], [14, 19.9], [0, 19.9], [0, 30]] },
    turret_corner_pass: { pts: [[3, 4], [-2.6, 12], [-2.6, 19.9], [0, 22]] },
    turret_corner_hug: { pts: [[0, 6], [-3.6, 14], [-3.6, 19.9], [-8, 19.9]] },                       // close to the A11 turret, then into the cross street
    awning_rows_walk: { pts: [[0, 38], [-3.4, 45], [-3.4, 54], [0, 59]] },
    cross_passage: { pts: [[-4, 46], [4, 46], [-4, 46]] },
    inn_lane_south: { pts: [[-19.2, 58.6], [-19.2, 41]] },
    inn_lane_north: { pts: [[-19.2, 41], [-19.2, 58.6]] },
    inn_diagonal_N38_N11: { pts: via('N38', 'N11') },
    inn_diagonal_N11_N38: { pts: via('N11', 'N38') },
    tea_route_N24_N17: { pts: via('N24', 'N41', 'N16', 'N17') },
    tea_route_N17_N24: { pts: via('N17', 'N16', 'N41', 'N24') },
    tea_N16_N17: { pts: via('N16', 'N17') },
    tea_N17_N16: { pts: via('N17', 'N16') },
    tea_from_west_oblique: { pts: [[34, 58], [36.16, 62.24]] },
    tea_from_east_oblique: { pts: [[38.5, 58], [36.16, 62.24]] },
    hall_stairs_up: { pts: [[0, 59.4], [0, 67], [0, 75]] },
    hall_stairs_down: { pts: [[0, 75], [0, 67], [0, 59.4]] },
    hall_porch_landing: { pts: [[0, 75], [0, 77.4], [-1.5, 77.4], [1.5, 77.4], [0, 75]] },
    // ---- P2-B batch 2: the Central Bazaar. Hall-local frame: West hall centre (-13, 50), East hall centre (13, 50); front (entrance) at n 44.
    bz_west_enter: { pts: [[-16, 38.5], [-13, 42.5], [-13, 49]] },
    bz_west_leave_south: { pts: [[-13, 49], [-13, 42.5], [-16, 38.5]] },
    bz_west_exit_east: { pts: [[-13, 49], [-8, 49], [-2.9, 49]] },
    bz_west_enter_from_cross: { pts: [[-2.9, 49], [-8, 49], [-13, 49]] },
    bz_west_loop: { pts: [[-13, 42.5], [-13, 46], [-13.6, 49], [-13, 52], [-11.6, 53.4], [-13.0, 53.3], [-14.4, 52.0], [-13.4, 47], [-13, 42.5]] },
    bz_west_north_end: { pts: [[-13, 49], [-13, 52.9], [-14.6, 53.4], [-13, 52.9], [-11.4, 53.4], [-13, 52.9], [-13, 49]] },     // the north end has a bench on the axis (n 54.9): turn before it
    bz_east_enter: { pts: [[16, 38.5], [13, 42.5], [13, 49]] },
    bz_east_leave_south: { pts: [[13, 49], [13, 42.5], [16, 38.5]] },
    bz_east_exit_west: { pts: [[13, 49], [8, 49], [2.9, 49]] },
    bz_east_enter_from_cross: { pts: [[2.9, 49], [8, 49], [13, 49]] },
    bz_east_loop: { pts: [[13, 42.5], [13, 46], [12.4, 49], [12.8, 52], [14.2, 53.4], [12.6, 53.3], [12.0, 52.0], [11.8, 47], [13, 42.5]] },
    bz_hall_to_hall: { pts: [[-13, 49], [-2.9, 49], [-2.9, 46.4], [0, 45.5], [2.9, 46.4], [2.9, 49], [13, 49]] },
    bz_hall_to_hall_back: { pts: [[13, 49], [2.9, 49], [2.9, 46.4], [0, 45.5], [-2.9, 46.4], [-2.9, 49], [-13, 49]] },
    bz_cross_circle_cw: { pts: [[2.9, 46.4], [2.9, 51.6], [-2.9, 51.6], [-2.9, 46.4], [2.9, 46.4]] },
    bz_cross_circle_ccw: { pts: [[-2.9, 46.4], [-2.9, 51.6], [2.9, 51.6], [2.9, 46.4], [-2.9, 46.4]] },
    bz_circuit: { pts: [[-16, 38.5], [-13, 42.5], [-13, 49], [-2.9, 49], [-2.9, 51.6], [0, 52.5], [2.9, 51.6], [2.9, 49], [13, 49], [13, 42.5], [16, 38.5], [0, 37.5], [-16, 38.5]] },
    bz_shop_B14_front: { pts: [[19.2, 41], [21.2, 40.4], [19.2, 41]] },
    bz_shop_E06_front: { pts: [[19.2, 46.8], [21.6, 46.9], [19.2, 46.8]] },
    bz_shop_E07_front: { pts: [[-19.2, 55.6], [-21.2, 55.6], [-19.2, 55.6]] },
  };

  // ---------------------------------------------------------------------------------------------- tests
  async function testScale() {
    const expected = await fetch('data/expected-bounds.json').then((r) => r.json());
    const out = { nodes: [], orientation: [], textures: [], materials: [] };
    for (const [name, node] of Object.entries(P.kit)) {
      const b = new T.Box3().setFromObject(node), s = b.getSize(new T.Vector3()), e = expected[name]?.bbox_gltf;           // [minx, miny, minz, maxx, maxy, maxz] from the Blender kit
      const rec = { node: name, size: [r3(s.x), r3(s.z), r3(s.y)], blender_bbox: e || null, delta_cm: e ? [r3((b.min.x - e[0]) * 100), r3((b.min.y - e[1]) * 100), r3((b.min.z - e[2]) * 100), r3((b.max.x - e[3]) * 100), r3((b.max.y - e[4]) * 100), r3((b.max.z - e[5]) * 100)] : null,
        min_y: r3(b.min.y), centre_xz: [r3((b.min.x + b.max.x) / 2), r3((b.min.z + b.max.z) / 2)] };
      out.nodes.push(rec);
    }
    const front = (n) => { const b = new T.Box3().setFromObject(P.kit[n]); return (b.min.z + b.max.z) / 2; };
    out.orientation.push({ check: 'A11 turret proud of the front: bounds centre z > 0 (front = +z in glTF)', value: r3(front('A11')), pass: front('A11') > 0 }, { check: 'A09 inn balcony projects to the front: centre z > 0', value: r3(front('A09')), pass: front('A09') > 0 },
      { check: 'A08 tea house veranda projects to the front: centre z > 0', value: r3(front('A08')), pass: front('A08') > 0 });
    const env = await fetch('data/expected-envelopes.json').then((r) => r.json());          // envelopes measured on the P1.4 Blender world (07 of P1.4)
    out.placement = [];
    for (const [id, e] of Object.entries(env)) {
      const objs = P.placed.filter((p) => p.name === id || p.name.startsWith(id + '_') || (e.union_with && p.name === e.union_with)); if (!objs.length) continue;
      const b = new T.Box3(); for (const o of objs) b.union(new T.Box3().setFromObject(o, true));
      const d = [b.min.x - e.full_x[0], b.max.x - e.full_x[1], b.min.z - -e.full_n[1], b.max.z - -e.full_n[0]].map((v) => r3(v * 100));
      out.placement.push({ id, three_x: [r3(b.min.x), r3(b.max.x)], three_n: [r3(-b.max.z), r3(-b.min.z)], blender_x: e.full_x, blender_n: e.full_n, delta_cm: d, bound_only: !!e.aabb_bound, pass: e.aabb_bound ? (d[0] >= -5 && d[1] <= 5 && d[2] >= -5 && d[3] <= 5 && Math.abs(d[0]) + Math.abs(d[1]) + Math.abs(d[2]) + Math.abs(d[3]) < 400) : d.every((v) => Math.abs(v) < 5) });
    }
    out.transforms_clean = Object.entries(P.kit).filter(([, n]) => n.position.lengthSq() > 1e-12 || Math.abs(n.quaternion.w - 1) > 1e-9 || Math.abs(n.scale.x - 1) > 1e-9).map(([k]) => k);
    for (const t of P.textures) { const im = t.image, w = im?.width || im?.videoWidth || 0, h = im?.height || 0; out.textures.push({ name: t.name || '', w, h, colorSpace: t.colorSpace, mips: t.generateMipmaps, gpu_mb: r3(w * h * 4 * 4 / 3 / 1048576) }); }
    out.texture_totals = { count: out.textures.length, gpu_mb: r3(out.textures.reduce((a, t) => a + t.gpu_mb, 0)), zero_sized: out.textures.filter((t) => !t.w).length, largest: out.textures.sort((a, b) => b.gpu_mb - a.gpu_mb).slice(0, 5) };
    for (const m of P.materials) out.materials.push({ name: m.name, map: !!m.map, normal: !!m.normalMap, rough: !!m.roughnessMap, vertexColors: m.vertexColors, side: m.side, transparent: m.transparent, alphaTest: m.alphaTest, mapSpace: m.map?.colorSpace || null });
    out.material_totals = { unique_materials: P.materials.size, unique_geometries: P.geometries.size, load_ms: r3(P.loadMs) };
    await save('scale-texture-report.json', out); return out;
  }

  async function testRoutes(names = Object.keys(ROUTES)) {
    const all = [];
    for (const name of names) for (const [mname, m] of Object.entries(MODES)) { const r = runRoute(name, ROUTES[name].pts, { run: ROUTES[name].run, mode: m }); r.mode = mname; all.push(r); await sleep(0); P.say(`route ${name} / ${mname}`); }
    setMode({});
    await save('camera-routes.json', all);
    return all.map(({ series, ...r }) => r);
  }


  // What limits the camera? Run each case to its end, let the camera settle, then cast the unobstructed camera ray (head to ideal position)
  // against every camera obstacle on its own and against the ground only, and list what it hits first.
  async function testCameraCause() {
    const cases = [['inn_diagonal_N38_N11', ROUTES.inn_diagonal_N38_N11.pts, {}], ['inn_diagonal_N11_N38', ROUTES.inn_diagonal_N11_N38.pts, {}], ['tea veranda, end of N16 > N17', ROUTES.tea_N16_N17.pts, {}], ['tea veranda facing out, end of N17 > N16 first leg', ROUTES.tea_N17_N16.pts.slice(0, 2), {}],
      ['turret_corner_pass', ROUTES.turret_corner_pass.pts, {}], ['junction_west_cross_street (outbound)', ROUTES.junction_west_cross_street.pts.slice(0, 3), {}], ['hall_porch_landing', ROUTES.hall_porch_landing.pts, {}], ['hall_stairs_down end', ROUTES.hall_stairs_down.pts, {}],
      ['street_axis_run (pennants on)', ROUTES.street_axis_run.pts, { pennant: true }], ['awning_rows_walk (cloth on)', ROUTES.awning_rows_walk.pts, { cloth: true }], ['cross_passage (cloth on)', ROUTES.cross_passage.pts, { cloth: true }]];
    const out = [];
    for (const [label, pts, mode] of cases) {
      const r = runRoute(label, pts, { mode }); for (let i = 0; i < 90; i++) P.stepSim(DT);
      const p = character.root.position, a = new T.Vector3(p.x, p.y + 1.25, p.z), dir = camera.position.clone().sub(a), settled = dir.length(); dir.normalize();
      const b = a.clone().addScaledVector(dir, FULL), hits = [];
      for (const o of P.camObs) { const d = P.clearDistance(a, b, [o], 0.28, heightAt); if (d < FULL - 0.02) hits.push({ src: o.src, group: o.group, at: [r3(o.x), r3(-o.z)], size: [r3(o.w), r3(o.d)], top: r3(o.h), minY: o.minY ?? null, clear_m: r3(d) }); }
      hits.sort((x, y) => x.clear_m - y.clear_m);
      out.push({ label, mode: r.mode, end: r.end, yaw: r3(input.yaw), settled_distance: r3(settled), full: r3(FULL), ground_only_clear_m: r3(P.clearDistance(a, b, [], 0.28, heightAt)), first_hits: hits.slice(0, 6) }); await sleep(0);
    }
    setMode({}); await save('camera-cause.json', out); return out;
  }


  // ---------------------------------------------------------------------------------------------- pedestrian network (every edge of the slice, both directions, real controller)
  const SLICE_EXCLUDE = new Set(['N20']);       // batch 4: the service court node N33 is now inside the built slice       // nodes inside buildings or yards that P2-A does not build (market halls, workyard, reservation)
  async function testNetwork() {
    setMode({});
    const nodes = sceneData.nodes, rects = sceneData.rects, inRect = (x, n) => rects.some(([a, b, c, d]) => x >= a && x <= b && n >= c && n <= d);
    const nrec = {};
    for (const [k, [x, n, label]] of Object.entries(nodes)) {
      const inside = inRect(x, n) && !SLICE_EXCLUDE.has(k); const [sc, who] = sideClearance(x, -n);
      nrec[k] = { x, n, label, in_slice: inside, standable: !P.blocked(x, -n, P.walkObs), clearance_m: r3(sc), nearest: who, support_y: r3(heightAt(x, -n)) };
    }
    const edges = [];
    for (const [a, b, kind] of sceneData.edges) {
      if (!nrec[a]?.in_slice || !nrec[b]?.in_slice || kind === 'reserved link') continue;
      const res = [];
      for (const [p, q] of [[a, b], [b, a]]) {
        const key = (sceneData.edge_via?.[p + '-' + q] ? p + '-' + q : q + '-' + p), vv = sceneData.edge_via?.[key] || []; const via2 = key === p + '-' + q ? vv : [...vv].reverse();
        const r = runRoute(p + '>' + q, [[nodes[p][0], nodes[p][1]], ...via2, [nodes[q][0], nodes[q][1]]], { maxSeconds: 60 });
        res.push({ dir: p + '>' + q, seconds: r.seconds, stuck: r.stuck, min_camera_m: r.min_distance, share_below_3m: r.share_below_3m, min_side_clearance_m: r.min_side_clearance_m, min_side_with: r.min_side_with, end_error_m: r3(Math.hypot(r.end[0] - nodes[q][0], r.end[1] - nodes[q][1])) });
        await sleep(0);
      }
      edges.push({ a, b, kind, length_m: r3(Math.hypot(nodes[a][0] - nodes[b][0], nodes[a][1] - nodes[b][1])), results: res, pass: res.every((x) => x.stuck === 0 && x.end_error_m < 0.6) });
    }
    const out = { nodes: nrec, edges, summary: { nodes_in_slice: Object.values(nrec).filter((n) => n.in_slice).length, not_standable: Object.entries(nrec).filter(([, n]) => n.in_slice && !n.standable).map(([k]) => k),
      edges_tested: edges.length, edges_failed: edges.filter((e) => !e.pass).map((e) => e.a + '-' + e.b), min_node_clearance_m: r3(Math.min(...Object.values(nrec).filter((n) => n.in_slice).map((n) => n.clearance_m))) } };
    await save('network.json', out); return out;
  }

  // ---------------------------------------------------------------------------------------------- the four critical camera cases: with and without the character fade

  const bbox = new T.Box3(), corner = new T.Vector3();
  function coverage() {                                              // share of the viewport covered by the character's projected bounding box
    camera.updateMatrixWorld(true); bbox.setFromObject(character.root); let x0 = 9, x1 = -9, y0 = 9, y1 = -9;
    for (let i = 0; i < 8; i++) { corner.set(i & 1 ? bbox.max.x : bbox.min.x, i & 2 ? bbox.max.y : bbox.min.y, i & 4 ? bbox.max.z : bbox.min.z); const behind = corner.clone().applyMatrix4(camera.matrixWorldInverse).z > -0.05; if (behind) return 1; corner.project(camera); x0 = Math.min(x0, corner.x); x1 = Math.max(x1, corner.x); y0 = Math.min(y0, corner.y); y1 = Math.max(y1, corner.y); }
    const w = Math.max(0, Math.min(1, x1) - Math.max(-1, x0)), h = Math.max(0, Math.min(1, y1) - Math.max(-1, y0)); return (w * h) / 4;
  }
  function yawSweep(label, x, n, { startYaw = 0, seconds = 6.28 } = {}) {
    P.teleport(x, -n, startYaw); for (let i = 0; i < 40; i++) P.stepSim(DT); input.keys.clear();
    const d = [], a = [], cov = []; let t = 0, stuck = 0;
    const p0 = character.root.position.clone();
    while (t < seconds) { input.yaw += DT; P.stepSim(DT); t += DT; d.push(camDist()); a.push(P.fade.alpha); cov.push(coverage()); }
    const p1 = character.root.position; if (Math.hypot(p1.x - p0.x, p1.z - p0.z) > 0.05) stuck = 1;
    return { label, at: [x, n], min_camera_m: r3(Math.min(...d)), median_m: r3(pct(d, 0.5)), share_below_3m: r3(d.filter((v) => v < 3).length / d.length), share_below_1_5m: r3(d.filter((v) => v < 1.5).length / d.length), min_alpha: r3(Math.min(...a)), max_screen_coverage: r3(Math.max(...cov)), max_effective_coverage: r3(Math.max(...cov.map((c, i) => c * a[i]))), share_coverage_over_25pct: r3(cov.filter((c) => c > 0.25).length / cov.length), share_effective_over_25pct: r3(cov.filter((c, i) => c * a[i] > 0.25).length / cov.length), share_alpha_below_half: r3(a.filter((v) => v < 0.5).length / a.length), moved_while_turning: stuck };
  }
  async function testCameraCases() {
    const out = { fade_on: [], fade_off: [] };
    const cases = [
      ['tea veranda: N16 to N17 and back', () => [runRoute('tea N16>N17', ROUTES.tea_N16_N17.pts), runRoute('tea N17>N16', ROUTES.tea_N17_N16.pts)], [['N17 yaw sweep', 36.16, 62.24, Math.PI]]],
      ["merchants' inn: N38 to N11 and back, lane walks", () => [runRoute('inn N38>N11', ROUTES.inn_diagonal_N38_N11.pts), runRoute('inn N11>N38', ROUTES.inn_diagonal_N11_N38.pts), runRoute('inn lane S-N', ROUTES.inn_lane_south.pts)], [['N38 yaw sweep', -19.2, 41, 0.35], ['inn door, yaw sweep', -19.4, 45, 1.57]]],
      ['tower corner: A11 turret pass and hug', () => [runRoute('turret pass', ROUTES.turret_corner_pass.pts), runRoute('turret hug', ROUTES.turret_corner_hug.pts), runRoute('west cross street', ROUTES.junction_west_cross_street.pts)], [['turret foot yaw sweep', -3.6, 17.5, 0], ['cross street mouth yaw sweep', -9, 19.9, 1.57]]],
      ['exchange hall approach: stairs up, porch landing, stairs down', () => [runRoute('hall up', ROUTES.hall_stairs_up.pts), runRoute('hall porch', ROUTES.hall_porch_landing.pts), runRoute('hall down', ROUTES.hall_stairs_down.pts)], [['N08 yaw sweep', 0, 75, Math.PI], ['porch landing yaw sweep', 0, 77.4, 0]]],
    ];
    for (const on of [true, false]) {
      P.fade.on = on;
      for (const [label, runs, sweeps] of cases) {
        const rs = runs().map((r) => ({ route: r.label, seconds: r.seconds, stuck: r.stuck, min_camera_m: r.min_distance, p05_m: r.p05, median_m: r.median, share_below_3m: r.share_below_3m, pops: r.pops_over_0_5m, end_error: r.stuck }));
        // fade statistics across the runs come from a second pass that records alpha with the same routes
        const sw = sweeps.map(([l, x, n, y]) => yawSweep(l, x, n, { startYaw: y }));
        (on ? out.fade_on : out.fade_off).push({ case: label, routes: rs, sweeps: sw });
        await sleep(0);
      }
    }
    P.fade.on = true; await save('camera-cases.json', out); return out;
  }


  // live-camera screenshots of the critical cases, character fade off and on (same position, yaw and settled camera)
  async function testCameraShots() {
    const cases = [['tea-veranda-facing-out', 36.16, 62.24, Math.PI], ['inn-door-facing-away', -19.4, 45, 1.57], ['tower-foot-facing-east', -3.6, 17.5, 1.57], ['hall-porch-facing-out', 0, 77.4, Math.PI]];
    renderer.userSize = true; renderer.setSize(1280, 720, false); camera.aspect = 16 / 9; camera.fov = 60; camera.updateProjectionMatrix(); const rec = [];
    for (const [name, x, n, yaw] of cases) for (const on of [false, true]) {
      P.fade.on = on; setMode({}); P.teleport(x, -n, yaw); for (let i = 0; i < 90; i++) P.stepSim(DT);
      renderer.render(scene, camera); const b = await new Promise((r) => renderer.domElement.toBlob(r, 'image/png')); await save(`cam-${name}-fade-${on ? 'on' : 'off'}.png`, b);
      rec.push({ name, fade: on, camera_m: r3(camDist()), alpha: r3(P.fade.alpha), coverage: r3(coverage()) });
    }
    P.fade.on = true; renderer.userSize = false; P.resize(); await save('camera-shots.json', rec); return rec;
  }


  // ---------------------------------------------------------------------------------------------- P2-B batch 2: the Central Bazaar
  async function testBazaar() {
    setMode({}); const names = Object.keys(ROUTES).filter((k) => k.startsWith('bz_')); const out = [];
    for (const n of names) {
      const r = runRoute(n, ROUTES[n].pts, { maxSeconds: 120 }); const last = ROUTES[n].pts[ROUTES[n].pts.length - 1];
      out.push({ route: n, seconds: r.seconds, stuck: r.stuck, stuck_at: r.stuck_waypoints, end_error_m: r3(Math.hypot(r.end[0] - last[0], r.end[1] - last[1])), turns_over_60: r.turns_over_60, total_turn_deg: r.total_turn_deg, min_camera_m: r.min_distance, median_camera_m: r.median, share_below_3m: r.share_below_3m,
        min_side_clearance_m: r.min_side_clearance_m, min_side_with: r.min_side_with, min_side_at: r.min_side_at, pass: r.stuck === 0 && Math.hypot(r.end[0] - last[0], r.end[1] - last[1]) < 0.7 });
      await sleep(0);
    }
    await save('bazaar-routes.json', out); return out;
  }

  // ---------------------------------------------------------------------------------------------- P2-B batch 3: the artisan lane (D6) and the south gateway (D1)
  // Routes built from the scene data: the lane both ways, the cross-street vista to the potter's shop, the arrival court, a market -> lane -> court -> street -> market loop, and for each
  // new building a walk round its walls (both ways, 1.8 m off the wall) that exercises every corner, lean-to post and prop edge.
  async function testDistrict() {
    setMode({}); const N = sceneData.nodes, pt = (k) => [N[k][0], N[k][1]], out = [];
    const routes = {
      d6_lane_south_to_north: [pt('N35'), pt('N09'), pt('N42'), pt('N10'), pt('N43'), pt('N44'), pt('N11')],
      d6_lane_north_to_south: [pt('N11'), pt('N44'), pt('N43'), pt('N10'), pt('N42'), pt('N09'), pt('N35')],
      d6_cross_street_vista: [pt('N03'), pt('N10'), pt('N43'), pt('N10'), pt('N03')],
      d1_arrival_court: [pt('N01'), pt('N45'), pt('N01'), pt('N46'), pt('N01'), pt('N02')],
      d6_workyard: [pt('N11'), pt('N40'), pt('N11')],
      loop_market_lane_court_street_market: [pt('N04'), pt('N11'), pt('N09'), pt('N35'), pt('N01'), pt('N02'), pt('N03'), pt('N04')],
      loop_market_lane_street_via_cross: [pt('N11'), pt('N10'), pt('N03'), pt('N13'), pt('N14'), pt('N04'), pt('N11')],
      // batch 4: the Eastern Trade Quarter and the tea route
      d7_lane_south_to_north: [pt('N36'), pt('N12'), pt('N47'), pt('N13'), pt('N50'), pt('N14')],
      d7_lane_north_to_south: [pt('N14'), pt('N50'), pt('N13'), pt('N47'), pt('N12'), pt('N36')],
      d7_bazaar_to_warehouse_gable: [pt('N04'), pt('N14'), pt('N50'), pt('N13'), pt('N47')],
      d7_court_loading_bays: [pt('N13'), pt('N33'), pt('N48'), pt('N33'), pt('N13')],
      d7_court_counting_loggia: [pt('N13'), pt('N33'), pt('N49'), pt('N33'), pt('N13')],
      d7_counting_house_lane_door: [pt('N14'), pt('N50'), pt('N14')],
      d7_court_to_path_to_terrace: [pt('N33'), pt('N51'), pt('N52'), pt('N53'), [32.6, 46.8], pt('N54'), pt('N59'), pt('N16')],
      d7_terrace_to_path_to_court: [pt('N16'), pt('N59'), pt('N54'), [32.6, 46.8], pt('N53'), pt('N52'), pt('N51'), pt('N33')],
      d8_tea_lane_e05_front: [pt('N24'), pt('N41'), pt('N16'), pt('N41'), pt('N24')],
      d8_e05_side_door_from_bazaar: [pt('N39'), pt('N58'), pt('N24'), pt('N58'), pt('N39')],
      d8_e05_east_door: [pt('N16'), pt('N59'), pt('N54'), pt('N59'), pt('N16')],
      loop_exploration_east: [pt('N04'), pt('N14'), pt('N13'), pt('N33'), pt('N51'), pt('N52'), pt('N53'), [32.6, 46.8], pt('N54'), pt('N59'), pt('N16'), pt('N41'), pt('N24'), pt('N39'), pt('N14'), pt('N04')],
      loop_exploration_east_reverse: [pt('N04'), pt('N14'), pt('N39'), pt('N24'), pt('N41'), pt('N16'), pt('N59'), pt('N54'), [32.6, 46.8], pt('N53'), pt('N52'), pt('N51'), pt('N33'), pt('N13'), pt('N14'), pt('N04')],
      // batch 5: the Civic Terrace and its tower houses
      d4_bazaar_to_assay_door: [pt('N04'), pt('N05'), pt('N30'), pt('N27'), pt('N06'), [-7.5, 60.3], pt('N23'), pt('N60'), pt('N23'), [-7.5, 60.3], pt('N06')],
      d4_bazaar_to_chart_door: [pt('N27'), pt('N06'), [7.5, 60.3], pt('N24'), pt('N61'), pt('N24'), [7.5, 60.3], pt('N06')],
      d4_terrace_stairs_up_and_down: [pt('N05'), pt('N29'), pt('N27'), pt('N06'), pt('N07'), pt('N08'), pt('N07'), pt('N06')],
      d4_terrace_benches_loop: [pt('N06'), pt('N07'), pt('N21'), pt('N07'), pt('N22'), pt('N07'), pt('N06')],
      d4_plaza_around_both_towers: [pt('N06'), [-7.5, 60.3], pt('N23'), pt('N60'), pt('N23'), [-7.5, 60.3], pt('N06'), [7.5, 60.3], pt('N24'), pt('N61'), pt('N24'), [7.5, 60.3], pt('N06')],
      loop_bazaar_terrace_lookout_court_lane: [pt('N04'), pt('N05'), pt('N30'), pt('N27'), pt('N06'), pt('N07'), pt('N06'), [7.5, 60.3], pt('N24'), pt('N41'), pt('N16'), pt('N59'), pt('N54'), [32.6, 46.8], pt('N53'), pt('N52'), pt('N51'), pt('N33'), pt('N13'), pt('N14'), pt('N04')],
      loop_street_cross_east_court_lane: [pt('N03'), pt('N13'), pt('N33'), pt('N13'), pt('N12'), pt('N36'), pt('N01'), pt('N02'), pt('N03')],
    };
    // Circumnavigation: a grid search (0.3 m cells, free where the body keeps 0.12 m off every walk-blocking solid, the same test the controller applies) joins anchor points on all sides of a
    // building; the resulting polyline is then WALKED with the real controller and camera. This replaces fixed rectangles, which collided with neighbours and with each building's own goods.
    let box = [-34, -10, 16, 40]; const step = 0.3; let nx = Math.ceil((box[2] - box[0]) / step), nn = Math.ceil((box[3] - box[1]) / step), fcache = new Map();
    const setBox = (b) => { box = b; nx = Math.ceil((box[2] - box[0]) / step); nn = Math.ceil((box[3] - box[1]) / step); fcache = new Map(); };
    const isFree = (i, j) => { if (i < 0 || j < 0 || i >= nx || j >= nn) return false; const k = j * nx + i; let v = fcache.get(k); if (v === undefined) { v = sideClearance(box[0] + (i + 0.5) * step, -(box[1] + (j + 0.5) * step))[0] >= 0.12; fcache.set(k, v); } return v; };
    const cellOf = (p) => [Math.floor((p[0] - box[0]) / step), Math.floor((p[1] - box[1]) / step)], centre = (c) => [box[0] + (c[0] + 0.5) * step, box[1] + (c[1] + 0.5) * step];
    const snap = (p) => { const c = cellOf(p); for (let r = 0; r < 14; r++) for (let di = -r; di <= r; di++) for (let dj = -r; dj <= r; dj++) if (Math.max(Math.abs(di), Math.abs(dj)) === r && isFree(c[0] + di, c[1] + dj)) return [c[0] + di, c[1] + dj]; return null; };
    const los = (p, q) => { const L = Math.hypot(q[0] - p[0], q[1] - p[1]), k = Math.ceil(L / 0.15); for (let t = 0; t <= k; t++) { const c = cellOf([p[0] + (q[0] - p[0]) * t / k, p[1] + (q[1] - p[1]) * t / k]); if (!isFree(c[0], c[1])) return false; } return true; };
    const astar = (pa, pb) => {
      const a = snap(pa), b = snap(pb); if (!a || !b) return null; const key = (c) => c[1] * nx + c[0], g = new Map([[key(a), 0]]), from = new Map(), open = [[0, a]], closed = new Set();
      const h = (c) => Math.hypot(c[0] - b[0], c[1] - b[1]);
      while (open.length) {
        let bi = 0; for (let i = 1; i < open.length; i++) if (open[i][0] < open[bi][0]) bi = i; const [, c] = open.splice(bi, 1)[0]; const ck = key(c); if (closed.has(ck)) continue; closed.add(ck);
        if (c[0] === b[0] && c[1] === b[1]) { const path = [c]; let k = ck; while (from.has(k)) { const pc = from.get(k); path.unshift(pc); k = key(pc); } const pts = path.map(centre), out = [pts[0]]; let anchor = 0;
          for (let i = 2; i < pts.length; i++) if (!los(pts[anchor], pts[i])) { out.push(pts[i - 1]); anchor = i - 1; } out.push(pts[pts.length - 1]); return out; }
        for (const [di, dj] of [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]) { const n2 = [c[0] + di, c[1] + dj]; if (!isFree(n2[0], n2[1])) continue; if (di && dj && (!isFree(c[0] + di, c[1]) || !isFree(c[0], c[1] + dj))) continue;
          const ng = g.get(ck) + Math.hypot(di, dj); const nk = key(n2); if (ng < (g.get(nk) ?? 1e9)) { g.set(nk, ng); from.set(nk, c); open.push([ng + h(n2), n2]); } }
      }
      return null;
    };
    const via = (anchors) => { let out = []; for (let i = 1; i < anchors.length; i++) { const leg = astar(anchors[i - 1], anchors[i]); if (!leg) return null; out = out.concat(out.length ? leg.slice(1) : leg); } return out; };
    const SEARCH = { B10: [-34, -10, 16, 40], B11: [-34, -10, 16, 40], B12: [-34, -10, 16, 40], E01: [-34, -10, 16, 40], E02: [-34, -10, 16, 40], B13: [10, 0, 40, 40], E04: [10, 14, 40, 44], E05: [14, 38, 44, 66], B15: [-34, 52, -6, 82], B16: [6, 52, 34, 82] };
    for (const b of ['B10', 'B11', 'B12', 'E01', 'E02', 'B13', 'E04', 'B15', 'B16']) {
      setBox(SEARCH[b]);
      const w = P.obstacles.filter((o) => o.src === b && o.group === 'wall' && !o.cameraOnly); if (!w.length) continue;
      const x0 = Math.min(...w.map((o) => o.x - o.w / 2)), x1 = Math.max(...w.map((o) => o.x + o.w / 2)), n0 = Math.min(...w.map((o) => -o.z - o.d / 2)), n1 = Math.max(...w.map((o) => -o.z + o.d / 2)), mx = (x0 + x1) / 2, mn = (n0 + n1) / 2, m = 2.2;
      const front = (b === 'E02' || b === 'B13' || b === 'E04') ? [x0 - m, mn] : (b === 'B15' || b === 'B16') ? [mx, n0 - m] : [x1 + m, mn], back = (b === 'E02' || b === 'B13' || b === 'E04') ? [x1 + m, mn] : (b === 'B15' || b === 'B16') ? [mx, n1 + m] : [x0 - m, mn];          // the artisan row and E01 face east, E02, B13 and E04 face west (E05 faces north: its anchors are just the four sides)
      const north = [mx, n1 + m], south = [mx, n0 - m];
      for (const [dir, anchors] of [['ccw', [front, north, back, south, front]], ['cw', [front, south, back, north, front]]]) { const pts = via(anchors); if (pts) routes[b + '_walk_round_' + dir] = pts; else out.push({ route: b + '_walk_round_' + dir, pass: false, error: 'no free path between the anchors (the building cannot be circumnavigated at 0.12 m clearance)' }); }
    }
    // batch 4: E05 stands in a block with E06 and B14; its 2.2 m south slot is closed by two fences, so it has no ring walk (the exploration loops loop_exploration_east* circle the block instead)
    for (const [name, pts] of Object.entries(routes)) {
      const r = runRoute(name, pts, { maxSeconds: 160 }), last = pts[pts.length - 1];
      out.push({ route: name, seconds: r.seconds, stuck: r.stuck, stuck_at: r.stuck_waypoints, end_error_m: r3(Math.hypot(r.end[0] - last[0], r.end[1] - last[1])), turns_over_60: r.turns_over_60, total_turn_deg: r.total_turn_deg, min_camera_m: r.min_distance, median_camera_m: r.median, share_below_3m: r.share_below_3m,
        min_side_clearance_m: r.min_side_clearance_m, min_side_with: r.min_side_with, min_side_at: r.min_side_at, min_alpha: r.min_alpha, share_faded_below_0_9: r.share_faded_below_0_9, pass: r.stuck === 0 && Math.hypot(r.end[0] - last[0], r.end[1] - last[1]) < 0.7 });
      await sleep(0);
    }
    await save('district-routes.json', out); return out.map(({ route, seconds, stuck, stuck_at, end_error_m, min_camera_m, pass, min_side_clearance_m, min_side_with }) => ({ route, seconds, stuck, stuck_at, end_error_m, min_camera_m, min_side_clearance_m, min_side_with, pass }));
  }

  // no-penetration test for every solid of the two halls and the new shops: walk at each one from every free direction and check the body never ends inside its footprint
  async function testMerchandise() {
    const rows = [], srcs = new Set(['B02', 'B03', 'B14', 'E06', 'E07', 'B10', 'B11', 'B12', 'E01', 'E02', 'B13', 'E04', 'E05', 'B15', 'B16', 'TERRACE', 'dressing']); setMode({});
    for (const o of P.obstacles) {
      if (o.cameraOnly || !srcs.has(o.src)) continue;
      const ext = Math.max(o.w, o.d) / 2 + 1.3; let tried = 0, worst = 99, ok = true, dirs = [];
      for (const deg of [0, 45, 90, 135, 180, 225, 270, 315]) {
        const a = deg * Math.PI / 180, sx = o.x + Math.sin(a) * ext, sz = o.z + Math.cos(a) * ext; if (P.blocked(sx, sz, P.walkObs)) continue;
        P.teleport(sx, sz, Math.atan2(-(o.x - sx), -(o.z - sz))); for (let i = 0; i < 10; i++) P.stepSim(DT); input.keys.clear(); input.keys.add('w');
        for (let i = 0; i < 150; i++) { input.yaw = Math.atan2(-(o.x - character.root.position.x), -(o.z - character.root.position.z)); P.stepSim(DT); }
        input.keys.clear(); const p = character.root.position, d = distToObstacle(p.x, p.z, o) - 0.34; worst = Math.min(worst, d); tried++; dirs.push(deg); if (d < -0.05) ok = false;
      }
      rows.push({ src: o.src, group: o.group, at: [r3(o.x), r3(-o.z)], size: [r3(o.w), r3(o.d)], top: r3(o.h), approaches: tried, worst_penetration_m: r3(worst === 99 ? null : worst), blocked_correctly: tried > 0 && ok, untestable: tried === 0 });
      await sleep(0);
    }
    const summary = { solids: rows.length, tested: rows.filter((r) => !r.untestable).length, passed: rows.filter((r) => r.blocked_correctly).length, failed: rows.filter((r) => !r.untestable && !r.blocked_correctly).map((r) => r.src + ':' + r.group + '@' + r.at), untestable: rows.filter((r) => r.untestable).length,
      posts_in_camera_list: P.camObs.filter((o) => o.group === 'post').length, posts_in_walk_list: P.walkObs.filter((o) => o.group === 'post' && !o.cameraOnly).length };
    await save('merchandise-collision.json', { summary, rows }); return summary;
  }

  // covered-hall camera: 360-degree turns at the aisle ends and centres, entering and leaving, fade on and off
  async function testHallCamera() {
    renderer.userSize = true; renderer.setSize(1280, 720, false); camera.aspect = 16 / 9; camera.updateProjectionMatrix();     // batch 4: a fixed 1280 x 720 viewport (screen-coverage fractions depend on the aspect ratio, which followed the size of the browser pane before)
    const out = { fade_on: [], fade_off: [] };
    const spots = [['West hall centre', -13, 50], ['West hall aisle south', -13, 45], ['West hall aisle north', -13, 54.5], ['East hall centre', 13, 50], ['East hall aisle south', 13, 45], ['East hall aisle north', 13, 54.5], ['West hall east side opening', -9.4, 49], ['East hall west side opening', 9.4, 49], ['Lane at the smithy forge bay', -16.3, 7.2], ['Lane at the smithy door', -16.3, 10.9], ['Lane at the potter', -16.0, 19.8], ['Lane at the joiner', -15.7, 29.7], ['Cross street, B11 end', -13, 20], ['Alley B11-B12 mouth', -17.5, 24.5], ['Alley B11-B12 middle', -22, 24.5], ['Alley B10-B11 middle', -21.5, 15.7], ['Workyard', -20.1, 35.4], ['Arrival court by E01', -6.1, 2.0], ['Arrival court by E02', 5.8, 2.5],
      ['Lane at B13 gable doors', 16.0, 12.0], ['Lane at the counting house', 16.0, 29.0], ['Court centre', 25.0, 20.0], ['Court by the loading bays', 28.6, 19.0], ['Court by the tally loggia', 23.5, 21.3], ['Court east opening', 32.5, 20.0], ['Porters path behind E04', 33.0, 30.0], ['Porters path gate', 31.0, 50.0], ['Tea lane in front of E05', 26.0, 59.0], ['East market lane by E05', 19.7, 54.5], ['Lookout terrace west end', 31.3, 53.8]];
    for (const on of [true, false]) { P.fade.on = on; for (const [l, x, n] of spots) (on ? out.fade_on : out.fade_off).push(yawSweep(l, x, n, { startYaw: 0 })); await sleep(0); }
    P.fade.on = true; renderer.userSize = false; P.resize(); out.viewport = [1280, 720]; await save('hall-camera.json', out); return out;
  }

  // ---------------------------------------------------------------------------------------------- P2-B batch 4: which obstacles compress the camera next to the new buildings
  // Stationary 360-degree turns (24 yaw steps, camera settled for 1.5 s each) at 1.8 m off every wall midpoint and corner of B13, E04, E05 (and, for comparison, B10, B12, E01 of batch 3). For each yaw the camera ray
  // (head anchor to full follow distance) is tested against every camera obstacle separately, so the compression is attributed to the obstacle group that causes it (roof proxy, wall, overhang, prop, post, balcony, cloth ...).
  let reachGrid = null;                                              // flood fill (0.3 m cells, body-radius test of the controller) from the arrival court: which free spots can a player actually walk to
  const reachable = (x, n) => {
    if (!reachGrid) {
      const x0 = -45, n0 = -12, st = 0.3, nx = Math.ceil(95 / st), nn = Math.ceil(88 / st), free = new Uint8Array(nx * nn), seen = new Uint8Array(nx * nn);
      for (let j = 0; j < nn; j++) for (let i = 0; i < nx; i++) free[j * nx + i] = P.blocked(x0 + (i + 0.5) * st, -(n0 + (j + 0.5) * st), P.walkObs) ? 0 : 1;
      const start = [Math.floor((0 - x0) / st), Math.floor((5 - n0) / st)], stack = [start[1] * nx + start[0]]; seen[stack[0]] = 1;
      while (stack.length) { const k = stack.pop(), i = k % nx, j = (k - i) / nx; for (const [di, dj] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) { const a = i + di, b = j + dj; if (a < 0 || b < 0 || a >= nx || b >= nn) continue; const kk = b * nx + a; if (free[kk] && !seen[kk]) { seen[kk] = 1; stack.push(kk); } } }
      reachGrid = { x0, n0, st, nx, nn, seen };
    }
    const g = reachGrid, i = Math.floor((x - g.x0) / g.st), j = Math.floor((n - g.n0) / g.st); return i >= 0 && j >= 0 && i < g.nx && j < g.nn && g.seen[j * g.nx + i] === 1;
  };
  async function testCompression() {
    setMode({}); const out = { fade_on_note: 'raw camera distance, not opacity', buildings: {} }, buildings = ['B15', 'B16', 'B13', 'E04', 'E05', 'B10', 'B12', 'E01'];
    for (const b of buildings) {
      const w = P.obstacles.filter((o) => o.src === b && o.group === 'wall' && !o.cameraOnly); if (!w.length) continue;
      const x0 = Math.min(...w.map((o) => o.x - o.w / 2)), x1 = Math.max(...w.map((o) => o.x + o.w / 2)), n0 = Math.min(...w.map((o) => -o.z - o.d / 2)), n1 = Math.max(...w.map((o) => -o.z + o.d / 2)), mx = (x0 + x1) / 2, mn = (n0 + n1) / 2, m = 1.8;
      const spots = [['W', x0 - m, mn], ['E', x1 + m, mn], ['S', mx, n0 - m], ['N', mx, n1 + m], ['SW', x0 - m, n0 - m], ['SE', x1 + m, n0 - m], ['NW', x0 - m, n1 + m], ['NE', x1 + m, n1 + m]];
      const rows = [], byGroup = {}; let all = [];
      for (const [side, sx, sn] of spots) {
        if (P.blocked(sx, -sn, P.walkObs)) { rows.push({ side, at: [r3(sx), r3(sn)], blocked: true }); continue; }
        if (!reachable(sx, sn)) { rows.push({ side, at: [r3(sx), r3(sn)], enclosed: true, note: 'free but not reachable on foot from the arrival court (closed by fences/walls): not a player position' }); continue; }
        P.teleport(sx, -sn, 0); for (let i = 0; i < 40; i++) P.stepSim(DT); input.keys.clear(); const d = [], causes = {};
        for (let k = 0; k < 24; k++) {
          input.yaw = k * Math.PI / 12; for (let i = 0; i < 90; i++) P.stepSim(DT);
          const dist = camDist(); d.push(dist); const p = character.root.position, a = new T.Vector3(p.x, p.y + 1.25, p.z), dir = camera.position.clone().sub(a).normalize(), bb = a.clone().addScaledVector(dir, FULL);
          let best = null, bd = FULL; for (const o of P.camObs) { const c = P.clearDistance(a, bb, [o], 0.28, heightAt); if (c < bd - 0.02) { bd = c; best = o; } }
          if (dist < 3) { const g = best ? best.group + (best.src && best.src !== b ? ' of ' + best.src : '') : 'ground'; causes[g] = (causes[g] || 0) + 1; byGroup[g] = (byGroup[g] || 0) + 1; }
        }
        all = all.concat(d); rows.push({ side, at: [r3(sx), r3(sn)], min_camera_m: r3(Math.min(...d)), median_m: r3(pct(d, 0.5)), share_below_3m: r3(d.filter((v) => v < 3).length / d.length), share_below_1_5m: r3(d.filter((v) => v < 1.5).length / d.length), causes_below_3m: causes });
        await sleep(0);
      }
      out.buildings[b] = { spots: rows, share_below_3m: r3(all.filter((v) => v < 3).length / (all.length || 1)), share_below_1_5m: r3(all.filter((v) => v < 1.5).length / (all.length || 1)), min_camera_m: r3(Math.min(...all)), causes_all_spots: byGroup, samples: all.length };
    }
    // the walkable nodes and lane spots of the quarter (the places a player actually stands), same attribution
    const named = [['Lane at B13 gable doors', 16.0, 12.0], ['Lane at the counting house', 16.0, 29.0], ['Court centre', 25.0, 20.0], ['Court by the loading bays', 28.6, 19.0], ['Court by the tally loggia', 23.5, 21.3], ['Court east opening', 32.5, 20.0], ['Porters path behind E04', 33.0, 30.0], ['Porters path behind the east shops', 33.0, 41.0], ['Porters path gate', 31.0, 50.0], ['Tea lane in front of E05', 26.0, 59.0], ['East market lane by E05', 19.7, 54.5], ['Lookout terrace west end', 31.3, 54.5], ['Assay office door (B15)', -19.0, 60.8], ['Chart maker door (B16)', 19.0, 60.8], ['Terrace stair foot', 0, 60.0], ['Terrace centre', 0, 68.0], ['Terrace by the west tower', -11.0, 66.0], ['Terrace by the east tower', 11.0, 66.0], ['Hall steps foot', 0, 74.5], ['Bazaar NW plaza', -17.0, 58.0], ['Bazaar NE plaza', 17.0, 58.0]];
    out.named_spots = [];
    for (const [label, sx, sn] of named) {
      P.teleport(sx, -sn, 0); for (let i = 0; i < 40; i++) P.stepSim(DT); input.keys.clear(); const d = [], causes = {};
      for (let k = 0; k < 24; k++) {
        input.yaw = k * Math.PI / 12; for (let i = 0; i < 90; i++) P.stepSim(DT);
        const dist = camDist(); d.push(dist); const p = character.root.position, a = new T.Vector3(p.x, p.y + 1.25, p.z), dir = camera.position.clone().sub(a).normalize(), bb = a.clone().addScaledVector(dir, FULL);
        let best = null, bd = FULL; for (const o of P.camObs) { const c = P.clearDistance(a, bb, [o], 0.28, heightAt); if (c < bd - 0.02) { bd = c; best = o; } }
        if (dist < 3) { const g = best ? best.group + ' of ' + best.src : 'ground'; causes[g] = (causes[g] || 0) + 1; }
      }
      out.named_spots.push({ label, at: [sx, sn], min_camera_m: r3(Math.min(...d)), median_m: r3(pct(d, 0.5)), share_below_3m: r3(d.filter((v) => v < 3).length / d.length), share_below_1_5m: r3(d.filter((v) => v < 1.5).length / d.length), causes_below_3m: causes });
      await sleep(0);
    }
    await save('compression-cause.json', out); return Object.fromEntries(Object.entries(out.buildings).map(([k, v]) => [k, { share_below_3m: v.share_below_3m, share_below_1_5m: v.share_below_1_5m, min_camera_m: v.min_camera_m, causes: v.causes_all_spots }]));
  }

  // the character fade in motion: a frame strip and an opacity/distance trace while walking into the West hall, turning at the north end and leaving
  async function testFadeMotion() {
    renderer.userSize = true; renderer.setSize(640, 360, false); camera.aspect = 16 / 9; camera.updateProjectionMatrix(); setMode({}); P.fade.on = true;
    const seqs = [['hall-walk', [[-16, 38.5], [-13, 42.5], [-13, 52], [-15, 55.0], [-11, 55.0], [-13, 46], [-13, 41.5]]], ['porch-steps', [[0, 59.4], [0, 67], [0, 75], [0, 75.6], [0, 75], [0, 67], [0, 59.4]]], ['tea-veranda', [[36, 57], [36.16, 62.24], [36.16, 61.0], [36, 57]]], ['lane-walk', [[-16, 4], [-16.3, 10.9], [-16, 19.8], [-15.7, 29.7], [-16, 38.5]]], ['vista-and-turn', [[-3.5, 20], [-13, 20], [-16, 19.8], [-16, 25], [-15.7, 29.7], [-16, 20], [-6, 20]]], ['workyard-turn', [[-16, 38.5], [-20.1, 35.4], [-23, 36.5], [-20.1, 35.4], [-16, 38.5]]],
      // batch 4
      ['east-lane-court', [[16, 4], [16, 12], [16, 20], [25, 20], [28.5, 19.4], [25, 20], [23.5, 21.3], [25, 20], [33, 20]]], ['terrace-approach', [[0, 52.5], [0, 59.4], [0, 67], [0, 75], [0, 67], [-9.5, 68], [0, 67], [9.5, 68], [0, 59.4]]], ['tower-doors', [[-13, 58.6], [-19, 60.8], [-17, 58.6], [17, 58.6], [19, 60.8], [13, 58.6]]], ['porters-path', [[33, 20], [33, 41], [32.6, 46.8], [31, 50], [31.3, 54.5], [36, 57]]],
      ['tea-lane-e05', [[19.2, 41], [19.7, 54.5], [19.2, 58.6], [26, 59], [36, 57], [26, 59], [19.2, 58.6]]]];
    const all = {};
    for (const [name, pts] of seqs) {
      const trace = []; let frame = 0, t = 0;
      P.teleport(pts[0][0], -pts[0][1], Math.atan2(-(pts[1][0] - pts[0][0]), (pts[1][1] - pts[0][1]))); for (let i = 0; i < 40; i++) P.stepSim(DT);
      for (let wp = 1; wp < pts.length; wp++) {
        const [tx, tn] = pts[wp]; let lim = 0;
        while (lim++ < 900) {
          const p = character.root.position, dx = tx - p.x, dz = -tn - p.z; if (Math.hypot(dx, dz) < 0.45) break;
          const want = Math.atan2(-dx, -dz), diff = Math.atan2(Math.sin(want - input.yaw), Math.cos(want - input.yaw)); input.yaw += Math.max(-2.4 * DT, Math.min(2.4 * DT, diff)); input.keys.add('w');
          P.stepSim(DT); t += DT; trace.push([r3(t), r3(p.x), r3(-p.z), r3(camDist()), r3(P.fade.alpha)]);
          if (Math.round(t * 60) % 30 === 0) { renderer.render(scene, camera); const b = await new Promise((r) => renderer.domElement.toBlob(r, 'image/png')); await save(`fademotion-${name}-${String(frame++).padStart(2, '0')}.png`, b); }
        }
      }
      input.keys.clear(); const a = trace.map((r) => r[4]), d = trace.map((r) => r[3]);
      all[name] = { frames: frame, seconds: r3(t), min_alpha: Math.min(...a), min_camera_m: Math.min(...d), share_faded_below_0_9: r3(a.filter((v) => v < 0.9).length / a.length), max_alpha_change_per_frame: r3(Math.max(...a.slice(1).map((v, i) => Math.abs(v - a[i])))), trace_10hz: trace.filter((_, i) => i % 6 === 0) };
    }
    renderer.userSize = false; P.resize(); await save('fade-motion.json', all);
    return Object.fromEntries(Object.entries(all).map(([k, v]) => [k, { frames: v.frames, seconds: v.seconds, min_alpha: v.min_alpha, min_camera_m: v.min_camera_m, share_faded: v.share_faded_below_0_9, max_step: v.max_alpha_change_per_frame }]));
  }

  // Batch 5: explicit pass criteria. Batch 4's autotest-suite.json showed "7 runs, 0 pass" because the suite counted a `pass` field that the records never had; the records are not wrong, the aggregation was.
  // Criteria, written before the re-run and not adjusted to the results (the expected heights come from the design: terrace +1.0 m, hall podium +2.0 m, paving +0.01 m):
  //   stairs (walk, run, jump): ends within 0.7 m of the target in n; ends at the expected height +-0.05 m AND on the support height the heightfield reports there; never stuck (no 60 frames without progress);
  //   never airborne on stairs when walking or running (jump run: exactly one jump); no single-frame rise above 0.45 m (the controller's step is 0.42 m) and no single-frame drop below -0.45 m;
  //   edge drop: starts on the terrace (y 1.01 +-0.05), falls, ends on the ground at 0.01 +-0.05 within 2.5 s and is grounded; side wall: never rises above its start height +0.05 m and stays on the ground side of the wall.
  async function testPlatform() {
    setMode({});
    const out = { criteria: 'see the comment above testPlatform in p2a-tests.js and 03 of batch 5', runs: [] };
    const climb = (label, from, to, expectEndY, { run = false, jumpAt = null } = {}) => {
      const [x, n0] = from; P.teleport(x, -n0, 0); for (let i = 0; i < 30; i++) P.stepSim(DT);
      input.keys.clear(); input.keys.add('w'); if (run) input.keys.add('shift'); input.yaw = to[1] > n0 ? 0 : Math.PI;
      const trace = []; let t = 0, prevY = character.root.position.y, maxUp = 0, maxDown = 0, airborne = 0, jumps = 0, minCam = 99, blockedSteps = 0, prevN = n0, still = 0;
      while (t < 40) {
        const p = character.root.position, n = -p.z;
        if ((to[1] > n0 && n >= to[1]) || (to[1] < n0 && n <= to[1])) break;
        const jn = jumpAt && Math.abs(n - jumpAt) < 0.05 && !jumps; if (jn) jumps++;
        P.stepSim(DT, !!jn); t += DT;
        const dy = p.y - prevY; maxUp = Math.max(maxUp, dy); maxDown = Math.min(maxDown, dy); prevY = p.y;
        if (!P.sim.motion.grounded) airborne++;
        if (Math.abs(n - prevN) < 0.0005) still++; else still = 0; prevN = n; if (still > 60) { blockedSteps = still; break; }
        minCam = Math.min(minCam, camDist());
        if (Math.round(t * 60) % 6 === 0) trace.push([r3(t), r3(n), r3(p.y), P.sim.motion.phase]);
      }
      input.keys.clear(); const p = character.root.position, support = heightAt(p.x, p.z), endN = -p.z;
      const c = { arrived: Math.abs(endN - to[1]) < 0.7 + (jumpAt ? 0 : 0) || (to[1] > n0 ? endN >= to[1] : endN <= to[1]), height_expected: Math.abs(p.y - expectEndY) <= 0.05, on_support: Math.abs(p.y - support) <= 0.05, not_stuck: blockedSteps === 0,
        no_airborne_on_stairs: jumpAt ? jumps === 1 : airborne === 0, step_up_ok: maxUp <= 0.45, step_down_ok: maxDown >= -0.45 };
      out.runs.push({ label, kind: 'stairs', from, to, seconds: r3(t), end_n: r3(endN), end_y: r3(p.y), expected_end_y: expectEndY, support_y: r3(support), max_step_up_m: r3(maxUp), max_step_down_m: r3(maxDown), airborne_steps: airborne, jumps, min_camera_distance: r3(minCam), stuck_steps: blockedSteps, criteria: c, pass: Object.values(c).every(Boolean), trace });
    };
    climb('ascend terrace steps then hall steps, walking (to the forecourt rail)', [0, 56], [0, 75.5], 2.01);
    climb('descend hall steps then terrace steps, walking', [0, 75.6], [0, 56], 0.01);
    climb('ascend both flights, running (to the forecourt rail)', [0, 56], [0, 75.5], 2.01, { run: true });
    climb('descend both flights, running', [0, 75.6], [0, 56], 0.01, { run: true });
    climb('ascend terrace steps with a jump on the third riser', [0, 56], [0, 70], 1.01, { jumpAt: 61.2 });
    const edge = (label, x, n, yaw, seconds, check) => {
      P.teleport(x, -n, yaw); for (let i = 0; i < 30; i++) P.stepSim(DT); input.keys.clear(); const y0 = character.root.position.y, x0 = character.root.position.x, n0 = -character.root.position.z; input.keys.add('w'); const tr = []; let minY = 9, maxY = -9, phases = new Set(), t = 0;
      while (t < seconds) { P.stepSim(DT); t += DT; const p = character.root.position; minY = Math.min(minY, p.y); maxY = Math.max(maxY, p.y); phases.add(P.sim.motion.phase); if (Math.round(t * 60) % 6 === 0) tr.push([r3(t), r3(p.x), r3(-p.z), r3(p.y), P.sim.motion.phase]); }
      input.keys.clear(); for (let i = 0; i < 30; i++) P.stepSim(DT); const p = character.root.position; const c = check({ y0, x0, n0, endX: p.x, endN: -p.z, endY: p.y, minY, maxY, grounded: !!P.sim.motion.grounded });
      out.runs.push({ label, kind: 'edge', start: [r3(x0), r3(n0), r3(y0)], end: [r3(p.x), r3(-p.z), r3(p.y)], min_y: r3(minY), max_y: r3(maxY), phases: [...phases], criteria: c, pass: Object.values(c).every(Boolean), trace: tr });
    };
    edge('walk off the terrace edge (south side, west of the steps): a 1 m drop', -9, 63.0, Math.PI, 2.5, (r) => ({ started_on_terrace: Math.abs(r.y0 - 1.01) <= 0.05, fell_to_ground: Math.abs(r.endY - 0.01) <= 0.05, grounded: r.grounded, left_the_terrace: Math.abs(r.endN - r.n0) > 0.5 }));
    edge('walk east into the terrace side from the ground (n 72.5, north of B15): must not climb, body must stop 0.34 m from the edge', -17, 72.5, -Math.PI / 2, 3.0, (r) => ({ never_rose: r.maxY <= r.y0 + 0.05, stayed_on_ground_side: r.endX <= -14.34 + 0.03, grounded: r.grounded }));
    out.summary = { runs: out.runs.length, passed: out.runs.filter((r) => r.pass).length, failed: out.runs.filter((r) => !r.pass).map((r) => r.label) };
    await save('platform-test.json', out);
    return { summary: out.summary, runs: out.runs.map(({ trace, ...r }) => r) };
  }

  async function capture(name, { w = 1600, h = 900 } = {}) {
    const v = sceneData.views[name]; if (!v) return null;
    renderer.userSize = true; renderer.setSize(w, h, false); camera.aspect = w / h; camera.fov = v.fov; camera.updateProjectionMatrix();
    P.setCharacterAt(v.who); P.fade.mats.forEach((m) => { m.opacity = 1; });
    camera.position.set(...v.pos); camera.lookAt(...v.look); camera.updateMatrixWorld(true);
    renderer.render(scene, camera);
    const blob = await new Promise((res) => renderer.domElement.toBlob(res, 'image/png'));
    await save('shot-' + name + (new URLSearchParams(location.search).get('shot') ? '-' + new URLSearchParams(location.search).get('shot') : '') + '.png', blob);
    return { name, bytes: blob.size };
  }
  P.setCharacterAt = (who) => { const root = character.root; if (who) { root.visible = true; root.position.set(who[0], heightAt(who[0], -who[1]), -who[1]); root.rotation.y = Math.PI; } else root.visible = false; };
  async function testViews(names) {
    const qn = (new URLSearchParams(location.search).get('names') || '').split(',').filter(Boolean); const list = names || (qn.length ? qn : Object.keys(sceneData.views).filter((k) => ['view-b-merchant-street', 'view-b2-merchant-street-eye', 'view-c2-bazaar-eye', 'view-g-bazaar-from-terrace', 'view-f-tea-route', 'view-d-exchange-court', 'p2b-hall-aerial', 'p2b-hall-porch', 'p2b-hall-tower', 'p2b-junction-fixed', 'p3-bazaar-aerial', 'p3-aisle-eye', 'p3-west-entrance', 'p3-east-entrance', 'p3-west-interior', 'p3-east-interior', 'p3-axis-to-hall', 'p3-shops-east', 'p3-shop-e07', 'view-c-central-bazaar', 'view-c2-bazaar-eye', 'p2a-aerial', 'p2a-junction', 'p2a-inn', 'p2a-terrace', 'p2a-tea'].includes(k)));
    P.sim.frozenCamera = true; const res = [];
    for (const n of list) { res.push(await capture(n)); await sleep(0); }
    // the live follow camera at the same place, for the gameplay-camera view
    renderer.userSize = true; renderer.setSize(1600, 900, false); camera.aspect = 1600 / 900; camera.fov = 60; camera.updateProjectionMatrix(); P.sim.frozenCamera = false;
    P.setCharacterAt(null); character.root.visible = true; P.teleport(0, -36, 0); for (let i = 0; i < 60; i++) P.stepSim(DT);
    renderer.render(scene, camera); const b = await new Promise((r) => renderer.domElement.toBlob(r, 'image/png')); await save('shot-live-follow-camera-bazaar.png', b); res.push({ name: 'live follow camera', camera: camera.position.toArray().map(r3) });
    renderer.userSize = false; P.resize();
    return res;
  }

  // static batching, to measure what a merged-by-material town costs

  function countScene() {
    let meshes = 0, tris = 0, draws = 0;
    scene.traverseVisible((o) => { if (!o.isMesh || o === P.ground || !o.visible) return; if (o.parent?.name === 'GROUND') return; const g = o.geometry, c = (g.index ? g.index.count : g.attributes.position.count) / 3, inst = o.isInstancedMesh ? o.count : 1; meshes += inst; tris += c * inst; draws += 1; });
    return { visible_mesh_instances: meshes, scene_triangles: Math.round(tris), draw_calls_expected: draws };
  }

  async function measure({ shadows = true, merged = false, w = 1280, h = 720, frames = Number(new URLSearchParams(location.search).get('pframes') || 240) } = {}) {
    P.setShadows(shadows); P.setMerged(merged); renderer.userSize = true; renderer.setSize(w, h, false); camera.aspect = w / h; camera.fov = 60; camera.updateProjectionMatrix(); P.sim.frozenCamera = false;
    setMode({}); P.teleport(0, -4, 0); input.keys.clear();
    for (let i = 0; i < 30; i++) { P.stepSim(DT); }
    renderer.info.reset(); const firstT0 = performance.now(); renderer.render(scene, camera); hardSync(); const first_render_ms = performance.now() - firstT0; const info = { calls: renderer.info.render.calls, triangles: renderer.info.render.triangles, lines: renderer.info.render.lines, points: renderer.info.render.points };
    const gl = renderer.getContext();
    // (1) a 60 Hz walk down the street with the real controller and camera; every frame is simulated, rendered and waited for (gl.finish)
    const intervals = [], cpu = []; let pts = ROUTES.street_axis.pts, wp = 1; input.keys.add('w'); const alive = () => document.visibilityState;
    P.paused = true;
    for (let f = 0; f < frames; f++) {
      const f0 = performance.now();
      const p = character.root.position, [tx, tn] = pts[wp]; if (Math.hypot(tx - p.x, -tn - p.z) < 0.6 && wp < pts.length - 1) wp++;
      const want = Math.atan2(-(tx - p.x), -(-tn - p.z)); const diff = Math.atan2(Math.sin(want - input.yaw), Math.cos(want - input.yaw)); input.yaw += Math.max(-0.04, Math.min(0.04, diff));
      P.stepSim(DT); const c0 = performance.now(); renderer.render(scene, camera); cpu.push(performance.now() - c0); hardSync(); intervals.push(performance.now() - f0);
      if (f % 20 === 0) await sleep();
    }
    input.keys.clear();
    // (2) unthrottled throughput: render back to back and wait for the GPU each time
    const sync = []; for (let i = 0; i < Math.min(90, frames); i++) { const s = performance.now(); renderer.render(scene, camera); hardSync(); sync.push(performance.now() - s); }
    const stat = (a) => ({ mean: r3(a.reduce((x, y) => x + y, 0) / a.length), p50: r3(pct(a, 0.5)), p95: r3(pct(a, 0.95)), p99: r3(pct(a, 0.99)), max: r3(Math.max(...a)) });
    const dbg = gl.getExtension('WEBGL_debug_renderer_info');
    const res = { shadows, merged, size: [w, h], first_render_ms: r3(first_render_ms), pixel_ratio: renderer.getPixelRatio(), info, counted: countScene(), walk_frame_ms: stat(intervals), walk_equivalent_fps: r3(1000 / (intervals.reduce((x, y) => x + y, 0) / intervals.length)), cpu_render_call_ms: stat(cpu), synced_frame_ms: stat(sync),
      programs: renderer.info.programs?.length, memory: { ...renderer.info.memory }, visibility: alive(), gpu: dbg ? gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL) : 'unavailable', gl_version: gl.getParameter(gl.VERSION) };
    renderer.userSize = false; P.resize(); P.setMerged(false);
    return res;
  }


  // Sensitivity tests on the one machine available: output resolution and shadow-map size (a stand-in for slower fill-rate / memory bandwidth, NOT a low-end device)
  async function testPerfScaling() {
    const out = { resolution: [], shadow_map: [] }; const pick = (r) => ({ size: r.size, shadows: r.shadows, merged: r.merged, calls: r.info.calls, first_render_ms: r.first_render_ms, walk_mean_ms: r.walk_frame_ms.mean, walk_p95_ms: r.walk_frame_ms.p95, synced_mean_ms: r.synced_frame_ms.mean, synced_p50_ms: r.synced_frame_ms.p50, synced_p95_ms: r.synced_frame_ms.p95, synced_max_ms: r.synced_frame_ms.max });
    const setShadowSize = (s) => { P.sun.shadow.mapSize.set(s, s); if (P.sun.shadow.map) { P.sun.shadow.map.dispose(); P.sun.shadow.map = null; } };
    setShadowSize(4096);
    for (const [w, h] of [[1280, 720], [1920, 1080], [2560, 1440], [3840, 2160]]) { out.resolution.push(pick(await measure({ shadows: true, merged: true, w, h, frames: 90 }))); await sleep(50); }
    for (const s of [1024, 2048, 4096]) { setShadowSize(s); out.shadow_map.push({ map: s, ...pick(await measure({ shadows: true, merged: true, w: 1280, h: 720, frames: 90 })) }); await sleep(50); }
    setShadowSize(4096); out.shadow_map.push({ map: 'off', ...pick(await measure({ shadows: false, merged: true, w: 1280, h: 720, frames: 90 })) });
    await save('performance-scaling.json', out); return out;
  }

  // draw calls and triangles actually submitted for each reference camera (frustum culling on): what the renderer was asked to draw, not a budget
  function viewCounts() {
    const rec = {}; P.sim.frozenCamera = true; renderer.userSize = true; renderer.setSize(1280, 720, false); camera.aspect = 16 / 9;
    for (const n of ['p3-bazaar-aerial', 'p3-aisle-eye', 'p3-west-interior', 'p3-west-entrance', 'p3-axis-to-hall', 'p3-gameplay', 'view-a-aerial']) {
      const v = sceneData.views[n]; if (!v) continue; camera.fov = v.fov; camera.updateProjectionMatrix(); camera.position.set(...v.pos); camera.lookAt(...v.look); camera.updateMatrixWorld(true);
      renderer.info.reset(); renderer.render(scene, camera); hardSync(); rec[n] = { calls: renderer.info.render.calls, triangles: renderer.info.render.triangles };
    }
    P.sim.frozenCamera = false; renderer.userSize = false; P.resize(); return rec;
  }
  async function testPerf() {
    const out = [];
    for (const cfg of [{ shadows: false, merged: 'none' }, { shadows: true, merged: 'none' }, { shadows: false, merged: 'scene' }, { shadows: true, merged: 'scene' }, { shadows: false, merged: 'district' }, { shadows: true, merged: 'district' }]) {
      const r = await measure(cfg); r.merge_mode = cfg.merged; P.setMerged(cfg.merged); r.view_calls = viewCounts(); P.setMerged('none'); out.push(r); P.say('perf ' + JSON.stringify(cfg)); await sleep(50);
    }
    P.setShadows(true);
    const counts = { prewarm_ms: P.prewarmMs ? Math.round(P.prewarmMs) : 0, mat_cache: { before: P.matStats.before, after: P.matStats.after }, shadow_fit: P.shadowFit, shadow_map: P.opt.smap, textures: P.textures.size, materials: P.materials.size, geometries: P.geometries.size, user_agent: navigator.userAgent, device_pixel_ratio: devicePixelRatio, window: [innerWidth, innerHeight], hardware_concurrency: navigator.hardwareConcurrency };
    const tag = new URLSearchParams(location.search).get('tag'); await save('performance' + (tag ? '-' + tag : '') + '.json', { runs: out, counts });
    return { runs: out.map((r) => ({ shadows: r.shadows, merged: r.merged, calls: r.info.calls, triangles: r.info.triangles, walk_fps: r.walk_equivalent_fps, walk_ms: r.walk_frame_ms.mean, p95: r.walk_frame_ms.p95, synced_ms: r.synced_frame_ms.mean })), counts };
  }

  // P2-B batch 3: merge-strategy comparison. Unmerged, per-district, scene-wide and spatial cells of 20/30/45/60 m, shadows off and on, on the same machine in one session,
  // interleaved repeats (median reported). Per mode: what the renderer was asked to draw in ten reference cameras (frustum culling on), synced frame time per camera,
  // a 60 Hz walk, resident geometry, JS heap, merge build time. ?town24=1 adds the five performance surrogates (see p2a.js) so the scene has all 24 P1.4 buildings.
  const geoBytes = (root) => { let b = 0; const seen = new Set(), bufs = new Set(); root.traverse((o) => { if (!o.isMesh || seen.has(o.geometry)) return; seen.add(o.geometry); for (const a of Object.values(o.geometry.attributes)) { const arr = a.isInterleavedBufferAttribute ? a.data.array : a.array; if (!bufs.has(arr)) { bufs.add(arr); b += arr.byteLength; } } if (o.geometry.index) b += o.geometry.index.array.byteLength; }); return b; };
  // ---------------------------------------------------------------------------------------------- P2-B batch 4: merged-geometry integrity (index precision, bounding volumes, corruption)
  // For every merge mode: index array type against vertex count (a Uint16 index on a bucket of more than 65,535 vertices would wrap), maximum index against vertex count, NaN positions, every vertex inside the
  // geometry's bounding sphere and box, total triangles against the unmerged scene, and a rendered comparison of ten views (640 x 360, shadows off) against the unmerged render.
  async function testMergeIntegrity() {
    const modes = (new URLSearchParams(location.search).get('modes') || 'district,cell60,cell45,cell30,cell20,scene').split(','), out = { modes: {}, views: {} };
    const triOf = (root) => { let t = 0; root.traverse((o) => { if (o.isMesh && !o.isInstancedMesh && o.visible !== undefined) { const g = o.geometry; t += (g.index ? g.index.count : g.attributes.position.count) / 3; } else if (o.isInstancedMesh) t += o.count * (o.geometry.index ? o.geometry.index.count : o.geometry.attributes.position.count) / 3; }); return t; };
    P.setMerged('none'); const ref = triOf(P.world), views = ['p5-east-aerial', 'p5-court-from-lane', 'p4-district-aerial', 'p3-bazaar-aerial', 'p3-aisle-eye', 'p5-lane-east', 'p5-quarter-gameplay', 'p3-west-interior', 'p4-town-aerial', 'p5-route-aerial'];
    renderer.userSize = true; renderer.setSize(640, 360, false); camera.aspect = 16 / 9; P.sim.frozenCamera = true; P.setShadows(false);
    const gl = renderer.getContext(), W = 640, H = 360, shot = (n) => { const v = sceneData.views[n]; camera.fov = v.fov; camera.updateProjectionMatrix(); camera.position.set(...v.pos); camera.lookAt(...v.look); camera.updateMatrixWorld(true); renderer.render(scene, camera); const px = new Uint8Array(W * H * 4); gl.readPixels(0, 0, W, H, gl.RGBA, gl.UNSIGNED_BYTE, px); return px; };
    const refShots = {}; for (const n of views) refShots[n] = shot(n);
    for (const mode of modes) {
      P.setMerged(mode); const set = P.mergedSets[mode]; let meshes = 0, maxV = 0, u16 = 0, u32 = 0, wrapRisk = 0, idxOver = 0, nan = 0, outSphere = 0, outBox = 0, worstSphere = 0, degenerate = 0;
      set.traverse((o) => {
        if (!o.isMesh || o.isInstancedMesh) return; meshes++; const g = o.geometry, pos = g.attributes.position, vc = pos.count, idx = g.index; maxV = Math.max(maxV, vc);
        const isU16 = idx.array.constructor === Uint16Array; if (isU16) u16++; else u32++; if (isU16 && vc > 65535) wrapRisk++;
        let mx = 0; for (let i = 0; i < idx.count; i++) { const v = idx.array[i]; if (v > mx) mx = v; } if (mx >= vc) idxOver++;
        for (let i = 0; i + 2 < idx.count; i += 3) if (idx.array[i] === idx.array[i + 1] || idx.array[i + 1] === idx.array[i + 2] || idx.array[i] === idx.array[i + 2]) degenerate++;
        const bs = g.boundingSphere, bb = g.boundingBox; let bad = false, far = 0, ob = false;
        for (let i = 0; i < vc; i++) { const x = pos.getX(i), y = pos.getY(i), z = pos.getZ(i); if (!(Number.isFinite(x) && Number.isFinite(y) && Number.isFinite(z))) { bad = true; continue; }
          const d = Math.hypot(x - bs.center.x, y - bs.center.y, z - bs.center.z) - bs.radius; if (d > far) far = d; if (x < bb.min.x - 1e-4 || x > bb.max.x + 1e-4 || y < bb.min.y - 1e-4 || y > bb.max.y + 1e-4 || z < bb.min.z - 1e-4 || z > bb.max.z + 1e-4) ob = true; }
        if (bad) nan++; if (far > 1e-3) outSphere++; worstSphere = Math.max(worstSphere, far); if (ob) outBox++;
      });
      const px = {}; let worstDiff = 0, worstView = null;
      for (const n of views) { const a = refShots[n], b = shot(n); let sum = 0, big = 0; for (let i = 0; i < a.length; i += 4) { const d = (Math.abs(a[i] - b[i]) + Math.abs(a[i + 1] - b[i + 1]) + Math.abs(a[i + 2] - b[i + 2])) / 3; sum += d; if (d > 24) big++; }
        const r = { mean_abs_diff_0_255: r3(sum / (a.length / 4)), share_pixels_diff_over_24: r3(big / (a.length / 4)) }; px[n] = r; if (r.share_pixels_diff_over_24 > worstDiff) { worstDiff = r.share_pixels_diff_over_24; worstView = n; } }
      out.modes[mode] = { meshes, max_vertices_in_one_mesh: maxV, uint16_index_meshes: u16, uint32_index_meshes: u32, uint16_meshes_with_more_than_65535_vertices: wrapRisk, meshes_with_index_beyond_vertex_count: idxOver, meshes_with_nan_positions: nan, meshes_with_vertices_outside_bounding_sphere: outSphere, worst_vertex_beyond_sphere_m: r3(worstSphere),
        meshes_with_vertices_outside_bounding_box: outBox, degenerate_triangles: degenerate, triangles: triOf(set), triangles_unmerged: ref, triangles_equal: triOf(set) === ref, render_vs_unmerged: px, worst_view_share_over_24: worstView ? { view: worstView, share: r3(worstDiff) } : null };
      await sleep(0);
    }
    P.setMerged('none'); P.sim.frozenCamera = false; renderer.userSize = false; P.resize();
    await save('merge-integrity.json', out); return out;
  }

  async function testMergeCells() {
    const q = new URLSearchParams(location.search), reps = Number(q.get('reps') || 3), modes = (q.get('modes') || 'none,district,cell60,cell45,cell30,cell20,scene').split(',');
    const views = ['p4-town-aerial', 'p3-bazaar-aerial', 'p4-district-aerial', 'p4-lane-north', 'p3-aisle-eye', 'p3-west-interior', 'p4-gate-back', 'p3-axis-to-hall', 'p3-gameplay', 'p2b-hall-aerial', 'p5-east-aerial', 'p5-lane-east', 'p5-court-from-lane', 'p5-quarter-gameplay', 'p5-route-aerial', 't02-southern-arrival', 't07-tea-route', 't08-civic-terrace', 't09-exchange-hall-approach', 'c01-terrace-aerial', 'c02-assay-office', 't10-lookout-to-terrace'];
    const med = (a) => { const b = [...a].sort((x, y) => x - y); return b.length ? b[Math.floor(b.length / 2)] : null; };
    const rows = []; const meta = { town24: q.get('town24') === '1', placed: P.placed.length, world_geometry_mb: r3(geoBytes(P.world) / 1048576), load_ms: P.loadMs, prewarm_ms: P.prewarmMs, kit_nodes: Object.keys(P.kit).length };
    for (let rep = 0; rep < reps; rep++) for (const merged of modes) for (const shadows of [false, true]) {
      P.setShadows(shadows); const r = await measure({ shadows, merged, frames: Number(q.get('pframes') || 120) });
      P.setMerged(merged); P.sim.frozenCamera = true; renderer.userSize = true; renderer.setSize(1280, 720, false); camera.aspect = 16 / 9; P.setShadows(shadows);
      const vr = {};
      for (const n of views) {
        const v = sceneData.views[n]; if (!v) continue; camera.fov = v.fov; camera.updateProjectionMatrix(); camera.position.set(...v.pos); camera.lookAt(...v.look); camera.updateMatrixWorld(true);
        renderer.info.reset(); renderer.render(scene, camera); hardSync(); const calls = renderer.info.render.calls, triangles = renderer.info.render.triangles, ts = [];
        for (let i = 0; i < 10; i++) { const t0 = performance.now(); renderer.render(scene, camera); hardSync(); ts.push(performance.now() - t0); }
        vr[n] = { calls, triangles, ms: r3(med(ts)) };
      }
      const set = merged === 'none' ? P.world : P.mergedSets[merged];
      rows.push({ rep, merged, shadows, cpu_ms: r.cpu_render_call_ms.mean, walk_ms: r.walk_frame_ms.mean, walk_p95_ms: r.walk_frame_ms.p95, walk_p50_ms: r.walk_frame_ms.p50, walk_p99_ms: r.walk_frame_ms.p99, walk_max_ms: r.walk_frame_ms.max, synced_p50_ms: r.synced_frame_ms.p50, synced_p95_ms: r.synced_frame_ms.p95, synced_p99_ms: r.synced_frame_ms.p99, synced_ms: r.synced_frame_ms.mean, first_render_ms: r.first_render_ms, programs: r.programs, views: vr,
        resident_geometry_mb: r3(geoBytes(set) / 1048576), meshes: (() => { let m = 0; set.traverse((o) => { if (o.isMesh) m++; }); return m; })(), build_ms: merged === 'none' ? 0 : r3(P.mergedSets[merged].userData.build_ms),
        heap_mb: performance.memory ? r3(performance.memory.usedJSHeapSize / 1048576) : null, gl_memory: { ...renderer.info.memory } });
      P.sim.frozenCamera = false; renderer.userSize = false; P.resize(); P.setMerged('none'); P.say(`mergecells rep ${rep} ${merged} shadows ${shadows}`); await sleep(30);
    }
    const summary = {};
    for (const merged of modes) for (const shadows of [false, true]) {
      const rs = rows.filter((r) => r.merged === merged && r.shadows === shadows), perView = {};
      for (const n of Object.keys(rs[0].views)) perView[n] = { calls: rs[0].views[n].calls, triangles: rs[0].views[n].triangles, ms: r3(med(rs.map((r) => r.views[n].ms))) };
      const vv = Object.values(perView);
      summary[merged + (shadows ? ' shadows' : ' no-shadows')] = { cpu_submit_ms: r3(med(rs.map((r) => r.cpu_ms))), walk_ms: r3(med(rs.map((r) => r.walk_ms))), walk_p95_ms: r3(med(rs.map((r) => r.walk_p95_ms))), walk_p50_ms: r3(med(rs.map((r) => r.walk_p50_ms))), walk_p99_ms: r3(med(rs.map((r) => r.walk_p99_ms))), walk_max_ms: r3(med(rs.map((r) => r.walk_max_ms))), synced_p50_ms: r3(med(rs.map((r) => r.synced_p50_ms))), synced_p95_ms: r3(med(rs.map((r) => r.synced_p95_ms))), synced_p99_ms: r3(med(rs.map((r) => r.synced_p99_ms))), synced_ms: r3(med(rs.map((r) => r.synced_ms))), synced_range: [Math.min(...rs.map((r) => r.synced_ms)), Math.max(...rs.map((r) => r.synced_ms))],
        mean_view_ms: r3(vv.reduce((a, b) => a + b.ms, 0) / vv.length), mean_view_calls: r3(vv.reduce((a, b) => a + b.calls, 0) / vv.length), mean_view_triangles: Math.round(vv.reduce((a, b) => a + b.triangles, 0) / vv.length), worst_view_ms: Math.max(...vv.map((b) => b.ms)),
        resident_geometry_mb: rs[0].resident_geometry_mb, meshes: rs[0].meshes, build_ms: rs[0].build_ms, heap_mb_median: rs[0].heap_mb == null ? null : r3(med(rs.map((r) => r.heap_mb))), gl_geometries: rs[0].gl_memory.geometries, gl_textures: rs[0].gl_memory.textures, programs: rs[0].programs, per_view: perView };
    }
    const out = { meta: { ...meta, reps, modes, views, user_agent: navigator.userAgent, device_pixel_ratio: devicePixelRatio, hardware_concurrency: navigator.hardwareConcurrency, hardSync: 'readPixels 1x1' }, summary, rows };
    await save('merge-cells' + (q.get('tag') ? '-' + q.get('tag') : '') + '.json', out); return { meta: out.meta, summary: Object.fromEntries(Object.entries(summary).map(([k, v]) => [k, { cpu_ms: v.cpu_submit_ms, walk_ms: v.walk_ms, synced_ms: v.synced_ms, range: v.synced_range, mean_view_ms: v.mean_view_ms, calls: v.mean_view_calls, tris: v.mean_view_triangles, geo_mb: v.resident_geometry_mb, meshes: v.meshes, build_ms: v.build_ms }])) };
  }

  // ---------------------------------------------------------------------------------------------- look calibration against the Blender renders
  const BLENDER = '/.asset-inspection/merchant-citadel-p1/p2a/world/renders/';
  async function blenderPixels(name, w, h) { const img = new Image(); img.src = BLENDER + name + '.png'; await img.decode(); const c = document.createElement('canvas'); c.width = w; c.height = h; const g = c.getContext('2d', { willReadFrequently: true }); g.drawImage(img, 0, 0, w, h); return g.getImageData(0, 0, w, h).data; }
  function cells(data, w, h, cw = 50) { const out = []; for (let cy = 0; cy < h; cy += cw) for (let cx = 0; cx < w; cx += cw) { let r = 0, g = 0, b = 0, n = 0; for (let y = cy; y < Math.min(h, cy + cw); y += 2) for (let x = cx; x < Math.min(w, cx + cw); x += 2) { const i = (y * w + x) * 4; r += data[i]; g += data[i + 1]; b += data[i + 2]; n++; } out.push([r / n, g / n, b / n]); } return out; }
  const luma = (c) => 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
  P.applyLook = ({ sun, env, exp, hemi, bg, ao }) => { if (bg != null) scene.backgroundIntensity = bg; if (sun != null) P.sun.intensity = sun; if (env != null) scene.environmentIntensity = env; if (exp != null) { renderer.toneMappingExposure = exp; P.look.exp.value = exp; } if (ao != null) P.look.ao.value = ao; if (hemi != null) P.hemi.intensity = hemi; };
  async function calibrate(views = ['view-b-merchant-street', 'view-c2-bazaar-eye', 'p2a-junction'], grid = { sun: [2.4, 3.2, 4.0], env: [0.9, 1.4, 2.0], exp: [0.7, 0.85, 1.0] }) {
    const W = 800, H = 450; const refs = {}; for (const v of views) refs[v] = cells(await blenderPixels(v, W, H), W, H);
    const rows = []; P.sim.frozenCamera = true;
    for (const sun of grid.sun) for (const env of grid.env) for (const exp of grid.exp) {
      P.applyLook({ sun, env, exp }); let abs = 0, bias = 0, n = 0, chroma = 0;
      for (const v of views) {
        renderer.userSize = true; renderer.setSize(W, H, false); const vw = sceneData.views[v]; camera.aspect = W / H; camera.fov = vw.fov; camera.updateProjectionMatrix(); P.setCharacterAt(vw.who); camera.position.set(...vw.pos); camera.lookAt(...vw.look); camera.updateMatrixWorld(true);
        renderer.render(scene, camera); const c = document.createElement('canvas'); c.width = W; c.height = H; const g = c.getContext('2d', { willReadFrequently: true }); g.drawImage(renderer.domElement, 0, 0); const mine = cells(g.getImageData(0, 0, W, H).data, W, H);
        mine.forEach((m, i) => { const r = refs[v][i]; abs += Math.abs(luma(m) - luma(r)); bias += luma(m) - luma(r); chroma += Math.abs((m[0] - m[2]) - (r[0] - r[2])); n++; });
      }
      rows.push({ sun, env, exp, mean_abs_luma: r3(abs / n), mean_bias_luma: r3(bias / n), mean_abs_warmth: r3(chroma / n) }); await sleep(0);
    }
    rows.sort((a, b) => a.mean_abs_luma - b.mean_abs_luma); renderer.userSize = false; P.resize(); P.sim.frozenCamera = false; await save('calibration.json', rows); return rows.slice(0, 6);
  }
  P.calibrate = calibrate;
  P.runRoute = runRoute; P.ROUTES = ROUTES; P.testRoutes = testRoutes; P.testPlatform = testPlatform; P.testViews = testViews; P.testScale = testScale; P.testPerf = testPerf; P.measure = measure; P.capture = capture; P.setMode = setMode; P.countScene = countScene;
  P.autotest = async (name) => {
    const t = performance.now(); let res;
    try {
      if (name === 'scale') res = await testScale();
      else if (name === 'routes') res = await testRoutes();
      else if (name === 'platform') res = await testPlatform();
      else if (name === 'cause') res = await testCameraCause();
      else if (name === 'network') res = await testNetwork();
      else if (name === 'perfscale') res = await testPerfScaling();
      else if (name === 'bazaar') res = await testBazaar();
      else if (name === 'merch') res = await testMerchandise();
      else if (name === 'hallcam') res = await testHallCamera();
      else if (name === 'fademotion') res = await testFadeMotion();
      else if (name === 'cases') res = await testCameraCases();
      else if (name === 'camshots') res = await testCameraShots();
      else if (name === 'views') res = await testViews();
      else if (name === 'perf') res = await testPerf();
      else if (name === 'mergecells') res = await testMergeCells();
      else if (name === 'district') res = await testDistrict();
      else if (name === 'compress') res = await testCompression();
      else if (name === 'mergeintegrity') res = await testMergeIntegrity();
      else if (name === 'suite') {                                    // batch 4: the whole walking/camera/collision suite in one page load; each test saves its own evidence file
        res = {}; const t0s = performance.now(); const run = async (k, f) => { const t1 = performance.now(); const r = await f(); res[k] = { seconds: Math.round((performance.now() - t1) / 1000), summary: r && r.summary ? r.summary : (Array.isArray(r) ? { n: r.length, pass: r.filter((x) => x.pass).length } : 'saved') }; };
        await run('network', testNetwork); await run('district', testDistrict); await run('merch', testMerchandise); await run('hallcam', testHallCamera); await run('compress', testCompression); await run('fademotion', testFadeMotion); await run('platform', testPlatform); res.total_seconds = Math.round((performance.now() - t0s) / 1000);
      }
      else if (name === 'calibrate') res = await calibrate();
      else if (name === 'all') { res = { scale: (await testScale()).texture_totals, routes: (await testRoutes()).length, platform: (await testPlatform()).length, views: (await testViews()).length, perf: await testPerf() }; }
    } catch (e) { res = { error: String(e), stack: e.stack }; }
    P.autotestResult = res; document.body.dataset.done = '1'; P.say('autotest done in ' + Math.round(performance.now() - t) + ' ms'); await save('autotest-' + name + (new URLSearchParams(location.search).get('tag') ? '-' + new URLSearchParams(location.search).get('tag') : '') + '.json', res);
  };
}
