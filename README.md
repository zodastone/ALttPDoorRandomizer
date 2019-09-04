# ALttPDoorRandomizer

This is a door randomizer for _The Legend of Zelda: A Link to the Past_ for the SNES
based on the Entrance Randomizer found at [KevinCathcart's Github Project.](https://github.com/KevinCathcart/ALttPEntranceRandomizer)
See https://alttpr.com/ for more details on the normal randomizer.

# Installation

Clone this repository and then run ```DungeonRandomizer.py``` (requires Python 3).

Alternatively, run ```Gui.py``` for a simple graphical user interface. (WIP)

# Settings

Only extra settings are found here. All entrance randomizer settings are supported. See their [readme](https://github.com/KevinCathcart/ALttPEntranceRandomizer/blob/master/README.md)

## Door Shuffle

### Basic

Doors are shuffled only within a single dungeon.

### Crossed

Doors are shuffled between dungeons as well.

### Vanilla

Doors are not shuffled.

### Experimental

Used for development testing. This will be removed in a future version. Use at your own risk. Might play like a plando.

# Command Line Options

```
-h, --help            
```

Show the help message and exit.

```
--door_shuffle      
```

For specifying the door shuffle you want as above. (default: basic)
