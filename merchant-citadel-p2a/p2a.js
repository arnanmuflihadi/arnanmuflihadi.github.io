// Merchant Citadel P2-A vertical slice: isolated preview.
// Uses the game's own, unmodified character, player controller, follow camera, input and island collision modules.
// Everything else (world loading, lighting, height field, collision proxies, tests) lives in this folder.
import * as T from '../assets/js/vendor/three-atlas.module.js?v=16';
import { createCharacter } from '../assets/js/urban-atlas/character.js?v=50';
import { createFollowCamera } from '../assets/js/urban-atlas/camera.js?v=e1c';
import { createInput } from '../assets/js/urban-atlas/input.js?v=22';
import { blocked, slide, clearDistance } from '../assets/js/floating-atlas/collision.js?v=73';
import { installTests } from './p2a-tests.js';
import { dedupeMaterials, mergeByGroup, fitSunShadow, dequantizeKit } from './loader.js';
import { loadIsland } from './island.js';
import { installIslandTests } from './p3b-tests.js';
import { createWildlife } from './wildlife.js';
import { installWildTests } from './p3b2-tests.js';
import { installB3Tests } from './p3b3-tests.js';
import { FIX_DATA, fixFlags, cutDressing, openGates, removeRailProxies, cameraTransparent, addSigns, addGapProps } from './p3b-fixes.js';

const params = new URLSearchParams(location.search);
const opt = { tone: params.get('tm') || 'neutral', shadows: params.get('shadows') !== '0', merge: params.get('merge') || 'cell30', matcache: params.get('matcache') !== '0', prewarm: params.get('prewarm') !== '0', smap: Number(params.get('smap') || 2048), autotest: params.get('autotest') || '', size: params.get('size') || '', island: params.get('island') !== '0' };      // P3-B batch 1: the floating island is on by default; ?island=0 restores the P2-B town-on-a-plane preview
const $ = (s) => document.querySelector(s);
const canvas = $('canvas'), statsEl = $('#stats'), statusEl = $('#status');
const say = (t) => { statusEl.textContent = t; };

const renderer = new T.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance', preserveDrawingBuffer: false });
// The vendored build only has ACES. Khronos PBR Neutral (the P1.4 Blender view transform) is injected per material below (renderer.toneMapping = 0 = none).
const look = { neutral: opt.tone !== 'aces', exp: { value: Number(params.get('exp') || (opt.tone === 'aces' ? 0.7 : 0.75)) }, ao: { value: Number(params.get('ao') ?? 0.8) } };
renderer.toneMapping = look.neutral ? 0 : T.ACESFilmicToneMapping;
renderer.toneMappingExposure = look.exp.value;
renderer.shadowMap.type = T.PCFSoftShadowMap; renderer.shadowMap.enabled = opt.shadows;
renderer.setPixelRatio(Math.min(devicePixelRatio, 1.5));
const scene = new T.Scene();

// ------------------------------------------------------------------------------------------------ light and sky (matches the Blender "afternoon" set-up)
// Image-based ambient light: a small equirect sky gradient. The vendored build has no PMREM helper, but the renderer converts an
// equirect scene.environment itself. Without it every metallic surface (lantern cages, hinges) renders black.
function envTexture() {
  // Same stops as the Blender world ramp of the P1.4 renders (linear colours converted to sRGB): zenith, sky, horizon haze, ground bounce.
  const c = document.createElement('canvas'); c.width = 256; c.height = 128; const g = c.getContext('2d'), grad = g.createLinearGradient(0, 0, 0, 128);
  grad.addColorStop(0, '#5f97dc'); grad.addColorStop(0.3, '#82b0e4'); grad.addColorStop(0.43, '#b4cfeb'); grad.addColorStop(0.49, '#ece4d6'); grad.addColorStop(0.5, '#f1e8d6'); grad.addColorStop(0.53, '#cdd6cd'); grad.addColorStop(1, '#bcc7bc');
  g.fillStyle = grad; g.fillRect(0, 0, 256, 128); const t = new T.CanvasTexture(c); t.colorSpace = T.SRGBColorSpace; t.mapping = 303; return t;     // 303 = EquirectangularReflectionMapping
}
const sky = envTexture(); scene.environment = sky; scene.background = sky; scene.backgroundIntensity = Number(params.get('bg') || 1.0); scene.environmentIntensity = Number(params.get('env') || 2.0);
const hemi = new T.HemisphereLight(0xa9c8ee, 0x8a8a6a, Number(params.get('hemi') || 0)); scene.add(hemi);
const sun = new T.DirectionalLight(0xfff2dc, Number(params.get('sun') || 4.2));
const sunDir = new T.Vector3(0.441, -0.616, -0.653).normalize();      // the Blender sun (rotation 52, 0, -34) in three axes: light travels east, down and north, i.e. it comes from the south-west (P2-A had it mirrored, from the north-east)
sun.position.set(0, 45, -40).addScaledVector(sunDir, -80); sun.target.position.set(0, 0, -45);
sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048); sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.03;
Object.assign(sun.shadow.camera, { left: -60, right: 60, top: 60, bottom: -60, near: 1, far: 260 });   // replaced by fitSunShadow once the world is built
scene.add(sun, sun.target);
const groundMat = new T.MeshStandardMaterial({ color: 0x5f7a45, roughness: 0.95, metalness: 0 });
const ground = new T.Mesh(new T.PlaneGeometry(900, 900), groundMat); ground.rotation.x = -Math.PI / 2; ground.position.y = -0.03; ground.receiveShadow = true; ground.name = 'GROUND'; scene.add(ground);

