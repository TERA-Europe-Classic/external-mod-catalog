# -*- coding: utf-8 -*-
"""#9 — rehost external mod images as optimized webp under media/, on our CDN.

For every mod whose featured_image is NOT already a webp on our jsDelivr media
path, download it, produce cover.webp (<=900px) + thumb.webp (<=288px) +
blur_data, write them under media/<id>/, and repoint featured_image / icon_url
at the CDN. Dead / unfetchable URLs are recorded and left untouched.

Idempotent: entries already on media/*.webp are skipped, so it can be re-run.
"""
import sys, os, io, base64, json, urllib.request, ssl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import catalog_io as C
from PIL import Image

ROOT = C.ROOT
CDN = 'https://cdn.jsdelivr.net/gh/TERA-Europe-Classic/external-mod-catalog@main/media'
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 catalog-rehost'})
    with urllib.request.urlopen(req, timeout=25, context=CTX) as r:
        return r.read()

def webp(img, q, m=6):
    b = io.BytesIO(); img.save(b, 'WEBP', quality=q, method=m); return b.getvalue()

def fit(img, mx):
    w, h = img.size; s = min(1.0, mx / max(w, h))
    return img.resize((max(1, round(w*s)), max(1, round(h*s))), Image.LANCZOS) if s < 1 else img

def is_ours(u):
    return isinstance(u, str) and 'external-mod-catalog@main/media' in u and u.endswith('.webp')

def main():
    d = C.load()
    done = skipped = dead = 0
    deadlist = []
    for m in d['mods']:
        fi = m.get('featured_image') or ''
        if not fi or is_ours(fi):
            skipped += 1
            continue
        mid = m['id']
        try:
            img = Image.open(io.BytesIO(fetch(fi))).convert('RGB')
        except Exception as e:
            dead += 1; deadlist.append([mid, fi, 'ERR', str(e)]); continue
        out = os.path.join(ROOT, 'media', mid)
        os.makedirs(out, exist_ok=True)
        with open(os.path.join(out, 'cover.webp'), 'wb') as f:
            f.write(webp(fit(img.copy(), 900), 84))
        with open(os.path.join(out, 'thumb.webp'), 'wb') as f:
            f.write(webp(fit(img.copy(), 288), 82))
        blur = base64.b64encode(webp(fit(img.copy(), 16), 40)).decode()
        m['featured_image'] = f'{CDN}/{mid}/cover.webp'
        if not is_ours(m.get('icon_url', '')):
            m['icon_url'] = f'{CDN}/{mid}/thumb.webp'
        m['blur_data'] = 'data:image/webp;base64,' + blur
        done += 1
        if done % 25 == 0:
            print(f'  rehosted {done}...', flush=True)
    if deadlist:
        with open(os.path.join(ROOT, 'media', '_dead_urls.json'), 'w', encoding='utf-8') as f:
            json.dump(deadlist, f, indent=1)
    d['version'] += 1
    C.save(d)
    print(f'DONE rehosted={done} skipped={skipped} dead={dead} version={d["version"]}')

if __name__ == '__main__':
    main()
