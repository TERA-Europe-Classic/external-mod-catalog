"""Map mount/pet packages to the items that grant them, via the skill.

Mounts are not equipment: an item teaches a summon SKILL, and the skill's icon
names the vehicle package. Four hops, all in the client datacenter:

    SkillIconData   iconName="Icon_Skills.Vehicle_SportCar_Tex" skillId="111324"
                        -> package Vehicle_SportCar  ->  skill 111324
    ItemData        <Item id="204096" linkSkillId="111324" .../>
                        -> skill 111324  ->  item 204096

NpcShape/VehicleData also connect the package to a Vehicle row (mesh ->
Shape.id -> VehicleData.shapeId), but that branch dead-ends: nothing in
ItemData references a Vehicle id. The skill icon is the route that reaches an
item.

Found by grepping the datacenter for a package name rather than guessing table
names -- guessing produced three dead ends before this.

Writes scripts/mount_index.json: "Vehicle_SportCar" -> [item ids].
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
ICON_SKILL = re.compile(r'<Icon\b[^>]*\biconName="([^"]*)"[^>]*\bskillId="(\d+)"')
ICON_SKILL2 = re.compile(r'<Icon\b[^>]*\bskillId="(\d+)"[^>]*\biconName="([^"]*)"')
# Anchored on the dot and greedy, for the same reason the accessory regex had
# to be fixed: `Vehicle_\w+?` is non-greedy and stops at the first character.
# Skill icons also drop the prefix -- Icon_Skills.Ookami_Tex is the package
# Vehicle_Ookami -- so the bare token is indexed under both forms, and trailing
# variant letters (Vehicle_Koinobori_A_Tex) are stripped back to the base too.
PKG = re.compile(r'\.([A-Za-z][A-Za-z0-9_]*?)(?:_Tex)?$')
TRIM = re.compile(r'_(?:[A-Z]|\d+)$')
ITEM_SKILL = re.compile(r'<Item\b[^>]*\bid="(\d+)"[^>]*\blinkSkillId="(\d+)"')
ITEM_SKILL2 = re.compile(r'<Item\b[^>]*\blinkSkillId="(\d+)"[^>]*\bid="(\d+)"')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dc', default=DEFAULT_DC)
    args = ap.parse_args()

    pkg_skill = collections.defaultdict(set)
    for f in glob.glob(os.path.join(args.dc, 'Client', 'DataCenter_Final_EUR',
                                    'SkillIconData', '*.xml')):
        t = io.open(f, encoding='utf-8', errors='ignore').read()
        pairs = ICON_SKILL.findall(t) + [(i, s) for s, i in ICON_SKILL2.findall(t)]
        for icon, skill in pairs:
            hit = PKG.search(icon)
            if not hit:
                continue
            base = hit.group(1)
            forms = {base, TRIM.sub('', base)}
            for f in list(forms):
                forms.add(f if f.startswith(('Vehicle_', 'Pet_')) else 'Vehicle_' + f)
            for f in forms:
                if f.startswith(('Vehicle_', 'Pet_')):
                    pkg_skill[f].add(skill)
    print(f'{len(pkg_skill):,} vehicle/pet packages named by a skill icon')

    skill_items = collections.defaultdict(set)
    for f in sorted(set(
            glob.glob(os.path.join(args.dc, 'Client', 'DataCenter_Final_EUR', 'ItemData', '*.xml')) +
            glob.glob(os.path.join(args.dc, 'Server', 'Datasheet', 'ItemData', '*.xml')))):
        t = io.open(f, encoding='utf-8', errors='ignore').read()
        for iid, sid in ITEM_SKILL.findall(t):
            skill_items[sid].add(int(iid))
        for sid, iid in ITEM_SKILL2.findall(t):
            skill_items[sid].add(int(iid))
    print(f'{len(skill_items):,} skills taught by an item')

    out = {}
    for pkg, skills in pkg_skill.items():
        ids = set()
        for s in skills:
            ids |= skill_items.get(s, set())
        if ids:
            out[pkg] = sorted(ids)
    print(f'{len(out):,} packages resolve to at least one item')
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dest = os.path.join(root, 'scripts', 'mount_index.json')
    io.open(dest, 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False))
    print(f'wrote {dest} ({os.path.getsize(dest):,} B)')
    for p in ('Vehicle_SportCar', 'Vehicle_Koinobori', 'Vehicle_Ookami', 'Vehicle_Dragon'):
        v = out.get(p)
        print(f'   {p}: {len(v) if v else 0} item(s) {v[:4] if v else ""}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