// ------------------------------------------------------------------------------------------------ data and world
// The game's vendored three build is a curated subset (46 exports): Matrix4 and friends are reached through Object3D.
const M4 = new T.Object3D().matrix.constructor;
const [sceneData, hfMeta, hfBuf] = await Promise.all([
  fetch('data/' + (new URLSearchParams(location.search).get('scenefile') || 'scene.json')).then((r) => r.json()), fetch('data/heightfield.json').then((r) => r.json()), fetch('data/heightfield.bin').then((r) => r.arrayBuffer())]);
const hf = { ...hfMeta, data: new Uint8Array(hfBuf) };
const townHeightAt = (x, z) => { const n = -z, i = Math.floor((x - hf.x0) / hf.cell), j = Math.floor((n - hf.n0) / hf.cell); return i < 0 || j < 0 || i >= hf.nx || j >= hf.nn ? 0 : hf.data[j * hf.nx + i] * 0.01; };
const isl = opt.island ? await loadIsland(T, { townHeightAt, params, scene, say }) : null;     // P3-B: terrain support, collision and island visuals
const heightAt = isl ? isl.heightAt : townHeightAt;
if (isl) ground.visible = false;

say('loading the production kit (GLB)…');
const loader = new T.GLTFLoader();
const t0 = performance.now();
const gltf = await loader.loadAsync(params.get('glb') || 'models/merchant-citadel-p2a-kit.glb');
const loadMs = performance.now() - t0;
const dequant = params.get('dequant') === '1' ? dequantizeKit(T, gltf.scene) : null;        // decode-at-load experiment (P2-B batch 4)
const kit = {}; gltf.scene.children.forEach((c) => { kit[c.name] = c; });
const matStats = opt.matcache ? dedupeMaterials(gltf.scene) : { before: 0, after: 0, saved: 0 };       // material cache: one object per distinct material
const aniso = renderer.capabilities.getMaxAnisotropy();
const materials = new Set(), textures = new Set(), geometries = new Set();
gltf.scene.traverse((o) => {
  if (!o.isMesh) return;
  geometries.add(o.geometry);
  { const g = o.geometry, a = g.attributes._ao || g.attributes._AO; if (a && !g.attributes.aoBaked) g.setAttribute('aoBaked', a); }
  for (const m of [].concat(o.material)) {
    materials.add(m);
    for (const k of ['map', 'normalMap', 'roughnessMap', 'metalnessMap', 'aoMap', 'emissiveMap', 'alphaMap']) if (m[k]) { m[k].anisotropy = Math.min(8, aniso); textures.add(m[k]); }
    if (m.name.startsWith('CUS_cloth') || m.name.includes('cloth')) m.side = T.DoubleSide;     // single-surface custom cloth must show from below
  }
});

