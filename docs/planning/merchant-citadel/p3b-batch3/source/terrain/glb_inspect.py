"""Print per-mesh attributes and colour statistics of a GLB (used to verify the island export). python3 glb_inspect.py file.glb"""
import sys, json, struct
import numpy as np
d = open(sys.argv[1], "rb").read(); jl, _ = struct.unpack("<II", d[12:20]); j = json.loads(d[20:20 + jl]); off = 20 + jl + 8; BIN = d[off:]
CT = {5120: np.int8, 5121: np.uint8, 5122: np.int16, 5123: np.uint16, 5125: np.uint32, 5126: np.float32}; NC = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}
def acc(i):
    a = j["accessors"][i]; bv = j["bufferViews"][a["bufferView"]]; n = a["count"] * NC[a["type"]]
    arr = np.frombuffer(BIN, CT[a["componentType"]], n, bv.get("byteOffset", 0) + a.get("byteOffset", 0)).reshape(a["count"], NC[a["type"]])
    if a.get("normalized"): arr = arr / np.iinfo(CT[a["componentType"]]).max
    return arr
tot = 0
for m in j["meshes"]:
    for p in m["primitives"]:
        at = p["attributes"]; n = j["accessors"][p["indices"]]["count"] // 3; tot += n; line = "%-22s tris %6d attrs %s" % (m.get("name"), n, ",".join(at))
        if "COLOR_0" in at:
            c = acc(at["COLOR_0"])[:, :3]; line += "  COLOR_0 mean %s min %.3f max %.3f" % (np.round(c.mean(0), 3), c.min(), c.max())
        print(line)
print("total tris", tot, "materials", [mm["name"] for mm in j["materials"]][:12])
