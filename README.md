# external-mod-catalog

Mod catalog for the
[TERA Europe Classic+ Launcher](https://github.com/TERA-Europe-Classic/TERA-Europe-ClassicPlus-Launcher).
The launcher reads `catalog.json` from this repo and shows everything in its
Browse tab. The mod files themselves live in this repo's
[Releases](https://github.com/TERA-Europe-Classic/external-mod-catalog/releases).

## How to install mods

Use the launcher. Browse tab, pick a mod, hit install. It handles the
download, deploys the files into the client, keeps them updated, and can
cleanly uninstall.

You can also grab files straight from
[Releases](https://github.com/TERA-Europe-Classic/external-mod-catalog/releases)
if you'd rather do things yourself. One release per mod, tagged
`mod-<name>-v<version>`, and the matching `catalog.json` entry has the
download link plus a SHA-256 for every file. Fair warning: GPK mods are not
drag and drop. Each entry describes how the file has to be deployed into the
client, and without the launcher you're doing that part by hand.

## What's in here

494 mods from 107 creators, as of catalog version 358. All but two are GPK
mods:

| Category | Count | | Category | Count |
|---|--:|---|---|--:|
| Costumes | 203 | | Removers | 12 |
| Accessories | 72 | | Chat & Alerts | 9 |
| HUD & Combat | 65 | | Sounds & Voice | 3 |
| Windows & Menus | 54 | | Tools | 2 |
| Mounts & Pets | 31 | | | |
| Performance & FX | 25 | | | |
| Weapon Skins | 18 | | | |

The catalog no longer carries character customization mods: faces, eye
decals, adornments and hairstyles.

The two that aren't GPKs:
[Shinra Meter (Classic+)](https://github.com/TERA-Europe-Classic/ShinraMeter)
is a damage meter and
[TCC (Classic+)](https://github.com/TERA-Europe-Classic/TCC) is a HUD
replacement. Both are external apps the launcher can install and start
alongside the game.

## Where the mods come from

Most of these were rescued from the community before they could disappear:
the mods-of-tera Tumblr and the "Community UI mods" channels on the TERA
Europe Classic Discord. The original creator is credited in every entry's
`credits` field. The old 32-bit packs were converted to work on the v100
(x64) client.

Made one of these and want it credited differently, or taken down? Open an
issue.

Two of the early seed uploaders deserve a mention here: Псина, whose
monster-HP gauge shipped as `psina.gage-monster-hp` along with party and
shortcut window variants, and Vaise, who shared a party window and themed
font packs.

## Contributing

Everything the launcher shows comes out of `catalog.json`. One file, fetched
once and cached for an hour. Top level:
`{ "version": number, "updated_at": "ISO-8601", "mods": [ ... ] }`.

Four fields are non-negotiable in every entry: `author`, `source_url`,
`license` (put `"Unknown"` if you really can't find one), and `credits`
(original author, packer tooling, art credits where they apply). PRs missing
any of them get closed.

### Schema

CI checks this table against `catalog.json` on every PR
(`scripts/check-readme-schema.mjs`). If a key exists in the catalog but not
here, or the other way around, the build fails. So the table can't go stale.

<!-- schema-table-begin -->
| Field | Type | Required | Scope | Notes |
|---|---|---|---|---|
| `id` | string | required | both | Stable catalog id, e.g. `classicplus.shinra`. |
| `kind` | `"external"` \| `"gpk"` | required | both | External app or GPK patch. |
| `name` | string | required | both | Display name shown in the launcher row. |
| `author` | string | required | both | Mod author. Never omit. |
| `short_description` | string | required | both | One-line description for the row. |
| `long_description` | string | optional | both | Full README-style body for the detail panel. Default `""`. |
| `category` | string | optional | both | Category chip grouping (UI, gameplay, etc.). Default `""`. |
| `license` | string | required | both | SPDX identifier or freeform. Use `"Unknown"` if truly unknown — never omit. |
| `credits` | string | required | both | Freeform attribution rendered verbatim in the detail panel. |
| `version` | string | required | both | Semver or publisher version string. Drives update detection. |
| `download_url` | string (HTTPS URL) | required | both | Direct download for the binary. HTTPS only; no embedded credentials. |
| `sha256` | string (64-char hex) | required | both | Lowercase hex SHA-256 of the downloaded bytes. |
| `size_bytes` | integer (positive) | optional | both | Expected byte size. Default `0`. |
| `source_url` | string | optional | both | Source-of-truth URL (GitHub, Tumblr, etc.) shown as "View source" in the detail panel. |
| `executable_relpath` | string | required for external | external-only | Relative path to the executable inside the extracted zip. |
| `auto_launch_default` | boolean | optional | external-only | Fresh install defaults to auto-launching with the game. Default `false`. |
| `settings_folder` | string | optional | external-only | OS-specific settings dir template, e.g. `%APPDATA%\\ShinraMeter`. Used by the uninstall flow. |
| `updated_at` | string (ISO-8601) | optional | both | Last publisher update. Default `""`. |
| `tagline` | string | optional | both | One-line punchy hook (≤90 chars). Row cards display this; falls back to `short_description` when missing. |
| `featured_image` | string (HTTPS URL) | optional | both | Hero image at the top of the detail panel. 16:9 preferred, ≥1200w. For restyles, the "after" shot. |
| `last_verified_patch` | string | optional | both | Last patch the mod was confirmed working on, e.g. `"patch 113"`. |
| `download_count` | integer | optional | both | Lifetime downloads, swept daily from GitHub release-asset stats by `scripts/update_download_counts.py` (max across a mod's assets, so multi-part installs count once). The launcher renders and sorts by it. |
| `icon_url` | string (HTTPS URL) | optional | both | Small square icon for the row/list. Falls back to `featured_image` when missing. |
| `tags` | string[] | optional | both | Searchable badges, e.g. `["ui","foglio"]`. Distinct from `category`. Default `[]`. |
| `compatibility_notes` | string | optional | both | Markdown callout ("Conflicts with X", "Broken on patch Y"). |
| `compatible_arch` | `"x32"` \| `"x64"` | optional | gpk-only | Binary arch of the GPK. Surfaces an "incompatible" badge when it disagrees with the client. |
| `composite_flag` | boolean | optional | gpk-only | True when the mod targets composite-packaged resources. |
| `gpk_files` | string[] | optional | gpk-only | Files this mod deploys, e.g. `["RestylePaperdoll.gpk"]`. For `tfc_patch`, the single span-payload filename. |
| `deploy_strategy` | `"composite_patch"` \| `"dropin"` \| `"composite_redirect"` \| `"tmm"` \| `"tfc_patch"` \| `"loose_replace"` \| `"loose_add"` \| `"decal_patch"` | optional | gpk-only | How the launcher deploys the GPK. Omitted = `composite_patch`. `loose_replace` swaps a whole vanilla loose file; `loose_add` writes a new one; `decal_patch` overwrites one decal's byte range inside the shared decal atlas so several designs coexist. |
| `target_object_path` | string | optional | gpk-only | Composite object path a `composite_redirect` mod targets (`Package.Object`). |
| `tmm_object_paths` | string[] | optional | gpk-only | Every object path a `tmm` payload's footer declares. Recorded so alternatives and conflicts derive from what the mod actually writes; regenerate with the footer recorder when the payload changes. |
| `target_dropin_filename` | string | optional | gpk-only | `dropin`: filename written to `CookedPC/<name>` (engine loads root files as overrides). Uninstall removes the file — it never existed in vanilla. |
| `screenshots` | string[] | optional | both | Additional gallery images shown in the detail panel; `featured_image` is the cover (first). |
| `blur_data` | string | optional | both | Tiny (~12px) inline WebP data-URI of the cover — painted instantly under the thumb/hero while the real image loads (blurhash-equivalent placeholder, no JS deps). |
| `target_patch` | string | optional | gpk-only | Game patch the payload was built against (informational), e.g. `v100.02`. |
| `replaces` | string | optional | gpk-only | What the mod overrides in game, in player-facing prose: costume/item names with their numeric item id (`#81159`), the UI window, mount, or face-decal slot, ending with a natural "To confirm it applied, …" hint. Numeric item ids are kept for testing; raw engine identifiers (package names, object paths) are not shown — the `gpk_files` row carries those. IDs are cross-checked against the elinu datacenter. |
| `replaces_data` | object | required | gpk-only | The machine-readable form of `replaces`, validated in CI against [`schema/replaces.schema.json`](schema/replaces.schema.json). `summary` is prose; then at least one of `targets` (items the game sells, by numeric id, per race/gender), `slots` (a character-creator or decal slot the game has no item for), `loose` (a file the mod replaces wholesale), or `objects` (engine objects read back out of the mod's OWN payload — CI re-opens the payload at the shipped sha256 and asserts each one is still exported). An entry that can declare none of these has to say why in `broken`. |
| `objects` | string[] | optional | gpk-only | Composite objects a `tmm` payload claims, harvested from its footer — full mapper uids (`<container>.<Sub>.<Object>_dup`). Two tmm costumes on the same package share no other key, so without this the launcher showed no conflict badge and the second one enabled silently won every object. Distinct from `replaces_data.objects`, which names payload exports rather than mapper rows. |
| `tfc_file` | string | optional | gpk-only | Vanilla texture cache a `tfc_patch` mod patches, e.g. `WorldTextures038.tfc`. |
| `tfc_spans` | object[] | optional | gpk-only | `tfc_patch` regions: `{ tfc_offset, size, payload_offset, vanilla_sha256 }`. Install verifies the vanilla hash, backs up, then writes; uninstall restores byte-perfect. |
| `parts` | object[] | optional | gpk-only | Multi-part mod: each part is `{ name, deploy_strategy, download_url, sha256, size_bytes, ... }` plus its strategy's own fields — `tfc_file`+`tfc_spans` (tfc_patch), `target_object_path` (composite_redirect), `target_dropin_filename` (dropin), or `target_loose_path`+`loose_vanilla_sha256` (loose_replace: replaces the vanilla loose file at the CookedPC-relative path after verifying its sha256; install backs it up, uninstall restores byte-perfect, and a hash mismatch means another mod owns the file → refused as a conflict), or `target_loose_path`+`loose_vanilla_sha256`+`decal_offset`+`decal_len` (decal_patch: overwrites that one byte range in the loose file after verifying the range's sha256, so parts on different ranges coexist). When present, `parts` is authoritative; the entry-level deploy fields remain as a fallback for launchers without multi-part support. |
| `last_verified` | object | optional | both | A known-good snapshot for regression bisecting: `{ date, launcher_version, mod_version, client, parts: {name: asset-path}, by, note }`. Stamped when the mod is confirmed working in-game, so a later break has an exact point to snap back to. The launcher renders it as a "Verified" badge. |
| `broken` | string | optional | both | Set when the mod is confirmed NOT working in-game; the text says what fails and what the fix plan is. The launcher renders a "Broken" badge and filter. Mods with neither `last_verified` nor `broken` count as "Untested". |
| `verification_status` | `"untested"` | optional | both | Marks an entry whose payload changed and has not been confirmed in-game since. `"untested"` is the only value the catalog uses. Related to `last_verified` / `broken` but separate: those record a test that already happened, this one flags a test still owed. |
| `target_loose_path` | string | optional | gpk-only | `loose_replace` / `loose_add` / `decal_patch`: the CookedPC-relative file the part writes, e.g. `Art_Data/Packages/CH/PC/Popori_F_Head.gpk`. Present on the part, not the entry. |
| `loose_vanilla_sha256` | string (64-char hex) | optional | gpk-only | Expected sha256 of the vanilla file at `target_loose_path`. Install verifies it, backs the file up, then writes; a mismatch means another mod owns the file and the install is refused as a conflict. |
| `review_required` | string | optional | both | Internal note that a converted payload needs a second look before it can be trusted (e.g. a source texture that has no v100 counterpart). The launcher does not render it. |
| `conflicts_with` | string[] | optional | both | Ids of mods that replace the same thing — colour variants of one costume, rival restyles of one window. Only one of a set can be active; the launcher lists them as links in the detail panel so the user can compare, and uses them for its conflict badges. Derived from shared deploy targets, not hand-authored. |
| `collection` | string | optional | both | Free-form key linking variants that coexist (one eye pack's designs). The launcher lists members as chips in the detail panel; unlike `conflicts_with`, collection members can be enabled together. |
<!-- schema-table-end -->

### Scripts

Tooling for catalog edits lives in `scripts/`. All of it writes
`catalog.json` back in its exact on-disk format (1-space indent, UTF-8,
CRLF), so diffs stay small.

| Script | Purpose |
|---|---|
| `check-readme-schema.mjs` | The CI gate described above. |
| `catalog_io.py` | Load/save helper with byte-identical round-trip. Import it (`load`, `save`, `by_id`) for any scripted edit. |
| `make_media.py` | Turn a source image into `media/<id>/cover.webp` + `thumb.webp` and print a `blur_data` URI. |
| `clean_copy.py` | Copy cleanup pass: de-dupes the Replaces block out of `long_description`, drops boilerplate, rephrases terse "Check:" hints. |
| `strip_identifiers.py` | Removes raw engine identifiers from visible copy (keeps numeric item ids). |

Images under `media/` are served through jsDelivr
(`cdn.jsdelivr.net/gh/TERA-Europe-Classic/external-mod-catalog@main/media/…`),
so pushing to main is the whole deploy.

### GPK tooling credit

- [lunchduck/GPK_RePack](https://github.com/lunchduck/GPK_RePack) is the
  unpack/repack tool the community uses to build redistributable mods.
- [vezel-dev/novadrop](https://github.com/vezel-dev/novadrop) is the UPK/GPK
  parser used by modern tooling.

## Licensing

This repo is MIT. The mods themselves carry their own licenses, listed per
entry.
