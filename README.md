# external-mod-catalog

Static JSON catalog consumed by the
[TERA Europe Classic+ Launcher](https://github.com/TERA-Europe-Classic/TERA-Europe-ClassicPlus-Launcher)
mod manager.

## Format

`catalog.json` is a single file the launcher fetches, caches for 1 h,
and renders in the Browse tab. Schema and field definitions are
documented in the launcher repo under `docs/mod-manager/DESIGN.md`
(§ "Catalog entry schema" and § "Credit / attribution requirements").

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
