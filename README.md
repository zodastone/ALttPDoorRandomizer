# ALttPDoorRandomizer

This is a door randomizer for _The Legend of Zelda: A Link to the Past_ for the SNES
based on the Entrance Randomizer found at [KevinCathcart's Github Project.](https://github.com/KevinCathcart/ALttPEntranceRandomizer)
See https://alttpr.com/ for more details on the normal randomizer.

# Known Issues

[List of Known Issues and Their Status](https://docs.google.com/document/d/1Bk-m-QRvH5iF60ndptKYgyaV7P93D3TiG8xmdxp_bdQ/edit?usp=sharing)

# Feedback and Bug Reports

Please just DM me on discord for now. I (Aerinon) can be found at the [ALTTP Randomizer discord](https://discordapp.com/invite/alttprandomizer).

# Installation

Clone this repository and then run ```DungeonRandomizer.py``` (requires Python 3).

Alternatively, run ```Gui.py``` for a simple graphical user interface. (WIP)

# Settings

Only extra settings are found here. All entrance randomizer settings are supported. See their [readme](https://github.com/KevinCathcart/ALttPEntranceRandomizer/blob/master/README.md)

## Door Shuffle (--doorShuffle)

### Basic

Doors are shuffled only within a single dungeon.

### Crossed

Doors are shuffled between dungeons as well.

### Vanilla

Doors are not shuffled.

## Intensity (--intensity number)

#### Level 1
Normal door and spiral staircases are shuffled
#### Level 2
Same as Level 1 plus open edges and straight staircases are shuffled.
#### Level 3
Same as Level 2 plus Dungeon Lobbies are shuffled

## KeyDropShuffle (--keydropshuffle)

Adds 33 new locations to the randomization pool. The 32 small keys found under pots and dropped by enemies and the Big
Key drop location are added to the pool. The keys normally found there are added to the item pool. Retro adds 
32 generic keys to the pool instead.

## Crossed Dungeon Specific Settings

### Mixed Travel (--mixed_travel value)

Due to Hammerjump, Hovering in PoD Arena, and the Mire Big Key Chest bomb jump two sections of a supertile that are
otherwise unconnected logically can be reach using these glitches. To prevent the player from unintentionally

#### Prevent

Rails are added the 3 spots to prevent this tricks. This setting is recommend for those learning crossed dungeon mode to
learn what is dangerous and what is not. No logic seeds ignore this setting.

#### Allow

The rooms are left alone and it is up to the discretion of the player whether to use these tricks or not.

#### Force

The two disjointed sections are forced to be in the same dungeon but never logically required to complete that game.


## Map/Compass/Small Key/Big Key shuffle (aka Keysanity)

These settings allow dungeon specific items to be distributed anywhere in the world and not just in their native dungeon.
Small Keys dropped by enemies or found in pots are not affected. The chest in southeast Skull Woods that is traditionally
a guaranteed Small Key still is. These items will be distributed according to the v26/balanced algorithm, but the rest
of the itempool will respect the algorithm setting. Music for dungeons is randomized so it cannot be used as a tell
for which dungeons contain pendants and crystals; finding a Map for a dungeon will allow the overworld map to display its prize.

## Retro

This setting turns all Small Keys into universal Small Keys that can be used in any dungeon and are distributed across the world.
The Bow now consumed rupees to shoot; the cost is 10 rupees per Wood Arrow and 50 per Silver Arrow. Shooting Wood Arrows requires
the purchase of an arrow item from shops, and to account for this and the dynamic use of keys, both Wood Arrows and Small Keys will
be added to several shops around the world. Four "take any" caves are added that allow the player to choose between an extra Heart
Container and a Bottle being filled with Blue Potion, and one of the four swords from the item pool is placed into a special cave as
well. The five caves that are removed for these will be randomly selected single entrance caves that did not contain any items or any shops.
In further concert with the Bow changes, all arrows under pots, in chests, and elsewhere in the seed will be replaced with rupees.

## Seed

Can be used to set a seed number to generate. Using the same seed with same settings on the same version of the entrance randomizer will always yield an identical output.

## Count

Use to batch generate multiple seeds with same settings. If a seed number is provided, it will be used for the first seed, then used to derive the next seed (i.e. generating 10 seeds with the same seed number given will produce the same 10 (different) roms each time).

# Command Line Options

```
-h, --help            
```

Show the help message and exit.

```
--door_shuffle      
```

For specifying the door shuffle you want as above. (default: basic)

```
--intensity      
```

For specifying the door shuffle intensity level you want as above. (default: 2)
