"""Shrink harvested screenshots so the repo stays a catalog, not an image host.

The source pass pulled 401 MB of author screenshots. That would sit in git
history forever and jsDelivr is a CDN for a repo, not a photo bucket. Re-encoding
to webp at a sane width keeps everything the detail panel can actually show.

Animated gifs become ANIMATED webp -- the animation is the point of a showcase
gif, so flattening them would lose the thing worth keeping.

    python scripts/compress_media.py --dry-run
    python scripts/compress_media.py --write
"""
import argparse
import glob
import io
import json
import os
import sys
import traceback

from PIL import Image, ImageSequence

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MAX_W_STILL = 1600
MAX_W_ANIM = 1024


def convert(path, write):
    """-> (new_path or None, old_size, new_size)."""
    old = os.path.getsize(path)
    im = Image.open(path)
    animated = getattr(im, 'n_frames', 1) > 1
    out = os.path.splitext(path)[0] + '.webp'
    if animated:
        frames = []
        for fr in ImageSequence.Iterator(im):
            fr = fr.convert('RGBA')
            if fr.width > MAX_W_ANIM:
                fr = fr.resize((MAX_W_ANIM, round(fr.height * MAX_W_ANIM / fr.width)),
                               Image.LANCZOS)
            frames.append(fr)
        if not write:
            return out, old, old
        frames[0].save(out, 'WEBP', save_all=True, append_images=frames[1:],
                       duration=im.info.get('duration', 100),
                       loop=im.info.get('loop', 0), quality=72, method=4)
    else:
        if im.width > MAX_W_STILL:
            im = im.resize((MAX_W_STILL, round(im.height * MAX_W_STILL / im.width)),
                           Image.LANCZOS)
        if not write:
            return out, old, old
        im.convert('RGBA' if im.mode == 'RGBA' else 'RGB').save(
            out, 'WEBP', quality=82, method=4)
    # PIL keeps the source file open, and on Windows an open handle makes
    # os.remove raise PermissionError [WinError 32]. Every conversion failed on
    # this until the handle was closed first -- and a bare `except` hid it.
    im.close()
    new = os.path.getsize(out)
    if new >= old and out != path:
        os.remove(out)                       # bigger than the source: keep the source
        return None, old, old
    if out != path:
        os.remove(path)
    return out, old, new


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(ROOT, 'media', '*', 'src*')))
    files = [f for f in files if not f.lower().endswith('.webp')]
    print(f'{len(files)} harvested files to consider', flush=True)

    before = after = 0
    renames, done, kept, failed = {}, 0, 0, 0
    for i, f in enumerate(files, 1):
        try:
            out, o, n = convert(f, args.write)
        except Exception:                                         # noqa: BLE001
            failed += 1
            if failed <= 3:
                traceback.print_exc()
            before += os.path.getsize(f)
            after += os.path.getsize(f)
            continue
        before += o
        after += n
        if out and out != f:
            renames[os.path.relpath(f, ROOT).replace(os.sep, '/')] = \
                os.path.relpath(out, ROOT).replace(os.sep, '/')
            done += 1
        else:
            kept += 1
        if i % 100 == 0:
            print(f'  {i}/{len(files)}  {before/1e6:.0f} -> {after/1e6:.0f} MB', flush=True)

    print(f'\n{done} converted, {kept} kept as-is, {failed} failed')
    print(f'{before/1e6:.0f} MB -> {after/1e6:.0f} MB')
    if not args.write:
        print('dry run -- pass --write')
        return 0

    raw = io.open(os.path.join(ROOT, 'catalog.json'), 'rb').read().decode('utf-8')
    nl = '\r\n' if '\r\n' in raw else '\n'
    doc = json.loads(raw)
    hits = 0
    for m in doc['mods']:
        for field in ('featured_image', 'cover'):
            v = m.get(field)
            if v:
                for old, new in renames.items():
                    if v.endswith(old):
                        m[field] = v.replace(old, new); hits += 1
        if m.get('screenshots'):
            out = []
            for s in m['screenshots']:
                for old, new in renames.items():
                    if s.endswith(old):
                        s = s.replace(old, new); hits += 1
                out.append(s)
            m['screenshots'] = out
    io.open(os.path.join(ROOT, 'catalog.json'), 'w', encoding='utf-8',
            newline=nl).write(json.dumps(doc, indent=1, ensure_ascii=False) + '\n')
    print(f'{hits} catalog references updated')
    return 0


if __name__ == '__main__':
    sys.exit(main())
