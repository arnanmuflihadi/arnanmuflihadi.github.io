"""Merchant Citadel P3-B batch 1: export the walkable terrain contract for the browser from p3b_model.

  python3 p3b_export_runtime.py <runtime_dir> [<top-mesh.npz>] [<evidence_dir>]

Writes island-terrain.json (grid spec, bounds, constants), island-terrain.bin (int16 centimetres, -32768 = no support) and island-mask.bin (uint8:
bit0 walkable, bit1 comfortable/safe ground). With the top mesh dump it also measures the visible mesh against the physical bilinear surface.
"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p3b_model as M

out = sys.argv[1]; os.makedirs(out, exist_ok=True)
spec = M.grid_spec(); X, N, h = M.sample_grid(spec)
edm = M.edge_distance(M.MAIN, X, N); eds = M.edge_distance(M.STACK, X, N); br = M.bridge_height(X, N)
walk, comf, slope = M.masks(h, edm, eds, br)
q = np.where(np.isnan(h), -32768, np.round(h * 100)).astype(np.int16)
assert q[~np.isnan(h)].min() > -32768 and q.max() < 32767
# bit2: the town's own 0.2 m grid authored a surface here (paving, steps, terrace, podium): walkable by the town's rules, whatever the terrain beneath does
tm = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../../merchant-citadel-p2a/data/heightfield.json")))
tb = np.fromfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../../merchant-citadel-p2a/data/heightfield.bin"), np.uint8).reshape(tm["nn"], tm["nx"])
ti = np.floor((X - tm["x0"]) / tm["cell"]).astype(int); tj = np.floor((N - tm["n0"]) / tm["cell"]).astype(int)
tin = (ti >= 0) & (tj >= 0) & (ti < tm["nx"]) & (tj < tm["nn"]); town = np.zeros(X.shape, bool); town[tin] = tb[tj[tin], ti[tin]] > 0
mask = (walk.astype(np.uint8) | (comf.astype(np.uint8) << 1) | ((town & ~np.isnan(h)).astype(np.uint8) << 2)).astype(np.uint8)
ext = M.extents()
maxabs = max(abs(ext["all"]["x"][0]), abs(ext["all"]["x"][1]), abs(ext["all"]["n"][0]), abs(ext["all"]["n"][1]))
meta = dict(version="p3b-batch1", frame="x east, n north (three z = -n), metres", x0=spec["x0"], n0=spec["n0"], cell=spec["cell"], nx=spec["nx"], nn=spec["nn"], unit_m=0.01, dtype="int16 little-endian row-major (n rows, x columns)",
            nosup_sentinel=-32768, nosup_height_m=M.NOSUP, interpolation="bilinear on the 0.5 m grid; missing corners replaced by the mean of the valid ones; heights over the town paving come from the 0.2 m town grid (max of both)",
            masks="island-mask.bin uint8, nearest cell: bit2 = the town grid authored a surface (walkable by the town rules); bit0 walkable (supported, >= %.1f m inside the rim, slope <= %.2f); bit1 comfortable (slope <= %.2f, >= 2.5 m inside the rim)" % (M.RIM_MARGIN, M.MAX_SLOPE, M.COMFORT_SLOPE),
            max_slope=M.MAX_SLOPE, comfort_slope=M.COMFORT_SLOPE, rim_margin=M.RIM_MARGIN, extents=ext, derived_bounds=dict(max_abs_extent_m=maxabs, controller_bounds_m=float(np.ceil(maxabs + 10)), note="the controller's bounds are symmetric about the origin: ceil(max |x|, |z| over all geometry) + 10 m"),
            grid_x=[spec["x0"], spec["x0"] + spec["cell"] * (spec["nx"] - 1)], grid_n=[spec["n0"], spec["n0"] + spec["cell"] * (spec["nn"] - 1)], height_range_m=[float(np.nanmin(h)), float(np.nanmax(h))],
            minY_recommended=-30.0, maxY_recommended=80.0, bridge=dict(zip(("name", "width", "a", "b", "za", "zb"), M.BRIDGE)))
json.dump(meta, open(os.path.join(out, "island-terrain.json"), "w"), indent=1)
q.tofile(os.path.join(out, "island-terrain.bin")); mask.tofile(os.path.join(out, "island-mask.bin"))
print("grid", spec["nx"], "x", spec["nn"], "bytes", q.nbytes, "+", mask.nbytes, "bounds", meta["derived_bounds"])
stats = dict(cells_supported=int((~np.isnan(h)).sum()), cells_walkable=int(walk.sum()), cells_comfortable=int(comf.sum()), area_supported_m2=float((~np.isnan(h)).sum() * M.CELL ** 2), area_walkable_m2=float(walk.sum() * M.CELL ** 2), area_comfortable_m2=float(comf.sum() * M.CELL ** 2))
# mesh vs physics
if len(sys.argv) > 2 and os.path.exists(sys.argv[2]):
    from matplotlib.tri import Triangulation
    d = np.load(sys.argv[2]); V, F = d["V"], d["F"]; tri = Triangulation(V[:, 0], V[:, 1], F); tf = tri.get_trifinder()
    rng = np.random.default_rng(5); px = rng.uniform(spec["x0"], spec["x0"] + 200, 60000); pn = rng.uniform(spec["n0"], spec["n0"] + 230, 60000)
    ok = walk[np.clip(((pn - spec["n0"]) / spec["cell"]).round().astype(int), 0, spec["nn"] - 1), np.clip(((px - spec["x0"]) / spec["cell"]).round().astype(int), 0, spec["nx"] - 1)]
    px, pn = px[ok], pn[ok]; idx = tf(px, pn); good = idx >= 0; px, pn, idx = px[good], pn[good], idx[good]
    A, B, C = V[F[idx, 0]], V[F[idx, 1]], V[F[idx, 2]]
    w0 = ((B[:, 1] - C[:, 1]) * (px - C[:, 0]) + (C[:, 0] - B[:, 0]) * (pn - C[:, 1])) / ((B[:, 1] - C[:, 1]) * (A[:, 0] - C[:, 0]) + (C[:, 0] - B[:, 0]) * (A[:, 1] - C[:, 1])); w1 = ((C[:, 1] - A[:, 1]) * (px - C[:, 0]) + (A[:, 0] - C[:, 0]) * (pn - C[:, 1])) / ((B[:, 1] - C[:, 1]) * (A[:, 0] - C[:, 0]) + (C[:, 0] - B[:, 0]) * (A[:, 1] - C[:, 1])); w2 = 1 - w0 - w1
    mesh_z = w0 * A[:, 2] + w1 * B[:, 2] + w2 * C[:, 2]
    fx = (px - spec["x0"]) / spec["cell"]; fy = (pn - spec["n0"]) / spec["cell"]; i = np.floor(fx).astype(int); j = np.floor(fy).astype(int); tx = fx - i; ty = fy - j
    Q = np.where(q == -32768, np.nan, q / 100.0)
    c00, c10, c01, c11 = Q[j, i], Q[j, i + 1], Q[j + 1, i], Q[j + 1, i + 1]
    phys = c00 * (1 - tx) * (1 - ty) + c10 * tx * (1 - ty) + c01 * (1 - tx) * ty + c11 * tx * ty
    e = np.abs(mesh_z - phys); e = e[~np.isnan(e)]
    stats["mesh_vs_physics"] = dict(samples=int(len(e)), mean_m=float(e.mean()), p50_m=float(np.percentile(e, 50)), p95_m=float(np.percentile(e, 95)), p99_m=float(np.percentile(e, 99)), max_m=float(e.max()), share_over_5cm=float((e > 0.05).mean()), share_over_10cm=float((e > 0.10).mean()), share_over_20cm=float((e > 0.20).mean()),
                                    note="visible top mesh (constrained Delaunay, adaptive 2/1/0.5 m) against the bilinear 0.5 m physical surface, random walkable points")
    print(json.dumps(stats["mesh_vs_physics"]))
if len(sys.argv) > 3:
    os.makedirs(sys.argv[3], exist_ok=True); json.dump(stats, open(os.path.join(sys.argv[3], "terrain-export-stats.json"), "w"), indent=1)
