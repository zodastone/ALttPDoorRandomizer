# Countdown

This is a prototype for a "countdown" game mode for the randomizer for _The Legend of Zelda: A Link to the Past_ for the SNES,
based on the Door Randomizer found at [Aerinon's Github Project.](https://github.com/aerinon/ALttPDoorRandomizer)

Inspired by the "Full Countdown" (aka VARIA hud) game mode for the [VARIA Randomizer](https://varia.run/) for Super Metroid,
every location checked will inform you of the number of important items remaining in the current region.

See https://alttpr.com/ for more details on the normal randomizer.
See https://github.com/aerinon/ALttPDoorRandomizer/blob/DoorDev/README.md for non-countdown-related features.

# Feedback and Bug Reports

Feel free to DM me (ZodaStone) on Discord. I'm in the [ALTTP Randomizer discord](https://discordapp.com/invite/alttprandomizer).

Please keep in mind that this is a quick-and-dirty prototype, and is not meant to be feature-complete, portable, efficient, etc.

# Quick Setup

(For those who already have a Entrance/Door Rando setup and wish to add countdown functionality to it).

From the main Github page on the Countdown branch, click the green "Code" dropdown, then Download ZIP.
Unzip the folder, then copy the following files into your existing entrance/door rando folder (place at the same level as Gui.py, MultiClient.py, etc.):
* Countdown.py
* countdown_display.txt
* MultiClientCountdown.py

This "should" work with most Entrance/Door Rando versions, provided the underlying multiclient code is unmodified, and the spoiler log format is compatible (untested).

# Installation from source

Note: Installation of dependencies can be skipped if you have already used another door rando fork, as the dependencies are the same. Github Releases with packaged executable files not currently supported.

Prerequisites: [Python 3.6+](http://python.org/downloads), [pip](https://pip.pypa.io/en/stable/installation/)

From the main Github page on the Countdown branch, click the green "Code" dropdown, then Download ZIP.

Navigate to resources/app/meta/manifests, open a command prompt and run ```pip install -r pip_requirements.txt```.

To use the CLI, run ```DungeonRandomizer.py```.

Alternatively, run ```Gui.py``` for a simple graphical user interface.

# Running Countdown Instructions

Generate a seed with the included generator, or via https://alttpr.com/

Rename the spoiler log (required) to countdown_spoiler.txt and place it in the same directory as Countdown.py, MultiClientCountdown.py.  Then:

* Non-Multiworld Games: Perform the usual steps for connecting to a multiworld (launch game and run QUsb2Snes/LUA scripts or SNI), but run Countdown.py instead of MultiClient.py
* Multiworld Games: Perform the usual steps for connecting to a multiworld (launch game and run QUsb2Snes/LUA scripts or SNI), but run MultiClientCountdown.py instead of MultiClient.py

# What's an "Important Item"?

* Progressive swords, gloves, shields, mail (not bomb/arrow capacity)
* Y-items (not Bombs)
* Others: Pearl, Flippers, Boots, Half Magic
* Keys (if Keysanity enabled.  Remaining keys are reported separately from important items)
* If Triforce Hunt is enabled, remaining triforce pieces are reported separately from important items

# Supported Game Modes

Typical "Defeat Ganon" seeds, plus:
* Triforce Hunts
* Keysanity
* Shopsanity
* Single Player or Multiworld Games (use Countdown.py or MultiClientCountdown.py accordingly)
Should be compatible with seeds generated with the included generator, other Door Rando forks, or via https://alttpr.com/

# Unsupported Game Modes

* Randomized key drops / pot keys / potsanity
* Race seeds (seeds without a spoiler log)
* Seeds generated with anything other than the included generator

### Note:

* Non-progressive swords/gloves/shields/mail will always be considered unimportant
* Location regions are not updated if entrance/door rando is applied
* Using command ```/countdown``` will display discovered regions with important items still remaining

# Region Definitions

Each dungeon is its own region.

Light World is divided into:
* Death Mountain
* Kakariko Village
* North Light World (everything north of Kakariko and west of the river)
* South Light World (everything south of Kakariko and the river, including the area around Hyrule Castle and Lake Hylia)
* East Light World (everything east of the river, including waterfall cave and the Zora area)

Dark World is divided along the same lines.
Yes, this means Bumper Ledge and Catfish are the only checks in North/East Dark World, unless Shopsanity is enabled.

The location-to-region mapping is specified in countdown_region_table in Countdown.py / MultiClientCountdown.py.

### Common Gachas

* Uncle, Secret Passage, and Man Under the Bridge are in South Light World, Pyramid is in South Dark World
* Purple Chest is in Village of Outcasts
* Race Game and Library are in Kakariko Village, Digging Game is in Village of Outcasts

# Text Source For Streaming

* The most recent important items log is stored in countdown_display.txt.
* If streaming, feel free to use this as a text source, to mimic having this data as part of the hud (a la Super Metroid rando).

