
from BaseClasses import Door, DoorType, Direction

def create_doors(world, player):
    world.doors += [
        # hyrule castle
        create_door(player, 'Hyrule Castle Lobby W', DoorType.Normal, Direction.West),
        create_door(player, 'Hyrule Castle Lobby E', DoorType.Normal, Direction.East),
        create_door(player, 'Hyrule Castle Lobby WN', DoorType.Normal, Direction.West),
        create_door(player, 'Hyrule Castle Lobby North Stairs', DoorType.StraightStairs, Direction.North),
        create_door(player, 'Hyrule Castle West Lobby E', DoorType.Normal, Direction.East),
        create_door(player, 'Hyrule Castle West Lobby N', DoorType.Normal, Direction.North),
        create_door(player, 'Hyrule Castle West Lobby EN', DoorType.Normal, Direction.East),
        create_door(player, 'Hyrule Castle East Lobby W', DoorType.Normal, Direction.West),
        create_door(player, 'Hyrule Castle East Lobby N', DoorType.Normal, Direction.North),
        create_door(player, 'Hyrule Castle East Lobby NE', DoorType.Normal, Direction.North),
        create_door(player, 'Hyrule Castle East Hall W', DoorType.Normal, Direction.West),
        create_door(player, 'Hyrule Castle East Hall S', DoorType.Normal, Direction.South),
        create_door(player, 'Hyrule Castle East Hall SE', DoorType.Normal, Direction.South),
        create_door(player, 'Hyrule Castle West Hall E', DoorType.Normal, Direction.East),
        create_door(player, 'Hyrule Castle West Hall S', DoorType.Normal, Direction.South),
        create_door(player, 'Hyrule Castle Back Hall W', DoorType.Normal, Direction.West),
        create_door(player, 'Hyrule Castle Back Hall E', DoorType.Normal, Direction.East),
        create_door(player, 'Hyrule Castle Back Hall Down Stairs', DoorType.SpiralStairs, None),
        create_door(player, 'Hyrule Castle Throne Room N', DoorType.Normal, Direction.North),
        create_door(player, 'Hyrule Castle Throne Room South Stairs', DoorType.StraightStairs, Direction.South),

        # hyrule dungeon level
        create_door(player, 'Hyrule Dungeon Map Room Up Stairs', DoorType.SpiralStairs, None),
        create_door(player, 'Hyrule Dungeon North Abyss South Edge', DoorType.Open, Direction.South),
        create_door(player, 'Hyrule Dungeon North Abyss Catwalk Edge', DoorType.Open, Direction.South),
        create_door(player, 'Hyrule Dungeon South Abyss North Edge', DoorType.Open, Direction.North),
        create_door(player, 'Hyrule Dungeon South Abyss West Edge', DoorType.Open, Direction.West),
        create_door(player, 'Hyrule Dungeon South Abyss Catwalk North Edge', DoorType.Open, Direction.North),
        create_door(player, 'Hyrule Dungeon South Abyss Catwalk West Edge', DoorType.Open, Direction.West),
        create_door(player, 'Hyrule Dungeon Guardroom Catwalk Edge', DoorType.Open, Direction.East),
        create_door(player, 'Hyrule Dungeon Guardroom Abyss Edge', DoorType.Open, Direction.West),
        create_door(player, 'Hyrule Dungeon Guardroom N', DoorType.Normal, Direction.North),
        create_door(player, 'Hyrule Dungeon Armory S', DoorType.Normal, Direction.South),
        create_door(player, 'Hyrule Dungeon Armory Down Stairs', DoorType.SpiralStairs, None),
        create_door(player, 'Hyrule Dungeon Staircase Up Stairs', DoorType.SpiralStairs, None),
        create_door(player, 'Hyrule Dungeon Staircase Down Stair', DoorType.SpiralStairs, None),
        create_door(player, 'Hyrule Dungeon Cellblock Up Stairs', DoorType.SpiralStairs, None),

        # sewers
        create_door(player, 'Sewers Behind Tapestry S', DoorType.Normal, Direction.South),  # one-way, this door is locked
        create_door(player, 'Sewers Behind Tapestry Down Stairs', DoorType.SpiralStairs, None),
        create_door(player, 'Sewers Rope Room Up Stairs', DoorType.SpiralStairs, None),
        create_door(player, 'Sewers Rope Room North Stairs', DoorType.StraightStairs, Direction.North),
        create_door(player, 'Sewers Dark Cross South Stairs', DoorType.StraightStairs, Direction.South),
        create_door(player, 'Sewers Dark Cross Key Door N', DoorType.Normal, Direction.North),
        create_door(player, 'Sewers Dark Cross Key Door S', DoorType.Normal, Direction.South),
        create_door(player, 'Sewers Water W', DoorType.Normal, Direction.West),
        create_door(player, 'Sewers Key Rat E', DoorType.Normal, Direction.East),
        create_door(player, 'Sewers Key Rat Key Door N', DoorType.Normal, Direction.North),
        create_door(player, 'Sewers Secret Room Key Door S', DoorType.Normal, Direction.South),
        create_door(player, 'Sewers Secret Room Up Stairs', DoorType.SpiralStairs, None),
        create_door(player, 'Sewers Pull Switch Down Stairs', DoorType.SpiralStairs, None),
        create_door(player, 'Sewers Pull Switch S', DoorType.Normal, Direction.South),
        create_door(player, 'Sanctuary N', DoorType.Normal, Direction.North),  # logically one way, but should be linked

        # Eastern Palace
        create_door(player, 'Eastern Lobby N', DoorType.Normal, Direction.North),
        create_door(player, 'Eastern Cannonball S', DoorType.Normal, Direction.South),
        create_door(player, 'Eastern Cannonball N', DoorType.Normal, Direction.North),
        create_door(player, 'Eastern Cannonball Ledge WN', DoorType.Normal, Direction.West),
        create_door(player, 'Eastern Cannonball Ledge Key Door EN', DoorType.Normal, Direction.East),
        create_door(player, 'Eastern Courtyard Ledge S', DoorType.Normal, Direction.South),
        create_door(player, 'Eastern Courtyard Ledge W', DoorType.Normal, Direction.West),
        create_door(player, 'Eastern Courtyard Ledge E', DoorType.Normal, Direction.East),
        create_door(player, 'Eastern Map Area W', DoorType.Normal, Direction.West),
        create_door(player, 'Eastern Compass Area E', DoorType.Normal, Direction.East),
        create_door(player, 'Eastern Compass Area EN', DoorType.Normal, Direction.East),
        create_door(player, 'Eastern Compass Area SW', DoorType.Normal, Direction.South),  # one-way
        create_door(player, 'Eastern Courtyard WN', DoorType.Normal, Direction.West),
        create_door(player, 'Eastern Courtyard EN', DoorType.Normal, Direction.East),
        create_door(player, 'Eastern Courtyard N', DoorType.Normal, Direction.North),  # big key
        create_door(player, 'Eastern Courtyard Potholes', DoorType.Hole, None),
        create_door(player, 'Eastern Fairies\' Warp', DoorType.Warp, None),
        create_door(player, 'Eastern Map Valley WN', DoorType.Normal, Direction.West),
        create_door(player, 'Eastern Map Valley SW', DoorType.Normal, Direction.South),
        create_door(player, 'Eastern Dark Square NW', DoorType.Normal, Direction.North),
        create_door(player, 'Eastern Dark Square Key Door WN', DoorType.Normal, Direction.West),
        create_door(player, 'Eastern Big Key EN', DoorType.Normal, Direction.East),
        create_door(player, 'Eastern Big Key NE', DoorType.Normal, Direction.North),
        create_door(player, 'Eastern Darkness S', DoorType.Normal, Direction.South),  # small key?
        create_door(player, 'Eastern Darkness Up Stairs', DoorType.SpiralStairs, None),
        create_door(player, 'Eastern Attic Start Down Stairs', DoorType.SpiralStairs, None),
        create_door(player, 'Eastern Attic Start WS', DoorType.Normal, Direction.West),
        create_door(player, 'Eastern Attic Switches ES', DoorType.Normal, Direction.East),
        create_door(player, 'Eastern Attic Switches WS', DoorType.Normal, Direction.West),
        create_door(player, 'Eastern Eyegores ES', DoorType.Normal, Direction.East),
        create_door(player, 'Eastern Eyegores NE', DoorType.Normal, Direction.North),
        create_door(player, 'Eastern Boss SE', DoorType.Normal, Direction.South),
    ]


def create_door(player, name, type, direction):
    return Door(player, name, type, direction)
