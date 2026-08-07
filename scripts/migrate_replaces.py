"""Turn every `replaces` sentence into `replaces_data`, resolved against the DC.

Both fields ship. `replaces_data` is the source of truth and is schema-checked;
`replaces` is regenerated from it so older launcher builds -- which type the
field as a plain string -- keep working. CI asserts the string equals the
render, so they cannot drift.

Every id is looked up in scripts/item_index.json (132,392 ids from the client
datacenter). An id that resolves to nothing is REPORTED, never invented, and
the race comes from the datacenter rather than from whatever the sentence
claimed. That is the whole point: a regex can see "#271132", only the DC knows
it is Thunor's Armor and that it is Elin.

    python scripts/migrate_replaces.py --dry-run
    python scripts/migrate_replaces.py --write
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

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PAYLOAD_PKGS = {}
ICON_MAP = {}
MOUNT_MAP = {}
WEAPON_MAP = {}
FISHING_MAP = {}
OBJECT_MAP = {}
# package/object name -> parts -> items. 207 wearables never cited an id in
# their prose -- mounts, pets, fishing rods, weapon skins. The sentence cannot
# be parsed into something it never said, so those resolve from the PACKAGE
# the mod ships instead. Guessing from the package NAME is what produced two
# wrong "what does this replace" claims; this walks the datacenter.
RESOLVER = (r"C:/Users/Lukas/Documents/GitHub/TERA EU Classic"
            r"/tera-mod-archive/dc_resolver.json")
FILENAME_SUFFIX = re.compile(r'(_dup|\.patched|\.castanic|_r\d+|_x64|_v\d+)+$', re.I)
# A tmm payload's `gpk_files` is the MOD's own filename, which the datacenter has
# never heard of. The vanilla object names live in the payload FOOTER, scanned
# once into tmm_objects.json (ranged HTTP reads, ~10 KB per mod instead of the
# 40 MB payload). Without this every tmm costume looked unresolvable.
TMM_OBJECTS = os.path.join(HERE, 'tmm_objects.json')
# For 186 entries nothing in the metadata names a vanilla package: `gpk_files`
# is the mod's own filename and ~40 dropins carry a hashed `.bin` as their
# target. But the payloads ARE gpk packages and their exports say what they
# replace -- Acc_047_diff + Attach_047_Skel means the package is Acc_047.
# Scanned once into payload_packages.json.
PAYLOAD_PACKAGES = os.path.join(HERE, 'payload_packages.json')
# package -> items, via the item ICON, which names the package directly:
#   <Item id="115594" icon="Icon_Equipments.Acc_206_Tex" .../>
# This is the join that Accessory.id / linkCustomizingId / partsId all failed
# to give. 774 packages, 715 of them accessories.
ICON_INDEX = os.path.join(HERE, 'icon_index.json')
# Mounts and pets are not equipment: an item teaches a summon SKILL and the
# skill's icon names the vehicle package. SkillIconData -> skillId ->
# ItemData.linkSkillId. The NpcShape/VehicleData branch dead-ends -- nothing in
# ItemData references a Vehicle id.
MOUNT_INDEX = os.path.join(HERE, 'mount_index.json')
# Weapons: WeaponData mesh -> Weapon id -> EquipmentLookInfoData *Partid ->
# LookInfo id -> ItemData.linkLookInfoId. The per-race Partid columns hold
# weapon ids on weapon rows and armour partids on armour rows, which is why
# reading one armour row made the id spaces look disjoint.
WEAPON_INDEX = os.path.join(HERE, 'weapon_index.json')
# Fishing rods carry their item id inline in FishingData. The float does not:
# FishingResourceData holds one FloatResourceData row and nothing equips it, so
# a float mod declares `objects`, not `targets`.
FISHING_INDEX = os.path.join(HERE, 'fishing_index.json')
# What the payload ACTUALLY exports, read back out of the mod's own file. The
# resolvers were being fed the entry's declared target filename, which for a
# harvested dropin is the blob name ("mf__aioshe-king-blob-...bin") and matches
# nothing. The exports name real packages, so the same indexes suddenly hit.
PAYLOAD_OBJECTS = os.path.join(HERE, 'payload_objects.json')

WEARABLE = {'Costumes', 'Accessories', 'Mounts & Pets', 'Weapon Skins'}
CUSTOM = {'Eyes & Face', 'Hair'}
INTERFACE = {'HUD & Combat', 'Windows & Menus', 'Chat & Alerts',
             'Performance & FX', 'Removers', 'Sounds & Voice'}

ID_RE = re.compile(r'#(\d{3,7})')
RANGE_RE = re.compile(r'#(\d{3,7})\s*[-–]\s*#(\d{3,7})')
SLOT_RE = re.compile(r'\b(face|hair(?:style)?|adornment|preset|tail|horn|ear)s?\b'
                     r'[^.#]{0,20}?(\d+(?:\s*(?:-|and|,)\s*\d+)*)', re.I)
RACE_RE = re.compile(r'\b(elin|popori|castanic|aman|high[\s-]?elf|human|baraka)\b', re.I)
RACE_KEY = {'elin': 'elin', 'popori': 'elin', 'castanic': 'castanic', 'aman': 'aman',
            'highelf': 'highelf', 'high elf': 'highelf', 'high-elf': 'highelf',
            'human': 'human', 'baraka': 'baraka'}


# Everything the renderer appends. The summary must never swallow it, or a
# second migration run makes the rendered tail part of the summary and the two
# compound. Migration has to be idempotent -- it will be run again.
RENDERED_TAIL = re.compile(
    r'\s*(?:Replaces\s+[^.]*#\d|Wearable by|Character creator|Changes\s+[A-Z])', re.I)


def first_sentence(text):
    cut = RENDERED_TAIL.search(text)
    if cut and cut.start() > 12:
        text = text[:cut.start()]
    m = re.match(r'\s*(.+?[.!])(\s|$)', text)
    s = (m.group(1) if m else text).strip()
    s = re.sub(r'\s+', ' ', s)
    if len(s) > 200:
        s = s[:197].rstrip() + '...'
    if not s.endswith(('.', '!')):
        s += '.'
    return (s[0].upper() + s[1:]) if s else s


def expand_ids(text):
    """Every id the sentence mentions. A written range is expanded and each
    member checked individually -- ranges hid non-items in the interior."""
    ids = []
    for a, b in RANGE_RE.findall(text):
        a, b = int(a), int(b)
        if 0 < b - a <= 64:
            ids.extend(range(a, b + 1))
        else:
            ids.extend([a, b])
    ids.extend(int(x) for x in ID_RE.findall(text))
    return sorted(set(ids))


def build_targets(text, index, problems, mid):
    """Group the sentence's ids by the race+gender the DATACENTER gives them."""
    by = collections.OrderedDict()
    unknown = []
    for i in expand_ids(text):
        info = index.get(str(i))
        if not info or not info.get('name'):
            unknown.append(i)
            continue
        key = (info['race'], info['gender'])
        by.setdefault(key, []).append({'id': i, 'name': info['name']})
    if unknown:
        problems[f'ids not in the datacenter'].append((mid, unknown[:6]))
    return [{'race': r, 'gender': g, 'items': items} for (r, g), items in by.items()]


