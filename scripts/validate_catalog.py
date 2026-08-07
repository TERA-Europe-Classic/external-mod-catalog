"""HARD gate. Every entry, every rule, exit 1 on the first violation anywhere.

This replaces a checker that asked "does this sentence contain a #id" and
passed everything. It could not catch a wrong id, a missing race, a name that
belongs to a different costume, or a range whose interior is a separate item.

What is enforced now:

  1. `replaces_data` validates against schema/replaces.schema.json --
     additionalProperties:false, enums for race/gender/kind, discrete ids only.
  2. the entry validates against schema/entry.schema.json -- category decides
     the shape, so a Costume without targets fails and an interface mod
     claiming item ids fails.
  3. EVERY item id EXISTS in the datacenter (scripts/item_index.json,
     132,392 ids). An invented id fails.
  4. EVERY item name MATCHES what the datacenter calls that id. A name copied
     from the wrong costume fails.
  5. EVERY race MATCHES the datacenter's requiredRace for that id. Claiming
     five races for a one-race costume fails.
  6. the stored `replaces` string EQUALS render_replaces.render(replaces_data).
     Hand-editing the copy fails, so the two cannot drift.
  7. every declared `objects` path IS exported by the mod's own payload, at the
     sha256 the catalog currently ships. Rule 3 does this for item ids against
     the datacenter; this is the same check for the things the game does not
     sell -- an NPC, a fishing float, a hairstyle -- which have no id to look up.

    python scripts/validate_catalog.py           # all entries, grouped report
    python scripts/validate_catalog.py --id X    # one entry, every error
"""
import argparse
import collections
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_replaces                                            # noqa: E402

try:
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
except ImportError:                                               # pragma: no cover
    print('needs: pip install jsonschema', file=sys.stderr)
    raise

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCHEMA_DIR = os.path.join(ROOT, 'schema')


def load_validator():
    def read(name):
        with io.open(os.path.join(SCHEMA_DIR, name), encoding='utf-8') as fh:
            return json.load(fh)
    entry = read('entry.schema.json')
    replaces = read('replaces.schema.json')
    registry = Registry().with_resources([
        ('replaces.schema.json', Resource.from_contents(replaces)),
        (replaces['$id'], Resource.from_contents(replaces)),
    ])
    return Draft202012Validator(entry, registry=registry)


def dc_errors(entry, index):
    """Every way `replaces_data` can disagree with the datacenter."""
    out = []
    data = entry.get('replaces_data') or {}
    for t in data.get('targets') or []:
        for it in t.get('items') or []:
            info = index.get(str(it.get('id')))
            if not info:
                out.append(f"item #{it.get('id')} does not exist in the datacenter")
                continue
            if info.get('name') and it.get('name') != info['name']:
                out.append(f"item #{it['id']} is {info['name']!r}, entry says {it.get('name')!r}")
            dc_race = info.get('race', 'any')
            if dc_race not in ('any', '') and t.get('race') != dc_race:
                out.append(f"item #{it['id']} is {dc_race}, entry says {t.get('race')}")
    return out


def object_errors(entry, proof):
    """`objects` must be what the payload actually exports -- not a nicer guess.

    The proof file records, per entry, the payload sha256 the objects were read
    out of. CI compares that against the sha256 the catalog currently ships. Edit
    the payload and the shas diverge, the proof goes stale, and the gate fails --
    so `objects` cannot quietly describe a file that no longer exists.

    Without this the field would be the soft option: a string nobody checks.
    Regenerate with scratch/read_objects.py, which opens the payload and lists
    its exports; a .bin dropin is a gpk and a tmm is N inner gpks.
    """
    data = entry.get('replaces_data') or {}
    declared = data.get('objects') or []
    if not declared:
        return []
    p = proof.get(entry['id'])
    if not p:
        return ['`objects` has no payload proof '
                '(regenerate with scratch/read_objects.py)']
    sha = entry.get('sha256') or ''
    if sha and p.get('sha256') and sha != p['sha256']:
        return ['`objects` proof is stale: the payload changed since it was read '
                '(regenerate with scratch/read_objects.py)']
    known = set(p.get('objects') or [])
    return [f"object {o['path']!r} is not exported by the payload"
            for o in declared if o.get('path') not in known]


def render_errors(entry):
    data = entry.get('replaces_data')
    if not data:
        return []
    want = render_replaces.render(data)
    got = (entry.get('replaces') or '').strip()
    if got != want.strip():
        return ['`replaces` does not match the render of `replaces_data` '
                '(regenerate with scripts/migrate_replaces.py --write)']
    return []


