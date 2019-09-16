
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
# Quadrants - just been using this in my head - no reason to keep them labeled this way
A = 0
S = 1
Z = 2
X = 3
# Layer transitions
HTH = 0  # High to High 00
HTL = 1  # High to Low  01
LTH = 2  # Low to High  10
LTL = 3  # Low to Low   11


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
        create_spiral_stairs(player, 'Hyrule Castle Back Hall Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x01, 0, HTL, A, 0x2a, 0x00),
        create_dir_door(player, 'Hyrule Castle Throne Room N', DoorType.Normal, Direction.North, 0x51, Mid, High),
        create_dir_door(player, 'Hyrule Castle Throne Room South Stairs', DoorType.StraightStairs, Direction.South, 0x51, Mid, Low),

        # hyrule dungeon level
        create_spiral_stairs(player, 'Hyrule Dungeon Map Room Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x72, 0, LTH, A, 0x4b, 0xec),
        create_small_key_door(player, 'Hyrule Dungeon Map Room Key Door S', DoorType.Interior, Direction.South, 0x71, Right, High),
        create_small_key_door(player, 'Hyrule Dungeon North Abyss Key Door N', DoorType.Interior, Direction.North, 0x71, Right, High),
        create_dir_door(player, 'Hyrule Dungeon North Abyss South Edge', DoorType.Open, Direction.South, 0x72, None, Low),
        create_dir_door(player, 'Hyrule Dungeon North Abyss Catwalk Edge', DoorType.Open, Direction.South, 0x72, None, High),
        create_dir_door(player, 'Hyrule Dungeon South Abyss North Edge', DoorType.Open, Direction.North, 0x82, None, Low),
        create_dir_door(player, 'Hyrule Dungeon South Abyss West Edge', DoorType.Open, Direction.West, 0x82, None, Low),
        create_dir_door(player, 'Hyrule Dungeon South Abyss Catwalk North Edge', DoorType.Open, Direction.North, 0x82, None, High),
        create_dir_door(player, 'Hyrule Dungeon South Abyss Catwalk West Edge', DoorType.Open, Direction.West, 0x82, None, High),
        create_dir_door(player, 'Hyrule Dungeon Guardroom Catwalk Edge', DoorType.Open, Direction.East, 0x81, None, High),
        create_dir_door(player, 'Hyrule Dungeon Guardroom Abyss Edge', DoorType.Open, Direction.West, 0x81, None, High),
        create_dir_door(player, 'Hyrule Dungeon Guardroom N', DoorType.Normal, Direction.North, 0x81, Left, Low),
        create_dir_door(player, 'Hyrule Dungeon Armory S', DoorType.Normal, Direction.South, 0x71, Left, Low),
        create_small_key_door(player, 'Hyrule Dungeon Armory Interior Key Door N', DoorType.Interior, Direction.North, 0x71, Left, High),
        create_small_key_door(player, 'Hyrule Dungeon Armory Interior Key Door S', DoorType.Interior, Direction.South, 0x71, Left, High),
        create_spiral_stairs(player, 'Hyrule Dungeon Armory Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x71, 0, HTL, A, 0x11, 0xa8, True),
        create_spiral_stairs(player, 'Hyrule Dungeon Staircase Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x70, 2, LTH, A, 0x32, 0x94, True),
        create_spiral_stairs(player, 'Hyrule Dungeon Staircase Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x70, 1, HTH, A, 0x11, 0x58),
        create_spiral_stairs(player, 'Hyrule Dungeon Cellblock Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x80, 0, HTH, A, 0x1a, 0x44),

        # sewers
        create_blocked_door(player, 'Sewers Behind Tapestry S', DoorType.Normal, Direction.South, 0x41, Mid, High, False, False, 0x2),
        create_spiral_stairs(player, 'Sewers Behind Tapestry Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x41, 0, HTH, S, 0x12, 0xb0),
        create_spiral_stairs(player, 'Sewers Rope Room Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x42, 0, HTH, S, 0x1b, 0x9c),
        create_dir_door(player, 'Sewers Rope Room North Stairs', DoorType.StraightStairs, Direction.North, 0x42, Mid, High),
        create_dir_door(player, 'Sewers Dark Cross South Stairs', DoorType.StraightStairs, Direction.South, 0x32, Mid, High),
        create_small_key_door(player, 'Sewers Dark Cross Key Door N', DoorType.Normal, Direction.North, 0x32, Mid, High),
        create_small_key_door(player, 'Sewers Dark Cross Key Door S', DoorType.Normal, Direction.South, 0x22, Mid, High),
        create_dir_door(player, 'Sewers Water W', DoorType.Normal, Direction.West, 0x22, Bot, High),
        create_dir_door(player, 'Sewers Key Rat E', DoorType.Normal, Direction.East, 0x21, Bot, High),
        create_small_key_door(player, 'Sewers Key Rat Key Door N', DoorType.Normal, Direction.North, 0x21, Right, High),
        create_small_key_door(player, 'Sewers Secret Room Key Door S', DoorType.Normal, Direction.South, 0x11, Right, High),
        create_spiral_stairs(player, 'Sewers Secret Room Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x11, 0, LTH, S, 0x33, 0x6c, True),
        create_spiral_stairs(player, 'Sewers Pull Switch Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x02, 0, HTL, S, 0x12, 0x80),
        create_toggle_door(player, 'Sewers Pull Switch S', DoorType.Normal, Direction.South, 0x02, Mid, Low, 0x2),
        # logically one way the sanc, but should be linked - also toggle
        create_blocked_door(player, 'Sanctuary N', DoorType.Normal, Direction.North, 0x12, Mid, 0, True),

        # Eastern Palace
        create_dir_door(player, 'Eastern Lobby N', DoorType.Normal, Direction.North, 0xc9, Mid, High),
        create_dir_door(player, 'Eastern Cannonball S', DoorType.Normal, Direction.South, 0xb9, Mid, High),
        create_dir_door(player, 'Eastern Cannonball N', DoorType.Normal, Direction.North, 0xb9, Mid, High),
        create_dir_door(player, 'Eastern Cannonball Ledge WN', DoorType.Normal, Direction.West, 0xb9, Top, High),
        create_small_key_door(player, 'Eastern Cannonball Ledge Key Door EN', DoorType.Normal, Direction.East, 0xb9, Top, High),
        create_dir_door(player, 'Eastern Courtyard Ledge S', DoorType.Normal, Direction.South, 0xa9, Mid, High),
        create_dir_door(player, 'Eastern Courtyard Ledge W', DoorType.Normal, Direction.West, 0xa9, Mid, High, 0x2),
        create_dir_door(player, 'Eastern Courtyard Ledge E', DoorType.Normal, Direction.East, 0xa9, Mid, High, 0x1),
        create_dir_door(player, 'Eastern Map Area W', DoorType.Normal, Direction.West, 0xaa, Mid, High),
        create_dir_door(player, 'Eastern Compass Area E', DoorType.Normal, Direction.East, 0xa8, Mid, High),
        create_dir_door(player, 'Eastern Compass Area EN', DoorType.Normal, Direction.East, 0xa8, Top, Low),
        create_blocked_door(player, 'Eastern Compass Area SW', DoorType.Normal, Direction.South, 0xa8, Right, High, False, True),
        create_dir_door(player, 'Eastern Courtyard WN', DoorType.Normal, Direction.West, 0xa9, Top, Low),
        create_dir_door(player, 'Eastern Courtyard EN', DoorType.Normal, Direction.East, 0xa9, Top, Low),
        create_big_key_door(player, 'Eastern Courtyard N', DoorType.Normal, Direction.North, 0xa9, Mid, High),
        create_door(player, 'Eastern Courtyard Potholes', DoorType.Hole),
        create_door(player, 'Eastern Fairy Landing', DoorType.Hole),
        create_door(player, 'Eastern Fairies\' Warp', DoorType.Warp),
        create_door(player, 'Eastern Courtyard Warp End', DoorType.Warp),
        create_dir_door(player, 'Eastern Map Valley WN', DoorType.Normal, Direction.West, 0xaa, Top, Low),
        create_dir_door(player, 'Eastern Map Valley SW', DoorType.Normal, Direction.South, 0xaa, Left, High),
        create_dir_door(player, 'Eastern Dark Square NW', DoorType.Normal, Direction.North, 0xba, Left, High),
        create_small_key_door(player, 'Eastern Dark Square Key Door WN', DoorType.Normal, Direction.West, 0xba, Top, High),
        create_dir_door(player, 'Eastern Big Key EN', DoorType.Normal, Direction.East, 0xb8, Top, High),
        create_big_key_door(player, 'Eastern Big Key NE', DoorType.Normal, Direction.North, 0xb8, Right, High),
        ugly_door(create_small_key_door(player, 'Eastern Darkness S', DoorType.Normal, Direction.South, 0x99, Mid, High)),
        # TODO: Up is a keydoor and down is not. Are they both spiralkeys or what?
        create_spiral_stairs(player, 'Eastern Darkness Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x99, 0, HTH, Z, 0x1a, 0x6c, False, True),
        ugly_door(create_spiral_stairs(player, 'Eastern Attic Start Down Stairs', DoorType.SpiralStairs, Direction.Down, 0xda, 0, HTH, Z, 0x11, 0x80, False, True)),
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


def create_blocked_door(player, name, type, direction, room, doorIndex, layer, toggle=False, key=False, trap=0x0):
    d = Door(player, name, type, direction, room, doorIndex, layer, toggle)
    d.blocked = True
    d.smallKey = key
    d.trap = trap
    return d

def create_dir_door(player, name, type, direction, room, doorIndex, layer, trap=0x0):
    d = Door(player, name, type, direction, room, doorIndex, layer)
    d.trap = trap
    return d


def create_toggle_door(player, name, type, direction, room, doorIndex, layer, trap=0x0):
    d = Door(player, name, type, direction, room, doorIndex, layer, True)
    d.trap = trap
    return d


def create_spiral_stairs(player, name, type, direction, room,
                         door_index, layer, quadrant, shift_y, shift_x, zero_hz_cam=False, zero_vt_cam=False):
    d = Door(player, name, type, direction, room, door_index, layer)
    d.quadrant = quadrant
    d.shiftY = shift_y
    d.shiftX = shift_x
    d.zeroHzCam = zero_hz_cam
    d.zeroVtCam = zero_vt_cam
    return d

def ugly_door(door):
  door.ugly = True
  return door
