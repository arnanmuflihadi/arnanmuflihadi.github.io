"""Side-by-side Blender vs Three.js comparison sheets: python3 p2a_compare.py <blender_renders> <browser_shots> <out_dir> [browser label]"""
import sys, os
from PIL import Image, ImageDraw
import numpy as np
R, S, O = sys.argv[1:4]
LABEL = sys.argv[4] if len(sys.argv) > 4 else 'Three.js browser (ACES, no AO)'
os.makedirs(O, exist_ok=True)
rows = []
for f in sorted(os.listdir(R)):
    n = f[:-4]; s = os.path.join(S, "shot-" + n + ".png")
    if not f.endswith(".png") or not os.path.exists(s): continue
    a = Image.open(os.path.join(R, f)).convert("RGB"); b = Image.open(s).convert("RGB").resize(a.size)
    la = np.asarray(a.convert("L"), float).mean(); lb = np.asarray(b.convert("L"), float).mean()
    W, H = 960, int(960 * a.size[1] / a.size[0])
    sheet = Image.new("RGB", (W * 2 + 6, H + 28), (24, 24, 24)); d = ImageDraw.Draw(sheet)
    sheet.paste(a.resize((W, H)), (0, 28)); sheet.paste(b.resize((W, H)), (W + 6, 28))
    d.text((8, 8), f"{n} - Blender Eevee, P1.4 look (AO, Neutral)  mean luma {la:.0f}", fill=(235, 235, 235))
    d.text((W + 14, 8), f"{LABEL}  mean luma {lb:.0f}", fill=(235, 235, 235))
    sheet.save(os.path.join(O, "cmp-" + n + ".png")); print(n, round(la, 1), round(lb, 1))
