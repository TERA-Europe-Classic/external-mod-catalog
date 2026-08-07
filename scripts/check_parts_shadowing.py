"""Guard: parts[] must never silently shadow a rebuilt top-level payload.

The launcher installs an entry's parts[] when it has any, and never applies the
top-level composite redirect. So an entry that gets rebuilt at the top level but
keeps an older parts[] ships the OLD payload, installs cleanly, reports success
and renders vanilla — with nothing anywhere saying the rebuild was skipped.

That is what happened to the two loading-progress entries: rebuilt twice
(catalog v234, then v235) while a stale loose_replace part kept shipping a
vanilla roundtrip. Both rebuilds were reported to the tester as "please test",
and both times he was looking at the same dead payload.

Run from the repo root:
    python scripts/check_parts_shadowing.py
Exits non-zero and names the offenders if any entry is shadowed.
"""
import json
import io
import os
import sys


def offenders(mods):
    out = []
    for m in mods:
        parts = m.get('parts') or []
        top_sha = m.get('sha256')
        # Only entries that declare a top-level composite redirect can be
        # shadowed; a parts-only entry is the normal multi-part shape.
        if not parts or not top_sha or not m.get('target_object_path'):
            continue
        if top_sha in {p.get('sha256') for p in parts if p.get('sha256')}:
            continue
        out.append(m)
    return out


def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    doc = json.load(io.open(os.path.join(here, 'catalog.json'), encoding='utf-8'))
    mods = doc['mods'] if isinstance(doc, dict) else doc

    bad = offenders(mods)
    if not bad:
        print(f"OK: no shadowed entries across {len(mods)} mods")
        return 0

    print(f"FAIL: {len(bad)} entries ship a payload that is not their top-level rebuild\n")
    for m in bad:
        top = (m.get('download_url') or '').rsplit('/', 1)[-1]
        print(f"  {m['id']} (v{m.get('version')})")
        print(f"     declares : {top} -> {m['target_object_path']}")
        for p in m['parts']:
            f = (p.get('download_url') or '').rsplit('/', 1)[-1]
            print(f"     ships    : [{p.get('deploy_strategy')}] {f}")
        print("     fix: drop parts[], or fold the rebuilt payload into a part\n")
    return 1


if __name__ == '__main__':
    sys.exit(main())
