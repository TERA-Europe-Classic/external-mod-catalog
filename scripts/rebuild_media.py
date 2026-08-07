"""Pick each mod's hero from everything we hold, and keep the rest as gallery.

`fetch_source_media.py --all` puts every image from every mod's original post
on disk. This decides which one a player should see first, and it MERGES --
the earlier passes recovered images the source posts no longer serve (448 from
a Discord export, a hand-picked GIF for the Sailor Moon bar), and replacing
`screenshots` wholesale would throw those away to make room for what the crawl
happened to find today.

WHY A HERO NEEDS PICKING AT ALL

The eye and face mods carry a macro texture dump as their cover: a blown-up
crop of the DDS, mostly one skin tone, nothing of the mod visible. It passes
every "does this entry have media" test ever written, which is why five media
passes left it in place. So the test here is not presence, it is whether the
image looks like a photograph of the game.

Two signals separate them, both cheap:

  colour spread   a texture dump of skin is a narrow band of one hue. A
                  screenshot carries UI, background, hair, sky -- a wide
                  spread. Measured as the mean per-channel standard deviation.
  aspect          screenshots are landscape or near it, from a game window.
                  Texture crops are square, because textures are square.

Neither is decisive alone: a dark screenshot has low spread, and a cropped
screenshot can be square. Scored together, with size as the tie-break, they
rank the real shots above the dumps reliably enough to be worth reviewing --
and the ranking is written to a report so it CAN be reviewed, rather than
silently applied to 542 entries.

    python scripts/rebuild_media.py                 # rank, write the report
    python scripts/rebuild_media.py --write         # ...and update catalog.json
"""
import argparse
import collections
import hashlib
import io
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MEDIA = os.path.join(ROOT, 'media')
CDN = ('https://cdn.jsdelivr.net/gh/TERA-Europe-Classic/'
       'external-mod-catalog@main/')
REPORT = os.path.join(ROOT, '_media_report.json')

# Under this and it is an avatar, a spacer or a flat swatch, never a hero.
MIN_BYTES = 20_000


def png_size(b):
    if b[:8] != b'\x89PNG\r\n\x1a\n':
        return None
    w, h = struct.unpack('>II', b[16:24])
    return w, h


def jpeg_size(b):
    i = 2
    while i < len(b) - 9:
        if b[i] != 0xFF:
            i += 1
            continue
        marker = b[i + 1]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3):
            h, w = struct.unpack('>HH', b[i + 5:i + 9])
            return w, h
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        i += 2 + struct.unpack('>H', b[i + 2:i + 4])[0]
    return None


def dimensions(path):
    """Width and height without decoding the pixels, or None."""
    try:
        b = io.open(path, 'rb').read(64 * 1024)
    except OSError:
        return None
    return png_size(b) or jpeg_size(b)


def measure(path):
    """(spread, (w, h)) via Pillow, falling back to the header parsers.

    Pillow is optional on purpose -- this repo's CI installs jsonschema and
    nothing else, and a media pass that only runs on one machine is worse than
    one that degrades to size-and-shape ranking everywhere. But when it IS
    present it must also supply the dimensions, because the header parsers
    above read PNG and JPEG only. Every curated cover in this repo is a .webp
    and every hand-picked capture is a .gif, so leaving those two to the
    fallback silently denied the resolution bonus to exactly the images most
    likely to be the right hero.
    """
    dim = None
    try:
        from PIL import Image, ImageStat
    except ImportError:
        return None, dimensions(path)
    try:
        with Image.open(path) as im:
            dim = im.size
            im = im.convert('RGB')
            im.thumbnail((160, 160))
            st = ImageStat.Stat(im)
            return sum(st.stddev) / len(st.stddev), dim
    except Exception:                                              # noqa: BLE001
        return None, dim or dimensions(path)


def score(path):
    """Higher is more likely to be a screenshot of the game."""
    size = os.path.getsize(path)
    if size < MIN_BYTES:
        return -1.0, {'bytes': size, 'why': 'too small to be a screenshot'}
    spread, dim = measure(path)
    detail = {'bytes': size}
    s = 0.0
    if dim:
        w, h = dim
        detail['dim'] = f'{w}x{h}'
        ratio = w / h if h else 1.0
        # Landscape reads as a game window; a perfect square reads as a texture.
        s += 25.0 if 1.2 <= ratio <= 2.4 else (-15.0 if 0.95 <= ratio <= 1.05 else 0.0)
        s += min(w * h / 40_000.0, 25.0)
    if spread is not None:
        detail['spread'] = round(spread, 1)
        # A flat crop of one skin tone sits near 10; a real shot clears 40.
        s += min(spread, 70.0)
    else:
        detail['spread'] = None
        s += min(size / 40_000.0, 20.0)
    return s, detail


EXTS = ('.png', '.jpg', '.jpeg', '.webp', '.gif')
# Above this many entries an image is the SITE, not the mod. Measured, not
# guessed: 2,349 images appear in one entry, 37 in two, 30 in three or four --
# then a gap, and 10 images appear in five or more. The top two sit in 364 and
# 213 entries.
CHROME_ENTRIES = 4

# A hero below this is one the player cannot see the mod in: a sub-20 KB
# swatch, a flat thumbnail, a macro crop of skin tone. Above it, leave it be.
REPLACE_BELOW = 45.0
# And the replacement has to be clearly better, not a rounding win.
MARGIN = 10.0


