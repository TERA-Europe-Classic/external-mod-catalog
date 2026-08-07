"""Criterion 10 for mods-of-tera, the source behind most of the catalog.

370 of the 647 entries come from this blog and it had never been diffed. The
earlier source audit covered only the 13 GitHub owners, which is 144 entries.

The blog's /archive page is a JS shell with no post ids in the HTML, but the
legacy /api/read endpoint still paginates 50 at a time without a key.

Matching is by post id first, then by slug, because mods-of-tera is a reblog
archive: the same mod is often catalogued under the original author's own blog,
so a post id we do not cite is not automatically a mod we do not have. Catalog
ids are slug-derived, which makes the slug comparison reliable.

Output is a candidate list to read, never to import blindly -- the blog also
carries asks, announcements, slider posts and screenshots.
"""
import collections
import io
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CATALOG = os.path.join(HERE, '..', 'catalog.json')
OUT = os.path.join(HERE, '_missing_from_tumblr.json')
BLOG = 'https://mods-of-tera.tumblr.com'

MOD = re.compile(r'\bmod|recolou?r|replaces?|retexture|download|dyeable|skin\b', re.I)
NONMOD = re.compile(r'\bask|announce|faq|rules|question|hiatus|masterlist|slider|giveaway|contest|psa\b', re.I)


def norm(s):
    return re.sub(r'[^a-z0-9]', '', (s or '').lower())


def fetch(start):
    r = subprocess.run(['curl', '-sL', '--max-time', '45',
                        '%s/api/read?num=50&start=%d' % (BLOG, start)],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    return r.stdout or ''


def main():
    cat = json.loads(io.open(CATALOG, encoding='utf-8').read())
    mods = cat.get('mods') if isinstance(cat, dict) else cat
    have_ids = set()
    for m in mods:
        mm = re.search(r'/post/(\d+)', m.get('source_url') or '')
        if mm:
            have_ids.add(mm.group(1))
    keys = {}
    for m in mods:
        keys[norm(m['id'].split('.', 1)[-1])] = m['id']
        keys[norm(m['name'])] = m['id']

    posts, start, empty = {}, 0, 0
    while start < 4000:
        body = fetch(start)
        found = re.findall(r'<post id="(\d+)"[^>]*url-with-slug="([^"]+)"', body)
        if not found:
            empty += 1
            if empty >= 2:
                break
        else:
            empty = 0
            posts.update(dict(found))
        start += 50

    unmatched, buckets = {}, collections.Counter()
    for pid, url in posts.items():
        if pid in have_ids:
            continue
        slug = url.rstrip('/').split('/')[-1] if url else ''
        n = norm(slug)
        hit = keys.get(n)
        if not hit and len(n) >= 18:
            for k, v in keys.items():
                if k.startswith(n[:24]) or n.startswith(k[:24]):
                    hit = v
                    break
        if hit:
            continue
        words = slug.replace('-', ' ')
        kind = ('non-mod' if NONMOD.search(words)
                else 'mod-like' if MOD.search(words) else 'unclear')
        buckets[kind] += 1
        unmatched.setdefault(kind, {})[pid] = url

    io.open(OUT, 'w', encoding='utf-8').write(json.dumps(
        {'blog_posts': len(posts), 'cited_by_post_id': len(have_ids),
         'unmatched': unmatched}, ensure_ascii=False, indent=1))
    print('posts on the blog            : %d' % len(posts))
    print('cited by a catalog entry     : %d' % len(have_ids))
    print('unmatched after slug matching: %d' % sum(buckets.values()))
    for k, v in buckets.most_common():
        print('   %-10s %4d' % (k, v))
    print('-> %s' % OUT)
    return 0


if __name__ == '__main__':
    sys.exit(main())
