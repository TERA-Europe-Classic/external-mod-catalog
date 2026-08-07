# -*- coding: utf-8 -*-
"""One-pass user-facing copy cleanup over every catalog entry:

- long_description: drop the leading '**Replaces:** ...' block (it duplicates
  the Replaces detail row shown separately), strip the rehost boilerplate
  sentence, and rephrase 'Check: X' testing hints into natural prose.
- replaces / short_description: rephrase the 'Check: X' hints.

The 'Check:' hints carry useful in-game verification info, so they are kept —
only the terse 'Check:' label the maintainer flagged is rewritten.
"""
import sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import catalog_io as C

VERB = ('preview', 'open', 'wear', 'fish', 'summon', 'equip', 'check', 'look', 'use', 'ride', 'enter')

def rephrase_check(text):
    if not text or 'Check:' not in text:
        return text
    def fix(m):
        cont = m.group(1).strip().replace('preview/wear', 'preview or wear')
        low = cont.lower()
        if low.startswith(VERB):
            body = cont
        elif low.startswith(('a ', 'an ')):
            body = 'check ' + cont
        else:
            body = 'check the ' + cont
        return 'To confirm it applied, ' + body
    return re.sub(r'Check:\s*([^.\n]*)', fix, text)

def clean_long(ld):
    if not ld:
        return ld
    ld = re.sub(r'^\*\*Replaces:\*\*[^\n]*(?:\n\n|\n|$)', '', ld, count=1)
    ld = rephrase_check(ld)
    ld = re.sub(r'\s*Install, enable,? and launch the game[^.]*needed\.', '', ld)
    return ld.strip()

def main():
    d = C.load()
    n_long = n_rep = n_short = 0
    for m in d['mods']:
        ld = m.get('long_description')
        if ld:
            nl = clean_long(ld)
            if nl != ld:
                m['long_description'] = nl; n_long += 1
        rep = m.get('replaces')
        if rep:
            nr = rephrase_check(rep)
            if nr != rep:
                m['replaces'] = nr; n_rep += 1
        sd = m.get('short_description')
        if sd:
            ns = rephrase_check(sd)
            if ns != sd:
                m['short_description'] = ns; n_short += 1
    d['version'] += 1
    C.save(d)
    print(f'long_description cleaned: {n_long}  replaces: {n_rep}  short: {n_short}  version {d["version"]}')

if __name__ == '__main__':
    main()