def current_hero_path(entry):
    """Local path of the hero the entry ships today, or None."""
    u = entry.get('featured_image') or ''
    marker = 'external-mod-catalog@main/'
    if marker not in u:
        return None
    p = os.path.join(ROOT, u.split(marker, 1)[1].replace('/', os.sep))
    return p if os.path.exists(p) else None


def sha(path):
    try:
        return hashlib.sha256(io.open(path, 'rb').read()).hexdigest()
    except OSError:
        return None


def chrome_hashes():
    """Images that belong to the blog rather than to any mod.

    The crawl pulls every image on the source page, and a tumblr page carries
    the blog's own banner and avatar. Scored on their pixels those are superb
    heroes -- big, landscape, wildly colourful -- so the ranker put a stock
    photo captioned "MODS!" in front of three mods in a sample of eight,
    replacing a good character shot each time.

    No pixel test separates them, because there is nothing wrong with the
    image. What gives it away is that it is the SAME image on hundreds of
    unrelated mods. Three or four entries sharing a shot is a colour-variant
    family and stays.
    """
    census = collections.defaultdict(set)
    for mid in os.listdir(MEDIA):
        d = os.path.join(MEDIA, mid)
        if not os.path.isdir(d):
            continue
        for name in os.listdir(d):
            if os.path.splitext(name)[1].lower() not in EXTS:
                continue
            h = sha(os.path.join(d, name))
            if h:
                census[h].add(mid)
    return {h for h, mids in census.items() if len(mids) > CHROME_ENTRIES}


def local_images(mid, chrome, seen_here=None):
    d = os.path.join(MEDIA, mid)
    if not os.path.isdir(d):
        return []
    keep, dupes = [], set()
    for name in sorted(os.listdir(d)):
        if os.path.splitext(name)[1].lower() not in EXTS:
            continue
        p = os.path.join(d, name)
        h = sha(p)
        if h in chrome:
            continue
        # The crawl saves src0.png and src0.webp for the same image; listing
        # both puts a duplicate in the gallery.
        if h in dupes:
            continue
        dupes.add(h)
        keep.append(p)
    return keep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--limit', type=int, default=0)
    args = ap.parse_args()

    raw = io.open(os.path.join(ROOT, 'catalog.json'), 'rb').read().decode('utf-8')
    nl = '\r\n' if '\r\n' in raw else '\n'
    doc = json.loads(raw)
    mods = doc['mods'][:args.limit] if args.limit else doc['mods']

    chrome = chrome_hashes()
    print(f'{len(chrome)} image(s) excluded as site chrome '
          f'(shared by more than {CHROME_ENTRIES} entries)')

    report, changed, nomedia = {}, 0, 0
    for m in mods:
        mid = m['id']
        files = local_images(mid, chrome)
        if not files:
            nomedia += 1
            # Say so. A silent skip here reads as "reviewed and fine".
            report[mid] = {'hero': None, 'why': 'no local media'}
            continue
        ranked = sorted(((score(f), f) for f in files),
                        key=lambda t: t[0][0], reverse=True)
        (best_score, best_detail), best = ranked[0]
        rel = [CDN + os.path.relpath(f, ROOT).replace('\\', '/') for _, f in ranked]

        # Replace the hero only when the CURRENT one is bad -- not merely when
        # something outranks it.
        #
        # Ranked purely by score, 383 of 584 heroes moved, and the sample said
        # most of those were sideways or worse: a wide landscape with two tiny
        # characters beat a tight portrait of the costume, because the score
        # rewards resolution and landscape aspect and cannot see that the
        # subject is 40 pixels tall. Meanwhile the actual complaint -- covers
        # you cannot see the mod in -- is 158 entries, 125 of them sub-20 KB
        # swatches that score below zero on sight.
        #
        # So: fix what is broken, leave what works. Churning 383 good heroes to
        # catch 158 bad ones is how five earlier passes made this worse.
        cur = current_hero_path(m)
        cur_score = score(cur)[0] if cur else -99.0
        take = cur_score < REPLACE_BELOW and best_score > cur_score + MARGIN
        report[mid] = {
            'hero': rel[0] if take else (m.get('featured_image') or rel[0]),
            'replaced': take,
            'current_score': round(cur_score, 1),
            'score': round(best_score, 1),
            'detail': best_detail,
            'ranked': [{'url': u, 'score': round(s[0], 1)}
                       for u, ((s), _) in zip(rel, [r for r in ranked])],
        }
        if args.write:
            if take:
                m['featured_image'] = rel[0]
                changed += 1
            # MERGE either way: everything already listed stays, ranked
            # additions follow, deduped. The 448 Discord-recovered images are
            # not re-fetchable, so a wholesale replace loses them for good.
            have = list(m.get('screenshots') or [])
            merged = have + [u for u in rel if u not in have
                             and u != m.get('featured_image')]
            if merged:
                m['screenshots'] = merged

    io.open(REPORT, 'w', encoding='utf-8').write(
        json.dumps(report, indent=1, ensure_ascii=False) + '\n')
    print(f'{len(report)} entries ranked, {nomedia} hold no local media')
    print(f'report -> {os.path.relpath(REPORT, ROOT)}')
    if args.write:
        io.open(os.path.join(ROOT, 'catalog.json'), 'w', encoding='utf-8',
                newline=nl).write(json.dumps(doc, indent=1, ensure_ascii=False) + '\n')
        print(f'catalog.json written, {changed} entries updated')
    else:
        print('dry run -- pass --write to update catalog.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
