#!/usr/bin/env python3
"""Batch 5: derive the town-to-terrain interface from the BUILT town (scene.json, kit-report.json, heightfield), not from the P1.4 planning envelope.
Usage: p2e_terrain_interface.py <scene.json> <kit-report.json> <heightfield.json> <heightfield.bin> <out.json>"""
import json, math, sys
import numpy as np
sc = json.load(open(sys.argv[1])); kit = json.load(open(sys.argv[2])); hfj = json.load(open(sys.argv[3])); hfb = np.fromfile(sys.argv[4], dtype=np.uint8)
nodes = kit["nodes"]; out = {"revision": "P2-B batch 5", "source": "scene.json instances, kit-report bounding boxes, collision proxies, heightfield", "buildings": []}
for i in sc["instances"]:
    n = i["node"]
    if n.startswith(("SIGN_", "TILE_")) or n in ("CROSS", "TERRACE", "PODIUM", "ARCH") or n.startswith("A01_") and i["id"] != "B01_main":
        continue
    kn = nodes.get(n)
    if not kn: continue
    b = kn["bbox_gltf"]; a = math.radians(i["ry"]); c, s = math.cos(a), math.sin(a); xs, zs = [], []
    for x in (b[0], b[3]):
        for z in (b[2], b[5]):
            xs.append(i["x"] + x * c + z * s); zs.append(i["z"] - x * s + z * c)
    walls = [o for o in sc["collision"] if o["src"] == i["id"].split("_")[0] and o["group"] == "wall"]
    fp = None
    if walls:
        fp = [round(min(o["x"] - o["w"] / 2 for o in walls), 2), round(max(o["x"] + o["w"] / 2 for o in walls), 2), round(min(-o["z"] - o["d"] / 2 for o in walls), 2), round(max(-o["z"] + o["d"] / 2 for o in walls), 2)]
    out["buildings"].append({"id": i["id"], "node": n, "label": i["label"], "plan_x": i["x"], "plan_n": round(-i["z"], 3), "rotation_deg": i["ry"], "ground_elevation_m": i["y"], "footprint_walls_x_n": fp,
                             "envelope_x": [round(min(xs), 2), round(max(xs), 2)], "envelope_n": [round(-max(zs), 2), round(-min(zs), 2)], "top_y_above_ground_m": round(b[4], 2), "district": i.get("district")})
# ground levels from the heightfield
meta = hfj; W, H = meta["nx"], meta["nn"]
out["heightfield_meta"] = {k: meta[k] for k in meta if k not in ("levels",)}
lv = {}
if W and H and hfb.size >= W * H:
    g = hfb[:W * H].reshape(H, W); cell = meta["cell"]
    for cm in np.unique(g):
        ys, xs_ = np.nonzero(g == cm); lv[int(cm)] = {"cells": int(ys.size), "area_m2": round(ys.size * cell ** 2, 1), "x": [round(meta["x0"] + xs_.min() * cell, 1), round(meta["x0"] + (xs_.max() + 1) * cell, 1)], "n": [round(meta["n0"] + ys.min() * cell, 1), round(meta["n0"] + (ys.max() + 1) * cell, 1)]}
out["ground_levels_cm"] = lv
tiles = sc["tiles"]; allt = [t for v in tiles.values() for t in v]
out["paved_tiles"] = {k: len(v) for k, v in tiles.items()}
out["paved_extent_x"] = [min(t[0] for t in allt) - 1, max(t[0] for t in allt) + 1]; out["paved_extent_n"] = [min(-t[1] for t in allt) - 1, max(-t[1] for t in allt) + 1]
bx = [x for b in out["buildings"] for x in b["envelope_x"]]; bn = [n for b in out["buildings"] for n in b["envelope_n"]]
out["town_extent"] = {"x": [round(min(bx + out["paved_extent_x"]), 1), round(max(bx + out["paved_extent_x"]), 1)], "n": [round(min(bn + out["paved_extent_n"]), 1), round(max(bn + out["paved_extent_n"]), 1)]}
out["nodes_outside_buildings"] = {k: v[:3] for k, v in sc["nodes"].items() if k in ("N20", "N16", "N17", "N33", "N51", "N54")}
json.dump(out, open(sys.argv[5], "w"), indent=1); print(len(out["buildings"]), "buildings", out["town_extent"], list(lv)[:8])
