#!/usr/bin/env python3
"""Compose rendered tiles into the labelled contact sheet (plain Pillow, no AI imagery).

Usage: python3 compose_contact_sheet.py <layout.json> <tiles_dir> <out.png> [cols]
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

layout, tiles_dir, out = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3]
COLS = int(sys.argv[4]) if len(sys.argv) > 4 else 8
T, LBL, PAD, HEAD, TOP = 300, 46, 10, 40, 96


def font(size, bold=False):
    for p in ("/System/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/Supplemental/Arial.ttf"):
        try:
            return ImageFont.truetype(p, size, index=1 if (bold and p.endswith(".ttc")) else 0)
        except Exception:
            continue
    return ImageFont.load_default()


F_T, F_H, F_L, F_S = font(30, True), font(19, True), font(13, True), font(12)
rows = sum(-(-len(s["tiles"]) // COLS) for s in layout)
W = PAD + COLS * (T + PAD)
H = TOP + len(layout) * HEAD + rows * (T + LBL + PAD) + PAD
img = Image.new("RGB", (W, H), (244, 243, 238))
d = ImageDraw.Draw(img)
d.text((PAD, 14), "Merchant Citadel P1 - REAL ASSET RENDER contact sheet", font=F_T, fill=(24, 44, 40))
d.text((PAD, 54), "Every tile is an actual model imported from the freshly downloaded free archives (Blender 5.2, EEVEE, neutral light). "
       "Teal figure = 1.9 m explorer. Labels: asset id | W x H x D metres as authored | triangles.", font=F_S, fill=(70, 80, 78))
y = TOP
for sec in layout:
    d.rectangle([0, y, W, y + HEAD - 6], fill=(28, 56, 52))
    d.text((PAD, y + 7), sec["title"], font=F_H, fill=(245, 240, 225))
    y += HEAD
    for i, t in enumerate(sec["tiles"]):
        if i and i % COLS == 0:
            y += T + LBL + PAD
        x = PAD + (i % COLS) * (T + PAD)
        d.rectangle([x, y, x + T, y + T + LBL], fill=(226, 228, 226), outline=(196, 198, 194))
        p = os.path.join(tiles_dir, t["id"] + ".png")
        if os.path.exists(p):
            im = Image.open(p).convert("RGBA").resize((T, T), Image.LANCZOS)
            img.paste(im, (x, y), im)
        else:
            d.text((x + 8, y + 8), "RENDER MISSING", font=F_L, fill=(160, 30, 30))
        name = t["id"]
        while d.textlength(name, font=F_L) > T - 8:
            name = name[:-2]
        d.text((x + 5, y + T + 4), name, font=F_L, fill=(20, 30, 30))
        w, h, dd = t["dims"]
        d.text((x + 5, y + T + 24), f"{w:.2f} x {h:.2f} x {dd:.2f} m | {t['tris']:,} tris", font=F_S, fill=(70, 80, 78))
    y += T + LBL + PAD
img.save(out, optimize=True)
print("wrote", out, img.size)
