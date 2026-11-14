/* EnerFab — 3D model of a biomass gasifier plant.
   Built from simple shapes (no model file), modelled on EnerFab's own plant
   drawing and photos: fuelwood store, orange hopper on an aluminium-clad
   reactor with a steel platform, gas pipework, a producer-gas flame and a
   gas engine generator. Glowing particles show the gas flowing.

   Two modes:
   - [data-plant3d][data-tour]  scroll-driven camera tour (home page). The
     enclosing .tour section and its .step blocks drive the camera.
   - [data-plant3d]             free orbit with clickable hotspots.
   A fallback <img> inside the mount stays visible if WebGL is unavailable. */
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// Wording taken from efpl.org
const PARTS = {
  fuelwood: { title: 'Fuelwood', text: 'Gliricidia, Ipil Ipil, cinnamon, timber off-cuts and coconut shells, from EnerFab’s plantation and a collection network of 3,000 farmers.' },
  hopper: { title: 'Hopper', text: 'Fuelwood sticks are chopped into small pieces for the gasifier. The EnerFab DM500 wood chopper processes 500 kg of fuelwood per hour.' },
  reactor: { title: 'Reactor', text: 'Gasification converts solid fuel into a combustible gas: producer gas.' },
  flame: { title: 'Producer gas flame', text: 'For heat, the gas is piped just like LPG to a burner on a boiler, furnace, kiln or dryer.' },
  engine: { title: 'Engine', text: 'For electricity, producer gas runs an internal combustion engine that turns a generator. EnerFab installed one that makes 200 kW from waste wood.' }
};

