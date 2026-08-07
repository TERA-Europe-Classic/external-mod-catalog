"""Map fishing gear meshes to the items that grant them.

One hop, unlike the weapon chain: FishingData carries the item id inline.

    <FishingRod itemTemplateId="206700"
                rodMeshName="Fishing_Flyrod.Skel.FishingRod_A_Skel" />

The float has no item. FishingResourceData holds exactly one FloatResourceData
row -- there is a single global bobber mesh and nothing equips it, so a float
mod cannot name an item however hard the schema asks. That is a fact about the
game, not a gap in the index.

Writes scripts/fishing_index.json: "Fishing_Flyrod" -> [item ids].
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
ROD_RE = re.compile(r'<FishingRod\b[^>]*>')
ITEM_RE = re.compile(r'\bitemTemplateId="(\d+)"')
MESH_RE = re.compile(r'\brodMeshName="([A-Za-z0-9_]+)\.')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dc', default=DEFAULT_DC)
    args = ap.parse_args()
    C = os.path.join(args.dc, 'Client', 'DataCenter_Final_EUR')

    out = collections.defaultdict(set)
    for f in glob.glob(os.path.join(C, 'FishingData', '*.xml')):
        t = io.open(f, encoding='utf-8', errors='ignore').read()
        for m in ROD_RE.finditer(t):
            g = m.group(0)
            iid, mesh = ITEM_RE.search(g), MESH_RE.search(g)
            if iid and mesh:
                out[mesh.group(1)].add(int(iid.group(1)))

    res = {k: sorted(v) for k, v in out.items()}
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dest = os.path.join(root, 'scripts', 'fishing_index.json')
    io.open(dest, 'w', encoding='utf-8').write(json.dumps(res, ensure_ascii=False))
    for k, v in sorted(res.items()):
        print(f'   {k}: {len(v)} item(s) {v[:4]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
