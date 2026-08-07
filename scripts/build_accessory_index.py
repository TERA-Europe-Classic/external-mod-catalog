"""Map accessory MESH packages (Acc_NNN) to the items that grant them.

Accessories are not in the costume asset2parts map, so 36 catalog entries had
no resolvable item id -- hats, bows, wings, hoods, all of which absolutely do
have items behind them. The chain the datacenter actually provides:

    Client/.../Accessory/*.xml
        <Accessory id="1" ...>
          <DataPerParts mesh="Acc_001.Skel.Attach_001_skel" partsId="206000"/>
      -> mesh package Acc_001  ->  Accessory id 1

    Client/.../ItemData/*.xml
        <Item id="..." linkCustomizingId="1" .../>
      -> Accessory id 1  ->  every item that grants it

RESULT SO FAR: THIS DOES NOT JOIN. Measured on the live datacenter --

    Accessory.id            400 files, ids 1-408
    ItemData.linkCustomizingId   905 distinct values, 40000-82316
    overlap                 ZERO

They are different id spaces, so `linkCustomizingId` is not the accessory id
and there is a third table in between that I have not located. `partsId`
(206000+) is a third space again. Do NOT ship a join built on either without
finding that table -- guessing the link is exactly how two mods ended up
described as replacing the wrong costume.

TABLES RULED OUT, so nobody re-walks them:
  CustomizingItems   ids ARE 40000+, matching linkCustomizingId exactly -- but
                     the row is only <CustomizingItem id passivityLink
                     destroyProbOnDead takeSlot />. No accessory reference at all.
  AccCustomizeData   <Accessory id="434" useCustomize="true"/>. Uses the 1-408+
                     Accessory id space, so it does not bridge to items either.
  EquipmentLookInfoData  partids are 906100-ish; Accessory partsId is 206000-ish.
                     Different space again.

What IS confirmed and useful: the mesh side works. Accessory-*.xml maps
mesh="Acc_047.Skel.Attach_047_skel" to an Accessory id reliably, and the mod
payloads name their vanilla package in their exports (Acc_047_diff,
Attach_047_Skel -> Acc_047). So the package is identifiable; only the last hop
to an item id is missing.

Writes scripts/accessory_index.json: "Acc_047" -> [item ids], EMPTY until the
join is found.
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

ACC_OPEN = re.compile(r'<Accessory\b[^>]*\bid="(\d+)"')
MESH_RE = re.compile(r'\bmesh="(Acc_\d+)[^"]*"')
ITEM_RE = re.compile(r'<Item\b[^>]*\bid="(\d+)"[^>]*\blinkCustomizingId="(\d+)"[^>]*>')
ITEM_RE2 = re.compile(r'<Item\b[^>]*\blinkCustomizingId="(\d+)"[^>]*\bid="(\d+)"[^>]*>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dc', default=DEFAULT_DC)
    args = ap.parse_args()

    # accessory id -> {mesh packages}
    acc_meshes = collections.defaultdict(set)
    files = sorted(glob.glob(os.path.join(
        args.dc, 'Client', 'DataCenter_Final_EUR', 'Accessory', 'Accessory-*.xml')))
    for f in files:
        t = io.open(f, encoding='utf-8', errors='ignore').read()
        # one <Accessory id=...> per file, meshes listed under it
        m = ACC_OPEN.search(t)
        if not m:
            continue
        aid = m.group(1)
        for mesh in MESH_RE.findall(t):
            acc_meshes[aid].add(mesh)
    print(f'{len(files)} Accessory files -> {len(acc_meshes):,} accessories with a mesh')

    # accessory id -> [item ids]
    acc_items = collections.defaultdict(set)
    ifiles = sorted(glob.glob(os.path.join(
        args.dc, 'Client', 'DataCenter_Final_EUR', 'ItemData', 'ItemData-*.xml')))
    for f in ifiles:
        t = io.open(f, encoding='utf-8', errors='ignore').read()
        for iid, aid in ITEM_RE.findall(t):
            acc_items[aid].add(int(iid))
        for aid, iid in ITEM_RE2.findall(t):
            acc_items[aid].add(int(iid))
    print(f'{len(ifiles)} ItemData files -> {len(acc_items):,} accessories referenced by items')

    # mesh package -> item ids
    out = collections.defaultdict(set)
    for aid, meshes in acc_meshes.items():
        for mesh in meshes:
            out[mesh] |= acc_items.get(aid, set())
    out = {k: sorted(v) for k, v in out.items() if v}
    print(f'{len(out):,} mesh packages resolve to at least one item')

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dest = os.path.join(root, 'scripts', 'accessory_index.json')
    io.open(dest, 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False))
    print(f'wrote {dest} ({os.path.getsize(dest):,} B)')
    for probe in ('Acc_047', 'Acc_038', 'Acc_384', 'Acc_004'):
        v = out.get(probe)
        print(f'   {probe}: {len(v) if v else 0} item(s) {v[:4] if v else ""}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
