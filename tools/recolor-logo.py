#!/usr/bin/env python3
"""Rechnet ein flaches 2-3-Farben-Logo (z. B. vom Betreiber geliefertes
PNG in Fremdfarben) auf die Website-Palette um, per gewichteter
Farbdistanz statt hartem Schwellenwert (erhaelt sauberes Anti-Aliasing
an Kanten).

Aufruf: python3 tools/recolor-logo.py <input.png> <output.png> \
    <alt_farbe1> <neu_farbe1> [<alt_farbe2> <neu_farbe2> ...]

Farben als Hex ohne #, z.B.:
python3 tools/recolor-logo.py alt.png neu.png \
    022b51 0d1729  f97305 f07a16  fdfdfd fdfdfd
"""
import sys
from PIL import Image
import numpy as np


def hex_to_rgb(h):
    h = h.lstrip('#')
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=float)


def recolor(path_in, path_out, farbpaare, scharfe=3):
    im = Image.open(path_in).convert('RGBA')
    arr = np.array(im).astype(float)
    rgb = arr[:, :, :3]
    alpha = arr[:, :, 3]

    refs = np.stack([hex_to_rgb(a) for a, _ in farbpaare])
    targets = np.stack([hex_to_rgb(b) for _, b in farbpaare])

    h, w, _ = rgb.shape
    flat = rgb.reshape(-1, 3)
    dists = np.linalg.norm(flat[:, None, :] - refs[None, :, :], axis=2)
    weights = 1.0 / (dists + 1e-3) ** scharfe
    weights = weights / weights.sum(axis=1, keepdims=True)
    neu_flat = weights @ targets
    neu_rgb = neu_flat.reshape(h, w, 3).clip(0, 255).astype('uint8')

    out = np.dstack([neu_rgb, alpha.astype('uint8')])
    Image.fromarray(out, 'RGBA').save(path_out)
    print(f"{path_in} -> {path_out}: {len(farbpaare)} Farbpaare umgerechnet")


if __name__ == "__main__":
    args = sys.argv[1:]
    path_in, path_out = args[0], args[1]
    rest = args[2:]
    paare = list(zip(rest[0::2], rest[1::2]))
    recolor(path_in, path_out, paare)
