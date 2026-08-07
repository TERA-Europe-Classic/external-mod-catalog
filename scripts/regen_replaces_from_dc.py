"""Give every whole-package wearable a `replaces` a player can act on.

61 of 584 entries carried item ids. The rest said things like "Turns the Red
Running Togs pastel pink" — nothing you can search your inventory for, which
is the entire point of the field.

The DC's asset index is keyed by the BARE PACKAGE NAME as well as by full
object paths, so `PC_Event_03` resolves to every part, and every item, that
renders out of it. No payload downloads needed.

A FALSE ALARM WORTH RECORDING. The first pass looked like it produced garbage:
PC_Event_48 came back with 22 "distinct" item names for a mod claiming one
outfit. It was a misread — those were the same costumes suffixed per race, and
TERA gives the male and female cuts DIFFERENT names. Strip the suffix and
PC_Event_48 is two costumes, not twenty-two:

    PC_Event_48  Wrestling Costume (male) / Sheriff Uniform (female)  + dyeables
    PC_Event_23A Clover-green Kobold Tailcoat / Dress
    PC_Event_49  Shearling Flying Jacket / Carmine Winter Dress       + dyeables
    PC_Event_03  Running Togs, Team Captain, Volleyball (blue + red)

So the resolution is sound, and it CORRECTS existing prose: the entry claiming
"Sugar Alice" ships PC_Event_23A, which holds no Sugar Alice at all.

Scope, deliberately narrow:
 - only `dropin` / `tmm`, which replace the whole package, so every item that
   renders from it really is affected
 - never entries whose copy already names a race — "the Aman female Santa suit"
   is more precise than any package-level answer, and overwriting it loses
   information. Those go to replaces_needs_object_level.json.

    python scripts/regen_replaces_from_dc.py --dry-run
    python scripts/regen_replaces_from_dc.py --write
"""
import argparse
import collections
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RESOLVER = (r"C:/Users/Lukas/Documents/GitHub/TERA EU Classic"
            r"/tera-mod-archive/dc_resolver.json")
RACE_INDEX = os.path.join(HERE, 'item_race_index.json')

# Whole-package strategies: the mod ships a replacement for the entire
# package, so every item rendering from it is genuinely affected.
WHOLE_PACKAGE = {'dropin', 'tmm'}
WEARABLE = {'Costumes', 'Accessories', 'Mounts & Pets', 'Weapon Skins', 'Hair'}

# A package resolves to every item that renders from it, across all races.
# That is the superset of what COULD be affected, not what the mod changes:
# a dropin swaps the whole .gpk, but the author usually retextured one race's
# variant and left the rest vanilla.
#
# So when the existing copy already names a race or gender, it is more precise
# than anything package-level resolution can produce, and overwriting it loses
# information. `zynnobia.santa-suit-recolor-for-aman-female` said "Replaces the
# Aman female Santa suit"; the resolved version listed all eleven races. Those
# entries need object-level targets, and are reported rather than rewritten.
# The trailing s? matters more than it looks. Without it "Recolors the dress
# for Castanics" did not read as race-naming copy, so the guard let it through
# and package-level resolution would have rewritten a Castanic-only mod to lead
# with Human Female -- the exact error that had Castanic Sleepy Running Togs
# claiming 153 ids across five races when only the Castanic was ever modified.
RACE_WORDS = re.compile(
    r'\b(elins?|poporis?|castanics?|amans?|high[\s-]?elves|high[\s-]?elfs?'
    r'|humans?|barakas?)\b', re.I)

RACE_LABEL = {'human': 'Human', 'highelf': 'High Elf', 'highElf': 'High Elf',
              'aman': 'Aman', 'castanic': 'Castanic', 'popori': 'Elin',
              'baraka': 'Baraka'}
ORDER = ['Human Female', 'High Elf Female', 'Aman Female', 'Castanic Female',
         'Elin', 'Human Male', 'High Elf Male', 'Aman Male', 'Castanic Male',
         'Popori Male', 'Baraka Male', 'Any race']


def label(race, gender):
    """Elin is the Popori female; the game never calls her 'Popori Female'."""
    if not race:
        return 'Any race'
    if race.lower() == 'popori':
        return 'Elin' if gender == 'female' else 'Popori Male'
    r = RACE_LABEL.get(race, race.title())
    return f'{r} {gender.title()}' if gender else r


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
            out.append(f'#{start}' if start == prev else f'#{start}-#{prev}')
            start = prev = i
    if start is not None:
        out.append(f'#{start}' if start == prev else f'#{start}-#{prev}')
    return ', '.join(out)


# Build and port suffixes that ride along on a shipped filename. The DC is
# keyed by the BARE package name, so `PC_Event_73_dup.gpk` never matched and
# 19 costumes were filed under "no items in the DC" when the DC knew them
# perfectly well. Both the suffixed and bare forms are returned, because a
# handful of packages genuinely end in a digit run.
FILENAME_SUFFIX = re.compile(r'(_dup|\.patched|\.castanic|_r\d+|_x64|_v\d+)+$', re.I)


def packages(entry):
    """Package names this entry ships, top level plus parts."""
    out = []
    for owner in [entry] + (entry.get('parts') or []):
        for g in owner.get('gpk_files') or []:
            name = re.sub(r'\.gpk$', '', g, flags=re.I)
            out.append(name)
            bare = FILENAME_SUFFIX.sub('', name)
            if bare != name:
                out.append(bare)
    return out


