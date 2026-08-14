#!/usr/bin/env python3
"""Neutraler Logo-Platzhalter (kein Fantasie-Logo!) in korrekten Groessen,
bis das echte Strandbad-Logo (blau mit Sonnenschirm) geliefert wird.
Gestrichelter Kreis + 'LOGO' - unmissverstaendlich ein Platzhalter.
"""
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img"

NAVY = (13, 23, 41, 255)
SAND = (245, 239, 226, 255)
ORANGE = (240, 122, 22, 255)


def draw_placeholder(size):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pad = max(2, size // 24)
    d.ellipse([pad, pad, size - pad, size - pad], fill=SAND)
    dash = max(1, size // 40)
    gap = dash * 2
    r = size / 2 - pad
    cx = cy = size / 2
    import math
    circumference = 2 * math.pi * r
    n = int(circumference // (dash + gap))
    for i in range(n):
        a0 = 2 * math.pi * i / n
        a1 = a0 + (2 * math.pi / n) * 0.55
        d.arc([pad, pad, size - pad, size - pad], math.degrees(a0), math.degrees(a1), fill=ORANGE, width=max(1, size // 40))
    if size >= 64:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size // 6)
        except OSError:
            font = ImageFont.load_default()
        text = "LOGO"
        bbox = d.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        d.text((cx - tw / 2, cy - th / 2 - bbox[1]), text, fill=NAVY, font=font)
    return im


def main():
    for size in (96, 192, 384):
        im = draw_placeholder(size)
        png_path = OUT / f"logo-{size}.png"
        im.save(png_path)
        webp_path = OUT / f"logo-{size}.webp"
        subprocess.run(["cwebp", "-q", "90", "-quiet", str(png_path), "-o", str(webp_path)], check=True)
        print(f"logo-{size}.png/.webp")

    favicon32 = draw_placeholder(32)
    favicon32.save(OUT / "favicon-32.png")
    favicon180 = draw_placeholder(180)
    favicon180.save(OUT / "favicon-180.png")
    print("favicon-32.png, favicon-180.png")


if __name__ == "__main__":
    main()
