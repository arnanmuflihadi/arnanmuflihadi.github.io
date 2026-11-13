#!/usr/bin/env python3
"""Structural inspection of the production GLB (no third-party validator needed): header, references, accessor ranges, attribute completeness, transforms, names, finite values.
Usage: python3 p2a_glb_inspect.py <kit.glb> <out.json>"""
import json, struct, sys
import numpy as np

path, out = sys.argv[1:3]
b = open(path, "rb").read()
magic, ver, length = struct.unpack("<4sII", b[:12]); jl, jt = struct.unpack("<I4s", b[12:20]); j = json.loads(b[20:20 + jl]); off = 20 + jl
bl, bt = struct.unpack("<I4s", b[off:off + 8]); binchunk = b[off + 8:off + 8 + bl]
CT = {5120: np.int8, 5121: np.uint8, 5122: np.int16, 5123: np.uint16, 5125: np.uint32, 5126: np.float32}; NC = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}
issues = []; checks = {}


def read(i):
    a = j["accessors"][i]; bv = j["bufferViews"][a["bufferView"]]; n = NC[a["type"]]
    dt = np.dtype(CT[a["componentType"]]); stride = bv.get("byteStride") or dt.itemsize * n
    start = bv.get("byteOffset", 0) + a.get("byteOffset", 0)
    if stride == dt.itemsize * n:
        return np.frombuffer(binchunk, dtype=dt, count=a["count"] * n, offset=start).reshape(a["count"], n)
    return np.stack([np.frombuffer(binchunk, dtype=dt, count=n, offset=start + k * stride) for k in range(a["count"])])


checks["header"] = {"magic": magic.decode(), "version": ver, "declared_length": length, "actual_length": len(b), "json_chunk": jt.decode(), "bin_chunk": bt.decode(), "ok": magic == b"glTF" and ver == 2 and length == len(b)}
checks["extensions_used"] = j.get("extensionsUsed", []); checks["extensions_required"] = j.get("extensionsRequired", [])
checks["counts"] = {k: len(j.get(k, [])) for k in ("scenes", "nodes", "meshes", "materials", "textures", "images", "samplers", "accessors", "bufferViews", "buffers")}
names = [n.get("name") for n in j["nodes"]]
checks["unique_node_names"] = len(names) == len(set(names))
nonid = [n["name"] for n in j["nodes"] if any(k in n for k in ("translation", "rotation", "scale", "matrix"))]
checks["nodes_with_transforms"] = nonid
tri = vert = prims = 0; aoprims = colprims = 0; missing = []; badrange = []; nonfinite = []; bbox_bad = []
tex_mats = {i for i, m in enumerate(j["materials"]) if any("Texture" in k for k in json.dumps(m))}
node_report = {}
for n in j["nodes"]:
    if "mesh" not in n:
        continue
    m = j["meshes"][n["mesh"]]; t = v = 0
    for p in m["primitives"]:
        prims += 1; at = p["attributes"]; pos = read(at["POSITION"]); vc = len(pos); v += vc; vert += vc
        if "indices" in p:
            idx = read(p["indices"]).ravel(); t += len(idx) // 3
            if idx.max() >= vc:
                badrange.append(n["name"])
        else:
            t += vc // 3
        if not np.isfinite(pos).all():
            nonfinite.append(n["name"])
        a = j["accessors"][at["POSITION"]]
        if "min" in a and (np.abs(pos.min(0) - np.array(a["min"])) > 1e-4).any():
            bbox_bad.append(n["name"])
        if "NORMAL" not in at:
            missing.append((n["name"], "NORMAL"))
        if p.get("material") in tex_mats and "TEXCOORD_0" not in at:
            missing.append((n["name"], "TEXCOORD_0 for a textured material"))
        if "_AO" in at:
            aoprims += 1; ao = read(at["_AO"]).ravel()
            if len(ao) != vc or ao.min() < 0 or ao.max() > 1.0001:
                issues.append(f"_AO out of range or wrong count in {n['name']}")
        if "COLOR_0" in at:
            colprims += 1
        if "material" not in p:
            missing.append((n["name"], "material"))
    tri += t; node_report[n["name"]] = {"triangles": t, "vertices": v, "primitives": len(m["primitives"])}
checks["geometry"] = {"nodes_with_mesh": len(node_report), "primitives": prims, "triangles": tri, "vertices": vert, "primitives_with_AO": aoprims, "primitives_with_COLOR_0": colprims}
checks["problems"] = {"missing_attributes": missing, "index_out_of_range": badrange, "non_finite_positions": nonfinite, "accessor_bbox_mismatch": bbox_bad}
mats = j["materials"]; checks["materials"] = {"count": len(mats), "distinct_names": len({m.get("name") for m in mats}), "double_sided": sum(1 for m in mats if m.get("doubleSided")), "with_base_texture": sum(1 for m in mats if "baseColorTexture" in m.get("pbrMetallicRoughness", {})),
                                              "alpha_mask": sum(1 for m in mats if m.get("alphaMode") == "MASK"), "alpha_blend": sum(1 for m in mats if m.get("alphaMode") == "BLEND")}
bad_ref = [i for i, t in enumerate(j.get("textures", [])) if t.get("source", -1) >= len(j.get("images", []))]
checks["texture_references_valid"] = not bad_ref
ims = j.get("images", []); sizes = [j["bufferViews"][i["bufferView"]]["byteLength"] for i in ims if "bufferView" in i]
checks["images"] = {"count": len(ims), "embedded_bytes": sum(sizes), "mime": sorted({i.get("mimeType") for i in ims})}
bbs = [j["accessors"][p["attributes"]["POSITION"]] for m in j["meshes"] for p in m["primitives"]]
mn = np.min([a["min"] for a in bbs], axis=0); mx = np.max([a["max"] for a in bbs], axis=0); checks["kit_bounds_m_gltf_axes"] = {"min": [round(float(x), 3) for x in mn], "max": [round(float(x), 3) for x in mx]}
checks["ok"] = checks["header"]["ok"] and checks["unique_node_names"] and not nonid and not any(checks["problems"].values()) and not issues and not bad_ref
json.dump({"file": path, "bytes": len(b), "checks": checks, "issues": issues, "nodes": node_report}, open(out, "w"), indent=1)
print(json.dumps({k: checks[k] for k in ("header", "counts", "geometry", "problems", "materials", "texture_references_valid", "images", "ok")}, indent=1))
