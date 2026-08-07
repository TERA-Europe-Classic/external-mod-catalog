"""Map asset packages to items via the item ICON, which names the package.

This is the join that Accessory.id / linkCustomizingId / partsId all failed to
provide. Items reference their asset package directly in the icon attribute:

    <Item id="115594" name="premium_hair" icon="Icon_Equipments.Acc_206_Tex" .../>
                                                              ^^^^^^^
    -> Acc_206 is granted by item 115594

Found by grepping the whole datacenter for a package name recovered from a mod
payload, rather than guessing table names -- three tables were ruled out by
guessing first (CustomizingItems, AccCustomizeData, EquipmentLookInfoData) and
none of them held the link.

Works for any package family the icons name: Acc_*, Vehicle_*, PC_Weapons_*.

Writes scripts/icon_index.json: "Acc_206" -> [item ids].
"""
import argparse
import collections
import glob
import io
import json
import os
import re
import sys

DEFAULT_DC = r'C:\Users\Lukas\Documents\GitHub\elinu'
# icon="Icon_Equipments.Acc_206_Tex" -> Acc_206
ITEM_RE = re.compile(r'<Item\b[^>]*\bid="(\d+)"[^>]*\bicon="([^"]*)"')
ITEM_RE2 = re.compile(r'<Item\b[^>]*\bicon="([^"]*)"[^>]*\bid="(\d+)"')
# Greedy enough to keep the whole package name. `PC_Weapons?_\w+?` was
# non-greedy and stopped at the first character, so every weapon icon
# (Icon_Equipments.PC_Weapons_Event04_Dual_Tex) missed. Both the full name and
# the family stem are indexed, since mods target either.
PKG_RE = re.compile(
    r'\.((?:Acc_\d+|Vehicle_[A-Za-z0-9]+|PC_Weapons?_[A-Za-z0-9]+|PC_Event_\d+[A-Z]?))')
STEM_RE = re.compile(r'^(PC_Weapons?_[A-Za-z]+?)\d*$')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dc', default=DEFAULT_DC)
    args = ap.parse_args()
    out = collections.defaultdict(set)
    files = sorted(set(
        glob.glob(os.path.join(args.dc, 'Client', 'DataCenter_Final_EUR', 'ItemData', '*.xml')) +
        glob.glob(os.path.join(args.dc, 'Server', 'Datasheet', 'ItemData', '*.xml'))))
    for f in files:
        t = io.open(f, encoding='utf-8', errors='ignore').read()
        pairs = [(i, ic) for i, ic in ITEM_RE.findall(t)]
        pairs += [(i, ic) for ic, i in ITEM_RE2.findall(t)]
        for iid, icon in pairs:
            hit = PKG_RE.search(icon)
            if hit:
                pkg = hit.group(1)
                out[pkg].add(int(iid))
                stem = STEM_RE.match(pkg)
                if stem and stem.group(1) != pkg:
                    out[stem.group(1)].add(int(iid))
    out = {k: sorted(v) for k, v in out.items()}
    print(f'{len(files)} ItemData files -> {len(out):,} packages named by an item icon')
    fam = collections.Counter(k.split('_')[0] for k in out)
    print('  families:', dict(fam.most_common(6)))
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dest = os.path.join(root, 'scripts', 'icon_index.json')
    io.open(dest, 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False))
    print(f'wrote {dest} ({os.path.getsize(dest):,} B)')
    for p in ('Acc_206', 'Acc_384', 'PC_Weapons_Event', 'PC_Weapons_Event03'):
        v = out.get(p)
        print(f'   {p}: {len(v) if v else 0} item(s) {v[:4] if v else ""}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
