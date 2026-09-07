/* Original articulated field analyst. GSAP provides the only animation clock. */
(() => {
  'use strict';

  window.createAnalyst3D = (host, { gsap } = {}) => {
    if (!host) return null;
    const T = window.Hero3DPrimitives;
    const fallback = host.querySelector('.analyst-fallback');
    const showFallback = () => {
      host.dataset.renderer = 'fallback';
      host.dataset.playing = 'false';
      if (fallback) {
        fallback.hidden = false;
        fallback.removeAttribute('hidden');
      }
    };
    showFallback();
    if (!T || !gsap || navigator.connection?.saveData) {
      return { play() {}, pause() {}, resize() {}, static() {}, snapshot() { return null; }, destroy() {} };
    }

    let renderer;
    try {
      const surface = document.createElement('canvas');
      const context = surface.getContext('webgl2', { alpha: true, antialias: true, powerPreference: 'low-power' });
      if (!context) return { play() {}, pause() {}, resize() {}, static() {}, snapshot() { return null; }, destroy() {} };
      renderer = new T.WebGLRenderer({ canvas: surface, context, alpha: true, antialias: true, powerPreference: 'low-power' });
    } catch (_) {
      return { play() {}, pause() {}, resize() {}, static() {}, snapshot() { return null; }, destroy() {} };
    }
    const canvas = renderer.domElement;
    canvas.className = 'analyst-canvas';
    canvas.setAttribute('aria-hidden', 'true');
    canvas.style.visibility = 'hidden';
    host.appendChild(canvas);
    renderer.setClearColor(0x000000, 0);
    renderer.outputColorSpace = T.SRGBColorSpace;
    renderer.toneMapping = T.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.2;

    const scene = new T.Scene();
    const camera = new T.OrthographicCamera(-1, 1, 1.21, -1.18, 0.1, 30);
    camera.position.set(4.1, 2.65, 8.5);
    camera.lookAt(0.035, 1.105, 0);
    scene.add(new T.HemisphereLight(0xfff7e8, 0x66625d, 2.5));
    const key = new T.DirectionalLight(0xfff2db, 3.2);
    key.position.set(4, 7, 6);
    scene.add(key);
    const rim = new T.DirectionalLight(0xc4dddc, 1.1);
    rim.position.set(-4, 3, -3);
    scene.add(rim);

    const materials = [];
    const geometries = [];
    const material = (color, extras = {}) => {
      const mat = new T.MeshStandardMaterial({ color, roughness: 0.85, metalness: 0, ...extras });
      materials.push(mat);
      return mat;
    };
    const skin = material(0xb67b56);
    const skinLight = material(0xc88d63);
    const hair = material(0x292722);
    const jacket = material(0xc49945);
    const jacketShade = material(0x9d762e);
    const lining = material(0xe7d8b3);
    const trousers = material(0x474f50);
    const trousersShade = material(0x394343);
    const bag = material(0x3e7771);
    const bagShade = material(0x285b59);
    const shoe = material(0xe3d8bc);
    const sole = material(0xb8ae94);
    const tabletShell = material(0x3d4945);
    const mapPaper = material(0xe9e2c8);
    const sphereGeometry = new T.SphereGeometry(1, 16, 12);
    const cylinderGeometry = new T.CylinderGeometry(1, 1, 1, 12, 1);
    const capsuleGeometry = new T.CapsuleGeometry(1, 1, 4, 12);
    const boxGeometry = new T.BoxGeometry(1, 1, 1);
    geometries.push(sphereGeometry, cylinderGeometry, capsuleGeometry, boxGeometry);
    const yAxis = new T.Vector3(0, 1, 0);
    const tempDirection = new T.Vector3();

    const mesh = (geometry, mat, parent, position, scale) => {
      const object = new T.Mesh(geometry, mat);
      if (position) object.position.set(...position);
      if (scale) object.scale.set(...scale);
      parent.add(object);
      return object;
    };
    const ellipsoid = (mat, parent, position, scale) => mesh(sphereGeometry, mat, parent, position, scale);
    const box = (mat, parent, position, scale) => mesh(boxGeometry, mat, parent, position, scale);
    const cylinder = (mat, parent, radius) => {
      const object = mesh(cylinderGeometry, mat, parent);
      object.userData.radius = radius;
      return object;
    };
    const connect = (object, from, to, radius = object.userData.radius) => {
      tempDirection.subVectors(to, from);
      const length = tempDirection.length();
      object.position.copy(from).addScaledVector(tempDirection, 0.5);
      object.quaternion.setFromUnitVectors(yAxis, tempDirection.normalize());
      object.scale.set(radius, length, radius);
    };
    const detailLine = (parent, mat, from, to, radius) => {
      const line = cylinder(mat, parent, radius);
      connect(line, new T.Vector3(...from), new T.Vector3(...to));
      return line;
    };

    // The silhouette is authored in world coordinates, facing +X. Its
    // shaded volumes and real joint rotations remain coherent at any size.
    const figure = new T.Group();
    scene.add(figure);
    const torso = new T.Group();
    figure.add(torso);
    mesh(capsuleGeometry, jacket, torso, [0.015, 1.365, 0], [0.225, 0.227, 0.226]);
    ellipsoid(jacketShade, torso, [0.003, 1.092, 0], [0.218, 0.085, 0.22]);
    ellipsoid(trousersShade, torso, [-0.025, 1.03, 0], [0.19, 0.12, 0.198]);
    // Open collar, front placket, and two small pockets read as fieldwear.
    ellipsoid(lining, torso, [0.168, 1.568, 0], [0.075, 0.17, 0.14]);
    detailLine(torso, jacketShade, [0.238, 1.50, 0.012], [0.232, 1.15, 0.012], 0.013);
    ellipsoid(jacketShade, torso, [0.205, 1.291, 0.126], [0.041, 0.082, 0.068]);
    ellipsoid(jacketShade, torso, [0.205, 1.291, -0.126], [0.041, 0.082, 0.068]);
    ellipsoid(skin, torso, [0.031, 1.744, 0], [0.09, 0.13, 0.09]);

    const head = new T.Group();
    head.position.set(0.028, 1.969, 0);
    torso.add(head);
    ellipsoid(skinLight, head, [0, 0, 0], [0.21, 0.247, 0.207]);
    ellipsoid(skin, head, [0.12, -0.109, 0], [0.107, 0.12, 0.163]);
    ellipsoid(skinLight, head, [0.211, 0.005, 0], [0.057, 0.049, 0.056]);
    ellipsoid(hair, head, [-0.031, 0.139, -0.004], [0.209, 0.158, 0.216]);
    ellipsoid(hair, head, [-0.13, 0.032, 0], [0.103, 0.17, 0.202]);
    ellipsoid(hair, head, [0.11, 0.194, 0.03], [0.118, 0.085, 0.165]);
    [-1, 1].forEach((side) => {
      ellipsoid(skin, head, [-0.025, -0.013, side * 0.20], [0.048, 0.066, 0.027]);
      ellipsoid(hair, head, [0.183, 0.055, side * 0.109], [0.009, 0.015, 0.014]);
      detailLine(head, hair, [0.175, 0.095, side * 0.085], [0.165, 0.103, side * 0.145], 0.008);
    });

    // A compact survey pack sits behind the torso; straps wrap around its
    // shoulders. All details are original solids, with no downloaded model.
    ellipsoid(bagShade, torso, [-0.219, 1.395, 0], [0.143, 0.285, 0.229]);
    ellipsoid(bag, torso, [-0.294, 1.40, 0], [0.117, 0.242, 0.22]);
    ellipsoid(bagShade, torso, [-0.365, 1.318, 0.015], [0.046, 0.126, 0.151]);
    [-1, 1].forEach((side) => {
      detailLine(torso, bagShade, [-0.12, 1.654, side * 0.177], [0.153, 1.615, side * 0.181], 0.029);
      detailLine(torso, bagShade, [0.153, 1.615, side * 0.181], [0.19, 1.259, side * 0.177], 0.026);
    });

    const legs = [-1, 1].map((side) => {
      const group = new T.Group();
      figure.add(group);
      const upper = cylinder(trousers, group, 0.095);
      const lower = cylinder(trousers, group, 0.076);
      const knee = ellipsoid(trousers, group, null, [0.082, 0.086, 0.081]);
      const hip = ellipsoid(trousers, group, null, [0.098, 0.104, 0.099]);
      const cuff = ellipsoid(trousersShade, group, null, [0.077, 0.049, 0.079]);
      const foot = new T.Group();
      group.add(foot);
      ellipsoid(sole, foot, [0.063, 0.027, 0], [0.168, 0.027, 0.088]);
      ellipsoid(shoe, foot, [0.075, 0.078, 0], [0.158, 0.063, 0.084]);
      ellipsoid(shoe, foot, [-0.024, 0.105, 0], [0.071, 0.063, 0.078]);
      detailLine(foot, sole, [0.042, 0.133, -0.049], [0.052, 0.133, 0.049], 0.007);
      return { side, upper, lower, knee, hip, cuff, foot, h: new T.Vector3(), k: new T.Vector3(), a: new T.Vector3() };
    });

    const arms = [-1, 1].map((side) => {
      const group = new T.Group();
      figure.add(group);
      const upper = cylinder(jacket, group, 0.078);
      const lower = cylinder(jacket, group, 0.062);
      const shoulder = ellipsoid(jacket, group, null, [0.089, 0.102, 0.091]);
      const elbow = ellipsoid(jacket, group, null, [0.069, 0.073, 0.069]);
      const hand = ellipsoid(skinLight, group, null, [0.066, 0.08, 0.057]);
      const carry = new T.Group();
      group.add(carry);
      if (side === 1) {
        box(tabletShell, carry, [0.025, -0.04, 0.044], [0.166, 0.226, 0.035]);
        box(mapPaper, carry, [0.025, -0.04, 0.064], [0.142, 0.196, 0.009]);
        detailLine(carry, bag, [-0.025, 0.026, 0.071], [0.047, -0.016, 0.071], 0.007);
        detailLine(carry, bag, [0.047, -0.016, 0.071], [0.014, -0.082, 0.071], 0.007);
        detailLine(carry, jacketShade, [-0.021, -0.08, 0.071], [0.072, -0.063, 0.071], 0.004);
        ellipsoid(jacketShade, carry, [0.047, -0.016, 0.076], [0.012, 0.012, 0.005]);
      }
      return { side, upper, lower, shoulder, elbow, hand, carry, s: new T.Vector3(), e: new T.Vector3(), w: new T.Vector3() };
    });

    // Soft contact shadows are transparent flattened discs. No shadow
    // maps, post-processing passes, textures, or GPU-heavy effects.
    const shadowGeometry = new T.CircleGeometry(1, 32);
    geometries.push(shadowGeometry);
    [0.14, 0.075, 0.035].forEach((opacity, index) => {
      const mat = new T.MeshBasicMaterial({ color: 0x302c23, transparent: true, opacity, depthWrite: false, side: T.DoubleSide });
      materials.push(mat);
      const shadow = mesh(shadowGeometry, mat, scene, [0.02, 0.004 + index * 0.0002, 0], [0.30 + index * 0.055, 0.18 + index * 0.035, 1]);
      shadow.rotation.x = -Math.PI / 2;
    });

    let destroyed = false;
    let playing = false;
    let contextLost = false;
    let resumeOnRestore = false;
    let elapsed = 0;
    let accumulated = 0;
    let lastWidth = 0;
    let lastHeight = 0;
    // The stance foot moves backward at the same approximate screen speed
    // as the existing street: 56 / 48 / 40 SVG units per second. The mobile
    // figure is proportionally larger, so its unhurried gait takes longer.
    const cycleForViewport = () => innerWidth < 700 ? 1.30 : (innerWidth < 1100 ? 0.97
      : (matchMedia('(hover: hover) and (pointer: fine)').matches ? 0.83 : 1.16));
    let cycleDuration = cycleForViewport();
    const tau = Math.PI * 2;
    const smoothstep = (value) => value * value * (3 - 2 * value);

    const pose = (seconds) => {
      const cycle = (seconds / cycleDuration) % 1;
      const bob = 0.012 * Math.sin(cycle * tau * 2);
      const sway = 0.012 * Math.sin(cycle * tau);
      torso.position.set(0, bob, sway);
      torso.rotation.x = 0.018 * Math.sin(cycle * tau);
      head.rotation.y = 0.025 * Math.sin(cycle * tau);
      legs.forEach((leg, index) => {
        const u = (cycle + index * 0.5) % 1;
        const stance = u < 0.62;
        const swing = Math.max(0, (u - 0.62) / 0.38);
        const footX = stance ? 0.25 - 0.50 * (u / 0.62) : -0.25 + 0.50 * smoothstep(swing);
        const lift = stance ? 0 : 0.17 * Math.sin(swing * Math.PI);
        leg.foot.position.set(footX, lift, leg.side * 0.145);
        leg.foot.rotation.z = stance ? 0 : 0.10 * Math.sin(swing * tau);
        leg.h.set(-0.025, 0.995 + bob, leg.side * 0.145 + sway);
        leg.a.set(footX - 0.012, 0.113 + lift, leg.side * 0.145);
        const dx = leg.a.x - leg.h.x;
        const dy = leg.a.y - leg.h.y;
        const distance = Math.max(0.001, Math.hypot(dx, dy));
        const upperLength = 0.485;
        const lowerLength = 0.475;
        const reach = Math.min(distance, upperLength + lowerLength - 0.001);
        const along = (upperLength * upperLength - lowerLength * lowerLength + reach * reach) / (2 * reach);
        const bend = Math.sqrt(Math.max(0, upperLength * upperLength - along * along));
        // Forward-bending knee IK keeps the planted foot on the sidewalk
        // instead of rotating an entire straight leg through the floor.
        leg.k.set(leg.h.x + dx / distance * along - dy / distance * bend,
          leg.h.y + dy / distance * along + dx / distance * bend,
          leg.side * 0.145 + sway * 0.5);
        connect(leg.upper, leg.h, leg.k);
        connect(leg.lower, leg.k, leg.a);
        leg.hip.position.copy(leg.h);
        leg.knee.position.copy(leg.k);
        leg.cuff.position.copy(leg.a);
        leg.cuff.position.y += 0.025;
      });
      arms.forEach((arm, index) => {
        const u = (cycle + index * 0.5) % 1;
        const angle = -0.47 * Math.cos(u * tau);
        const forearmAngle = angle + 0.31;
        arm.s.set(0.003, 1.586 + bob, arm.side * 0.253 + sway);
        arm.e.set(arm.s.x + Math.sin(angle) * 0.285,
          arm.s.y - Math.cos(angle) * 0.285, arm.side * 0.268 + sway);
        arm.w.set(arm.e.x + Math.sin(forearmAngle) * 0.265,
          arm.e.y - Math.cos(forearmAngle) * 0.265, arm.side * 0.282 + sway);
        connect(arm.upper, arm.s, arm.e);
        connect(arm.lower, arm.e, arm.w);
        arm.shoulder.position.copy(arm.s);
        arm.elbow.position.copy(arm.e);
        arm.hand.position.copy(arm.w);
        arm.hand.rotation.z = forearmAngle;
        arm.carry.position.copy(arm.w);
        arm.carry.rotation.z = forearmAngle * 0.65;
      });
    };

    const revealCanvas = () => {
      canvas.style.visibility = 'visible';
      host.dataset.renderer = 'webgl';
      if (fallback) {
        fallback.hidden = true;
        fallback.setAttribute('hidden', '');
      }
    };
    const render = () => {
      if (destroyed || contextLost) return false;
      try {
        renderer.render(scene, camera);
        revealCanvas();
        return true;
      } catch (_) {
        pause();
        canvas.style.visibility = 'hidden';
        showFallback();
        return false;
      }
    };
    const tick = (_time, deltaTime) => {
      if (!playing || destroyed || contextLost) return;
      const delta = Math.min(Math.max(Number(deltaTime) || 16.67, 0), 64) / 1000;
      elapsed += delta;
      accumulated += delta;
      if (accumulated < 1 / 30) return;
      accumulated %= 1 / 30;
      pose(elapsed);
      render();
    };
    function pause() {
      playing = false;
      resumeOnRestore = false;
      accumulated = 0;
      gsap.ticker.remove(tick);
      host.dataset.playing = 'false';
    }
    function play() {
      if (destroyed || playing || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      if (contextLost) {
        resumeOnRestore = true;
        return;
      }
      playing = true;
      accumulated = 0;
      host.dataset.playing = 'true';
      gsap.ticker.add(tick);
    }
    function resize() {
      if (destroyed || contextLost) return;
      const bounds = host.getBoundingClientRect();
      const width = Math.max(1, Math.round(bounds.width || 110));
      const height = Math.max(1, Math.round(bounds.height || 130));
      const dpr = Math.min(window.devicePixelRatio || 1, innerWidth < 700 ? 1.25 : 1.5);
      const nextDuration = cycleForViewport();
      if (nextDuration !== cycleDuration) {
        elapsed = elapsed / cycleDuration * nextDuration;
        cycleDuration = nextDuration;
      }
      if (width !== lastWidth || height !== lastHeight || renderer.getPixelRatio() !== dpr) {
        lastWidth = width;
        lastHeight = height;
        renderer.setPixelRatio(dpr);
        renderer.setSize(width, height, false);
        const halfWidth = 2.39 * width / height / 2;
        camera.left = -halfWidth;
        camera.right = halfWidth;
        camera.updateProjectionMatrix();
      }
      render();
    }
    const staticPose = () => {
      pause();
      elapsed = 0;
      pose(0);
      render();
    };
    const snapshot = () => {
      if (!render()) return null;
      try { return canvas.toDataURL('image/png'); } catch (_) { return null; }
    };
    const lost = (event) => {
      event.preventDefault();
      const wasPlaying = playing;
      contextLost = true;
      pause();
      resumeOnRestore = wasPlaying;
      canvas.style.visibility = 'hidden';
      showFallback();
    };
    const restored = () => {
      if (destroyed) return;
      contextLost = false;
      lastWidth = 0;
      lastHeight = 0;
      pose(elapsed);
      resize();
      if (resumeOnRestore && !document.hidden && !matchMedia('(prefers-reduced-motion: reduce)').matches) play();
      resumeOnRestore = false;
    };
    canvas.addEventListener('webglcontextlost', lost);
    canvas.addEventListener('webglcontextrestored', restored);

    const destroy = () => {
      if (destroyed) return;
      pause();
      destroyed = true;
      canvas.removeEventListener('webglcontextlost', lost);
      canvas.removeEventListener('webglcontextrestored', restored);
      geometries.forEach((geometry) => geometry.dispose());
      materials.forEach((mat) => mat.dispose());
      renderer.dispose();
      renderer.forceContextLoss();
      canvas.remove();
      showFallback();
    };

    pose(0);
    resize();
    return { play, pause, resize, static: staticPose, snapshot, destroy };
  };
})();
