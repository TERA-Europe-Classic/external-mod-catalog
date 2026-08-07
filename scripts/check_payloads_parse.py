"""Guard: every published payload must actually parse as a package.

The Rainbow Monster HP Gauge shipped a 1.1 MB file whose name table was broken
("Name index 112 is outside name table"). The client loads S1UI packages early,
hit it, and fatalled nine seconds in — before the character screen. Nothing in
the catalog said so; the entry claimed to be a harmless no-op.

A malformed payload is the worst failure we ship: it takes the client down for
anyone who enables it. This downloads each payload and runs it through the same
reader the launcher uses, so a package that cannot be read is caught before a
player finds it.

    python scripts/check_payloads_parse.py                 # everything
    python scripts/check_payloads_parse.py --version 2026-05-01-x64-port
    python scripts/check_payloads_parse.py --limit 20

Downloads are cached under .payload-cache/ so re-runs are cheap. Exits non-zero
and names every payload that failed to parse.
"""
import argparse
import hashlib
import io
import json
import os
import subprocess
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, '.payload-cache')
INSPECT = (r"C:/Users/Lukas/Documents/GitHub/TERA EU Classic/tera-mod-archive"
           r"/bin/inspect-gpk-resources.exe")


def fetch(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return True
    try:
        with urllib.request.urlopen(url, timeout=180) as r, open(dest, 'wb') as f:
            f.write(r.read())
        return True
    except Exception:
        if os.path.exists(dest):
            os.remove(dest)
        return False


def parses(path):
    """First line of the reader's output; 'FAIL: ...' means the package is unreadable."""
    try:
        out = subprocess.run([INSPECT, path], capture_output=True, text=True,
                             encoding='utf-8', errors='replace', timeout=180).stdout
    except Exception as e:
        return False, f'reader crashed: {e}'
    first = (out.strip().splitlines() or ['(no output)'])[0]
    return (not first.startswith('FAIL')), first


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--version', help='only entries with this version string')
    ap.add_argument('--limit', type=int)
    args = ap.parse_args()

    with io.open(os.path.join(ROOT, 'catalog.json'), 'rb') as f:
        mods = json.loads(f.read())['mods']

    todo = [m for m in mods
            if m.get('kind') == 'gpk'
            and str(m.get('download_url', '')).startswith('http')]
    if args.version:
        todo = [m for m in todo if m.get('version') == args.version]
    if args.limit:
        todo = todo[:args.limit]

    os.makedirs(CACHE, exist_ok=True)
    bad, unreachable, ok = [], [], 0
    for n, m in enumerate(todo, 1):
        url = m['download_url']
        dest = os.path.join(CACHE, hashlib.sha1(url.encode()).hexdigest()[:16] + '.gpk')
        if not fetch(url, dest):
            unreachable.append(m['id'])
            print(f"[{n}/{len(todo)}] UNREACHABLE {m['id']}")
            continue
        good, detail = parses(dest)
        if good:
            ok += 1
        else:
            bad.append((m['id'], detail, os.path.getsize(dest)))
            print(f"[{n}/{len(todo)}] BROKEN      {m['id']}  {detail[:70]}")

    print(f"\nparsed ok {ok}   BROKEN {len(bad)}   unreachable {len(unreachable)}")
    for mid, detail, size in bad:
        print(f"  {mid}  ({size} B)  {detail}")
    json.dump({'broken': [{'id': i, 'detail': d, 'size': s} for i, d, s in bad],
               'unreachable': unreachable, 'ok': ok},
              io.open(os.path.join(ROOT, 'payload-parse-report.json'), 'w', encoding='utf-8'),
              indent=1)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
