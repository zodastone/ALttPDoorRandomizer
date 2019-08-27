
from BaseClasses import Door, DoorType, Direction

# constants
# door offsets
Top = 0
Left = 0
Mid = 1
Bot = 2
Right = 2
# layer numbers
High = 0
Low = 1


def create_doors(world, player):
    world.doors += [
        # hyrule castle
        create_toggle_door(player, 'Hyrule Castle Lobby W', DoorType.Normal, Direction.West, 0x61, Mid, High),
        create_toggle_door(player, 'Hyrule Castle Lobby E', DoorType.Normal, Direction.East, 0x61, Mid, High),
        create_dir_door(player, 'Hyrule Castle Lobby WN', DoorType.Normal, Direction.West, 0x61, Top, High),
        create_dir_door(player, 'Hyrule Castle Lobby North Stairs', DoorType.StraightStairs, Direction.North, 0x61, Mid, High),
        create_toggle_door(player, 'Hyrule Castle West Lobby E', DoorType.Normal, Direction.East, 0x60, Mid, Low),
        create_dir_door(player, 'Hyrule Castle West Lobby N', DoorType.Normal, Direction.North, 0x60, Right, Low),
        create_dir_door(player, 'Hyrule Castle West Lobby EN', DoorType.Normal, Direction.East, 0x60, Top, High),
        create_toggle_door(player, 'Hyrule Castle East Lobby W', DoorType.Normal, Direction.West, 0x62, Mid, Low),
        create_dir_door(player, 'Hyrule Castle East Lobby N', DoorType.Normal, Direction.North, 0x62, Mid, High),
        create_dir_door(player, 'Hyrule Castle East Lobby NW', DoorType.Normal, Direction.North, 0x62, Left, Low),
        create_dir_door(player, 'Hyrule Castle East Hall W', DoorType.Normal, Direction.West, 0x52, Top, Low),
        create_dir_door(player, 'Hyrule Castle East Hall S', DoorType.Normal, Direction.South, 0x52, Mid, High),
        create_dir_door(player, 'Hyrule Castle East Hall SW', DoorType.Normal, Direction.South, 0x52, Left, Low),
        create_dir_door(player, 'Hyrule Castle West Hall E', DoorType.Normal, Direction.East, 0x50, Top, Low),
        create_dir_door(player, 'Hyrule Castle West Hall S', DoorType.Normal, Direction.South, 0x50, Right, Low),
        create_dir_door(player, 'Hyrule Castle Back Hall W', DoorType.Normal, Direction.West, 0x01, Top, Low),
        create_dir_door(player, 'Hyrule Castle Back Hall E', DoorType.Normal, Direction.East, 0x01, Top, Low),
        create_door(player, 'Hyrule Castle Back Hall Down Stairs', DoorType.SpiralStairs),
        create_dir_door(player, 'Hyrule Castle Throne Room N', DoorType.Normal, Direction.North, 0x51, Mid, High),
        create_dir_door(player, 'Hyrule Castle Throne Room South Stairs', DoorType.StraightStairs, Direction.South, 0x51, Mid, Low),

        # hyrule dungeon level
        create_door(player, 'Hyrule Dungeon Map Room Up Stairs', DoorType.SpiralStairs),
        create_dir_door(player, 'Hyrule Dungeon North Abyss South Edge', DoorType.Open, Direction.South, 0x72, None, Low),
        create_dir_door(player, 'Hyrule Dungeon North Abyss Catwalk Edge', DoorType.Open, Direction.South, 0x72, None, High),
        create_dir_door(player, 'Hyrule Dungeon South Abyss North Edge', DoorType.Open, Direction.North, 0x82, None, Low),
        create_dir_door(player, 'Hyrule Dungeon South Abyss West Edge', DoorType.Open, Direction.West, 0x82, None, Low),
        create_dir_door(player, 'Hyrule Dungeon South Abyss Catwalk North Edge', DoorType.Open, Direction.North, 0x82, None, High),
        create_dir_door(player, 'Hyrule Dungeon South Abyss Catwalk West Edge', DoorType.Open, Direction.West, 0x82, None, High),
        create_dir_door(player, 'Hyrule Dungeon Guardroom Catwalk Edge', DoorType.Open, Direction.East, 0x81, None, High),
        create_dir_door(player, 'Hyrule Dungeon Guardroom Abyss Edge', DoorType.Open, Direction.West, 0x81, None, High),
        create_dir_door(player, 'Hyrule Dungeon Guardroom N', DoorType.Normal, Direction.North, 0x81, Left, Low), # todo: is this a toggle door?
        create_dir_door(player, 'Hyrule Dungeon Armory S', DoorType.Normal, Direction.South, 0x71, Left, Low), # not sure what the layer should be here
        create_door(player, 'Hyrule Dungeon Armory Down Stairs', DoorType.SpiralStairs),
        create_door(player, 'Hyrule Dungeon Staircase Up Stairs', DoorType.SpiralStairs),
        create_door(player, 'Hyrule Dungeon Staircase Down Stairs', DoorType.SpiralStairs),
        create_door(player, 'Hyrule Dungeon Cellblock Up Stairs', DoorType.SpiralStairs),

        # sewers
        create_blocked_door(player, 'Sewers Behind Tapestry S', DoorType.Normal, Direction.South, 0x41, Mid, High),
        create_door(player, 'Sewers Behind Tapestry Down Stairs', DoorType.SpiralStairs),
        create_door(player, 'Sewers Rope Room Up Stairs', DoorType.SpiralStairs),
        create_dir_door(player, 'Sewers Rope Room North Stairs', DoorType.StraightStairs, Direction.North, 0x42, Mid, High),
        create_dir_door(player, 'Sewers Dark Cross South Stairs', DoorType.StraightStairs, Direction.South, 0x32, Mid, High),
        create_dir_door(player, 'Sewers Dark Cross Key Door N', DoorType.Normal, Direction.North, 0x32, Mid, High),
        create_dir_door(player, 'Sewers Dark Cross Key Door S', DoorType.Normal, Direction.South, 0x22, Mid, High),
        create_dir_door(player, 'Sewers Water W', DoorType.Normal, Direction.West, 0x22, Bot, High),
        create_dir_door(player, 'Sewers Key Rat E', DoorType.Normal, Direction.East, 0x21, Bot, High),
        create_small_key_door(player, 'Sewers Key Rat Key Door N', DoorType.Normal, Direction.North, 0x21, Right, High),
        create_small_key_door(player, 'Sewers Secret Room Key Door S', DoorType.Normal, Direction.South, 0x11, Right, High),
        create_door(player, 'Sewers Secret Room Up Stairs', DoorType.SpiralStairs),
        create_door(player, 'Sewers Pull Switch Down Stairs', DoorType.SpiralStairs),
        create_toggle_door(player, 'Sewers Pull Switch S', DoorType.Normal, Direction.South, 0x02, Mid, Low),
        # logically one way the sanc, but should be linked - also toggle
        create_blocked_door(player, 'Sanctuary N', DoorType.Normal, Direction.North, 0x12, Mid, 0, True),

        # Eastern Palace
        create_dir_door(player, 'Eastern Lobby N', DoorType.Normal, Direction.North, 0xc9, Mid, High),
        create_dir_door(player, 'Eastern Cannonball S', DoorType.Normal, Direction.South, 0xb9, Mid, High),
        create_dir_door(player, 'Eastern Cannonball N', DoorType.Normal, Direction.North, 0xb9, Mid, High),
        create_dir_door(player, 'Eastern Cannonball Ledge WN', DoorType.Normal, Direction.West, 0xb9, Top, High),
        create_small_key_door(player, 'Eastern Cannonball Ledge Key Door EN', DoorType.Normal, Direction.East, 0xb9, Top, High),
        create_dir_door(player, 'Eastern Courtyard Ledge S', DoorType.Normal, Direction.South, 0xa9, Mid, High),
        create_dir_door(player, 'Eastern Courtyard Ledge W', DoorType.Normal, Direction.West, 0xa9, Mid, High),
        create_dir_door(player, 'Eastern Courtyard Ledge E', DoorType.Normal, Direction.East, 0xa9, Mid, High),
        create_dir_door(player, 'Eastern Map Area W', DoorType.Normal, Direction.West, 0xaa, Mid, High),
        create_dir_door(player, 'Eastern Compass Area E', DoorType.Normal, Direction.East, 0xa8, Mid, High),
        create_dir_door(player, 'Eastern Compass Area EN', DoorType.Normal, Direction.East, 0xa8, Top, Low),
        create_blocked_door(player, 'Eastern Compass Area SW', DoorType.Normal, Direction.South, 0xa8, Right, High),
        create_dir_door(player, 'Eastern Courtyard WN', DoorType.Normal, Direction.West, 0xa9, Top, Low),
        create_dir_door(player, 'Eastern Courtyard EN', DoorType.Normal, Direction.East, 0xa9, Top, Low),
        create_big_key_door(player, 'Eastern Courtyard N', DoorType.Normal, Direction.North, 0xa9, Mid, High),
        create_door(player, 'Eastern Courtyard Potholes', DoorType.Hole),
        create_door(player, 'Eastern Fairy Landing', DoorType.Hole),
        create_door(player, 'Eastern Fairies\' Warp', DoorType.Warp),
        create_door(player, 'Eastern Courtyard Warp End', DoorType.Warp),
        create_dir_door(player, 'Eastern Map Valley WN', DoorType.Normal, Direction.West, 0xaa, Top, Low),
        create_dir_door(player, 'Eastern Map Valley SW', DoorType.Normal, Direction.South, 0xaa, Left, High),
        create_small_key_door(player, 'Eastern Dark Square NW', DoorType.Normal, Direction.North, 0xba, Left, High),
        create_small_key_door(player, 'Eastern Dark Square Key Door WN', DoorType.Normal, Direction.West, 0xba, Top, High),
        create_small_key_door(player, 'Eastern Big Key EN', DoorType.Normal, Direction.East, 0xb8, Top, High),
        create_dir_door(player, 'Eastern Big Key NE', DoorType.Normal, Direction.North, 0xb8, Right, High),
        create_small_key_door(player, 'Eastern Darkness S', DoorType.Normal, Direction.South, 0x99, Mid, High),
        create_door(player, 'Eastern Darkness Up Stairs', DoorType.SpiralStairs),
        create_door(player, 'Eastern Attic Start Down Stairs', DoorType.SpiralStairs),
        create_dir_door(player, 'Eastern Attic Start WS', DoorType.Normal, Direction.West, 0xda, Bot, High),
        create_dir_door(player, 'Eastern Attic Switches ES', DoorType.Normal, Direction.East, 0xd9, Bot, High),
        create_dir_door(player, 'Eastern Attic Switches WS', DoorType.Normal, Direction.West, 0xd9, Bot, High),
        create_dir_door(player, 'Eastern Eyegores ES', DoorType.Normal, Direction.East, 0xd8, Bot, High),
        create_dir_door(player, 'Eastern Eyegores NE', DoorType.Normal, Direction.North, 0xd8, Right, High),
        create_dir_door(player, 'Eastern Boss SE', DoorType.Normal, Direction.South, 0xc8, Right, High),
    ]


def create_door(player, name, type):
    return Door(player, name, type, None, None, None, None)


def create_small_key_door(player, name, type, direction, room, doorIndex, layer):
    d = Door(player, name, type, direction, room, doorIndex, layer)
    d.smallKey = True
    return d


def create_big_key_door(player, name, type, direction, room, doorIndex, layer):
    d = Door(player, name, type, direction, room, doorIndex, layer)
    d.bigKey = True
    return d


def create_blocked_door(player, name, type, direction, room, doorIndex, layer, toggle=False):
    d = Door(player, name, type, direction, room, doorIndex, layer, toggle)
    d.blocked = True
    return d


def create_dir_door(player, name, type, direction, room, doorIndex, layer):
    return Door(player, name, type, direction, room, doorIndex, layer)


def create_toggle_door(player, name, type, direction, room, doorIndex, layer):
    return Door(player, name, type, direction, room, doorIndex, layer, True)
