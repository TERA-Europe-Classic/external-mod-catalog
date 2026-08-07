# In-game verification sheet Close TERA before toggling. The client reads the mapper once at launch, so
restart after every install or enable. On any crash: stop and report;
Launch.log names the failing package. ## Test these first -- each verdict gates a class (3) | Mod | id | What to do | What it unlocks |
|---|---|---|---|
| Animation Route Canary (diagnostic) | `diagnostic.animation-canary` | FIRST, before GFTime Dance. Install, restart, and just tell me whether you reach the character screen -- do not test the dance. These 12 slices are re-serialised and redirected through the identical route with every animation byte unchanged from vanilla, so a crash means the route itself cannot carry an animation slice, and a clean boot means the earlier fatal was the x32 payload data. Uninstalling in the launcher restores everything. | every animation mod (12) -- decides whether composite_redirect can carry an animation slice at all |
| Steam Weapons | `amynet.steam-weapons` | install, restart, preview any series-05 steam event weapon -- the reskin should show on every weapon type including the rod | the importer-fix rebuild class |
| Modern UI: Guild Window | `foglio1024.modern-ui-guild-window` | SUPERVISED. Install, restart, open the guild window. This is the first movie-route mod offered -- a composite redirect of a Flash movie crashed the client once before, so if the game fails to launch, uninstall in the launcher (that restores everything) and tell me. A redesigned guild window means the whole foglio/taorelia family unlocks. | the other 17 movie-route UI mods, all built and verified against vanilla | ## Ready for verification (439) | Mod | id | What to do |
|---|---|---|
| HP/MP Center Piece Recolor | `aioshe.simple-healthmanacenter-piece-recolor` | in game, look at the HP and MP bars (and 1 more) |
| White Castanica Demon (All Races) | `aioshe.white-castanica-demons-re-color-for-all` | equip Arborean College Gear (Amani Female) #152357 (aman female) |
| Mount-Flight Walk | `alqmia.fly-walk` | in game, look at the walking animation on Elin (12 slices) |
| Air-Swim (Forward) | `alqmia.swim-forward` | in game, look at the walking animation on Elin (9 slices) |
| Air-Swim (In Place) | `alqmia.swim-idle` | in game, look at the walking animation on Elin (12 slices) |
| Blue Horn Glow | `amynet.blue-horn-glow` | equip Devil Horns #178132 (any race) |
| Clean White Police Outfit | `anastasik.white-police-clean-v2` | equip TERA Squad Leader (Elin) #150322 (elin female) |
| Pixel Moon Block | `aunu.block-moon` | in game, look at the Defense Success (block) popup |
| Blossom Hanbok Recolor I (lighter set) | `banana.event27a-recolor-a` | equip Orchid Blossom Hanbok (Elin) #150846 (elin female) |
| Blossom Hanbok Recolor II (detailed set) | `banana.event27a-recolor-b` | equip Orchid Blossom Hanbok (Elin) #150846 (elin female) |
| Cavities Elin Face 7 Adornment 2 | `cannibalism-princess.cavities` | character creator: elin any, pick face 7 |
| Glasgow Elin Face 11 Adornment 3 | `cannibalism-princess.glasgow` | character creator: elin any, pick face 11 |
| Princess Elin Face Decals | `cannibalism.princess-elin-face-decals` | character creator: elin any, pick face 7 |
| Colored HP Bar v1 | `catannadev.colored-hp-bar` | in game, look at the HP bar in the character window |
| Pink Crosshair | `catannadev.pink-crosshair` | in game, look at the aiming crosshair |
| Pink HP Bar (CharacterWindow) | `catannadev.pink-hp-bar` | in game, look at the HP bar in the character window |
| Red Crosshair | `catannadev.red-crosshair` | in game, look at the aiming crosshair |
| Red Loading Progress | `catannadev.red-loading-progress` | in game, look at the loading progress bar |
| Yellow/Orange HP Bar | `catannadev.yellow-orange-hp-bar` | in game, look at the HP bar in the character window |
| Dragon Crit Orange (0% transparency) | `cosy.dragon-crit-orange-0` | in game, look at the in-game text, which uses these fonts everywhere |
| Dragon Crit Orange (50% transparency) | `cosy.dragon-crit-orange-50` | in game, look at the in-game text, which uses these fonts everywhere |
| Dragon Crit White (50% transparency) | `cosy.dragon-crit-white-50` | in game, look at the in-game text, which uses these fonts everywhere |
| 2016 Swimsuit Recolor (Elin) | `cute.swimsuit` | equip Striped Boardshorts (Human Male) #250476 (human male) |
| Archdevan Castanic Face 1 Adornment 17 | `deathwrack.archdevan-for-fyregem-for-face` | character creator: castanic female, pick face 1 |
| Better Now Castanic Male Rapidos | `deathwrack.better-now-for-rapidos-works-on` | equip Cool Beach Boy (Human Male) #179735 (human male) |
| Dragonfruit Human Face 1 Adornment 17 | `deathwrack.dragonfruit-human-face-1-adornment` | character creator: human female, pick face 1 |
| Love Letter Castanic Face 11 Adornment 8 | `deathwrack.love-letter-for-f-11-a-8` | character creator: castanic female, pick face 11 |
| Misty Castanic Face 11 Adornment 8 | `deathwrack.mistyhi-its-been-awhile-since-i` | character creator: castanic female, pick face 11 |
| Preach Human Face 1 Adornment 17 | `deathwrack.preach-for-face-1-adornment-17-i` | character creator: human female, pick face 1 |
| Renegade Dyeable Business Suit | `deathwrack.renegade-for-dyeable` | equip [TBU] #131818 (aman female) |
| Shego Castanic Face 11 Adornment 8 | `deathwrack.shego-for-face-11-adornment-8` | character creator: castanic female, pick face 11 |
| Soft Serenade Castanic Face 11 Adornment 8 | `deathwrack.soft-serenade-for-castanic-face-11` | character creator: castanic female, pick face 11 |
| Youkai Castanic Face 11 Adornment 11 | `deathwrack.youkai-for-f-11-a-11-i-was-admiring` | character creator: castanic female, pick face 11 |
| Green Eyes Elin Face 9 Adornment 2 | `demokron.green-eyes` | character creator: elin any, pick face 9 |
| Animation Route Canary (diagnostic) | `diagnostic.animation-canary` | in game, look at 12 Elin emote animation slices, rewritten with identical content |
| Jeans & Jacket White/Black Shorts | `dyeable.jeans-and-jacket-shorts-mod` | equip Arborean College Gear (Amani Female) #152357 (aman female) and DYE it (undyed matches vanilla) |
| Plain Witchypooh | `egonurse.plain-witchypooh-mod-quick-mod-i-did` | equip [TBU] #115423 (any race) |
| Red Alice Bow | `elinsailorsuit.decided-to-upload-my-red-alice` | equip Black Hair Ribbon #116106 (any race) |
| Castanic L21 Armor Retexture | `eroaulon.got-bored-waiting-for-servers-to-come` | look at: Repaints the castanic female L21 armor body texture |
| Noble Moon Recolor | `eroaulon.recolor-of-noble-moon-down` | equip Riding Skill: Ookami #100974 (any race) |
| Academy Outfit Coral Red Recolor | `eroaulon.replaces-the-red-version` | equip Sky Blue Academy Uniform (Amani Female) #154661 (aman female) |
| Celeboom Red and White Retextures | `etsaki.celeboom-red-white-retextures-i-was` | look at: Retextures the Celeboom gun in red and white |
| Sleepy Elin Face 5 Adornment 3 | `fancy.pantsu-need-your-elin-to-look-sleep` | character creator: elin any, pick face 5 |
| Modern UI: Jewels Fix (Item Icons) | `foglio1024.modern-ui-jewels-fix-icons` | in game, look at the item icons |
| Spring Ninja Suit (Elin) | `glorbie.hi-there-sharing-the-first-mod-ive` | equip Moonlight Armor (Amani Female) #178683 (aman female) |
| Darker Rogue Gallery Armor | `gravebow.long-time-no-post-ill-be-getting` | equip Nightwalker Armor (Human Male) #151868 (human male) |
| Personalized Gym Uniform Rework | `gymuni.gymuni` | equip Imprintable Sportswear (Human Male) #251652 (human male) |
| Mint Ombre Snowy Winter Scarf | `gyunuslab.a-mod-that-gives-the-snowy-winter` | equip Snowy Winter Scarf #150713 (any race) |
| Mint Spun Sugar Wings | `gyunuslab.a-simple-mod-that-changes-the-color` | equip White Butterfly Wings #115181 (any race) |
| Cutie Bear Elin Face 1 Adornment 2 | `gyunuslab.cutie-bear-face` | character creator: elin any, pick face 1 |
| Bruiseweave-Match Ribbon Headband | `gyunuslab.good-morning-everyone-i-received-a` | equip Pink Giant Bow Headband #179619 (any race) |
| Pastel Felicity | `gyunuslab.im-sorry-about-the-shitty` | look at: Recolors the Felicity pet pastel with heart pupils |
| Moomizu Cow Print Maillot | `gyunuslab.moomizu-this-mod-changes-both` | equip 2013 Aman Female Swimsuits 1 #131352 (aman female) |
| Butterfly Elin Face 9 Adornment 4 | `henapuff.butterfly` | character creator: elin any, pick face 9 |
| Revamp Elin Face 1 Adornment 4 | `henapuff.face-1-adornment-4-revamp` | character creator: elin any, pick face 1 |
| Freckles Elin Face 12 Adornment 3 | `henapuff.freckles` | character creator: elin any, pick face 12 |
| Freckles (Elin Face 12) | `henapuff.freckles-elin-face-12` | character creator: elin any, pick face 12 |
| Pearl Bow Recolors | `henapuff.pearl-bow-recolors` | equip Pastel Yellow Pearl Bow #263024 (any race) |
| Pearl Bow Recolors — Black | `henapuff.pearl-bow-recolors-black` | equip Pastel Yellow Pearl Bow #263024 (any race) |
| Pearl Bow Recolors — Blue | `henapuff.pearl-bow-recolors-blue` | equip Pastel Yellow Pearl Bow #263024 (any race) |
| Pearl Bow Recolors — Dark Blue | `henapuff.pearl-bow-recolors-dark-blue` | equip Pastel Yellow Pearl Bow #263024 (any race) |
| Pearl Bow Recolors — Dark Yellow | `henapuff.pearl-bow-recolors-dark-yellow` | equip Pastel Yellow Pearl Bow #263024 (any race) |
| Pearl Bow Recolors — Orange | `henapuff.pearl-bow-recolors-orange` | equip Pastel Yellow Pearl Bow #263024 (any race) |
| Pearl Bow Recolors — Other Pink | `henapuff.pearl-bow-recolors-other-pink` | equip Pastel Yellow Pearl Bow #263024 (any race) |
| Pearl Bow Recolors — Peach | `henapuff.pearl-bow-recolors-peach` | equip Pastel Yellow Pearl Bow #263024 (any race) |
| Pearl Bow Recolors — Pink | `henapuff.pearl-bow-recolors-pink` | equip Pastel Yellow Pearl Bow #263024 (any race) |
| Pearl Bow Recolors — Purple | `henapuff.pearl-bow-recolors-purple` | equip Pastel Yellow Pearl Bow #263024 (any race) |
| Pearl Bow Recolors — Red | `henapuff.pearl-bow-recolors-red` | equip Pastel Yellow Pearl Bow #263024 (any race) |
| Beige School Uniform Recolor | `herb0604.tera` | equip Blue-brown High School Uniform (Human Female) #179123 (human female) |
| Pink Cat Sports Car | `i.made-a-mod-of-car-add-the-cat-pictures-on-the` | equip Riding Skill: Sport GX800 #151945 (any race) |
| Korean Awakened Gunner Voices | `igeluu.awaken-gunner-skill-voice-mod-i-applied` | in game, look at the Gunner's awakening skill voice lines |
| Qipao Costume Retexture | `its.time` | equip Elegant Cheongsam (Human Female) #150226 (human female) |
| Pride Castanic Face 11 Adornment 11 | `kanstria.pride-in-celebration-of-pride-month` | character creator: castanic female, pick face 11 |
| Umbra Torpedo Swimsuit Recolor | `kanstria.umbra-for-the-sanguine-niveous` | equip Red Bandeau Swimsuit #60266 (aman female) |
| Wilted Summer Lei | `kanstria.wilted-for-the-summer-lei-download` | equip Summery Floral Crown #116023 (any race) |
| Katmods Animation Pack | `katmods.animation-pack` | in game, look at a set of combat, sit and emote animations on Elin (117 sequences) |
| GFTime Dance + School Sit | `katmods.gftime-school-sit` | in game, look at the /dance emote and the sit animations on Elin (112 sequences) |
| GFToday Dance | `katmods.gftoday-dance` | in game, look at the /dance emote animation (Elin) |
| Reaper and Standard Animations Swapped | `katmods.reaper-to-normal` | in game, look at the Reaper and standard stance animations on Elin (60 sequences) |
| Designer Shirt Red Details | `katmods.recolour-for-the-designer-shirt-3-some` | equip Amani Female Housekeeper Uniform #81146 (aman female) |
| Dark Red Fairy Wings | `katmods.recolour-for-the-new-fairy-wings-the` | equip Wood Pixie Wings #260636 (any race) |
| Frostrune Sword Recolor | `katmods.recolour-mod-for-frostrune-sword-top` | equip Frost Guards Twin Swords #256136 (any race) |
| Gold Glimmerdress Recolors | `katmods.so-more-elin-stuff-d-here-are-two` | equip Metallic Cocktail Dress (Amani Female) #252820 (aman female) |
| Pastel Blue Fishing Rod + Float | `kawaakari.pastel-fishing-rod-blue` | equip Old Fishing Rod #206700 (any race) |
| Still Into You Outfit | `khelpmods.still-into-you-still-into-you-i` | equip Sky Blue Academy Uniform (Amani Female) #154661 (aman female) |
| Blushy Perfect Evade Emote | `kirabera.blushy-emote-that-pops-up-during` | in game, look at the emote art on the Perfect Evade popup |
| Blushybane Skill Icon | `kirabera.blushybane-titansbaneuwu` | equip Riding Skill: Ostrich #137023 (any race) |
| Bright Pastel HP/MP Bar | `kirabera.bright-pastel-hpmp-bar-with-edge-and` | in game, look at the HP and MP bars in the character window |
| Bright Pastel Party UI | `kirabera.bright-pastel-party-ui-with` | in game, look at the party member frames |
| Isis Eyes (Elin Face 1) | `kittieology.isis-eye-mod-by-after` | equip Annihilation Arcannon #89581 (any race) |
| Elena Elite Steward 2012 Swimsuit | `kourinn.elena-elite-steward-swimsuit` | look at: Puts the 2012 swimsuit look on the Elite Steward companion |
| Shadowlaced Mooncloak Weapon Skins | `kourinn.shadowlaced-mooncloak-weapons` | look at: Reskins the tier-13 weapon set with the Shadowlaced Mooncloak art |
| Gudetama Thrall Lord | `la.petite-soeur-tera-thrall-lord-as-gudetama` | look at: Turns the Thrall Lord summon into Gudetama |
| Red Bloodshadow Ninjagi Fix | `lewdshi.red-bloodshadow-ninjagi-fix-updated` | equip Moonlight Armor (Human Male) #178653 (human male) |
| Watered Silk Black Stockings | `lewdshi.watered-silk-black-stockings` | equip Orchid Blossom Hanbok (Amani Female) #150810 (aman female) |
| River Dokkaebi Hanbok Retexture | `lilisahime.my-first-mod-an-outfit-mod-on-my` | equip Human Female Devilicious Costume #81155 (human female) |
| Elin Hairstyles 6 and 13 Retexture | `lilisahime.requested-hairstyle-hairstyle-1` | character creator: elin any, pick hair 6, 13 |
| Linaandasuka Elin Face 12 Adornment 2 | `linaandasuka.hay-there-i-dont-do-mods-but-i` | character creator: elin any, pick face 12 |
| School Uniform Recolor | `litterboxchan.a-re-color-of-the-school` | equip Midnight Blue Private School Uniform (Human Male) #205144 (human male) |
| Care Bear Panda Costumes | `litterboxchan.care-bear-recolors-the-panda` | equip Tough Teddy (Human Male) #179286 (human male) |
| Pink and Mint Christmas Skins | `litterboxchan.christmas-skins-pink-x-mint` | equip River Dokkaebi Hanbok (Human Male) #260808 (human male) |
| D.Va Swimsuit | `litterboxchan.dva-swimsuit-mod-for-the-new` | equip Triton Swimwear (Amani Female) #264184 (aman female) |
| Skirtless Dyeable Pixie Dress | `litterboxchan.dyeable-pixie-dress-mod-removes` | equip Wood Pixie Costume (Amani Female) #260492 (aman female) |
| Gingham Blossom Hanbok | `litterboxchan.gingham-blossom-thank-you` | equip Orchid Blossom Hanbok (Amani Female) #150810 (aman female) |
| Grump Cat Pink Ribbon | `litterboxchan.grump-cat-pink-ribbon` | equip Vigilant Velvet Paws #152283 (any race) |
| Hello Kitty Pink Car | `litterboxchan.hello-kitty-car-replaced-the` | equip Riding Skill: Sport GX800 #151945 (any race) |
| Sky Blue & Teal Koinobori | `litterboxchan.koinobori` | equip Riding Skill: Carnelian Koinobori #262704 (any race) |
| Lolita Goth Melody Recolor | `litterboxchan.l-o-l-i-t-a-a` | equip Party Noblesse Suit [Human Male] #141453 (human male) |
| Lil Red Picnic Dress | `litterboxchan.lilred-turns-the-green-picnic` | equip Frilled Sunday Dress (Human Female) #251388 (human female) |
| Bluebird Mount Recolor | `litterboxchan.litterboxchan` | equip [Event] Lilly #92135 (any race) |
| Lucky Star Uniform | `litterboxchan.lucky-star-lucky-star` | equip School Uniform (Human Female) #131218 (human female) |
| No Panda Ice Cream Staff | `litterboxchan.no-panda-ice-cream-staff` | equip Chocolate & Strawberry #131149 (any race) |
| Pastel Swimsuit 2019 | `litterboxchan.pastel-swimsuit-mod-2019` | equip Triton Swimwear (Human Male) #264004 (human male) |
| Pastel Varsity Jeans & Jacket | `litterboxchan.pastel-varsity-turns-the` | equip Arborean College Gear (Amani Female) #152357 (aman female) |
| Rico & Elo Pet Recolors | `litterboxchan.pets-i-re-colored-two-of-the` | look at: Recolors the Rico pet's event skin |
| Pink Bell Antlers | `litterboxchan.pink-bell-antlers-re-color` | equip Reindeer Hairband #115594 (any race) |
| Pink Idol Dress and Mic | `litterboxchan.pink-idol-dress-and-mic` | equip Golden Pop Star (Human Female) #257528 (human female) |
| Pink Reading Glasses & Rally Cap | `litterboxchan.pink-reading-glasses-pink-rally` | equip Orange Baseball Cap #151730 (any race) |
| Pink Skeleton Costume | `litterboxchan.pink-skeleton-costume-mod` | equip Human Male Skeleton Costume #146073 (human male) |
| Pink Snow Globe Mount | `litterboxchan.pink-snow-globe-removes-the` | equip Riding Skill: Wintera Snowbite #150656 (any race) |
| Popo Backpack Recolors | `litterboxchan.popo-backpack-white-pink` | equip Racoon Pipe Backpack #131235 (any race) |
| Rainbow Bunny Mount | `litterboxchan.rainbow-bunny-mount-changes-the` | equip [Event] Skill Manual: Cobalt Moon Bunny (30 Days) #206581 (any race) |
| Rainbow Syringe | `litterboxchan.rainbow-syringe-works-on-only` | equip Mega Syringe Green #116239 (any race) |
| Blue Airy Dress | `litterboxchan.ready-for-school-new-mod` | equip Cheerleader Outfit (Castanic Female) #151673 (castanic female) |
| Seren's Night Uniform White Socks | `litterboxchan.serens-night-uniform-white-sock` | equip Schoolgirl Outfit (Elin) #179183 (elin female) |
| Sheep Girl Pink Hood | `litterboxchan.sheep-girl-with-a-pink` | equip Little Hazel Riding Hood (Human Female) #268764 (human female) |
| Snowball Socko | `litterboxchan.snowball-socko-a-re-color-of` | equip Riding Skill: Noble Socks(Rare_Flower Effects) #147038 (any race) |
| Spring Maid Dress | `litterboxchan.spring-maid-dress` | equip Candy Apron (Human Female) #263048 (human female) |
| White Pig Mount | `litterboxchan.white-pig-turns-the-normal-pink` | equip Riding Skill: Waddles #137035 (any race) |
| White Pink Kitten Paws | `litterboxchan.white-pink-kitten-paws` | equip [Promotion] Fluffy White Cat Paw #141370 (any race) |
| Arcadian Academy Triple-T Uniform | `littleshistar.arcadian-academy-triple-t-school` | equip Blue-brown High School Uniform (Castanic Female) #179153 (castanic female) |
| Black Beret | `littleshistar.black-beret` | equip Black Academy Cap #154745 (any race) |
| Black Cat Ears | `littleshistar.black-cat-ears` | equip Cat Ears #160838 (any race) |
| Black Lil Devil Horns | `littleshistar.black-lil-devil-horns` | equip Petite Red Demon Headband #131328 (any race) |
| Black Swan Tiara Fix | `littleshistar.black-swan-tiara-fix` | equip [Event] White Feather Tiara #149369 (any race) |
| Blue Elin Ninjagi Costumes | `littleshistar.blue-elin-ninjagi-costumes` | equip Moonlight Armor (Amani Female) #178683 (aman female) |
| Blue Wreath | `littleshistar.blue-wreath` | equip Red Rudolph Hairband #60498 (any race) |
| Cardigan Charcoal Eldritch | `littleshistar.cardigan-charcoal-eldritch` | equip School Uniform A (HighElf Female) #131228 (castanic female) |
| Dyeable Alice Dress Fix | `littleshistar.dyeable-alice-dress-fix` | equip Dreamland Alice (Amani Female) #150124 (aman female) and DYE it (undyed matches vanilla) |
| Dyeable Heros Memorial Dress Fix | `littleshistar.dyeable-heros-memorial-dress-fix` | equip Human Female Devilicious Costume #81155 (human female) |
| Elin Tuxedo Fishnets | `littleshistar.elin-tuxedo-fishnets` | equip Conjurer's Costume (Amani Female) #150554 (aman female) |
| Notes By Dolme | `littleshistar.notes-by-dolme` | equip Stylish Headphones #115606 (any race) |
| Pastel Blue Spun Sugar Wings | `littleshistar.pastel-blue-spun-sugar-wings` | equip White Butterfly Wings #115181 (any race) |
| Pora Elinu Prep School Uniforms | `littleshistar.pora-elinu-prep-school-uniforms` | equip Sky Blue Academy Uniform (Amani Female) #154661 (aman female) |
| Snowflakes Summersilk Robe | `littleshistar.snowflakes-summersilk-robe` | equip Azure Blue Yukata (Amani Female) #265584 (aman female) |
| Llama Mount Recolor | `llama.recolor` | equip Riding Skill: Llara #154954 (any race) |
| Sad Pepe Block | `luke.block-sad-pepe` | in game, look at the Defense Success (block) popup |
| Hip Hop Rogue (Bandit Mask) | `magus-imperator.hip-hop-rogue` | equip Shadow Hunter Leather Mask[Untradable] #141385 (any race) |
| Lycoris (Castanic Male Hair 8) | `magus-imperator.lycoris-hair` | character creator: castanic any, pick hair 1 |
| Imperator Antipyretic Horse | `magus.imperator-antipyretic-although-i` | look at: Reskins the Bay Geld horse mount as a parody |
| Kun Accessory Recolors | `manooy.kun-a-recolor-on-accessories` | equip Medical Eye Patch Black #116235 (any race) |
| Matching Anniversary Wings | `matchingwings.matchingwings` | equip Destiny's Wings of Discord #255004 (any race) |
| Silver Eyes | `mayukari.hello-i-came-to-introduce-my-first-mod` | equip Annihilation Arcannon #89581 (any race) |
| Legitimate Boat Cadet (Elin) | `mayukari.legitimate-boat-cadet-elin-well-i` | equip Uniform 1 (Human Female) #131245 (human female) |
| Silver Eyes (Elin Face 11) | `mayukari.silver-eyes` | character creator: elin any, pick face 11 |
| Elin Face 12 Adornment 3 Decal | `miscellaneousdotcom.tera-mod-face-12-adornment` | character creator: elin any, pick face 12 |
| Dark Elin Face 9 Adornment 1 | `moddymcmodface.dark-download-here-for` | equip Annihilation Arcannon #89581 (any race) |
| Dark Human Face 3 Adornment 1 | `moddymcmodface.dark-download-here-human-f` | character creator: human female, pick face 2 |
| Glamour High Elf Face 2 Adornment 1 (Hair Ve | `moddymcmodface.glamour-high-elf-female-face-hair` | character creator: highelf female, pick face 1 |
| Honey Elin Face 9 Adornment 1 | `moddymcmodface.honey-download-here-for` | equip Annihilation Arcannon #89581 (any race) |
| Human Male Face 1 Adornment 1 Decal | `moddymcmodface.my-new-projects-are-giving-me-so` | look at: Replaces the human male Face 0 look — the face texture and its colour mask, plus the matching face decal |
| Gachi Block | `moonshi.block-gachi` | in game, look at the Defense Success (block) popup |
| Ricardo Milos Block | `moonshi.block-ricardo-milos` | in game, look at the Defense Success (block) popup |
| Black Cheerleader Outfit | `morcotulke.black-cheerleader` | equip Cheerleader Outfit (Castanic Female) #151673 (castanic female) |
| Black and White Qipao | `morcotulke.black-white-qipao` | equip Elegant Cheongsam (Amani Female) #150232 (aman female) |
| Amethyst Elin Face 11 Adornment 5 | `mtforum.amethyst` | character creator: elin any, pick face 11 |
| CosmicGreenPink Elin Face 11 Adornment 3 | `mtforum.cosmicgreenpink` | character creator: elin any, pick face 11 |
| CosmicPink Elin Face 11 Adornment 3 | `mtforum.cosmicpink` | character creator: elin any, pick face 11 |
| DarkIce Castanic F Face 1 Adornment 8 | `mtforum.darkice-castanicf` | character creator: castanic female, pick face 1 |
| Dragon Elin Face 8 Adornment 5 | `mtforum.dragon` | character creator: elin any, pick face 8 |
| Dragon No Shine Elin Face 8 Adornment 5 | `mtforum.dragon-no-shine` | character creator: elin any, pick face 8 |
| EmoPrincess Elin | `mtforum.emoprincess-elin` | character creator: elin any, pick face 10 |
| Enchantress Elin Face 10 Adornment 2 | `mtforum.enchantress` | character creator: elin any, pick face 10 |
| Goldie Elin Face 12 Adornment 2 | `mtforum.goldie` | character creator: elin any, pick face 12 |
| Hauntercatseye Elin Face 11 Adornment 5 | `mtforum.hauntercatseye` | character creator: elin any, pick face 11 |
| Haunterdreamyeyes Elin Face 8 Adornment 5 | `mtforum.haunterdreamyeyes` | character creator: elin any, pick face 8 |
| Hearteyes Elin Face 8 Adornment 5 | `mtforum.hearteyes` | character creator: elin any, pick face 8 |
| Honey Elin Face 11 Adornment 5 | `mtforum.honey` | character creator: elin any, pick face 11 |
| Hu Tao Eyes Elin Face 8 Adornment 5 | `mtforum.hu-tao-eyes` | character creator: elin any, pick face 8 |
| Hu Tao Eyes Elin Face 11 Adornment 5 | `mtforum.hu-tao-eyes-11-05` | character creator: elin any, pick face 11 |
| Hu Tao Eyeses Elin Face 8 Adornment 5 | `mtforum.hu-tao-eyeses` | character creator: elin any, pick face 8 |
| Indigo Elin Face 10 Adornment 2 | `mtforum.indigo` | character creator: elin any, pick face 10 |
| Light Green Eyes Elin Face 8 Adornment 5 | `mtforum.light-green-eyes` | character creator: elin any, pick face 8 |
| Mioh Makeup F9A3 Elin Face 9 Adornment 3 | `mtforum.mioh-makeup-f9a3` | character creator: elin any, pick face 9 |
| NightBlue Elin Face 12 Adornment 2 | `mtforum.nightblue` | character creator: elin any, pick face 12 |
| Pantypon Yandere Elin Face 12 Adornment 2 | `mtforum.pantypon-yandere-face12-adorment2` | character creator: elin any, pick face 12 |
| Pink Eyes Elin Face 8 Adornment 5 | `mtforum.pink-eyes` | character creator: elin any, pick face 8 |
| PinkPinkPink Elin Face 11 Adornment 5 | `mtforum.pinkpinkpink` | character creator: elin any, pick face 11 |
| Plum Elin Face 8 Adornment 5 | `mtforum.plum` | character creator: elin any, pick face 8 |
| Pretty Eyes Elin Face 1 Adornment 3 | `mtforum.pretty-eyes-mod` | character creator: elin any, pick face 1 |
| Red | `mtforum.red` | character creator: elin any, pick face 1 |
| RoyalAmber Castanic F Face 1 Adornment 6 | `mtforum.royalamber-castanicf` | character creator: castanic female, pick face 1 |
| Skull Emogi Elin Face 11 Adornment 5 | `mtforum.skull-emogi-11-5` | character creator: elin any, pick face 11 |
| Starry Elin Face 5 Adornment 2 | `mtforum.starry` | character creator: elin any, pick face 5 |
| Sunset Elin Face 12 Adornment 2 | `mtforum.sunset` | character creator: elin any, pick face 12 |
| Sweet Memories Elin Face 11 Adornment 5 | `mtforum.sweet-memories` | character creator: elin any, pick face 11 |
| Valentines Eyes 2.0 Elin Face 8 Adornment 5 | `mtforum.valentines-eyes-2-0-mod` | character creator: elin any, pick face 8 |
| Valentines Eyes 2.0 Pink Elin Face 8 Adornme | `mtforum.valentines-eyes-2-0pink-mod` | character creator: elin any, pick face 8 |
| Valentines Eyes Elin Face 11 Adornment 5 | `mtforum.valentines-eyes-mod` | character creator: elin any, pick face 11 |
| Zombie Patch Elin Face 8 Adornment 5 | `mtforum.zombie-patch` | character creator: elin any, pick face 8 |
| King Thrall | `mystics.king-thrall-mod` | look at: Retextures the King Thrall summon |
| Dyeable Wedding Dress Fix | `nadeko22.dyeable-wedding-dress-mod-ive-always` | equip Human Female Devilicious Costume #81155 (human female) |
| Deep Teal Eyes Elin Face 11 Adornment 5 | `nefristreo.deep-teal-eyes` | character creator: elin any, pick face 11 |
| Forester Elin Face 11 Adornment 5 | `nefristreo.forester-im-mixed-with-this-one` | character creator: elin any, pick face 11 |
| Two-Tone High Elf Face 1 | `nefristreo.mod-for-a-friend-makes-the-hair-for` | character creator: highelf female, pick face 1 |
| Azn Human Male Face & Hair Retexture | `nmg.1305-azn-so-i-guess-people-wont-do-much-for` | equip Martial Artist's Helmet #153264 (any race) |
| Artemis Felicity | `norukjerky.artemis-felicity-mod-made-this` | look at: Recolors the Felicity pet with an Artemis theme |
| Sailor Moon Luna Cat | `norukjerky.based-off-luna-from-sailor-moon` | look at: Turns the cat pet into Luna from Sailor Moon |
| FaceMod01 Elin Face 10 Adornment 4 | `norukjerky.facemod01` | character creator: elin any, pick face 10 |
| Plain Brawler Rage Bar | `norukjerky.finally-i-got-lazy-first-off-i` | in game, look at the Brawler rage bar |
| Little White Dress | `norukjerky.little-white-dress-since-a-few` | equip Spring Breeze Hanbok (Amani Female) #150801 (aman female) |
| Keikogi Retexture (Elin) | `norukjerky.my-first-mod-in-ages-so-i-apologize` | equip Martial Artist's Keikogi (Amani Female) #153228 (aman female) |
| Pink Eye Elin Face 11 Adornment 3 | `norukjerky.pink-eye` | character creator: elin any, pick face 11 |
| Rainbow Robin | `norukjerky.rainbow-robin-since-a-few-people` | equip Riding Skill: Ostrich #137023 (any race) |
| Black Dress for Castanics | `norukjerky.recoloured-dress-for-castanics-as` | equip Spring Breeze Hanbok (Amani Female) #150801 (aman female) |
| Riddling Set Texture Replacement | `norukjerky.riddling-set-texture-replacement` | look at: Replaces the Elin Riddling set textures for the plate, leather and cloth pieces |
| KakaoTalk Ryan | `norukjerky.something-cute-ive-wanted-to-make` | look at: Retextures a pet as Ryan from KakaoTalk |
| Dark Sketch Block | `nyanko.block-dark-sketch` | in game, look at the Defense Success (block) popup |
| Kuromi Block | `nyanko.block-kuromi` | in game, look at the Defense Success (block) popup |
| Onigiri Cat Block | `nyanko.block-onigiri-cat` | in game, look at the Defense Success (block) popup |
| Onigiri Cat Block II | `nyanko.block-onigiri-cat-2` | in game, look at the Defense Success (block) popup |
| Sketch Girl Block | `nyanko.block-sketch-girl` | in game, look at the Defense Success (block) popup |
| Cat Meme Counterattack | `nyanko.counter-cat` | in game, look at the Defense Success (block) popup |
| Kaneki Counterattack | `nyanko.counter-kaneki` | in game, look at the Defense Success (block) popup |
| Bunny Hair (Elin Hair 5) | `nyankouu.bunny-hair` | character creator: elin any, pick hair 5 |
| Mimikyu Snowsuit | `nyankouu.mimikyu-snowsuit-mod-i-dont-own` | equip Snowsuit (Human Male) #131076 (human male) |
| Pinky Elin Face 11 Adornment 5 | `nyankouu.pinky-mod-for-the-new-ninja-face` | character creator: elin any, pick face 11 |
| Black Cowgirl Recolor | `nyankouu.recolour-mod-cowgirl-black` | equip Wrestling Costume (Human Male) #252096 (human male) |
| FPS Pack: Awaken FX Archer | `owyn.fps-pack-fx-awaken-archer` | in game, look at the awakening visual effects for archer |
| FPS Pack: Awaken FX Berserker | `owyn.fps-pack-fx-awaken-berserker` | in game, look at the awakening visual effects for berserker |
| FPS Pack: Awaken FX Lancer | `owyn.fps-pack-fx-awaken-lancer` | in game, look at the awakening visual effects for lancer |
| FPS Pack: Awaken FX Priest | `owyn.fps-pack-fx-awaken-priest` | in game, look at the awakening visual effects for priest |
| FPS Pack: Awaken FX Slayer | `owyn.fps-pack-fx-awaken-slayer` | in game, look at the awakening visual effects for slayer |
| FPS Pack: Awaken FX Sorcerer | `owyn.fps-pack-fx-awaken-sorcerer` | in game, look at the awakening visual effects for sorcerer |
| FPS Pack: Awaken FX Warrior | `owyn.fps-pack-fx-awaken-warrior` | in game, look at the awakening visual effects for warrior |
| FPS Pack: FX Enchant | `owyn.fps-pack-fx-enchant` | in game, look at the enchanting visual effects |
| Albino (Elin Face 7, Adornment 1) | `pantypon.albino-face` | character creator: elin any, pick face 7 |
| Alice Blue Ribbon Bow Fix | `pantypon.alice-blue-bow-fix` | equip Light Blue Hair Ribbon #116107 (any race) |
| Apple Tart Elin Face 11 Adornment 5 | `pantypon.apple-tart-elin-face-11-adornment-5` | character creator: elin any, pick face 11 |
| Archer Pink Slingshot | `pantypon.archer-pink-slingshot` | equip Chocolate & Strawberry #131149 (any race) |
| Battle Bunny Gunner Companion | `pantypon.battle-bunny-for-gunner-awakened` | look at: Retextures the Gunner's awakened mecha companion in pastel pink with bunnies, strawberries and stars |
| Berserker Dessert Fork | `pantypon.berserker-dessert-fork` | equip Shish Kebab #131151 (any race) |
| Better Dyeable Flight Suit | `pantypon.better-dyeable-flight-suit-changes` | equip IM39 Prototype (Amani Female) #99750 (aman female) |
| Black Double Buns | `pantypon.black-double-buns` | equip Double Bobble Hairband #116124 (any race) |
| Black Sheep Doll Hat | `pantypon.black-sheep-doll-this-mod-is-made-by` | equip Velik's Festival Hat #424 (any race) |
| Brighter Whiter Hair (Castanic Hair 11) | `pantypon.castanic-brighter-whiter-hair-11` | character creator: castanic female, pick hair 11 |
| Castanic Face 11 Adornment 8 | `pantypon.castanic-f11a8` | character creator: castanic female, pick face 11 |
| Freckles (Castanic Face 2) | `pantypon.castanic-freckles` | character creator: castanic female, pick face 2 |
| Castanic Hair 15, White Horns | `pantypon.castanic-hair15-white-horns` | character creator: castanic female, pick hair 15 |
| Brighter Whiter Hair 12 (Castanic Female) | `pantypon.castanic-whiter-hair-12` | character creator: castanic female, pick hair 12 |
| Cotton Candy Face 8 Adornment 5 | `pantypon.cotton-candy-face-8-adornment-5` | character creator: elin any, pick face 8 |
| Cute Crafter Icons | `pantypon.cute-crafter-icons` | in game, look at the system icons |
| D.Va Backpack | `pantypon.dva-backpack-this-mod-changes` | equip Pink College Backpack #152414 (any race) |
| Dyeable 2020 Hanbok Shoulder Fix | `pantypon.dyeable-2020-hanbok-fix-shoulder-pad` | equip Skyrider's Robes (Human Male) #267512 (human male) |
| Dyeable Housekeeper Fix | `pantypon.dyeable-housekeeper-fix` | equip Human Female Housekeeper Uniform #81144 (human female) and DYE it (undyed matches vanilla) |
| Elin Better Dyeable 2019 Swimsuit | `pantypon.elin-better-dyeable-2019-swimsuit-v1` | equip Triton Swimwear (Amani Female) #264184 (aman female) |
| Elin Black Business Suit | `pantypon.elin-black-business-suit` | equip [TBU] #131808 (human male) |
| Elin Black Sleeve Business Suit | `pantypon.elin-black-sleeve-business-suit` | equip [TBU] #131818 (aman female) |
| Elin Brighter New Hairstyles | `pantypon.elin-brighter-new-hairstyles` | character creator: elin any, pick hair 1, 4 |
| Elin English Lavender Raincoat | `pantypon.elin-english-lavender-raincoat` | equip Elin Raincoat #154850 (elin female) |
| Elin Face 1 Adornment 2 | `pantypon.elin-face-1-adornment-2` | character creator: elin any, pick face 1 |
| Elin Face 1 Adornment 3 Decal | `pantypon.elin-face-1-adornment-3-the` | character creator: elin any, pick face 1 |
| Demon Elin Face 11 Adornment 5 | `pantypon.elin-face-11-adornment-5-demon` | character creator: elin any, pick face 11 |
| Ice Queen Elin Face 11 Adornment 5 | `pantypon.elin-face-11-adornment-5-ice-queen` | character creator: elin any, pick face 11 |
| Sapphire Elin Face 11 Adornment 5 | `pantypon.elin-face-11-adornment-5-sapphire` | character creator: elin any, pick face 11 |
| Yandere Elin Face 12 Adornment 2 | `pantypon.elin-face-12-adonrment-2-yandere` | character creator: elin any, pick face 12 |
| Senseless Elin Face 12 Adornment 3 | `pantypon.elin-face-12-adornment-3-senseless` | character creator: elin any, pick face 12 |
| Ghost Elin Face 8 Adornment 4 | `pantypon.elin-face-8-adornment-4-ghost` | character creator: elin any, pick face 8 |
| Cosmic Elin Face 8 Adornment 5 | `pantypon.elin-face-8-adornment-5-cosmic` | character creator: elin any, pick face 8 |
| Pantypon Plum Elin Face 8 Adornment 5 | `pantypon.elin-face-8-adornment-5-plum` | character creator: elin any, pick face 8 |
| Black Doll Elin Face 9 Adornment 2 | `pantypon.elin-face-9-adornment-2-black-doll` | character creator: elin any, pick face 9 |
| Elin Pale Writer Shoes and Socks Fix | `pantypon.elin-pale-writer-shoes-fix` | equip School Uniform (Human Female) #131218 (human female) |
| Elin Pink Social Dress | `pantypon.elin-pink-social-dress` | equip Frilled Sunday Dress (Human Female) #251388 (human female) |
| Elin Prettier Skin | `pantypon.elin-prettier-skin` | equip Conjurer's Costume (Amani Female) #150554 (aman female) |
| Elin Smooth Skin | `pantypon.elin-smooth-skin-this-mod-is-super` | equip Disciplinary Genya's Black Lace Innerwear #9375 (aman female) |
| Elin Strawberry Maid | `pantypon.elin-strawberry-maid` | equip Chambermaid's Dress (Human Female) #254300 (human female) |
| Elin Sugar Alice | `pantypon.elin-sugar-alice` | equip Clover-green Kobold Tailcoat (Human Male) #262524 (human male) |
| Fairy Stump Mount | `pantypon.fairy-stump-mount` | equip Riding Skill: Buzzer(Rare) #147031 (any race) |
| Flying Pink Cushion Mount | `pantypon.flying-pink-cushion-mount` | equip Festive Carpet #70050 (any race) |
| Ice Cream Social - Black Pantyhose | `pantypon.ice-cream-black-pantyhose` | equip Frilled Sunday Dress (Human Female) #251388 (human female) |
| Ice Cream Social - White Pantyhose and Shoes | `pantypon.ice-cream-white-pantyhose-shoes` | equip Frilled Sunday Dress (Human Female) #251388 (human female) |
| Just Bows (Ribbon Headbands) | `pantypon.just-bows` | equip Black Headband with Ears #115741 (any race) |
| Just Bows Hello Kitty Pink Headband | `pantypon.just-bows-hello-kitty-pink-headband` | equip Hello Kitty Pink Headband #185433 (any race) |
| Kitsune Mask Remake | `pantypon.kitsune-mask-remake-this-mask-is` | equip Kitsune Mask #115387 (any race) |
| Hair-Matching Angel Wings | `pantypon.matching-angel-wings-this-mod-makes` | equip Snow White Angel Wings #27377 (any race) |
| Hair-Matching Archangel Wings | `pantypon.matching-archangel-wings-this-mod` | equip Ruby Snow Blossom Hanbok (Human Female) #153354 (human female) |
| MultiClass Just Plasma | `pantypon.multiclass-just-plasma` | equip Blue Plasma Smart Box #184121 (any race) |
| Mystic Iceglow Rod | `pantypon.mystic-iceglow-rod` | equip Icegrip Twin Swords #131127 (any race) |
| Mystic Ninja Oni Removal | `pantypon.mystic-ninja-oni-removal` | equip Ninja Three-Oni Scepter #180799 (any race) |
| Mystic Strawberry Nuthatch | `pantypon.mystic-strawberry-nuthatch` | look at: Replaces the Mystic scepter in the PC Weapons Event09 event weapon-skin family |
| Mystic Wand, Better Pink | `pantypon.mystic-wand-pink` | look at: Recolors the witch event rod model in pink |
| Ninja Pink Prop Fan | `pantypon.ninja-pink-prop-fan` | equip Chocolate & Strawberry #131149 (any race) |
| No Poofs, No Curls + Pink | `pantypon.no-poofs-no-curls` | character creator: elin any, pick hair 47 |
| O Death Elin Face 11 Adornment 5 | `pantypon.o-death-elin-face-11-adornment-5` | character creator: elin any, pick face 11 |
| Panda Elin Face 11 Adornment 5 | `pantypon.panda-this-entire-outfit-look-is` | character creator: elin any, pick face 11 |
| Pastel Pink Ribbon | `pantypon.pastel-pink-ribbon-requested-by` | equip Crimson Bowler Hat #251568 (any race) |
| Pastel Pora Elinu Uniform | `pantypon.pastel-pora-elinu-uniform` | equip Sky Blue Academy Uniform (Human Female) #154607 (human female) |
| Pastel Purple Alice Bow | `pantypon.pastel-purple-alice-bow-request` | equip Black Hair Ribbon #116106 (any race) |
| Pink Snowbelle (Elin) | `pantypon.pink-elin-snowbelle-requested-by` | equip Festive Costume (Aman Female) #155340 (aman female) |
| Pink Picnic Dress | `pantypon.pink-picnic-dress` | equip Frilled Sunday Dress (Human Female) #251388 (human female) |
| Pink Royal Diamond Dragon Mount | `pantypon.pink-royal-diamond-dragon-mount` | look at: Replaces the golden dragon flying mount model |
| Pink Santa Hood | `pantypon.pink-santa-hood-requested-by-anon` | equip Festive Hat #115593 (any race) |
| Pink Skill Slots (Ex) | `pantypon.pink-skill-slots-ex` | in game, look at the on-screen message popups |
| Pink Skill Slots (Ex2) | `pantypon.pink-skill-slots-ex2` | in game, look at the on-screen message popups |
| Pink Skill Slots (Main) | `pantypon.pink-skill-slots-main` | in game, look at the on-screen message popups |
| Pink Snowbelle (Castanic/Aman/Elf) | `pantypon.pink-snowbelle-request-requested` | equip Festive Costume (Aman Female) #155340 (aman female) |
| Pink Winter Scarves | `pantypon.pink-winter-scarves-i-just-thought` | equip Snowy Winter Scarf #150713 (any race) |
| Priest Iceglow Staff | `pantypon.priest-iceglow-staff` | equip Icegrip Twin Swords #131127 (any race) |
| Red Miko Costume | `pantypon.red-miko-costume` | equip Ruby Snow Blossom Hanbok (Human Female) #153354 (human female) |
| Red Ribbon Bow | `pantypon.red-ribbon-bow-requested-by` | equip Black Hair Ribbon #116106 (any race) |
| Sand (Elin Face 5, Adornment 3) | `pantypon.sand-face` | character creator: elin any, pick face 5 |
| Sharingan Eyes (Elin Face 1, Adornment 2) | `pantypon.sharingan-eyes` | character creator: elin any, pick face 1 |
| Sherbert Days (Mystic Staff) | `pantypon.sherbert-days` | look at: Recolors one staff weapon model |
| Static Heart Crosshair | `pantypon.static-heart-crosshair` | in game, look at the aiming crosshair (and 1 more) |
| Strawberry Sundae (Elin Face 12, Adornment 1 | `pantypon.strawberry-sundae-face` | character creator: elin any, pick face 12 |
| Sugar Alice St. Patrick's Day | `pantypon.sugar-alice-st-patricks-day` | equip Clover-green Kobold Tailcoat (Human Male) #262524 (human male) |
| Sugar Witch Loo/Rumi | `pantypon.sugar-witch-works-on-loorumi` | look at: Recolors the Loo/Rumi companion pet into a sugar pink witch |
| Tea Time Raincoats | `pantypon.tea-time-raincoats` | equip Elin Raincoat #154850 (elin female) |
| White Dragon Elin Face 11 Adornment 5 | `pantypon.white-dragon-elin-face-11-adornment` | character creator: elin any, pick face 11 |
| White Sinestral Academy Uniform | `pantypon.white-sinestral-academy-uniform` | equip Sky Blue Academy Uniform (Human Female) #154607 (human female) |
| White SWAT Cap | `pantypon.white-swat-cap-requested-by` | equip SWAT Team Cap #250276 (any race) |
| Wreath Recolor Pack | `pantypon.wreath-recolor-mod-pack-this-mod` | equip Red Rudolph Hairband #60498 (any race) |
| Yunicorn Defense Pop Up | `pantypon.yunicorn-defense-pop-up` | in game, look at the Defense Success (block) popup |
| Phoenixclaw Gi Rework | `phoenixgi.phoenixgi` | equip Martial Artist's Keikogi (Human Male) #153198 (human male) |
| Zepheryine Head Accessory | `pinkteachan.aura-kingdom-zepheryine-head-for` | equip Blue Tuwangi Turban #50057 (any race) |
| Pompoms | `pompoms.pompoms` | equip Reindeer Hairband #115594 (any race) |
| Cherries Police Uniform | `puppetplayers.cherries-this-mod-goes-for-the` | equip TERA Police Officer (Amani Male) #150310 (aman female) |
| Fox Hair (Elin Hair 8) | `puppetplayers.fox-hair` | character creator: elin any, pick hair 8 |
| Muted Raid Window Colors | `puppetplayers.hi-friends-just-dropping-a` | in game, look at the raid windows |
| Shades to Reading Glasses | `puppetplayers.these-heckin-shades-into-regular` | look at: Turns the shades accessory into reading glasses |
| White Tie-Up Hair Accessory | `puppetplayers.white-recolor-of-red-tie-up` | equip Orange Cheerful Headband #151739 (any race) |
| Steel Wings to Angel Wings | `purpleelf.steel-wings-to-angel` | equip Steel-Tipped Devil Wings #155193 (any race) |
| Steel Wings to Demon Wings | `purpleelf.steel-wings-to-demon` | equip Steel-Tipped Devil Wings #155193 (any race) |
| Steel Wings to Demonic Wings | `purpleelf.steel-wings-to-demonic` | equip Steel-Tipped Devil Wings #155193 (any race) |
| Steel Wings to Raven Wings | `purpleelf.steel-wings-to-raven` | equip Steel-Tipped Devil Wings #155193 (any race) |
| Experiment Elin Face 11 Adornment 2 | `readeyedghost.experiment` | character creator: elin any, pick face 11 |
| Cheeks Popori Boy NPC Recolor | `recolor.for-cheeks` | look at: Recolors the popori boy NPC Cheeks |
| 2017 Maid Dress Recolor (Elin) | `recolor.of-2017-maid-dress-for-elin` | equip Chambermaid's Dress (Amani Female) #254348 (aman female) |
| Snowsilk Winter Dress Recolor (Elin) | `recolor.of-snowsilk-winter-dress-for-elin` | equip Ruby Snow Blossom Hanbok (Human Female) #153354 (human female) |
| Morighost Elin Face 7 Adornment 3 | `sheinamaried.morighost-my-mod-for-whatever` | character creator: elin any, pick face 7 |
| Elin Short Hair | `short.hair-for-elin` | look at: Retextures one Elin hairstyle |
| Smoothmt Elin Face 11 Adornment 5 | `smoothmt.this-mod-is-for-elin-face-11-adornment` | character creator: elin any, pick face 11 |
| Frost Business Suit | `snugglezz.snugglezz` | equip Imperial Nutcracker Jacket (Amani Female) #258572 (aman female) |
| Rainbow Eyes Blush Elin Face 8 Adornment 5 | `stardustkujo.rainbow-eyes-blush` | character creator: elin any, pick face 8 |
| Bear Animal Mask | `taylorswiftmodding.bear-animal-mask` | equip Shadow Hunter Leather Mask[Untradable] #141385 (any race) |
| Blacker Bow | `taylorswiftmodding.blacker-bow` | equip Black Hair Ribbon #116106 (any race) |
| Bunny Chu | `taylorswiftmodding.bunny-chu-mount` | equip Riding Skill: Llara #154954 (any race) |
| Candied Dragon | `taylorswiftmodding.candied-dragon` | equip Sunny Gold Dragon Box #138071 (any race) |
| Grin and Bear It (with Cocomin) | `taylorswiftmodding.grin-and-bear-it-cocomin` | look at: Retextures the Acc_557 and Acc_562 accessories and the Cocomin partner |
| Grin and Bear It (with KunKun) | `taylorswiftmodding.grin-and-bear-it-kunkun` | look at: Retextures the Acc_557 and Acc_562 accessories and the KunKun partner |
| Happy Kitty Animal Mask | `taylorswiftmodding.happy-kitty-mask` | equip Shadow Hunter Leather Mask[Untradable] #141385 (any race) |
| I Can Haz Backpack | `taylorswiftmodding.i-can-haz-backpack` | equip Cat Backpack #131234 (any race) |
| Maria Maria | `taylorswiftmodding.maria-maria` | look at: Replaces the event skin of the partner (pet) Rumi |
| Peaches and Jeans | `taylorswiftmodding.peaches-and-jeans` | equip Chambermaid's Dress (Human Female) #254300 (human female) |
| Pikachu Raincoat | `taylorswiftmodding.pikachu-raincoat` | equip Elin Raincoat #154850 (elin female) |
| Pinky Kun | `taylorswiftmodding.pinky-kun` | look at: Replaces the event skin of the partner (pet) KunKun |
| Dyeable Evening Apparel Rework | `tera.elin-aesthetics-hi-i-made-a` | equip Disciplinary Genya's Black Lace Innerwear #9375 (aman female) |
| Soft Crescent Moon Dress | `tera.elin-aesthetics-hii-i-changed-dyeable` | equip Noble Crescent Moon Dress (Amani Female) #268436 (aman female) |
| Halloween Mummy Mod | `tera.halloween-mummy-mod` | equip Human Female Devilicious Costume #81155 (human female) |
| Dress Part-Removal Variants | `tera.majuki-norukjerky-this-was-just-me` | equip Spring Breeze Hanbok (Amani Female) #150801 (aman female) |
| Candy Pop (Elin Face 12) | `terabuns.candy-pop-face` | character creator: elin any, pick face 12 |
| Remove Artisan Icons | `teralove.remove-artisan-icons` | in game, look at the system icons |
| Dyeable Sheriff Uniform | `tetorichu.dyeable-sheriff-uniforme-mods` | equip Sheriff Uniform (Amani Female) #252216 (aman female) and DYE it (undyed matches vanilla) |
| Adventure Time Red Cap | `tetorichu.hey-guys-its-my-first-mods` | equip Orange Baseball Cap #151730 (any race) |
| Predator (Castanic Face 4) | `timeless-woods.predator-face` | character creator: castanic female, pick face 4 |
| Black Carnival Captain Cap | `timeless.woods-black-carnival-captain-cap` | equip Captain's Hat #116026 (any race) |
| Black Summer Sunglasses | `timeless.woods-black-summer-sunglasses-mod` | equip Stylish Shades #116022 (any race) |
| Cat Hair Tie Recolor | `timeless.woods-cat-hair-tie-recolor-changes` | look at: Recolors the hairband on the small ponytail hairstyle |
| Plain Anniversary Scarf | `timeless.woods-do-you-like-the-color-of-the` | equip Purple Anniversary Scarf #254008 (any race) |
| Pink Heart Shades | `timeless.woods-pink-heart-shades-turns` | equip Heart Shades #131350 (any race) |
| Vampira Castanic Face 4 Adornment 1 | `timeless.woods-vampira-another-mod-for` | look at: Replaces the Castanic female face decal at Face 4, Adornment 1 |
| Casual and Formal Finishing School | `tsweetypie.casualformal-finishing-school` | equip Sky Blue Academy Uniform (Amani Female) #154661 (aman female) |
| Pink & Purple Wolf | `tsweetypie.pinkpurple-wolf-mod-this-only` | equip Riding Skill: Ookami #100974 (any race) |
| White Ribbon | `tsweetypie.white-ribbon-mod-replaces-red` | equip Red Tie-Up #183681 (any race) |
| Blue Eyes Elin Face 8 Adornment 5 | `tyfia.blue-eyes` | character creator: elin any, pick face 8 |
| Pink Thrall of Vengeance | `tyfia.pinky-thrall-of-vengeance-my-mystic-is` | look at: Recolors the Mystic's Thrall of Vengeance pink |
| Purple Staff 19 Weapon Skin | `tyfia.purple-mods-face-mods-elin` | equip Frost Guards Twin Swords #256136 (any race) |
| Blue Eye Elin Face 8 Adornment 5 | `unamusedelin.blue-eye` | character creator: elin any, pick face 8 |
| Red Eye Elin Face 8 Adornment 5 | `unamusedelin.red-eye` | character creator: elin any, pick face 8 |
| Silver Eye Elin Face 8 Adornment 5 | `unamusedelin.silver-eye` | character creator: elin any, pick face 8 |
| Soft Lipstick (Elin Face 5) | `unamusedelin.soft-lipstick` | character creator: elin any, pick face 5 |
| Soft Lipstick (Elin Face 5) — Nude | `unamusedelin.soft-lipstick-nude` | character creator: elin any, pick face 5 |
| Soft Lipstick (Elin Face 5) — Pink | `unamusedelin.soft-lipstick-pink` | character creator: elin any, pick face 5 |
| Black Light Shine Damage | `unknown.black-light-shine` | in game, look at the in-game text, which uses these fonts everywhere |
| Boom Crit | `unknown.boom-crit` | in game, look at the in-game text, which uses these fonts everywhere |
| Butterfly Crits Cyan | `unknown.butterfly-crit-cyan` | in game, look at the in-game text, which uses these fonts everywhere |
| Butterfly Crits Orange/Green | `unknown.butterfly-crit-orange` | in game, look at the in-game text, which uses these fonts everywhere |
| Butterfly Crits Purple | `unknown.butterfly-crit-purple` | in game, look at the in-game text, which uses these fonts everywhere |
| Butterfly Crits Red | `unknown.butterfly-crit-red` | in game, look at the in-game text, which uses these fonts everywhere |
| Small Transparent Digits 50% | `unknown.digits-small-50-transp` | in game, look at the in-game text, which uses these fonts everywhere |
| Dragon Crit White (0% transparency) | `unknown.dragon-crit-white-0` | in game, look at the in-game text, which uses these fonts everywhere |
| Flower Crits | `unknown.flower-crits` | in game, look at the in-game text, which uses these fonts everywhere |
| Halloween Bat Crits | `unknown.halloween-bat-crits` | in game, look at the in-game text, which uses these fonts everywhere |
| Ninja Stance + Sit + GFTime | `unknown.ninja-sit-gftime` | in game, look at the ninja stance, sit and /dance animations on Elin (178 sequences) |
| Pink Font & Crit Splash (Shemyaza) | `unknown.pink-font-crit-splash` | in game, look at the in-game text, which uses these fonts everywhere |
| Agnes White Iris Face 11 Adornment 8 | `veinlace.agnes-face-11-adorn-8-white-iris` | character creator: castanic female, pick face 11 |
| Black & Pink Rose Eyepatch | `veinlace.black-pink-rose-didnt-really` | equip Red Rose Eye Patch #115388 (any race) |
| Bony Visage Recolored Skull Mask | `veinlace.bony-visage-recolored-skull-mask` | equip Shadow Hunter Skeletal Mask[Untradable] #141384 (any race) |
| Cold Shoulder Aman Face 6 Adornment 3 | `veinlace.cold-shoulder-face-6-adornment-a` | character creator: aman female, pick face 5 |
| Gremlin 2.0 Castanic Face 11 Adornment 8 | `veinlace.gremlin-20-you-ever-wanted-to` | character creator: castanic female, pick face 11 |
| Jaded AF Castanic Face 11 Adornment 8 | `veinlace.jaded-af-u-come-into-my-inbox-and` | character creator: castanic female, pick face 11 |
| Jaded Red Castanic Face 11 Adornment 11 | `veinlace.jaded-face-11-adornment-11-red` | character creator: castanic female, pick face 11 |
| Love Letters Dark Brows Castanic Face 11 Ado | `veinlace.love-letters-w-dark-brows-requested` | character creator: castanic female, pick face 11 |
| Party Monster Castanic Face 11 Adornment 8 | `veinlace.party-monster-for-face-11-adornment-8` | character creator: castanic female, pick face 11 |
| Trauma Blood-Splatter Eyepad | `veinlace.trauma-another-eyepatch-mod-but-for` | equip Medical Eye Patch White #116233 (any race) |
| Volcanic Kelsaik Helmet | `veinlace.volcanic-kelsaik-requested-by` | equip Kelsaik Mask #60719 (any race) |
| Elin Sitting Animation | `watmod.this-mod-was-inspired` | look at: Replaces the Elin sitting animation, including face, hair and tail motion |
| Wings Damage & Heal | `well.wings-damage-heal` | in game, look at the in-game text, which uses these fonts everywhere |
| Asian Silk Dress Patterns | `yunachiu.asian-silk-dress-patterns` | equip Elegant Cheongsam (Amani Female) #150232 (aman female) |
| Bewitching Elin (Face 11, Adornment 1) | `yunachiu.bewitching-elin-face` | character creator: elin any, pick face 11 |
| Black Scarf Recolor | `yunachiu.black-scarf-recolor` | equip Sullen Winter Scarf #150707 (any race) |
| Butterfly Heal Effect | `yunachiu.butterfly-heal-effect` | in game, look at the in-game text, which uses these fonts everywhere |
| School Uniform Recolors (Elin) | `yunachiu.i-make-a-mod-of-the` | equip School Uniform (Human Female) #131218 (human female) |
| Plaid Aubergine Topper | `yunachiu.i-make-a-mod-of-the-aubergine-topper` | equip Brilliant Topper #141477 (any race) |
| Pink & Purple Boat Cadet (Elin) | `yunachiu.i-make-a-mod-of-the-boat-cadet` | equip Uniform 1 (Castanic Female) #131261 (castanic female) |
| Kunoichi Robe Recolors (Elin) | `yunachiu.i-make-a-mod-of-the-kunoichi-robe-to` | equip Kunoichi Robes #154605 (elin female) |
| White Rogue's Weapon (Gunner) | `yunachiu.i-make-a-mod-of-the-rogues-weapon` | look at: Recolors the Rogue's Weapon white, Gunner only |
| Green Plaid Scarf Recolors | `yunachiu.i-make-some-mods-of` | equip Checkered Winter Scarf #116348 (any race) |
| Kurumi Clock Eyes (Elin Face 12) | `yunachiu.kurumi-clock-eyes` | character creator: elin any, pick face 12 |
| BL Manga Book Covers | `yunachiu.mods-bl-wwww` | look at: Swaps in BL manga cover art |
| Red Scarf Recolors | `yunachiu.ouo` | equip Cheery Winter Scarf #116346 (any race) |
| Purple Eyes & Brows (Elin Face 11, Adornment | `yunachiu.purple-eyes-brows` | character creator: elin any, pick face 11 |
| Black Swimsuit (Elin) | `yunachiu.qaq` | equip Radiant Beach Beauty (Amani Female) #179759 (aman female) |
| Polka Dot Heart Wand | `yunachiu.qq` | look at: Adds polka dots to the heart wand weapon |
| Shining Blue Starlight Wings | `yunachiu.qq-i-make-a` | equip Golden Gliders #141450 (any race) |
| Purple Snowflake Hanbok (Elin) | `yunachiu.qqqq-i` | equip Ruby Snow Blossom Hanbok (Amani Female) #153378 (aman female) |
| Devil Wings to Dragon Wings | `yupi.devil-wings-to-dragon` | equip Little Devil's Wings #131236 (any race) |
| Amber Queen Elin Face 9 Adornment 3 | `zephyia.amber-queen-face-8-adornment` | character creator: elin any, pick face 9 |
| Contrast Aman Face 6 Adornment 3 | `zynnobia.aman-face-6-adornment-3` | character creator: aman female, pick face 6 |
| Red Ribbon Double Hair Buns | `zynnobia.red-ribbon-double-hair-buns-works-for` | equip Double Bobble Hairband #116124 (any race) |
| Santa Suit Recolor For Aman Female | `zynnobia.santa-suit-recolor-for-aman-female` | equip Human Male Santa Suit #131054 (human male) | ## Held back -- rebuild in progress (1) | Mod | id | What to do |
|---|---|---|
| Arthurian Knight Scepter (Mystic) | `recolor.for-arthurian-knight-scepter-for-mystic` | equip Discontinued Template #4065 (any race) | ## Verified (50) | Mod | id | What to do |
|---|---|---|
| Hank Hill Block Icon | `aioshe.hank-hill-is-impressed-by-your-ability-to` | in game, look at the shield art on the Defense Success popup |
| Keaton's Kitsune Mask | `aioshe.kitsune-mask-converted-to-look-like` | equip Kitsune Mask #115387 (any race) |
| Loading Bar Recolor | `aioshe.loading-bar-recolor` | in game, look at the loading progress bar |
| Golden Tommy Gun | `aioshe.need-that-golden-tommy-gun-to-mow-down` | equip [TBU] #131839 (any race) |
| Colorful Sparky Recolor | `aioshe.sparky-got-a-spiffy-new-makeover` | equip Riding Skill: Sparky #90100 (any race) |
| Recolored Steam-Powered Weapons | `aioshe.steam-powered-recolor` | equip Tool & Die #177983 (any race) |
| Fan Costume Recolor | `anastasik.fan-costume-recolor` | equip Cheerleader Outfit (Castanic Female) #151673 (castanic female) |
| Qipao Recolor | `anastasik.qipao-recolor` | equip Elegant Cheongsam (Amani Female) #150232 (aman female) |
| GigaChad Block | `artexlib.block-gigachad` | in game, look at the Defense Success (block) popup |
| Gray College Backpack | `artexlib.gray-college-backpack` | equip Gray College Backpack #152411 (any race) |
| White Valkyrie Helmet | `artexlib.white-valkyrie-helmet` | equip [Promotion] Eagle Warrior Helm #149374 (any race) |
| Peach Blossom Elin Face 1 Adornment 4 | `atliasatlas.peach-blossom` | character creator: elin any, pick face 1 |
| Starlight (Elin Face 4) | `atliasatlas.starlight-face` | character creator: elin any, pick face 4 |
| Cat & Peach Block | `aunu.block-cat-peach` | in game, look at the Defense Success (block) popup |
| Pink Loading Progress | `catannadev.pink-loading-progress` | in game, look at the loading progress bar |
| Shinra Meter (Classic+) | `classicplus.shinra` | in game, look at Shinra combat meter (external application, replaces nothing in the client) |
| TCC (Classic+) | `classicplus.tcc` | in game, look at TCC combat UI (external application, replaces nothing in the client) |
| Transparent Digits 50% | `cosy.digits-50-transp` | in game, look at the in-game text, which uses these fonts everywhere |
| RGB Scarf | `htmslf.rgb-scarf` | equip Snowy Winter Scarf #150713 (any race) |
| Green Crosshair | `justcrazy.green-crosshair` | in game, look at the aiming crosshair (and 1 more) |
| GFTime Dance | `katmods.gftime-dance` | in game, look at the /dance emote animation (Elin) |
| Reaper and Ninja Animations Swapped | `katmods.reaper-to-ninja` | in game, look at the Reaper and Ninja stance animations on Elin (66 sequences) |
| Pastel Pink Fishing Rod + Float | `kawaakari.pastel-fishing-rod-pink` | equip Old Fishing Rod #206700 (any race) |
| Hello Kitty Maid Dress | `litterboxchan.not-gonna-stop-until-every` | equip Hello Kitty Elin Dress #185412 (elin female) |
| Dark Blue Batwing Cape | `littleshistar.dark-blue-batwing-cape` | equip Dragonclaw Cape #266076 (any race) |
| No Ears Governess Frills | `littleshistar.no-ears-governess-frills` | equip Black Headband with Ears #115741 (any race) |
| Thinkblob Mount | `lukas.thinkblob-mount` | equip Skill Manual: Darkwynder #280231 (any race) |
| Glamour High Elf Face 2 Adornment 1 | `moddymcmodface.glamour-high-elf-female-face` | character creator: highelf female, pick face 1 |
| Brownee Elin Face 5 Adornment 2 | `mtforum.brownee` | character creator: elin any, pick face 5 |
| Bunny v2 Elin Face 11 Adornment 5 | `mtforum.bunny-v2` | character creator: elin any, pick face 11 |
| Crystal BBrwon High Elf F Face 1 Adornment 1 | `mtforum.crystal-bbrwon` | character creator: highelf female, pick face 1 |
| PadamPadam Castanic F Face 1 Adornment 3 | `mtforum.padampadam-castanicf` | character creator: castanic female, pick face 1 |
| SterlingSilver Castanic F Face 1 Adornment 1 | `mtforum.sterlingsilver-castanicf` | character creator: castanic female, pick face 1 |
| Strawberry Melody 2.5 Elin Face 11 Adornment | `mtforum.strawberry-melody-2-5` | character creator: elin any, pick face 11 |
| Turquoise Elin Face 12 Adornment 2 | `mtforum.turquoise` | character creator: elin any, pick face 12 |
| Kitty Socks | `norukjerky.kitty-socks` | equip School Uniform A (Elin) #131233 (elin female) |
| Sailor Moon HP Bar | `novatera.sailor-moon-hp` | in game, look at the character window (and 2 more) |
| Sleepy Castanic Running Togs | `pantypon.castanic-sleepy-running-togs` | equip Blue Team Captain Uniform #60651 (castanic female) |
| Elin Rose Gold Raincoat | `pantypon.elin-rose-gold-raincoat` | equip Elin Raincoat #154850 (elin female) |
| Pink Hearts Crosshair | `pantypon.pink-hearts-crosshair` | in game, look at the aiming crosshair (and 1 more) |
| White Castanica Demon | `pantypon.white-castanica-demon` | equip Heavy Metal Star (Human Female) #152324 (human female) |
| BnS Plate Armor (Elin) | `yupi.bns-plate-armor` | equip Resolute Plate Armor (Elin) #254708 (elin female) |
| BnS Plate Armor Evil's God (Elin) | `yupi.bns-plate-evil-god` | equip Evil God's Armor (Elin) #270943 (elin female) |
| BnS Plate Armor Heavy Metal Star (Elin) | `yupi.bns-plate-heavy-metal` | equip Heavy Metal Star (Elin) #152396 (elin female) |
| BnS Plate Armor Woden & Thunor (Elin) | `yupi.bns-plate-woden-thunor` | equip Thunor’s Armor (Elin) #271132 (elin female) |
| Elin Matching Ears & Tails | `yupi.elin-matching-ears-tails` | character creator: elin any, pick hair 1, 13 |
| Bewitching Elin Genshin Impact Mona | `yupi.genshin-mona` | equip Elin Devilicious Costume #81159 (elin female) | ## Not yet installable -- being fixed (157) Every entry here names why it cannot ship. Nothing is abandoned;
each line is a fix in the queue, worked by class. | Mod | id | Why it is held |
|---|---|---|
| Dyeable 2017 Maid Dress (Elin) | `2017.maid-dress-mod-dyeable-version` | The stored file is byte-identical to the Black 2017 maid dress entry, so one of the two carries the wrong payload -- the same intake mix-up that hit H |
| Black 2017 Maid Dress (Elin) | `2017maidfix.elin` | The stored file is byte-identical to the Dyeable 2017 maid dress entry, so one of the two carries the wrong payload -- the same intake mix-up that hit |
| Kitty Club Black Paw Pads (Elin) | `a.lysstaise-and-if-you-doubt-me-for-a` | Tester 2026-07-31: does not apply in game |
| Red & Black Triple T Uniform | `a.lyssu-mod-requested-by-iwakiii-this-mod` | Tester 2026-07-31: does not apply in game |
| Lyssu Costume Retexture | `a.lyssu-this-is-probably-my-very-first-official` | Tester: "no clue what costume this is, no ID" -- correct, and the entry could not say |
| Character Select Music Replacement | `aioshe.audio-may-scramble-or-go-into-a-jumbled` | Tester 2026-07-31: does not apply in game |
| Totoro King Blob | `aioshe.king-blob-likes-to-cosplay-as-totoro` | Tester 2026-07-31: does not apply |
| King Blob Repaint | `aioshe.king-blob-seems-very-excited-to-tell-you` | Tester 2026-07-31: does not apply |
| VIP Shop Window Recolor | `aioshe.simple-vip-shop-window-recolor-make-your` | Nothing to recolour on this server: the VIP shop window is disabled, so the mod cannot show |
| Ice Grip Staff Glow | `amynet.iceglow-staff` | Partially migrated to the streamed layer -- some textures apply in game now, others still show vanilla |
| Steam Weapons | `amynet.steam-weapons` | Partially migrated to the streamed layer -- some textures apply in game now, others still show vanilla |
| Academy Newcomer Gradient | `anastasik.academy-newcomer-gradient` | Tester 2026-07-31: no change on the Blue-brown uniform |
| Brawler Chad Block Animation (BrawlerCha | `artexlib.brawler-chad-block-animation` | Route found, one blocker left |
| Pixel Strawberry Block | `aunu.block-strawberry` | Duplicate-payload defect: this entry ships bytes identical to "Cute Popup Pack — Block, Brawler & Evasion" by another author, so one of them cannot be |
| Academy Newcomer, Author's Color | `banana.academy-newcomer-authors-color` | Tester 2026-07-31: no change on the Blue-brown uniform |
| Maid Dress Recolor (Elin) | `banana.event19a-recolor` | Tester 2026-07-31: no change on #178997 (Black Maid's Dress) |
| Target Window, 50% Transparent | `cosy.targetinfo-50-transparent` | Pulled after in-game testing on 2026-07-31: the loose whole-package route this build ships on does not change what the client renders (target window, |
| UI Remover: Quest Tracker | `deathdefying.ui-remover-quest-tracker` | Interface window mod, re-listed after being pulled |
| UI Remover: TERA Rewards | `deathdefying.ui-remover-tera-rewards` | Interface window mod, re-listed after being pulled |
| Happy Trail Castanic Male Rapidos | `deathwrack.happy-trail-requested-by-anon-truly` | Re-harvested from its own source post on 2026-07-31 and the fresh payload STILL reads vanilla on every comparable texture -- the original release itse |
| Snake Eyes Cold and Arctic Bomber | `deathwrack.snake-eyes-for-coldarctic-bomber` | Duplicate-payload defect: this entry ships bytes identical to "Rockstar Bomber Jacket Swap" by another author, so one of them cannot be delivering its |
| Summer Breeze Crop Top Swimsuit | `deathwrack.summer-breeze-for-regular-and` | Re-harvested from its own source post on 2026-07-31 and the fresh payload STILL reads vanilla on every comparable texture -- the original release itse |
| Elin Matching Hair & Tail (Updated) | `elin.matching-hairtail-mod` | Duplicate-payload defect: this entry ships bytes identical to "Elin Face + Matching Ears & Tail" by another author, so one of them cannot be deliverin |
| Pink 2017 Maid Dress | `elinsailorsuit.2017-maid-dress-pink-mod-changes` | Duplicate-payload defect: this entry shares its exact payload with Elin, Maid Dress Mod Dyeable Version — it cannot deliver its own distinct content |
| Mount Mod | `flying.mount-mod` | The payload does not match this entry |
| BadGUI Loader (Update Notification) | `foglio1024.badgui-loader` | SUPERVISED FIRST TEST -- the first movie-route mod offered |
| Modern UI: Community Window | `foglio1024.modern-ui-community-window` | SUPERVISED FIRST TEST -- the first movie-route mod offered |
| Modern UI: EP Window | `foglio1024.modern-ui-ep-window` | SUPERVISED FIRST TEST -- the first movie-route mod offered |
| Modern UI: Equipment Combine | `foglio1024.modern-ui-equipment-combine` | Root cause found 2026-08-01, twice over |
| Modern UI: Equipment Upgrade | `foglio1024.modern-ui-equipment-upgrade` | SUPERVISED FIRST TEST -- the first movie-route mod offered |
| Modern UI: Guild Window | `foglio1024.modern-ui-guild-window` | SUPERVISED FIRST TEST -- the first movie-route mod offered |
| Modern UI: Interaction Popup | `foglio1024.modern-ui-interaction-popup` | Root cause found 2026-08-01, twice over |
| Modern UI: Jewels Fix (Inventory) | `foglio1024.modern-ui-jewels-fix-inventory` | Root cause found 2026-08-01, twice over |
| Modern UI: Jewels Fix (PaperDoll) | `foglio1024.modern-ui-jewels-fix-paperdoll` | Root cause found 2026-08-01, twice over |
| Modern UI: Minimap | `foglio1024.modern-ui-minimap` | SUPERVISED FIRST TEST -- the first movie-route mod offered |
| Modern UI: Parcel Post Log | `foglio1024.modern-ui-parcel-post-log` | SUPERVISED FIRST TEST -- the first movie-route mod offered |
| Modern UI: Production Create Popup | `foglio1024.modern-ui-production-create` | SUPERVISED FIRST TEST -- the first movie-route mod offered |
| Modern UI: Production List | `foglio1024.modern-ui-production-list` | Root cause found 2026-08-01, twice over |
| Modern UI: Servant Storage Window | `foglio1024.modern-ui-servant-storage` | SUPERVISED FIRST TEST -- the first movie-route mod offered |
| Modern UI: Store Window | `foglio1024.modern-ui-store-window` | SUPERVISED FIRST TEST -- the first movie-route mod offered |
| Modern UI: System Option | `foglio1024.modern-ui-system-option` | SUPERVISED FIRST TEST -- the first movie-route mod offered |
| Modern UI: Trade Popup | `foglio1024.modern-ui-trade-popup` | Root cause found 2026-08-01, twice over |
| Restyle: Community Window | `foglio1024.restyle-community-window` | The author's real art IS available and the payload does not carry it -- located 2026-08-01 at github.com/foglio1024/tera-restyle, which holds 455 .dds |
| Restyle: EP Window | `foglio1024.restyle-ep-window` | The author's real art IS available and the payload does not carry it -- located 2026-08-01 at github.com/foglio1024/tera-restyle, which holds 455 .dds |
| Restyle: Equipment Combine | `foglio1024.restyle-equipment-combine` | The author's real art IS available and the payload does not carry it -- located 2026-08-01 at github.com/foglio1024/tera-restyle, which holds 455 .dds |
| Restyle: Equipment Upgrade | `foglio1024.restyle-equipment-upgrade` | Expected not to work |
| Restyle: Guild Window | `foglio1024.restyle-guild-window` | The author's real art IS available and the payload does not carry it -- located 2026-08-01 at github.com/foglio1024/tera-restyle, which holds 455 .dds |
| Restyle: Interaction Popup | `foglio1024.restyle-interaction-popup` | The author's real art IS available and the payload does not carry it -- located 2026-08-01 at github.com/foglio1024/tera-restyle, which holds 455 .dds |
| Restyle: Inventory Window | `foglio1024.restyle-inventory` | The author's real art IS available and the payload does not carry it -- located 2026-08-01 at github.com/foglio1024/tera-restyle, which holds 455 .dds |
| Restyle: MiniMap | `foglio1024.restyle-minimap` | The author's real art IS available and the payload does not carry it -- located 2026-08-01 at github.com/foglio1024/tera-restyle, which holds 455 .dds |
| Restyle: PaperDoll (x64 port) | `foglio1024.restyle-paperdoll` | Interface window mod, re-listed after being pulled |
| Restyle: ParcelPostLog | `foglio1024.restyle-parcelpost` | The author's real art IS available and the payload does not carry it -- located 2026-08-01 at github.com/foglio1024/tera-restyle, which holds 455 .dds |
| Restyle: Production Create Popup | `foglio1024.restyle-production-create` | Expected not to work |
| Restyle: Production List | `foglio1024.restyle-production-list` | The author's real art IS available and the payload does not carry it -- located 2026-08-01 at github.com/foglio1024/tera-restyle, which holds 455 .dds |
| Restyle: Quickslot Bar | `foglio1024.restyle-quickslot` | Expected not to work |
| Restyle: Servant Storage | `foglio1024.restyle-servant-storage` | Interface window mod, re-listed after being pulled |
| Restyle: Skill Window | `foglio1024.restyle-skill-window` | The author's real art IS available and the payload does not carry it -- located 2026-08-01 at github.com/foglio1024/tera-restyle, which holds 455 .dds |
| Restyle: Store Window | `foglio1024.restyle-store-window` | The author's real art IS available and the payload does not carry it -- located 2026-08-01 at github.com/foglio1024/tera-restyle, which holds 455 .dds |
| Restyle: System Option | `foglio1024.restyle-system-option` | The author's real art IS available and the payload does not carry it -- located 2026-08-01 at github.com/foglio1024/tera-restyle, which holds 455 .dds |
| Restyle: Trade Popup | `foglio1024.restyle-trade-popup` | The author's real art IS available and the payload does not carry it -- located 2026-08-01 at github.com/foglio1024/tera-restyle, which holds 455 .dds |
| Restyle: Warehouse | `foglio1024.restyle-warehouse` | The author's real art IS available and the payload does not carry it -- located 2026-08-01 at github.com/foglio1024/tera-restyle, which holds 455 .dds |
| Foglio's Chat2 (Patch 75) | `foglio1024.s1ui-chat2-p75` | SUPERVISED FIRST TEST -- the first movie-route mod offered |
| Toolbox Client Mod: GageBar TopScreen | `foglio1024.toolbox-gagebar-topscreen` | SUPERVISED FIRST TEST -- the first movie-route mod offered |
| UI Remover: Boss Window | `foglio1024.ui-remover-bosswindow` | The author's real art IS available and the payload does not carry it -- located 2026-08-01 at github.com/foglio1024/tera-restyle, which holds 455 .dds |
| UI Remover: Buffs Window | `foglio1024.ui-remover-buffs` | Expected not to work |
| UI Remover: Character Window | `foglio1024.ui-remover-character` | Interface window mod, re-listed after being pulled |
| UI Remover: Flight Gauge | `foglio1024.ui-remover-flight-gauge` | Expected not to work |
| UI Remover: LFG Board | `foglio1024.ui-remover-lfg-board` | The author's real art IS available and the payload does not carry it -- located 2026-08-01 at github.com/foglio1024/tera-restyle, which holds 455 .dds |
| UI Remover: LFG Member Info | `foglio1024.ui-remover-lfg-member` | The author's real art IS available and the payload does not carry it -- located 2026-08-01 at github.com/foglio1024/tera-restyle, which holds 455 .dds |
| UI Remover: Party Window | `foglio1024.ui-remover-party-window` | The author's real art IS available and the payload does not carry it -- located 2026-08-01 at github.com/foglio1024/tera-restyle, which holds 455 .dds |
| UI Remover: Raid Info | `foglio1024.ui-remover-raid-window` | The author's real art IS available and the payload does not carry it -- located 2026-08-01 at github.com/foglio1024/tera-restyle, which holds 455 .dds |
| UI Remover: Target Info | `foglio1024.ui-remover-targetinfo` | The author's real art IS available and the payload does not carry it -- located 2026-08-01 at github.com/foglio1024/tera-restyle, which holds 455 .dds |
| Rockstar Bomber Jacket Swap | `fyregem.rockstar-hello-my-lovelies-today-i` | Re-harvested successfully, but no composite owns any of its 22 textures -- this one is a loose-file mod, and the loose route is confirmed dead for the |
| Cute Popup Pack — Block, Brawler & Evasi | `honestlylovingbunny.ui-perfect-block-icon-for` | Duplicate-payload defect: this entry ships bytes identical to "Pixel Strawberry Block" by another author, so one of them cannot be delivering its own |
| Elin Full-Body Tattoos | `katmods.here-is-the-mod-some-of-you-asking-for` | Duplicate-payload defect: this entry ships bytes identical to "Elin Better Skin" by another author, so one of them cannot be delivering its own art |
| Elleon Mooncloak Weapon Models | `kourinn.elleon-moon-weapons` | Pulled after in-game testing on 2026-07-31: the loose whole-package route this build ships on does not change what the client renders (target window, |
| Elleon Shadowlaced Weapon Models | `kourinn.elleon-sun-weapons` | Pulled after in-game testing on 2026-07-31: the loose whole-package route this build ships on does not change what the client renders (target window, |
| 2014 Swimsuits Scar Restore | `lewdshi.scar-restore-2014-swimsuits-long` | Re-harvested from its own source post on 2026-07-31 and the fresh payload STILL reads vanilla on every comparable texture -- the original release itse |
| Pusheen Snowsuit | `litterboxchan.pusheen-snowsuit` | Tester: the scarf part shows but the snowsuit itself does not -- reported as not working on the items tried (Elin) |
| Sanrio Gym Uniforms | `litterboxchan.s-a-n-r-i-changes-all-the` | Duplicate-payload defect: this entry shares its exact payload with Floral Tee And Jean Shorts Outfit For, Sleepy C |
| Soft Pink Llama | `litterboxchan.soft-pink-llama-changes-the` | Duplicate-payload defect: this entry ships bytes identical to "Llama Mount Recolor" by another author, so one of them cannot be delivering its own art |
| Elin Face + Matching Ears & Tail | `mayukari.new-this-second-link-is-the-same-mod` | Duplicate-payload defect: this entry ships bytes identical to "Elin Matching Hair & Tail (Updated)" by another author, so one of them cannot be delive |
| Atlas: Clean Onscreen Messages | `merusira.atlas-clean-onscreen-messages` | Does not work yet: this window is driven by a movie file, and neither replacing the loose package nor redirecting it takes effect — the whole movie cl |
| Reaper Scythes Block Icon (MoonShi) | `moonshi.lancer-block-reaper-scythes` | Re-listed after being pulled for a boot crash |
| Chat2 (neowutran) | `neowutran.s1ui-chat2` | The published payload carries vanilla art |
| Japanese Voice Pack (Players + NPCs) | `novatera.jp-voice-pack` | ROUTE SOLVED 2026-08-01, and it needs no download at all |
| Panda Ice Cream Bar Variants | `nyankouu.panda-ice-cream-bar-mod-blushy` | Duplicate-payload defect: this entry shares its exact payload with No Panda Ice Cream Staff, Soo I Made My Very First Mod — it cannot deliver its own |
| Pokemon Go Team Outfits | `nyankouu.pok-mon-go-blue-dogs-mod-works-on` | Duplicate-payload defect: this entry shares its exact payload with Pastel Varsity Turns The — it cannot deliver its own distinct content |
| FPS Pack: PostProcess | `owyn.fps-pack-postprocess` | Duplicate-payload defect: this entry ships bytes identical to "PostProcess — gunner-effect cleanup" by another author, so one of them cannot be delive |
| Castanic Female Pink Horns Hair | `pantypon.castanic-female-pink-horns-hair` | Cannot work as built: this build carries no deploy_strategy, so it never routes anywhere, and its ~8 KB payload is only the costume's specular/custom |
| Elin Better Skin | `pantypon.elin-better-skin-this` | Duplicate-payload defect: this entry ships bytes identical to "Elin Full-Body Tattoos" by another author, so one of them cannot be delivering its own |
| Elin Dyeable Raincoat Match | `pantypon.elin-dyeable-raincoat-match` | The raincoat dye texture is shared across 29 costume containers and the rebuild refuses to guess which of them this mod means |
| Elin Matching Ears and Tails | `pantypon.elin-matching-ears-and-tails` | Cannot work as built: this build carries no deploy_strategy, so it never routes anywhere, and its ~8 KB payload is only the costume's specular/custom |
| Elin Whiter Dyeable Ice Cream Social | `pantypon.elin-whiter-ice-cream-social` | Duplicate-payload defect: this entry ships bytes identical to "Ice Cream Social - White Pantyhose" by another author, so one of them cannot be deliver |
| Elin Whiter Dyeable Raincoat Accents | `pantypon.elin-whiter-raincoat-accents` | Same shared-texture situation as the dyeable raincoat match: the accent texture appears in 29 containers and the rebuild refuses to guess |
| Elin Fancy Nails | `pantypon.fancy-nails-all-this-mod-does-is` | Install fails its file check: the parts share filenames across different builds, and the rebuild came back partially verified because the nails live i |
| Hana Reward Tier | `pantypon.hana-reward-tier` | Expected not to work |
| Housekeeper Dyeable Bow and Soles | `pantypon.housekeeper-dyeable-bow-and-soles` | Install fails its file check on the dye material |
| Ice Cream Social - White Pantyhose | `pantypon.ice-cream-white-pantyhose` | Duplicate-payload defect: this entry ships bytes identical to "Elin Whiter Dyeable Ice Cream Social" by another author, so one of them cannot be deliv |
| Mystic Pale Pink Princess Wand | `pantypon.mystic-pale-pink-princess-wand` | Cannot work as built: this build carries no deploy_strategy, so it never routes anywhere, and its ~8 KB payload is only the costume's specular/custom |
| Pink Boss HP Bar | `pantypon.pink-boss-hp-bar` | Expected not to work |
| Pink Chat Window | `pantypon.pink-chat-window` | Expected not to work |
| Pink Controller UI | `pantypon.pink-controller-ui` | Expected not to work |
| Pink Exp Bar (S1UI_ExpBar) | `pantypon.pink-exp-bar` | Interface window mod, re-listed after being pulled |
| Pink Fishing Float | `pantypon.pink-fishing-float` | This build carries no deploy_strategy, so the launcher falls back to its default composite path and the mod may install without taking effect |
| Pink Fishing Rod | `pantypon.pink-fishing-rod` | This build carries no deploy_strategy, so the launcher falls back to its default composite path and the mod may install without taking effect |
| Pink Heart HP MP (S1UI_CharacterWindow) | `pantypon.pink-heart-hp-mp` | Interface window mod, re-listed after being pulled |
| Pink Main Menu | `pantypon.pink-menu` | Expected not to work |
| Pink Party Member HP Bar | `pantypon.pink-party-member-hp-bar` | Expected not to work |
| Pure White Pixie | `pantypon.pure-white-pixierequested-by-vildir` | Duplicate-payload defect: this entry ships bytes identical to "White Pixie" by another author, so one of them cannot be delivering its own art |
| Simplicity 2.0 Pastel | `pantypon.simplicity-2-pastel` | Duplicate-payload defect: this entry ships bytes identical to "Simplicity UI" by another author, so one of them cannot be delivering its own art |
| Simplicity UI | `pantypon.simplicity-ui` | Duplicate-payload defect: this entry ships bytes identical to "Simplicity 2.0 Pastel" by another author, so one of them cannot be delivering its own a |
| Simplified Pastel UI (S1UI_CharacterWind | `pantypon.simplified-pastel-ui` | Interface window mod, re-listed after being pulled |
| Sorcerer Gloomy Bear Patches (PC_Weapons | `pantypon.sorcerer-gloomy-bear-patches` | Re-listed after being pulled for a client crash |
| Party Window No Background | `pantypon.ui-party-window-no-background-20` | Partially rebuilt 2026-08-01: 2 package(s) now carry this mod's art on the v100 symbols that survived the recompile |
| Pink Pastel HP/MP Bars | `pantypon.ui-pink-pastel-ui-makes-the-hpmp-bars` | Partially rebuilt 2026-08-01: 2 package(s) now carry this mod's art on the v100 symbols that survived the recompile |
| Pantypon Sweets UI | `pantypon.ui-sweets-ui-30` | Partially rebuilt 2026-08-01: 2 package(s) now carry this mod's art on the v100 symbols that survived the recompile |
| White Pixie | `pantypon.white-pixie` | Install fails its file check, and the rebuild triage reads the payload as near-vanilla -- a whiter-white edit the comparison cannot separate from enco |
| Whiter Dyeable Jeans and Jacket | `pantypon.whiter-jeans-and-jacket` | Install fails its file check on the dye material |
| Event Staff 4 Weapon Skin | `princessbuttpunch.soo-i-made-my-very-first-mod` | Duplicate-payload defect: this entry shares its exact payload with No Panda Ice Cream Staff, Panda Ice Cream Bar Mod Blushy — it cannot deliver its ow |
| Rainbow Monster HP Gauge | `psina.gage-monster-hp` | CRASHES THE CLIENT AT LAUNCH — do not enable |
| PostProcess — gunner-effect cleanup | `psina.postprocess` | Effect mod, re-listed after being pulled |
| Flowery Tattoos | `puppetplayers.flowery-tattoos-for` | Install fails its file check: shared filenames across different builds |
| Black And White Sakura Staff | `readeyedghost.black-and-white-sakura-staff` | Duplicate-payload defect: this entry ships bytes identical to "Blood Petals Rare Weapon Skin" by another author, so one of them cannot be delivering i |
| Character window — cleaned | `saltymonkey.characterwindow-clean` | Interface window mod, re-listed after being pulled |
| Extended Boss HP Gauge | `saltymonkey.gageboss-extended` | The published payload carries vanilla art |
| Instant Join TBA Mode | `saltymonkey.instant-join-tba-mode` | Expected not to work |
| Centered Clean Message Window | `saltymonkey.message-centered` | Expected not to work |
| Overlay Map Fix (Patch 103) | `saltymonkey.overlaymap-fixed` | The published payload carries vanilla art |
| Taorelia Restyle: Community | `taorelia.restyle-community` | SUPERVISED FIRST TEST -- the first movie-route mod offered |
| Taorelia Restyle: Guild | `taorelia.restyle-guild` | Root cause found 2026-08-01, twice over |
| Taorelia Restyle: Interaction Popup | `taorelia.restyle-interaction-popup` | Root cause found 2026-08-01, twice over |
| Taorelia Restyle: Inventory | `taorelia.restyle-inventory` | SUPERVISED FIRST TEST -- the first movie-route mod offered |
| Taorelia Restyle: PaperDoll | `taorelia.restyle-paperdoll` | SUPERVISED FIRST TEST -- the first movie-route mod offered |
| Taorelia Restyle: Production Create | `taorelia.restyle-production-create` | SUPERVISED FIRST TEST -- the first movie-route mod offered |
| Taorelia Restyle: Warehouse | `taorelia.restyle-warehouse` | SUPERVISED FIRST TEST -- the first movie-route mod offered |
| Bunny Coco | `taylorswiftmodding.bunny-coco` | This build carries no deploy_strategy, so the launcher falls back to its default composite path and the mod may install without taking effect |
| Hanbok Bubblegum Princess | `taylorswiftmodding.hanbok-bubblegum-princess` | The rebuild found no unambiguous home for its textures and refused to guess |
| Party Window Raid Info | `teralove.partywindowraidinfo` | The published payload carries vanilla art |
| Target Info Restyle | `teralove.targetinfo` | The published payload carries vanilla art |
| Avenger Minion: Witch | `unknown.avenger-witch` | Composite route now half-works and the crash cause is gone |
| Destroyer Minion: Elion | `unknown.destroyer-elion` | Composite route now half-works and the crash cause is gone |
| Destroyer Minion Reskin | `unknown.destroyer-nukes` | Composite route now half-works and the crash cause is gone |
| Destroyer Minion: Zolin | `unknown.destroyer-zolin` | Composite route now half-works and the crash cause is gone |
| Guardian Minion: Argo Wolf | `unknown.guardian-argo-wolf` | Composite route now half-works and the crash cause is gone |
| Guardian Minion: Elin | `unknown.guardian-elin` | Composite route now half-works and the crash cause is gone |
| Guardian Minion: Korean Original | `unknown.guardian-kr-original` | Composite route now half-works and the crash cause is gone |
| Guardian Minion: New Year | `unknown.guardian-new-year` | Composite route now half-works and the crash cause is gone |
| Guardian Minion: Sandra Thrall | `unknown.guardian-sandra-thrall` | Composite route now half-works and the crash cause is gone |
| Healer Minion: Blue Girl | `unknown.healer-blue-girl` | Composite route now half-works and the crash cause is gone |
| Healer Minion Reskin | `unknown.healer-khil` | Composite route now half-works and the crash cause is gone |
| Special Sit for Standard Sit | `unknown.special-sit-swap` | Route proven on the GFTime dance 2026-08-01: the payload's AnimSets transplant cleanly into the composite objects the client resolves, so the loose ro |
| Blood Petals Rare Weapon Skin | `veinlace.blood-petals-recolors-silver-into` | Install fails its file check on two weapon materials whose filenames were shared across builds |
| Royal Weapon Flower Recolors | `yunachiu.dds` | Install fails its file check on one rod material |
| Devil Wings to Darkan Wings | `yupi.devil-wings-to-darkan` | Mesh route is solved and its four siblings are rebuilt on it, but this entry's original payload is not in the local cache and the catalog's copy is th |
| Floral Tee & Jean Shorts | `zynnobia.floral-tee-and-jean-shorts-outfit-for` | Duplicate-payload defect: this entry shares its exact payload with S A N R I Changes All, Sleepy Castanic Running |
