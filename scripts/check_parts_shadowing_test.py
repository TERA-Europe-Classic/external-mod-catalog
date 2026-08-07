"""Self-test for the parts-shadowing detector.

A guard that silently stops detecting is worse than no guard, and this one
protects against a failure that is invisible from the outside: the entry
installs cleanly, reports success and renders vanilla. So prove the detector
still catches a shadowed entry and still passes the shapes that are fine.

    python scripts/check_parts_shadowing_test.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_parts_shadowing import offenders  # noqa: E402

failures = 0


def check(ok, what):
    global failures
    if ok:
        print("  ok   " + what)
        return
    failures += 1
    print("  FAIL " + what)


def entry(**kw):
    base = {'id': 'x.y', 'sha256': 'aaa', 'target_object_path': 'Pkg.Obj_dup'}
    base.update(kw)
    return base


# The real bug: top level rebuilt, parts left behind pointing at the old file.
check(len(offenders([entry(parts=[{'sha256': 'bbb', 'deploy_strategy': 'loose_replace'}])])) == 1,
      "catches a part whose payload is not the top-level one")

# Parts carrying the same payload are the normal multi-target shape.
check(offenders([entry(parts=[{'sha256': 'aaa', 'deploy_strategy': 'composite_redirect'},
                              {'sha256': 'ccc', 'deploy_strategy': 'composite_redirect'}])]) == [],
      "passes when the top-level payload is among the parts")

# A parts-only entry declares no top-level redirect, so nothing is shadowed.
check(offenders([{'id': 'x.y', 'parts': [{'sha256': 'bbb'}]}]) == [],
      "passes a parts-only entry with no top-level redirect")

# No parts at all: the top-level redirect is what installs.
check(offenders([entry()]) == [], "passes an entry with no parts")

# A top-level payload with no target cannot be a composite redirect.
check(offenders([{'id': 'x.y', 'sha256': 'aaa',
                  'parts': [{'sha256': 'bbb'}]}]) == [],
      "passes when there is no target_object_path to shadow")

# Parts without shas must not be read as a match.
check(len(offenders([entry(parts=[{'deploy_strategy': 'loose_replace'}])])) == 1,
      "a part with no sha does not count as carrying the top-level payload")

# The exact pair that shipped: two entries, same stale part sha.
both = [entry(id='catannadev.pink-loading-progress',
              sha256='331f0f71', parts=[{'sha256': '40fced85'}]),
        entry(id='catannadev.red-loading-progress',
              sha256='75f73c1f', parts=[{'sha256': '40fced85'}])]
check(len(offenders(both)) == 2, "catches both loading-progress entries as they shipped")

print("OK" if failures == 0 else f"{failures} FAILED")
sys.exit(0 if failures == 0 else 1)
