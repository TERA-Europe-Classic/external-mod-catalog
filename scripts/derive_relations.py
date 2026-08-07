"""Derive `conflicts_with` from what each mod actually writes.

Two mods are alternatives when they write the SAME target object. That is a fact
about the deploy metadata, not a judgement call, so it should be computed rather
than curated — hand-maintained lists drift the moment a mod is re-pointed, and
the Alternatives panel has been inconsistent for exactly that reason.

Targets are gathered from every layer a mod can write:
  composite_redirect  target_object_path
  tmm                 the object paths inside the TMM footer, recorded per entry
  dropin              target_dropin_filename
  loose_replace/add   target_loose_path
  tfc_patch           tfc_file + span
...including any carried on parts[].

A COLLECTION is a different relation — same author and theme, may coexist — and
is deliberately not inferred here; guessing it wrong buries real conflicts.

    python scripts/derive_relations.py --dry-run
    python scripts/derive_relations.py
"""
import argparse
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import catalog_io


def targets(mod):
    """Every object this entry writes, normalised so the same slot compares equal."""
    out = set()
    for owner in [mod] + list(mod.get('parts') or []):
        t = owner.get('target_object_path')
        if t:
            # the composite id prefix varies per client build; the object path does not
            out.add(('object', t.split('.', 1)[-1].lower()))
        for field, kind in (('target_dropin_filename', 'file'),
                            ('target_loose_path', 'loose'),
                            ('tfc_file', 'tfc')):
            v = owner.get(field)
            if v:
                out.add((kind, str(v).lower()))
        for p in owner.get('tmm_object_paths') or []:
            out.add(('object', p.split('.', 1)[-1].lower()))
    return out


def derive(mods):
    owners = collections.defaultdict(set)
    for m in mods:
        for t in targets(m):
            owners[t].add(m['id'])
    rel = collections.defaultdict(set)
    for t, ids in owners.items():
        if len(ids) < 2:
            continue
        for a in ids:
            rel[a] |= (ids - {a})
    return rel


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    cat = catalog_io.load()
    mods = cat['mods']
    rel = derive(mods)

    # Only prune an entry we can actually see. A `tmm` mod records its object
    # paths in the TMM footer, not the catalog, so 151 entries have no derivable
    # target at all — pruning those would have deleted 125 entries' curated
    # conflicts, including bns-plate-heavy-metal <-> white-castanica-demon, which
    # is a real same-slot conflict proven in game. Where we are blind we only add.
    added = removed = touched = blind = 0
    for m in mods:
        derived = rel.get(m['id'], set())
        have = set(m.get('conflicts_with') or [])
        visible = bool(targets(m))
        if not visible:
            blind += 1
        want = sorted(derived if visible else (have | derived))
        if want == sorted(have):
            continue
        touched += 1
        added += len(set(want) - have)
        removed += len(have - set(want))
        if not args.dry_run:
            if want:
                m['conflicts_with'] = want
            else:
                m.pop('conflicts_with', None)
    print(f"{blind} entries have no derivable target (tmm footers are not in the catalog) - kept as-is")

    print(f"{touched} entries change  (+{added} links, -{removed} stale)")
    print(f"{sum(1 for m in mods if rel.get(m['id']))} entries end up with at least one alternative")
    if not args.dry_run and touched:
        cat['version'] += 1
        catalog_io.save(cat)
        print(f"catalog v{cat['version']}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
