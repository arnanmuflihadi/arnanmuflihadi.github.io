// Merchant Citadel P3-B batch 2 (animal source change, Quaternius-only ecology): habitat-aware wildlife for the isolated preview.
// Assets: Quaternius Ultimate Animated Animals / Farm Animal Pack / Animals pack (CC0, rigged, real clips: farm animals + pug Idle/Walk/Run, cat/dog Idle/Walking, eagle Flying/Idle,
// fox/chick walk cycle, bird flap cycle) plus the Gobkit Swallowtail (CC0, fly / perch). Every rig is skinned and cloned with the vendored cloneSkeleton. Animals are drawn at natural size.
//   * rigs with an Idle clip use it; rigs with a single action (fox, chick, bird) hold a standing frame (idleT) when idle and play the action when moving / flying
//   * run (FLEE) uses the Run clip where one exists, otherwise the walk clip at a higher rate; clip rate follows ground speed (foot-slide control via cs / csr, m/s at rate 1)
//   * grazing / rooting: Neck + Head bone pitch added after the mixer update (rigs with named bones: farm animals)
//   * birds and the eagle fly with their real clips (no procedural wing code); the small bird perches on roofs / rocks / props and hops between perches, the eagle soars on the crag
// Movement validates every step against the terrain (walk mask, slope, step height), the town obstacles and the dragon-landing keep-outs. No agent is simulated beyond 90 m.
const TAU = Math.PI * 2;
export const SPECIES = {
  // kind, h = natural standing height m (from the posed bounds), walk / flee speed m/s, cs / csr = ground speed one rate-1 walk / run cycle covers, alert / flee distance, activity radius, weights {wander, graze, rest, look}
  Sheep: { kind: 'ground', m: 0.45, h: 0.9, walk: 0.7, flee: 2.8, cs: 0.9, csr: 3.0, alert: 6, fleeAt: 3, radius: 8, graze: true, w: [3, 6, 2, 1] },
  Lamb: { kind: 'ground', m: 0.35, file: 'Sheep', h: 0.6, walk: 0.8, flee: 3.2, cs: 0.7, csr: 2.4, alert: 6, fleeAt: 2.6, radius: 7, graze: true, w: [4, 4, 1, 2], follow: 'Sheep' },
  Cow: { kind: 'ground', m: 0.75, h: 1.4, walk: 0.6, flee: 2.6, cs: 1.1, csr: 3.6, alert: 6, fleeAt: 3, radius: 8, graze: true, w: [2, 6, 4, 1] },
  Horse: { kind: 'ground', m: 0.8, h: 1.7, walk: 0.9, flee: 5.0, cs: 1.4, csr: 5.5, alert: 10, fleeAt: 5, radius: 10, graze: true, w: [3, 5, 2, 3] },
  Llama: { kind: 'ground', m: 0.55, h: 1.6, walk: 0.8, flee: 4.0, cs: 1.2, csr: 4.5, alert: 9, fleeAt: 4.5, radius: 9, graze: false, w: [3, 0, 4, 4] },
  Pig: { kind: 'ground', m: 0.5, h: 0.85, walk: 0.6, flee: 3.2, cs: 0.8, csr: 3.2, alert: 5, fleeAt: 2.4, radius: 5, graze: true, w: [3, 5, 2, 1] },
  Pug: { kind: 'ground', m: 0.3, h: 0.4, walk: 0.9, flee: 3.0, cs: 0.8, csr: 3.0, alert: 6, fleeAt: 0, radius: 6, graze: false, w: [3, 0, 5, 2], calm: true },
  Dog: { kind: 'ground', m: 0.4, h: 0.65, walk: 1.0, flee: 3.5, cs: 0.9, alert: 7, fleeAt: 0, radius: 7, graze: false, w: [3, 0, 4, 3], calm: true },
  Cat: { kind: 'ground', m: 0.28, h: 0.3, walk: 0.7, flee: 4.2, cs: 0.6, alert: 7, fleeAt: 3.5, radius: 5, graze: false, w: [3, 0, 5, 2], cover: true },
  RedFox: { kind: 'ground', m: 0.35, h: 0.5, walk: 1.0, flee: 5.5, cs: 1.0, alert: 16, fleeAt: 10, radius: 9, graze: false, w: [4, 0, 3, 4], cover: true },
  Chick: { kind: 'ground', m: 0.25, h: 0.2, walk: 0.45, flee: 2.0, cs: 0.35, alert: 3, fleeAt: 1.8, radius: 3, graze: false, w: [5, 0, 1, 1] },
  Bird: { kind: 'flyer', h: 0.3, speed: 4.2, rate: 1, flyRate: 1.0 }, Eagle: { kind: 'flyer', h: 0.8, speed: 7.0, rate: 1, flyRate: 1.0, soar: true },
  Swallowtail: { kind: 'butterfly', h: 0.22, speed: 0.9, file: 'Swallowtail' },
};

