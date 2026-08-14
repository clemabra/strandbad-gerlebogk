#!/usr/bin/env python3
"""Kontaktabzug: rasterisiert alle Bilder eines Ordners mit Dateinamen als
Label, damit man schnell sichten kann, ohne jede Datei einzeln zu oeffnen."""
import sys
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont

def build_sheet(folder, out_path, cols=4, thumb=340, label_h=22):
    exts = {".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"}
    files = sorted([p for p in Path(folder).iterdir() if p.suffix in exts and not p.name.startswith(".")])
    if not files:
        print(f"keine Bilder in {folder}")
        return
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb, rows * (thumb + label_h)), "white")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 13)
    except OSError:
        font = ImageFont.load_default()
    for i, f in enumerate(files):
        try:
            im = Image.open(f)
            im = ImageOps.exif_transpose(im)
            im.thumbnail((thumb, thumb))
        except Exception as e:
            print(f"FEHLER {f}: {e}")
            continue
        x = (i % cols) * thumb
        y = (i // cols) * (thumb + label_h)
        ox = x + (thumb - im.width) // 2
        oy = y + (thumb - im.height) // 2
        sheet.paste(im, (ox, oy))
        draw.rectangle([x, y + thumb, x + thumb, y + thumb + label_h], fill="black")
        draw.text((x + 4, y + thumb + 3), f"{i}: {f.name}", fill="white", font=font)
    sheet.save(out_path, quality=85)
    print(f"{out_path}  ({len(files)} Bilder, {cols}x{rows})")

if __name__ == "__main__":
    build_sheet(sys.argv[1], sys.argv[2], cols=int(sys.argv[3]) if len(sys.argv) > 3 else 4)
