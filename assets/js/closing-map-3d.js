/* Original, schematic city maquette. No geographic or analytical data implied.
 * Shared GSAP ticker only; the page's motion lifecycle owns visibility/pause. */
(() => {
  'use strict';

  window.createClosingMap3D = (host, { gsap } = {}) => {
    if (!host) return null;
    // Authored conceptual scenes. None represents measured case-study data.
    const variants = {
      city: { rotation: 0, riverWidth: 0.29, omitted: [] },
      district: { rotation: -0.055, riverWidth: 0.29, omitted: [] },
      garden: { rotation: 0.045, riverWidth: 0.29, omitted: [4, 5, 6, 7] },
      river: { rotation: -0.035, riverWidth: 0.34, omitted: [2, 3, 10, 11, 19] },
      atlas: { rotation: 0, semantic: true, halfHeight: 2.45, halfWidth: 6.2 },
      method: { rotation: 0, semantic: true, halfHeight: 2.85, halfWidth: 3.6 },
      fieldnotes: { rotation: 0, semantic: true, halfHeight: 2.8, halfWidth: 4.0 },
      inquiry: { rotation: 0, semantic: true, halfHeight: 2.35, halfWidth: 3.5 }
    };
    const variantName = Object.hasOwn(variants, host.dataset.mapVariant) ? host.dataset.mapVariant : 'city';
    const variant = variants[variantName];
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
    if (variantName === 'atlas') {
      camera.position.set(3.8, 10.5, 16);
      camera.lookAt(0, 0.35, 0);
    } else if (variant.semantic) {
      camera.position.set(7, 10, 13);
      camera.lookAt(0, variantName === 'method' ? 0.9 : 0.15, 0);
    }
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
      // Limestone, warm concrete, oxidised clay and sage keep every variant
      // in the same architectural material family, including the static poster.
      base: material(0xc4b7a0), land: material(0xe1d9c7), edge: material(0x8b8172),
      paper: material(0xefe7d9), stone: material(0xc9c4b5), roof: material(0x9ca99b),
      roofDark: material(0x748a80), glass: material(0x78918a), clay: material(0xb87558),
      road: material(0xf3ecde), sidewalk: material(0xd1c8b5), park: material(0xa5b08b),
      lawn: material(0xb7bf9c), tree: material(0x6f8670), treeLight: material(0x92a080),
      trunk: material(0x8b765f), water: material(0x85a3a0, { roughness: 0.48 }),
      bank: material(0xc8cbaa), route: material(0xb9674c, { emissive: 0x783a25, emissiveIntensity: 0.10 }),
      signal: material(0xffd29b, { emissive: 0xce8a4f, emissiveIntensity: 0.55 })
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
    let route, runner, stops = [];
    const projectedPoints = [];
    const focusMaterials = [];
    const routeLine = (points, radius = 0.025, routeMaterial = mat.route) => {
      const curve = new T.CatmullRomCurve3(points.map((p) => new T.Vector3(...p)), false, 'centripetal', 0.1);
      mesh(geometry(new T.TubeGeometry(curve, 96, radius, 6, false)), routeMaterial);
      return curve;
    };
    const plant = (x, z, y = 0.1, height = 0.4) => {
      mesh(unitCylinder, mat.trunk, [x, y + 0.10, z], [0.025, 0.20, 0.025]);
      mesh(crown, mat.tree, [x, y + height * 0.6 + 0.12, z], [height * 0.28, height * 0.6, height * 0.28]);
    };
    const pin = (x, z, y = 0.12, height = 0.58) => {
      mesh(unitCylinder, mat.route, [x, y + height * 0.45, z], [0.021, height * 0.9, 0.021]);
      mesh(crown, mat.clay, [x, y + height, z], [0.125, 0.16, 0.125]);
      mesh(crown, mat.paper, [x + 0.06, y + height + 0.02, z + 0.1], [0.04, 0.043, 0.03]);
    };
    const building = (x, z, w, h, d, color = mat.paper, y = 0.07) => {
      box(mat.sidewalk, x, y + 0.013, z, w + 0.11, 0.026, d + 0.11);
      box(color, x, y + h / 2, z, w, h, d);
      box(mat.roofDark, x, y + h + 0.009, z, w - 0.055, 0.018, d - 0.055);
      for (let floor = 0.15; floor < h - 0.06; floor += 0.26) {
        box(mat.glass, x, y + floor, z + d / 2 + 0.004, w * 0.72, 0.047, 0.007);
      }
    };
    const focusZone = (id, x, z, w, d, point) => {
      const focus = new T.MeshBasicMaterial({ color: 0xb9674c, transparent: true, opacity: 0, depthWrite: false });
      materials.push(focus);
      box(focus, x, 0.065, z, w, 0.009, d);
      focusMaterials[id] = focus;
      const element = host.querySelector(`[data-map-point="${id}"]`);
      if (element) projectedPoints.push({ element, point: new T.Vector3(...point), projected: new T.Vector3() });
    };

    if (variantName === 'atlas') {
      // A continuous rural-to-urban transect: each precinct describes the
      // subject of one portfolio project and is linked by native HTML controls.
      const ground = [[-5.4,-2.48],[-4.15,-2.7],[-1.4,-2.54],[1.3,-2.7],[3.9,-2.35],[5.15,-1.25],[5.2,1.8],[4.65,2.55],[1.2,2.6],[-1.3,2.4],[-4.85,2.6],[-5.4,1.5]];
      solid(ground, 0.045, mat.land, 0, 0.012);
      solid([[-5.33,-2.40],[-4.1,-2.61],[-1.75,-2.48],[-1.75,-0.50],[-5.33,-0.43]], 0.014, mat.lawn, 0.046);
      // 01 Transit: two tracks, sleepers, a platform and a canopy.
      [-0.19,0.19].forEach((offset) => box(mat.roofDark, -3.5, 0.085, 1.66 + offset, 3.23, 0.035, 0.035));
      for (let i = 0; i < 15; i += 1) box(mat.stone, -5.04 + i * 0.22, 0.063, 1.66, 0.05, 0.025, 0.55);
      box(mat.stone, -3.43, 0.115, 1.06, 2.25, 0.12, 0.63);
      [-4.25,-2.6].forEach((x) => [0.85,1.22].forEach((z) => box(mat.clay, x, 0.43, z, 0.045, 0.56, 0.045)));
      box(mat.paper, -3.43, 0.735, 1.06, 2.43, 0.09, 0.84);
      box(mat.paper, -4.02, 0.265, 1.67, 1.04, 0.31, 0.30);
      box(mat.glass, -4.02, 0.31, 1.826, 0.83, 0.10, 0.008);
      box(mat.clay, -4.02, 0.43, 1.67, 1.03, 0.02, 0.30);
      // 02 Food systems: shallow rice terraces and a modest logistics shed.
      for (let i = 0; i < 4; i += 1) {
        const z = -2.14 + i * 0.41, y = 0.06 + (3 - i) * 0.045;
        box(i % 2 ? mat.park : mat.lawn, -3.17, y, z, 2.1 - i * 0.12, 0.07, 0.36);
        box(mat.bank, -3.17, y + 0.049, z - 0.17, 2.08 - i * 0.12, 0.03, 0.032);
        box(mat.water, -3.17, y + 0.038, z + 0.08, 1.95 - i * 0.12, 0.008, 0.025);
      }
      building(-4.79, -1.69, 0.55, 0.35, 0.85, mat.clay);
      box(mat.stone, -4.71, 0.08, -0.99, 0.8, 0.035, 0.37);
      // 03 Earth observation: a lifted sample, with an authored raster mosaic.
      box(mat.paper, 0.03, 0.18, -1.73, 2.15, 0.18, 1.48);
      const raster = [mat.lawn,mat.park,mat.stone,mat.water,mat.paper,mat.roofDark];
      for (let row = 0; row < 4; row += 1) for (let column = 0; column < 6; column += 1) {
        const sample = (column + row * 2 + (row === 2 ? 1 : 0)) % raster.length;
        box(raster[sample], -0.84 + column * 0.34, 0.281, -2.25 + row * 0.34, 0.317, 0.022, 0.317);
      }
      // Fine registration corners describe sampling, without invented metrics.
      [[-1.13,-2.52],[1.2,-2.52],[-1.13,-0.94],[1.2,-0.94]].forEach(([x,z]) => {
        box(mat.route, x, 0.31, z, 0.25, 0.025, 0.025);
        box(mat.route, x, 0.31, z, 0.025, 0.025, 0.25);
      });
      // 04 Housing: fine grain, a shared court and short local streets.
      box(mat.road, 0.0, 0.068, 1.45, 2.2, 0.018, 0.16);
      box(mat.road, 0.10, 0.069, 1.53, 0.16, 0.018, 1.75);
      [[-0.75,0.98],[-0.25,0.98],[0.43,0.98],[0.92,0.98],[-0.72,1.97],[-0.2,1.97],[0.50,1.97],[1.0,1.97]].forEach(([x,z],i) => {
        building(x,z,0.33,0.26+(i%3)*0.09,0.43,i%3===0?mat.clay:mat.paper);
      });
      box(mat.park, -0.35, 0.064, 1.48, 0.4, 0.014, 0.36);
      plant(-0.34,1.48,0.07,0.3);
      // 05 Business district: concentrated towers, setbacks and a public forecourt.
      [[2.65,-1.12,0.58,1.05,0.64],[3.47,-0.91,0.61,1.60,0.62],[4.25,-0.46,0.52,1.17,0.58],[2.67,0.07,0.63,0.61,0.62],[3.66,0.43,0.72,0.80,0.62]].forEach(([x,z,w,h,d]) => {
        building(x,z,w,h,d);
        if (h > 1) building(x-0.05,z,w*0.62,0.20,d*0.63,mat.paper,h+0.07);
      });
      box(mat.road, 3.38, 0.07, 1.12, 2.38, 0.024, 0.55);
      [[2.38,1.58],[3.14,1.62],[4.26,1.1],[-1.56,0.87],[-1.57,-1.4]].forEach(([x,z])=>plant(x,z,0.06,0.36));
      // One restrained connective spine threads the five zones together.
      route = routeLine([[-4.77,0.095,0.16],[-2.85,0.095,0.1],[-1.45,0.095,-0.27],[0.4,0.095,-0.35],[1.72,0.095,0.02],[2.22,0.095,1.57],[4.25,0.095,1.78]], 0.018);
      runner = mesh(crown, mat.signal, null, [0.05,0.05,0.05]);
      focusZone(0,-3.5,1.36,3.25,1.65,[-3.17,0.12,2.28]);
      focusZone(1,-3.4,-1.6,3.05,1.8,[-2.66,0.21,-0.62]);
      focusZone(2,0.03,-1.73,2.54,1.93,[0.09,0.33,-0.81]);
      focusZone(3,0.1,1.52,2.4,1.7,[0.39,0.16,2.43]);
      focusZone(4,3.45,0.04,2.65,3.5,[3.48,0.14,1.63]);
    } else if (variantName === 'method') {
      // Spatial method made legible: terrain -> network -> decision, as three
      // thin registered layers. Height expresses process, never data magnitude.
      const plate = [[-2.65,-1.54],[2.15,-1.54],[2.45,-1.24],[2.45,1.44],[-2.65,1.44]];
      solid(plate,0.055,mat.land,0,0.012);
      solid([[-2.4,-1.30],[-0.8,-1.30],[-0.32,-0.8],[-0.75,0.34],[-1.65,0.82],[-2.4,0.7]],0.10,mat.bank,0.065,0.025);
      solid([[-2.35,-1.22],[-1.1,-1.22],[-0.67,-0.72],[-1.05,0.1],[-1.82,0.4],[-2.35,0.32]],0.075,mat.park,0.17,0.02);
      routeLine([[-2.35,0.075,0.96],[-0.73,0.075,0.52],[0.10,0.075,-0.24],[2.14,0.075,-0.48]],0.11,mat.water);
      solid(plate.map(([x,z])=>[x+0.22,z-0.10]),0.04,mat.paper,1.04,0.01);
      [-0.85,0.62].forEach((z)=>box(mat.sidewalk,0.15,1.09,z,4.6,0.018,0.055));
      [-1.32,0.13,1.43].forEach((x)=>box(mat.sidewalk,x,1.09,-0.06,0.055,0.018,2.61));
      route = routeLine([[-2.21,1.125,0.64],[-1.3,1.125,0.64],[-1.3,1.125,-0.82],[0.1,1.125,-0.82],[0.1,1.125,0.64],[1.98,1.125,0.64]],0.028);
      runner=mesh(crown,mat.signal,null,[0.065,0.065,0.065]);
      [-1.32,0.13,1.43].forEach((x)=>mesh(unitCylinder,mat.clay,[x,1.13,0.62],[0.085,0.025,0.085]));
      solid(plate.map(([x,z])=>[x+0.44,z-0.20]),0.04,mat.paper,2.07,0.01);
      solid([[-0.79,-0.98],[0.52,-0.98],[1.22,-0.45],[1.08,0.66],[-0.21,0.82],[-0.79,0.34]],0.023,mat.lawn,2.12,0.008);
      routeLine([[-0.76,2.17,0.35],[-0.76,2.17,-0.95],[0.50,2.17,-0.95],[1.18,2.17,-0.43],[1.05,2.17,0.63],[-0.19,2.17,0.79],[-0.76,2.17,0.35]],0.021);
      pin(0.15,0.13,2.14,0.38);
      // Small vertical registration marks tie the same place across layers.
      [[-2.38,-1.22],[2.2,1.04]].forEach(([x,z])=>{
        for(let y=0.32;y<2.04;y+=0.19) box(mat.stone,x+0.21,y,z-0.10,0.025,0.065,0.025);
      });
    } else if (variantName === 'fieldnotes') {
      // An open survey landscape and two paper notes: observation before claims.
      const site=[[-3.50,-1.54],[-2.24,-2.09],[-0.57,-1.81],[1.32,-2.1],[3.21,-0.96],[3.37,0.92],[2.16,1.80],[0.05,1.54],[-2.68,1.81],[-3.53,0.73]];
      solid(site,0.045,mat.land,0,0.015);
      solid([[-3.1,-1.21],[-1.76,-1.62],[-0.56,-1.33],[-0.38,-0.22],[-1.02,0.54],[-2.87,0.48]],0.08,mat.bank,0.06,0.018);
      solid([[-2.91,-1.08],[-1.80,-1.41],[-0.81,-1.13],[-0.77,-0.28],[-1.24,0.28],[-2.68,0.24]],0.07,mat.lawn,0.15,0.018);
      routeLine([[-3.09,0.075,1.02],[-1.49,0.075,0.72],[-0.31,0.075,-0.28],[1.12,0.075,-0.40],[2.85,0.075,0.1]],0.075,mat.water);
      [[-2.7,-0.74],[-2.07,-1.03],[-1.33,-0.60],[2.44,-0.98],[2.88,0.78]].forEach(([x,z])=>plant(x,z,0.12,0.36));
      // Deliberate pen strokes on paper, rather than decorative charts or values.
      [[0.02,0.76,0.25],[1.88,-0.96,0.30]].forEach(([x,z,y],index)=>{
        box(mat.stone,x+0.035,y-0.035,z+0.03,1.48,0.018,0.91);
        box(mat.paper,x,y,z,1.48,0.024,0.91);
        box(mat.clay,x-0.39,y+0.02,z-0.23,0.45,0.008,0.035);
        [0,1,2].forEach((line)=>box(mat.roofDark,x-0.1,y+0.023,z-0.03+line*0.15,0.99-line*0.13,0.008,0.014));
        pin(x+0.55,z-0.27,y+0.02,index?0.39:0.48);
      });
      route=routeLine([[-2.9,0.11,0.99],[-1.31,0.11,1.1],[0.55,0.11,1.34],[1.33,0.11,0.27],[2.53,0.11,0.10]],0.018);
      runner=mesh(crown,mat.signal,null,[0.045,0.045,0.045]);
    } else if (variantName === 'inquiry') {
      // A mostly open parcel and a single focus point leave room for a question.
      const site=[[-2.65,-1.43],[-0.93,-1.82],[1.58,-1.43],[2.68,-0.30],[2.21,1.46],[-0.28,1.77],[-2.65,0.99]];
      solid(site,0.045,mat.land,0,0.012);
      solid([[-2.42,-1.12],[-1.04,-1.49],[-0.5,-1.04],[-0.70,0.10],[-1.84,0.55],[-2.42,0.43]],0.035,mat.bank,0.06,0.012);
      solid([[-2.20,-0.96],[-1.12,-1.20],[-0.81,-0.88],[-1.01,-0.08],[-1.77,0.25],[-2.20,0.11]],0.035,mat.lawn,0.10,0.012);
      // One surveyed boundary; the main interior remains intentionally open.
      routeLine([[-0.32,0.075,-1.17],[1.45,0.075,-0.97],[2.12,0.075,-0.19],[1.69,0.075,1.04],[-0.22,0.075,1.21]],0.009,mat.stone);
      route=routeLine([[-2.10,0.085,0.95],[-0.85,0.085,0.80],[0.05,0.085,0.21],[0.91,0.085,0.16]],0.019);
      runner=mesh(crown,mat.signal,null,[0.045,0.045,0.045]);
      pin(0.91,0.16,0.09,0.80);
      mesh(unitCylinder,mat.paper,[0.91,0.088,0.16],[0.21,0.025,0.21]);
      plant(-1.74,-0.50,0.15,0.43);
      plant(-2.01,-0.22,0.15,0.31);
    } else {
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
    solid(ribbon(river, variant.riverWidth + 0.14), 0.016, mat.bank, 0.17);
    solid(ribbon(river, variant.riverWidth), 0.018, mat.water, 0.19);

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
    if (variantName === 'garden') {
      // Replace the civic towers with a walled garden and quiet central walk.
      solid([[-1.94,-2.85],[1.39,-2.85],[1.39,-1.84],[-1.94,-1.84]], 0.035, mat.lawn, 0.17, 0.025);
      box(mat.road, -0.28, 0.224, -2.35, 2.87, 0.02, 0.20);
      box(mat.stone, -0.28, 0.29, -2.81, 3.02, 0.15, 0.065);
      box(mat.clay, 0.82, 0.30, -2.02, 0.42, 0.13, 0.17);
    } else if (variantName === 'river') {
      // Open the low-rise waterfront into two riparian park precincts.
      solid([[-4.63,-1.39],[-2.58,-1.39],[-2.58,-0.77],[-3.8,-0.50],[-4.63,-0.46]], 0.027, mat.lawn, 0.17, 0.025);
      solid([[-4.63,0.53],[-2.58,0.40],[-2.58,1.28],[-4.63,1.28]], 0.027, mat.park, 0.17, 0.025);
      solid([[2.11,-1.36],[3.50,-1.36],[3.50,-0.78],[2.11,-0.78]], 0.027, mat.lawn, 0.17, 0.025);
      box(mat.road, -3.63, 0.22, 0.87, 1.78, 0.025, 0.14);
      box(mat.stone, -3.7, 0.28, 1.09, 0.58, 0.14, 0.13);
    }

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
    buildings.forEach(([x,z,w,baseHeight,d,color], index) => {
      if (variant.omitted.includes(index)) return;
      const h = baseHeight * (variantName === 'district' && [5, 6, 9, 18].includes(index) ? 1.24 : 1);
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
    if (variantName === 'garden') trees.push(
      [-1.65,-2.62],[-1.11,-2.62],[-0.52,-2.62],[0.14,-2.62],[0.78,-2.62],
      [-1.58,-2.06],[-0.93,-2.06],[-0.26,-2.06],[0.36,-2.06]
    );
    if (variantName === 'river') trees.push(
      [-4.33,-1.11],[-3.78,-1.15],[-3.20,-1.12],[-2.77,-1.01],
      [-4.29,0.64],[-3.79,0.58],[-3.27,0.61],[-2.79,1.06],
      [2.41,-1.11],[2.83,-1.09],[3.22,-1.09]
    );
    trees.forEach(([x,z], i) => {
      const h = 0.24 + (i % 3) * 0.035;
      mesh(unitCylinder, mat.trunk, [x, 0.28, z], [0.026, 0.16, 0.026]);
      mesh(crown, i % 3 ? mat.tree : mat.treeLight, [x, 0.35 + h * 0.5, z], [0.15, h, 0.15]);
    });

    // The narrow terracotta itinerary is tied to streets and a bridge.
    // Spline corners are deliberately softened rather than dashboard-like.
    route = new T.CatmullRomCurve3([
      new T.Vector3(-4.38,0.29,1.52), new T.Vector3(-2.58,0.29,1.52),
      new T.Vector3(-2.25,0.29,1.23), new T.Vector3(-2.25,0.29,-1.27),
      new T.Vector3(-1.92,0.29,-1.60), new T.Vector3(1.34,0.29,-1.60),
      new T.Vector3(1.65,0.29,-1.26), new T.Vector3(1.65,0.29,1.20),
      new T.Vector3(1.96,0.29,1.52), new T.Vector3(3.45,0.29,1.52)
    ], false, 'centripetal', 0.1);
    mesh(geometry(new T.TubeGeometry(route, 160, 0.025, 6, false)), mat.route);
    runner = mesh(crown, mat.signal, null, [0.065,0.065,0.065]);
    stops = [0.035, 0.33, 0.60, 0.965].map((u) => {
      const point = route.getPointAt(u);
      mesh(unitCylinder, mat.paper, [point.x,0.28,point.z], [0.104,0.026,0.104]);
      mesh(unitCylinder, mat.route, [point.x,0.303,point.z], [0.064,0.032,0.064]);
      const pulseMat = new T.MeshBasicMaterial({ color: 0xcf9873, transparent: true, opacity: 0.38, side: T.DoubleSide, depthWrite: false });
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
    }

    let playing = false, destroyed = false, contextLost = false, resumeOnRestore = false;
    let seconds = 0, accumulated = 0, lastWidth = 0, lastHeight = 0;
    const state = (time, moving = true) => {
      map.rotation.y = variant.rotation + (moving ? Math.sin(time * 0.18) * (variant.semantic ? 0.008 : 0.026) : 0);
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
      projectedPoints.forEach(({ element, point, projected }) => {
        projected.copy(point).applyMatrix4(map.matrixWorld).project(camera);
        element.style.left = `${(projected.x * 0.5 + 0.5) * 100}%`;
        element.style.top = `${(-projected.y * 0.5 + 0.5) * 100}%`;
      });
    };
    const resize = () => {
      if (destroyed || contextLost) return;
      const { width, height } = host.getBoundingClientRect();
      if (!width || !height) return;
      const ratio = width / height;
      // Width-fit on portrait screens and height-fit on the wider desktop
      // canvas. Both keep the complete slab + pin inside the camera frustum.
      const halfHeight = Math.max(variant.halfHeight || 4.08, (variant.halfWidth || 6.22) / ratio);
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
    const selectionListeners = [];
    if (variantName === 'atlas') {
      const scope = host.closest('.study-atlas') || host;
      const links = [...new Set([...scope.querySelectorAll('[data-map-select]'), ...host.querySelectorAll('[data-map-point]')])];
      const updateSelection = () => {
        const selected = links.find((link) => link === document.activeElement) || links.find((link) => link.matches(':hover'));
        const active = selected ? Number(selected.dataset.mapSelect ?? selected.dataset.mapPoint) : -1;
        focusMaterials.forEach((focus, i) => { focus.opacity = i === active ? 0.20 : 0; });
        links.forEach((link) => { link.dataset.mapActive = String(Number(link.dataset.mapSelect ?? link.dataset.mapPoint) === active); });
        host.dataset.activeMapPoint = active < 0 ? '' : String(active);
        render();
      };
      links.forEach((link) => ['pointerenter','pointerleave','focus','blur'].forEach((type) => {
        link.addEventListener(type,updateSelection);
        selectionListeners.push([link,type,updateSelection]);
      }));
    }
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
        selectionListeners.forEach(([link,type,listener])=>link.removeEventListener(type,listener));
        geometries.forEach((g) => g.dispose()); materials.forEach((m) => m.dispose());
        renderer.dispose(); canvas.remove(); fallback();
      }
    };
  };
})();
