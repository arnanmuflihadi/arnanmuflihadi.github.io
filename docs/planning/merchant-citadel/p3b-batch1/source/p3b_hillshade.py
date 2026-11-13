"""Hillshade + contour plan of the island model, with the built town footprints (iteration aid and evidence). python3 p3b_hillshade.py <scene.json> <out.png>"""
import sys, json, time
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import p3b_model as M

scene, out = sys.argv[1], sys.argv[2]
t = time.time(); spec = M.grid_spec(); X, N, h = M.sample_grid(spec); print("grid", spec["nx"], spec["nn"], "in", round(time.time() - t, 1), "s")
hh = np.where(np.isnan(h), np.nan, h)
ls = matplotlib.colors.LightSource(azdeg=225, altdeg=40)
fig, ax = plt.subplots(figsize=(13, 14), dpi=100)
sh = ls.shade(np.nan_to_num(hh, nan=-12.0), cmap=plt.cm.terrain, vert_exag=3.0, blend_mode="overlay", vmin=-9, vmax=24)
ax.imshow(sh, origin="lower", extent=[X.min() - M.CELL / 2, X.max() + M.CELL / 2, N.min() - M.CELL / 2, N.max() + M.CELL / 2])
ax.contour(X, N, np.nan_to_num(hh, nan=-99), levels=np.arange(-9, 25, 1.0), colors="k", linewidths=0.2, alpha=0.5)
for r in json.load(open(scene))["rects"]:
    ax.add_patch(plt.Rectangle((r[0], r[2]), r[1] - r[0], r[3] - r[2], fill=False, ec="red", lw=1))
for nm, cx, cn, r, z in M.CLEARINGS:
    ax.add_patch(plt.Circle((cx, cn), r, fill=False, ec="cyan", lw=1)); ax.text(cx, cn, nm, color="white", fontsize=7, ha="center")
for nm, kind, w, pts in M.PATHS:
    p = np.array([q[:2] for q in pts]); ax.plot(p[:, 0], p[:, 1], "y-", lw=1)
w = np.array(M.WATER); ax.plot(w[:, 0], w[:, 1], "c-", lw=2)
ax.set_aspect("equal"); ax.set_title("P3-B island model: height (-9..24 m), 1 m contours"); plt.savefig(out, bbox_inches="tight"); print("wrote", out)
print("heights min/max", np.nanmin(hh), np.nanmax(hh), "extents", json.dumps(M.extents()))
