"""Prepare the selected third-party flora for the island: copy the chosen Quaternius Stylized Nature MegaKit (Standard, CC0) glTF files, downscale textures
(bark/rock 1024, leaf/flower 512, grass 256), drop normal maps (texture memory), keep alpha-mask materials. Original files are never modified.
python3 p3b2_prepare_flora.py <nature-standard dir> <out dir>"""
import sys, os, json, shutil
from PIL import Image
src, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
SEL = ["CommonTree_1", "CommonTree_3", "CommonTree_4", "Pine_1", "Pine_5", "TwistedTree_2", "DeadTree_3", "Bush_Common", "Bush_Common_Flowers", "Fern_1", "Plant_1_Big", "Plant_7_Big", "Clover_1", "Flower_3_Group", "Flower_4_Group", "Flower_3_Single", "Flower_4_Single",
       "Grass_Common_Tall", "Grass_Common_Short", "Grass_Wispy_Tall", "Mushroom_Common", "Rock_Medium_1", "Rock_Medium_2", "Rock_Medium_3", "Pebble_Round_1", "Pebble_Round_3", "Pebble_Square_1", "Pebble_Square_3", "RockPath_Round_Small_1", "RockPath_Round_Small_2", "RockPath_Square_Small_1", "RockPath_Round_Wide", "RockPath_Square_Wide"]
SIZE = lambda n: 1024 if n.startswith(("Bark", "Rocks", "PathRocks")) else (256 if n.startswith("Grass") else 512)
done = {}
for name in SEL:
    j = json.load(open(os.path.join(src, "glTF", name + ".gltf")))
    for m in j["materials"]:
        m.pop("normalTexture", None)
        if "pbrMetallicRoughness" in m: m["pbrMetallicRoughness"]["metallicFactor"] = 0.0; m["pbrMetallicRoughness"]["roughnessFactor"] = max(m["pbrMetallicRoughness"].get("roughnessFactor", 0.9), 0.85)
    used = set()
    for m in j["materials"]:
        t = m.get("pbrMetallicRoughness", {}).get("baseColorTexture")
        if t: used.add(j["textures"][t["index"]]["source"])
    for k, im in enumerate(j["images"]):
        if k not in used: continue
        uri = im["uri"]
        if uri == 'Leaves_TwistedTree_C.png': uri = 'Leaves_TwistedTree.png'; im['uri'] = uri      # the _C variant is the autumn (red) leaf; the plain one is green
        dst = os.path.join(out, uri)
        if uri not in done:
            img = Image.open(os.path.join(src, "Textures", uri)); s = SIZE(uri); img.thumbnail((s, s), Image.LANCZOS); img.save(dst); done[uri] = img.size
        im["uri"] = uri
    # point images at the resized copies, dropping unused (normal map) entries from use by clearing their uri to the same file if present
    for k, im in enumerate(j["images"]):
        if k not in used:
            im["uri"] = sorted(done)[0] if done else im["uri"]
    shutil.copy(os.path.join(src, "glTF", name + ".bin"), out) if os.path.exists(os.path.join(src, "glTF", name + ".bin")) else None
    json.dump(j, open(os.path.join(out, name + ".gltf"), "w"))
json.dump(done, open(os.path.join(out, "textures.json"), "w"), indent=1); print(len(SEL), "models,", len(done), "textures", done)
