"""Every entry, every criterion, in one report.

The ten criteria were being tracked in three different places -- some enforced
by validate_catalog, some measured ad hoc, some only in commit messages -- so
"where does the catalog actually stand?" had no single answer. This gives one.

Each criterion is either MET, MET WITH A RECORDED REASON (a documented
exception, which the gate already demands), or OPEN. Anything OPEN is listed
with its ids so the next pass has a worklist rather than a number.

Reports, does not fix. Fixing belongs in the targeted scripts beside this one.
"""
import collections
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CATALOG = os.path.join(HERE, '..', 'catalog.json')
OUT = os.path.join(HERE, '..', 'AUDIT.md')


def load(name, default):
    p = os.path.join(HERE, name)
    if not os.path.exists(p):
        return default
    return json.loads(io.open(p, encoding='utf-8').read())


def main():
    j = json.loads(io.open(CATALOG, encoding='utf-8').read())
    mods = j.get('mods') if isinstance(j, dict) else j
    no_media = load('_no_media.json', {})
    total = len(mods)

    def ids(rows):
        return sorted(m['id'] for m in rows)

    # 1 title + hero
    no_title = [m for m in mods if not (m.get('name') or '').strip()]
    no_hero = [m for m in mods if not m.get('featured_image')]
    hero_excused = [m for m in no_hero if m['id'] in no_media]
    hero_open = [m for m in no_hero if m['id'] not in no_media]

    # 2 subtitle: present, uniform shape, and an item-replacing mod names ids
    no_sub = [m for m in mods if not (m.get('short_description') or '').strip()]
    bad_shape = [m for m in mods if (m.get('short_description') or '') and
                 (not m['short_description'][0].isupper()
                  or not m['short_description'].rstrip().endswith('.')
                  or len(m['short_description']) > 90)]
    # ids live as JSON numbers on targets[].items[].id, not as "#1234" text --
    # searching the rendered string reported 255 false failures.
    def items_of(m):
        return [it for t in ((m.get('replaces_data') or {}).get('targets') or [])
                for it in (t.get('items') or [])]
    item_no_id = [m for m in mods
                  if items_of(m) and any(not str(it.get('id') or '').isdigit() for it in items_of(m))]
    # and the rendered subtitle/replaces should actually surface those ids
    item_not_rendered = [m for m in mods
                         if items_of(m) and not re.search(r'#\d{4,}', m.get('replaces') or '')]

    # 3 description present and not a stub
    no_desc = [m for m in mods if not (m.get('long_description') or '').strip()]
    thin = [m for m in mods if 0 < len(m.get('long_description') or '') < 120]
    scaffold = [m for m in mods if '<!--' in (m.get('long_description') or '')]

    # 4 media
    no_shots = [m for m in mods if not m.get('screenshots')]
    shots_excused = [m for m in no_shots if m['id'] in no_media]
    shots_open = [m for m in no_shots if m['id'] not in no_media]
    shots_no_blur = [m for m in mods if m.get('screenshots') and not m.get('blur_data')]

    # 5 collections: a collection of one is a tagging error
    members = collections.defaultdict(list)
    for m in mods:
        if m.get('collection'):
            members[m['collection']].append(m['id'])
    lonely = {c: v for c, v in members.items() if len(v) == 1}

    # 6 alternatives: derived, so the check is drift against the derivation
    import build_alternatives
    groups = collections.defaultdict(list)
    for m in mods:
        k = build_alternatives.semkey(m)
        if k:
            groups[k].append(m['id'])
    want = {}
    for g in groups.values():
        for i in g:
            want[i] = sorted(x for x in g if x != i)
    alt_drift = [m for m in mods
                 if sorted(m.get('alternatives') or []) != (want.get(m['id']) or [])]
    linked = [m for m in mods if m.get('alternatives')]
    ungrouped = [m for m in mods if not build_alternatives.semkey(m)]

    # 7 functional
    broken = [m for m in mods if (m.get('broken') or '').strip()]
    verified = [m for m in mods if m.get('last_verified')]
    no_payload = [m for m in mods
                  if not (m.get('broken') or '').strip()
                  and not (m.get('parts') or m.get('download_url'))]
    ready = [m for m in mods if not (m.get('broken') or '').strip()
             and (m.get('parts') or m.get('download_url'))]

    rows = [
        ('1  title present', total - len(no_title), 0, ids(no_title)),
        ('1  hero image', total - len(no_hero), len(hero_excused), ids(hero_open)),
        ('2  subtitle present', total - len(no_sub), 0, ids(no_sub)),
        ('2  subtitle uniform', total - len(bad_shape), 0, ids(bad_shape)),
        ('2  item ids valid', total - len(item_no_id), 0, ids(item_no_id)),
        ('2  item ids shown to player', total - len(item_not_rendered), 0, ids(item_not_rendered)),
        ('3  description present', total - len(no_desc), 0, ids(no_desc)),
        ('3  no render scaffolding', total - len(scaffold), 0, ids(scaffold)),
        ('3  description not a stub', total - len(thin), 0, ids(thin)),
        ('4  screenshots', total - len(no_shots), len(shots_excused), ids(shots_open)),
        ('4  blur placeholders', total - len(shots_no_blur), 0, ids(shots_no_blur)),
        ('5  no single-member collection', total - len(lonely), 0, sorted(lonely)),
        ('6  alternatives current', total - len(alt_drift), 0, ids(alt_drift)),
        ('7  has a payload', total - len(no_payload), 0, ids(no_payload)),
        ('7  not flagged broken', total - len(broken), 0, []),
        ('7  verified in game', len(verified), 0, []),
    ]

    out = ['# Catalog audit', '',
           'Generated by `scripts/audit_all_criteria.py`. Every entry, every criterion.',
           '', '| Criterion | Met | Excused | Open |', '|---|---:|---:|---:|']
    for name, met, excused, open_ids in rows:
        out.append('| %s | %d/%d | %d | %d |' % (name, met, total, excused, len(open_ids)))
    out += ['', '## Open items', '']
    any_open = False
    for name, met, excused, open_ids in rows:
        if open_ids:
            any_open = True
            out.append('**%s** (%d)' % (name, len(open_ids)))
            out.append('')
            for i in open_ids[:40]:
                out.append('- `%s`' % i)
            if len(open_ids) > 40:
                out.append('- ... and %d more' % (len(open_ids) - 40))
            out.append('')
    if not any_open:
        out.append('None.')
    out += ['', '## Criterion 7 detail', '',
            '- verified in game: **%d**' % len(verified),
            '- ready to test: **%d**' % len(ready),
            '- flagged with a diagnosis: **%d**' % len(broken),
            '- entries with no semantic target, so no alternatives apply: **%d**' % len(ungrouped),
            '- entries carrying alternatives: **%d**' % len(linked), '']

    io.open(OUT, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    for name, met, excused, open_ids in rows:
        print('%-32s %4d/%d met, %3d excused, %3d open' % (name, met, total, excused, len(open_ids)))
    print('\n-> %s' % OUT)
    return 0


if __name__ == '__main__':
    sys.exit(main())
