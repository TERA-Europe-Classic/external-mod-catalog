"""Load/save catalog.json preserving its exact on-disk format
(1-space indent, ensure_ascii=False, CRLF newlines, no trailing newline).
Round-trip is byte-identical, so a targeted field change produces a minimal diff.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "catalog.json")

def load():
    with open(PATH, "rb") as f:
        return json.loads(f.read())

def save(data):
    text = json.dumps(data, indent=1, ensure_ascii=False).replace("\n", "\r\n")
    with open(PATH, "wb") as f:
        f.write(text.encode("utf-8"))

def by_id(data):
    return {m["id"]: m for m in data["mods"]}