def build_slots(text):
    race = RACE_RE.search(text)
    gender = re.search(r'\b(male|female)\b', text, re.I)
    out = []
    for m in SLOT_RE.finditer(text):
        kind = m.group(1).lower()
        kind = 'hair' if kind.startswith('hair') else kind
        nums = sorted({int(n) for n in re.findall(r'\d+', m.group(2)) if 1 <= int(n) <= 999})
        if not nums or not race:
            continue
        out.append({'kind': kind, 'numbers': nums,
                    'race': RACE_KEY.get(race.group(1).lower().replace('-', ' '), 'any'),
                    'gender': (gender.group(1).lower() if gender else 'any')})
    return out


def tmm_object_names(entry, tmm):
    """Vanilla object names from a tmm payload's footer."""
    rec = (tmm or {}).get(entry.get('id')) or {}
    out = []
    for path in rec.get('names') or []:
        p = path[4:] if path.startswith('MOD:') else path
        bits = p.split('.')
        if len(bits) >= 3:
            out.append(FILENAME_SUFFIX.sub('', bits[-1]))   # the object
            out.append(bits[0])                             # the composite uid
        pkg = rec.get('packages') or []
        out.extend(pkg)
    return out


TEX_SUFFIX = re.compile(r'_(?:diff|norm|spec|mask|emis|rage|cstm|MI|Tex|skel|Skel)$', re.I)


