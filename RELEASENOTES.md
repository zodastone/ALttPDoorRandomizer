# New Features

* Lobby shuffle added as Intensity level 3
	* Can now be found in the spoiler
	* Palette changes:
		* Certain doors/transition no longer have an effect on the palette choice (dead ends mostly or just bridges)
		* Sanctuary palette back to the adjacent rooms to Sanctuary (sanctuary stays the dungeon color for now)
		* Sewer palette comes back for part of Hyrule Castle for areas "near" the sewer dropdown
	* Known issues:
		* Palettes aren't perfect 
			May add a way to turn off palette "fixing"
			* Some ugly colors
			* Invisible floors can be see in many palettes		
* --keydropshuffle added (coming to the GUI soon). This add 33 new locations to the game where keys are found under pots
and where enemies drop keys. This includes 32 small key location and the ball and chain guard who normally drop the HC
Big Key. 
	* Overall location count updated
	* Setting mentioned in spoiler
	* Known issue:
		* GT Big Key count needs to be updated
* --mixed_travel setting added
	* Due to Hammerjump, Hovering in PoD Arena, and the Mire Big Key Chest bomb jump two sections of a supertile that are
otherwise unconnected logically can be reach using these glitches. To prevent the player from unintentionally
		* prevent: Rails are added the 3 spots to prevent this tricks. This setting is recommend for those learning
		 crossed dungeon mode to learn what is dangerous and what is not. No logic seeds ignore this setting.
		 * allow: The rooms are left alone and it is up to the discretion of the player whether to use these tricks or not.
		 * force: The two disjointed sections are forced to be in the same dungeon but never logically required to complete that game.

### Experimental features

* Redesign of Keysanity Menu for Crossed Dungeon - soon to move out of experimental

#### Temporary debug features

* Removed the red square in the upper right corner of the hud if the castle gate is closed  

# Bug Fixes

* 2.0.11u
	* Fix output path setting in settings.json
	* Fix trock entrances when intensity <= 2
* 2.0.10u
	* Fix POD, TR, GT and SKULL 3 entrance if sanc ends up in that dungeon in crossed ER+
	* TR Lobbies that need a bomb and can be entered before bombing should be pre-opened
	* Animated tiles are loaded correctly in lobbies
	* If a wallmaster grabs you and the lobby is dark, the lamp turns on now
	* Certain key rules no longer override item requirements (e.g. Somaria behind TR Hub)
	* Old Man Cave is correctly one way in the graph
	* Some key logic fixes
* 2.0.9-u
	* /missing command in MultiClient fixed
* 2.0.8-u
	* Player sprite disappears after picking up a key drop in keydropshuffle
	* Sewers and Hyrule Castle compass problems
	* Double count of the Hera Basement Cage item (both overall and compass)
	* Unnecessary/inconsistent rug cutoff
	* TR Crystal Maze thought you get through backwards without Somaria
	* Ensure Thieves Attic Window area can always be reached
	* Fixed where HC big key was not counted	
* Prior fixes
	* Fixed a situation where logic did not account properly for Big Key doors in standard Hyrule Castle
	* Fixed a problem ER shuffle generation that did not account for lobbies moving around
	* Fixed a problem with camera unlock (GT Mimics and Mire Minibridge)
	* Fixed a problem with bad-pseudo layer at PoD map Balcony (unable to hit switch with Bomb)
	* Fixed a problem with the Ganon hint when hints are turned off

# Known Issues

* Multiworld = /missing command not working
* Potenial keylocks in multi-entrance dungeons
* Incorrect vanilla keylogic for Mire
* ER - Potential for Skull Woods West to be completely inaccessible in non-beatable logic