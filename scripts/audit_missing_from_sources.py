"""Criterion 10: find mods that exist at a source but are absent from the catalog.

Run it to re-check the sources; it is a discovery pass, not a fixer.

Matching on source_url alone is wrong. Most GitHub-hosted mods here are
catalogued under the author's tumblr post instead, so a URL diff reports every
one of them as missing -- 11 of 19 hits on the first run were that false
positive. Repo names are matched against catalog names and ids as well, with a
fuzzy pass for the near misses ("Pika-Raincoat-" vs "pikachu-raincoat").

A repo counts as a mod only if its tree carries a .gpk. That drops tools and
Toolbox modules, which otherwise dominate: of 533 unaccounted repos, 514 had no
payload at all.

TCC (tera-custom-cooldowns and its release repos) ships .gpk fonts but is a
cooldown tracker, not a cosmetic mod, and is out of scope by campaign rule.
"""
import difflib
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CATALOG = os.path.join(HERE, '..', 'catalog.json')
SKIP_REPO = re.compile(r'^tcc|custom-cooldowns', re.I)


def sh(args, timeout=60):
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        return r.stdout if r.returncode == 0 else ''
    except Exception:
        return ''


def norm(s):
    return re.sub(r'[^a-z0-9]', '', (s or '').lower())


def main():
    j = json.loads(io.open(CATALOG, encoding='utf-8').read())
    mods = j.get('mods') if isinstance(j, dict) else j
    names = {norm(m['name']): m['id'] for m in mods}
    ids = {norm(m['id'].split('.', 1)[-1]): m['id'] for m in mods}
    known = set(names) | set(ids)

    owners = sorted({re.match(r'https?://github\.com/([^/]+)', (m.get('source_url') or '').lower()).group(1)
                     for m in mods
                     if re.match(r'https?://github\.com/([^/]+)', (m.get('source_url') or '').lower())})
    print('github owners in the catalog: %d' % len(owners))

    missing, checked, payloadless = [], 0, 0
    for o in owners:
        repos = [x.strip() for x in
                 sh(['gh', 'api', '--paginate', 'users/%s/repos?per_page=100' % o, '--jq', '.[].name']).splitlines()
                 if x.strip()]
        for r in repos:
            if SKIP_REPO.match(r):
                continue
            key = norm(r)
            if key in known or difflib.get_close_matches(key, known, n=1, cutoff=0.86):
                continue
            checked += 1
            tree = sh(['gh', 'api', 'repos/%s/%s/git/trees/HEAD?recursive=1' % (o, r),
                       '--jq', '.tree[]? | select(.type=="blob") | .path'])
            gpks = [p for p in tree.splitlines() if p.lower().endswith('.gpk')]
            if not gpks:
                payloadless += 1
                continue
            missing.append({'owner': o, 'repo': r, 'gpks': gpks,
                            'url': 'https://github.com/%s/%s' % (o, r)})
            print('  MISSING  %-24s %-44s %d gpk' % (o, r[:44], len(gpks)))

    out = os.path.join(HERE, '_missing_from_sources.json')
    io.open(out, 'w', encoding='utf-8').write(json.dumps(missing, ensure_ascii=False, indent=1))
    print('\nunmatched repos inspected : %d' % checked)
    print('of those, no .gpk payload : %d' % payloadless)
    print('genuinely missing mods    : %d  -> %s' % (len(missing), out))
    return 0


if __name__ == '__main__':
    sys.exit(main())
