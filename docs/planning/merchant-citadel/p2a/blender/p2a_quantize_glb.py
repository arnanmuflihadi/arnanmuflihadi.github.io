#!/usr/bin/env python3
"""Compression experiment (P2-B batch 4): rewrite the kit GLB with quantised vertex attributes (KHR_mesh_quantization, supported natively by the vendored GLTFLoader).

Per mesh (one node per kit asset, no parent transforms):
  POSITION   float32 x3  ->  int16 x3 (not normalised), stride 8; the node gets scale 2^-k, k chosen per mesh so that max|p| * 2^k <= 32767 (k <= 13: 0.12 mm steps; k = 8 for the world-placed dressing, 3.9 mm)
  NORMAL     float32 x3  ->  int8 x3 normalised, stride 4
  TEXCOORD_0 float32 x2  ->  uint16 x2 normalised, stride 4, only if every value of the primitive lies in [0, 1] (otherwise left as float32; the count is reported)
  COLOR_0    float32 x3  ->  uint8 x3 normalised, stride 4
  _AO        float32     ->  unchanged (a one-byte scalar would still need a 4-byte stride)
  indices, images, materials, textures: unchanged
Usage: python3 p2a_quantize_glb.py <in.glb> <out.glb> [report.json]        (needs numpy)
"""
import json, struct, sys
import numpy as np

src, dst = sys.argv[1], sys.argv[2]; rep_path = sys.argv[3] if len(sys.argv) > 3 else None
b = open(src, "rb").read(); jl, _ = struct.unpack("<II", b[12:20]); js = json.loads(b[20:20 + jl]); bl = struct.unpack("<I", b[20 + jl:24 + jl])[0]; bin_ = b[28 + jl:28 + jl + bl]
acc, bvs = js["accessors"], js["bufferViews"]
CT = {5120: np.int8, 5121: np.uint8, 5122: np.int16, 5123: np.uint16, 5125: np.uint32, 5126: np.float32}; NC = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}


def read(ai):
    a = acc[ai]; v = bvs[a["bufferView"]]; n = NC[a["type"]]; dt = np.dtype(CT[a["componentType"]]); off = v.get("byteOffset", 0) + a.get("byteOffset", 0); stride = v.get("byteStride") or n * dt.itemsize
    if stride == n * dt.itemsize:
        return np.frombuffer(bin_, dtype=dt, count=a["count"] * n, offset=off).reshape(a["count"], n)
    raw = np.frombuffer(bin_, dtype=np.uint8, count=stride * a["count"], offset=off).reshape(a["count"], stride)[:, :n * dt.itemsize]
    return np.ascontiguousarray(raw).view(dt).reshape(a["count"], n)


out = bytearray(); new_bv, new_acc = [], []; report = {"meshes": {}, "float_uv_primitives": 0, "primitives": 0}


def put(data, target=None, stride=None):
    while len(out) % 4: out.append(0)
    v = {"buffer": 0, "byteOffset": len(out), "byteLength": len(data)}
    if target: v["target"] = target
    if stride: v["byteStride"] = stride
    out.extend(data); new_bv.append(v); return len(new_bv) - 1


def add_acc(bv, ct, count, typ, normalized=False, mn=None, mx=None):
    a = {"bufferView": bv, "componentType": ct, "count": count, "type": typ}
    if normalized: a["normalized"] = True
    if mn is not None: a["min"], a["max"] = mn, mx
    new_acc.append(a); return len(new_acc) - 1


def pad_rows(arr, width):                                         # rows of `arr` (n, k) -> (n, width) bytes with zero padding, flattened
    n = arr.shape[0]; raw = np.zeros((n, width), np.uint8); flat = arr.reshape(n, -1).view(np.uint8); raw[:, :flat.shape[1]] = flat; return raw.tobytes()