function mount(el) {
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
  } catch (e) { return; }
  if (!renderer.getContext()) return;

  const tourMode = el.hasAttribute('data-tour');
  const small = Math.min(window.innerWidth, window.innerHeight) < 700;
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, small ? 1.5 : 1.75));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.domElement.setAttribute('role', 'img');
  renderer.domElement.setAttribute('aria-label', '3D model of an EnerFab biomass gasifier plant: fuelwood, hopper, reactor, producer gas flame and engine.');
  el.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 100);

  /* ---------- materials ---------- */
  const M = {
    clad: new THREE.MeshStandardMaterial({ color: 0xc8cecd, metalness: 0.85, roughness: 0.3 }),
    orange: new THREE.MeshStandardMaterial({ color: 0xe5621c, metalness: 0.25, roughness: 0.42 }),
    steel: new THREE.MeshStandardMaterial({ color: 0x1d2220, metalness: 0.55, roughness: 0.5 }),
    pipe: new THREE.MeshStandardMaterial({ color: 0x252a28, metalness: 0.6, roughness: 0.38 }),
    stainless: new THREE.MeshStandardMaterial({ color: 0xdfe3e2, metalness: 1, roughness: 0.2 }),
    vessel: new THREE.MeshStandardMaterial({ color: 0x55605a, metalness: 0.4, roughness: 0.45 }),
    green: new THREE.MeshStandardMaterial({ color: 0x3f8a3f, metalness: 0.3, roughness: 0.45 }),
    grille: new THREE.MeshStandardMaterial({ color: 0x1a201c, metalness: 0.5, roughness: 0.6 }),
    slab: new THREE.MeshStandardMaterial({ color: 0x3c4741, metalness: 0, roughness: 0.92 }),
    grate: new THREE.MeshStandardMaterial({ color: 0x2b322e, metalness: 0.5, roughness: 0.55 }),
    wood: new THREE.MeshStandardMaterial({ color: 0x8a6440, roughness: 0.85 }),
    woodEnd: new THREE.MeshStandardMaterial({ color: 0xc9a273, roughness: 0.8 }),
    leaf: new THREE.MeshStandardMaterial({ color: 0x3f9a46, roughness: 0.7 }),
    roof: new THREE.MeshStandardMaterial({ color: 0x5e6f68, metalness: 0.6, roughness: 0.4, side: THREE.DoubleSide }),
    glow: new THREE.MeshStandardMaterial({ color: 0x331100, emissive: 0xff6a1a, emissiveIntensity: 2.4 })
  };

  const plant = new THREE.Group();
  scene.add(plant);
  const add = (geo, mat, x, y, z, parent = plant) => {
    const m = new THREE.Mesh(geo, mat);
    m.position.set(x, y, z);
    m.castShadow = true; m.receiveShadow = true;
    parent.add(m);
    return m;
  };
  const cyl = (rt, rb, h, seg = 36) => new THREE.CylinderGeometry(rt, rb, h, seg);
  const box = (w, h, d) => new THREE.BoxGeometry(w, h, d);

  /* ---------- ground ---------- */
  const slab = add(box(12.4, 0.16, 5.6), M.slab, 0.2, -0.08, -0.2);
  slab.castShadow = false;
  const floor = new THREE.Mesh(new THREE.CircleGeometry(16, 64), new THREE.ShadowMaterial({ opacity: 0.4 }));
  floor.rotation.x = -Math.PI / 2; floor.position.y = -0.17; floor.receiveShadow = true;
  scene.add(floor);

  /* ---------- fuelwood store with curved roof, as in EnerFab's plant drawing ---------- */
  const WX = -4.6;
  const logGeo = cyl(0.07, 0.07, 1.2, 10);
  for (let row = 0; row < 6; row++) {
    for (let i = 0; i < 10 - row; i++) {
      const lg = add(logGeo, [M.wood, M.woodEnd, M.woodEnd], WX - 0.7 + i * 0.15 + row * 0.075, 0.07 + row * 0.13, 0.2 + Math.sin(i * 7.3 + row) * 0.05);
      lg.rotation.x = Math.PI / 2;
    }
  }
  for (let i = 0; i < 6; i++) {
    const l = add(new THREE.IcosahedronGeometry(0.22, 0), M.leaf, WX + 0.75 + (i % 3) * 0.25, 0.2 + Math.floor(i / 3) * 0.22, -0.9 + (i % 2) * 0.2);
    l.rotation.set(i, i * 2, 0);
  }
  [[-1.1, -1.4], [1.1, -1.4], [-1.1, 1.4], [1.1, 1.4]].forEach(([dx, dz]) => add(box(0.08, 2.2, 0.08), M.steel, WX + dx, 1.1, dz));
  const roof = add(new THREE.CylinderGeometry(1.25, 1.25, 3.0, 32, 1, true, -Math.PI / 2, Math.PI), M.roof, WX, 2.2, 0);
  roof.rotation.x = Math.PI / 2; roof.rotation.y = Math.PI / 2; roof.scale.set(1, 1, 0.45);

  /* ---------- reactor + hopper ---------- */
  const RX = -2.2;
  [[-0.55, -0.55], [0.55, -0.55], [-0.55, 0.55], [0.55, 0.55]].forEach(([dx, dz]) => add(box(0.09, 0.9, 0.09), M.steel, RX + dx, 0.45, dz));
  add(cyl(0.78, 0.3, 0.6), M.clad, RX, 1.15, 0);
  add(cyl(0.26, 0.26, 0.25), M.steel, RX, 0.78, 0);
  add(cyl(0.82, 0.82, 2.0, 48), M.clad, RX, 2.45, 0);
  add(cyl(0.9, 0.9, 0.08, 48), M.steel, RX, 3.47, 0);
  for (let i = 0; i < 24; i++) {
    const a = (i / 24) * Math.PI * 2;
    add(cyl(0.025, 0.025, 0.12, 8), M.steel, RX + Math.cos(a) * 0.86, 3.5, Math.sin(a) * 0.86);
  }
  add(cyl(0.66, 0.78, 0.75, 48), M.orange, RX, 3.88, 0);
  add(cyl(0.22, 0.66, 0.45, 48), M.orange, RX, 4.48, 0);
  add(cyl(0.28, 0.28, 0.08), M.steel, RX, 4.74, 0);
  const port = add(cyl(0.07, 0.07, 0.6, 20), M.orange, RX + 0.62, 3.95, 0.36);
  port.rotation.z = -0.9; port.rotation.x = 0.4;
  const glowPort = add(cyl(0.11, 0.11, 0.06, 28), M.glow, RX + 0.42, 1.95, 0.72);
  glowPort.rotation.x = Math.PI / 2; glowPort.rotation.z = 0.5; glowPort.castShadow = false;
  add(new THREE.TorusGeometry(0.13, 0.025, 10, 28), M.steel, RX + 0.42, 1.95, 0.73).rotation.y = 0.5;
  const fireLight = new THREE.PointLight(0xff7a2a, 3.5, 3.2, 2);
  fireLight.position.set(RX + 0.6, 1.95, 1.05);
  plant.add(fireLight);

  /* ---------- frame, platform, railings, stairs ---------- */
  const PY = 3.3;
  [[-1.05, -1.05], [1.05, -1.05], [-1.05, 1.05], [1.05, 1.05]].forEach(([dx, dz]) => add(box(0.12, PY + 1.15, 0.12), M.steel, RX + dx, (PY + 1.15) / 2, dz));
  add(box(2.2, 0.06, 0.6), M.grate, RX, PY, -0.8);
  add(box(2.2, 0.06, 0.6), M.grate, RX, PY, 0.8);
  add(box(0.6, 0.06, 1.0), M.grate, RX - 0.8, PY, 0);
  add(box(0.6, 0.06, 1.0), M.grate, RX + 0.8, PY, 0);
  const RH = 1.0;
  const rail = (x1, z1, x2, z2) => {
    const len = Math.hypot(x2 - x1, z2 - z1);
    const r = add(cyl(0.025, 0.025, len, 10), M.steel, (x1 + x2) / 2, PY + RH, (z1 + z2) / 2);
    r.rotation.z = Math.PI / 2; r.rotation.y = -Math.atan2(z2 - z1, x2 - x1);
    const r2 = r.clone(); r2.position.y = PY + RH / 2; plant.add(r2);
  };
  rail(RX - 1.1, -1.1, RX + 1.1, -1.1);
  rail(RX - 1.1, -1.1, RX - 1.1, 1.1);
  rail(RX + 1.1, -1.1, RX + 1.1, 1.1);
  rail(RX - 1.1, 1.1, RX + 0.3, 1.1);
  [[-1.1, -1.1], [0, -1.1], [1.1, -1.1], [-1.1, 0], [1.1, 0], [-1.1, 1.1], [1.1, 1.1], [0.3, 1.1]].forEach(([dx, dz]) =>
    add(cyl(0.025, 0.025, RH, 8), M.steel, RX + dx, PY + RH / 2, dz));
  const stairs = new THREE.Group();
  stairs.position.set(RX + 0.7, 0, 1.1);
  plant.add(stairs);
  const run = 2.4, steps = 13, ang = Math.atan2(PY, run), sLen = Math.hypot(PY, run);
  [0, 0.7].forEach((ox) => { add(box(0.06, 0.18, sLen), M.steel, ox, PY / 2, run / 2, stairs).rotation.x = ang; });
  for (let i = 1; i < steps; i++) { const t = i / steps; add(box(0.66, 0.04, 0.2), M.grate, 0.35, PY * (1 - t), run * t, stairs); }
  add(cyl(0.022, 0.022, sLen, 8), M.steel, 0.72, PY / 2 + 0.9, run / 2, stairs).rotation.x = Math.PI / 2 - ang;

  /* ---------- pipes ---------- */
  function pipeCurve(pts, bend = 0.22) {
    const path = new THREE.CurvePath();
    const P = pts.map((p) => new THREE.Vector3(...p));
    let cur = P[0].clone();
    for (let i = 1; i < P.length - 1; i++) {
      const a = P[i - 1], b = P[i], c = P[i + 1];
      const r = Math.min(bend, a.distanceTo(b) / 2, b.distanceTo(c) / 2);
      const p1 = b.clone().add(a.clone().sub(b).setLength(r));
      const p2 = b.clone().add(c.clone().sub(b).setLength(r));
      path.add(new THREE.LineCurve3(cur, p1));
      path.add(new THREE.QuadraticBezierCurve3(p1, b, p2));
      cur = p2;
    }
    path.add(new THREE.LineCurve3(cur, P[P.length - 1]));
    return path;
  }
  function pipe(pts, r = 0.07) {
    const c = pipeCurve(pts);
    const m = new THREE.Mesh(new THREE.TubeGeometry(c, 100, r, 14, false), M.pipe);
    m.castShadow = true; plant.add(m);
    return c;
  }
  const flange = (x, y, z, rz = 0, r = 0.11) => { add(cyl(r, r, 0.05, 20), M.steel, x, y, z).rotation.z = rz; };

  /* ---------- gas cleaning ---------- */
  const CX = -0.4;
  add(cyl(0.32, 0.32, 0.7), M.stainless, CX, 2.45, 0);
  add(cyl(0.32, 0.07, 0.8), M.stainless, CX, 1.7, 0);
  add(cyl(0.12, 0.12, 0.35), M.stainless, CX, 1.12, 0);
  add(cyl(0.18, 0.18, 0.3), M.vessel, CX, 0.8, 0);
  [[-0.3, -0.3], [0.3, -0.3], [-0.3, 0.3], [0.3, 0.3]].forEach(([dx, dz]) => add(box(0.06, 2.3, 0.06), M.steel, CX + dx, 1.15, dz));
  add(box(0.72, 0.06, 0.72), M.steel, CX, 2.1, 0);
  const vessel = (x, h) => {
    add(cyl(0.36, 0.36, h), M.vessel, x, 0.35 + h / 2, -0.15);
    add(new THREE.SphereGeometry(0.36, 28, 14, 0, Math.PI * 2, 0, Math.PI / 2), M.vessel, x, 0.35 + h, -0.15);
    [[-0.25, -0.4], [0.25, -0.4], [-0.25, 0.1], [0.25, 0.1]].forEach(([dx, dz]) => add(box(0.05, 0.35, 0.05), M.steel, x + dx, 0.175, dz));
    add(cyl(0.38, 0.38, 0.05), M.steel, x, 0.35 + h * 0.65, -0.15);
  };
  vessel(0.8, 1.9);
  vessel(1.7, 1.6);

  /* ---------- producer gas flame on a stack ---------- */
  const FX = 1.25, FZ = -1.5, FH = 3.1;
  add(cyl(0.09, 0.11, FH, 18), M.pipe, FX, FH / 2, FZ);
  add(cyl(0.15, 0.12, 0.14, 18), M.steel, FX, FH + 0.02, FZ);
  const flameGroup = new THREE.Group();
  flameGroup.position.set(FX, FH + 0.1, FZ);
  plant.add(flameGroup);
  const flameMat = (c, o) => new THREE.MeshBasicMaterial({ color: c, transparent: true, opacity: o, blending: THREE.AdditiveBlending, depthWrite: false });
  const outer = new THREE.Mesh(new THREE.ConeGeometry(0.2, 0.95, 20, 1, true), flameMat(0xff7a2a, 0.75));
  outer.position.y = 0.47;
  const inner = new THREE.Mesh(new THREE.ConeGeometry(0.1, 0.45, 16, 1, true), flameMat(0x6fb6ff, 0.9));
  inner.position.y = 0.22;
  const glowS = new THREE.Mesh(new THREE.SphereGeometry(0.35, 16, 12), flameMat(0xff6a1a, 0.18));
  glowS.position.y = 0.35;
  flameGroup.add(outer, inner, glowS);
  const flameLight = new THREE.PointLight(0xff8a3a, 6, 5, 2);
  flameLight.position.set(FX, FH + 0.5, FZ);
  plant.add(flameLight);

  /* ---------- blower + gas engine generator ---------- */
  add(box(0.5, 0.36, 0.4), M.steel, 2.55, 0.5, 0.35);
  add(cyl(0.3, 0.3, 0.22, 32), M.orange, 2.55, 0.95, 0.35).rotation.x = Math.PI / 2;
  add(box(0.32, 0.26, 0.3), M.green, 2.55, 0.95, 0.66);
  const EX = 4.3;
  add(box(2.3, 0.14, 1.2), M.steel, EX, 0.07, 0);
  add(box(2.1, 1.25, 1.0), M.green, EX, 0.77, 0);
  add(box(0.06, 1.0, 0.86), M.grille, EX + 1.07, 0.75, 0);
  for (let i = 0; i < 9; i++) add(box(0.07, 0.025, 0.86), M.steel, EX + 1.09, 0.32 + i * 0.105, 0);
  for (let i = 0; i < 6; i++) add(box(0.3, 0.02, 0.02), M.grille, EX - 0.6 + i * 0.12, 1.0, 0.51);
  add(box(0.5, 0.36, 0.04), M.grille, EX - 0.3, 0.7, 0.51);
  add(cyl(0.07, 0.07, 1.0, 16), M.pipe, EX + 0.6, 1.9, -0.25);
  add(cyl(0.1, 0.07, 0.12, 16), M.pipe, EX + 0.6, 2.42, -0.25);

  /* ---------- gas line ---------- */
  const segs = [
    pipe([[RX + 0.8, 2.6, 0], [CX - 0.75, 2.6, 0], [CX - 0.75, 2.6, 0.3], [CX - 0.3, 2.6, 0.3]], 0.085),
    pipe([[CX, 2.8, 0], [CX, 3.25, 0], [0.8, 3.25, 0], [0.8, 3.25, -0.15], [0.8, 2.6, -0.15]], 0.075),
    pipe([[0.8, 0.55, 0.21], [0.8, 0.55, 0.45], [1.7, 0.55, 0.45], [1.7, 0.55, 0.21]], 0.07),
    pipe([[1.7, 2.3, -0.15], [1.7, 2.6, -0.15], [2.55, 2.6, -0.15], [2.55, 2.6, 0.35], [2.55, 1.25, 0.35]], 0.07),
    pipe([[2.85, 0.95, 0.35], [3.15, 0.95, 0.35], [3.15, 1.6, 0.35], [3.75, 1.6, 0.35], [3.75, 1.4, 0.35]], 0.065)
  ];
  const branch = pipe([[1.7, 2.6, -0.15], [1.7, 2.6, -0.9], [FX, 2.6, -0.9], [FX, 2.6, FZ + 0.1]], 0.06);
  flange(RX + 0.86, 2.6, 0, Math.PI / 2, 0.13);
  flange(CX, 2.83, 0, 0, 0.12);
  flange(0.8, 2.58, -0.15);
  flange(1.7, 2.28, -0.15);
  flange(3.75, 1.42, 0.35, 0, 0.1);

  /* ---------- gas particles ---------- */
  const lens = segs.map((c) => c.getLength());
  const total = lens.reduce((a, b) => a + b, 0);
  const COUNT = small ? 70 : 120;
  const BR = 24;
  const pos = new Float32Array((COUNT + BR) * 3);
  const col = new Float32Array((COUNT + BR) * 3);
  const offs = Array.from({ length: COUNT + BR }, () => Math.random());
  const pGeo = new THREE.BufferGeometry();
  pGeo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  pGeo.setAttribute('color', new THREE.BufferAttribute(col, 3));
  const c2 = document.createElement('canvas'); c2.width = c2.height = 64;
  const g = c2.getContext('2d');
  const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.35, 'rgba(255,255,255,.5)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = gr; g.fillRect(0, 0, 64, 64);
  const sprite = new THREE.CanvasTexture(c2);
  plant.add(new THREE.Points(pGeo, new THREE.PointsMaterial({ size: 0.17, map: sprite, vertexColors: true, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending })));
  const hot = new THREE.Color(0xff7a2a), cool = new THREE.Color(0x8fe39a), tmp = new THREE.Vector3(), cc = new THREE.Color();
  function placeParticles(time) {
    for (let i = 0; i < COUNT + BR; i++) {
      if (i < COUNT) {
        const f = (offs[i] + time * 0.045) % 1;
        let d = f * total, k = 0;
        while (k < segs.length - 1 && d > lens[k]) { d -= lens[k]; k++; }
        segs[k].getPointAt(Math.min(d / lens[k], 1), tmp);
        cc.copy(hot).lerp(cool, Math.min(1, f * 1.4));
      } else {
        const f = (offs[i] + time * 0.12) % 1;
        branch.getPointAt(f, tmp);
        cc.copy(cool).lerp(hot, f);
      }
      pos[i * 3] = tmp.x; pos[i * 3 + 1] = tmp.y; pos[i * 3 + 2] = tmp.z;
      col[i * 3] = cc.r; col[i * 3 + 1] = cc.g; col[i * 3 + 2] = cc.b;
    }
    pGeo.attributes.position.needsUpdate = true;
    pGeo.attributes.color.needsUpdate = true;
  }
  placeParticles(0);

  /* ---------- lights ---------- */
  scene.add(new THREE.HemisphereLight(0xdfeee5, 0x1a241e, 0.55));
  const sun = new THREE.DirectionalLight(0xfff1de, 2.2);
  sun.position.set(5, 9, 6);
  sun.castShadow = true;
  sun.shadow.mapSize.set(small ? 1024 : 2048, small ? 1024 : 2048);
  Object.assign(sun.shadow.camera, { left: -8, right: 8, top: 7, bottom: -4, near: 1, far: 25 });
  sun.shadow.bias = -0.0005;
  scene.add(sun);
  const rim = new THREE.DirectionalLight(0x9fd0ff, 0.8);
  rim.position.set(-6, 4, -6);
  scene.add(rim);

  const anchors = {
    fuelwood: new THREE.Vector3(WX, 1.1, 0.4),
    hopper: new THREE.Vector3(RX, 4.6, 0),
    reactor: new THREE.Vector3(RX + 0.8, 2.0, 0.4),
    flame: new THREE.Vector3(FX, FH + 0.6, FZ),
    engine: new THREE.Vector3(EX, 1.45, 0.4)
  };

  let W = 1, H = 1;
  const v = new THREE.Vector3();
  const project = (p) => { v.copy(p).project(camera); return { x: ((v.x + 1) / 2) * W, y: ((1 - v.y) / 2) * H, off: v.z > 1 || Math.abs(v.x) > 1.05 || Math.abs(v.y) > 1.05 }; };

  let update = () => {};
  let refit = null;
  if (tourMode) {
    /* ---------- scroll tour ---------- */
    const section = el.closest('.tour');
    const stepEls = section ? [...section.querySelectorAll('.step')] : [];
    const K = [
      [[12.5, 7.2, 16.5], [0.2, 1.9, 0], null],
      [[-2.2, 4.2, 6.6], [-4.4, 1.2, 0.2], 'fuelwood'],
      [[0.6, 6.6, 6.2], [-2.2, 3.4, 0.2], 'hopper'],
      [[1.4, 2.4, 5.4], [-2.0, 1.9, 0.3], 'reactor'],
      [[4.6, 4.8, 3.6], [1.2, 3.0, -1.2], 'flame'],
      [[8.2, 2.8, 5.2], [4.2, 1.0, 0], 'engine'],
      [[-8.5, 7.0, 10.5], [0.2, 1.4, 0], null]
    ].map(([p, t, tag]) => ({ p: new THREE.Vector3(...p), t: new THREE.Vector3(...t), tag }));
    const tag = document.createElement('div');
    tag.className = 'tag3d';
    tag.setAttribute('aria-hidden', 'true');
    tag.innerHTML = '<i></i><span></span>';
    el.appendChild(tag);
    const pCur = new THREE.Vector3(), tCur = new THREE.Vector3(), pGoal = new THREE.Vector3(), tGoal = new THREE.Vector3();
    let first = true, mx = 0, my = 0;
    if (!reduceMotion) window.addEventListener('pointermove', (e) => { mx = e.clientX / window.innerWidth - 0.5; my = e.clientY / window.innerHeight - 0.5; }, { passive: true });
    const smooth = (x) => x * x * (3 - 2 * x);
    function progress() {
      if (!stepEls.length) return 0;
      const mid = window.innerHeight * 0.5;
      const centers = stepEls.map((s) => { const r = s.getBoundingClientRect(); return r.top + r.height / 2; });
      if (mid <= centers[0]) return 0;
      for (let i = 0; i < centers.length - 1; i++) {
        if (mid <= centers[i + 1]) return i + (mid - centers[i]) / (centers[i + 1] - centers[i]);
      }
      return centers.length - 1;
    }
    update = (dt) => {
      const p = Math.min(progress(), K.length - 1);
      const k = Math.min(Math.floor(p), K.length - 2), f = smooth(Math.min(1, p - k));
      const portrait = W / H < 0.9;
      pGoal.lerpVectors(K[k].p, K[k + 1].p, f);
      tGoal.lerpVectors(K[k].t, K[k + 1].t, f);
      // close-ups sit further back so the whole part stays in view
      // narrower landscape screens pull back too, so the plant still fits beside the text
      const aspectPull = portrait ? 1.55 : Math.max(1, 1.75 / (W / H));
      const zoom = aspectPull * (1 + 0.55 * (1 - Math.abs(2 * (p / (K.length - 1)) - 1) ** 6));
      pGoal.sub(tGoal).multiplyScalar(zoom).add(tGoal);
      if (first || reduceMotion) { pCur.copy(pGoal); tCur.copy(tGoal); first = false; }
      const e = 1 - Math.pow(0.0015, dt);
      pCur.lerp(pGoal, e); tCur.lerp(tGoal, e);
      camera.position.copy(pCur);
      camera.position.x += mx * 0.6; camera.position.y -= my * 0.3;
      camera.lookAt(tCur);
      // keep the subject clear of the text: right of centre on wide screens, upper half on phones
      if (portrait) camera.setViewOffset(W, H, 0, H * 0.2, W, H);
      else camera.setViewOffset(W, H, -W * 0.25, 0, W, H);  // plant centred in the right half, clear of the text column
      const near = Math.round(p);
      const key = Math.abs(p - near) < 0.32 ? K[near].tag : null;
      if (key) {
        const s = project(anchors[key]);
        tag.querySelector('span').textContent = PARTS[key].title;
        tag.style.transform = `translate(${s.x - 7}px, ${s.y - 7}px)`;
        tag.classList.toggle('is-on', !s.off);
      } else tag.classList.remove('is-on');
    };
  } else {
    /* ---------- free orbit with hotspots ---------- */
    camera.position.set(7, 5, 10);
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.target.set(0, 1.6, -0.2);
    Object.assign(controls, { enableZoom: false, enablePan: false, enableDamping: true, dampingFactor: 0.06, minPolarAngle: 0.7, maxPolarAngle: 1.45, autoRotate: !reduceMotion, autoRotateSpeed: 0.5 });
    renderer.domElement.style.touchAction = 'pan-y';
    let idle;
    controls.addEventListener('start', () => { controls.autoRotate = false; clearTimeout(idle); });
    controls.addEventListener('end', () => { if (!reduceMotion) idle = setTimeout(() => (controls.autoRotate = true), 6000); });
    const card = document.createElement('div');
    card.className = 'hotcard';
    card.setAttribute('aria-live', 'polite');
    card.innerHTML = '<button type="button" aria-label="Close">×</button><h3></h3><p></p>';
    el.appendChild(card);
    const spots = Object.keys(anchors).map((key) => {
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'hotspot';
      b.setAttribute('aria-expanded', 'false');
      b.setAttribute('aria-label', PARTS[key].title);
      b.innerHTML = '<i></i><span>' + PARTS[key].title + '</span>';
      b.addEventListener('click', () => {
        const open = b.getAttribute('aria-expanded') === 'true';
        spots.forEach((s) => s.b.setAttribute('aria-expanded', 'false'));
        if (open) { card.classList.remove('is-open'); return; }
        b.setAttribute('aria-expanded', 'true');
        card.querySelector('h3').textContent = PARTS[key].title;
        card.querySelector('p').textContent = PARTS[key].text;
        card.classList.add('is-open');
        controls.autoRotate = false; clearTimeout(idle);
      });
      el.appendChild(b);
      return { key, b };
    });
    card.querySelector('button').addEventListener('click', () => {
      card.classList.remove('is-open');
      spots.forEach((s) => s.b.setAttribute('aria-expanded', 'false'));
      if (!reduceMotion) controls.autoRotate = true;
    });
    let fitted = false;
    refit = () => { fitted = false; };
    update = () => {
      if (!fitted) {
        const vt = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2));
        const dist = Math.max(6.4 / (vt * camera.aspect), 3.2 / vt);
        camera.position.copy(controls.target).add(camera.position.clone().sub(controls.target).setLength(dist));
        fitted = true;
      }
      controls.update();
      spots.forEach(({ key, b }) => {
        const s = project(anchors[key]);
        b.classList.toggle('is-hidden', s.off);
        b.style.transform = `translate(${s.x - 7}px, ${s.y - 7}px)`;
      });
    };
  }

  /* ---------- size + loop ---------- */
  function resize() {
    const r = el.getBoundingClientRect();
    W = Math.max(1, r.width); H = Math.max(1, r.height);
    renderer.setSize(W, H, false);
    camera.aspect = W / H;
    camera.updateProjectionMatrix();
    if (refit) refit();
  }
  new ResizeObserver(resize).observe(el);
  resize();

  const clock = new THREE.Clock();
  let visible = true, raf = 0, t = 0;
  function frame() {
    raf = 0;
    if (!visible) return;
    const dt = Math.min(clock.getDelta(), 0.05);
    if (!reduceMotion) {
      t += dt;
      placeParticles(t);
      const flick = 0.85 + Math.sin(t * 9) * 0.08 + Math.sin(t * 23) * 0.05;
      M.glow.emissiveIntensity = 2.4 * flick;
      fireLight.intensity = 3.5 * flick;
      flameLight.intensity = 6 * flick;
      outer.scale.set(1 + Math.sin(t * 13) * 0.06, 0.9 + flick * 0.15 + Math.sin(t * 7) * 0.05, 1 + Math.cos(t * 11) * 0.06);
      inner.scale.y = 0.9 + Math.sin(t * 17) * 0.1;
    }
    update(dt);
    renderer.render(scene, camera);
    raf = requestAnimationFrame(frame);
  }
  new IntersectionObserver((en) => {
    visible = en[0].isIntersecting;
    if (visible && !raf) { clock.getDelta(); raf = requestAnimationFrame(frame); }
  }).observe(el);
  document.addEventListener('visibilitychange', () => {
    visible = !document.hidden;
    if (visible && !raf) { clock.getDelta(); raf = requestAnimationFrame(frame); }
  });
  el.classList.add('is-3d');
  raf = requestAnimationFrame(frame);
}

document.querySelectorAll('[data-plant3d]').forEach((el) => {
  if (el.hasAttribute('data-lazy') && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver((en) => { if (en[0].isIntersecting) { io.disconnect(); mount(el); } }, { rootMargin: '400px' });
    io.observe(el);
  } else mount(el);
});
