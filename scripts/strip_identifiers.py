# -*- coding: utf-8 -*-
"""#11 — get raw underscored engine identifiers out of user-facing copy.

- Drop parenthetical raw identifiers that carry an underscore and no numeric
  item id: "(package Popori_F_AH0004)", "(S1UI_Message)", "(Awaken_SpiritKing)"
  — they duplicate the GPK files row and mean nothing to a player.
- "the PC_Event_16 costume set" -> "the costume set" (the item names + #ids
  stay).
- Any remaining underscored token in the short visible fields is spaced out,
  honouring "spaces, not underlines" (e.g. leading decal slot names).

Numeric item ids (#81159) are always kept — they're the one technical bit the
maintainer wants shown for testing.
"""
import sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import catalog_io as C

PAREN = re.compile(r'\s*\((?:package\s+)?[^)#]*_[^)#]*\)')
SET = re.compile(r'\bthe \w+_\w[\w_]* costume set')
TOKEN = re.compile(r'\b[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+\b')

def despace(text):
    return re.sub(r'  +', ' ', text).replace(' .', '.').replace(' ,', ',').strip()

def strip_paren(text):
    if not text:
        return text
    text = PAREN.sub('', text)
    text = SET.sub('the costume set', text)
    return despace(text)

def space_tokens(text):
    if not text:
        return text
    return despace(TOKEN.sub(lambda m: m.group(0).replace('_', ' '), text))

def main():
    d = C.load()
    np = nt = 0
    for m in d['mods']:
        for f in ('replaces', 'long_description', 'short_description', 'tagline'):
            v = m.get(f)
            if not v:
                continue
            nv = strip_paren(v)
            if nv != v:
                m[f] = nv; np += 1
        # residual underscored tokens only in the short, most-visible fields
        for f in ('replaces', 'short_description', 'tagline'):
            v = m.get(f)
            if v and TOKEN.search(v):
                nv = space_tokens(v)
                if nv != v:
                    m[f] = nv; nt += 1
    d['version'] += 1
    C.save(d)
    print(f'parenthetical/set strips: {np}  residual-token spacings: {nt}  version {d["version"]}')

if __name__ == '__main__':
    main()