def is_declaration_rule(err):
    """True for the rules that demand the entry declare what it replaces.

    Three of them, and only these three:

      * which FORM was declared -- `...properties.replaces_data.anyOf`. Category
        decides the shape: a Costume owes `targets` or `objects`, an interface
        mod `loose` or `objects`.
      * that a gpk entry has `replaces` at all.
      * that `replaces` is at least 8 characters. An entry with nothing to name
        renders the empty string, because `render()` refuses to turn a bare
        summary into copy -- so the length rule fires on exactly the entries the
        first rule already excused.

    Matched on schema path and keyword, never on message text, so the waiver
    cannot widen by accident: an unknown key, a bad race enum or a wrong type
    inside `replaces_data` trips a different keyword and still blocks.
    """
    path = list(err.schema_path)
    if 'replaces_data' in path and path[-1:] == ['anyOf']:
        return True
    if err.validator == 'required' and 'replaces' in err.message:
        return True
    return err.validator == 'minLength' and list(err.absolute_path) == ['replaces']


def check(entry, validator, index, proof):
    # "Every entry declares what it replaces, OR says why not." `broken` is
    # where the why-not lives -- it names what is wrong and what has to happen
    # before the entry can ship. Demanding a declaration from an entry that has
    # already said its payload is unexplained gets you an invented one, which
    # is the failure this gate exists to prevent. Everything else still runs.
    waived = bool((entry.get('broken') or '').strip())
    errs = [f'{".".join(str(p) for p in e.absolute_path) or "(entry)"}: {e.message}'
            for e in validator.iter_errors(entry)
            if not (waived and is_declaration_rule(e))]
    errs += dc_errors(entry, index)
    errs += object_errors(entry, proof)
    errs += render_errors(entry)
    return errs




def presentation_errors(entry, no_media, part_names):
    """The audit criteria that are checkable without opening a payload.

    Born from one night of field failures, each rule is a bug class:
      * part filename collisions shipped one file under a name two different
        builds claimed, and half the installs failed their hash check;
      * entries with no media and no recorded reason read as "nobody looked"
        -- 48 of them turned out to be showing a blog's placeholder card;
      * an empty long_description is a card that cannot be judged.
    """
    out = []
    mid = entry.get('id', '?')
    broken = bool((entry.get('broken') or '').strip())
    # media present, or its absence reasoned in _no_media.json
    if not (entry.get('screenshots') or []) and mid not in no_media:
        out.append('no screenshots and no reason recorded in scripts/_no_media.json')
    if (entry.get('screenshots') or []) and not entry.get('blur_data'):
        out.append('screenshots without blur_data (rows paint blank while loading)')
    ld = (entry.get('long_description') or '').strip()
    if not ld:
        out.append('long_description is empty')
    # a description that adds nothing to the subtitle is a card that cannot
    # be judged either; 139 entries were composed up to this floor and the
    # floor keeps new ones from slipping back under it
    elif len(ld) < 60:
        out.append(f'long_description is {len(ld)} chars (min 60)')
    elif ld == (entry.get('short_description') or '').strip():
        out.append('long_description merely repeats the subtitle')
    # subtitle shape: one capitalised sentence, no 'Replaces' opener (the
    # panel already labels that field), at most 90 characters
    sub = (entry.get('tagline') or entry.get('short_description') or '').strip()
    if sub:
        if len(sub) > 91:
            out.append(f'subtitle is {len(sub)} chars (max 90)')
        if sub.lower().startswith('replaces '):
            out.append('subtitle starts with Replaces -- the panel already labels that')
        if not sub.endswith(('.', '!', '?')):
            out.append('subtitle has no final period')
    # part filename uniqueness: one release filename must mean one build.
    # A broken entry is exempt: its flag already says do-not-install, and
    # demanding clean filenames from parts awaiting a rebuild would force
    # either a lie or a removal -- both worse than the flag.
    for p_ in ([] if broken else entry.get('parts') or []):
        name = (p_.get('download_url') or '').rsplit('/', 1)[-1]
        if not name:
            continue
        sha = p_.get('sha256')
        seen = part_names.setdefault(name, (mid, sha))
        if seen[1] != sha:
            out.append(f'part file {name!r} is claimed with a different sha by {seen[0]}')
    return out