idx_map, img_views = {}, {i["bufferView"] for i in js.get("images", [])}
node_of_mesh = {n["mesh"]: n for n in js["nodes"] if "mesh" in n}
for mi, mesh in enumerate(js["meshes"]):
    pmax = max(float(np.abs(read(p["attributes"]["POSITION"])).max()) for p in mesh["primitives"]); k = min(13, int(np.floor(np.log2(32767.0 / max(pmax, 1e-6)))))
    node = node_of_mesh[mi]; assert "scale" not in node and "matrix" not in node, "kit nodes are expected to carry no transform"; node["scale"] = [2.0 ** -k] * 3; err = 0.0
    for p in mesh["primitives"]:
        report["primitives"] += 1; at = p["attributes"]; na = {}
        pos = read(at["POSITION"]); q = np.rint(pos * (2.0 ** k)).astype(np.int16); err = max(err, float(np.abs(q.astype(np.float64) / (2.0 ** k) - pos).max()))
        na["POSITION"] = add_acc(put(pad_rows(q, 8), 34962, 8), 5122, len(q), "VEC3", False, [int(x) for x in q.min(0)], [int(x) for x in q.max(0)])
        nr = read(at["NORMAL"]); qn = np.clip(np.rint(nr * 127.0), -127, 127).astype(np.int8); na["NORMAL"] = add_acc(put(pad_rows(qn, 4), 34962, 4), 5120, len(qn), "VEC3", True)
        if "TEXCOORD_0" in at:
            uv = read(at["TEXCOORD_0"])
            if uv.min() >= 0.0 and uv.max() <= 1.0:
                qu = np.rint(uv * 65535.0).astype(np.uint16); na["TEXCOORD_0"] = add_acc(put(qu.tobytes(), 34962, 4), 5123, len(qu), "VEC2", True)
            else:
                report["float_uv_primitives"] += 1; na["TEXCOORD_0"] = add_acc(put(uv.astype(np.float32).tobytes(), 34962, 8), 5126, len(uv), "VEC2")
        if "COLOR_0" in at:
            c = read(at["COLOR_0"]); qc = np.clip(np.rint(c * 255.0), 0, 255).astype(np.uint8); na["COLOR_0"] = add_acc(put(pad_rows(qc, 4), 34962, 4), 5121, len(qc), "VEC3", True)
        for key in at:
            if key not in na:                                                  # _AO and anything else: copied as it was
                a = acc[at[key]]; arr = read(at[key]); na[key] = add_acc(put(np.ascontiguousarray(arr).tobytes(), 34962, arr.shape[1] * arr.itemsize if arr.shape[1] > 1 else None), a["componentType"], a["count"], a["type"], a.get("normalized", False))
        p["attributes"] = na
        if p["indices"] not in idx_map:
            ia = acc[p["indices"]]; arr = read(p["indices"]); idx_map[p["indices"]] = add_acc(put(np.ascontiguousarray(arr).tobytes(), 34963), ia["componentType"], ia["count"], "SCALAR")
        p["indices"] = idx_map[p["indices"]]
    report["meshes"][node.get("name", str(mi))] = {"k": k, "position_step_mm": round(1000.0 / (2 ** k), 3), "max_position_error_mm": round(err * 1000, 4)}
img_new = {}
for k, v in enumerate(bvs):
    if k in img_views:
        while len(out) % 4: out.append(0)
        img_new[k] = len(new_bv); new_bv.append({"buffer": 0, "byteOffset": len(out), "byteLength": v["byteLength"]}); out.extend(bin_[v.get("byteOffset", 0):v.get("byteOffset", 0) + v["byteLength"]])
for im in js.get("images", []):
    im["bufferView"] = img_new[im["bufferView"]]
js["accessors"], js["bufferViews"] = new_acc, new_bv
for key in ("extensionsUsed", "extensionsRequired"):
    js.setdefault(key, [])
    if "KHR_mesh_quantization" not in js[key]: js[key].append("KHR_mesh_quantization")
while len(out) % 4: out.append(0)
js["buffers"][0]["byteLength"] = len(out)
jb = json.dumps(js, separators=(",", ":")).encode()
while len(jb) % 4: jb += b" "
glb = struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(jb) + 8 + len(out)) + struct.pack("<II", len(jb), 0x4E4F534A) + jb + struct.pack("<II", len(out), 0x004E4942) + bytes(out)
open(dst, "wb").write(glb)
report.update({"in_bytes": len(b), "out_bytes": len(glb), "saved_pct": round(100.0 * (1 - len(glb) / len(b)), 2), "max_position_error_mm": max(m["max_position_error_mm"] for m in report["meshes"].values())})
print({k: v for k, v in report.items() if k != "meshes"})
if rep_path: json.dump(report, open(rep_path, "w"), indent=1)
