# New Features

## Shuffle SFX

Shuffles a large portion of the sounds effects. Can be used with the adjuster.

CLI: ```--shuffle_sfx```
 
## Bomb Logic 

When enabling this option, you do not start with bomb capacity but rather you must find 1 of 2 bomb bags. (They are represented by the +10 capacity item.) Bomb capacity upgrades are otherwise unavailable.
 
CLI: ```--bombbag```


# Bug Fixes and Notes.

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