def duplicate_errors(mods):
    """Two entries must never ship the same payload bytes.

    Identical bytes under two names means at most one of them delivers what it
    claims -- the harvest fetched one file twice. 27 groups of this were live
    at once, including four differently-named HP bars off a single download.
    A pair that deliberately shares a file records it in `shares_payload_with`.
    """
    sha_map = collections.defaultdict(set)
    for m in mods:
        for p in [m] + (m.get('parts') or []):
            if p.get('sha256'):
                sha_map[p['sha256']].add(m['id'])
    by_id = {m['id']: m for m in mods}
    errs = collections.defaultdict(list)
    for ids in {frozenset(v) for v in sha_map.values() if len(v) > 1}:
        # deliberate sharing, declared on BOTH sides, is fine
        if all(set(by_id[i].get('shares_payload_with') or []) >= (ids - {i})
               for i in ids):
            continue
        undeclared = [i for i in sorted(ids)
                      if not (by_id[i].get('broken') or '').strip()]
        if len(undeclared) > 1:
            errs['entries ship identical payload bytes without a broken flag '
                 'or a declared shares_payload_with'].append(', '.join(undeclared)[:100])
    return errs


def presentation_sweep_errors(mods):
    """Criteria 1-3 as blocking checks, catalog-wide."""
    errs = collections.defaultdict(list)
    for m in mods:
        mid = m['id']
        name = (m.get('name') or '').strip()
        if re.search(r'\b(this mod|requested by|i made|hello my|download here|'
                     r'works on only|my first mod)\b', name, re.I):
            errs['title reads as scraped post prose, not a mod name'].append(mid)
        sub = (m.get('short_description') or '').strip()
        if sub and re.search(r'(^|\s)(i|my|me|we|our)\s', sub, re.I):
            errs['subtitle is written in the first person'].append(mid)
        if not (m.get('credits') or '').strip():
            errs['no credits'].append(mid)
        if not (m.get('source_url') or '').strip():
            errs['no source_url'].append(mid)
        rd = m.get('replaces_data') or {}
        if not (rd.get('targets') or rd.get('slots') or rd.get('objects')
                or rd.get('loose')):
            errs['replaces_data resolves to nothing -- no items, slots, objects '
                 'or loose targets'].append(mid)
    return errs


def relation_errors(mods):
    """Catalog-level invariants: collections have members, links are mutual.

    A collection of one is a tagging error -- either the tag is wrong or the
    siblings lost theirs (found live: pantypon-brighter-whiter sat at one member
    while hair 12 went untagged). A one-way conflicts_with link means one side
    was edited without the other; a dangling one points at a deleted mod.
    """
    by_id = {m['id']: m for m in mods}
    members = collections.defaultdict(list)
    for m in mods:
        if m.get('collection'):
            members[m['collection']].append(m['id'])
    errs = collections.defaultdict(list)
    for coll, ids in members.items():
        if len(ids) == 1:
            errs[f'collection "{coll}" has a single member -- tag its '
                 'siblings or drop the tag'].append(ids[0])
    for m in mods:
        for other in m.get('conflicts_with') or []:
            if other not in by_id:
                errs['conflicts_with points at a deleted mod'].append(
                    f'{m["id"]} -> {other}')
            elif m['id'] not in (by_id[other].get('conflicts_with') or []):
                errs['conflicts_with is one-way (run derive_relations.py)'].append(
                    f'{m["id"]} -> {other}')
    return errs


def alternatives_errors(mods):
    """Every mod replacing a given thing must link the others that replace it.

    Not "the same gpk" -- the same item, slot or object. conflicts_with is a
    weaker relation: of its edges, 1520 join identical targets and 750 join
    entries that merely overlap, and an overlap is a compatibility warning
    rather than a swap a player can choose between.

    Rebuilding the links is deterministic, so the gate is a comparison: if the
    stored field differs from what build_alternatives.py derives, the catalog
    was hand-edited and the derivation has to run again.
    """
    import build_alternatives
    errs = collections.defaultdict(list)
    groups = collections.defaultdict(list)
    for m in mods:
        k = build_alternatives.semkey(m)
        if k:
            groups[k].append(m['id'])
    want = {}
    for ids in groups.values():
        for i in ids:
            want[i] = sorted(x for x in ids if x != i)
    for m in mods:
        expected = want.get(m['id']) or []
        got = sorted(m.get('alternatives') or [])
        if got != expected:
            missing = sorted(set(expected) - set(got))
            extra = sorted(set(got) - set(expected))
            detail = []
            if missing:
                detail.append('missing ' + ', '.join(missing[:3]))
            if extra:
                detail.append('should not list ' + ', '.join(extra[:3]))
            errs['alternatives are stale -- run scripts/build_alternatives.py'].append(
                '%s (%s)' % (m['id'], '; '.join(detail) or 'out of date'))
        marker = build_alternatives.HEADING
        body = m.get('long_description') or ''
        if expected and marker not in body:
            errs['description has no rendered alternatives section'].append(m['id'])
        if not expected and marker in body:
            errs['description renders alternatives but the mod has none'].append(m['id'])
    return errs


