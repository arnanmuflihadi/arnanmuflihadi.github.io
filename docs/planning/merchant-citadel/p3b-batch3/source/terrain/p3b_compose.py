"""Compose comparison sheets: P3-A massing reference | P3-B Blender | P3-B browser (Three.js). python3 p3b_compose.py <blender_dir> <browser_dir> <p3a_dir> <out_dir>
Blender files p3b-<view>.png, browser files p3b-b-<view>.jpg, P3-A files <view>.jpg. Missing inputs are skipped and reported."""
import sys, os, json
from PIL import Image, ImageDraw, ImageFont

bl, br, p3a, out = sys.argv[1:5]; os.makedirs(out, exist_ok=True)
views = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "p3b_views.json")))
W = 800
try:
    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
except Exception:
    font = ImageFont.load_default()


def load(path):
    if not os.path.exists(path):
        return None
    im = Image.open(path).convert("RGB"); h = int(im.height * W / im.width); return im.resize((W, h), Image.LANCZOS)


def label(im, text):
    d = ImageDraw.Draw(im); d.rectangle([0, 0, W, 30], fill=(20, 32, 28)); d.text((10, 4), text, fill=(243, 234, 216), font=font); return im


done, missing = [], []
for name in views:
    a = load(os.path.join(p3a, name + ".jpg")); b = load(os.path.join(bl, "p3b-%s.png" % name)); c = load(os.path.join(br, "p3b-b-%s.jpg" % name))
    cols = [(x, t) for x, t in ((a, "P3-A concept (Blender massing)"), (b, "P3-B Blender (from the exported GLB)"), (c, "P3-B browser (Three.js preview)")) if x is not None]
    if len(cols) < 2:
        missing.append(name); continue
    h = max(x.height for x, _ in cols); sheet = Image.new("RGB", (W * len(cols), h + 30), (20, 32, 28))
    for i, (x, t) in enumerate(cols):
        sheet.paste(label(x.copy(), t), (i * W, 0)) if False else (sheet.paste(x, (i * W, 30)), ImageDraw.Draw(sheet).text((i * W + 10, 4), t, fill=(243, 234, 216), font=font))
    sheet.save(os.path.join(out, "compare-%s.jpg" % name), quality=88); done.append(name)
print("sheets", len(done), "missing", missing)
