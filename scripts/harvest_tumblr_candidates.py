"""Phase 1 of the tumblr harvest: pull what each candidate post actually says.

The audit found ~1300 posts the catalog does not account for, of which a spot
check put roughly 60% genuinely absent. Slugs alone cannot tell a mod from an
ask, and cannot tell whether a download still resolves, so this reads the post
bodies and records the three things that decide whether an entry can be built:

  - the download link, and whether it points somewhere still alive
  - the author, which on a reblog archive is the reblogged-from blog, not
    mods-of-tera
  - the photos, which are the only hero images these mods will ever have

Writes one record per post. Nothing is imported here; a post with no download
is a dead end and a post whose host is gone needs a different source.
"""
import collections
import html
import io
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
BLOG = 'https://mods-of-tera.tumblr.com'
OUT = os.path.join(HERE, '_tumblr_candidates.json')
LOG = os.path.join(HERE, 'motera_harvest.log')

HOSTS = re.compile(r'(mediafire|drive\.google|dropbox|mega\.nz|mega\.co\.nz|onedrive|1drv\.ms|'
                   r'sendspace|zippyshare|dropmefiles|gofile|pixeldrain|puu\.sh|cdn\.discordapp)', re.I)


def log(m):
    line = '[%s] %s' % (time.strftime('%H:%M:%S'), m)
    with io.open(LOG, 'a', encoding='utf-8') as f:
        f.write(line + '\n')
    print(line, flush=True)


def fetch(start):
    r = subprocess.run(['curl', '-sL', '--max-time', '60',
                        '%s/api/read?num=50&start=%d' % (BLOG, start)],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    return r.stdout or ''


def main():
    io.open(LOG, 'w').close()
    want = set()
    p = os.path.join(HERE, '_missing_from_tumblr.json')
    if os.path.exists(p):
        want = set(json.loads(io.open(p, encoding='utf-8').read()))
    log('candidates to read: %d' % len(want))

    records, start, empty = {}, 0, 0
    while start < 4000:
        body = fetch(start)
        chunks = re.split(r'(?=<post id=")', body)
        if len(chunks) <= 1:
            empty += 1
            if empty >= 2:
                break
        else:
            empty = 0
        for c in chunks:
            m = re.match(r'<post id="(\d+)"', c)
            if not m:
                continue
            pid = m.group(1)
            if want and pid not in want:
                continue
            url = re.search(r'url-with-slug="([^"]+)"', c)
            reblog = re.search(r'reblogged-root-name="([^"]+)"', c) or \
                     re.search(r'reblogged-from-name="([^"]+)"', c)
            photos = re.findall(r'<photo-url max-width="1280">([^<]+)</photo-url>', c)
            if not photos:
                photos = re.findall(r'<photo-url max-width="500">([^<]+)</photo-url>', c)
            text = html.unescape(re.sub(r'<[^>]+>', ' ', c))
            links = [html.unescape(x) for x in re.findall(r'href="([^"]+)"', c)]
            dl = [l for l in links if HOSTS.search(l)]
            records[pid] = {
                'url': url.group(1) if url else '',
                'author': reblog.group(1) if reblog else None,
                'photos': photos[:6],
                'downloads': sorted(set(dl))[:6],
                'text': ' '.join(text.split())[:600],
            }
        start += 50
        if start % 500 == 0:
            log('  read to start=%d, %d candidate records' % (start, len(records)))

    io.open(OUT, 'w', encoding='utf-8').write(json.dumps(records, ensure_ascii=False, indent=1))
    withdl = [r for r in records.values() if r['downloads']]
    withph = [r for r in records.values() if r['photos']]
    hosts = collections.Counter()
    for r in records.values():
        for d in r['downloads']:
            mm = HOSTS.search(d)
            if mm:
                hosts[mm.group(1).lower()] += 1
    log('records: %d' % len(records))
    log('  with a download link : %d' % len(withdl))
    log('  with at least a photo: %d' % len(withph))
    log('  download hosts: %s' % dict(hosts.most_common(8)))
    log('-> %s' % OUT)


if __name__ == '__main__':
    main()
