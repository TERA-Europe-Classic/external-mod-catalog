"""Render `replaces_data` into the lines a player reads.

    Thunor's Armor (Elin)   (#271132)
    Woden's Armor (Elin)    (#271139)

ONE renderer. CI asserts every entry's stored `replaces` string equals this
function's output, so the copy cannot drift from the data and nobody writes a
sentence by hand. 584 entries each hand-written is why the field read
differently on every mod.

Keep in sync with renderReplaces() in the launcher's mods.js.
"""
import re

RACE_LABEL = {
    'human': 'Human', 'highelf': 'High Elf', 'aman': 'Aman', 'castanic': 'Castanic',
    'elin': 'Elin', 'popori': 'Elin', 'baraka': 'Baraka', 'any': 'All races',
}
GENDER_LABEL = {'male': 'Male', 'female': 'Female', 'any': ''}


def _who(t):
    """"Elin" / "Castanic Female" / "All races". The datacenter already bakes
    the race into most costume names ("Thunor's Armor (Elin)"), so the gender
    is only worth adding when it actually distinguishes something."""
    race = RACE_LABEL.get(t.get('race', 'any'), t.get('race', ''))
    gender = GENDER_LABEL.get(t.get('gender', 'any'), '')
    return f'{race} {gender}'.strip() if gender else race


RACE_WORDS = ('Elin', 'Popori', 'Castanic', 'Aman', 'High Elf', 'Human', 'Baraka')

# One mount ships as dozens of items that differ only by rarity tier:
#   Flying Skill: Carnelian Koinobori
#   Flying Skill: Mythical Carnelian Koinobori
#   Flying Skill: Legendary Carnelian Koinobori   ... 311 in total for Koinobori
# All of them are the same mount and the mod changes all of them, so listing
# each is accurate and useless. Strip the tier word and they collapse to three
# rows -- one per actual colour.
RARITY = re.compile(
    r'\b(?:Legendary|Mythical|Fabled|Chimeric|Almighty|Gilded|Superior|Exalted)\s+',
    re.I)


def collapse(name):
    return RARITY.sub('', name).strip()


def item_lines(data):
    """[(label, "(#id)")] -- Lukas's format:

        Thunor's Armor (Elin)   (#271132)
        Woden's Armor (Elin)    (#271139)

    One row per DISTINCT item name. The datacenter gives the same costume
    several ids (one per dye state), and printing "Chambermaid's Dress" four
    times over is noise -- the ids collapse onto one row instead.

    The race is appended only when the name does not already carry it. Most
    costume names do ("Thunor's Armor (Elin)"), and saying it twice reads as
    "Thunor's Armor (Elin) (Elin Female)".
    """
    rows = []
    for t in data.get('targets') or []:
        who = _who(t)
        race_label = RACE_LABEL.get(t.get('race', 'any'), '')
        seen = {}
        for it in t['items']:
            name = it['name']
            name = collapse(name)
            has_race = any(f'({w})' in name for w in RACE_WORDS) or race_label in name
            label = name if has_race else f'{name} ({who})'
            seen.setdefault(label, []).append(it['id'])
        for label, ids in seen.items():
            rows.append((label, '(' + ', '.join(f'#{i}' for i in ids) + ')'))
    return rows


def slot_lines(data):
    """One row per WHO, not per number.

        Face 1, Adornment 8 (Castanic Female)

    A face mod that touches a face and an adornment used to print
    "Face 1 (Castanic Female); Adornment 8 (Castanic Female)" -- the same
    person named twice for one edit. Slots are grouped by who they belong to
    and the race is said once, at the end, where the item rows already put it.
    """
    by_who = {}
    for s in data.get('slots') or []:
        kind = s['kind'].capitalize()
        by_who.setdefault(_who(s), []).extend(f'{kind} {n}' for n in s['numbers'])
    return [(f'{", ".join(slots)} ({who})' if who else ', '.join(slots), '')
            for who, slots in by_who.items()]


