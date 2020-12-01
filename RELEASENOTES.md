# New Features

## Lobby shuffle added as Intensity level 3

* Standard notes: 
	* The sanctuary is vanilla, and will be missing the exit door until Zelda is rescued
	* In entrance shuffle the hyrule castle left and right exit door will be missing until Zelda is rescued. This
		replaces the rails that used to block those lobby exits
	* In non-entrance shuffle, Agahnims tower can be in logic if you have cape and/or Master sword, but you are never
		required to beat Agahnim 1 until Zelda is rescued.
* Open notes:
	* The Sanctuary is limited to be in a LW dungeon unless you have ER Crossed or higher enabled
	* Mirroring from the Sanctuary to the new "Sanctuary" lobby is now in logic, as is exiting there.
	* In ER crossed or higher, if the Sanctuary is in the Dark World, Link starts as Bunny there until the Moon Pearl
		 is found. Nothing inside that dungeon is in logic until the Moon Pearl is found. (Unless it is a multi-entrance
		  dungeon that you can access from some LW entrance)		 
* Lobby list is found in the spoiler
* Exits for Multi-entrance dungeons after beating bosses now makes more sense. Generally you'll exit from a entrance
	from which the boss can logically be reached. If there are multiple, ones that do not lead to regions only accessible 
	by connector are preferred. The exit is randomly chosen if there's no obvious preference. However, In certain poor
	 cases like Skull Woods in ER, sometimes an exit is chosen not because you can reach the boss from there, but to
	 prevent a potential forced S&Q.
* Palette changes:
	* Certain doors/transition no longer have an effect on the palette choice (dead ends mostly or just bridges)
	* Sanctuary palette used on the adjacent rooms to Sanctuary (Sanctuary stays the dungeon color for now)
	* Sewer palette comes back for part of Hyrule Castle for areas "near" the sewer dropdown
	* There is a setting to keep original palettes (--standardize_palettes original)
* Known issues:
	* Palettes aren't perfect 			
		* Some ugly colors
		* Invisible floors can be see in many palettes		

## Key Drop Shuffle

--keydropshuffle added. This add 33 new locations to the game where keys are found under pots
and where enemies drop keys. This includes 32 small key location and the ball and chain guard who normally drop the HC
Big Key. 

* Overall location count updated
* Setting mentioned in spoiler
* Minor change: if a key is Universal or for that dungeon, then if will use the old mechanics of picking up the key without
an entire pose and should be obtainable with the hookshot or boomerang as before

## --mixed_travel setting
* Due to Hammerjump, Hovering in PoD Arena, and the Mire Big Key Chest bomb jump two sections of a supertile that are
otherwise unconnected logically can be reach using these glitches. To prevent the player from unintentionally
	* prevent: Rails are added the 3 spots to prevent this tricks. This setting is recommend for those learning
	 crossed dungeon mode to learn what is dangerous and what is not. No logic seeds ignore this setting.
	 * allow: The rooms are left alone and it is up to the discretion of the player whether to use these tricks or not.
	 * force: The two disjointed sections are forced to be in the same dungeon but never logically required to complete that game.

## Keysanity menu redesign

Redesign of Keysanity Menu complete for crossed dungeon and moved out of experimental.
* First screen about Big Keys and Small Keys
	* 1st Column: The map is required for information about the Big Key
		* If you don't have the map, it'll be blank until you obtain the Big Key
		* If have the map:
			* 0 indicates there is no Big Key for that dungeon
			* A red symbol indicates the Ball N Chain guard has the big key for that dungeon (does not apply in 
			--keydropshuffle)
			* Blank if there a big key but you haven't found it yet
	* 2nd Column displays the current number of keys for that dungeon. Suppressed in retro (always blank)
	* 3rd Column only display if you have the map. It shows the number of keys left to collect for that dungeon. If
	--keydropshuffle is off, this does not count key drops. If on, it does.
	* (Note: the key columns can display up to 36 using the letters A-Z after 9)
* Second screen about Maps / Compass
	* 1st Column: indicate if you have foudn the map of not for that dungeon
	* 2nd and 3rd Column: You must have the compass to see these columns. A two-digit display that show you how
	many chests are left in the dungeon. If -keydropshuffle is off, this does not count key drop. If on, it does. 
	
## Potshuffle by compiling

Same flag as before but uses python logic written by compiling instead of the enemizer logic-less version. Needs some
testing to verify logic is all good.

## Other features

### Spoiler log improvements

* In crossed mode, the new dungeon is listed along with the location designated by a '@' sign
* Random gt crystals and ganon crystal are noted in the settings for better reproduction of seeds

### Experimental features

* Only the random bomb doors and the item counter are currently experimental
	* Item counter is suppressed in Triforce Hunt

#### Temporary debug features

* Removed the red square in the upper right corner of the hud if the castle gate is closed  

# Bug Fixes

* 2.0.17u
	* Generation improvements
* 2.0.16u
	* Prevent HUD from showing key counter when in the overworld. (Aga 2 doesn't always clear the dungeon indicator)
	* Fixed key logic regarding certain isolated "important" locations
	* Fixed a problem with keydropshuffle thinking certain progression items are keys
	* A couple of inverted rules fixed
	* A more accurate count of which locations are blocked by teh big key in Ganon's Tower
	* Updated base rom to 31.0.7 (includes potential hera basement cage fix)
* 2.0.15u
	* Allow Aga Tower lobby door as a a paired keydoor (typo)
	* Fix portal check for multi-entrance dungeons
* 2.0.14u
	* Removal of key doors no longer messes up certain lobbies
	* Fixed ER entrances when Desert Back is a connector
* 2.0.13u
	* Minor portal re-work for certain logic and spoiler information 
	* Repaired certain exits wrongly affected by Sanctuary placement (ER crossed + intensity 3)
	* Fix for inverted ER + intensity 3
	* Fix for current small keys missing on keysanity menu
	* Logic added for cases where you can flood Swamp Trench 1 before finding flippers and lock yourself out of getting
	something behind the trench that leads to the flippers
* 2.0.12u
	* Another fix for animated tiles (fairy fountains)
	* GT Big Key stat fixed on credits
	* Any denomination of rupee 20 or below can be removed to make room for Crossed Dungeon's extra dungeon items. This
	helps retro generate more often.
	* Fix for TR Lobbies in intensity 3 and ER shuffles that was causing a hardlock
	* Standard ER logic revised for lobby shuffle and rain state considerations.
* 2.0.11u
	* Fix output path setting in settings.json
	* Fix trock entrances when intensity <= 2
* 2.0.10u
	* Fix POD, TR, GT and SKULL 3 entrances if sanc ends up in that dungeon in crossed ER+
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