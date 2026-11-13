"""P3-B batch 3 WP1: ground map for the terrain shader.

  python3 p3b3_groundmap.py <out_dir>

Writes groundmap-r.bin and groundmap-g.bin (uint8, one channel each, row-major, n rows x x columns; the vendored three build exports RedFormat only) and groundmap.json (grid spec). 0.3 m cells over the island:
  R = signed distance to the nearest walking path edge (path_distance, m), clamped to [-1, 2] and mapped to 0..255 (< 0 inside the path); 255 on the quay (no earth paths there)
  G = tea planting-row soil weight (0..255) inside the tea benches, 0 elsewhere (same row formula as top_colours in batch 1, soft gaussian rows)
The browser shader turns R into a crisp path edge and G into soil strips between grass, replacing the per-vertex baked colours that smeared at the mesh resolution.
"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/terrain")
import p3b_model as M

out = sys.argv[1]; os.makedirs(out, exist_ok=True)
CELL = 0.3; x0, n0, x1, n1 = -90.0, -89.0, 131.0, 145.0
nx, nn = int(round((x1 - x0) / CELL)) + 1, int(round((n1 - n0) / CELL)) + 1
xs = x0 + CELL * np.arange(nx); ns = n0 + CELL * np.arange(nn); X, N = np.meshgrid(xs, ns)
d = M.path_distance(X.ravel(), N.ravel()).reshape(X.shape)
d = np.where(N < -26.5, 3.0, d)                                           # quay and ramp end: no earth path
R = np.round((np.clip(d, -1.0, 2.0) + 1.0) / 3.0 * 255).astype(np.uint8)
Z = M.terrain(X.ravel(), N.ravel()).reshape(X.shape)
dl = np.hypot(X - M.LOOKOUT[0], N - M.LOOKOUT[1]); tea = (X > 47) & (X < 99) & (N < 90) & (N > 4) & (Z < -0.6)
dw = dl + 2.4 * M.field_noise(X.ravel(), N.ravel(), 91, (38, 21, 12), (1, 0.6, 0.35)).reshape(X.shape); u = (dw - M.TEA_D0) / M.TEA_W; f = u - np.floor(u)
wr = np.maximum(np.exp(-((f - 0.22) / 0.10) ** 2), np.exp(-((f - 0.58) / 0.10) ** 2))
G = np.round(np.where(tea & (d > 0.3), wr, 0) * 255).astype(np.uint8)       # no soil strips under paths
R.tofile(os.path.join(out, "groundmap-r.bin")); G.tofile(os.path.join(out, "groundmap-g.bin")); buf = np.stack([R, G], -1)
json.dump(dict(version="p3b-batch3", cell=CELL, x0=x0, n0=n0, nx=nx, nn=nn, channels="RG uint8; R=(clamp(path_edge_distance_m,-1,2)+1)/3, G=tea soil row weight", bytes=int(buf.nbytes)), open(os.path.join(out, "groundmap.json"), "w"), indent=1)
print("groundmap", nx, "x", nn, buf.nbytes, "bytes; path cells", int((d < 0).sum()), "tea soil cells", int((G > 40).sum()))
