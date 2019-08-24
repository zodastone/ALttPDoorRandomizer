
from BaseClasses import Door, DoorType, Direction

# constants
Top = 0
Left = 0
Mid = 1
Bot = 2
Right = 2


def create_doors(world, player):
    world.doors += [
        # hyrule castle
        create_toggle_door(player, 'Hyrule Castle Lobby W', DoorType.Normal, Direction.West, 0x61, Mid, 0),
        create_toggle_door(player, 'Hyrule Castle Lobby E', DoorType.Normal, Direction.East, 0x61, Mid, 0),
        create_dir_door(player, 'Hyrule Castle Lobby WN', DoorType.Normal, Direction.West, 0x61, Top, 0),
        create_dir_door(player, 'Hyrule Castle Lobby North Stairs', DoorType.StraightStairs, Direction.North, 0x61, Mid, 0),
        create_toggle_door(player, 'Hyrule Castle West Lobby E', DoorType.Normal, Direction.East, 0x60, Mid, 1),
        create_dir_door(player, 'Hyrule Castle West Lobby N', DoorType.Normal, Direction.North, 0x60, Right, 1),
        create_dir_door(player, 'Hyrule Castle West Lobby EN', DoorType.Normal, Direction.East, 0x60, Top, 0),
        create_toggle_door(player, 'Hyrule Castle East Lobby W', DoorType.Normal, Direction.West, 0x62, Mid, 1),
        create_dir_door(player, 'Hyrule Castle East Lobby N', DoorType.Normal, Direction.North, 0x62, Mid, 0),
        create_dir_door(player, 'Hyrule Castle East Lobby NW', DoorType.Normal, Direction.North, 0x62, Left, 1),
        create_dir_door(player, 'Hyrule Castle East Hall W', DoorType.Normal, Direction.West, 0x52, Top, 1),
        create_dir_door(player, 'Hyrule Castle East Hall S', DoorType.Normal, Direction.South, 0x52, Mid, 1),
        create_dir_door(player, 'Hyrule Castle East Hall SW', DoorType.Normal, Direction.South, 0x52, Left, 1),
        create_dir_door(player, 'Hyrule Castle West Hall E', DoorType.Normal, Direction.East, 0x50, Top, 1),
        create_dir_door(player, 'Hyrule Castle West Hall S', DoorType.Normal, Direction.South, 0x50, Right, 1),
        create_dir_door(player, 'Hyrule Castle Back Hall W', DoorType.Normal, Direction.West, 0x01, Top, 1),
        create_dir_door(player, 'Hyrule Castle Back Hall E', DoorType.Normal, Direction.East, 0x01, Top, 1),
        create_door(player, 'Hyrule Castle Back Hall Down Stairs', DoorType.SpiralStairs),
        create_dir_door(player, 'Hyrule Castle Throne Room N', DoorType.Normal, Direction.North, 0x51, Mid, 0),
        create_dir_door(player, 'Hyrule Castle Throne Room South Stairs', DoorType.StraightStairs, Direction.South, 0x51, Mid, 1),

        # hyrule dungeon level
        create_door(player, 'Hyrule Dungeon Map Room Up Stairs', DoorType.SpiralStairs),
        create_dir_door(player, 'Hyrule Dungeon North Abyss South Edge', DoorType.Open, Direction.South, 0x72, None, 1),
        create_dir_door(player, 'Hyrule Dungeon North Abyss Catwalk Edge', DoorType.Open, Direction.South, 0x72, None, 0),
        create_dir_door(player, 'Hyrule Dungeon South Abyss North Edge', DoorType.Open, Direction.North, 0x82, None, 1),
        create_dir_door(player, 'Hyrule Dungeon South Abyss West Edge', DoorType.Open, Direction.West, 0x82, None, 1),
        create_dir_door(player, 'Hyrule Dungeon South Abyss Catwalk North Edge', DoorType.Open, Direction.North, 0x82, None, 0),
        create_dir_door(player, 'Hyrule Dungeon South Abyss Catwalk West Edge', DoorType.Open, Direction.West, 0x82, None, 0),
        create_dir_door(player, 'Hyrule Dungeon Guardroom Catwalk Edge', DoorType.Open, Direction.East, 0x81, None, 0),
        create_dir_door(player, 'Hyrule Dungeon Guardroom Abyss Edge', DoorType.Open, Direction.West, 0x81, None, 0),
        create_dir_door(player, 'Hyrule Dungeon Guardroom N', DoorType.Normal, Direction.North, 0x81, Left, 1), # todo: is this a toggle door?
        create_dir_door(player, 'Hyrule Dungeon Armory S', DoorType.Normal, Direction.South, 0x71, Left, 1), # not sure what the layer should be here
        create_door(player, 'Hyrule Dungeon Armory Down Stairs', DoorType.SpiralStairs),
        create_door(player, 'Hyrule Dungeon Staircase Up Stairs', DoorType.SpiralStairs),
        create_door(player, 'Hyrule Dungeon Staircase Down Stairs', DoorType.SpiralStairs),
        create_door(player, 'Hyrule Dungeon Cellblock Up Stairs', DoorType.SpiralStairs),

        # sewers
        create_blocked_door(player, 'Sewers Behind Tapestry S', DoorType.Normal, Direction.South, 0x41, Mid, 0),
        create_door(player, 'Sewers Behind Tapestry Down Stairs', DoorType.SpiralStairs),
        create_door(player, 'Sewers Rope Room Up Stairs', DoorType.SpiralStairs),
        create_dir_door(player, 'Sewers Rope Room North Stairs', DoorType.StraightStairs, Direction.North, 0x42, Mid, 0),
        create_dir_door(player, 'Sewers Dark Cross South Stairs', DoorType.StraightStairs, Direction.South, 0x32, Mid, 0),
        create_dir_door(player, 'Sewers Dark Cross Key Door N', DoorType.Normal, Direction.North, 0x32, Mid, 0),
        create_dir_door(player, 'Sewers Dark Cross Key Door S', DoorType.Normal, Direction.South, 0x22, Mid, 0),
        create_dir_door(player, 'Sewers Water W', DoorType.Normal, Direction.West, 0x22, Bot, 0),
        create_dir_door(player, 'Sewers Key Rat E', DoorType.Normal, Direction.East, 0x21, Bot, 0),
        create_small_key_door(player, 'Sewers Key Rat Key Door N', DoorType.Normal, Direction.North, 0x21, Right, 0),
        create_small_key_door(player, 'Sewers Secret Room Key Door S', DoorType.Normal, Direction.South, 0x11, Right, 0),
        create_door(player, 'Sewers Secret Room Up Stairs', DoorType.SpiralStairs),
        create_door(player, 'Sewers Pull Switch Down Stairs', DoorType.SpiralStairs),
        create_dir_door(player, 'Sewers Pull Switch S', DoorType.Normal, Direction.South, 0x02, Mid, 0),
        create_blocked_door(player, 'Sanctuary N', DoorType.Normal, Direction.North, 0x12, Mid, 0),  # logically one way, but should be linked

        # Eastern Palace
        create_dir_door(player, 'Eastern Lobby N', DoorType.Normal, Direction.North, 0xc9, Mid, 0),
        create_dir_door(player, 'Eastern Cannonball S', DoorType.Normal, Direction.South, 0xb9, Mid, 0),
        create_dir_door(player, 'Eastern Cannonball N', DoorType.Normal, Direction.North, 0xb9, Mid, 0),
        create_dir_door(player, 'Eastern Cannonball Ledge WN', DoorType.Normal, Direction.West, 0xb9, Top, 0),
        create_small_key_door(player, 'Eastern Cannonball Ledge Key Door EN', DoorType.Normal, Direction.East, 0xb9, Top, 0),
        create_dir_door(player, 'Eastern Courtyard Ledge S', DoorType.Normal, Direction.South, 0xa9, Mid, 0),
        create_dir_door(player, 'Eastern Courtyard Ledge W', DoorType.Normal, Direction.West, 0xa9, Mid, 0),
        create_dir_door(player, 'Eastern Courtyard Ledge E', DoorType.Normal, Direction.East, 0xa9, Mid, 0),
        create_dir_door(player, 'Eastern Map Area W', DoorType.Normal, Direction.West, 0xaa, Mid, 0),
        create_dir_door(player, 'Eastern Compass Area E', DoorType.Normal, Direction.East, 0xa8, Mid, 0),
        create_dir_door(player, 'Eastern Compass Area EN', DoorType.Normal, Direction.East, 0xa8, Top, 1),
        create_blocked_door(player, 'Eastern Compass Area SW', DoorType.Normal, Direction.South, 0xa8, Right, 0),
        create_dir_door(player, 'Eastern Courtyard WN', DoorType.Normal, Direction.West, 0xa9, Top, 1),
        create_dir_door(player, 'Eastern Courtyard EN', DoorType.Normal, Direction.East, 0xa9, Top, 1),
        create_big_key_door(player, 'Eastern Courtyard N', DoorType.Normal, Direction.North, 0xa9, Mid, 0),
        create_door(player, 'Eastern Courtyard Potholes', DoorType.Hole),
        create_door(player, 'Eastern Fairies\' Warp', DoorType.Warp),
        create_dir_door(player, 'Eastern Map Valley WN', DoorType.Normal, Direction.West, 0xaa, Top, 1),
        create_dir_door(player, 'Eastern Map Valley SW', DoorType.Normal, Direction.South, 0xaa, Left, 0),
        create_small_key_door(player, 'Eastern Dark Square NW', DoorType.Normal, Direction.North, 0xba, Left, 0),
        create_small_key_door(player, 'Eastern Dark Square Key Door WN', DoorType.Normal, Direction.West, 0xba, Top, 0),
        create_small_key_door(player, 'Eastern Big Key EN', DoorType.Normal, Direction.East, 0xb8, Top, 0),
        create_dir_door(player, 'Eastern Big Key NE', DoorType.Normal, Direction.North, 0xb8, Right, 0),
        create_small_key_door(player, 'Eastern Darkness S', DoorType.Normal, Direction.South, 0x99, Mid, 0),
        create_door(player, 'Eastern Darkness Up Stairs', DoorType.SpiralStairs),
        create_door(player, 'Eastern Attic Start Down Stairs', DoorType.SpiralStairs),
        create_dir_door(player, 'Eastern Attic Start WS', DoorType.Normal, Direction.West, 0xda, Bot, 0),
        create_dir_door(player, 'Eastern Attic Switches ES', DoorType.Normal, Direction.East, 0xd9, Bot, 0),
        create_dir_door(player, 'Eastern Attic Switches WS', DoorType.Normal, Direction.West, 0xd9, Bot, 0),
        create_dir_door(player, 'Eastern Eyegores ES', DoorType.Normal, Direction.East, 0xd8, Bot, 0),
        create_dir_door(player, 'Eastern Eyegores NE', DoorType.Normal, Direction.North, 0xd8, Right, 0),
        create_dir_door(player, 'Eastern Boss SE', DoorType.Normal, Direction.South, 0xc8, Right, 0),
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


def create_blocked_door(player, name, type, direction, room, doorIndex, layer):
    d = Door(player, name, type, direction, room, doorIndex, layer)
    d.blocked = True
    return d


def create_dir_door(player, name, type, direction, room, doorIndex, layer):
    return Door(player, name, type, direction, room, doorIndex, layer)


def create_toggle_door(player, name, type, direction, room, doorIndex, layer):
    return Door(player, name, type, direction, room, doorIndex, layer, True)
