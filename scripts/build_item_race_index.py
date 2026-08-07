"""Build the item -> (race, gender) map every `replaces` string depends on.

Race and gender come from the DC, never from the item name. Every Running Togs
variant is called "Blue Running Togs" no matter who wears it, so guessing from
the name is how a tester gets sent to try the Human id on a Castanic — which
happened, twice, and both times read as a mod failure rather than bad copy.

ItemData carries requiredRace / requiredGender per id. This walks all of it and
writes the map next to the catalog so the regen scripts stop depending on a
scratch file that only ever held the 22 costumes I had done by hand.

    python scripts/build_item_race_index.py
"""
import io
import json
import os
import re
import sys

DC = (r"C:/Users/Lukas/Documents/GitHub/elinu/Client/DataCenter_Final_EUR/ItemData")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   'scripts', 'item_race_index.json')

# Attributes are unordered in the XML, so pull each by name rather than by
# position — an id-first assumption breaks on the rows that omit a field.
ITEM = re.compile(r'<Item\b([^>]*)>')
ATTR = re.compile(r'(\w+)="([^"]*)"')


def main():
    if not os.path.isdir(DC):
        print(f'DC not found: {DC}', file=sys.stderr)
        return 1
    index = {}
    files = sorted(f for f in os.listdir(DC) if f.lower().endswith('.xml'))
    for name in files:
        with io.open(os.path.join(DC, name), encoding='utf-8', errors='replace') as fh:
            body = fh.read()
        for m in ITEM.finditer(body):
            a = dict(ATTR.findall(m.group(1)))
            iid = a.get('id')
            if not iid:
                continue
            race = (a.get('requiredRace') or '').strip()
            gender = (a.get('requiredGender') or '').strip()
            # "all" means the item has no race lock; recording it as a race
            # would invent a restriction the game does not have.
            if race.lower() in ('', 'all', 'none'):
                race = ''
            if gender.lower() in ('', 'all', 'none'):
                gender = ''
            if race or gender:
                index[iid] = [race, gender]
    with io.open(OUT, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(index, ensure_ascii=False, sort_keys=True, indent=0) + '\n')
    print(f'{len(files)} ItemData files -> {len(index)} items with a race/gender lock')
    print(f'written: {OUT}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
