# New Features

## Maiden Hint for Theives Town Attic

In crossed dungeon mode, if you bring the maiden to the boss room when the attic is not bombed (and thus no light in the room), she mentions the dungeon where you can find the cracked floor.

## Shuffle Links House

Links house can now be shuffled in different ER settings. It will be limited to the Light World (or Dark World in inverted) if Crossed or Insanity shuffle is not one. It it also limited if door shuffle settings allow the Sanctuary to be in the dark world. (This is prevent having no Light World spawn points in Open modes) This setting is ignored by standard mode. THe CLI parameter is --shufflelinks

## OWG Glitch Logic

Thanks to qadan, cheuer, & compiling

## Pseudo Boots

Thanks to Bonta. You can now start with pseudo boots that let you move fast, but have no other logical uses (bonking open things, hovering, etc)

## Pendant/Crystal Indicator

For accessibility, you now get a C or P indicator to the left of the magic bar on the HUD when instead a Crystal or Pendant. Requires ownership of the map of that dungeon for display. Thanks to kan. 

# Bug Fixes and Notes.

* 0.4.0.12
	* ER Inverted fix for HC Ledge, and Aga Tower choosing Links House incorrectly
	* Credits again - hopefully for good
	* Incorporated music fixes for now (may revisit later)
	* Secure random re-incorporated
* 0.4.0.11
	* Some minor base rom fixes
	* Improved distribution of bombable/dashable doors
* 0.4.0.10
	* Renamed to pseudoboots
	* Some release note updates
* 0.4.0.9
	* Fixes for stats and P/C indicator (thanks Kara)
	* Swamp lobby fixes (thanks Catobat)
	* Fix for --hints flag on CLI
* 0.4.0.8
	* Ganon jokes added for when silvers aren't available
	* Some text updated (Blind jokes, uncle text)
	* Fixed some enemizer Mystery settings
	* Added a setting that's random enemy shuffle without Unkillable Thieves possible
	* Fixed shop spoiler when money balancing/multiworld balancing
	* Fixed a problem with insanity
	* Fixed an issue with the credit stats specific to DR (e.g. collection rate total)
	* More helpful error message when bps is missing?
	* Minor generation issues involving enemizer and the link sprite
	* Baserom updates (from Bonta, kan, qwertymodo, ardnaxelark)
		* Boss icon on dungeon map (if you have a compass)
		* Progressive bow sprite replacement
		* Quickswap - consecutive special swaps
		* Bonk Counter
		* One mind
		* MSU fix
		* Chest turn tracking (not yet in credits)
		* Damaged and magic stats in credits (gt bk removed)
		* Fix for infinite bombs
		* Pseudo boots option
		* Always allowed medallions for swordless (no option yet)
* 0.4.0.7
	* Reduce flashing option added
	* Sprite author credit added
	* Ranged Crystal switch rules tweaked
	* Baserom update: includes Credits Speedup, reduced flashing option, msu resume (but turned off by default)
	* Create link sprite's zspr from local ROM and no longer attempts to download it from website
	* Some minor bug fixes
* 0.4.0.6
	* Hints now default to off
	* The maiden gives you a hint to the attic if you bring her to the unlit boss room
	* Beemizer support and fix for shopsanity
	* Capacity upgrades removed in hard/expert item difficulties
	* Swamp Hub added to lobby shuffle with ugly cave entrance.
	* TR Lava Escape added to lobby shuffle.
	* Hyrule Main Lobby and Sanctuary can now have a more visible outside exit, and rugs modified to be fully clipped. 
* 0.4.0.5
	* Insanity - less restrictions on exiting (all modes)
	* Fix for simple bosses shuffle
	* Fix for boss shuffle from Mystery.py
	* Minor msu fade out bug (thanks codemann8)
	* Other bug fixes (thanks Catobat)
* 0.4.0.4
	* Added --shufflelinks option
	* Moved spawning as a bunny indoors to experimental
	* Baserom bug fixes	
* 0.4.0.3
	* Fixed a bug where Sanctuary could be chosen as a lobby for a DW dungeon in non-crossed ER modes
* 0.4.0.2
	* Fixed a bug where Defeat Ganon is not possible
	* Fixed the item counter total
	* Fixed the bunny state when starting out in Sanc in a dark world dungeon
* 0.4.0.1
	* Moved stonewall pre-opening to not happen in experimental
	* Updated baserom
		* Boss RNG perseved between files
		* Vanilla prize pack fix
		* Starting equipment fix
		* Post-Aga world state option
		* Code optimzation
		* Bottle quickswap via double shoulder
		* Credits update
		* Accessibility option
		* Sewer map/compass fix
	* Fixed a standard bug where the exits to the ledge would be unavailable if the pyramid was pre-opened
	* DR ASM optimization
	* Removed Archery Game from Take-Any caves in inverted
	* Fixed a problem with new YAML parser
* 0.4.0.0
	* Mystery yaml parser updated to a package maintained version (Thanks StructuralMike)
	* Bomb-logic and extend crystal switch logic (Thanks StructuralMike)
	* Fixed logic for moved locations in playthrough (Thanks compiling)
	* OWG Glitch logic added

# Known Issues

* Shopsanity Issues
	* Hints for items in shops can be misleading (ER)
	* Forfeit in Multiworld not granting all shop items
* Potential keylocks in multi-entrance dungeons
* Incorrect vanilla key logic for Mire

## Other Notes

### Triforce Hunt Options

Thanks to deathFouton!

--triforce_pool and --triforce_goal added to the CLI. 

Also, to the Mystery.py he added the following options:
* triforce_goal_min
* triforce_goal_max
* triforce_pool_min
* triforce_pool_max
* triforce_min_difference

See the example yaml file for demonstrated usage.