def testability_errors(mods):
    """A testable entry must say WHERE to look, not repeat its own title.

    The verification sheet derives its instruction from replaces_data. When
    nothing resolves it used to fall back to "install, restart, observe the
    change the title describes", which reached 70 entries -- an eleventh of the
    deliverable -- and tells a tester nothing.

    A loose target that merely restates the mod name is the same failure wearing
    a disguise: "Pixel Moon Block" replaces "Pixel Moon Block" renders as "look
    at Pixel Moon Block". Both are blocked here so the sheet stays usable.

    Only entries a tester could actually reach are checked; a broken one is on
    the fix list, not the test list.
    """
    import difflib
    import make_verify
    errs = collections.defaultdict(list)
    for m in mods:
        if (m.get('broken') or '').strip():
            continue
        if not (m.get('parts') or m.get('download_url')):
            continue
        if not make_verify.first_target(m):
            errs['no in-game instruction can be derived -- give replaces_data an '
                 'item, slot, object or loose target'].append(m['id'])
            continue
        loose = [str(x) for x in ((m.get('replaces_data') or {}).get('loose') or [])]
        if loose:
            a = re.sub(r'[^a-z0-9 ]', '', loose[0].lower()).strip()
            b = re.sub(r'[^a-z0-9 ]', '', (m.get('name') or '').lower()).strip()
            if a == b or difflib.SequenceMatcher(None, a, b).ratio() > 0.9:
                errs['loose target just repeats the mod name -- say what to look '
                     'at (run scripts/fix_circular_loose.py)'].append(m['id'])
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--id')
    args = ap.parse_args()

    mods = json.loads(io.open(os.path.join(ROOT, 'catalog.json'), 'rb').read())['mods']
    index = json.loads(io.open(os.path.join(HERE, 'item_index.json'), 'rb').read())
    proof_f = os.path.join(HERE, 'object_proof.json')
    proof = json.loads(io.open(proof_f, 'rb').read()) if os.path.exists(proof_f) else {}
    nm_f = os.path.join(HERE, '_no_media.json')
    no_media = json.loads(io.open(nm_f, 'rb').read()) if os.path.exists(nm_f) else {}
    part_names = {}
    validator = load_validator()

    if args.id:
        entry = next((m for m in mods if m['id'] == args.id), None)
        if not entry:
            print(f'no such entry: {args.id}')
            return 1
        errs = check(entry, validator, index, proof)
        errs += presentation_errors(entry, no_media, part_names)
        print(f'{args.id}: {"VALID" if not errs else str(len(errs)) + " error(s)"}')
        for e in errs:
            print(f'   {e}')
        return 1 if errs else 0

    failed = 0
    buckets = collections.defaultdict(list)
    for m in mods:
        errs = check(m, validator, index, proof)
        errs += presentation_errors(m, no_media, part_names)
        if errs:
            failed += 1
            for e in errs:
                buckets[e[:110]].append(m.get('id', '?'))

    for sweep in (relation_errors, duplicate_errors, presentation_sweep_errors,
                  alternatives_errors, testability_errors):
        for kind, rows in sweep(mods).items():
            failed += 1  # counts once per invariant so the gate still blocks
            buckets[kind] = rows

    print(f'{len(mods) - failed}/{len(mods)} entries valid\n')
    for kind in sorted(buckets, key=lambda k: -len(buckets[k])):
        rows = buckets[kind]
        print(f'  {kind}  ({len(rows)})')
        for r in rows[:5]:
            print(f'     {r}')
        if len(rows) > 5:
            print(f'     ... and {len(rows) - 5} more')
        print()
    if failed:
        print(f'FAILED: {failed} entries violate the schema. '
              'Fix every one -- this gate does not warn, it blocks.')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
