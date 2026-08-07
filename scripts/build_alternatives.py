"""Link every mod to the mods that replace THE EXACT SAME THING.

`conflicts_with` is close but not this: of its edges, 1520 join entries whose
replacement targets are identical and 750 join entries that merely overlap.
Overlap is a compatibility warning. Only the identical ones are alternatives --
"the same gpk" is not the bar, "the same item, slot or object" is.

The key is semantic, not technical: item ids with their race and gender, or
character-creator slots as (kind, number, race, gender), or the named loose
target. Two entries are alternatives when those sets are equal.

Idempotent: the rendered section is delimited, so re-running replaces it rather
than stacking copies.
"""
import io
import json
import os
import sys
import collections

HERE = os.path.dirname(os.path.abspath(__file__))
CATALOG = os.path.join(HERE, '..', 'catalog.json')
# A plain heading, not an HTML comment. The launcher renders the description as
# markdown and showed the old <!-- alternatives:begin --> delimiters as literal
# text, so the section arrived with its own scaffolding on screen.
HEADING = '**Alternatives -- other mods that replace the same thing**'


def semkey(m):
    """The set of things this mod replaces, named the way a player would."""
    d = m.get('replaces_data') or {}
    toks = set()
    for t in d.get('targets') or []:
        race = (t.get('race') or 'any').lower()
        gender = (t.get('gender') or 'any').lower()
        for it in t.get('items') or []:
            toks.add('item:%s:%s:%s' % (it.get('id'), race, gender))
    for s in d.get('slots') or []:
        race = (s.get('race') or 'any').lower()
        gender = (s.get('gender') or 'any').lower()
        for n in s.get('numbers') or []:
            toks.add('slot:%s:%s:%s:%s' % ((s.get('kind') or '').lower(), n, race, gender))
    for o in d.get('objects') or []:
        p = o.get('path') if isinstance(o, dict) else o
        if p:
            toks.add('object:%s' % str(p).lower())
    for l in d.get('loose') or []:
        toks.add('loose:%s' % str(l).strip().lower())
    return frozenset(toks)


def render(mods_by_id, ids):
    lines = [HEADING, '']
    for i in sorted(ids):
        o = mods_by_id[i]
        note = ' — currently being fixed' if o.get('broken') else ''
        lines.append('- [%s](mod:%s) by %s%s' % (o['name'], i, o.get('author') or 'unknown', note))
    return '\n'.join(lines)


def strip_section(text):
    # Clears the old comment-delimited form too, so a catalog written before the
    # format change regenerates clean instead of keeping its scaffolding.
    begin, end = '<!-- alternatives:begin -->', '<!-- alternatives:end -->'
    if begin in text:
        head, _, rest = text.partition(begin)
        _, _, tail = rest.partition(end)
        text = (head.rstrip() + '\n' + tail.strip()).rstrip()
    if HEADING in text:
        text = text.partition(HEADING)[0].rstrip()
    return text.rstrip()


def main(write=True):
    j = json.loads(io.open(CATALOG, encoding='utf-8').read())
    mods = j.get('mods') if isinstance(j, dict) else j
    byid = {m['id']: m for m in mods}

    groups = collections.defaultdict(list)
    for m in mods:
        k = semkey(m)
        if k:
            groups[k].append(m['id'])

    linked = 0
    sizes = collections.Counter()
    for k, ids in groups.items():
        sizes[len(ids)] += 1
        for i in ids:
            m = byid[i]
            others = sorted(x for x in ids if x != i)
            base = strip_section(m.get('long_description') or '')
            if others:
                m['alternatives'] = others
                m['long_description'] = (base + '\n\n' + render(byid, others)).strip()
                linked += 1
            else:
                m.pop('alternatives', None)
                m['long_description'] = base
    for m in mods:
        if not semkey(m):
            m.pop('alternatives', None)
            m['long_description'] = strip_section(m.get('long_description') or '')

    if write:
        io.open(CATALOG, 'w', encoding='utf-8').write(json.dumps(j, ensure_ascii=False, indent=1))
    print('entries with a resolvable target : %d' % sum(len(v) for v in groups.values()))
    print('distinct exact-target groups     : %d' % len(groups))
    print('entries given alternatives       : %d' % linked)
    print('group sizes: %s' % dict(sorted(sizes.items())))
    return 0


if __name__ == '__main__':
    sys.exit(main(write='--dry-run' not in sys.argv))
