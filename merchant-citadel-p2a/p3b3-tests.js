// Merchant Citadel P3-B batch 3: capture and measurement helpers for the polish packages (real browser, scripted).
export function installB3Tests(P) {
  const { camera, character } = P; const I = P.island; const DT = 1 / 60;
  const mc = new MessageChannel(); const sleep = () => new Promise((r) => { mc.port1.onmessage = () => r(); mc.port2.postMessage(0); });
  const save = async (name, data) => { await fetch('/__save?name=' + encodeURIComponent(name), { method: 'POST', body: data instanceof Blob ? data : JSON.stringify(data, null, 1) }); };
  // list entries: { name, game: [x, n, yawDeg] } (follow camera standing there, plan frame) or { name, free: [[x, n, up], [lx, ln, lup], fov] }; eye: true hides the character
  async function shots(tag, list, { w = 1280, h = 720, wait = 60 } = {}) {
    const done = [];
    for (const e of list) {
      const was = character.root.visible;
      if (e.game) { P.sim.frozenCamera = false; character.root.visible = true; P.teleport(e.game[0], -e.game[1], (e.game[2] || 0) * Math.PI / 180); for (let i = 0; i < wait; i++) P.stepSim(DT); }
      else { character.root.visible = false; let fr = e.free; if (e.view) { const vv = await (await fetch('data/p3b-views.json')).json(); fr = vv[e.view]; } const [p, look, fov] = fr; I.setCam(p, look, fov); }
      if (e.prep) e.prep();
      await sleep(); await sleep(); await save(`p3b3-${tag}-${e.name}.jpg`, await I.blob(w, h, 0.9)); character.root.visible = was; P.sim.frozenCamera = false; done.push(e.name);
    }
    return done;
  }
  const H = (x, n) => P.heightAt(x, -n), eye = (x, n) => H(x, n) + 1.65;
  const lists = {
    wp1: () => [{ name: 'tea-promenade-game', game: [60, 55.5, -90] }, { name: 'tea-promenade-eye', free: [[44, 57.2, eye(44, 57.2)], [62, 55.3, eye(44, 57.2) - 0.5], 62] }, { name: 'terraces-aerial', free: [[72, 8, 26], [72, 52, -2], 52] },
      { name: 'terraces-rows-eye', free: [[56, 40, H(56, 40) + 1.65], [76, 40, H(76, 40) + 0.2], 62] }, { name: 'green-road-game', game: [-30, 9, 110] }, { name: 'crag-ascent-game', game: [24, 94, 0] },
      { name: 'porters-loop-eye', free: [[34, 21, eye(34, 21)], [48, 20, eye(34, 21) - 0.7], 62] }, { name: 'path-edge-closeup', free: [[58, 50.5, H(58, 52.4) + 1.1], [58, 54.2, H(58, 54.2)], 45] }],
  };
  lists.wp3 = () => [{ name: 'side-east', view: 'v2-side-east' }, { name: 'side-south', view: 'v2b-side-south' }, { name: 'approach-sw', view: 'v6-dragon-approach' }, { name: 'approach-east', view: 'v6b-dragon-approach-east' }, { name: 'crag', view: 'b2-crag' }, { name: 'crag-to-town', view: 'v8-crag-to-town' },
    { name: 'underside-south', free: [[10, -70, -50], [10, 10, -12], 64] }, { name: 'underside-north', free: [[60, 175, -42], [46, 100, -12], 64] }, { name: 'crag-game', game: [30, 100, 0] }, { name: 'cliff-top-game', game: [88, 40, 90] }];
  lists.wp4 = () => [{ name: 'cloudfall-overlook', view: 'b2-cloudfall' }, { name: 'fall-east-approach', free: [[150, 70, -6], [92, 64, -18], 50] }, { name: 'fall-below', free: [[120, 60, -40], [92, 64, -16], 55] }, { name: 'fall-game', game: [80, 60, 90] }, { name: 'fall-lip-eye', free: [[84, 64, H(84, 64) + 1.65], [92, 64, -10], 62] }, { name: 'stream-bank-eye', free: [[66, 74, H(66, 74) + 1.65], [74, 68, H(74, 68)], 60] }];
  lists.wp2 = () => [{ name: 'green-game', game: [-44, 16, 90] }, { name: 'town-vegetation', view: 'b2-town-vegetation' }, { name: 'crag-game', game: [30, 100, 0] }, { name: 'caravan-wide', view: 'b2-caravan-green-wide' }, { name: 'grove-eye', free: [[-62, 30, H(-62, 30) + 1.65], [-52, 22, H(-52, 22) + 2.5], 66] }, { name: 'tea-game', game: [60, 55.5, -90] }];
  P.b3 = { shots, save, sleep, lists };
}
