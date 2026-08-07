"""Tests for the entry-schema guard.

Run from the repo root:
    python scripts/check_entry_schema_test.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_entry_schema import problems


def complete(**over):
    """A minimal entry that passes every check, so each test varies one thing."""
    e = {
        'id': 'a.b', 'kind': 'gpk', 'name': 'B', 'author': 'a', 'category': 'Costumes',
        'version': '1.0.0', 'short_description': 'x', 'replaces': 'y', 'credits': 'z',
        'source_url': 'https://example.invalid/post',
        'download_url': 'https://example.invalid/b.gpk', 'sha256': 'ff', 'size_bytes': 1,
        'gpk_files': ['b.gpk'], 'deploy_strategy': 'tmm',
    }
    e.update(over)
    return e


def check(name, mods, expect_key, expect_absent=False):
    found = problems(mods)
    hit = expect_key in found
    ok = (not hit) if expect_absent else hit
    print(f"{'PASS' if ok else 'FAIL'}  {name}")
    if not ok:
        print(f"        keys: {sorted(found)}")
    return ok


def main():
    results = [
        check('a complete entry passes', [complete()], 'no deploy_strategy', expect_absent=True),

        # The bug this guard exists for: 37 entries shipped with no strategy and
        # silently fell through to the default composite path.
        check('missing deploy_strategy is caught',
              [complete(deploy_strategy=None)], 'no deploy_strategy'),

        # Seventeen loose_replace entries had nothing to replace.
        check('loose_replace without target_loose_path is caught',
              [complete(deploy_strategy='loose_replace')],
              'loose_replace missing target_loose_path'),

        check('composite_redirect without target_object_path is caught',
              [complete(deploy_strategy='composite_redirect')],
              'composite_redirect missing target_object_path'),

        check('a strategy carried only by a part still counts',
              [complete(deploy_strategy=None,
                        parts=[{'deploy_strategy': 'tmm'}])],
              'no deploy_strategy', expect_absent=True),

        # One version grammar. Zero-padding was mechanical and is done; the
        # dated build strings are an open question, so they are reported
        # separately and must never fail the build.
        check('a bare two-part version is caught',
              [complete(version='1.7')], 'version is not MAJOR.MINOR.PATCH'),
        check('semver with a tag passes',
              [complete(version='3.0.16-classicplus')],
              'version is not MAJOR.MINOR.PATCH', expect_absent=True),
        check('a dated version is a pending decision, not a defect',
              [complete(version='2026-r2')], 'dated version, pending a scheme'),
        check('a dated version is not reported as a grammar failure',
              [complete(version='2026-r2')],
              'version is not MAJOR.MINOR.PATCH', expect_absent=True),

        # `replaces` must match the shape its category implies. One grammar
        # cannot fit all three: a costume owes ids you can paste into
        # inventory search, a face decal has no item and owes its
        # character-creation slot, a window restyle owes neither.
        check('a costume with no item id is caught',
              [complete(category='Costumes', replaces='Turns the togs pink.')],
              'wearable replaces carries no #item id'),
        check('a costume with item ids passes',
              [complete(category='Costumes', replaces='Replaces Sheriff Uniform. Elin #252264-#252287.')],
              'wearable replaces carries no #item id', expect_absent=True),
        check('a face decal naming its slot and race passes',
              [complete(category='Eyes & Face',
                        replaces='Replaces the Elin face decal at Face 11, Adornment 3.')],
              'customization replaces names no slot (face/adornment/preset number)',
              expect_absent=True),
        check('a face decal with no slot is caught',
              [complete(category='Eyes & Face', replaces='Recolours the Elin eyes.')],
              'customization replaces names no slot (face/adornment/preset number)'),
        check('a face decal with a slot but no race is caught',
              [complete(category='Eyes & Face', replaces='Replaces the decal at Face 11, Adornment 3.')],
              'customization replaces names no race'),
        check('a hair ACCESSORY may answer with item ids instead of a slot',
              [complete(category='Hair', replaces='Replaces Black Bow (#182134).')],
              'customization replaces names no slot (face/adornment/preset number)',
              expect_absent=True),
        check('a UI mod owes neither ids nor a slot',
              [complete(category='Windows & Menus', replaces='Restyles the inventory window.')],
              'wearable replaces carries no #item id', expect_absent=True),

        check('an unknown strategy is caught',
              [complete(deploy_strategy='teleportation')], 'unknown deploy_strategy'),

        # last_verified is deliberately not required: blank is the honest value
        # for a mod nobody has confirmed in game.
        check('a mod with no last_verified still passes',
              [complete()], 'missing last_verified', expect_absent=True),

        check('external tools need no deploy_strategy',
              [complete(kind='external', deploy_strategy=None)],
              'no deploy_strategy', expect_absent=True),

        check('external tools need no payload fields',
              [complete(kind='external', deploy_strategy=None, download_url=None,
                        sha256=None, size_bytes=None, gpk_files=None)],
              'missing sha256', expect_absent=True),

        check('an overlay tool needs no replaces — it swaps nothing',
              [complete(kind='external', replaces=None)], 'missing replaces', expect_absent=True),

        check('a placeholder download_url is caught',
              [complete(download_url='TODO://x.gpk')], 'placeholder download_url'),

        check('missing credits is caught', [complete(credits=None)], 'missing credits'),
        check('a dead-forum entry with no source_url still passes',
              [complete(source_url=None)], 'missing source_url', expect_absent=True),

    ]
    failed = results.count(False)
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