function rng32(seed) { let s = seed >>> 0 || 1; return () => { s ^= s << 13; s >>>= 0; s ^= s >>> 17; s ^= s << 5; s >>>= 0; return s / 4294967296; }; }
const wrap = (a) => { while (a > Math.PI) a -= TAU; while (a < -Math.PI) a += TAU; return a; };

const GRAZE = { head: -0.75, neck: -0.55 };                                   // bone pitch (rad) added to Head / Neck while grazing or rooting; negative = down; sign and size verified on the farm rigs, evidence p3b2q-grazetest*
export async function createWildlife(T, { scene, isl, heightAt, blockedFn, obstaclesRef, flora, params, say = () => {}, seed = 7 }) {
  const rnd = rng32(seed), R = (a, b) => a + (b - a) * rnd(), pick = (arr) => arr[Math.floor(rnd() * arr.length)];
  const loader = new T.GLTFLoader(), protos = {};
  const names = new Set(); const hab = flora.habitats;
  for (const h of Object.values(hab)) for (const [sp, n] of Object.entries(h.species)) if (n > 0 && SPECIES[sp]) names.add(sp);
  say('loading wildlife (' + names.size + ' species)…'); const t0 = performance.now();
  const WSCALE = Number(params.get('wscale') || 1);                       // owner review knob: ?wscale=1.3 draws every animal 30 % larger (default natural size)
  const cache = {};                                                      // one GLB fetch per file (Lamb reuses the Sheep file)
  const fileOf = (sp) => SPECIES[sp].file || sp, urlOf = (sp) => (sp === 'Swallowtail' ? 'assets-p3b2/fauna/' : 'assets-p3b2/fauna-q/') + fileOf(sp) + '.glb';
  await Promise.all([...names].map(async (sp) => {
    const spec = SPECIES[sp]; const url = urlOf(sp); const g = await (cache[url] ||= loader.loadAsync(url)); g.scene.updateMatrixWorld(true);
    const cl = Object.fromEntries(g.animations.map((a) => [a.name, a])), nm = Object.keys(cl), single = nm.length === 1 ? cl[nm[0]] : null;
    // clip aliases: the packs name their clips differently (Idle / Walk / Walking / Run / Flying / ArmatureAction*)
    const alias = { idle: cl.Idle || cl.idle, walk: cl.Walk || cl.Walking || cl.walk || (spec.kind === 'ground' ? single : null), run: cl.Run || cl.run, fly: cl.Flying || cl.fly || (spec.kind === 'flyer' ? single : null), perch: cl.perch };
    for (const k of Object.keys(alias)) if (!alias[k]) delete alias[k];
    // white wool / feathers clip in this scene's lighting (env 2.0, sun 4.2): fauna albedo x0.86
    g.scene.traverse((o) => { if (o.isMesh) for (const m of [].concat(o.material)) if (!m.userData.p3b2) { m.userData.p3b2 = 1; m.metalness = 0; m.roughness = Math.max(m.roughness ?? 0.9, 0.85); if (sp !== 'Swallowtail' && m.color) m.color.multiplyScalar(0.86); } });
    const mixer = new T.AnimationMixer(g.scene); const pose = alias.idle || alias.walk || alias.fly; const act = mixer.clipAction(pose); act.play(); mixer.setTime(alias.idle ? 0.3 : (spec.idleT || 0) * pose.duration); g.scene.updateMatrixWorld(true);
    const b = new T.Box3().setFromObject(g.scene, true), size = b.getSize(new T.Vector3());
    const dim = spec.kind === 'ground' ? size.y : Math.max(size.x, size.y, size.z); const k = spec.h * WSCALE / dim;      // natural size, no apparent-size boost
    mixer.stopAllAction(); mixer.uncacheRoot(g.scene);
    protos[sp] = { gltf: g, k, yoff: -b.min.y * k, raw: [size.x, size.y, size.z], clips: cl, alias };
  }));
  const loadMs = performance.now() - t0;
  const forbidden = (x, n) => flora.keepouts.some((k) => Math.hypot(x - k.x, n - k.n) < k.r);
  const obsList = () => obstaclesRef();
  let curM = 0.28;                                                         // obstacle margin (m) of the agent being simulated: big animals keep further from walls
  const groundOk = (x, z, prevY) => { if (!isl.walkable(x, z)) return false; if (forbidden(x, -z)) return false; if (blockedFn(x, z, obsList(), curM)) return false; const y = heightAt(x, z); if (y < -50 || (prevY !== undefined && Math.abs(y - prevY) > 0.3)) return false; return Math.hypot(heightAt(x + 0.4, z) - heightAt(x - 0.4, z), heightAt(x, z + 0.4) - heightAt(x, z - 0.4)) / 0.8 <= 0.5; };       // walk mask, keep-outs, obstacles, step height and slope <= 0.5

  const snapFree = (x, z) => { if (groundOk(x, z)) return [x, z]; for (let r = 0.5; r <= 8; r += 0.5) for (let k = 0; k < 16; k++) { const a = k * TAU / 16, px = x + Math.cos(a) * r, pz = z + Math.sin(a) * r; if (groundOk(px, pz)) return [px, pz]; } return [x, z]; };
  const agents = []; const group = new T.Group(); group.name = 'WILDLIFE'; scene.add(group);
  function build(sp, hid) {
    const P = protos[sp]; const root = new T.Group(); root.name = 'W_' + sp; const model = T.cloneSkeleton(P.gltf.scene); model.scale.setScalar(P.k); model.position.y = P.yoff; root.add(model); group.add(root);
    const mixer = new T.AnimationMixer(model), act = {}; for (const [n, c] of Object.entries(P.alias)) act[n] = mixer.clipAction(c);
    let head = null, neck = null; model.traverse((o) => { if (o.isBone) { if (o.name === 'Head') head = o; else if (o.name === 'Neck') neck = o; } if (o.isSkinnedMesh) { o.castShadow = true; o.frustumCulled = false; } });
    const a = { sp, hid, spec: SPECIES[sp], root, model, mixer, act, head, neck, cur: null, stat: false, state: 'IDLE', t: 0, timer: R(1, 4), pos: root.position, yaw: R(0, TAU), tx: 0, tz: 0, home: null, graze: 0, alertT: 0, fleeT: 0, calm: 0, accum: 0, lod: 0, phase: R(0, TAU), stuck: 0, log: [] };
    play(a, a.spec.kind === 'butterfly' ? 'fly' : 'idle', R(0, 1)); return a;
  }
  // clip alias layer: 'idle' falls back to a held standing frame of the walk / fly action (speed 0); 'run' falls back to the walk clip; 'walk' / 'fly' fall back to idle
  function play(a, name, offset = 0, speed = 1) {
    let n = name, sp = speed;
    if (!a.act[n]) { if (n === 'idle') { n = a.act.walk ? 'walk' : a.act.fly ? 'fly' : null; sp = 0; } else if (n === 'run') n = a.act.walk ? 'walk' : null; else n = a.act.idle ? 'idle' : null; }
    if (!n) return; const next = a.act[n], dur = next.getClip().duration || 1, stat = name === 'idle' && n !== 'idle', t = (a.spec.idleT || 0) * dur;
    if (a.cur === n) { if (stat && !a.stat) next.time = t; a.stat = stat; next.timeScale = sp; return; }
    next.reset(); next.setEffectiveTimeScale(sp); next.setEffectiveWeight(1); next.time = stat ? t : offset * dur; if (a.cur) a.act[a.cur].crossFadeTo(next, 0.25, false); next.play(); a.cur = n; a.stat = stat;
  }
  const setState = (a, s, t = 0) => { if (a.state !== s) { a.log.push(s); if (a.log.length > 12) a.log.shift(); } a.state = s; a.t = 0; a.timer = t; };

  // ---------------------------------------------------------------------------------------------- spawn
  const used = {};
  for (const [hid, h] of Object.entries(hab)) {
    for (const [sp, n] of Object.entries(h.species)) {
      if (!n || !protos[sp]) continue; const spec = SPECIES[sp];
      if (spec.kind === 'ground') {
        const homes = (h.homes[sp] || []).slice(); for (let i = 0; i < n && homes.length; i++) { const k = Math.floor(rnd() * homes.length), [hx, hn] = homes.splice(k, 1)[0]; const a = build(sp, hid); curM = spec.m || 0.28; const [sx, sz] = snapFree(hx, -hn); a.home = { x: sx, z: sz }; a.pos.set(sx, heightAt(sx, sz), sz); a.yaw = R(0, TAU); a.group = 'ground'; agents.push(a); }
      } else if (spec.kind === 'perch' || spec.kind === 'flyer') { for (let i = 0; i < n; i++) { const a = build(sp, hid); a.group = 'bird'; agents.push(a); } }
      else if (spec.kind === 'butterfly') { for (let i = 0; i < n; i++) { const a = build(sp, hid); a.group = 'butterfly'; agents.push(a); } }
    }
  }
  // perch sites
  const roofs = flora.perches.roof, rocks = flora.perches.rock, trees = flora.perches.tree, props = flora.perches.prop;
  const perchPool = { roof: roofs.map((r) => ({ x: r.x + R(-r.w / 4, r.w / 4), z: -(r.n + R(-r.d / 4, r.d / 4)), y: r.z, kind: 'roof', src: r.src })), rock: rocks.map(([x, n, z]) => ({ x, z: -n, y: z, kind: 'rock' })), tree: trees.map(([x, n, z]) => ({ x, z: -n, y: z, kind: 'tree' })), prop: props.map((p) => ({ x: p.x, z: -p.n, y: p.z, kind: 'prop', src: p.name })) };
  const taken = new Set(); const takePerch = (list) => { const free = list.filter((p) => !taken.has(p)); const p = free.length ? pick(free) : pick(list); taken.add(p); return p; };
  const pool = (kinds, filt) => kinds.flatMap((k) => perchPool[k]).filter((p) => !forbidden(p.x, -p.z)).filter(filt || (() => true));          // no perches inside the dragon-landing keep-outs
  for (const a of agents.filter((q) => q.group === 'bird')) {
    const sp = a.sp; let list; const H = a.hid[0], near = (cx, cz, r) => (p) => Math.hypot(p.x - cx, p.z - cz) < r;
    if (sp === 'Bird') {                                                  // one small songbird, habitat decides the perch family (all perch sites exclude the dragon-landing keep-outs)
      list = H === 'A' ? pool(['roof']) : H === 'F' ? pool(['prop'], (p) => p.src === 'pavilion roof') : H === 'G' ? pool(['prop'], (p) => p.src !== 'pavilion roof')
        : H === 'C' ? pool(['rock'], near(46, -110, 45)) : H === 'D' ? pool(['roof', 'rock', 'tree'], near(70, -42, 46)) : H === 'E' ? pool(['rock', 'tree'], near(72, -80, 30)) : pool(['rock', 'tree'], near(-50, -18, 30));
    } else list = null;                                                   // eagle: soaring patrol
    if (list && !list.length) list = pool(['rock', 'tree']);
    a.perch = list ? takePerch(list) : null; a.perchList = list || [];
    if (a.perch) { a.pos.set(a.perch.x, a.perch.y, a.perch.z); a.home = { x: a.perch.x, z: a.perch.z }; a.state = 'PERCHED'; a.timer = R(8, 30); }
    else { // eagle: thermal circle over the crag
      const c = { x: 46, z: -110, r: R(20, 34), y: 38, dir: rnd() < 0.5 ? 1 : -1 }; a.orbit = c; a.state = 'CIRCLE'; a.t = R(0, TAU); a.pos.set(c.x + c.r, c.y, c.z);
    }
    a.yaw = R(0, TAU);
  }
  const fl = flora.data.instances; const flowerSpots = ['Flower_3_Single', 'Flower_4_Single', 'Flower_3_Group', 'Flower_4_Group'].flatMap((k) => fl[k] || []);
  for (const a of agents.filter((q) => q.group === 'butterfly')) {
    const zones = { B: [-50, -18, 17], D: [70, -42, 24], E: [72, -66, 12], F: [32, -55, 12] }; const z = zones[a.hid[0]] || zones.B;
    const near = flowerSpots.filter(([x, n]) => Math.hypot(x - z[0], -n - z[1]) < z[2]); a.flowers = (near.length ? near : flowerSpots).map(([x, n, h]) => ({ x, z: -n, y: h })); a.zone = { x: z[0], z: z[1], r: z[2] };
    const f = pick(a.flowers); a.pos.set(f.x, f.y + 1.0, f.z); a.target = f; a.state = 'FLY'; a.bf = R(0, TAU);
  }
  const ground = agents.filter((a) => a.group === 'ground');
  // lambs follow a sheep
  for (const a of ground) if (a.spec.follow) { const lead = ground.find((q) => q.sp === a.spec.follow && q.hid === a.hid); if (lead) { a.leader = lead; a.home = { ...lead.home }; curM = a.spec.m || 0.28; const [sx, sz] = snapFree(lead.pos.x + R(-2.5, 2.5), lead.pos.z + R(-2.5, 2.5)); a.pos.set(sx, heightAt(sx, sz), sz); } }

  // ---------------------------------------------------------------------------------------------- behaviour
  const P0 = { x: 0, z: 0, y: 0 };
  const faceTo = (a, tx, tz, dt, rate = 4) => { const want = Math.atan2(tx - a.pos.x, tz - a.pos.z); a.yaw += wrap(want - a.yaw) * Math.min(1, rate * dt); };
  function step(a, dx, dz) { const x = a.pos.x + dx, z = a.pos.z + dz; const y0 = a.pos.y; if (groundOk(x, z, y0)) { a.pos.x = x; a.pos.z = z; a.pos.y = heightAt(x, z); return true; } if (groundOk(a.pos.x + dx, a.pos.z, y0)) { a.pos.x += dx; a.pos.y = heightAt(a.pos.x, a.pos.z); return true; } if (groundOk(a.pos.x, a.pos.z + dz, y0)) { a.pos.z += dz; a.pos.y = heightAt(a.pos.x, a.pos.z); return true; } return false; }
  function chooseWander(a) {
    const home = a.leader ? a.leader.pos : a.home, r = a.spec.radius;
    for (let i = 0; i < 14; i++) { const ang = R(0, TAU), d = R(1.5, Math.min(6, r)), x = home.x + Math.cos(ang) * R(0, r) * 0.9, z = home.z + Math.sin(ang) * R(0, r) * 0.9; if (Math.hypot(x - a.pos.x, z - a.pos.z) < 1.2) continue; if (groundOk(x, z)) { a.tx = x; a.tz = z; return true; } }
    return false;
  }
  const lineOk = (x0, z0, x1, z1) => { const n = Math.ceil(Math.hypot(x1 - x0, z1 - z0) / 0.8); let py = heightAt(x0, z0); for (let i = 1; i <= n; i++) { const x = x0 + (x1 - x0) * i / n, z = z0 + (z1 - z0) * i / n; if (!groundOk(x, z, py)) return false; py = heightAt(x, z); } return true; };
  function chooseFlee(a, px, pz) {
    let best = null, bs = -1e9; const home = a.home; const away = Math.atan2(a.pos.z - pz, a.pos.x - px);
    for (let k = 0; k < 24; k++) for (const d of [4, 8, 12]) { const ang = k * TAU / 24 + R(-0.1, 0.1), x = a.pos.x + Math.cos(ang) * d, z = a.pos.z + Math.sin(ang) * d; if (!groundOk(x, z) || !lineOk(a.pos.x, a.pos.z, x, z)) continue;
      let s = Math.hypot(x - px, z - pz) - Math.hypot(a.pos.x - px, a.pos.z - pz) * 0.5 + d * 0.15; if (a.spec.cover && coverNear(x, z, 3.5)) s += 4; if (Math.hypot(x - home.x, z - home.z) > a.spec.radius * 2.6) s -= 6; if (Math.abs(wrap(ang - away)) > 1.9) s -= 3; if (s > bs) { bs = s; best = [x, z]; } }
    if (!best) { const ang = away + (rnd() < 0.5 ? 1.57 : -1.57); best = [a.pos.x + Math.cos(ang) * 3, a.pos.z + Math.sin(ang) * 3]; }
    a.tx = best[0]; a.tz = best[1];
  }
  const coverPts = [...(flora.data.instances.Bush_Common || []), ...(flora.data.instances.Bush_Common_Flowers || [])].map(([x, n]) => [x, -n]).concat((flora.data.trunks || []).map((t) => [t.x, -t.n]));
  const coverNear = (x, z, r) => coverPts.some(([cx, cz]) => Math.hypot(cx - x, cz - z) < r);

  function updateGround(a, dt, px, pz, dp) {
    const sp = a.spec; curM = sp.m || 0.28; a.t += dt; a.timer -= dt; a.habit = Math.max(0, (a.habit || 0) - dt); const toHome = a.home ? Math.hypot(a.pos.x - a.home.x, a.pos.z - a.home.z) : 0; let moveSpeed = 0, anim = 'idle', animSpeed = 1, headDown = 0;
    // player reaction
    if (!sp.calm && sp.fleeAt > 0) {
      if (a.state !== 'FLEE' && dp < sp.fleeAt) { chooseFlee(a, px, pz); setState(a, 'FLEE', R(2.5, 4)); a.fleeT = 0; }
      else if (['IDLE', 'GRAZE', 'WANDER', 'REST', 'LOOK_AROUND', 'RETURN_TO_HABITAT'].includes(a.state) && dp < sp.alert && !(a.habit > 0)) { setState(a, 'ALERT', R(1.2, 2.2)); }
    }
    switch (a.state) {
      case 'IDLE': case 'REST': case 'LOOK_AROUND': case 'GRAZE': {
        if (a.state === 'LOOK_AROUND') a.yaw += Math.sin(a.t * 1.5 + a.phase) * dt * 0.9; if (a.state === 'GRAZE' && sp.graze) headDown = 1; if (a.state === 'REST') animSpeed = 0.6;
        if (a.timer <= 0) { const w = sp.w, tot = w[0] + w[1] + w[2] + w[3]; let r = rnd() * tot; const choice = r < w[0] ? 'WANDER' : (r -= w[0]) < w[1] ? 'GRAZE' : (r -= w[1]) < w[2] ? 'REST' : 'LOOK_AROUND';
          if (choice === 'WANDER') { if (chooseWander(a)) setState(a, 'WANDER', 20); else setState(a, 'IDLE', R(2, 5)); } else setState(a, choice === 'GRAZE' && !sp.graze ? 'IDLE' : choice, choice === 'REST' ? R(6, 16) : choice === 'GRAZE' ? R(4, 10) : R(2, 5)); }
        break; }
      case 'WANDER': case 'RETURN_TO_HABITAT': {
        const tx = a.state === 'RETURN_TO_HABITAT' ? a.home.x : a.tx, tz = a.state === 'RETURN_TO_HABITAT' ? a.home.z : a.tz, d = Math.hypot(tx - a.pos.x, tz - a.pos.z); faceTo(a, tx, tz, dt); anim = 'walk'; moveSpeed = sp.walk * (a.leader ? 1.15 : 1);
        if (d < 0.6 || a.t > 25) setState(a, 'IDLE', R(1.5, 4)); else if (a.stuck > 1.2) { setState(a, 'IDLE', R(1, 2)); a.stuck = 0; }
        break; }
      case 'ALERT': { faceTo(a, px, pz, dt, 6); if (dp > sp.alert * 1.5) setState(a, 'IDLE', R(1, 3)); else if (a.timer <= 0) { if (dp > sp.fleeAt * 1.3) a.habit = 14; setState(a, 'LOOK_AROUND', R(1, 2.5)); } break; }
      case 'FLEE': { a.fleeT += dt; faceTo(a, a.tx, a.tz, dt, 9); anim = 'run'; moveSpeed = sp.flee; const d = Math.hypot(a.tx - a.pos.x, a.tz - a.pos.z);
        if (a.stuck > 0.5 && dp < 2.5) { a.cornered = (a.cornered || 0) + dt; if (a.cornered > 0.7) { let moved = false; for (let i = 0; i < 40 && !moved; i++) { const ang = R(0, TAU), dd = R(6, 12), x = a.pos.x + Math.cos(ang) * dd, z = a.pos.z + Math.sin(ang) * dd; if (groundOk(x, z) && Math.hypot(x - px, z - pz) > 5) { a.pos.set(x, heightAt(x, z), z); moved = true; stats.relocations++; a.log.push('CORNERED_RELOCATE'); } } a.cornered = 0; setState(a, 'ALERT', 1.5); a.stuck = 0; break; } } else a.cornered = 0;
        if (d < 0.8 || a.stuck > 0.5) { if (dp < sp.fleeAt * 1.3 && a.fleeT < 5) { chooseFlee(a, px, pz); a.stuck = 0; } else setState(a, 'ALERT', 1.5); }
        else if (a.fleeT > sp.fleeAt && dp > sp.alert) setState(a, 'RETURN_TO_HABITAT', 0);
        break; }
    }
    if (a.state === 'ALERT' && a.timer < 0 && dp > sp.alert * 1.4) setState(a, toHome > sp.radius * 1.2 ? 'RETURN_TO_HABITAT' : 'IDLE', 1);
    if (['IDLE', 'GRAZE', 'REST', 'LOOK_AROUND'].includes(a.state) && toHome > sp.radius * 1.4) setState(a, 'RETURN_TO_HABITAT', 0);
    if (moveSpeed > 0) { const sx = Math.sin(a.yaw) * moveSpeed * dt, sz = Math.cos(a.yaw) * moveSpeed * dt; if (!step(a, sx, sz)) a.stuck += dt; else a.stuck = Math.max(0, a.stuck - dt * 0.5); }
    // foot-slide control: the clip rate follows ground speed (cs / csr = ground speed one rate-1 cycle covers); rigs without a Run clip run their walk cycle faster
    if (anim === 'idle') play(a, 'idle', 0, animSpeed); else { const ref = anim === 'run' && a.act.run ? (sp.csr || sp.cs) : sp.cs; play(a, anim, 0, Math.max(0.4, Math.min(2.8, moveSpeed / ref))); }
    a.headDown += ((headDown ? 1 : 0) - a.headDown) * Math.min(1, dt * 4);
    // slope alignment (pitch/roll from heights 0.3 m ahead/aside)
    const sx = Math.sin(a.yaw), cz = Math.cos(a.yaw); const hf = heightAt(a.pos.x + sx * 0.3, a.pos.z + cz * 0.3), hb = heightAt(a.pos.x - sx * 0.3, a.pos.z - cz * 0.3), hr = heightAt(a.pos.x + cz * 0.25, a.pos.z - sx * 0.25), hl = heightAt(a.pos.x - cz * 0.25, a.pos.z + sx * 0.25);
    const pitch = Math.atan2(hf - hb, 0.6), roll = Math.atan2(hr - hl, 0.5); a.root.rotation.set(Math.max(-0.35, Math.min(0.35, -pitch)), a.yaw, Math.max(-0.3, Math.min(0.3, roll)), 'YXZ');
  }
  function updatePerched(a, dt, px, pz, dp) {
    a.t += dt; a.timer -= dt; play(a, 'idle', 0, 1);
    if (a.state === 'PERCHED') { a.yaw += Math.sin(a.t * 0.7 + a.phase) * dt * 0.8; if (a.spec.kind === 'flyer' && a.flies !== false && (dp < 7 && a.spec.kind === 'flyer' || a.timer <= 0)) startFlight(a, dp < 7 ? px : null, pz); }
    a.pos.set(a.pos.x, a.perch ? a.perch.y : a.pos.y, a.pos.z); a.root.rotation.set(0, a.yaw, 0);
  }
  const FLIERS = new Set(['Bird', 'Eagle']);
  function startFlight(a, px, pz) {
    if (!FLIERS.has(a.sp)) return; const list = a.perchList.filter((p) => p !== a.perch); if (!list.length) { a.legs = [a.perch]; const E = { x: a.pos.x + R(-22, 22), y: a.pos.y + R(8, 14), z: a.pos.z + R(-22, 22) }; a.dest = E; a.from = { x: a.pos.x, y: a.pos.y, z: a.pos.z }; a.flightT = 0; a.flightDur = 6; a.arcH = 3; setState(a, 'TAKEOFF', 0); return; }
    const far = list.filter((p) => Math.hypot(p.x - a.pos.x, p.z - a.pos.z) > 12 && Math.hypot(p.x - a.pos.x, p.z - a.pos.z) < 90); const tgt = far.length ? pick(far) : pick(list); a.dest = tgt; a.from = { x: a.pos.x, y: a.pos.y, z: a.pos.z }; a.flightT = 0; const d = Math.hypot(tgt.x - a.pos.x, tgt.z - a.pos.z); a.flightDur = Math.max(3, d / a.spec.speed + 2); a.arcH = Math.max(3, d * 0.18); setState(a, 'TAKEOFF', 0);
  }
  function updateFlyer(a, dt, px, pz, dp) {
    const sp = a.spec; a.t += dt; a.timer -= dt;
    if (a.state === 'PERCHED') { updatePerched(a, dt, px, pz, dp); return; }
    if (a.state === 'TAKEOFF' || a.state === 'FLY' || a.state === 'LAND') {
      a.flightT += dt; const u = Math.min(1, a.flightT / a.flightDur), e = u * u * (3 - 2 * u); const d = a.dest, f = a.from;
      const x = f.x + (d.x - f.x) * e, z = f.z + (d.z - f.z) * e, y = f.y + (d.y - f.y) * e + Math.sin(Math.PI * e) * a.arcH; const nx = f.x + (d.x - f.x) * Math.min(1, e + 0.02), nz = f.z + (d.z - f.z) * Math.min(1, e + 0.02);
      const prevYaw = a.yaw; a.yaw += wrap(Math.atan2(nx - x, nz - z) - a.yaw) * Math.min(1, dt * 5); a.pos.set(x, y, z);
      const bank = Math.max(-0.5, Math.min(0.5, wrap(a.yaw - prevYaw) * 9)), pitch = -Math.cos(Math.PI * e) * 0.35; a.root.rotation.set(pitch, a.yaw, -bank, 'YXZ');
      play(a, 'fly', 0, sp.flyRate * (u < 0.15 || u > 0.85 ? 1.35 : 1)); a.state = u < 0.15 ? 'TAKEOFF' : u > 0.85 ? 'LAND' : 'FLY';
      if (u >= 1 && a.legs && a.legs.length) { a.from = { x: a.pos.x, y: a.pos.y, z: a.pos.z }; a.dest = a.legs.shift(); a.flightT = 0; a.flightDur = 7; a.arcH = 2; return; }
      if (u >= 1) { a.perch = d; a.home = { x: d.x, z: d.z }; a.pos.set(d.x, d.y, d.z); setState(a, 'PERCHED', R(10, 40)); a.root.rotation.set(0, a.yaw, 0); play(a, 'idle', 0, 1); }
      return;
    }
    if (a.state === 'CIRCLE') {
      const o = a.orbit; const w = (sp.speed / o.r) * o.dir; a.ang = (a.ang ?? a.phase) + w * dt;
      const x = o.x + Math.cos(a.ang) * o.r, z = o.z + Math.sin(a.ang) * o.r, y = o.y + Math.sin(a.ang * 2 + a.phase) * 2.5; const nx = o.x + Math.cos(a.ang + 0.05 * o.dir) * o.r, nz = o.z + Math.sin(a.ang + 0.05 * o.dir) * o.r;
      a.yaw = Math.atan2(nx - x, nz - z); a.pos.set(x, y, z); a.root.rotation.set(-0.08, a.yaw, -0.45 * o.dir * (sp.soar ? 1 : 0.6), 'YXZ');
      play(a, 'fly', 0, sp.soar ? 0.55 + 0.25 * Math.sin(a.t * 0.5) : sp.flyRate);
    }
  }
  function updateButterfly(a, dt) {
    a.t += dt; a.timer -= dt; const sp = a.spec;
    if (a.state === 'PERCH') { play(a, 'perch', 0, 1); if (a.timer <= 0) { a.target = pick(a.flowers); setState(a, 'FLY', 0); } return; }
    play(a, 'fly', 0, 1.2); const tg = a.target; if (!tg) return; const ty = tg.y + 0.55 + Math.sin(a.t * 2 + a.phase) * 0.35; const dx = tg.x + Math.sin(a.t * 1.3 + a.phase) * 0.9 - a.pos.x, dz = tg.z + Math.cos(a.t * 1.1 + a.phase) * 0.9 - a.pos.z, dy = ty - a.pos.y, d = Math.hypot(dx, dz);
    const v = sp.speed * (0.7 + 0.3 * Math.sin(a.t * 3 + a.phase)); a.pos.x += dx / (d + 0.01) * Math.min(v * dt, d); a.pos.z += dz / (d + 0.01) * Math.min(v * dt, d); a.pos.y += Math.max(-1, Math.min(1, dy)) * dt * 1.5 + Math.sin(a.t * 9 + a.phase) * 0.004;
    a.pos.y = Math.max(a.pos.y, heightAt(a.pos.x, a.pos.z) + 0.25); a.yaw += wrap(Math.atan2(dx, dz) - a.yaw) * Math.min(1, dt * 3); a.root.rotation.set(0.15, a.yaw, Math.sin(a.t * 2 + a.phase) * 0.25, 'YXZ');
    if (d < 0.5 && a.timer <= 0) { if (rnd() < 0.5) { setState(a, 'PERCH', R(3, 8)); a.pos.y = tg.y + 0.35; } else { a.target = pick(a.flowers); a.timer = R(1, 3); } }
  }
  for (const a of agents) { a.headDown = 0; if (a.group === 'butterfly') a.timer = R(1, 3); }

  // ---------------------------------------------------------------------------------------------- update loop with distance throttling
  const ctl = { forceFull: false }; const stats = { relocations: 0, agents: agents.length, simulated: 0, mixers: 0, visible: 0, ms: 0, frames: 0, lastMs: 0 }; let frame = 0;
  function update(dt, player, cam) {
    const t0 = performance.now(); frame++; stats.simulated = 0; stats.mixers = 0; stats.visible = 0; const px = player.x, pz = player.z;
    for (const a of agents) {
      const cdx = a.pos.x - cam.x, cdz = a.pos.z - cam.z, cd = Math.hypot(cdx, cdz, a.pos.y - cam.y), dp = Math.hypot(a.pos.x - px, a.pos.z - pz);
      if (cd > 130 && !ctl.forceFull) { a.root.visible = false; continue; } a.root.visible = true; stats.visible++;
      a.accum += dt; const lod = ctl.forceFull ? 0 : cd < 32 ? 0 : cd < 70 ? 1 : 2; const every = lod === 0 ? 1 : lod === 1 ? 3 : 8; if ((frame + (a.phase * 7 | 0)) % every !== 0) continue; const sdt = Math.min(a.accum, 0.25); a.accum = 0; stats.simulated++;
      if (a.group === 'ground') updateGround(a, sdt, px, pz, dp); else if (a.group === 'bird') { if (a.spec.kind === 'perch' || !FLIERS.has(a.sp)) updatePerched(a, sdt, px, pz, dp); else updateFlyer(a, sdt, px, pz, dp); } else updateButterfly(a, sdt);
      a.root.position.copy(a.pos);
      if (lod < 2) { a.mixer.update(sdt); stats.mixers++; }
      if (a.head && a.headDown > 0.01) { a.head.rotation.x += a.headDown * GRAZE.head; if (a.neck) a.neck.rotation.x += a.headDown * GRAZE.neck; }
      const sh = cd < 26; a.model.traverse((o) => { if (o.isSkinnedMesh && o.castShadow !== sh) o.castShadow = sh; });
    }
    stats.lastMs = performance.now() - t0; stats.ms += stats.lastMs; stats.frames++;
  }
  const summary = () => { const by = {}; for (const a of agents) { const k = a.sp; (by[k] ||= { n: 0, kind: a.spec.kind, states: {} }).n++; by[k].states[a.state] = (by[k].states[a.state] || 0) + 1; } return by; };
  // demo / inspection helper: a posed, un-simulated clone (not part of `agents`)
  function demo(sp, x, z, yaw, clip, t, graze = 0, grp = group) {
    const a = build(sp, 'demo'); { const ix = agents.indexOf(a); if (ix >= 0) agents.splice(ix, 1); } grp.add(a.root); a.pos.set(x, heightAt(x, z), z); a.root.position.copy(a.pos); a.root.rotation.set(0, yaw, 0);
    const key = a.act[clip] ? clip : clip === 'idle' ? (a.act.walk ? 'walk' : 'fly') : clip === 'run' ? 'walk' : 'idle'; for (const n of Object.keys(a.act)) a.act[n].stop(); const c = a.act[key]; c.reset(); c.setEffectiveTimeScale(1); c.setEffectiveWeight(1); c.play(); a.mixer.setTime(t); a.cur = key; a.stat = false;
    if (graze && a.head) { a.head.rotation.x += graze * GRAZE.head; if (a.neck) a.neck.rotation.x += graze * GRAZE.neck; } a.root.updateMatrixWorld(true); return a;
  }
  return { ctl, demo, build, agents, update, stats, protos, summary, loadMs, group, SPECIES, groundOk, forbidden, perchPool, setState, play, startFlight };
}