def object_package_names(entry):
    """Package names recovered from the payload's own exports."""
    out = []
    for path in OBJECT_MAP.get(entry.get('id')) or []:
        obj = path.rsplit('.', 1)[-1]
        out.append(TEX_SUFFIX.sub('', obj))
        if '.' in path:
            out.append(path.split('.', 1)[0])
    return out


def package_names(entry, tmm=None):
    """Package names this entry ships, top level plus parts, bare and suffixed.
    The DC is keyed by the BARE name, so `PC_Event_73_dup.gpk` never matched
    and 19 costumes were filed as unresolvable when the DC knew them."""
    out = []
    for owner in [entry] + (entry.get('parts') or []):
        for g in owner.get('gpk_files') or []:
            name = re.sub(r'\.gpk$', '', g, flags=re.I)
            out.append(name)
            bare = FILENAME_SUFFIX.sub('', name)
            if bare != name:
                out.append(bare)
        for path in filter(None, [owner.get('target_object_path')]):
            tail = path.split('.')[-1]
            out.append(FILENAME_SUFFIX.sub('', tail))
        # A dropin's target filename IS the vanilla package name, which is
        # exactly what the datacenter is keyed by -- `PC_Event_53.gpk` ->
        # `PC_Event_53`, 10 parts. 167 entries were unresolvable purely
        # because this field was never read.
        drop = owner.get('target_dropin_filename')
        if drop:
            out.append(re.sub(r'\.gpk$', '', drop, flags=re.I))
        loose = owner.get('target_loose_path')
        if loose:
            out.append(re.sub(r'\.gpk$', '', os.path.basename(loose), flags=re.I))
    out.extend(tmm_object_names(entry, tmm))
    rec = (PAYLOAD_PKGS or {}).get(entry.get('id')) or {}
    out.extend(rec.get('packages') or [])
    out.extend(rec.get('objects') or [])
    out.extend(object_package_names(entry))
    return out


def targets_from_package(entry, resolver, index, tmm=None):
    """Items reachable from the packages this entry ships."""
    if not resolver:
        return []
    a2p, l2i = resolver['asset2parts'], resolver['look2items']
    ids = set()
    for n in package_names(entry, tmm):
        for part in a2p.get(n) or []:
            for it in l2i.get(part) or []:
                iid = it[0] if isinstance(it, (list, tuple)) else it
                ids.add(str(iid))
        for iid in ((ICON_MAP.get(n) or []) + (MOUNT_MAP.get(n) or [])
                    + (WEAPON_MAP.get(n) or []) + (FISHING_MAP.get(n) or [])):
            ids.add(str(iid))
    by = collections.OrderedDict()
    for iid in sorted(ids, key=int):
        info = index.get(iid)
        if not info or not info.get('name'):
            continue
        by.setdefault((info['race'], info['gender']), []).append(
            {'id': int(iid), 'name': info['name']})
    return [{'race': r, 'gender': g, 'items': items} for (r, g), items in by.items()]


