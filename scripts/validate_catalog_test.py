"""An entry that says it is broken is exempt from declaring what it replaces.

The gate's own docstring promises "every entry declares what it replaces, or
says why not". The second half was never implemented, so one entry whose
payload nobody can explain -- `flying.mount-mod`, described as a mount but
exporting 14 loading-bar objects -- held the whole workflow red. A gate that is
permanently red stops being read, which costs more than the entry it blocks.

The exemption is narrow on purpose: it waives ONLY the "which declaration form"
rule. A broken entry with a genuinely malformed `replaces_data` -- a bad race,
an unknown property, an invented item id -- still fails, or `broken` would
become the way to skip validation entirely.

    python scripts/validate_catalog_test.py
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import validate_catalog as V                                       # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

PASSED = []
FAILED = []


def it(name):
    def deco(fn):
        try:
            fn()
            PASSED.append(name)
        except AssertionError as e:                                # noqa: BLE001
            FAILED.append((name, str(e)))
        return fn
    return deco


def base_entry(**over):
    """A Costume-shaped entry, the category whose anyOf demands a target form."""
    e = {
        'id': 'test.entry',
        'kind': 'gpk',
        'name': 'Test',
        'author': 'Nobody',
        'short_description': 'A test costume entry.',
        'license': 'Unknown',
        'credits': 'Created by nobody; fixture only.',
        'version': '1.0.0',
        'download_url': 'https://example.invalid/a.gpk',
        'sha256': 'a' * 64,
        'category': 'Costumes',
        'deploy_strategy': 'tmm',
        # An entry with nothing to name renders nothing. `render()` refuses to
        # turn a bare summary into copy, so a broken entry cannot read like a
        # working one.
        'replaces': '',
        'replaces_data': {'summary': 'Replaces a costume.'},
    }
    e.update(over)
    return e


VALIDATOR = V.load_validator()


@it('a bare replaces_data fails when the entry does not say it is broken')
def _():
    errs = V.check(base_entry(), VALIDATOR, {}, {})
    assert any('replaces_data' in e for e in errs), \
        f'expected the shape rule to block it, got {errs!r}'


@it('the same entry passes once `broken` explains why it cannot declare one')
def _():
    errs = V.check(base_entry(broken='The payload does not match this entry.'),
                   VALIDATOR, {}, {})
    assert not errs, f'broken entries are exempt from the shape rule, got {errs!r}'


@it('`broken` does not waive a malformed replaces_data')
def _():
    bad = base_entry(broken='Unknown payload.')
    bad['replaces_data'] = {'summary': 'x', 'not_a_real_key': 1}
    errs = V.check(bad, VALIDATOR, {}, {})
    assert errs, 'an unknown property must still fail, broken or not'


@it('`broken` does not waive an invented item id')
def _():
    bad = base_entry(broken='Unknown payload.')
    bad['replaces_data'] = {
        'summary': 'x',
        'targets': [{'race': 'elin', 'gender': 'female',
                     'items': [{'id': 999999, 'name': 'Nope'}]}],
    }
    errs = V.check(bad, VALIDATOR, {}, {})
    assert any('does not exist in the datacenter' in e for e in errs), \
        f'the datacenter check must still run, got {errs!r}'


@it('an empty `broken` string is not an exemption')
def _():
    errs = V.check(base_entry(broken='   '), VALIDATOR, {}, {})
    assert any('replaces_data' in e for e in errs), \
        'blank text explains nothing and must not open the gate'


@it('the live catalog passes the gate end to end')
def _():
    mods = json.loads(io.open(os.path.join(ROOT, 'catalog.json'), 'rb').read())['mods']
    index = json.loads(io.open(os.path.join(HERE, 'item_index.json'), 'rb').read())
    pf = os.path.join(HERE, 'object_proof.json')
    proof = json.loads(io.open(pf, 'rb').read()) if os.path.exists(pf) else {}
    bad = {m['id']: V.check(m, VALIDATOR, index, proof) for m in mods}
    bad = {k: v for k, v in bad.items() if v}
    assert not bad, f'{len(bad)} entries still fail: {list(bad)[:5]}'


if __name__ == '__main__':
    for n, why in FAILED:
        print(f'FAIL  {n}\n      {why}')
    print(f'validate_catalog_test: {len(PASSED)} passed, {len(FAILED)} failed')
    sys.exit(1 if FAILED else 0)
