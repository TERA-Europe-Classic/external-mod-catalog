"""Guard: every catalog entry declares how it deploys and where.

A gpk entry with no `deploy_strategy` falls through to the launcher's default
composite path. It installs, reports success, and does nothing — or worse,
writes into a layer the engine never reads. Thirty-seven entries shipped that
way under version "2026-05-01-x64-port" before anyone noticed, including
Castanic Sleepy Running Togs, which a tester reported as simply not working.

Each strategy also needs the field that tells the installer *where* to write.
A `loose_replace` with no `target_loose_path` has nothing to replace; seventeen
entries were in that state.

The checks are deliberately structural — they ask "can this entry possibly
deploy?", not "is the art correct". Run from the repo root:

    python scripts/check_entry_schema.py

Exits non-zero and names every offender, grouped by problem.
"""
import io
import re
import json
import os
import sys

# What each strategy needs before the installer can act on it.
REQUIRED_BY_STRATEGY = {
    'composite_redirect': ['target_object_path'],
    'tmm': [],                       # object paths live in the TMM footer
    'dropin': ['target_dropin_filename'],
    'loose_replace': ['target_loose_path'],
    'loose_add': ['target_loose_path'],
    'tfc_patch': ['tfc_file'],
    'decal_patch': ['target_loose_path'],
    'composite_patch': [],
}

# Entries that legitimately carry no strategy: external tools are installed by
# their own installer, not by the gpk deploy machinery.
EXEMPT_KINDS = {'external'}

# Every entry owes the player these, whatever it deploys. `last_verified` is
# deliberately NOT here: blank is the honest value for a mod nobody has
# confirmed in game, and filling it to satisfy a checker would be a lie.
REQUIRED_FIELDS = [
    'id', 'kind', 'name', 'author', 'category', 'version',
    'short_description', 'replaces', 'credits',
]

# `source_url` is NOT required, for the same reason as `last_verified`: for 42
# entries there is nothing to point at. Thirty-three came off the MT forum,
# which no longer exists; the rest were Discord attachments whose links have
# expired. Their provenance lives in `credits`, which every entry does owe —
# an author's name and how the mod reached us is the debt we can always pay.
# Demanding a URL here would only invite an invented one.

# Fields whose absence only matters for a downloadable payload.
REQUIRED_FOR_PAYLOAD = ['download_url', 'sha256', 'size_bytes', 'gpk_files']

# ---------------------------------------------------------------------------
# `replaces` must match the SHAPE its category implies.
#
# One grammar cannot fit all three. A costume owes item ids you can paste into
# inventory search. A face decal has no item at all — it owes the character-
# creation slot. A window restyle has neither and owes the window's name.
# Writing "no item ids" on a UI mod is correct; leaving a costume without them
# is how a tester ends up staring at a panel that says "Turns the Red Running
# Togs pastel pink" with nothing to search for.
WEARABLE_CATEGORIES = {'Costumes', 'Accessories', 'Mounts & Pets', 'Weapon Skins'}
CUSTOMIZATION_CATEGORIES = {'Eyes & Face', 'Hair'}

ITEM_ID = re.compile(r'#\d{4,}')
# "Face 11, Adornment 3", "face preset 10", "hairstyles 1-13" — the shapes the
# catalog already uses; the slot number is what makes it findable in the
# character creator.
SLOT = re.compile(r'\b(face|adornment|preset|hairstyle|hair)s?\b[^.]{0,24}?\d', re.I)
RACE = re.compile(r'\b(elin|popori|castanic|aman|high[\s-]?elf|human|baraka)\b', re.I)


def replaces_problem(entry):
    """The shape violation for this entry's `replaces`, or None."""
    text = (entry.get('replaces') or '').strip()
    category = entry.get('category') or ''
    if not text:
        return None                      # 'missing replaces' already reports it

    if category in WEARABLE_CATEGORIES:
        if not ITEM_ID.search(text):
            return 'wearable replaces carries no #item id'
        return None

    if category in CUSTOMIZATION_CATEGORIES:
        # Some "Hair" entries are actually hair ACCESSORIES — real items with
        # real ids. An id is a stronger answer than a slot, so it passes.
        if ITEM_ID.search(text):
            return None
        if not SLOT.search(text):
            return 'customization replaces names no slot (face/adornment/preset number)'
        if not RACE.search(text):
            return 'customization replaces names no race'
        return None

    # Interface and system mods: no item, no slot. They owe a description of
    # what changes, and must not claim item ids they cannot have.
    return None

