# New Features

## OWG Glitch Logic

Thanks to qadan, cheuer, & compiling

# Bug Fixes and Notes.

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
	* Hints for items in shops can be misleading
	* Capacity upgrades present in hard/expert item pools
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