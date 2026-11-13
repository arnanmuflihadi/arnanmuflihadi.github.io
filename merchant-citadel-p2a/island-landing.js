// Merchant Citadel P3-B batch 1: dynamic landing-surface scan on the loaded terrain (NOT a whitelist).
// Any loaded surface that meets the criteria is eligible; the four P3-A "examples" are only reported separately in the evidence.
// The criteria are this phase's proposal: the game's dragon system (free flight) is not in this branch (travelConfig.implemented = false), so nothing here is the game's own rule set.
export function createLandingScan(isl) {
  const { terrainAt, meta } = isl;
  const supported = (x, n) => terrainAt(x, n) > isl.NOSUP + 1;
  const solidTop = (o) => terrainAt(o.x, -o.z) + (o.h ?? 3);

  /** Disc test at plan centre (x, n). Returns null if the disc is not fully supported, else the measurements. */
  function evaluate(x, n, { radius, edgeClear = 4, obstacleClear = 1.0, maxRange = 0.5, maxSlope = 0.18, obstacles = [], approachRange = 40, approachClear = 3.0, glide = 0.10, dismountDist = 3.0 }) {
    const zc = terrainAt(x, n); if (zc <= isl.NOSUP + 1) return null;
    let zmin = zc, zmax = zc, rim = Infinity;
    for (const f of [0.25, 0.5, 0.75, 1.0]) for (let k = 0; k < 16; k++) { const a = k * Math.PI / 8, z = terrainAt(x + Math.cos(a) * radius * f, n + Math.sin(a) * radius * f); if (z <= isl.NOSUP + 1) return null; zmin = Math.min(zmin, z); zmax = Math.max(zmax, z); }
    for (let k = 0; k < 24; k++) { const a = k * Math.PI / 12; for (let d = radius; d <= radius + edgeClear + 8; d += 1) if (!supported(x + Math.cos(a) * d, n + Math.sin(a) * d)) { rim = Math.min(rim, d - radius); break; } }
    if (rim === Infinity) rim = edgeClear + 8;
    let slope = 0; for (let k = 0; k < 16; k++) { const a = k * Math.PI / 8; for (const f of [0.3, 0.7, 1.0]) { const px = x + Math.cos(a) * radius * f, pn = n + Math.sin(a) * radius * f; slope = Math.max(slope, Math.hypot(terrainAt(px + 0.5, pn) - terrainAt(px - 0.5, pn), terrainAt(px, pn + 0.5) - terrainAt(px, pn - 0.5))); } }
    let obs = Infinity, who = null;                                                     // nearest solid (town buildings, props, trunks), measured from the disc edge
    for (const o of obstacles) { if (o.cameraOnly || (o.h !== undefined && o.h < 0.3)) continue; const dx = Math.max(Math.abs(x - o.x) - o.w / 2, 0), dz = Math.max(Math.abs(-n - o.z) - o.d / 2, 0), d = Math.hypot(dx, dz) - radius; if (d < obs) { obs = d; who = o.src; } }
    const approach = [];                                                                // 15-degree bearings with a clear glide path: 3 m over the disc rising at `glide` out to approachRange
    for (let k = 0; k < 24; k++) { const a = k * Math.PI / 12; let ok = true;
      for (let d = radius + 2; d <= approachRange && ok; d += 2) { const px = x + Math.cos(a) * d, pn = n + Math.sin(a) * d, path = zc + approachClear + (d - radius) * glide; if (terrainAt(px, pn) > path) ok = false; }
      if (ok) for (const o of obstacles) { if (o.cameraOnly) continue; const dx = o.x - x, dz = -o.z - n, d = Math.hypot(dx, dz) - radius; if (d < 2 || d > approachRange) continue;
        const ang = Math.atan2(dz, dx), da = Math.abs(Math.atan2(Math.sin(ang - a), Math.cos(ang - a))), reach = Math.max(o.w, o.d) / 2 + 3; if (da * Math.hypot(dx, dz) > reach) continue; if (solidTop(o) > zc + approachClear + d * glide) { ok = false; break; } }
      if (ok) approach.push(k * 15); }
    let dismount = false; for (let k = 0; k < 16 && !dismount; k++) { const a = k * Math.PI / 8; for (let d = radius + 2; d <= radius + dismountDist + 3; d += 1) if (isl.comfortable(x + Math.cos(a) * d, -(n + Math.sin(a) * d))) { dismount = true; break; } }
    const range = zmax - zmin;
    return { x, n, z: zc, range, slope, rim_distance: rim, obstacle_clearance: obs, obstacle: who, approach_bearings: approach, dismount, eligible: range <= maxRange && slope <= maxSlope && rim >= edgeClear && obs >= obstacleClear && approach.length > 0 && dismount };
  }
  /** Grid scan: every node at `step`; returns the eligible discs. */
  function scan(opts, { step = 2, x0 = meta.grid_x[0], x1 = meta.grid_x[1], n0 = meta.grid_n[0], n1 = meta.grid_n[1] } = {}) {
    const hits = []; for (let n = n0; n <= n1; n += step) for (let x = x0; x <= x1; x += step) { const r = evaluate(x, n, opts); if (r && r.eligible) hits.push(r); } return hits;
  }
  /** Largest eligible radius centred exactly at (x, n) (0.5 m steps up to rMax). */
  function largestAt(x, n, opts, rMax = 30) { let best = 0, last = null; for (let r = 1; r <= rMax; r += 0.5) { const e = evaluate(x, n, { ...opts, radius: r }); if (e && e.eligible) { best = r; last = e; } else if (best > 0) break; } return { radius: best, detail: last }; }
  return { evaluate, scan, largestAt };
}