def convert(entry, index, problems, resolver=None, tmm=None):
    # Idempotency without losing information: a previous run already reduced
    # `replaces` to the rendered form, whose summary no longer carries the ids.
    # So re-use the structured targets when they exist, and only ever parse the
    # ORIGINAL prose for ids. Reading the summary back in dropped 207 entries'
    # ids on the second run.
    prior = entry.get('replaces_data') or {}
    text = (entry.get('replaces') or '').strip()
    cat = entry.get('category') or ''
    mid = entry.get('id', '?')
    if not text:
        problems['empty replaces'].append((mid, ''))
        return None
    data = {'summary': prior.get('summary') or first_sentence(text)}
    # `objects` is read out of the payload by a separate pipeline and verified
    # against it by the gate; nothing here can re-derive it, so preserve it or
    # the next migration silently un-resolves every entry that has one.
    for keep in ('targets', 'slots', 'loose', 'objects'):
        if prior.get(keep):
            data[keep] = prior[keep]
    if data.get('targets') or data.get('slots') or data.get('loose'):
        return data
    if data.get('objects'):
        return data

    if cat in WEARABLE:
        t = build_targets(text, index, problems, mid)
        if not t:
            t = targets_from_package(entry, resolver, index, tmm)
        if not t:
            problems['wearable with no resolvable item id'].append((mid, text[:50]))
            return data
        data['targets'] = t
        return data

    if cat in CUSTOM:
        t = build_targets(text, index, problems, mid)
        if t:
            data['targets'] = t
            return data
        s = build_slots(text)
        if not s:
            problems['customization with no slot+race'].append((mid, text[:50]))
            return data
        data['slots'] = s
        return data

    if cat in INTERFACE:
        data['loose'] = [entry.get('name', '').strip() or 'interface element']
        return data

    problems[f'unhandled category {cat!r}'].append((mid, ''))
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    index = json.loads(io.open(os.path.join(HERE, 'item_index.json'), 'rb').read())
    global PAYLOAD_PKGS, ICON_MAP, MOUNT_MAP, WEAPON_MAP, FISHING_MAP, OBJECT_MAP
    if os.path.exists(PAYLOAD_OBJECTS):
        OBJECT_MAP = json.loads(io.open(PAYLOAD_OBJECTS, 'rb').read())
        print(f'payload objects: {len(OBJECT_MAP)} entries')
    if os.path.exists(FISHING_INDEX):
        FISHING_MAP = json.loads(io.open(FISHING_INDEX, 'rb').read())
        print(f'fishing index: {len(FISHING_MAP)} packages')
    if os.path.exists(WEAPON_INDEX):
        WEAPON_MAP = json.loads(io.open(WEAPON_INDEX, 'rb').read())
        print(f'weapon index: {len(WEAPON_MAP)} packages')
    if os.path.exists(MOUNT_INDEX):
        MOUNT_MAP = json.loads(io.open(MOUNT_INDEX, 'rb').read())
        print(f'mount index: {len(MOUNT_MAP)} packages')
    if os.path.exists(ICON_INDEX):
        ICON_MAP = json.loads(io.open(ICON_INDEX, 'rb').read())
        print(f'icon index: {len(ICON_MAP)} packages')
    if os.path.exists(PAYLOAD_PACKAGES):
        PAYLOAD_PKGS = json.loads(io.open(PAYLOAD_PACKAGES, 'rb').read())
        print(f'payload scans: {len(PAYLOAD_PKGS)} entries')
    tmm = {}
    if os.path.exists(TMM_OBJECTS):
        tmm = json.loads(io.open(TMM_OBJECTS, 'rb').read())
        print(f'tmm footers: {len(tmm)} payloads')
    resolver = None
    if os.path.exists(RESOLVER):
        resolver = json.loads(io.open(RESOLVER, 'rb').read())
        print(f"resolver: {len(resolver['asset2parts']):,} assets, "
              f"{len(resolver['look2items']):,} looks")
    raw = io.open(os.path.join(ROOT, 'catalog.json'), 'rb').read().decode('utf-8')
    nl = '\r\n' if '\r\n' in raw else '\n'
    doc = json.loads(raw)

    problems = collections.defaultdict(list)
    ok = 0
    for m in doc['mods']:
        if m.get('kind') == 'external':
            continue
        data = convert(m, index, problems, resolver, tmm)
        if not data:
            continue
        m['replaces_data'] = data
        m['replaces'] = render_replaces.render(data)     # regenerated, never hand-written
        if data.get('targets') or data.get('slots') or data.get('loose'):
            ok += 1

    total = len([m for m in doc['mods'] if m.get('kind') != 'external'])
    print(f'{ok}/{total} entries now carry structured replaces_data\n')
    for kind in sorted(problems, key=lambda k: -len(problems[k])):
        rows = problems[kind]
        print(f'  {kind}  ({len(rows)})')
        for mid, detail in rows[:6]:
            print(f'     {mid}{"  " + str(detail) if detail else ""}')
        if len(rows) > 6:
            print(f'     ... and {len(rows) - 6} more')
        print()

    if args.write:
        io.open(os.path.join(ROOT, 'catalog.json'), 'w', encoding='utf-8',
                newline=nl).write(json.dumps(doc, indent=1, ensure_ascii=False) + '\n')
        print('catalog.json written')
    else:
        print('dry run -- pass --write to apply')
    return 0


if __name__ == '__main__':
    sys.exit(main())
