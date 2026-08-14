#!/usr/bin/env python3
"""Erzeugt alle responsiven Bildvarianten (WebP + JPG-Fallback) fuer die
Strandbad-Gerlebogk-Website aus den bereits umbenannten/geraderichteten
Quellbildern in assets/img/src/.

Aufruf: python3 tools/build-images.py
"""
import subprocess
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "img" / "src"
OUT = ROOT / "assets" / "img"

# name -> Liste der Zielbreiten (px), grösste zuerst wird nicht ueberschritten
MANIFEST = {
    "sonnenuntergang-see": [640, 1000, 1536],
    "traubogen-see": [500, 750, 1002],
    "trauung-strand": [480, 750, 970],
    "luftaufnahme-strandbad": [480, 800, 1600],
    "see-blaue-stunde": [480, 800, 1200],
    "strandbar-liegestuehle": [480, 800, 1600],
    "lounge-deck-nacht": [480, 800, 1536],
    "terrasse-abendsonne": [480, 800, 1536],
    "zeltanlage-terrasse": [480, 800, 1600],
    "festzelt-hochzeitstafel": [480, 800, 1600],
    "tischdeko-detail": [480, 800, 1536],
    "ruderboot-daemmerung": [380],
    "catering-fingerfood": [380],
    "catering-buffet": [380],

    # Zweite Lieferung (Kategorie-Ordner "Strandbad Assets")
    "ruderboot-tag": [480, 800, 1600],
    "abenddaemmerung-baum": [480, 800, 1599],
    "wolken-spiegelung-see": [480, 800, 1600],
    "sonnenuntergang-allee": [640, 1000, 1600],
    "nachtfeier-lichter": [640, 1000, 1600],
    "deck-abend-schirme": [480, 800, 1600],
    "hochzeitstafel-kerzen": [480, 800, 1600],
    "deck-sonnensegel-tag": [640, 1000, 1600],
    "deko-kiste-laterne": [480, 800],
    "festzelt-tafel-innen": [640, 1000, 1600],
    "festzelt-tischdeko-palme": [480, 800, 1600],
    "mondaufgang-strand": [640, 1000, 1600],
    "team-shirt": [480, 800, 1600],
    "team-grillen": [480, 800, 1600],
    "catering-tafel-uebersicht": [640, 1000, 1600],
    "catering-fruchtsalat": [480, 800, 1200],
    "catering-kaesebrett": [480, 800, 1200],
    "catering-grillspiesse": [480, 800, 1200],
    "catering-braten": [480, 800, 1200],
    "catering-dessert": [480, 800, 1200],
    "catering-salat-bluete": [480, 800, 1200],
    "catering-haehnchen": [480, 800, 1200],
    "catering-krautsalat": [480, 800, 1200],
    "campingplatz-wohnwagen": [480, 800, 1600],
}

JPG_QUALITY = 82
WEBP_QUALITY = 82


def build_variant(im, width, base_out):
    w, h = im.size
    width = min(width, w)
    height = round(h * (width / w))
    resized = im.resize((width, height), Image.LANCZOS)

    jpg_path = base_out.with_name(f"{base_out.name}-{width}.jpg")
    resized.convert("RGB").save(jpg_path, "JPEG", quality=JPG_QUALITY, optimize=True, progressive=True)

    webp_path = base_out.with_name(f"{base_out.name}-{width}.webp")
    subprocess.run(
        ["cwebp", "-q", str(WEBP_QUALITY), "-quiet", str(jpg_path), "-o", str(webp_path)],
        check=True,
    )
    return width, height, jpg_path.stat().st_size, webp_path.stat().st_size


def cover_crop(im, target_ratio):
    w, h = im.size
    cur_ratio = w / h
    if cur_ratio > target_ratio:
        new_w = round(h * target_ratio)
        left = (w - new_w) // 2
        return im.crop((left, 0, left + new_w, h))
    else:
        new_h = round(w / target_ratio)
        top = (h - new_h) // 2
        return im.crop((0, top, w, top + new_h))


def build_og(name, out_name):
    im = Image.open(SRC / f"{name}.jpg")
    im = ImageOps.exif_transpose(im)
    cropped = cover_crop(im, 1200 / 630).resize((1200, 630), Image.LANCZOS)
    path = OUT / f"{out_name}.jpg"
    cropped.convert("RGB").save(path, "JPEG", quality=85, optimize=True)
    print(f"OG  {out_name}.jpg  1200x630  ({path.stat().st_size // 1024} KB)")


def main():
    print(f"{'Datei':40s} {'Breite':>7s} {'Hoehe':>7s} {'JPG':>8s} {'WebP':>8s}")
    for name, widths in MANIFEST.items():
        im = Image.open(SRC / f"{name}.jpg")
        im = ImageOps.exif_transpose(im)
        for width in sorted(set(widths)):
            w, h, jsize, wsize = build_variant(im, width, OUT / name)
            print(f"{name:40s} {w:7d} {h:7d} {jsize/1024:7.1f}K {wsize/1024:7.1f}K")

    build_og("luftaufnahme-strandbad", "og-default")
    build_og("traubogen-see", "og-hochzeit")
    build_og("catering-tafel-uebersicht", "og-catering")


if __name__ == "__main__":
    main()
