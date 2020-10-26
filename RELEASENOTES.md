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

### Experimental features

* Redesign of Keysanity Menu for Crossed Dungeon - soon to move out of experimental

#### Temporary debug features

* Removed the red square in the upper right corner of the hud if the castle gate is closed  

# Bug Fixes

* Fixed a situation where logic did not account properly for Big Key doors in standard Hyrule Castle
* Fixed a problem ER shuffle generation that did not account for lobbies moving around
* Fixed a problem with camera unlock (GT Mimics and Mire Minibridge)
* Fixed a problem with bad-pseudo layer at PoD map Balcony (unable to hit switch with Bomb)

# Known Issues 

(I'm planning to fix theese in this Unstable iteration hopefully)

* Hammerjump (et al) rails
* Backward TR Crystal Maze locking Somaria
* Ganon hint when hints are turned off not correct