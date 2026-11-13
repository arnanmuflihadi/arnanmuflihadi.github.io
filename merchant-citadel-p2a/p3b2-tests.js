// Merchant Citadel P3-B batch 2: wildlife and landscape measurements in the real preview. Scripted, not a human playtest. Results are POSTed to evidence/.
export function installWildTests(P) {
  const { T, isl, wild: W, camera, character } = P; if (!W) return;
  const mc = new MessageChannel(); const sleep = () => new Promise((r) => { mc.port1.onmessage = () => r(); mc.port2.postMessage(0); });
  const save = async (name, data) => { await fetch('/__save?name=' + encodeURIComponent(name), { method: 'POST', body: data instanceof Blob ? data : JSON.stringify(data, null, 1) }); };
  const r3 = (v) => Math.round(v * 1000) / 1000, pct = (a, p) => { const s = [...a].sort((x, y) => x - y); return s.length ? s[Math.min(s.length - 1, Math.floor(p * s.length))] : null; };
  const solids = () => P.walkObs.filter((o) => !o.cameraOnly), distSolid = (x, z) => { let b = 99, who = null; for (const o of solids()) { const dx = Math.max(Math.abs(x - o.x) - o.w / 2, 0), dz = Math.max(Math.abs(z - o.z) - o.d / 2, 0), d = Math.hypot(dx, dz); if (d < b) { b = d; who = o.src; } } return [b, who]; };
  const slopeAt = (x, z) => Math.hypot(P.heightAt(x + 0.4, z) - P.heightAt(x - 0.4, z), P.heightAt(x, z + 0.4) - P.heightAt(x, z - 0.4)) / 0.8;
  const inKeepout = (x, z) => W.forbidden(x, -z);

  // 1. spawn validation: every ground agent stands on walkable, gentle, free ground outside the dragon keep-outs, with the feet on the support height
  async function testSpawn() {
    const out = { ground: [], summary: null, birds: [], butterflies: [] };
    for (const a of W.agents) {
      const x = a.pos.x, z = a.pos.z;
      if (a.group === 'ground') { const [sd, who] = distSolid(x, z); out.ground.push({ sp: a.sp, hid: a.hid, at: [r3(x), r3(-z)], walkable: isl.walkable(x, z), slope: r3(slopeAt(x, z)), solid_m: r3(sd), nearest: who, keepout: inKeepout(x, z), on_ground_err_m: r3(Math.abs(a.pos.y - P.heightAt(x, z))), blocked: P.blocked(x, z, P.walkObs, 0.28) }); }
      else if (a.group === 'bird') out.birds.push({ sp: a.sp, hid: a.hid, state: a.state, perch: a.perch ? [a.perch.kind, r3(a.perch.x), r3(-a.perch.z), r3(a.perch.y), a.perch.src || null] : null, keepout: a.perch ? inKeepout(a.perch.x, a.perch.z) : false, y: r3(a.pos.y) });
      else out.butterflies.push({ hid: a.hid, at: [r3(x), r3(-z)], above_ground_m: r3(a.pos.y - P.heightAt(x, z)) });
    }
    const g = out.ground; out.summary = { ground_agents: g.length, not_walkable: g.filter((q) => !q.walkable).length, blocked: g.filter((q) => q.blocked).length, in_keepout: g.filter((q) => q.keepout).length, max_slope: Math.max(...g.map((q) => q.slope)), min_solid_clearance_m: Math.min(...g.map((q) => q.solid_m)), max_ground_error_m: Math.max(...g.map((q) => q.on_ground_err_m)),
      by_habitat: Object.fromEntries([...new Set(g.map((q) => q.hid))].map((h) => [h, g.filter((q) => q.hid === h).length])), birds: out.birds.length, birds_in_keepout: out.birds.filter((b) => b.keepout).length, butterflies: out.butterflies.length };
    await save('p3b2-wildlife-spawn.json', out); return out;
  }

  // 2. long simulation at full rate (the player stands far away, so nobody is disturbed): ambient behaviour must stay legal and varied
  async function testSim(seconds = 600, dt = 0.05) {
    W.ctl.forceFull = true; const far = { x: 120, z: 130, y: 0 }, cam = { x: 120, y: 5, z: 130 }; const v = { not_walkable: 0, blocked: 0, keepout: 0, step: 0, slope: 0, ground_err: 0, outside_habitat: 0 }; const states = {}; const walked = new Map(); let maxStep = 0; const t0 = performance.now();
    const prev = new Map(W.agents.map((a) => [a, [a.pos.x, a.pos.z, a.pos.y]]));
    const homeD = new Map(); const steps = Math.floor(seconds / dt);
    for (let i = 0; i < steps; i++) {
      W.update(dt, far, cam);
      if (i % 4 === 0) for (const a of W.agents) {
        if (a.group !== 'ground') continue; const x = a.pos.x, z = a.pos.z, p = prev.get(a); const d = Math.hypot(x - p[0], z - p[1]); maxStep = Math.max(maxStep, Math.abs(a.pos.y - p[2]));
        if (!isl.walkable(x, z)) v.not_walkable++; if (P.blocked(x, z, P.walkObs, 0.2)) v.blocked++; if (inKeepout(x, z)) v.keepout++; if (Math.abs(a.pos.y - P.heightAt(x, z)) > 0.02) v.ground_err++;
        if (a.home && Math.hypot(x - a.home.x, z - a.home.z) > a.spec.radius * 3) v.outside_habitat++; walked.set(a, (walked.get(a) || 0) + d); prev.set(a, [x, z, a.pos.y]); (states[a.sp] ||= {})[a.state] = (states[a.sp][a.state] || 0) + 1;
      }
      if (i % 200 === 0) await sleep();
    }
    W.ctl.forceFull = false;
    const per = {}; for (const a of W.agents.filter((q) => q.group === 'ground')) { (per[a.sp] ||= []).push(walked.get(a) || 0); }
    const out = { simulated_seconds: seconds, dt, wall_ms: r3(performance.now() - t0), violations: v, max_height_step_between_samples_m: r3(maxStep), distance_walked_m: Object.fromEntries(Object.entries(per).map(([k, a]) => [k, r3(a.reduce((x, y) => x + y, 0) / a.length)])), state_share: Object.fromEntries(Object.entries(states).map(([k, o]) => { const t = Object.values(o).reduce((x, y) => x + y, 0); return [k, Object.fromEntries(Object.entries(o).map(([s, n]) => [s, r3(n / t)]))]; })) };
    await save('p3b2-wildlife-sim.json', out); return out;
  }

  // 3. reactions to the player
  function settle(n = 20, dt = 0.05, px = 0, pz = 0, cam = { x: 0, y: 5, z: 0 }) { for (let i = 0; i < n; i++) W.update(dt, { x: px, z: pz, y: 0 }, cam); }
  async function testReactions() {
    const out = []; W.ctl.forceFull = true;
    const cases = [['Sheep', 0], ['Lamb', 0], ['Cow', 0], ['Horse', 0], ['Llama', 0], ['Pig', 0], ['Cat', 0], ['RedFox', 0], ['Chick', 0], ['Pug', 0], ['Dog', 0]];
    for (const [sp, k] of cases) {
      const a = W.agents.filter((q) => q.sp === sp)[k]; if (!a) { out.push({ sp, error: 'none' }); continue; }
      a.pos.set(a.home.x, P.heightAt(a.home.x, a.home.z), a.home.z); W.setState(a, 'IDLE', 5); const home = { ...a.home }; const dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]; let player = null;
      for (const [dx, dz] of dirs) { const ok = [14, 12, 10, 8, 6, 4, 3, 2].every((d) => P.heightAt(a.pos.x + dx * d, a.pos.z + dz * d) > -50); if (ok) { player = { x: a.pos.x + dx * 14, z: a.pos.z + dz * 14, dx, dz }; break; } } if (!player) player = { x: a.pos.x + 14, z: a.pos.z, dx: 1, dz: 0 };
      const rec = { sp, start: [r3(a.pos.x), r3(-a.pos.z)], alert_at: null, flee_at: null, min_dist: 99, max_speed: 0 }; let t = 0, prev = [a.pos.x, a.pos.z]; const dt = 0.05; const cam = { x: player.x, y: 5, z: player.z };
      // approach at walking speed (2.1 m/s) for 14 m, then stop and watch 8 s, then retreat 30 m and watch 25 s
      for (let i = 0; i < 400; i++) { const approaching = t < 6.2; if (approaching) { player.x -= player.dx * 2.1 * dt; player.z -= player.dz * 2.1 * dt; } W.update(dt, { x: player.x, z: player.z, y: 0 }, { x: player.x, y: 5, z: player.z }); t += dt; const d = Math.hypot(a.pos.x - player.x, a.pos.z - player.z); rec.min_dist = Math.min(rec.min_dist, d); const sp_ = Math.hypot(a.pos.x - prev[0], a.pos.z - prev[1]) / dt; rec.max_speed = Math.max(rec.max_speed, sp_); prev = [a.pos.x, a.pos.z];
        if (rec.alert_at === null && a.state === 'ALERT') rec.alert_at = { t: r3(t), dist: r3(d) }; if (rec.flee_at === null && a.state === 'FLEE') rec.flee_at = { t: r3(t), dist: r3(d) }; }
      rec.after_approach = { state: a.state, dist: r3(Math.hypot(a.pos.x - player.x, a.pos.z - player.z)), displaced_m: r3(Math.hypot(a.pos.x - rec.start[0], -a.pos.z - rec.start[1])) };
      for (let i = 0; i < 600; i++) { player.x += player.dx * 3.0 * dt; player.z += player.dz * 3.0 * dt; W.update(dt, { x: player.x, z: player.z, y: 0 }, { x: player.x, y: 5, z: player.z }); }
      for (let i = 0; i < 900; i++) W.update(dt, { x: player.x + 60 * player.dx, z: player.z + 60 * player.dz, y: 0 }, { x: player.x, y: 5, z: player.z });
      rec.after_retreat = { state: a.state, dist_from_home: r3(Math.hypot(a.pos.x - home.x, a.pos.z - home.z)), radius: a.spec.radius, legal: isl.walkable(a.pos.x, a.pos.z) && !inKeepout(a.pos.x, a.pos.z) }; out.push(rec); await sleep();
    }
    W.ctl.forceFull = false; await save('p3b2-wildlife-reactions.json', out); return out;
  }

  // 4. birds: perch -> takeoff -> fly -> land cycle, and orbiters
  async function testBirds() {
    W.ctl.forceFull = true; const out = []; const dt = 0.05;
    for (const [sp, hid] of [['Bird', 'A_settlement'], ['Bird', 'B_caravan_green'], ['Bird', 'D_tea_terraces'], ['Bird', 'G_sky_quay']]) {
      const a = W.agents.filter((q) => q.sp === sp && q.hid === hid && q.perch && q.perchList && q.perchList.length > 1)[0]; if (a) { a.state = 'PERCHED'; a.t = 0; a.root.rotation.set(0, a.yaw, 0); a.pos.set(a.perch.x, a.perch.y, a.perch.z); } if (!a) { out.push({ sp, error: 'no perched agent' }); continue; }
      const seq = [a.state], p0 = [a.pos.x, a.pos.y, a.pos.z]; a.timer = 0.05; let maxY = a.pos.y, minD = 1e9, t = 0, dest = null;
      for (let i = 0; i < 20 * 120; i++) { W.update(dt, { x: 150, z: 150, y: 0 }, { x: 150, y: 5, z: 150 }); t += dt; if (seq[seq.length - 1] !== a.state) seq.push(a.state); maxY = Math.max(maxY, a.pos.y); if (a.dest && !dest) dest = [a.dest.x, a.dest.y, a.dest.z]; if (a.state === 'PERCHED' && seq.length > 1) break; }
      out.push({ sp, hid, sequence: seq, seconds: r3(t), start: p0.map(r3), end: [a.pos.x, a.pos.y, a.pos.z].map(r3), destination: dest && dest.map(r3), landed_on_destination_m: dest ? r3(Math.hypot(a.pos.x - dest[0], a.pos.y - dest[1], a.pos.z - dest[2])) : null, max_height_m: r3(maxY), flight_keepout_perch: dest ? inKeepout(dest[0], dest[2]) : null });
    }
    const nonFly = []; for (let i = 0; i < 20 * 60; i++) W.update(dt, { x: P.character.root.position.x, z: P.character.root.position.z, y: 0 }, { x: 0, y: 5, z: 0 });
    
    for (const sp of ['Eagle']) { const a = W.agents.filter((q) => q.sp === sp)[0]; const ys = [], ds = []; for (let i = 0; i < 20 * 120; i++) { W.update(dt, { x: 150, z: 150, y: 0 }, { x: 150, y: 5, z: 150 }); ys.push(a.pos.y); ds.push(Math.hypot(a.pos.x - a.orbit.x, a.pos.z - a.orbit.z)); } out.push({ sp, orbit: [r3(a.orbit.x), r3(-a.orbit.z), r3(a.orbit.r)], altitude_m: [r3(Math.min(...ys)), r3(Math.max(...ys))], radius_m: [r3(Math.min(...ds)), r3(Math.max(...ds))], above_terrain_min_m: r3(Math.min(...ys) - Math.max(...[0].map(() => P.heightAt(a.pos.x, a.pos.z)))) }); }
    W.ctl.forceFull = false; await save('p3b2-wildlife-birds.json', out); return out;
  }
  P.wildTests = { testSpawn, testSim, testReactions, testBirds, settle, distSolid, slopeAt, save, sleep };
  // 5. performance: same cameras with each layer on/off; CPU cost of wildlife and flora updates; texture memory
  async function testPerfB2(tag = '') {
    const I = P.island, vv = await (await fetch('data/p3b-views.json')).json(); const DT = 1 / 60;
    const view = (n) => () => { const [p, look, fov] = vv[n]; I.setCam(p, look, fov); };
    const play = (x, n, yaw, steps = 90) => () => { P.sim.frozenCamera = false; P.teleport(x, -n, yaw); for (let i = 0; i < steps; i++) P.stepSim(DT); };
    const cases = [['street: arrival court (gameplay camera)', play(0, -16, 0)], ['street: Exchange Hall forecourt', play(0, 75.4, 0)], ['Caravan Green meadow (gameplay camera, animals around)', play(-44, 16, Math.PI / 2)], ['Counting Crag bench (gameplay camera)', play(36, 101, Math.PI * 0.9)], ['tea terraces promenade (gameplay camera)', play(60, 55.5, -Math.PI / 2)],
      ['aerial: whole island', view('v1-aerial')], ['flight: south-west approach', view('v6-dragon-approach')], ['flight: east approach', view('v6b-dragon-approach-east')], ['town with vegetation (low aerial)', view('b2-town-vegetation')]];
    const layers = { 'all on': () => {}, 'flora hidden': () => { isl.flora && isl.group.traverse((o) => { if (o.name && o.name.startsWith('FL_')) o.visible = false; }); }, 'wildlife hidden': () => { W.group.visible = false; }, 'island + flora + wildlife hidden': () => { isl.group.visible = false; W.group.visible = false; } };
    const reset = () => { isl.group.traverse((o) => { if (o.name && o.name.startsWith('FL_')) o.visible = true; }); isl.group.visible = true; W.group.visible = true; };
    const out = { when: new Date().toISOString(), note: 'frame_complete = render() + 1x1 read-back (GPU completion, not vsync-limited); 1280x720, DPR 1, shadows on; shared desktop machine, see load in README', cases: [] };
    for (const [label, setup] of cases) for (const [lname, apply] of Object.entries(layers)) { reset(); const m = await I.measure(label + ' [' + lname + ']', () => { setup(); apply(); }, { frames: 120, warm: 20 }); out.cases.push(m); await sleep(); }
    reset();
    // CPU per frame of the whole step (character + camera + wildlife + flora) with the wildlife running at its real LOD (player at the Green)
    P.teleport(-44, -16, Math.PI / 2); for (let i = 0; i < 60; i++) P.stepSim(DT); W.stats.ms = 0; W.stats.frames = 0; const f0 = isl.flora.stats.ms, u0 = isl.flora.stats.updates; const t0 = performance.now(); for (let i = 0; i < 600; i++) { P.stepSim(DT); isl.tick(P.sim.time, camera); }
    out.cpu = { frames: 600, step_ms_per_frame: r3((performance.now() - t0) / 600), wildlife_update_ms_per_frame: r3(W.stats.ms / W.stats.frames), wildlife_agents: W.stats.agents, simulated_last_frame: W.stats.simulated, mixers_last_frame: W.stats.mixers, visible_last_frame: W.stats.visible, flora_rebucket_ms_each: r3((isl.flora.stats.ms - f0) / Math.max(1, isl.flora.stats.updates - u0)), flora_instances_drawn: isl.flora.stats.drawn, flora_l0: isl.flora.stats.l0, flora_l1: isl.flora.stats.l1, flora_triangles_now: Math.round(isl.flora.triangles()) };
    // texture memory (GPU estimate with mips) of the flora library and everything the renderer holds
    let mb = 0; const seen = new Set(); isl.flora.materials.forEach((m) => { const im = m.map && m.map.image; if (im && !seen.has(im)) { seen.add(im); mb += im.width * im.height * 4 * 1.333 / 1048576; } });
    out.memory = { flora_textures: seen.size, flora_texture_mb_estimate: r3(mb), renderer_textures: P.renderer.info.memory.textures, renderer_geometries: P.renderer.info.memory.geometries, load_ms: { island_glb: r3(isl.loadMs), flora_glb: r3(isl.flora.loadMs), wildlife: r3(W.loadMs) }, files_bytes: await Promise.all(['assets-p3b2/flora.glb', 'models/merchant-citadel-p3b-island.glb', 'data/island-flora.json'].map(async (u) => [u, (await (await fetch(u)).arrayBuffer()).byteLength])) };
    await save('p3b2-perf' + tag + '.json', out); return out;
  }
  P.wildTests.testPerfB2 = testPerfB2;

  // 7. foot slide (batch 3 WP5): a clone walks / runs at the species speed with the clip rate swept; the four lowest bones are the feet; slide = mean horizontal speed of a foot in ground contact, as a fraction of the body speed
  async function testFootSlide(species = null) {
    const out = {}, DTf = 1 / 60;
    for (const sp of Object.keys(W.SPECIES)) {
      const spec = W.SPECIES[sp]; if (spec.kind !== 'ground' || (species && !species.includes(sp))) continue; const Pp = W.protos[sp]; out[sp] = {};
      for (const mode of ['walk', 'run']) {
        const clip = mode === 'run' ? (Pp.alias.run || Pp.alias.walk) : Pp.alias.walk, v = mode === 'run' ? spec.flee : spec.walk, cs0 = mode === 'run' && Pp.alias.run ? (spec.csr || spec.cs) : spec.cs;
        const model = T.cloneSkeleton(Pp.gltf.scene), root = new T.Object3D(); root.add(model); model.scale.setScalar(Pp.k); const mixer = new T.AnimationMixer(model), act = mixer.clipAction(clip); act.play(); const bones = []; model.traverse((o) => { if (o.isBone) bones.push(o); });
        const ymin = bones.map(() => 1e9), zlo = bones.map(() => 1e9), zhi = bones.map(() => -1e9); for (let i = 0; i < 48; i++) { mixer.setTime(clip.duration * i / 48); root.updateMatrixWorld(true); bones.forEach((b, k) => { const e = b.matrixWorld.elements; ymin[k] = Math.min(ymin[k], e[13]); zlo[k] = Math.min(zlo[k], e[14]); zhi[k] = Math.max(zhi[k], e[14]); }); }
        const order = ymin.map((y, k) => [zhi[k] - zlo[k], k, y]).filter((q) => q[2] < 0.3 * spec.h * 1.4).sort((a, b) => b[0] - a[0]).slice(0, 4).map((q) => q[1]); const feet = order.map((k) => bones[k]), floor = order.map((k) => ymin[k]);
        const run = (ts) => { mixer.stopAllAction(); const ac = mixer.clipAction(clip); ac.reset(); ac.play(); ac.timeScale = ts; mixer.setTime(0); ac.timeScale = ts; root.position.set(0, 0, 0); const n = Math.ceil(clip.duration / ts * 2 / DTf), prev = feet.map(() => null); let sum = 0, cnt = 0;
          for (let i = 0; i < n; i++) { root.position.z += v * DTf; mixer.update(DTf); root.updateMatrixWorld(true); feet.forEach((b, k) => { const e = b.matrixWorld.elements, x = e[12], y = e[13], z = e[14], con = y <= floor[k] + 0.04 * spec.h; if (con && prev[k] && i > n / 2) { sum += Math.hypot(x - prev[k][0], z - prev[k][1]) / DTf; cnt++; } prev[k] = con ? [x, z] : null; }); }
          return cnt ? sum / cnt / v : null; };
        const cur = run(Math.max(0.4, Math.min(2.8, v / cs0))), best = { ts: null, ratio: 9 }; for (let ts = 0.4; ts <= 3.01; ts += 0.05) { const r = run(ts); if (r !== null && r < best.ratio) { best.ratio = r; best.ts = ts; } }
        out[sp][mode] = { speed: v, current_rate: r3(Math.max(0.4, Math.min(2.8, v / cs0))), current_slide: cur === null ? null : r3(cur), best_rate: best.ts && r3(best.ts), best_slide: r3(best.ratio), cs_best: best.ts ? r3(v / best.ts) : null, clip_s: r3(clip.duration), feet: feet.map((b) => b.name) };
        await sleep();
      }
    }
    await save('p3b3-foot-slide.json', out); return out;
  }
  P.wildTests.testFootSlide = testFootSlide;

  // 6. captures in the real browser: portrait (close three-quarter view of one live agent), encounter (gameplay follow camera standing at a distance), strip (frame sequence for a GIF)
  const DT = 1 / 60;
  const planCam = (x, z, y, lx, lz, ly, fov = 36) => P.island.setCam([x, -z, y], [lx, -lz, ly], fov);               // three-frame x / z in, plan frame inside
  async function snap(name, w, h) { await sleep(); await sleep(); await save(name, await P.island.blob(w, h, 0.88)); return name; }
  const live = (sp, k = 0) => W.agents.filter((q) => q.sp === sp)[k];
  const clearBearing = (a, d, yw) => { const x1 = a.pos.x + Math.sin(yw) * d, z1 = a.pos.z + Math.cos(yw) * d; for (let u = 0.1; u <= 1; u += 0.06) { const x = a.pos.x + (x1 - a.pos.x) * u, z = a.pos.z + (z1 - a.pos.z) * u; if (P.blocked(x, z, P.walkObs, 0.3)) return false; } return !W.agents.some((q) => q !== a && Math.hypot(q.pos.x - x1, q.pos.z - z1) < 1.2) && isl.walkable(x1, z1); };
  async function portrait(sp, { k = 0, w = 1280, h = 720, side = 0.8, dist, tag = 'p3b2q-wild', posed = null } = {}) {
    const spec = W.SPECIES[sp]; let a = live(sp, k); W.ctl.forceFull = true; const was = P.character.root.visible; P.character.root.visible = false;
    if (posed) { const x = posed.x, z = posed.z; const d = W.demo(sp, x, z, posed.yaw ?? 0.6, posed.clip || 'idle', posed.t ?? 0.3, posed.graze || 0); d.root.position.y += posed.lift || 0; a = d; a.yaw = posed.yaw ?? 0.6; }
    else if (a.state !== 'IDLE' && a.group === 'ground') W.setState(a, 'IDLE', 6);
    const hh = spec.h, d = dist || Math.max(hh < 0.35 ? 1.5 : 2.2, hh * 3.4); let yaw = (a.yaw || 0) + side, cx = a.pos.x + Math.sin(yaw) * d, cz = a.pos.z + Math.cos(yaw) * d;
    const clear = (yw) => { const x1 = a.pos.x + Math.sin(yw) * d, z1 = a.pos.z + Math.cos(yw) * d; for (let u = 0.15; u <= 1; u += 0.07) { const x = a.pos.x + (x1 - a.pos.x) * u, z = a.pos.z + (z1 - a.pos.z) * u; if (P.blocked(x, z, P.walkObs, 0.25) && u > 0.1) return false; } return !W.agents.some((q) => q !== a && Math.hypot(q.pos.x - x1, q.pos.z - z1) < 1.2); };
    if (!posed && a.group === 'ground') for (const off of [0, 0.5, -0.5, 1.0, -1.0, 1.6, -1.6, 2.3, -2.3, 3.0]) { const yw = (a.yaw || 0) + side + off; if (clear(yw)) { yaw = yw; cx = a.pos.x + Math.sin(yaw) * d; cz = a.pos.z + Math.cos(yaw) * d; break; } }
    const y0 = a.root.position.y; planCam(cx, cz, y0 + hh * 0.95 + 0.3, a.pos.x, a.pos.z, y0 + hh * 0.5);
    for (let i = 0; i < 6; i++) P.stepSim(DT); const name = `${tag}-${sp.toLowerCase()}${k ? k : ''}${posed ? '-posed' : ''}.jpg`; await snap(name, w, h);
    P.character.root.visible = was; P.sim.frozenCamera = false; W.ctl.forceFull = false; if (posed) { a.root.parent && a.root.parent.remove(a.root); } return { name, state: a.state, at: [r3(a.pos.x), r3(-a.pos.z)] };
  }
  const standSpot = (x, z, ax, az, d) => { for (let k = 0; k < 24; k++) for (const dd of [d, d * 0.8, d * 1.2]) { const ang = Math.atan2(ax - x, az - z) + Math.PI + (k % 2 ? 1 : -1) * Math.floor(k / 2) * 0.26, px = x + Math.sin(ang) * dd, pz = z + Math.cos(ang) * dd; if (isl.walkable(px, pz) && !inKeepout(px, pz) && !P.blocked(px, pz, P.walkObs, 0.5)) return [px, pz]; } return null; };
  async function encounter(sp, { k = 0, dist, name, w = 1280, h = 720, settle = 90 } = {}) {
    const a = live(sp, k), spec = W.SPECIES[sp]; W.setState(a, 'IDLE', 20); const d = dist || Math.max(5.5, Math.min(9, (spec.alert || 6) + 1.5)); const spot = standSpot(a.pos.x, a.pos.z, a.pos.x, a.pos.z, d); if (!spot) return { sp, error: 'no stand spot' };
    P.sim.frozenCamera = false; P.character.root.visible = true; const yaw = Math.atan2(a.pos.x - spot[0], a.pos.z - spot[1]); P.teleport(spot[0], spot[1], yaw + (P.yawOffset || 0)); for (let i = 0; i < settle; i++) P.stepSim(DT);
    const file = `p3b2q-encounter-${name || sp.toLowerCase()}.jpg`; await snap(file, w, h); const cam = camera; const fwd = { x: -Math.sin(Math.atan2(cam.position.x - P.character.root.position.x, cam.position.z - P.character.root.position.z)) };
    return { sp, file, player: [r3(spot[0]), r3(-spot[1])], agent: [r3(a.pos.x), r3(-a.pos.z)], dist: r3(Math.hypot(a.pos.x - P.character.root.position.x, a.pos.z - P.character.root.position.z)), state: a.state, yaw: r3(yaw), cam_to_char_bearing: r3(Math.atan2(cam.position.x - P.character.root.position.x, cam.position.z - P.character.root.position.z)), fwd: r3(fwd.x) };
  }
  // frame sequence: the camera tracks the agent from a fixed bearing; the (hidden) player walks at `speed` m/s toward it from `start` m for `approachFrames` frames, then stands still
  async function strip(label, sp, { k = 0, start = 12, speed = 2.1, frames = 24, every = 8, approachFrames = 12, side = 0.9, dist, w = 640, h = 360, setup, bearing, camLift = 0.35 } = {}) {
    const a = live(sp, k), spec = W.SPECIES[sp]; W.ctl.forceFull = true; const was = P.character.root.visible; P.character.root.visible = false; if (setup) setup(a); else if (a.group === 'ground') W.setState(a, 'IDLE', 20);
    const d0 = dist || Math.max(3, spec.h * 4.2), files = []; let yaw = bearing ?? 0.6; if (bearing == null && a.group === 'ground') for (const off of [0, 0.8, -0.8, 1.6, -1.6, 2.4, -2.4, 3.1]) if (clearBearing(a, d0, 0.6 + off)) { yaw = 0.6 + off; break; } let px = a.pos.x + Math.sin(0.4) * start, pz = a.pos.z + Math.cos(0.4) * start; const spot = standSpot(a.pos.x, a.pos.z, a.pos.x, a.pos.z, start); if (spot) { px = spot[0]; pz = spot[1]; }
    P.character.root.position.set(px, P.heightAt(px, pz), pz);
    for (let f = 0; f < frames; f++) {
      for (let i = 0; i < every; i++) { if (f < approachFrames) { const dx = a.pos.x - px, dz = a.pos.z - pz, dd = Math.hypot(dx, dz) || 1, st = Math.min(speed * DT, dd - 1.2 > 0 ? dd - 1.2 : 0); px += dx / dd * st; pz += dz / dd * st; P.character.root.position.set(px, P.heightAt(px, pz), pz); } P.stepSim(DT); }
      const cx = a.pos.x + Math.sin(yaw) * d0, cz = a.pos.z + Math.cos(yaw) * d0, yy = a.root.position.y; planCam(cx, cz, yy + spec.h * 0.9 + camLift, a.pos.x, a.pos.z, yy + spec.h * 0.45, 40);
      files.push(await snap(`p3b2q-gif-${label}-${String(f).padStart(2, '0')}.jpg`, w, h));
    }
    P.character.root.visible = was; P.sim.frozenCamera = false; W.ctl.forceFull = false; return { label, sp, files: files.length, end_state: a.state, states: a.log.slice(-8) };
  }
  P.wildTests.shots = { portrait, encounter, strip, planCam, snap, live, standSpot };
}
