# New Features

## Shuffle SFX

Shuffles a large portion of the sounds effects. Can be used with the adjuster.

CLI: ```--shuffle_sfx```
 
## Bomb Logic 

When enabling this option, you do not start with bomb capacity but rather you must find 1 of 2 bomb bags. (They are represented by the +10 capacity item.) Bomb capacity upgrades are otherwise unavailable.
 
CLI: ```--bombbag```


# Bug Fixes and Notes.

* 0.5.1.7
	* Baserom update
	* Fix for Inverted Mode: Dark Lake Hylia shop defaults to selling a blue potion
	* Fix for Ijwu's enemizer: Boss door in Thieves' Town no longer closes after the maiden hint if Blind is shuffled to Theives' Town in boss shuffle + crossed mode
	* No logic now sets the AllowAccidentalMajorGlitches flag in the rom appropriately
	* Houlihan room now exits wherever Link's House is shuffled to
	* Rom fixes from Catobat and Codemann8. Thanks!
* 0.5.1.6
	* Rules fixes for TT (Boss and Cell) can now have TT Big Key if not otherwise required (boss shuffle + crossed dungeon)
	* BUg fix for money balancing
	* Add some bomb assumptions for bosses in bombbag mode
* 0.5.1.5
	* Fix for hard pool capacity upgrades missing
	* Bonk Fairy (Light) is no longer in logic for ER Standard and is forbidden to be a connector, so rain state isn't exitable
	* Bug fix for retro + enemizer and arrows appearing under pots
	* Added bombbag and shufflelinks to settings code
	* Catobat fixes:
		* Fairy refills in spoiler
		* Subweights support in mystery
		* More defaults for mystery weights
		* Less camera jank for straight stair transitions
		* Bug with Straight stairs with vanilla doors where Link's walking animation stopped early is fixed		 
* 0.5.1.4
	* Revert quadrant glitch fix for baserom
	* Fix for inverted
* 0.5.1.3
	* Certain lobbies forbidden in standard when rupee bow is enabled
	* PoD EG disarmed when mirroring (except in nologic)
	* Fixed issue with key logic
	* Updated baserom
* 0.5.1.2
	* Allowed Blind's Cell to be shuffled anywhere if Blind is not the boss of Thieves Town
	* Remove unique annotation from a FastEnum that was causing problems
	* Updated prevent mixed_travel setting to prevent more mixed travel
	* Prevent key door loops on the same supertile where you could have spent 2 keys on one logical door
	* Promoted dynamic soft-lock prevention on "stonewalls" from experimental to be the primary prevention (Stonewalls are now never pre-opened)
	* Fix to money balancing algorithm with small item_pool, thanks Catobat
	* Many fixes and refinements to key logic and generation	
* 0.5.1.1
	* Shop hints in ER are now more generic instead of using "near X" because they aren't near that anymore
	* Added memory location for mutliworld scripts to read what item was just obtain (longer than one frame)
	* Fix for bias in boss shuffle "full"
	* Fix for certain lone big chests in keysanity (allowed you to get contents without big key)
	* Fix for pinball checking
	* Fix for multi-entrance dungeons
	* 2 fixes for big key placement logic
		* ensure big key is placed early if the validator assumes it)
		* Open big key doors appropriately when generating rules and big key is forced somewhere
	* Updated cutoff entrances for intensity 3
* 0.5.1.0
	* Large logic refactor introducing a new method of key logic 
	* Some performance optimization
	* Some outstanding bug fixes (boss shuffle "full" picks three unique bosses to be duplicated, e.g.)
* 0.5.0.3
	* Fixed a bug in retro+vanilla and big key placement
	* Fixed a problem with shops not registering in the Multiclient until you visit one
	* Fixed a bug in the Mystery code with sfx
* 0.5.0.2
	* --shuffle_sfx option added 
* 0.5.0.1
	* --bombbag option added 
* 0.5.0.0
	* Handles headered roms for enemizer (Thanks compiling)
	* Warning added for earlier version of python (Thanks compiling)
	* Minor logic issue for defeating Aga in standard (Thanks compiling)
	* Fix for boss music in non-DR modes (Thanks codemann8)

# Known Issues

* Shopsanity Issues
	* Hints for items in shops can be misleading (ER)
	* Forfeit in Multiworld not granting all shop items
* Potential keylocks in multi-entrance dungeons
* Incorrect vanilla key logic for Mire