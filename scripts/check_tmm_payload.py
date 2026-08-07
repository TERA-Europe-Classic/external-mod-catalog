"""Validate a TMM payload before it ships.

PantyponCastanicSleepyRunningTogs.gpk went out with 49 inner packages where
48 were correct and one carried the mod's own name instead of a composite uid
— and was 17.4 MB against neighbours of 4 KB to 430 KB, because the build had
appended the entire converted source package as an extra entry. The installer
aborts when any single object fails to resolve, correctly, so the whole mod
was uninstallable. A tester found it, not us.

Every one of these checks would have caught it in under a second:

  paths     every inner package must be MOD:<uid>.<Class>.<Object>_dup.
            A path containing "modres", or any package name that is not a
            composite uid, cannot resolve in the mapper.
  sizes     no inner package wildly out of band. A whole source package
            smuggled in among per-object packages stands out by 40x.
  footer    strings read back intact, offsets sorted, count matches.

    python scripts/check_tmm_payload.py <file.gpk> [more.gpk ...]
    python scripts/check_tmm_payload.py --release pantypon-costumes-v1

Exits non-zero if any payload fails.
"""
import argparse
import io
import json
import os
import re
import struct
import subprocess
import sys
import tempfile
import urllib.request

MAGIC = 0x9E2A83C1
MOD_PREFIX = 'MOD:'
# <8 hex>_<hex>_<hex>.Skel|Tex.<object>_dup — the shape every resolvable
# composite path takes.
PATH_RE = re.compile(r'^[0-9a-f]{8}_[0-9a-f]+_[0-9a-f]+\.[A-Za-z0-9]+\.\S+_dup$')
# A package more than this many times the median is not a sibling of the
# others. The real case was 40x; 8x is comfortably clear of legitimate
# variation between a Skel and a small mask texture.
SIZE_OUTLIER_FACTOR = 8


def read_str(b, off):
    """TMM length-prefixed string. The length is the EXACT byte count —
    it does not exclude a trailing null. Subtracting one yields 'pantypo'
    and a writer built on that ships a corrupt container name."""
    n = struct.unpack_from('<i', b, off)[0]
    if n == 0:
        return ''
    if n > 0:
        return b[off + 4:off + 4 + n].decode('utf-8', 'replace')
    return b[off + 4:off + 4 - 2 * n].decode('utf-16-le', 'replace')


def check(path):
    b = io.open(path, 'rb').read()
    name = os.path.basename(path)
    problems = []
    if len(b) < 40 or struct.unpack_from('<I', b, len(b) - 4)[0] != MAGIC:
        return [f'{name}: not a TMM payload (no footer magic)']

    pos = len(b) - 4

    def back():
        nonlocal pos
        pos -= 4
        return struct.unpack_from('<i', b, pos)[0]

    meta_size = back(); count = back(); offs_off = back()
    cont_off = back(); name_off = back(); auth_off = back()
    back()  # region_lock
    back()  # version

    if count <= 0 or offs_off <= 0 or offs_off + count * 4 > len(b):
        return [f'{name}: footer offsets table is out of range']
    for label, off in (('author', auth_off), ('name', name_off), ('container', cont_off)):
        if not read_str(b, off).strip():
            problems.append(f'{name}: footer {label} string is empty')

    offs = [struct.unpack_from('<i', b, offs_off + i * 4)[0] for i in range(count)]
    if offs != sorted(offs):
        problems.append(f'{name}: inner package offsets are not ascending')

    meta_start = len(b) - meta_size
    sizes = [(offs[i + 1] - offs[i]) if i + 1 < count else meta_start - offs[i]
             for i in range(count)]

    paths = []
    for o in offs:
        folder = read_str(b, o + 12).rstrip('\x00')
        paths.append(folder[len(MOD_PREFIX):] if folder.startswith(MOD_PREFIX) else folder)

    for i, p in enumerate(paths):
        if 'modres' in p:
            problems.append(f'{name}: object {i} carries a build-local name, not a composite uid: {p[:70]}')
        elif not PATH_RE.match(p):
            problems.append(f'{name}: object {i} is not <uid>.<Class>.<Object>_dup: {p[:70]}')

    # Compare sizes WITHIN a class, never across. A SkeletalMesh is
    # legitimately several MB while a mask texture is a few KB, so a payload
    # holding 15 Skels among 84 textures has a texture-dominated median and
    # every Skel reads as an outlier — Black Business Suit tripped exactly
    # that. The real defect was a .Tex object 60x its texture siblings.
    by_class = {}
    for i, p in enumerate(paths):
        parts = p.split('.')
        by_class.setdefault(parts[1] if len(parts) > 2 else '?', []).append(i)
    for cls, idxs in by_class.items():
        if len(idxs) < 4:
            continue
        peer = sorted(sizes[i] for i in idxs)[len(idxs) // 2]
        if not peer:
            continue
        for i in idxs:
            if sizes[i] > peer * SIZE_OUTLIER_FACTOR:
                problems.append(
                    f'{name}: object {i} ({cls}) is {sizes[i]} bytes against a '
                    f'{cls} median of {peer} ({sizes[i] // peer}x) — a whole '
                    f'source package may have been appended')
    return problems


def release_payloads(tag):
    out = subprocess.run(['gh', 'release', 'view', tag, '--json', 'assets'],
                         capture_output=True, text=True)
    assets = json.loads(out.stdout)['assets']
    return [(a['name'], a['url']) for a in assets if a['name'].lower().endswith('.gpk')]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('files', nargs='*')
    ap.add_argument('--release', help='check every .gpk asset on a GitHub release')
    args = ap.parse_args()

    targets = list(args.files)
    tmp = None
    if args.release:
        tmp = tempfile.mkdtemp()
        for n, url in release_payloads(args.release):
            dest = os.path.join(tmp, n)
            print(f'  fetching {n}...', flush=True)
            subprocess.run(['gh', 'release', 'download', args.release,
                            '--pattern', n, '--dir', tmp, '--clobber'],
                           capture_output=True)
            if os.path.exists(dest):
                targets.append(dest)

    failed = 0
    for t in targets:
        problems = check(t)
        if problems:
            failed += 1
            for p in problems:
                print(f'FAIL  {p}')
        else:
            print(f'ok    {os.path.basename(t)}')
    print(f'\n{len(targets) - failed}/{len(targets)} payloads pass')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
