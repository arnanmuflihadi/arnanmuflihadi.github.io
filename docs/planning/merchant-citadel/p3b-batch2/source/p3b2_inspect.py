"""Inspect third-party GLB/glTF files without executing anything: triangles, skins/bones, animation clips (name, duration), bounds, materials, textures, file size.
python3 p3b2_inspect.py <out.json> <file-or-dir> ...   (data only; files are never imported into anything that runs code)"""
import sys, os, json, struct, glob
import numpy as np
CT = {5120: np.int8, 5121: np.uint8, 5122: np.int16, 5123: np.uint16, 5125: np.uint32, 5126: np.float32}; NC = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}

def load(path):
    if path.endswith(".glb"):
        d = open(path, "rb").read(); jl = struct.unpack("<I", d[12:16])[0]; j = json.loads(d[20:20 + jl]); off = 20 + jl + 8; return j, d[off:]
    j = json.load(open(path)); b = b""
    if j.get("buffers") and "uri" in j["buffers"][0] and not j["buffers"][0]["uri"].startswith("data:"):
        b = open(os.path.join(os.path.dirname(path), j["buffers"][0]["uri"]), "rb").read()
    return j, b

def acc(j, bin_, i):
    a = j["accessors"][i]; bv = j["bufferViews"][a["bufferView"]]; n = a["count"] * NC[a["type"]]
    return np.frombuffer(bin_, CT[a["componentType"]], n, bv.get("byteOffset", 0) + a.get("byteOffset", 0)).reshape(a["count"], NC[a["type"]])

def inspect(path):
    j, b = load(path); tris = 0; mn = np.full(3, 1e9); mx = np.full(3, -1e9)
    for m in j.get("meshes", []):
        for p in m["primitives"]:
            if "indices" in p: tris += j["accessors"][p["indices"]]["count"] // 3
            elif "POSITION" in p["attributes"]: tris += j["accessors"][p["attributes"]["POSITION"]]["count"] // 3
            a = j["accessors"][p["attributes"]["POSITION"]]
            if "min" in a: mn = np.minimum(mn, a["min"]); mx = np.maximum(mx, a["max"])
    anims = []
    for an in j.get("animations", []):
        dur = 0.0
        for s in an["samplers"]:
            t = j["accessors"][s["input"]]; dur = max(dur, t.get("max", [0])[0])
        anims.append(dict(name=an.get("name"), seconds=round(dur, 3), channels=len(an["channels"])))
    skins = [len(s["joints"]) for s in j.get("skins", [])]
    jn = [j["nodes"][k].get("name") for s in j.get("skins", []) for k in s["joints"]][:60]
    return dict(file=os.path.basename(path), bytes=os.path.getsize(path), triangles=tris, bounds_min=[round(float(v), 3) for v in mn], bounds_size=[round(float(v), 3) for v in (mx - mn)], meshes=len(j.get("meshes", [])), materials=len(j.get("materials", [])), textures=len(j.get("textures", [])), images=len(j.get("images", [])),
                skins=skins, bones=sum(skins), animations=anims, bone_names=jn, generator=j.get("asset", {}).get("generator"), extensions=j.get("extensionsUsed", []))

out = sys.argv[1]; files = []
for a in sys.argv[2:]:
    files += sorted(glob.glob(os.path.join(a, "*.glb")) + glob.glob(os.path.join(a, "*.gltf"))) if os.path.isdir(a) else [a]
res = [inspect(f) for f in files]; json.dump(res, open(out, "w"), indent=1); print(len(res), "files,", sum(r["triangles"] for r in res), "triangles")
