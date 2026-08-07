"""Bake GitHub release-asset download counts into catalog.json.

Every mod payload is a GitHub release asset, and the GitHub API reports a
lifetime download_count per asset. This script sweeps the releases of every
repo referenced by a download_url, maps assets back to catalog entries, and
writes each entry's download_count (the max across its assets — installs pull
every part, so summing parts would double-count one install).

Runs locally (token from GH_TOKEN / GITHUB_TOKEN env, or `gh auth token`) and
in CI (see .github/workflows/update-download-counts.yml). Only rewrites
catalog.json when at least one count changed.
"""
import json
import os
import re
import subprocess
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(__file__))
from catalog_io import load, save

API = "https://api.github.com"
RELEASE_URL = re.compile(
    r"https://github\.com/([^/]+)/([^/]+)/releases/download/([^/]+)/([^/?#]+)"
)


def token():
    for k in ("GH_TOKEN", "GITHUB_TOKEN"):
        if os.environ.get(k):
            return os.environ[k]
    try:
        return subprocess.run(
            ["gh", "auth", "token"], capture_output=True, text=True, check=True
        ).stdout.strip()
    except Exception:
        return None


def get_json(url, tok):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "external-mod-catalog-count-sweep",
        **({"Authorization": f"Bearer {tok}"} if tok else {}),
    })
    with urllib.request.urlopen(req) as r:
        return json.load(r), r.headers.get("Link", "")


def asset_counts(owner, repo, tok):
    """browser_download_url -> download_count for every asset in every release."""
    counts = {}
    url = f"{API}/repos/{owner}/{repo}/releases?per_page=100"
    while url:
        page, link = get_json(url, tok)
        for rel in page:
            for a in rel.get("assets", []):
                counts[a["browser_download_url"]] = a.get("download_count", 0)
        m = re.search(r'<([^>]+)>;\s*rel="next"', link)
        url = m.group(1) if m else None
    return counts


def entry_urls(m):
    urls = [m.get("download_url") or ""]
    urls += [p.get("download_url") or "" for p in (m.get("parts") or [])]
    return [u for u in urls if u]


def main():
    tok = token()
    if not tok:
        print("WARNING: no GitHub token; unauthenticated rate limit is 60/h", file=sys.stderr)
    cat = load()

    repos = set()
    for m in cat["mods"]:
        for u in entry_urls(m):
            mt = RELEASE_URL.match(u)
            if mt:
                repos.add((mt.group(1), mt.group(2)))

    counts = {}
    for owner, repo in sorted(repos):
        got = asset_counts(owner, repo, tok)
        counts.update(got)
        print(f"{owner}/{repo}: {len(got)} assets")

    changed = 0
    matched = 0
    for m in cat["mods"]:
        vals = [counts[u] for u in entry_urls(m) if u in counts]
        if not vals:
            continue
        matched += 1
        new = max(vals)
        if m.get("download_count") != new:
            m["download_count"] = new
            changed += 1

    print(f"mods matched to assets: {matched}/{len(cat['mods'])}, counts changed: {changed}")
    if changed:
        cat["version"] += 1
        save(cat)
        print(f"catalog version -> {cat['version']}")
    else:
        print("no changes; catalog untouched")


if __name__ == "__main__":
    main()