// P2-B batch 3: paving/stone grade. ?warm=r,g,b multiplies the colour of the two stone-paving materials (linear), default = no change; tuning aid for the browser-looks-blue finding.
for (const [par, nm] of [['warm', 'MI_UnevenBrick'], ['warmb', 'MI_Brick']]) { const w = (params.get(par) || '').split(',').map(Number); if (w.length === 3 && w.every(Number.isFinite)) for (const m of materials) if (m.name === nm) m.color.setRGB(w[0], w[1], w[2]); }
const world = new T.Group(); world.name = 'WORLD'; scene.add(world);
const placed = [];
for (const inst of sceneData.instances) {
  const src = kit[inst.node]; if (!src) { console.warn('missing node', inst.node); continue; }
  const o = src.clone(true); o.name = inst.id; o.position.set(inst.x, inst.y, inst.z); o.rotation.y = THREE_RAD(inst.ry); o.userData.inst = inst; o.userData.district = inst.district || 'D3';
  world.add(o); placed.push(o);
}
function THREE_RAD(d) { return d * Math.PI / 180; }
// ?town24=1 used to add performance surrogates for unbuilt buildings (batch 3: five, batch 4: two); with B15 and B16 built it adds nothing: existing kit nodes of similar size at their P1.4 sites,
// so the renderer sees a 24-building town. They have no collision and are not final architecture; used only by the merge-strategy measurements (P2-B batch 3).
const SURROGATES = [];                                          // batch 5: all 24 buildings are built; no surrogates remain (?town24=1 is kept as a no-op for old URLs)
if (new URLSearchParams(location.search).get('town24') === '1') for (const [id, node, x, n, ry, dist] of SURROGATES) {
  const src = kit[node]; if (!src) continue; const o = src.clone(true); o.name = id; o.position.set(x, 0, -n); o.rotation.y = THREE_RAD(ry); o.userData.district = dist; o.userData.surrogate = true; world.add(o); placed.push(o);
}
for (const [k, node] of Object.entries(kit)) if (k.startsWith('DRESSING')) { const d = node.clone(true); d.name = k; d.userData.district = k.split('_')[1] || 'D3'; world.add(d); }
const FX = fixFlags(params), fixLog = { flags: FX };                  // P3-B batch 1 targeted corrections (p3b-fixes.js)
if (FX.rail) fixLog.rail_triangles_removed = cutDressing(world, FIX_DATA.rail.cutBox);
if (FX.signs) fixLog.signs_added = addSigns(T, kit, world, placed, FIX_DATA.signs.add);
for (const [key, list] of Object.entries(sceneData.tiles)) {          // paving: one InstancedMesh per tile type
  const src = kit['TILE_' + key]; if (!src) continue; let mesh = src; src.traverse((c) => { if (c.isMesh) mesh = c; });
  const im = new T.InstancedMesh(mesh.geometry, mesh.material, list.length); const m = new M4();
  list.forEach(([x, z, y], i) => { m.makeTranslation(x, y, z); im.setMatrixAt(i, m); });
  im.name = 'PAVING_' + key; im.receiveShadow = true; world.add(im);
}
const standin = null;                                                  // P2-A had a grey stand-in box here; the Exchange Hall is now built from kit modules
world.traverse((o) => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; if (o.isInstancedMesh) o.castShadow = false; } });
const districtOf = (m) => { for (let o = m; o; o = o.parent) if (o.userData && o.userData.district) return o.userData.district; return 'D3'; };
const state = { mergeMode: 'none' };
const mergedSets = {};                                                 // lazily built: 'district' (production), 'scene' (comparison)
function setMerged(mode) {
  mode = mode === true ? 'district' : (mode === false || !mode || mode === '0' ? 'none' : mode);
  for (const m of Object.values(mergedSets)) m.visible = false;
  if (mode !== 'none') {
    if (!mergedSets[mode]) { const t = performance.now(); const cs = /^cell(\d+)$/.exec(mode); mergedSets[mode] = mergeByGroup(T, world, mode === 'scene' ? () => 'ALL' : districtOf, { name: 'MERGED_' + mode, cellSize: cs ? Number(cs[1]) : 0, quantize: new URLSearchParams(location.search).get('qmerge') === '1' }); mergedSets[mode].userData.build_ms = performance.now() - t; scene.add(mergedSets[mode]); }
    mergedSets[mode].visible = true;
  }
  world.visible = mode === 'none'; state.mergeMode = mode;
}
// shadow frustum fitted to the built area (light space), map size from ?smap= (default 2048, see P2-B 05)
sun.shadow.mapSize.set(opt.smap, opt.smap);
const worldBox = new T.Box3().setFromObject(world); const shadowFit = fitSunShadow(T, sun, worldBox);


