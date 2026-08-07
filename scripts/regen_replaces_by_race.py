"""Rewrite long `replaces` item lists as race-grouped, collapsed ranges.

The old copy was a wall of bare ids with the outfit name repeated after itself:

  "Blue Running Togs: Blue Running Togs (#60581, #60582, #60611, ... x36)"

Nobody could tell which id their character can wear — not the player, and not me:
I sent a tester to try Castanic Sleepy Running Togs with #60581, which is the
HUMAN female item, and the wasted run looked like a mod failure (2026-07-27).

Race and gender come from the DC, never from the item name — every Running Togs
variant is called "Blue Running Togs" regardless of who wears it. ItemData carries
requiredRace/requiredGender per id; scratchpad/item_race_index.json is that map.

    python scripts/regen_replaces_by_race.py --dry-run
    python scripts/regen_replaces_by_race.py
"""
import argparse
import io
import json
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import catalog_io

INDEX = (r"C:/Users/Lukas/AppData/Local/Temp/claude"
         r"/C--Users-Lukas-Documents-GitHub-GPK-RePack"
         r"/c1d99a35-c7a4-45d1-b04e-782f20971475/scratchpad/item_race_index.json")

RACE_LABEL = {
    'human': 'Human', 'highelf': 'High Elf', 'highElf': 'High Elf',
    'aman': 'Aman', 'castanic': 'Castanic', 'popori': 'Elin', 'baraka': 'Baraka',
}


def label(race, gender):
    """Elin is the Popori female; the game never calls her 'Popori Female'."""
    r = RACE_LABEL.get(race, race.title() if race else 'Unknown')
    if race.lower() == 'popori':
        return 'Elin' if gender == 'female' else 'Popori Male'
    return f"{r} {gender.title()}" if gender else r


def ranges(ids):
    """[1,2,3,7] -> '#1-#3, #7' — a wall of ids is unreadable, runs are not."""
    ids = sorted(set(int(i) for i in ids))
    out, start, prev = [], None, None
    for i in ids:
        if start is None:
            start = prev = i
        elif i == prev + 1:
            prev = i
        else:
            out.append(f"#{start}" if start == prev else f"#{start}-#{prev}")
            start = prev = i
    if start is not None:
        out.append(f"#{start}" if start == prev else f"#{start}-#{prev}")
    return ', '.join(out)


def regroup(text, index):
    ids = re.findall(r'#(\d+)', text or '')
    if len(ids) < 8:
        return None                      # short lists already read fine
    by = {}
    for i in ids:
        race, gender = index.get(i, ('', ''))
        by.setdefault(label(race, gender), []).append(i)
    if len(by) < 2:
        return None
    order = ['Human Female', 'High Elf Female', 'Aman Female', 'Castanic Female',
             'Elin', 'Human Male', 'High Elf Male', 'Aman Male', 'Castanic Male',
             'Popori Male', 'Baraka Male']
    keys = [k for k in order if k in by] + sorted(k for k in by if k not in order)
    parts = [f"{k} {ranges(by[k])}" for k in keys]
    return ("Ships a full replacement of this costume set, so any of these can be "
            "affected. Wearable by — " + '; '.join(parts) + '.')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    index = {k: tuple(v) for k, v in json.load(io.open(INDEX, encoding='utf-8')).items()}
    cat = catalog_io.load()
    changed = []
    for m in cat['mods']:
        new = regroup(m.get('replaces'), index)
        if new and new != m.get('replaces'):
            changed.append((m['id'], len(m.get('replaces') or ''), len(new)))
            if not args.dry_run:
                m['replaces'] = new
    print(f"{len(changed)} entries regrouped")
    for mid, a, b in changed[:10]:
        print(f"  {mid[:46]:48s} {a:5d} -> {b:4d} chars")
    if not args.dry_run and changed:
        cat['version'] += 1
        catalog_io.save(cat)
        print(f"catalog v{cat['version']}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
