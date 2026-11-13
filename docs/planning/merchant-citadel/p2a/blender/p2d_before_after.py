"""Batch 4 evidence sheets (needs Pillow).

  python3 p2d_before_after.py <blender_before> <blender_after> <browser_dir> <before_tag> <after_tag> <out_dir> <view> [<view> ...]

For every view writes
  ba-<view>.jpg   2 x 2 sheet: top row Blender (before | after), bottom row Three.js (before | after), same camera in all four
  cmp-<view>.jpg  Blender after | Three.js after (the matched pair), with mean luma of each
Browser shots are <browser_dir>/shot-<view>-<tag>.png (written by the preview's ?autotest=views&shot=<tag>); Blender renders are <dir>/renders/<view>.png.
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw

BB, BA, BR, TB, TA, OUT = sys.argv[1:7]; views = sys.argv[7:]
os.makedirs(OUT, exist_ok=True)
W = 800


def load(path, w=W):
    im = Image.open(path).convert("RGB"); return im.resize((w, int(w * im.size[1] / im.size[0])))


def label(im, text):
    d = ImageDraw.Draw(im); d.rectangle((0, 0, im.size[0], 22), fill=(20, 20, 20)); d.text((8, 5), text, fill=(240, 240, 240)); return im


for v in views:
    paths = {"bb": os.path.join(BB, "renders", v + ".png"), "ba": os.path.join(BA, "renders", v + ".png"), "tb": os.path.join(BR, f"shot-{v}-{TB}.png"), "ta": os.path.join(BR, f"shot-{v}-{TA}.png")}
    have = {k: p for k, p in paths.items() if os.path.exists(p)}
    if "ba" in have and "ta" in have:
        a, b = load(have["ba"]), load(have["ta"]); la = np.asarray(a.convert("L"), float).mean(); lb = np.asarray(b.convert("L"), float).mean()
        sheet = Image.new("RGB", (W * 2 + 6, a.size[1] + 22), (24, 24, 24)); sheet.paste(label(a, f"{v}  Blender (Eevee, P1.4 look)  luma {la:.0f}"), (0, 0)); sheet.paste(label(b, f"Three.js browser (production GLB, real controller)  luma {lb:.0f}"), (W + 6, 0))
        sheet.convert("RGB").save(os.path.join(OUT, f"cmp-{v}.jpg"), quality=88)
    if all(k in have for k in ("tb", "ta")):
        ims = [label(load(have[k]), t) for k, t in (("bb", os.environ.get("P2D_LBL_BB","Blender before")), ("ba", os.environ.get("P2D_LBL_BA","Blender after")), ("tb", os.environ.get("P2D_LBL_TB","Three.js before")), ("ta", os.environ.get("P2D_LBL_TA","Three.js after"))) if k in have]
        h = ims[0].size[1]; rows = (len(ims) + 1) // 2; sheet = Image.new("RGB", (W * 2 + 6, rows * (h + 6)), (24, 24, 24))
        for i, im in enumerate(ims):
            sheet.paste(im, ((i % 2) * (W + 6), (i // 2) * (h + 6)))
        sheet.save(os.path.join(OUT, f"ba-{v}.jpg"), quality=88); print(v, "ok")
