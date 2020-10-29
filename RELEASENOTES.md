# New Features

* Lobby shuffle added as Intensity level 3
	* Can now be found in the spoiler
	* Known issues:
		* Palettes aren't perfect - may add Sanctuary and Sewer palette back. May add a way to turn off palette "fixing"
		* Certain hints in ER due to lobby changes
		* Animated tiles aren't loaded correctly in lobbies
		* If a wallmaster grabs you and the lobby is dark, the lamp doesn't turn on
* --keydropshuffle added (coming to the GUI soon). This add 33 new locations to the game where keys are found under pots
and where enemies drop keys. This includes 32 small key location and the ball and chain guard who normally drop the HC
Big Key. 
	* Multiworld untested - May need changes to MultiClient/MultiServer to recognize new locations
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

* Fixed a situation where logic did not account properly for Big Key doors in standard Hyrule Castle
* Fixed a problem ER shuffle generation that did not account for lobbies moving around
* Fixed a problem with camera unlock (GT Mimics and Mire Minibridge)
* Fixed a problem with bad-pseudo layer at PoD map Balcony (unable to hit switch with Bomb)
* Fixed a problem with the Ganon hint when hints are turned off

# Known Issues 

(I'm planning to fix theese in this Unstable iteration hopefully)

* Backward TR Crystal Maze locking Somaria