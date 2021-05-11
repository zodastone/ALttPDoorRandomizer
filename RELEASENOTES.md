# New Features

## OWG Glitch Logic

Thanks to qadan, cheuer, & compiling

# Bug Fixes and Notes.

* 0.4.0.1
	* Moved stonewall pre-opening to not happen in experimental
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