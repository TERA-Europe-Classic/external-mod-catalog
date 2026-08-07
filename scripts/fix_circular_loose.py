"""Name what a UI mod replaces, instead of repeating its own title.

142 entries declared a loose target that was just the mod's name -- "Pixel Moon
Block" replaces "Pixel Moon Block". That reads fine in the catalog and is
useless in the verification sheet, where it becomes "in game, look at Pixel Moon
Block" and tells a tester nothing about where to look.

The target objects already say what the mod touches, so the description is
derived from those rather than hand-written 142 times: an S1UI_<Window> target
becomes "the <window> window" by splitting the CamelCase, and the handful of
objects whose names are not self-describing get an explicit phrase.
"""
import collections
import difflib
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CATALOG = os.path.join(HERE, '..', 'catalog.json')

# objects whose name does not tell a player where to look
EXPLICIT = {
    'Message_I*': 'the Defense Success (block) popup',
    'Message': 'the on-screen message popups',
    'TexturedFonts': 'the in-game text, which uses these fonts everywhere',
    'Crosshair_I5': 'the aiming crosshair',
    'normalBg': 'the aiming crosshair background',
    'hp': 'the HP bar in the character window',
    'hp1': 'the HP bar in the character window',
    'mp': 'the MP bar in the character window',
    'LoadingProgress_I1': 'the loading progress bar',
    'LoadingSymbols': 'the loading screen symbols',
    'ProgressBar': 'the quest tracker progress bar',
    'GageBoss': 'the boss HP gauge',
    'PaperDoll': 'the equipment paper doll',
    'CommonComponent': 'the shared window chrome',
    'Icon_Items': 'the item icons',
    'Icon_System': 'the system icons',
    'Icon_Equipments': 'the equipment icons',
    'Icon_Skills': 'the skill icons',
    'FX_Enchant': 'the enchanting visual effects',
    'Abnormality': 'the buff and debuff bar',
    'Benefit': 'the rewards and benefits window',
}

# An FPS pack strips a class's awakening effects; the class is in the name.
FX_AWAKEN = re.compile(r'^FX_Awaken_([A-Za-z]+)$')


def phrase(obj):
    if obj in EXPLICIT:
        return EXPLICIT[obj]
    fx = FX_AWAKEN.match(obj)
    if fx:
        return 'the awakening visual effects for %s' % fx.group(1).lower()
    name = re.sub(r'^S1UI_', '', obj)
    name = re.sub(r'_I\*$', '', name)
    # Only a real CamelCase window name earns "the <x> window". Internal asset
    # names -- hp1_abnormal, hpEff, st -- are not windows, and appending the
    # word produced instructions like "look at the st window". Better to say
    # nothing about a part than to invent a place to look.
    if '_' in name or len(name) < 5 or not re.match(r'^[A-Z][a-z]+[A-Z]', name):
        return None
    words = re.sub(r'(?<!^)(?=[A-Z])', ' ', name).lower().strip()
    if not words:
        return None
    if words.endswith((' window', ' popup', ' bar', ' gauge')):
        return 'the ' + words
    return 'the ' + words + ' window'


def targets_of(m):
    out = []
    srcs = [str(p.get('target_object_path') or p.get('target_loose_path') or '')
            for p in (m.get('parts') or [])]
    srcs += [str(m.get('target_object_path') or ''), str(m.get('target_dropin_filename') or '')]
    # a tmm entry keeps its targets here rather than in parts
    srcs += [str(x) for x in (m.get('tmm_object_paths') or [])]
    for t in srcs:
        if not t:
            continue
        if t.lower().endswith(('.gpk', '.bin')):
            out.append(os.path.basename(t).rsplit('.', 1)[0])
        else:
            o = re.sub(r'_dup$', '', t.split('.')[-1])
            out.append(re.sub(r'_I[0-9A-F]{2,4}$', '_I*', o))
    return sorted(set(out))


def norm(s):
    return re.sub(r'[^a-z0-9 ]', '', (s or '').lower()).strip()


def is_circular(m):
    loose = [str(x) for x in ((m.get('replaces_data') or {}).get('loose') or [])]
    if not loose:
        return False
    a, b = norm(loose[0]), norm(m['name'])
    return a == b or difflib.SequenceMatcher(None, a, b).ratio() > 0.8


def main(write=True):
    j = json.loads(io.open(CATALOG, encoding='utf-8').read())
    mods = j.get('mods') if isinstance(j, dict) else j
    fixed, unresolved = 0, []
    for m in mods:
        if not is_circular(m):
            continue
        phrases = [p for p in (phrase(t) for t in targets_of(m)) if p]
        # drop the S1UI_X duplicate of X
        seen, uniq = set(), []
        for p in phrases:
            if p not in seen:
                seen.add(p)
                uniq.append(p)
        if not uniq:
            unresolved.append(m['id'])
            continue
        m['replaces_data']['loose'] = uniq
        fixed += 1
    if write:
        io.open(CATALOG, 'w', encoding='utf-8').write(json.dumps(j, ensure_ascii=False, indent=1))
    print('rewrote %d circular loose targets' % fixed)
    if unresolved:
        print('%d could not be derived from their targets: %s'
              % (len(unresolved), unresolved[:8]))
    return 0


if __name__ == '__main__':
    sys.exit(main(write='--dry-run' not in sys.argv))
