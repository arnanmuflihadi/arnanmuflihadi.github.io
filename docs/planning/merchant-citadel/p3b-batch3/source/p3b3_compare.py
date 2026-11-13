"""Before | after sheets: python3 p3b3_compare.py <wp> <out.jpg> <name> [<name> ...]   (reads merchant-citadel-p2a/evidence/p3b3-<wp>-before-<name>.jpg and -after-)"""
import sys
from PIL import Image, ImageDraw
wp, out, names = sys.argv[1], sys.argv[2], sys.argv[3:]
E = "merchant-citadel-p2a/evidence"; W, H = 720, 405
sheet = Image.new("RGB", (W * 2, H * len(names)), (20, 20, 20))
for r, n in enumerate(names):
    for c, k in enumerate(("before", "after")):
        im = Image.open(f"{E}/p3b3-{wp}-{k}-{n}.jpg").convert("RGB").resize((W, H)); d = ImageDraw.Draw(im); d.rectangle((0, 0, 260, 18), fill=(0, 0, 0)); d.text((6, 4), f"{k}: {n}", fill=(255, 255, 255)); sheet.paste(im, (c * W, r * H))
sheet.save(out, quality=85); print(out, sheet.size)