// ------------------------------------------------------------------------------------------------ look: baked AO (indirect light only) and Khronos Neutral tone mapping
const NEUTRAL_GLSL = `vec3 p2Neutral(vec3 color){ const float startCompression = 0.8 - 0.04; const float desaturation = 0.15;
  float x = min(color.r, min(color.g, color.b)); float offset = x < 0.08 ? x - 6.25 * x * x : 0.04; color -= offset;
  float peak = max(color.r, max(color.g, color.b)); if (peak < startCompression) return color;
  float d = 1.0 - startCompression; float newPeak = 1.0 - d * d / (peak + d - startCompression); color *= newPeak / peak;
  float g = 1.0 - 1.0 / (desaturation * (peak - newPeak) + 1.0); return mix(color, vec3(newPeak), g); }`;
function patchMaterial(m, hasAo) {
  if (m.userData.p2aPatched) return; m.userData.p2aPatched = true;
  const key = 'p2a:' + (hasAo ? 'ao' : 'plain') + (look.neutral ? ':n' : ':a') + (m.userData.extraCompile ? ':x' + m.name + (m.userData.extraCompile.name || '') : '');
  m.onBeforeCompile = (shader) => {
    shader.uniforms.uP2Exp = look.exp; shader.uniforms.uP2Ao = look.ao;
    let vs = shader.vertexShader, fs = shader.fragmentShader;
    if (hasAo) {
      vs = vs.replace('#include <common>', 'attribute float aoBaked;\nvarying float vAoB;\n#include <common>').replace('#include <begin_vertex>', '#include <begin_vertex>\nvAoB = aoBaked;');
      fs = fs.replace('#include <common>', 'varying float vAoB;\nuniform float uP2Ao;\n#include <common>')
        .replace('#include <aomap_fragment>', '#include <aomap_fragment>\n{ float aoB = mix(1.0, vAoB, uP2Ao); reflectedLight.indirectDiffuse *= aoB; reflectedLight.indirectSpecular *= aoB; }');
    }
    if (look.neutral) fs = fs.replace('#include <common>', 'uniform float uP2Exp;\n' + NEUTRAL_GLSL + '\n#include <common>').replace('#include <tonemapping_fragment>', 'gl_FragColor.rgb = p2Neutral(gl_FragColor.rgb * uP2Exp);');
    shader.vertexShader = vs; shader.fragmentShader = fs;
    if (m.userData.extraCompile) m.userData.extraCompile(shader);                // P3-B: island terrain detail / water animation
  };
  m.customProgramCacheKey = () => key; m.needsUpdate = true;
}
function patchScene() {
  // A material can be shared by meshes with and without baked AO (paving tiles use the stone material of the buildings), so every mesh gets an
  // aoBaked attribute (1.0 = unoccluded where nothing was baked) and every standard material gets the same AO-capable program.
  scene.traverse((o) => {
    if (!o.isMesh) return; const g = o.geometry;
    if (!g.attributes.aoBaked) g.setAttribute('aoBaked', new T.Float32BufferAttribute(new Float32Array(g.attributes.position.count).fill(1), 1));
    for (const m of [].concat(o.material)) if (m.isMeshStandardMaterial || m.isMeshPhysicalMaterial) patchMaterial(m, true);
  });
}

// ------------------------------------------------------------------------------------------------ collision proxies (same record format as the first island)
const obstacles = sceneData.collision.map((o) => ({ ...o }));
if (isl) obstacles.push(...isl.obstacles);
if (FX.rail) fixLog.rail_proxies_removed = removeRailProxies(obstacles, FIX_DATA.rail.removeBays);
if (FX.gates) fixLog.gates = openGates(world, obstacles);
if (FX.gap) fixLog.gap_props = addGapProps(T, isl, scene, obstacles);
const camGroups = { cloth: false, sign: false, pennant: false, balcony: true, roof: true, overhang: true, arch: true };   // camera-only groups: true = the camera collides with it
const camOff = new Set(params.get('postsblock') === '1' ? [] : ['post']);   // solid groups the camera ignores: thin posts (0.4-0.5 m) by default (P2-A closeout decision, see 01); ?postsblock=1 restores the P2-A behaviour
const lowPropTop = Number(params.get('lowprops') ?? 1.25);                 // batch 4: floor props whose top is at or below this height (m) are invisible to the camera (solid for the body as always); 0 = off
let walkObs = obstacles, camObs = obstacles;
function refreshObstacles() { walkObs = obstacles; camObs = obstacles.filter((o) => !(o.cameraOnly && o.group in camGroups && !camGroups[o.group]) && !camOff.has(o.group) && !(lowPropTop > 0 && o.group === 'prop' && !o.cameraOnly && o.minY === undefined && o.h <= lowPropTop) && !cameraTransparent(o, FX)); }
refreshObstacles();
const debug = new T.Group(); debug.visible = false; scene.add(debug);
for (const o of obstacles) {
  const y0 = o.minY ?? -0.2, h = o.h - y0; const m = new T.Mesh(new T.BoxGeometry(o.w, Math.max(h, 0.02), o.d), new T.MeshBasicMaterial({ color: o.cameraOnly ? 0xe8a33d : 0x39a0ed, wireframe: true, transparent: true, opacity: 0.8 }));
  m.position.set(o.x, y0 + h / 2, o.z); if (o.oriented) m.rotation.y = o.oriented.rotation, m.scale.set(o.oriented.w / o.w, 1, o.oriented.d / o.d); debug.add(m);
}

