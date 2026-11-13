#!/usr/bin/env python3
"""Batch 4: refresh data/expected-bounds.json (every kit node's bounding box as built in Blender, from kit-report.json) and add placement envelopes for B13, E04 and E05
(the Blender-built node's box transformed by the instance transform; exact for rotations that are multiples of 90 degrees). Usage: p2d_expected.py <kit-report.json> <scene.json> <data dir>"""
import json, math, os, sys
kit = json.load(open(sys.argv[1])); sc = json.load(open(sys.argv[2])); data = sys.argv[3]
bounds = {k: {"bbox_gltf": v["bbox_gltf"]} for k, v in kit["nodes"].items()}
json.dump(bounds, open(os.path.join(data, "expected-bounds.json"), "w"), indent=0)
env_path = os.path.join(data, "expected-envelopes.json"); env = json.load(open(env_path)); n_added = []
for bid, node in (("B13", "A07w"), ("E04", "A05c"), ("E05", "A03cT"), ("B15", "A11a"), ("B16", "A11c")):
    i = next(x for x in sc["instances"] if x["id"] == bid); b = bounds[node]["bbox_gltf"]; a = math.radians(i["ry"]); c, s = math.cos(a), math.sin(a)
    xs, zs = [], []
    for x in (b[0], b[3]):
        for z in (b[2], b[5]):
            xs.append(i["x"] + x * c + z * s); zs.append(i["z"] - x * s + z * c)                    # three.js rotation about y by +ry: x' = x cos + z sin, z' = -x sin + z cos
    env[bid] = {"full_x": [round(min(xs), 3), round(max(xs), 3)], "full_n": [round(-max(zs), 3), round(-min(zs), 3)],
                "note": "batch 4: expected = the Blender-built kit node's bounding box (kit-report) transformed by the instance (exact, rotation is a multiple of 90 degrees); the P1.4 envelope of this building was not recomputed (placement may differ by the documented adjustments in 01)"}
    n_added.append(bid)
json.dump(env, open(env_path, "w"), indent=0); print("bounds", len(bounds), "envelopes added", n_added)