# One version grammar: a three-part numeric core, optionally a tag.
#
# The catalog grew five shapes across as many eras. Zero-padding the bare
# numerics (1.7 -> 1.7.0) was mechanical and is done. The dated build strings
# (2026-r2, 2026-05-01-x64-port) are NOT mechanical — rewriting them means
# deciding what our port revisions mean as major/minor/patch, which is Lukas's
# call, not a script's. So this rule bites on anything NEW that drifts, and the
# existing dated entries are listed under their own heading rather than
# silently mangled.
VERSION_RE = re.compile(r'^\d+\.\d+\.\d+(-.+)?$')
DATED_VERSION_RE = re.compile(r'^\d{4}-')

# Reported, but not counted as failures — these are open decisions, not
# defects, and 447 of them would bury the 140 things that are actually
# broken. Blocking CI on a question only Lukas can answer helps nobody.
PENDING_KINDS = {'dated version, pending a scheme'}


def _strategies(entry):
    """Every strategy this entry deploys with, top level plus parts."""
    out = []
    if entry.get('deploy_strategy'):
        out.append((entry, entry['deploy_strategy']))
    for part in entry.get('parts') or []:
        if part.get('deploy_strategy'):
            out.append((part, part['deploy_strategy']))
    return out


def problems(mods):
    """Returns {problem: [(id, detail), ...]} — empty dict means the catalog passes."""
    found = {}

    def add(kind, mod_id, detail=''):
        found.setdefault(kind, []).append((mod_id, detail))

    for m in mods:
        mid = m.get('id', '<no id>')

        external = m.get('kind') in EXEMPT_KINDS
        for field in REQUIRED_FIELDS:
            # Shinra and TCC are overlay apps. They swap no game asset, so
            # `replaces` has nothing true to say and blank is the answer.
            if external and field == 'replaces':
                continue
            if not m.get(field):
                add(f'missing {field}', mid, '')

        shape = replaces_problem(m)
        if shape:
            add(shape, mid, (m.get('replaces') or '')[:60])

        version = str(m.get('version', '')).strip()
        if version and not VERSION_RE.match(version):
            add('dated version, pending a scheme' if DATED_VERSION_RE.match(version)
                else 'version is not MAJOR.MINOR.PATCH', mid, version)

        if external:
            continue

        for field in REQUIRED_FOR_PAYLOAD:
            if not m.get(field):
                add(f'missing {field}', mid, '')

        strategies = _strategies(m)
        if not strategies:
            add('no deploy_strategy', mid,
                f"target={m.get('target_object_path') or '-'} size={m.get('size_bytes')}")
            continue

        for owner, strat in strategies:
            if strat not in REQUIRED_BY_STRATEGY:
                add('unknown deploy_strategy', mid, strat)
                continue
            for field in REQUIRED_BY_STRATEGY[strat]:
                if not owner.get(field):
                    add(f"{strat} missing {field}", mid, '')

        if str(m.get('download_url', '')).startswith('TODO'):
            add('placeholder download_url', mid, str(m['download_url'])[:40])

    return found


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with io.open(os.path.join(root, 'catalog.json'), 'rb') as f:
        mods = json.loads(f.read())['mods']

    found = problems(mods)
    pending = {k: v for k, v in found.items() if k in PENDING_KINDS}
    failures = {k: v for k, v in found.items() if k not in PENDING_KINDS}

    def report(groups, heading):
        total = sum(len(v) for v in groups.values())
        print(f'{total} {heading} across {len(mods)} entries:\n')
        for kind in sorted(groups, key=lambda k: -len(groups[k])):
            rows = groups[kind]
            print(f'  {kind}  ({len(rows)})')
            for mid, detail in rows[:12]:
                print(f'     {mid}{"  " + detail if detail else ""}')
            if len(rows) > 12:
                print(f'     ... and {len(rows) - 12} more')
            print()

    if failures:
        report(failures, 'problem(s)')
    else:
        print(f'OK: {len(mods)} entries, every one declares how and where it deploys.')
    if pending:
        report(pending, 'pending decision(s)')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