// ------------------------------------------------------------------------------------------------ player, input, camera: the game's real modules
const input = createInput(canvas, $('[data-move-host]'), () => {});
const spawn = { x: sceneData.spawn.x, z: sceneData.spawn.z };
say('loading the explorer…');
const character = await createCharacter(scene, {}, spawn, { heightAt, movementOptions: { collision: isl ? isl.collision : { blocked, slide }, bounds: isl ? isl.bounds : 130, minY: -30, maxY: 80, recoveryPoint: spawn, isSafe: isl ? isl.isSafe : () => true } });
character.root.traverse((o) => { if (o.isMesh) { o.castShadow = true; } });
// Character fade (preview-side, the production camera and controller are not touched): when the camera is squeezed close to the player the
// explorer fades toward `min` opacity between `far` and `near` metres, so a back-on-the-lens view of the character never hides the scene.
const fade = { tauOut: 0.06, tauIn: 0.3, on: params.get('fade') !== '0', near: Number(params.get('fnear') || 1.3), far: Number(params.get('ffar') || 3.4), min: 0.14, alpha: 1, mats: [] };
character.root.traverse((o) => { if (o.isMesh) for (const m of [].concat(o.material)) { m.transparent = true; fade.mats.push(m); } });
const follow = createFollowCamera({ clearance: (a, b, list) => clearDistance(a, b, list, 0.28, heightAt), distance: 11.8 });
const camera = follow.camera; camera.far = isl ? 2500 : 600; camera.updateProjectionMatrix();
input.yaw = sceneData.spawn.yaw; input.pitch = 0.19;

function resize() { const w = canvas.clientWidth || innerWidth, h = canvas.clientHeight || innerHeight; if (renderer.userSize) return; renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); }
addEventListener('resize', resize); resize();

const sim = { time: 0, motion: null, frozenCamera: false };
function updateFade(dt = 1 / 60) {
  const p = character.root.position, d = Math.hypot(camera.position.x - p.x, camera.position.y - (p.y + 1.25), camera.position.z - p.z);
  const target = fade.on ? fade.min + (1 - fade.min) * Math.max(0, Math.min(1, (d - fade.near) / (fade.far - fade.near))) : 1;
  // temporal smoothing (P2-B finding: the raw distance mapping jumped by up to 0.75 opacity in one frame when the camera snapped inward): fade out in ~0.06 s, fade back in over ~0.3 s
  const tau = target < fade.alpha ? fade.tauOut : fade.tauIn; fade.alpha += (target - fade.alpha) * (1 - Math.exp(-dt / tau));
  if (!fade.on) fade.alpha = 1; for (const m of fade.mats) m.opacity = fade.alpha;
}
patchScene();
function prewarm() {                                                   // compile every program (main + shadow depth, shadows on and off) before the first visible frame
  const t = performance.now(), culled = [], gl = renderer.getContext(), px = new Uint8Array(4); scene.traverse((o) => { if (o.isMesh && o.frustumCulled) { o.frustumCulled = false; culled.push(o); } });
  const was = renderer.shadowMap.enabled;
  for (const on of [was, !was, was]) { renderer.shadowMap.enabled = on; sun.castShadow = on; scene.traverse((o) => { if (o.material) [].concat(o.material).forEach((m) => { m.needsUpdate = true; }); }); renderer.render(scene, camera); gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px); }
  culled.forEach((o) => { o.frustumCulled = true; }); return performance.now() - t;
}
setMerged(opt.merge);
const prewarmMs = opt.prewarm ? prewarm() : 0;
let wild = null; if (isl && isl.flora && params.get('wild') !== '0') wild = await createWildlife(T, { scene, isl, heightAt, blockedFn: isl.collision.blocked, obstaclesRef: () => walkObs, flora: isl.flora, params, say });
function stepSim(dt, jumpNow = false) {
  input.updateCamera(dt);
  const jump = input.consumeActions().has('jump') || jumpNow;
  sim.motion = character.update(dt, input, walkObs, false, { jump });
  if (!sim.frozenCamera) follow.update(character.root, input, camObs, dt, false);
  if (wild) wild.update(dt, character.root.position, camera.position);                    // P3-B batch 2 wildlife
  updateFade(dt);
  sim.time += dt;
}
function render() { if (isl) isl.tick(sim.time, camera); renderer.render(scene, camera); }