def object_lines(data):
    """What the player sees, for the things the game does not sell.

    The `what` is shown, never the path. "Partner_C_CoCo_Event00.Skel.
    Partner_C_CoCo_Event01_Skel" is the proof, not the copy -- one distinct
    row per description, because a mod that repaints one pet across eight
    textures replaces one visible thing.
    """
    rows, seen = [], set()
    for o in data.get('objects') or []:
        w = unlead(o['what'])
        if w and w not in seen:
            seen.add(w)
            rows.append((w, ''))
    return rows


LEAD_VERB = re.compile(r'^(?:replaces|changes|swaps|replace)\s+', re.I)


def unlead(text):
    """Strip a leading "Replaces "/"Changes " and recase what is left.

    The launcher prints the word REPLACES in the label column immediately to
    the left, so a value beginning "Replaces the chat window" reads "REPLACES
    Replaces the chat window".
    """
    out = LEAD_VERB.sub('', text.strip())
    return out[:1].upper() + out[1:] if out else ''


def loose_lines(data):
    """UI mods are the one freeform case, and their `loose` list is not it.

    A window restyle has no item id, no slot and no character -- there is
    nothing to tabulate, so what it replaces has to be described. `loose`
    holds the MOD'S OWN NAME ("Centered Clean Message Window"), which the
    detail panel already prints as the title two rows up; the description
    lives in `summary`. So for these, and only these, the summary is the copy.
    """
    summary = unlead(data.get('summary') or '')
    if summary:
        return [(summary, '')]
    return [(name.strip(), '') for name in data.get('loose') or [] if name.strip()]


def rows(data):
    """Every row this entry shows, in one list, in one shape: (label, ids).

    The four kinds are four ways of NAMING a thing, not four formats. A costume
    knows its item ids, a character-creation slot does not and never will, a pet
    recolor has neither -- so the id half is empty for some rows and that is the
    only difference between them.
    """
    named = item_lines(data) + slot_lines(data) + object_lines(data)
    if named:
        # An entry that can NAME what it replaces says only that. The prose
        # would repeat it -- which is what "the castanic female face decal at
        # Face 1, Adornment 8 ... Character creator -- Adornment 8 (Castanic
        # Female)" was.
        return named
    # Only a declared `loose` earns the freeform line. Without that guard an
    # entry that declares NOTHING -- `flying.mount-mod`, whose payload nobody
    # can explain -- would render its summary and read like a working mod.
    return loose_lines(data) if data.get('loose') else []


def render(data):
    """The one string every mod gets. Same shape for all 584.

        Thunor's Armor (Elin) (#271132); Woden's Armor (Elin) (#271139)
        Face 1, Adornment 8 (Castanic Female)
        Face 10 (Elin)

    `summary` is deliberately NOT rendered. It is the one free-text field in
    `replaces_data`, it was written by hand per entry, and it is the whole
    reason the field read differently on every mod: one entry opened "the
    castanic female face decal at Face 1, Adornment 8 in character creation"
    and the next "Replaces Elin face preset 10, the whole face texture for that
    character-creation face" -- both then repeating the slot they had just
    described. It stays in the data, where search still reads it, and out of
    the copy.

    No lead-in verb either. The field is labelled REPLACES in the launcher, so
    "Replaces ..." said it twice, and "Character creator --" vs "Changes ..."
    made the same kind of edit look like three different kinds.
    """
    if not data:
        return ''
    return '; '.join(f'{lbl} {ident}'.strip() for lbl, ident in rows(data))


if __name__ == '__main__':
    import io, json, os, sys
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mods = json.loads(io.open(os.path.join(root, 'catalog.json'), 'rb').read())['mods']
    want = sys.argv[1] if len(sys.argv) > 1 else None
    for m in mods:
        if want and m['id'] != want:
            continue
        d = m.get('replaces_data')
        if not d:
            continue
        print(m['id'])
        for lbl, ident in item_lines(d) + slot_lines(d) + object_lines(d):
            print(f'    {lbl:<44} {ident}')
        print()
