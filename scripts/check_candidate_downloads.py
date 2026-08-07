"""Which of the harvest candidates can still be downloaded at all.

A candidate is only worth building if its payload still exists. The links are
2016-2019 and the hosts have aged very differently: mediafire mostly answers,
mega mostly does not -- the API returns -16 (account terminated) or -9 (not
found) for almost every file link sampled.

mega needs its own check. The share URL is fragment-based, so an HTTP HEAD sees
nothing and reports a false death for every one of them; the file id has to go
to g.api.mega.co.nz instead.

Splits the candidates into recoverable and not, so the import campaign works a
real list rather than a hopeful one.
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
OUT = os.path.join(HERE, 'motera_liveness.json')
LOG = os.path.join(HERE, 'motera_liveness.log')
MEGA_FILE = re.compile(r'mega\.(?:nz|co\.nz)/#!([A-Za-z0-9_-]{8})!')
MEGA_FOLDER = re.compile(r'mega\.(?:nz|co\.nz)/#F!')


def log(m):
    line = '[%s] %s' % (time.strftime('%H:%M:%S'), m)
    with io.open(LOG, 'a', encoding='utf-8') as f:
        f.write(line + '\n')
    print(line, flush=True)


def check_mega(fid):
    try:
        p = subprocess.run(['curl', '-s', '--max-time', '15', '-H', 'Content-Type: application/json',
                            '-d', json.dumps([{"a": "g", "p": fid}]),
                            'https://g.api.mega.co.nz/cs?id=0'],
                           capture_output=True, text=True, timeout=25)
        out = (p.stdout or '').strip()
        return ('alive', out) if out.startswith('[{') and '"s"' in out else ('gone', out[:12])
    except Exception:
        return ('error', '')


def check_http(url):
    try:
        p = subprocess.run(['curl', '-sIL', '--max-time', '15', '-o', os.devnull,
                            '-w', '%{http_code}', url], capture_output=True, text=True, timeout=25)
        code = (p.stdout or '').strip()[-3:]
        return ('alive' if code in ('200', '206', '302') else 'gone'), code
    except Exception:
        return 'error', ''


def main():
    io.open(LOG, 'w').close()
    d = json.loads(io.open(os.path.join(HERE, 'motera_harvest.json'), encoding='utf-8').read())
    results, n = {}, 0
    for pid, r in d.items():
        states = []
        for u in r['downloads']:
            mm = MEGA_FILE.search(u)
            if mm:
                s, detail = check_mega(mm.group(1))
            elif MEGA_FOLDER.search(u):
                s, detail = 'unknown-folder', ''      # folder links need the folder API
            else:
                s, detail = check_http(u)
            states.append({'url': u, 'state': s, 'detail': detail})
        results[pid] = {'url': r['url'], 'author': r['author'],
                        'photos': len(r['photos']), 'links': states,
                        'recoverable': any(x['state'] == 'alive' for x in states)}
        n += 1
        if n % 50 == 0:
            ok = sum(1 for v in results.values() if v['recoverable'])
            log('  %d/%d checked, %d recoverable' % (n, len(d), ok))
            io.open(OUT, 'w', encoding='utf-8').write(json.dumps(results, ensure_ascii=False, indent=1))

    io.open(OUT, 'w', encoding='utf-8').write(json.dumps(results, ensure_ascii=False, indent=1))
    ok = [p for p, v in results.items() if v['recoverable']]
    hosts = collections.Counter()
    for v in results.values():
        for l in v['links']:
            h = re.search(r'https?://([^/]+)', l['url'])
            hosts[(h.group(1) if h else '?', l['state'])] += 1
    log('candidates checked : %d' % len(results))
    log('with a live download: %d' % len(ok))
    for (h, s), c in hosts.most_common(14):
        log('   %-26s %-14s %d' % (h[:26], s, c))
    log('-> %s' % OUT)


if __name__ == '__main__':
    main()