const api = { dequant, get mergeMode() { return state.mergeMode; }, look, fade, patchScene, prewarm, prewarmMs, opt, matStats, shadowFit, worldBox, mergedSets, districtOf, setMerged, T, scene, renderer, camera, follow, character, input, sceneData, hf, heightAt, townHeightAt, isl, FX, fixLog, wild, kit, placed, world, obstacles, standin, ground, sun, hemi, debug, opt, sim, loadMs,
  get walkObs() { return walkObs; }, get camObs() { return camObs; }, camGroups, camOff, refreshObstacles, stepSim, render, resize, materials, textures, geometries, say, blocked: isl ? isl.collision.blocked : blocked, clearDistance,
  teleport(x, z, yaw = 0) { character.root.position.set(x, heightAt(x, z), z); character.movement.settle(); input.yaw = yaw; input.keys.clear(); follow.reset(); stepSim(0.0001); },
  setShadows(on) { renderer.shadowMap.enabled = on; sun.castShadow = on; scene.traverse((o) => { if (o.material) [].concat(o.material).forEach((m) => { m.needsUpdate = true; }); }); } };
window.P2A = api;
installTests(api);
if (isl) installIslandTests(api);
if (wild) installWildTests(api);
if (isl) installB3Tests(api);

// ------------------------------------------------------------------------------------------------ interactive loop and UI
const PRESETS = { spawn: [0, 4, 0], junction: [-1.5, 8, 0], market: [0, 38, 0], steps: [0, 54, 0], inn: [-17.5, 41, 0.35], tea: [24.5, 57.5, -1.57], westhall: [-13, 39.6, 0], easthall: [13, 39.6, 0], shops: [20.6, 44.6, -1.57], potter: [-19.3, 53.6, 1.57] };
document.querySelectorAll('[data-tp]').forEach((b) => b.addEventListener('click', () => { const [x, n, yaw] = PRESETS[b.dataset.tp]; api.teleport(x, -n, yaw); canvas.focus(); }));
const toggle = (id, fn) => { const b = $(id); b.addEventListener('click', () => { const on = b.getAttribute('aria-pressed') !== 'true'; b.setAttribute('aria-pressed', String(on)); fn(on); }); };
toggle('#t-shadows', (on) => api.setShadows(on)); toggle('#t-cloth', (on) => { camGroups.cloth = on; refreshObstacles(); });
toggle('#t-sign', (on) => { camGroups.sign = on; camGroups.pennant = on; refreshObstacles(); }); toggle('#t-debug', (on) => { debug.visible = on; });
$('#t-shadows').setAttribute('aria-pressed', String(opt.shadows));
let last = performance.now(), acc = 0, frames = 0, shown = 0;
function frame(now) {
  const dt = Math.min(0.05, (now - last) / 1000); last = now;
  if (!api.paused) { stepSim(dt); render(); }
  frames++; acc += dt;
  if (acc >= 0.5) {
    const i = renderer.info, m = sim.motion;
    statsEl.textContent = `${Math.round(frames / acc)} fps   calls ${i.render.calls}   tris ${i.render.triangles.toLocaleString()}\ntextures ${i.memory.textures}   geometries ${i.memory.geometries}\n` +
      `x ${character.root.position.x.toFixed(1)}  n ${(-character.root.position.z).toFixed(1)}  y ${character.root.position.y.toFixed(2)}  ${m ? m.phase : ''}\ncamera ${camera.position.distanceTo(new T.Vector3(character.root.position.x, character.root.position.y + 1.25, character.root.position.z)).toFixed(1)} m`;
    frames = 0; acc = 0;
  }
  requestAnimationFrame(frame);
}
say('ready'); document.body.dataset.ready = '1';
if (!opt.autotest) requestAnimationFrame(frame); else { api.paused = true; say('autotest: ' + opt.autotest); api.autotest(opt.autotest); }
