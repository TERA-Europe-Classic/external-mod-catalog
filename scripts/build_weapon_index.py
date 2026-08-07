"""Map weapon/armour mesh packages to the items that grant them.

Four hops, all in the client datacenter:

    WeaponData              meshL="PC_Weapons_Event03.SM.Dual03_L_SM"
                            <Weapon id="2101988" .../>
    EquipmentLookInfoData    <LookInfo id="601008" humanMalePartid="2101988"
                                      castanicFemalePartid="2102042" .../>
    ItemData                 <Item id="..." linkLookInfoId="601008" .../>

The per-race *Partid columns hold WEAPON ids (2.1M range) on weapon rows and
armour partids (900k range) on armour rows. I ruled this table out earlier
after reading a single armour row and concluding the id spaces did not meet --
they do, per row type. Grepping for an actual weapon id found it immediately,
which is the third time that beat guessing at table names.

Writes scripts/weapon_index.json: "PC_Weapons_Event03" -> [item ids].
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

WEAPON_RE = re.compile(r'<Weapon\b[^>]*>')
WID_RE = re.compile(r'\bid="(\d+)"')
MESH_RE = re.compile(r'\bmesh[LR]="([A-Za-z0-9_]+)\.')
PARTID_RE = re.compile(r'\b\w*[Pp]artid="(\d+)"')
LOOK_ID_RE = re.compile(r'<LookInfo\b[^>]*\bid="(\d+)"')
ITEM_LOOK = re.compile(r'<Item\b[^>]*\bid="(\d+)"[^>]*\blinkLookInfoId="(\d+)"')
ITEM_LOOK2 = re.compile(r'<Item\b[^>]*\blinkLookInfoId="(\d+)"[^>]*\bid="(\d+)"')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dc', default=DEFAULT_DC)
    args = ap.parse_args()
    C = os.path.join(args.dc, 'Client', 'DataCenter_Final_EUR')

    # mesh package -> {weapon ids}
    pkg_wid = collections.defaultdict(set)
    for f in glob.glob(os.path.join(C, 'WeaponData', '*.xml')):
        t = io.open(f, encoding='utf-8', errors='ignore').read()
        for m in WEAPON_RE.finditer(t):
            g = m.group(0)
            wid = WID_RE.search(g)
            if not wid:
                continue
            for pkg in set(MESH_RE.findall(g)):
                pkg_wid[pkg].add(wid.group(1))
    print(f'{len(pkg_wid):,} mesh packages in WeaponData')

    # partid -> {lookinfo ids}
    part_look = collections.defaultdict(set)
    for f in glob.glob(os.path.join(C, 'EquipmentLookInfoData', '*.xml')):
        t = io.open(f, encoding='utf-8', errors='ignore').read()
        for m in re.finditer(r'<LookInfo\b[^>]*>', t):
            g = m.group(0)
            lid = LOOK_ID_RE.search(g)
            if not lid:
                continue
            for p in PARTID_RE.findall(g):
                part_look[p].add(lid.group(1))
    print(f'{len(part_look):,} partids in EquipmentLookInfoData')

    # lookinfo id -> {item ids}
    look_items = collections.defaultdict(set)
    for f in sorted(set(glob.glob(os.path.join(C, 'ItemData', '*.xml')) +
                        glob.glob(os.path.join(args.dc, 'Server', 'Datasheet',
                                               'ItemData', '*.xml')))):
        t = io.open(f, encoding='utf-8', errors='ignore').read()
        for iid, lid in ITEM_LOOK.findall(t):
            look_items[lid].add(int(iid))
        for lid, iid in ITEM_LOOK2.findall(t):
            look_items[lid].add(int(iid))
    print(f'{len(look_items):,} lookinfo ids referenced by an item')

    out = {}
    for pkg, wids in pkg_wid.items():
        ids = set()
        for w in wids:
            for lid in part_look.get(w, ()):
                ids |= look_items.get(lid, set())
        if ids:
            out[pkg] = sorted(ids)
    print(f'{len(out):,} packages resolve to at least one item')

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dest = os.path.join(root, 'scripts', 'weapon_index.json')
    io.open(dest, 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False))
    print(f'wrote {dest} ({os.path.getsize(dest):,} B)')
    for p in ('PC_Weapons_Event03', 'PC_Weapons_Event08', 'PC_Weapons_Event',
              'PC_Weapons_Event19'):
        v = out.get(p)
        print(f'   {p}: {len(v) if v else 0} item(s) {v[:4] if v else ""}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
