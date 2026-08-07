"""Build id -> {name, race, gender} for every item in the client datacenter.

`replaces` has to read "Thunor's Armor (Elin) (#271132)" -- name, race, id, one
line per item. That needs all three facts per id, and the only honest source is
the datacenter:

    Client/DataCenter_Final_EUR/StrSheet_Item/  -> id -> display name
    Client/DataCenter_Final_EUR/ItemData/       -> id -> requiredRace/Gender

Guessing any of it from a package name is how two mods got described as
replacing the wrong costume. See the dc-item-resolver note.

    python scripts/build_item_index.py [--dc <path>]

Writes scripts/item_index.json.
"""
import argparse
import collections
import glob
import html
import io
import json
import os
import re
import sys

DEFAULT_DC = r'C:\Users\Lukas\Documents\GitHub\elinu'

# The datacenter says popori/female for what every player calls an Elin.
RACE_LABEL = {
    'human': 'Human', 'highelf': 'High Elf', 'aman': 'Aman',
    'castanic': 'Castanic', 'popori': 'Elin', 'elin': 'Elin',
    'baraka': 'Baraka',
}

ITEM_RE = re.compile(r'<Item\b[^>]*\bid="(\d+)"[^>]*>')
ATTR_RE = re.compile(r'\b(requiredRace|requiredGender)="([^"]*)"')
STR_RE = re.compile(r'<String\b[^>]*\bid="(\d+)"[^>]*\bstring="([^"]*)"')


def scan_names(dc):
    out = {}
    pats = [os.path.join(dc, 'Client', 'DataCenter_Final_EUR', 'StrSheet_Item', '*.xml'),
            os.path.join(dc, 'Client', 'DataCenter_Final_EUR', 'StrSheet_Item*', '*.xml')]
    files = sorted({f for p in pats for f in glob.glob(p)})
    for f in files:
        t = io.open(f, encoding='utf-8', errors='ignore').read()
        for mid, name in STR_RE.findall(t):
            # The datacenter stores display names as XML, so "Ancient & Modern"
            # is on disk as "Ancient &amp; Modern". Indexing the raw attribute
            # put the escaped form into `replaces` and the gate then failed
            # every entry naming one of those items against itself.
            name = html.unescape(name)
            if name and mid not in out:
                out[mid] = name
    return out, len(files)


def scan_items(dc):
    out = {}
    files = sorted(set(
        glob.glob(os.path.join(dc, 'Client', 'DataCenter_Final_EUR', 'ItemData', '*.xml')) +
        glob.glob(os.path.join(dc, 'Server', 'Datasheet', 'ItemData', '*.xml'))))
    for f in files:
        t = io.open(f, encoding='utf-8', errors='ignore').read()
        for m in ITEM_RE.finditer(t):
            iid = m.group(1)
            if iid in out:
                continue
            attrs = dict(ATTR_RE.findall(m.group(0)))
            out[iid] = (attrs.get('requiredRace', ''), attrs.get('requiredGender', ''))
    return out, len(files)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dc', default=DEFAULT_DC)
    args = ap.parse_args()
    if not os.path.isdir(args.dc):
        print(f'datacenter not found: {args.dc}', file=sys.stderr)
        return 1

    names, nf = scan_names(args.dc)
    items, itf = scan_items(args.dc)
    print(f'{len(names):,} names from {nf} StrSheet files')
    print(f'{len(items):,} items from {itf} ItemData files')

    index = {}
    for iid, (race, gender) in items.items():
        r = race.lower()
        index[iid] = {
            'name': names.get(iid, ''),
            'race': 'elin' if r == 'popori' else (r or 'any'),
            'gender': (gender or 'any').lower(),
        }
    # ids that have a name but no ItemData row still deserve to resolve
    for iid, name in names.items():
        index.setdefault(iid, {'name': name, 'race': 'any', 'gender': 'any'})

    named = sum(1 for v in index.values() if v['name'])
    print(f'{len(index):,} ids indexed, {named:,} with a display name')
    by_race = collections.Counter(v['race'] for v in index.values())
    print('  by race:', dict(by_race.most_common(8)))

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dest = os.path.join(root, 'scripts', 'item_index.json')
    io.open(dest, 'w', encoding='utf-8').write(json.dumps(index, ensure_ascii=False))
    print(f'wrote {dest} ({os.path.getsize(dest):,} B)')
    for probe in ('271132', '271139', '185412', '60651'):
        print(f'   #{probe}: {index.get(probe)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
