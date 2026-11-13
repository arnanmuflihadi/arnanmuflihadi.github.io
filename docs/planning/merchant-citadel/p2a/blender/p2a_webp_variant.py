#!/usr/bin/env python3
"""Compression experiment (P2-B batch 3): rewrite the kit GLB with every embedded JPEG/PNG re-encoded as WebP (EXT_texture_webp, supported natively by the vendored GLTFLoader).
Geometry is untouched. Usage: python3 p2a_webp_variant.py <in.glb> <out.glb> [quality]   (needs Pillow)"""
import io, json, struct, sys
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]; Q = int(sys.argv[3]) if len(sys.argv) > 3 else 88
b = open(src, "rb").read(); jl, _ = struct.unpack("<II", b[12:20]); js = json.loads(b[20:20 + jl]); bl = struct.unpack("<I", b[20 + jl:24 + jl])[0]; bin_ = b[28 + jl:28 + jl + bl]
bvs = js["bufferViews"]; image_views = {i["bufferView"] for i in js["images"]}
new = bytearray(); offs = {}
for k, v in enumerate(bvs):
    data = bin_[v.get("byteOffset", 0):v.get("byteOffset", 0) + v["byteLength"]]
    if k in image_views:
        im = Image.open(io.BytesIO(data)); o = io.BytesIO()
        im.save(o, "WEBP", quality=Q, method=6, lossless=False) if im.mode in ("RGB", "RGBA") else im.convert("RGB").save(o, "WEBP", quality=Q, method=6)
        data = o.getvalue()
    while len(new) % 4: new.append(0)
    offs[k] = (len(new), len(data)); new += data
for k, v in enumerate(bvs):
    v["byteOffset"], v["byteLength"] = offs[k]
for im in js["images"]:
    im["mimeType"] = "image/webp"
for t in js.get("textures", []):
    s = t.pop("source"); t.setdefault("extensions", {})["EXT_texture_webp"] = {"source": s}
for key in ("extensionsUsed", "extensionsRequired"):
    js.setdefault(key, [])
    if "EXT_texture_webp" not in js[key]:
        js[key].append("EXT_texture_webp")
while len(new) % 4: new.append(0)
js["buffers"][0]["byteLength"] = len(new)
jb = json.dumps(js, separators=(",", ":")).encode()
while len(jb) % 4: jb += b" "
out = struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(jb) + 8 + len(new)) + struct.pack("<II", len(jb), 0x4E4F534A) + jb + struct.pack("<II", len(new), 0x004E4942) + bytes(new)
open(dst, "wb").write(out); print("in", len(b), "out", len(out), "images", len(js["images"]))
