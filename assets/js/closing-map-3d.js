/* Original, schematic city maquette. No geographic or analytical data implied.
 * Shared GSAP ticker only; the page's motion lifecycle owns visibility/pause. */
(() => {
  'use strict';

  window.createClosingMap3D = (host, { gsap } = {}) => {
    if (!host) return null;
    const T = window.Hero3DPrimitives;
    const poster = host.querySelector('.closing-map__poster');
    // Creation itself is visibility-gated. Fetch the fallback now, before
    // hiding it, so an unexpected context loss can reveal it immediately.
    if (poster) poster.loading = 'eager';
    const fallback = () => {
      host.dataset.renderer = 'fallback';
      host.dataset.playing = 'false';
      if (poster) poster.hidden = false;
    };
    const noop = { play() {}, pause() {}, resize() {}, static() {}, snapshot() { return null; }, destroy() {} };
    fallback();
    if (!T || !gsap || navigator.connection?.saveData) return noop;

    let renderer;
    try {
      const canvas = document.createElement('canvas');
      const context = canvas.getContext('webgl2', { alpha: true, antialias: true, powerPreference: 'low-power' });
      if (!context) return noop;
      renderer = new T.WebGLRenderer({ canvas, context, alpha: true, antialias: true, powerPreference: 'low-power' });
    } catch (_) { return noop; }
    const canvas = renderer.domElement;
    canvas.className = 'closing-map__canvas';
    canvas.setAttribute('aria-hidden', 'true');
    canvas.style.visibility = 'hidden';
    host.appendChild(canvas);
    renderer.setClearColor(0, 0);
    renderer.outputColorSpace = T.SRGBColorSpace;
    renderer.toneMapping = T.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.12;

    const scene = new T.Scene();
    const camera = new T.OrthographicCamera(-7, 7, 4, -4, 0.1, 80);
    camera.position.set(10, 12.5, 15);
    camera.lookAt(0, 0.2, 0);
    scene.add(new T.HemisphereLight(0xfffaf0, 0x697674, 2.4));
    const key = new T.DirectionalLight(0xffead1, 3.1);
    key.position.set(-7, 10, 4);
    scene.add(key);
    const rim = new T.DirectionalLight(0xc9e3e3, 1.4);
    rim.position.set(5, 6, -8);
    scene.add(rim);

    const geometries = [];
    const materials = [];
    const geometry = (g) => { geometries.push(g); return g; };
    const material = (color, options = {}) => {
      const mat = new T.MeshStandardMaterial({ color, roughness: 0.88, metalness: 0, ...options });
      materials.push(mat);
      return mat;
    };
    const mat = {
      base: material(0xb8baa8), land: material(0xd7d9be), edge: material(0x859189),
      paper: material(0xf5eddc), stone: material(0xd5caba), roof: material(0xaeb5a7),
      roofDark: material(0x8eaaa4), glass: material(0x69958e), clay: material(0xbd8771),
      road: material(0xf6edda), sidewalk: material(0xd0cbb8), park: material(0x8fa984),
      lawn: material(0xa5b895), tree: material(0x608975), treeLight: material(0x7d9c7d),
      trunk: material(0x8c8067), water: material(0x669e99, { roughness: 0.48 }),
      bank: material(0xbbc7a3), route: material(0xe4578b, { emissive: 0x5d132b, emissiveIntensity: 0.2 }),
      signal: material(0xffb8cf, { emissive: 0xce477a, emissiveIntensity: 0.7 })
    };
    const unitBox = geometry(new T.BoxGeometry(1, 1, 1));
    const unitCylinder = geometry(new T.CylinderGeometry(1, 1, 1, 12));
    const crown = geometry(new T.SphereGeometry(1, 9, 6));
    const disc = geometry(new T.CircleGeometry(1, 48));
    const ring = geometry(new T.RingGeometry(0.72, 1, 40));
    const map = new T.Group();
    scene.add(map);
    const mesh = (g, m, position, scale, parent = map) => {
      const object = new T.Mesh(g, m);
      if (position) object.position.set(...position);
      if (scale) object.scale.set(...scale);
      parent.add(object);
      return object;
    };
    const box = (m, x, y, z, w, h, d) => mesh(unitBox, m, [x, y, z], [w, h, d]);
    const solid = (points, depth, m, y, bevel = 0) => {
      const shape = new T.Shape();
      points.forEach(([x, z], i) => i ? shape.lineTo(x, -z) : shape.moveTo(x, -z));
      shape.closePath();
      const g = geometry(new T.ExtrudeGeometry(shape, {
        depth, steps: 1, bevelEnabled: bevel > 0, bevelSegments: 2,
        bevelThickness: bevel, bevelSize: bevel, curveSegments: 12
      }));
      const object = mesh(g, m, [0, y, 0]);
      object.rotation.x = -Math.PI / 2;
      return object;
    };
    const outline = [[-4.9,-2.85],[-4.7,-3.05],[4.7,-3.05],[4.9,-2.85],[4.9,2.85],[4.7,3.05],[-4.7,3.05],[-4.9,2.85]];
    // Thin stacked cartographic layers give the map a tangible cut edge.
    solid(outline, 0.085, mat.edge, -0.42, 0.035);
    solid(outline.map(([x,z]) => [x * 0.987, z * 0.985]), 0.30, mat.base, -0.27, 0.025);
    solid(outline, 0.09, mat.land, 0.07, 0.035);

    // A meandering water corridor creates one compositional diagonal. Banks
    // are one continuous polygon, not disconnected decorative fragments.
    const river = new T.CatmullRomCurve3([
      new T.Vector3(-4.90,0,-0.08), new T.Vector3(-3.1,0,-0.01),
      new T.Vector3(-1.0,0,-0.82), new T.Vector3(1.0,0,-0.40),
      new T.Vector3(2.8,0,0.23), new T.Vector3(4.90,0,0.70)
    ]);
    const ribbon = (curve, width) => {
      const a = [], b = [];
      for (let i = 0; i <= 64; i += 1) {
        const p = curve.getPoint(i / 64), t = curve.getTangent(i / 64);
        a.push([p.x - t.z * width, p.z + t.x * width]);
        b.push([p.x + t.z * width, p.z - t.x * width]);
      }
      // Keep every point within the slab at the two river mouths.
      return a.concat(b.reverse()).map(([x,z]) => [Math.max(-4.9, Math.min(4.9, x)), z]);
    };
    solid(ribbon(river, 0.43), 0.016, mat.bank, 0.17);
    solid(ribbon(river, 0.29), 0.018, mat.water, 0.19);

    // Streets stay quiet and pale. Three crossings bind the two riverbanks.
    [-1.6, 1.52].forEach((z) => box(mat.road, 0, 0.195, z, 9.5, 0.028, 0.23));
    [-2.25, 1.65, 3.8].forEach((x) => {
      box(mat.sidewalk, x, 0.215, 0.05, 0.34, 0.06, 5.66);
      box(mat.road, x, 0.25, 0.05, 0.22, 0.028, 5.66);
    });
    // Riverside park: an irregular precinct with a small paved courtyard.
    solid([[-1.94,0.23],[-1.25,-0.15],[0.25,0.14],[1.40,0.60],[1.40,1.34],[-1.94,1.34]], 0.045, mat.park, 0.17, 0.025);
    solid([[2.05,-2.86],[3.58,-2.86],[3.58,-1.85],[2.3,-1.85]], 0.028, mat.lawn, 0.17, 0.035);
    box(mat.road, -0.38, 0.235, 0.72, 1.06, 0.035, 0.38);

    // Authored precincts: a low-rise waterfront, a taller civic ensemble,
    // and a terraced residential quarter. No random heights or fake metrics.
    const buildings = [
      [-4.08,-2.33,0.72,0.74,0.68,'paper'],[-3.13,-2.35,0.62,0.52,0.65,'stone'],
      [-4.12,-0.90,0.77,0.40,0.60,'clay'],[-3.15,-0.85,0.55,0.63,0.54,'paper'],
      [-1.48,-2.35,0.76,0.38,0.65,'stone'],[-0.46,-2.33,0.70,1.40,0.66,'paper'],
      [0.48,-2.35,0.59,1.02,0.59,'paper'],[1.13,-2.28,0.31,0.56,0.48,'stone'],
      [4.32,-2.36,0.55,0.47,0.65,'paper'],[4.29,-1.11,0.56,0.67,0.71,'stone'],
      [-4.06,0.94,0.67,0.32,0.49,'stone'],[-3.08,0.95,0.60,0.48,0.53,'paper'],
      [-4.07,2.31,0.75,0.58,0.73,'paper'],[-3.09,2.32,0.56,0.77,0.67,'paper'],
      [-1.43,2.33,0.67,0.42,0.66,'clay'],[-0.53,2.29,0.65,0.60,0.74,'paper'],
      [0.55,2.28,0.86,0.35,0.73,'stone'],[2.64,2.32,1.04,0.46,0.70,'paper'],
      [4.33,2.34,0.54,0.81,0.60,'paper'],[2.75,-1.14,0.95,0.29,0.48,'stone']
    ];
    buildings.forEach(([x,z,w,h,d,color], index) => {
      const ground = 0.22;
      box(mat.sidewalk, x, 0.193, z, w + 0.15, 0.028, d + 0.15);
      box(mat[color], x, ground + h / 2, z, w, h, d);
      // Recessed roof with a thin parapet; a few terrace setbacks, not
      // window noise on every surface. Details still read on small screens.
      box(index % 3 === 0 ? mat.roofDark : mat.roof, x, ground + h + 0.013, z, w - 0.07, 0.025, d - 0.07);
      if (h > 0.9) {
        box(mat.paper, x - w * 0.10, ground + h + 0.14, z, w * 0.62, 0.24, d * 0.64);
        box(mat.roofDark, x - w * 0.10, ground + h + 0.266, z, w * 0.53, 0.013, d * 0.54);
      }
      if (index % 3 !== 1) {
        const floors = Math.max(1, Math.floor(h / 0.24));
        for (let floor = 0; floor < floors; floor += 1) {
          box(mat.glass, x, ground + 0.11 + floor * 0.235, z + d / 2 + 0.004, w * 0.73, 0.048, 0.008);
        }
      }
      // A translucent, single-pass contact patch grounds each building.
      const shadowMat = new T.MeshBasicMaterial({ color: 0x495c54, transparent: true, opacity: 0.13, depthWrite: false });
      materials.push(shadowMat);
      box(shadowMat, x + 0.09, 0.211, z - 0.08, w + h * 0.24, 0.004, d + h * 0.16);
    });

    const trees = [[-1.62,0.55],[-1.29,0.83],[-1.60,1.06],[0.43,0.66],[0.80,0.93],[1.10,1.12],
      [2.43,-2.48],[2.80,-2.53],[3.22,-2.46],[2.55,-2.04],[3.15,-2.02],
      [-4.47,1.91],[-2.68,2.71],[1.14,2.72],[2.07,2.74],[3.23,1.99],[4.61,-0.44]];
    trees.forEach(([x,z], i) => {
      const h = 0.24 + (i % 3) * 0.035;
      mesh(unitCylinder, mat.trunk, [x, 0.28, z], [0.026, 0.16, 0.026]);
      mesh(crown, i % 3 ? mat.tree : mat.treeLight, [x, 0.35 + h * 0.5, z], [0.15, h, 0.15]);
    });

    // The narrow pink itinerary is spatially tied to streets and a bridge.
    // Spline corners are deliberately softened rather than dashboard-like.
    const route = new T.CatmullRomCurve3([
      new T.Vector3(-4.38,0.29,1.52), new T.Vector3(-2.58,0.29,1.52),
      new T.Vector3(-2.25,0.29,1.23), new T.Vector3(-2.25,0.29,-1.27),
      new T.Vector3(-1.92,0.29,-1.60), new T.Vector3(1.34,0.29,-1.60),
      new T.Vector3(1.65,0.29,-1.26), new T.Vector3(1.65,0.29,1.20),
      new T.Vector3(1.96,0.29,1.52), new T.Vector3(3.45,0.29,1.52)
    ], false, 'centripetal', 0.1);
    mesh(geometry(new T.TubeGeometry(route, 160, 0.025, 6, false)), mat.route);
    const runner = mesh(crown, mat.signal, null, [0.065,0.065,0.065]);
    const stops = [0.035, 0.33, 0.60, 0.965].map((u) => {
      const point = route.getPointAt(u);
      mesh(unitCylinder, mat.paper, [point.x,0.28,point.z], [0.104,0.026,0.104]);
      mesh(unitCylinder, mat.route, [point.x,0.303,point.z], [0.064,0.032,0.064]);
      const pulseMat = new T.MeshBasicMaterial({ color: 0xef739e, transparent: true, opacity: 0.38, side: T.DoubleSide, depthWrite: false });
      materials.push(pulseMat);
      const pulse = mesh(ring, pulseMat, [point.x,0.29,point.z], [0.16,0.16,0.16]);
      pulse.rotation.x = -Math.PI / 2;
      return { u, pulse, pulseMat };
    });
    // One fine map pin is the final punctuation mark, not another label.
    const destination = route.getPointAt(0.965);
    mesh(unitCylinder, mat.route, [destination.x,0.60,destination.z], [0.023,0.56,0.023]);
    mesh(crown, mat.route, [destination.x,0.92,destination.z], [0.14,0.17,0.14]);
    mesh(crown, mat.paper, [destination.x+0.073,0.95,destination.z+0.101], [0.045,0.049,0.034]);

    // Layered transparent discs approximate soft studio contact shadow without
    // shadow maps, texture downloads, post-processing, or an extra render pass.
    [0.07,0.045,0.025].forEach((opacity, i) => {
      const shadowMat = new T.MeshBasicMaterial({ color: 0x141f1e, transparent: true, opacity, depthWrite: false, side: T.DoubleSide });
      materials.push(shadowMat);
      const shadow = mesh(disc, shadowMat, [0,-0.71-i*0.003,0], [5.5+i*0.15,3.5+i*0.12,1], scene);
      shadow.rotation.x = -Math.PI / 2;
    });

    let playing = false, destroyed = false, contextLost = false, resumeOnRestore = false;
    let seconds = 0, accumulated = 0, lastWidth = 0, lastHeight = 0;
    const state = (time, moving = true) => {
      map.rotation.y = moving ? Math.sin(time * 0.18) * 0.026 : 0;
      // Start at the poster's marker position, so enabling motion does not
      // teleport the signal from a static/reduced-motion frame.
      const progress = moving ? (0.6 + time / 14) % 1 : 0.6;
      runner.position.copy(route.getPointAt(progress));
      stops.forEach(({ u, pulse, pulseMat }) => {
        const distance = Math.min(Math.abs(progress-u), 1-Math.abs(progress-u));
        const activity = moving ? Math.max(0, 1 - distance / 0.07) : 0;
        pulse.scale.setScalar(0.14 + activity * 0.15);
        pulseMat.opacity = 0.16 + activity * 0.4;
      });
    };
    const render = () => {
      if (destroyed || contextLost) return;
      renderer.render(scene, camera);
    };
    const resize = () => {
      if (destroyed || contextLost) return;
      const { width, height } = host.getBoundingClientRect();
      if (!width || !height) return;
      const ratio = width / height;
      // Width-fit on portrait screens and height-fit on the wider desktop
      // canvas. Both keep the complete slab + pin inside the camera frustum.
      const halfHeight = Math.max(4.08, 6.22 / ratio);
      camera.left = -halfHeight * ratio; camera.right = halfHeight * ratio;
      camera.top = halfHeight; camera.bottom = -halfHeight;
      camera.updateProjectionMatrix();
      if (width !== lastWidth || height !== lastHeight) {
        renderer.setPixelRatio(Math.min(devicePixelRatio || 1, innerWidth < 700 ? 1.25 : 1.5));
        renderer.setSize(width, height, false);
        lastWidth = width; lastHeight = height;
      }
      render();
    };
    const tick = (_time, delta) => {
      if (!playing || contextLost) return;
      accumulated += Math.min(delta, 80);
      const frameInterval = innerWidth < 700 ? 1000 / 24 : 1000 / 30;
      if (accumulated < frameInterval) return;
      seconds += accumulated / 1000; accumulated = 0;
      state(seconds); render();
    };
    const pause = () => {
      playing = false; resumeOnRestore = false; accumulated = 0;
      gsap.ticker.remove(tick); host.dataset.playing = 'false';
    };
    const play = () => {
      if (destroyed) return;
      if (contextLost) { resumeOnRestore = true; return; }
      if (playing) return;
      playing = true; host.dataset.playing = 'true'; gsap.ticker.add(tick);
    };
    const staticScene = () => { pause(); seconds = 0; state(0, false); resize(); render(); };
    const lost = (event) => {
      event.preventDefault();
      const resume = playing;
      pause(); contextLost = true; resumeOnRestore = resume;
      canvas.style.visibility = 'hidden'; fallback();
    };
    const restored = () => {
      contextLost = false; resize();
      canvas.style.visibility = 'visible'; host.dataset.renderer = 'webgl';
      if (poster) poster.hidden = true;
      if (resumeOnRestore && !document.hidden && !matchMedia('(prefers-reduced-motion: reduce)').matches) play();
    };
    canvas.addEventListener('webglcontextlost', lost);
    canvas.addEventListener('webglcontextrestored', restored);
    state(0, false); resize();
    host.dataset.renderer = 'webgl'; canvas.style.visibility = 'visible';
    if (poster) poster.hidden = true;
    return {
      play, pause, resize, static: staticScene,
      snapshot() { render(); return contextLost ? null : canvas.toDataURL('image/webp', 0.92); },
      destroy() {
        pause(); destroyed = true;
        canvas.removeEventListener('webglcontextlost', lost);
        canvas.removeEventListener('webglcontextrestored', restored);
        geometries.forEach((g) => g.dispose()); materials.forEach((m) => m.dispose());
        renderer.dispose(); canvas.remove(); fallback();
      }
    };
  };
})();
