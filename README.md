# ALttPDoorRandomizer

This is a door randomizer for _The Legend of Zelda: A Link to the Past_ for the SNES
based on the Entrance Randomizer found at [KevinCathcart's Github Project.](https://github.com/KevinCathcart/ALttPEntranceRandomizer)
See https://alttpr.com/ for more details on the normal randomizer.

# Known Issues

[List of Known Issues and Their Status](https://docs.google.com/document/d/1Bk-m-QRvH5iF60ndptKYgyaV7P93D3TiG8xmdxp_bdQ/edit?usp=sharing)

# Feedback and Bug Reports

Please just DM me on discord for now. I (Aerinon) can be found at the [ALTTP Randomizer discord](https://discordapp.com/invite/alttprandomizer).

# Installation

Click on 

https://github.com/aerinon/ALttPDoorRandomizer/releases

Go down to Assets and find a build for your system (Windows, Mac, or Linux)

Download and unzip. Find the DungeonRandomizer.exe or equivalent

# Installation from source

See these instructions.

https://github.com/aerinon/ALttPDoorRandomizer/blob/DoorDev/docs/BUILDING.md

When installing platform specific dependencies, don't forget to run the appropriate command from the bottom of the page! Those will install missing pip dependencies.

Running the MultiServer and MultiClient for multiworld should run resources/ci/common/local_install.py for those dependencies as well.

To use the CLI, run ```DungeonRandomizer.py```.

Alternatively, run ```Gui.py``` for a simple graphical user interface.

# Commonly Missed Things and Differences from other Randomizers

Most of these apply only when the door shuffle is not vanilla.

### Starting Item

You start with a “Mirror Scroll”, a dumbed-down mirror that only works in dungeons, not the overworld and can’t erase blocks like the Mirror.

### Navigation

* The Pinball Room’s trap door can be removed in the case where it is required to go through to get to the back of Skull Woods.
* Holes in Mire Torches Top and Mire Torches Bottom fall through to rooms below (you only need fire to get the chest)
* You can Hookshot from the left Mire wooden Bridge to the right one.
* In the PoD Arena, you can bonk with Boots between the two blue crystal barriers against the ladder to reach the Arena Bridge chest and door. (Bomb Jump also possible but not in logic - Boots are required)
* Flooded Rooms in Swamp can be traversed backward and may be required.

### Other Logic

* The chest in southeast Skull Woods that is traditionally a guaranteed Small Key in ER is not guaranteed here.
* Fire Rod is not in logic for dark rooms. (Hard enough to figure out which dark room you are in.) This is different from Advanced mode on the VT randomizer. Otherwise Advanced logic is always used. (There is no basic logic.)
* The hammerjump (and some other skips) are not in logic by default (see the mixed_travel setting for details). Doing so in a crossed dungeon seed can put you into another dungeon with the wrong dungeon id. (Much like EG)

### Boss Differences

* You have to find the attic floor and bomb it open and bring the maiden to the light to fight Blind. In cross dungeon door shuffle, the attic can be in any dungeon. If you bring the maiden to the boss arena, she will hint were the cracked floor can be found. If hints are on, there is a special one about the cracked floor.
* GT Bosses do not respawn after killing them in this mode.
* Enemizer change: The attic/maiden sequence is now active and required when Blind is the boss of Theives' Town even when bosses are shuffled.

### Crystal Switches

* You can hit the PoD crystal switch in the Sexy Statue room with a bomb from the balcony above without jumping down.
* GT Crystal Conveyor room (it has gibdos) - You can hit the crystal switch with a bomb when the blue barrier is up from the far side so you can leave the room to the left with blue barriers down.
* PoD Arena Bridge. If entering from the bridge, you can circle round and hit the switch, then fall into the hole to respawn at the bridge again with the crystal barriers different (if you don’t have a proper ranged weapon that can hit it)

### Misc

* Compass counts no longer function after you get the Triforce (this is actually true in all randomizers)

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
Same as Level 1 plus open edges and both types of straight staircases are shuffled.
#### Level 3
Same as Level 2 plus Dungeon Lobbies are shuffled

## KeyDropShuffle (--keydropshuffle)

Adds 33 new locations to the randomization pool. The 32 small keys found under pots and dropped by enemies and the Big
Key drop location are added to the pool. The keys normally found there are added to the item pool. Retro adds 
32 generic keys to the pool instead.

## Crossed Dungeon Specific Settings

### Mixed Travel (--mixed_travel value)

Due to Hammerjump, Hovering in PoD Arena, and the Mire Big Key Chest bomb jump two sections of a supertile that are
otherwise unconnected logically can be reached using these glitches. To prevent the player from unintentionally changing
dungeons while doing these tricks, you may use one of the following options.

#### Prevent (default)

Rails are added the 3 spots to prevent this tricks. This setting is recommend for those learning crossed dungeon mode to
learn what is dangerous and what is not. No logic seeds ignore this setting.

#### Allow

The rooms are left alone and it is up to the discretion of the player whether to use these tricks or not.

#### Force

The two disjointed sections are forced to be in the same dungeon but the glitches are never logically required to complete that game.cause then you would need time to check the map in a d

### Standardize Palettes (--standardize_palettes)
No effect if door shuffle is not on crossed

#### Standardize (default)
Rooms in the same dungeon have their palettes changed to match. Hyrule Castle is split between Sewer and HC palette.
Rooms adjacent to sanctuary get their coloring to match the Sanctuary's original palette.

#### Original
Rooms/supertiles keep their original palettes.

## Shopsanity

This adds 32 shop locations (9 more in retro) to the general location pool.

Multi-world supported. Thanks go to Pepper and CaitSith2 for figuring out several items related to this major feature.

Shop locations:
* Lake Hylia Cave Shop (3 items)
* Kakariko Village Shop (3 items)
* Potion Shop (3 new items)
* Paradox Cave Shop (3 items)
* Capacity Upgrade Fairy (2 items)
* Dark Lake Hylia Shop (3 items)
* Curiosity/Red Shield Shop (3 items)
* Dark Lumberjack Shop (3 items)
* Dark Potion Shop (3 items)
* Village of Outcast Hammer Peg Shop (3 items)
* Dark Death Mountain Shop (3 items)

Item Pool changes: To accommodate the new locations, new items are added to the pool, as follows:

* 10 - Red Potion Refills
* 9 - Ten Bombs
* 4 - Small Hearts
* 4 - Blue Shields
* 1 - Red Shield
* 1 - Bee
* 1 - Ten Arrows
* 1 - Green Potion Refill
* 1 - Blue Potion Refill
* 1 - +5 Bomb Capacity
* 1 - +5 Arrow Capacity

1. Initially, 1 of each type of potion refill is shuffled to the shops. (the Capacity Fairy is excluded from this, see step 4). This ensures that potions can be bought somewhere.
2. The rest of the shop pool is shuffled with the rest of the item pool. 
3. At this time, only Ten Bombs, Ten Arrows, Capacity upgrades, Small Hearts, and the non-progressive shields can appear outside of shops. Any other shop items are replaced with rupees of various amounts. This is because of one reason: potion refills and the Bee are indistinguishable from Bottles with that item in them. Receiving those items without a bottle or empty bottle is essentially a nothing item but looks like a bottle. Note, the non-progressive Shields interact fine with Progressive Shields (you never get downgraded) but are usually also a nothing item most of the time.
4. The Capacity Fairy cannot sell Potion Refills because the graphics are incompatible. 300 Rupees will replace any potion refill that ends up there.
5. For capacity upgrades, if any shop sells capacity upgrades, then it will sell all seven of that type. Otherwise, if plain bombs or arrows are sold somewhere, then the other six capacity upgrades will be purchasable first at those locations and then replaced by the underlying ammo. If no suitable spot is found, then no more capacity upgrades will be available for that seed. (There is always one somewhere in the pool.)
6. Any shop item that is originally sold by shops can be bought indefinitely, but only the first purchase counts toward total checks on the credits screen & item counter. All other items can be bought only once.

All items in the general item pool may appear in shops. This includes normal progression items and dungeon items in the appropriate keysanity settings.

#### Pricing Guide

#### Sphere effects

Design goal: Shops in early spheres may be discounted below the base price while shops in later spheres will likely exceed the base price range. This is an attempt to balance out the rupees in the item pool vs. the prices the shops charges. Poorer item pools like Triforce Hunt may have early shop prices be adjusted downward while rupee rich item pools will have prices increased, but later in the game.

Detailed explanation: It is calculated how much money is available in the item pool and various rupee sources. If this amount exceeds the total amount of money needed for shop prices for items, then shops that are not in sphere 1 will raise their prices by a calculated amount to help balance out the money. Conversely, if the amount is below the money needed, then shops in sphere 1 will be discounted by a calculated amount to help ensure everything is purchase-able with minimal grinding.

#### Base prices

All prices range approx. from half the base price to twice the base price (as a max) in increments of 5, the exact price is chosen randomly within the range subject to adjustments by the sphere effects above.

| Category          | Items   | Base Price | Typical Range |
| ----------------- | ------- |:----------:|:-------------:|
| Major Progression | Hammer, Hookshot, Mirror, Ocarina, Boots, Somaria, Fire Rod, Ice Rod | 250 | 125-500
|                   | Moon Pearl | 200 | 100-400
|                   | Lamp, Progressive Bows, Gloves, & Swords | 150 | 75-300
|                   | Triforce Piece | 100 | 50-200
| Medallions        | Bombos, Ether, Quake | 100 | 50-200
| Safety/Fetch      | Cape, Mushroom, Shovel, Powder, Bug Net, Byrna, Progressive Armor & Shields, Half Magic | 50 | 25-100
| Bottles			| Empty Bottle or Bee Bottle | 50 | 25-100
|       			| Green Goo or Good Bee | 60 | 30-120
|       			| Red Goo or Fairy | 70 | 35-140
|        			| Blue Goo | 80 | 40-160
| Health            | Heart Container | 40 | 20-80
|                   | Sanctuary Heart | 50 | 25-100 
|                   | Piece of Heart | 10 | 5-20
| Dungeon           | Big Keys | 60 | 30-120
|                   | Small Keys | 40 | 20-80
|                   | Info Maps | 20 | 10-40
|                   | Other Maps & Compasses | 10 | 5-20
| Rupees			| Green | Free | Free
|       			| Blue  | 2 | 2-4
|       			| Red  | 10 | 5-20
|       			| Fifty  | 25 | 15-50
|       			| One Hundred  | 50 | 25-100
|       			| Three Hundred  | 150 | 75-300
| Ammo	            | Three Bombs | 15 | 10-30
|       			| Single Arrow | 3 | 3-6
| Original Shop Items | Other Ammo, Refills, Non-Progressive Shields, Capacity Upgrades, Small Hearts, Retro Quiver, Universal Key | Original | .5 - 2 * Original

#### Rupee Balancing Algorithm

To prevent needed to grind for rupees to buy things in Sphere 1 and later, a money balancing algorithm has been developed to counteract the need for rupees. Basic logic: it assumes you buy nothing until you are blocked by a shop, a check that requires money, or blocked by Kiki. Then you must have enough to make all purchases. If not, any free rupees encountered may be swapped with higher denominations that have not been encountered. Ammo may also be swapped, if necessary.

(Checks that require money: Bottle Merchant, King Zora, Digging Game, Chest Game, Blacksmith, anything blocked by Kiki e.g. all of Palace of Darkness when ER is vanilla)

The Houlihan room is not in logic but the five dungeon rooms that provide rupees are. Pots with rupees, the arrow game, and all other gambling games are not counted for determining income.

Currently this is applied to seeds without shopsanity on so early money is slightly more likely if progression is on a check that requires money even if Shopsanity is not turned on. 

#### Retro and Shopsanity

9 new locations are added.

The four "Take Any" caves are converted into "Take Both" caves. Those and the old man cave are included in the shuffle. The sword is returned to the pool, and the 4 heart containers and 4 blue potion refills are also added to the general item pool. All items found in the retro caves are free to take once. Potion refills will disappear after use.

Arrow Capacity upgrades are now replaced by Rupees wherever it might end up.
 
The Ten Arrows and 5 randomly selected Small Hearts or Blue Shields are replaced by the quiver item (represented by the Single Arrow in game.) 5 Red Potion refills are replaced by the Universal small key. It is assured that at least one shop sells Universal Small Keys. The quiver may thus not be found in shops. The quiver and small keys retain their original base price, but may be discounted.

## Logic Level

### Overworld Glitches

Set `--logic` to `owglitches` to make overworld glitches required in the logic.

## Shuffle Links House

In certain ER shuffles, (not dungeonssimple or dungeonsfulls), you can now control whether Links House is shuffled or remains vanilla. Previously, inverted seeds had this behavior and would shuffle links house, but now if will only do so if this is specified. Now, also works for open modes, but links house is never shuffled in standard mode.

## Reduce Flashing

Accessibility option to reducing some flashing animations in the game.

## Pseudo-boots

Option to start with ability to dash, but not able to make any boots required logical checks or traversal.

## Experimental Features

The treasure check counter is turned on. Also, you will start as a bunny if your spawn point is in the dark world.

## Triforce Hunt Settings

A collection of settings to control the triforce piece pool.

* --triforce_goal_min: Minimum number of pieces to collect to win
* --triforce_goal_max: Maximum number of pieces to collect to win
* --triforce_pool_min: Minimum number of pieces in item pool
* --triforce_pool_max: Maximum number of pieces in item pool
* --triforce_min_difference: Minimum difference between pool and goal to win

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
--door_shuffle <mode>     
```

For specifying the door shuffle you want as above. (default: basic)

```
--intensity <number>     
```

For specifying the door shuffle intensity level you want as above. (default: 2)

```
--keydropshuffle      
```

Include mobs and pots drop in the item pool. (default: not enabled)

```
--shopsanity      
```

Includes shop locations in the item pool.

```
--pseudoboots
```

Start with dash ability, but no way to use boots to accomplish checks 

```
--shufflelinks
```

Whether to shuffle links house in most ER modes.

```
--experimental
```

Enables experimental features

```
--mixed_travel <mode>      
```

How to handle certain glitches in crossed dungeon mode. (default: prevent)

```
--standardize_palettes (mode)
```

Whether to standardize dungeon palettes in crossed dungeon mode. (default: standardize)

```
--reduce_flashing
```

Reduces amount of flashing in some animations