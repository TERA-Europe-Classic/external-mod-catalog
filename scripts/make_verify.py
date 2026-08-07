"""Regenerate VERIFY.md -- the in-game verification sheet.

One row per mod that is published, unbroken and awaiting in-game verification,
with the shortest instruction that proves it: the first audited item id, plus
the dye caveat where the change only shows dyed. Coverage state comes from the
converter sweep when present: a mod whose recorded parts miss a package its
textures live in is listed as needing a rebuild, not a test.

    python scripts/make_verify.py
"""
import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SWEEP = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Temp',
                     'claude', 'scratch', 'sweep_gaps.json')


def first_target(m):
    rd = m.get('replaces_data') or {}
    for t in rd.get('targets') or []:
        for it in t.get('items') or []:
            race = t.get('race', 'any')
            who = 'any race' if race == 'any' else f"{race} {t.get('gender', '')}".strip()
            return f"equip {it['name']} #{it['id']} ({who})"
    # a creator-slot mod is verified in the character creator, not a wardrobe
    for s in rd.get('slots') or []:
        nums = ', '.join(str(n) for n in s.get('numbers', []))
        return (f"character creator: {s.get('race', 'any')} {s.get('gender', '')}".strip()
                + f", pick {s.get('kind', 'slot')} {nums}")
    # object-declared mods carry their own human phrasing in the summary
    if rd.get('objects') and (rd.get('summary') or '').strip():
        return 'look at: ' + rd['summary'].strip().rstrip('.')
    # A loose target is already written the way a player would look for it --
    # "the shield art on the Defense Success popup", "the character select and
    # creation music". Ignoring it sent 70 UI mods to the sheet with "observe
    # the change the title describes", which tells a tester nothing about where
    # to look and made an eleventh of the deliverable useless.
    loose = [str(x).strip() for x in (rd.get('loose') or []) if str(x).strip()]
    if loose:
        what = loose[0].rstrip('.')
        if len(loose) > 1:
            what += f" (and {len(loose) - 1} more)"
        return 'in game, look at ' + what
    s = m.get('replaces') or ''
    mm = re.search(r'([A-Za-z][^;(]{2,40})\(#(\d+)', s)
    return f"equip {mm.group(1).strip()} #{mm.group(2)}" if mm else None


def main():
    cat = json.loads(io.open(os.path.join(ROOT, 'catalog.json'), 'rb').read())['mods']
    gaps = {}
    if os.path.exists(SWEEP):
        gaps = json.loads(io.open(SWEEP, 'rb').read())
    ready, needs_rebuild, verified, blocked = [], [], [], []
    for m in sorted(cat, key=lambda x: x['id']):
        # Every mod appears somewhere. A sheet that silently drops the broken
        # ones answers "what can I test?" but not "where does this mod stand?",
        # and the second question is the one that shows whether the campaign is
        # finishing. Broken entries carry the first sentence of their own
        # diagnosis so the list doubles as the fix backlog.
        b = (m.get('broken') or '').strip()
        if b:
            # An entry that has been rebuilt and republished is testable NOW --
            # its flag exists only until someone confirms it. Burying it in the
            # being-fixed table is how the dance and the wings got tested on
            # their old builds.
            mm = re.search(r'RETEST[: ]+(.+?)(?:\.\s|$)', b, re.S)
            if mm and 'republished' in b:
                ready.append(f"| {m['name'][:44]} | `{m['id']}` | "
                             f"{' '.join(mm.group(1).split())[:120]} |")
                continue
            why = b.split('. ')[0].rstrip('.')
            blocked.append(f"| {m['name'][:40]} | `{m['id']}` | {why[:150]} |")
            continue
        if not (m.get('parts') or m.get('download_url')):
            blocked.append(f"| {m['name'][:40]} | `{m['id']}` | no payload attached yet |")
            continue
        instr = first_target(m) or 'install, restart, observe the change the title describes'
        if 'dye' in (m.get('compatibility_notes') or '').lower():
            instr += ' and DYE it (undyed matches vanilla)'
        row = f"| {m['name'][:44]} | `{m['id']}` | {instr} |"
        if m.get('last_verified'):
            verified.append(row)
        elif m['id'] in gaps:
            needs_rebuild.append(row)
        else:
            ready.append(row)
    can_f = os.path.join(HERE, '_canaries.json')
    canaries = json.loads(io.open(can_f, 'rb').read()) if os.path.exists(can_f) else {}
    by_id = {m['id']: m for m in cat}
    pinned = []
    for cid, c in canaries.items():
        if by_id.get(cid, {}).get('last_verified'):
            continue          # verdict in -- it graduates off the pinned list
        pinned.append(f"| {by_id.get(cid, {}).get('name', cid)[:40]} | `{cid}` "
                      f"| {c['test']} | {c['gates']} |")

    doc = ['# In-game verification sheet', '',
           'Close TERA before toggling. The client reads the mapper once at launch, so',
           'restart after every install or enable. On any crash: stop and report;',
           'Launch.log names the failing package.', '',
           f'## Test these first -- each verdict gates a class ({len(pinned)})', '',
           '| Mod | id | What to do | What it unlocks |', '|---|---|---|---|',
           *pinned, '',
           f'## Ready for verification ({len(ready)})', '',
           '| Mod | id | What to do |', '|---|---|---|', *ready, '',
           f'## Held back -- rebuild in progress ({len(needs_rebuild)})', '',
           '| Mod | id | What to do |', '|---|---|---|', *needs_rebuild, '',
           f'## Verified ({len(verified)})', '',
           '| Mod | id | What to do |', '|---|---|---|', *verified, '',
           f'## Not yet installable -- being fixed ({len(blocked)})', '',
           'Every entry here names why it cannot ship. Nothing is abandoned;',
           'each line is a fix in the queue, worked by class.', '',
           '| Mod | id | Why it is held |', '|---|---|---|', *blocked, '']
    io.open(os.path.join(ROOT, 'VERIFY.md'), 'w', encoding='utf-8',
            newline='\n').write('\n'.join(doc))
    print(f'{len(blocked)} being fixed, {len(ready)} ready, '
          f'{len(needs_rebuild)} held for rebuild, '
          f'{len(verified)} verified')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
