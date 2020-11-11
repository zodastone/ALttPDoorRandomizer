# New Features

* Lobby shuffle added as Intensity level 3
	* Can now be found in the spoiler
	* Known issues:
		* If a dungeon is vanilla in ER and Sanc is in that dungeon and the dungeon has an entrance that needs to let link out: is broken.
			* e.g. PoD, GT, TR
		* Some TR lobbies that need a bomb aren't pre-opened.
		* Palettes aren't perfect - may add Sanctuary and Sewer palette back. May add a way to turn off palette "fixing"
			* Some ugly colors
			* Invisible floors can be see in many palettes
		* Animated tiles aren't loaded correctly in lobbies
		* If a wallmaster grabs you and the lobby is dark, the lamp doesn't turn on
* --keydropshuffle added (coming to the GUI soon). This add 33 new locations to the game where keys are found under pots
and where enemies drop keys. This includes 32 small key location and the ball and chain guard who normally drop the HC
Big Key. 
	* Overall location count updated
	* Setting mentioned in spoiler
	* GT Big Key count / total location count needs to be updated
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