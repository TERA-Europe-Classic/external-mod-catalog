#!/usr/bin/env python3
"""Produce catalog media (cover.webp + thumb.webp) and a blur_data URI from a
source image. Keeps every mod image webp + optimized + small, matching the
existing media pipeline. Usage:

    python make_media.py <src-image> <mod-id> [--cover-max 900] [--thumb 288]

Writes media/<mod-id>/cover.webp and thumb.webp, and prints the blur_data
data-URI (tiny 16px webp, base64) to stdout so it can be pasted into the
catalog entry's blur_data field.
"""
import sys, io, os, base64, argparse
from PIL import Image

def to_webp_bytes(img, quality=82, method=6):
    buf = io.BytesIO()
    img.save(buf, format="WEBP", quality=quality, method=method)
    return buf.getvalue()

def fit(img, max_dim):
    w, h = img.size
    scale = min(1.0, max_dim / max(w, h))
    if scale < 1.0:
        img = img.resize((max(1, round(w * scale)), max(1, round(h * scale))), Image.LANCZOS)
    return img

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("mod_id")
    ap.add_argument("--cover-max", type=int, default=900)
    ap.add_argument("--thumb", type=int, default=288)
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    args = ap.parse_args()

    img = Image.open(args.src).convert("RGB")
    out_dir = os.path.join(args.root, "media", args.mod_id)
    os.makedirs(out_dir, exist_ok=True)

    cover = fit(img.copy(), args.cover_max)
    with open(os.path.join(out_dir, "cover.webp"), "wb") as f:
        f.write(to_webp_bytes(cover, quality=82))

    thumb = fit(img.copy(), args.thumb)
    with open(os.path.join(out_dir, "thumb.webp"), "wb") as f:
        f.write(to_webp_bytes(thumb, quality=80))

    blur = fit(img.copy(), 16)
    blur_uri = "data:image/webp;base64," + base64.b64encode(to_webp_bytes(blur, quality=40)).decode()

    print(f"cover: {os.path.getsize(os.path.join(out_dir,'cover.webp'))} B  "
          f"thumb: {os.path.getsize(os.path.join(out_dir,'thumb.webp'))} B")
    print(blur_uri)

if __name__ == "__main__":
    main()
