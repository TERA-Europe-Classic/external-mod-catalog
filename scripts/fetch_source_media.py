"""Pull hero and screenshot images from each mod's original post.

407 entries carry no screenshot at all and a dozen covers are under 4 KB --
flat swatches that render as a washed-out blob in the detail panel. The
original posts have the author's own shots; they were just never harvested.

Tumblr serves the real images from media.tumblr.com with a size suffix
(_500, _1280). The largest variant is the one worth keeping, and images under
~20 KB are thumbnails or avatars rather than screenshots.

    python scripts/fetch_source_media.py --dry-run
    python scripts/fetch_source_media.py --write [--limit N]

Downloads only; it does not touch catalog.json unless --write is given.
"""
import argparse
import collections
import io
import json
import os
import re
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MEDIA = os.path.join(ROOT, 'media')
UA = {'User-Agent': 'Mozilla/5.0 (compatible; classicplus-catalog/1.0)'}

# media.tumblr.com/<hash>/tumblr_<id>_<size>.<ext>
IMG_RE = re.compile(
    r'https?://[\w.-]*media\.tumblr\.com/[^"\'\\\s]+?\.(?:png|jpe?g|gifv?|webp)',
    re.I)
GH_RE = re.compile(
    r'https?://(?:raw\.githubusercontent\.com|user-images\.githubusercontent\.com)'
    r'/[^"\'\\\s]+?\.(?:png|jpe?g|gif|webp)', re.I)
SIZE_RE = re.compile(r'_(\d{3,4})\.(png|jpe?g|gifv?|webp)$', re.I)
MIN_BYTES = 20_000          # below this it is a thumbnail or an avatar


def biggest(urls):
    """Tumblr posts embed several sizes of the same image; keep the largest,
    and dedupe on the id so one photo does not become four screenshots."""
    by_id = {}
    for u in urls:
        m = SIZE_RE.search(u)
        size = int(m.group(1)) if m else 0
        key = SIZE_RE.sub('', u)
        if size >= by_id.get(key, (0, ''))[0]:
            by_id[key] = (size, u)
    return [u for _, u in sorted(by_id.values(), key=lambda x: -x[0])]


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def images_in(post_url):
    try:
        html = fetch(post_url).decode('utf-8', 'replace')
    except Exception:                                             # noqa: BLE001
        return []
    urls = IMG_RE.findall(html) + GH_RE.findall(html)
    # avatars and theme furniture live under /avatar_ or are tiny by name
    urls = [u for u in urls if '/avatar_' not in u and 'favicon' not in u]
    return biggest(urls)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--limit', type=int, default=0)
    # Re-crawl EVERY entry that has a source, not only the ones holding no
    # media. Having a screenshot is not the same as having a usable one: the
    # eye and face mods carry a macro texture dump as their hero -- a blurred
    # crop of skin tone where nothing of the mod is visible -- and that passes
    # a "has media" test while showing the player nothing.
    ap.add_argument('--all', action='store_true')
    args = ap.parse_args()

    raw = io.open(os.path.join(ROOT, 'catalog.json'), 'rb').read().decode('utf-8')
    nl = '\r\n' if '\r\n' in raw else '\n'
    doc = json.loads(raw)

    tiny = set()
    tinyf = os.path.join(ROOT, '_tiny_covers.json')
    if os.path.exists(tinyf):
        tiny = set(json.loads(io.open(tinyf, 'rb').read()))

    todo = [m for m in doc['mods']
            if (m.get('source_url') or '').startswith('http')
            and (args.all or not (m.get('screenshots') or []) or m['id'] in tiny)]
    if args.limit:
        todo = todo[:args.limit]
    print(f'{len(todo)} entries need media from source\n', flush=True)

    stats = collections.Counter()
    for i, m in enumerate(todo, 1):
        mid = m['id']
        urls = images_in(m['source_url'])
        kept = []
        d = os.path.join(MEDIA, mid)
        for n, u in enumerate(urls[:6]):
            try:
                b = fetch(u)
            except Exception:                                     # noqa: BLE001
                continue
            if len(b) < MIN_BYTES:
                continue
            os.makedirs(d, exist_ok=True)
            ext = os.path.splitext(u.split('?')[0])[1].lower() or '.png'
            f = os.path.join(d, f'src{n}{ext}')
            io.open(f, 'wb').write(b)
            kept.append((f'media/{mid}/src{n}{ext}', len(b)))
        stats['with images' if kept else 'none found'] += 1
        print(f'[{i:3}/{len(todo)}] {mid[:44]:44} {len(kept)} image(s)'
              f'{"  " + str(max(k[1] for k in kept) // 1024) + " KB best" if kept else ""}',
              flush=True)
        if kept and args.write:
            base = ('https://cdn.jsdelivr.net/gh/TERA-Europe-Classic/'
                    'external-mod-catalog@main/')
            paths = [base + p for p, _ in kept]
            # the biggest becomes the hero when the current one is a flat swatch
            if mid in tiny:
                m['featured_image'] = paths[0]
                rest = paths[1:]
            else:
                rest = paths
            if rest:
                m['screenshots'] = rest

    print(f'\n{dict(stats)}')
    if args.write:
        io.open(os.path.join(ROOT, 'catalog.json'), 'w', encoding='utf-8',
                newline=nl).write(json.dumps(doc, indent=1, ensure_ascii=False) + '\n')
        print('catalog.json written')
    return 0


if __name__ == '__main__':
    sys.exit(main())
