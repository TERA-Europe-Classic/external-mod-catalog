# What's blocked, and the three things that unblock it

Everything that can be settled from a terminal has been. What's left needs
someone looking at a running client — three observations, in one sitting.

Everything below assumes: **close the client first, and restart it after
toggling anything.** The mapper is read once at launch, so a mod switched on
while TERA is running shows vanilla until you relaunch. That has been mistaken
for a broken mod more than once.

After any crash or oddity, read `D:/Elinu/S1Game/Logs/Launch.log` (UTF-16) and
diff it against `tera-mod-archive/vanilla-launch-baseline.log`. Only new lines
matter, and `Can't find file for package '<uid>'` names the exact missing mapper
row or container.

---

## 1. Two or three mods from the Route-A batch — unblocks the conversion recipe

**Equip any two or three, look, say which look right.**

Route-A rebuilds a whole 32-bit package into a 64-bit container. That is *not*
the recipe Hello Kitty confirmed — that one imports art into packages v100
already has. Nobody has seen a Route-A output render, and building a queue on an
unconfirmed recipe is this campaign's documented failure mode: White Castanica
Demon took four rounds that way, Castanic Sleepy three.

Also unblocks nine costume mods whose orphaned art is routed, built and verified
at MAD 0.00 against the authors' own textures, staged in `scratch/orphanfix`.
They are partial no-ops today: some of their art reaches the game and some does
not.

---

## 2. Face 11 on an Elin — unblocks native customization

**Open character creation, Elin, Face 11, and count the adornments.**

Every offline question is answered and all of them are favourable: no server
datasheet bounds the adornment index, not one of the 82 shipped Popori_F presets
references a non-default adornment, the string table carries no ids, and the ids
are contiguous with 24 free. What is unknown is what an unpatched client does
when it meets adornment 24 — which only a client can say.

---

## 3. A round of Untested mods — stamps the verification log

**Filter the launcher's mod list by Status = Untested, install a few, look.**

The list is the deliverable; there is no staging work left. Results stamp
`last_verified`, which is what makes future regressions bisectable.

This round overlaps observation 1 — testing Route-A mods here does both.

---

## One decision, no testing — the locale DC packs

LobbyShape differs from EUR in exactly 16 rows (FRA/GER/RUS identical to each
other). Of those, 13 are `RepresentativeSkills` — character-creation skill
previews — and 3 are the port fixes (`11004 customSkinTone`,
`11011/11012 animSetShare`).

Recommendation: **copy the three.** A bulk copy pushes 13 unrelated
character-creation changes into three locales to fix a port problem, and none of
the 13 read as port-related.

(`UserShape` has zero real drift. A naive diff calls 98 of 103 rows different;
every one is float re-serialisation — `bodyFxSize '1.000000'` vs `'1'`.)

---

## Blocked with no observation available

These are properties of the format. No amount of looking at a client changes
them; they need a different technique.

**The S1UI window mods** — 3 pantypon entries, plus
`saltymonkey.message-centered`. v100 compiles each window into Flash symbols and
names the textures from the symbol table (`_temp1_`, `Component_I1C1`,
`$Party_bitmap_mp`); the 32-bit payloads named their art by hand (`bgImg0`,
`party_0_TEX`, `classIcon8`). Measured on the party window: **39 composite
objects against 114 payload objects, zero overlap.** There is no name
correspondence to find, so no lookup can port them. The route that works for
this shape is the one the block-popup family is confirmed rendering with in
game — place the art into the v100 symbol slot by appearance rather than by
name.

Worth knowing before anyone touches this family: **S1UI reuses object names
across unrelated windows.** `bgImg0` exists in `S1UI_EventSystemAlim` (262 KB),
`S1UI_EnchantPopUp` (524 KB), `S1UI_ToolTip` (32 KB) and `S1UI_WorldMap2`
(32 KB) as four different images. A bare-name lookup returns all four, and
writing to all four clobbers three windows the mod never targeted.

**The JP voice pack.** Both routes are closed:

- `composite_redirect` is a silent no-op — eleven loose PCVoice banks shadow the
  mapper, and the shadowing is object-level: the loose bank holds the very
  `SoundNodeWave` objects the mod replaces.
- `loose_replace` is fatal — the client's size check guards exactly these files,
  so any size difference kills it at launch.

That leaves size-exact `loose_replace`. A GPK RePack fix removed the bulk of the
gap: the writer had been reading compression from a global UI toggle instead of
the source package, so a vanilla bank came back **+36%** with nothing edited. It
is +14.4% now. Closing the last 250 KB means matching the original packer's exact
LZO block boundaries, or padding to the vanilla byte count if the check is
size-only rather than content-hashing. Nobody knows which, and guessing wrong
fatals the client at startup.

**10 effect mods** — particle `DistributionFloat*`, post-process, DOF/AO. No
texture route applies at all; there is nothing to redirect.

**48 entries genuinely ship vanilla art** on every texture they carry, several
compared across 78–140 textures with a resampling comparison. These are dumps,
not broken ports.

---

## One catalog entry is red on purpose

`flying.mount-mod` is described as a mount retexture. Its payload exports 14
`ProgressBar_I*` objects — loading-bar UI. Either the wrong file was attached at
intake or the description belongs to another mod. The gate refuses it, and the
evidence is recorded in its `broken` field. Inventing an identity for it from a
payload nobody can explain is not a fix; it needs whoever knows the mod.
