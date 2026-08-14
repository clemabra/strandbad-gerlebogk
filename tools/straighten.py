#!/usr/bin/env python3
"""Straighten a tilted photo: rotate by ANGLE degrees (CCW positive) and
crop to the largest axis-aligned rectangle that fits without empty corners.

Usage: python3 straighten.py <input.jpg> <output.jpg> <angle_degrees>
"""
import sys
import math
from PIL import Image


def rotated_rect_with_max_area(w, h, angle_deg):
    angle = math.radians(angle_deg)
    if w <= 0 or h <= 0:
        return 0, 0
    width_is_longer = w >= h
    side_long, side_short = (w, h) if width_is_longer else (h, w)
    sin_a, cos_a = abs(math.sin(angle)), abs(math.cos(angle))
    if side_short <= 2. * sin_a * cos_a * side_long or abs(sin_a - cos_a) < 1e-10:
        x = 0.5 * side_short
        wr, hr = (x / sin_a, x / cos_a) if width_is_longer else (x / cos_a, x / sin_a)
    else:
        cos_2a = cos_a * cos_a - sin_a * sin_a
        wr, hr = (w * cos_a - h * sin_a) / cos_2a, (h * cos_a - w * sin_a) / cos_2a
    return wr, hr


def straighten(path_in, path_out, angle_deg):
    im = Image.open(path_in)
    w, h = im.size
    rotated = im.rotate(angle_deg, expand=True, resample=Image.BICUBIC)
    rw, rh = rotated.size
    cw, ch = rotated_rect_with_max_area(w, h, angle_deg)
    cw, ch = min(cw, rw), min(ch, rh)
    left = (rw - cw) / 2
    top = (rh - ch) / 2
    cropped = rotated.crop((left, top, left + cw, top + ch))
    cropped.save(path_out, quality=95)
    print(f"{path_in} -> {path_out}: rotate {angle_deg}deg, {w}x{h} -> {cropped.size[0]:.0f}x{cropped.size[1]:.0f}")


if __name__ == "__main__":
    straighten(sys.argv[1], sys.argv[2], float(sys.argv[3]))