def strategies(entry):
    s = {entry.get('deploy_strategy')}
    s |= {p.get('deploy_strategy') for p in (entry.get('parts') or [])}
    return {x for x in s if x}


def resolve_items(names, a2p, l2i):
    """(id, name) for every item reachable from these package/object names."""
    items = {}
    for n in names:
        for part in a2p.get(n) or []:
            for it in l2i.get(part) or []:
                iid, iname = (it if isinstance(it, (list, tuple)) else (it, ''))
                items[str(iid)] = iname
    return items


def compose(entry, items, race_index):
    """The standard sentence: which costumes, then who can wear which ids."""
    by = collections.defaultdict(list)
    for iid in items:
        race, gender = race_index.get(iid, ['', ''])
        by[label(race, gender)].append(iid)
    keys = [k for k in ORDER if k in by] + sorted(k for k in by if k not in ORDER)
    groups = '; '.join(f'{k} {ranges(by[k])}' for k in keys)

    # Male and female cuts of one costume carry different names, each suffixed
    # with "(Race Gender)". Strip the suffix or a two-costume package reads as
    # twenty-two.
    sets = sorted({re.sub(r'\s*\([^)]*\)\s*$', '', n) for n in items.values() if n})
    # Dyeable twins are the same costume with a dye channel; fold them in.
    base = sorted({re.sub(r'^Dyeable\s+', '', n) for n in sets})
    if len(base) == 1:
        lead = f'Replaces {base[0]}'
    elif len(base) <= 4:
        lead = 'Replaces ' + ', '.join(base[:-1]) + f' and {base[-1]}'
    else:
        lead = ('Ships a full replacement of this package, so any of these '
                'can be affected')
    if any(n.startswith('Dyeable') for n in sets):
        lead += ', dyeable versions included'
    return f'{lead}. Wearable by — {groups}.'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--write', action='store_true',
                    help='actually rewrite replaces — see the module docstring '
                         'first, package-level output is not precise enough')
    ap.add_argument('--limit', type=int, default=0)
    args = ap.parse_args()

    res = json.load(io.open(RESOLVER, encoding='utf-8'))
    a2p, l2i = res['asset2parts'], res['look2items']
    a2p = {k: v for k, v in a2p.items()}
    race_index = json.load(io.open(RACE_INDEX, encoding='utf-8'))

    path = os.path.join(ROOT, 'catalog.json')
    raw = io.open(path, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in raw else '\n'
    doc = json.loads(raw, object_pairs_hook=collections.OrderedDict)

    stats = collections.Counter()
    changed = []
    needs_object = []
    for m in doc['mods']:
        if m.get('category') not in WEARABLE:
            stats['skipped: not a wearable'] += 1
            continue
        if re.search(r'#\d{4,}', m.get('replaces') or ''):
            stats['skipped: already has ids'] += 1
            continue
        if not (strategies(m) & WHOLE_PACKAGE):
            stats['skipped: not a whole-package deploy'] += 1
            continue
        # Read the id and name too, not just `replaces`. A mod called
        # "elin-aesthetics" or "recoloured-dress-for-castanics" is telling you
        # which race it touches even when the replaces line does not, and
        # package-level resolution would overwrite that with a five-race
        # superset led by Human Female. Running Togs shipped exactly that
        # error -- 153 ids across five races for a mod where only the Castanic
        # was ever modified. The narrower claim is the true one; keep it.
        if RACE_WORDS.search(' '.join(filter(None, (
                m.get('replaces'), m.get('name'), m.get('id')))).replace('-', ' ')):
            stats['kept: existing copy names a race (needs object-level)'] += 1
            needs_object.append(m['id'])
            continue
        pkgs = packages(m)
        if not pkgs:
            stats['skipped: no package named'] += 1
            continue
        items = resolve_items(pkgs, a2p, l2i)
        if not items:
            stats['no items in the DC for that package'] += 1
            continue
        text = compose(m, items, race_index)
        changed.append((m['id'], len(items), m.get('replaces') or '', text))
        if args.write:
            m['replaces'] = text
        stats['RESOLVED'] += 1
        if args.limit and len(changed) >= args.limit:
            break

    for k, v in stats.most_common():
        print(f'  {v:5}  {k}')
    print(f'\n{len(changed)} entries would change' if args.dry_run
          else f'\n{len(changed)} entries updated')
    for mid, n, old, new in changed[:5]:
        print(f'\n--- {mid}  ({n} items)\n  was: {old[:90]}\n  now: {new[:220]}')

    if needs_object:
        out_path = os.path.join(HERE, 'replaces_needs_object_level.json')
        with io.open(out_path, 'w', encoding='utf-8') as fh:
            fh.write(json.dumps(sorted(needs_object), ensure_ascii=False, indent=1))
            fh.write(chr(10))
        print('')
        print(str(len(needs_object)) + ' entries need object-level targets -> ' + out_path)

    if args.write and changed:
        doc['version'] += 1
        io.open(path, 'w', encoding='utf-8', newline=nl).write(
            json.dumps(doc, ensure_ascii=False, indent=1) + '\n')
        print(f'\ncatalog v{doc["version"]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
