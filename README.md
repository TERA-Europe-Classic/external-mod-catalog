# external-mod-catalog

Static JSON catalog consumed by the
[TERA Europe Classic+ Launcher](https://github.com/TERA-Europe-Classic/TERA-Europe-ClassicPlus-Launcher)
mod manager.

## Format

`catalog.json` is a single file the launcher fetches, caches for 1 h,
and renders in the Browse tab.

## Schema

Top level: `{ "version": number, "updated_at": "ISO-8601", "mods": [ ... ] }`.

Each `mods[]` entry has the fields below. The CI gate at
`scripts/check-readme-schema.mjs` fails any PR where this table
diverges from the actual set of keys used across every entry in
`catalog.json` — so this table is the authoritative schema, and
`catalog.json` is the authoritative truth about what we've shipped.

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
| `download_count` | integer | optional | both | Stub for future telemetry; the launcher does NOT render this yet. |
| `icon_url` | string (HTTPS URL) | optional | both | Small square icon for the row/list. Falls back to `featured_image` when missing. |
| `tags` | string[] | optional | both | Searchable badges, e.g. `["ui","foglio"]`. Distinct from `category`. Default `[]`. |
| `compatibility_notes` | string | optional | both | Markdown callout ("Conflicts with X", "Broken on patch Y"). |
| `compatible_arch` | `"x32"` \| `"x64"` | optional | gpk-only | Binary arch of the GPK. Surfaces an "incompatible" badge when it disagrees with the client. |
| `composite_flag` | boolean | optional | gpk-only | True when the mod targets composite-packaged resources. |
| `gpk_files` | string[] | optional | gpk-only | Files this mod deploys, e.g. `["RestylePaperdoll.gpk"]`. For `tfc_patch`, the single span-payload filename. |
| `deploy_strategy` | `"composite_patch"` \| `"dropin"` \| `"composite_redirect"` \| `"tmm"` \| `"tfc_patch"` | optional | gpk-only | How the launcher deploys the GPK. `None` = `composite_patch`. |
| `target_object_path` | string | optional | gpk-only | Composite object path a `composite_redirect` mod targets (`Package.Object`). |
| `target_dropin_filename` | string | optional | gpk-only | `dropin`: filename written to `CookedPC/<name>` (engine loads root files as overrides). Uninstall removes the file — it never existed in vanilla. |
| `tfc_file` | string | optional | gpk-only | Vanilla texture cache a `tfc_patch` mod patches, e.g. `WorldTextures038.tfc`. |
| `tfc_spans` | object[] | optional | gpk-only | `tfc_patch` regions: `{ tfc_offset, size, payload_offset, vanilla_sha256 }`. Install verifies the vanilla hash, backs up, then writes; uninstall restores byte-perfect. |
| `parts` | object[] | optional | gpk-only | Multi-part mod: each part is `{ name, deploy_strategy, download_url, sha256, size_bytes, ... }` plus its strategy's own fields — `tfc_file`+`tfc_spans` (tfc_patch), `target_object_path` (composite_redirect), `target_dropin_filename` (dropin), or `target_loose_path`+`loose_vanilla_sha256` (loose_replace: replaces the vanilla loose file at the CookedPC-relative path after verifying its sha256; install backs it up, uninstall restores byte-perfect, and a hash mismatch means another mod owns the file → refused as a conflict). When present, `parts` is authoritative; the entry-level deploy fields remain as a fallback for launchers without multi-part support. |
<!-- schema-table-end -->

### Legacy pointer

Earlier docs pointed here for the schema definition: `docs/mod-manager/DESIGN.md` in the launcher repo. That file has not shipped; the table above replaces it.

## Contributor rules

Every entry MUST populate:
- `author`
- `source_url`
- `license` (use `"Unknown"` if the license truly is unknown; never
  omit)
- `credits` (include the original author, packer tooling credits, art
  credits where applicable)

Submissions without those four fields are closed unmerged.

## Current entries

### External apps

| id | name | source |
|----|------|--------|
| `classicplus.shinra` | Shinra Meter (Classic+) | [ShinraMeter](https://github.com/TERA-Europe-Classic/ShinraMeter) |
| `classicplus.tcc` | TCC (Classic+) | [TCC](https://github.com/TERA-Europe-Classic/TCC) |

### GPK mods — research pool (not yet shipped)

The following community GPK mods have been catalogued but are **not**
in the distributable catalog pending redistribution permission from
the original uploaders. They were shared on the TERA Europe Classic
Discord "Community UI mods :3" channel; authorship is per the
attachment uploader.

Uploader: **Псина** (Discord handle — Russian for "dog")
- `S1UI_GageMonsterHp.gpk` — monster HP gauge restyled as party HP bar
  (original Tumblr reference: miyo-ni/rainbow-hp-bar-group)
- `FX_Awaken_Engineer.gpk`, `FX_E_HotFix_140925.gpk`, `PostProcess.gpk`
  — "removing gunner from the game" effect pack
- `NPC_DisPenser.gpk` — custom dispenser NPC model (install at
  `S1Game\CookedPC\Art_Data\Packages\CH\NPC\NPC_Objects` read-only)
- `Icon_Skills.gpk` — reworked skill icons for Slayer and Lancer
- `S1UI_ExtShortCut.gpk`, `S1UI_ShortCut.gpk` — frameless shortcut bar
  with corrected ESC behaviour and cooldown animation fixes
- `S1UI_PaperDoll.gpk` — equipment/paperdoll window variant
- `S1UI_PartyWindow_1.gpk` — party window with the player number
  removed
- `S1UI_PartyWindow_2.gpk` — party window with debuffs only (no
  buffs)

Uploader: **Vaise**
- `S1UI_PartyWindow.gpk` — custom party window layout
- `TexturedFonts.gpk` — themed font packs (New Year, Santa/Bow, blue
  bow, hearts/knives) with styled healing numbers

Before adding any of these to `catalog.json`, obtain explicit
redistribution permission from the uploader and record the permission
(with date) in the entry's `credits` field. The launcher's mod
detail panel renders `credits` verbatim, so the acknowledgment is
visible to every end user.

### GPK tooling credit

Applies to every GPK entry once shipped:
- [lunchduck/GPK_RePack](https://github.com/lunchduck/GPK_RePack) —
  GPK unpack/repack tool the community uses to build redistributable
  mods.
- [vezel-dev/novadrop](https://github.com/vezel-dev/novadrop) —
  UPK/GPK parser used by modern tooling.

## Licensing

Catalog contents (this repo) are MIT. Individual mods carry their own
licenses, listed per-entry.
