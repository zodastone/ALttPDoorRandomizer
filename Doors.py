
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
        toggle(create_dir_door(player, 'Hyrule Castle Lobby W', DoorType.Normal, Direction.West, 0x61, Mid, High)),
        toggle(create_dir_door(player, 'Hyrule Castle Lobby E', DoorType.Normal, Direction.East, 0x61, Mid, High)),
        create_dir_door(player, 'Hyrule Castle Lobby WN', DoorType.Normal, Direction.West, 0x61, Top, High),
        create_dir_door(player, 'Hyrule Castle Lobby North Stairs', DoorType.StraightStairs, Direction.North, 0x61, Mid, High),
        toggle(create_dir_door(player, 'Hyrule Castle West Lobby E', DoorType.Normal, Direction.East, 0x60, Mid, Low)),
        create_dir_door(player, 'Hyrule Castle West Lobby N', DoorType.Normal, Direction.North, 0x60, Right, Low),
        create_dir_door(player, 'Hyrule Castle West Lobby EN', DoorType.Normal, Direction.East, 0x60, Top, High),
        toggle(create_dir_door(player, 'Hyrule Castle East Lobby W', DoorType.Normal, Direction.West, 0x62, Mid, Low)),
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
        small_key(create_dir_door(player, 'Hyrule Dungeon Map Room Key Door S', DoorType.Interior, Direction.South, 0x72, Mid, High)),
        small_key(create_dir_door(player, 'Hyrule Dungeon North Abyss Key Door N', DoorType.Interior, Direction.North, 0x72, Mid, High)),
        create_dir_door(player, 'Hyrule Dungeon North Abyss South Edge', DoorType.Open, Direction.South, 0x72, None, Low),
        create_dir_door(player, 'Hyrule Dungeon North Abyss Catwalk Edge', DoorType.Open, Direction.South, 0x72, None, High),
        create_door(player, 'Hyrule Dungeon North Abyss Catwalk Dropdown', DoorType.Logical),
        create_dir_door(player, 'Hyrule Dungeon South Abyss North Edge', DoorType.Open, Direction.North, 0x82, None, Low),
        create_dir_door(player, 'Hyrule Dungeon South Abyss West Edge', DoorType.Open, Direction.West, 0x82, None, Low),
        create_dir_door(player, 'Hyrule Dungeon South Abyss Catwalk North Edge', DoorType.Open, Direction.North, 0x82, None, High),
        create_dir_door(player, 'Hyrule Dungeon South Abyss Catwalk West Edge', DoorType.Open, Direction.West, 0x82, None, High),
        create_dir_door(player, 'Hyrule Dungeon Guardroom Catwalk Edge', DoorType.Open, Direction.East, 0x81, None, High),
        create_dir_door(player, 'Hyrule Dungeon Guardroom Abyss Edge', DoorType.Open, Direction.West, 0x81, None, High),
        create_dir_door(player, 'Hyrule Dungeon Guardroom N', DoorType.Normal, Direction.North, 0x81, Left, Low),
        trap(create_dir_door(player, 'Hyrule Dungeon Armory S', DoorType.Normal, Direction.South, 0x71, Left, Low), 0x1),
        small_key(create_dir_door(player, 'Hyrule Dungeon Armory Interior Key Door N', DoorType.Interior, Direction.North, 0x71, Left, High)),
        small_key(create_dir_door(player, 'Hyrule Dungeon Armory Interior Key Door S', DoorType.Interior, Direction.South, 0x71, Left, High)),
        create_spiral_stairs(player, 'Hyrule Dungeon Armory Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x71, 0, HTL, A, 0x11, 0xa8, True),
        create_spiral_stairs(player, 'Hyrule Dungeon Staircase Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x70, 2, LTH, A, 0x32, 0x94, True),
        create_spiral_stairs(player, 'Hyrule Dungeon Staircase Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x70, 1, HTH, A, 0x11, 0x58),
        create_spiral_stairs(player, 'Hyrule Dungeon Cellblock Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x80, 0, HTH, A, 0x1a, 0x44),

        # sewers
        trap(blocked(create_dir_door(player, 'Sewers Behind Tapestry S', DoorType.Normal, Direction.South, 0x41, Mid, High)), 0x2),
        create_spiral_stairs(player, 'Sewers Behind Tapestry Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x41, 0, HTH, S, 0x12, 0xb0),
        create_spiral_stairs(player, 'Sewers Rope Room Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x42, 0, HTH, S, 0x1b, 0x9c),
        create_dir_door(player, 'Sewers Rope Room North Stairs', DoorType.StraightStairs, Direction.North, 0x42, Mid, High),
        create_dir_door(player, 'Sewers Dark Cross South Stairs', DoorType.StraightStairs, Direction.South, 0x32, Mid, High),
        small_key(create_dir_door(player, 'Sewers Dark Cross Key Door N', DoorType.Normal, Direction.North, 0x32, Mid, High)),
        small_key(create_dir_door(player, 'Sewers Dark Cross Key Door S', DoorType.Normal, Direction.South, 0x22, Mid, High)),
        create_dir_door(player, 'Sewers Water W', DoorType.Normal, Direction.West, 0x22, Bot, High),
        create_dir_door(player, 'Sewers Key Rat E', DoorType.Normal, Direction.East, 0x21, Bot, High),
        small_key(create_dir_door(player, 'Sewers Key Rat Key Door N', DoorType.Normal, Direction.North, 0x21, Right, High)),
        small_key(create_dir_door(player, 'Sewers Secret Room Key Door S', DoorType.Normal, Direction.South, 0x11, Right, High)),
        create_door(player, 'Sewers Secret Room Push Block', DoorType.Logical),
        create_spiral_stairs(player, 'Sewers Secret Room Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x11, 0, LTH, S, 0x33, 0x6c, True),
        create_spiral_stairs(player, 'Sewers Pull Switch Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x02, 0, HTL, S, 0x12, 0x80),
        trap(toggle(create_dir_door(player, 'Sewers Pull Switch S', DoorType.Normal, Direction.South, 0x02, Mid, Low)), 0x2),
        # logically one way the sanc, but should be linked - also toggle
        toggle(blocked(create_dir_door(player, 'Sanctuary N', DoorType.Normal, Direction.North, 0x12, Mid, High))),

        # Eastern Palace
        create_dir_door(player, 'Eastern Lobby N', DoorType.Normal, Direction.North, 0xc9, Mid, High),
        create_dir_door(player, 'Eastern Cannonball S', DoorType.Normal, Direction.South, 0xb9, Mid, High),
        create_dir_door(player, 'Eastern Cannonball N', DoorType.Normal, Direction.North, 0xb9, Mid, High),
        create_dir_door(player, 'Eastern Cannonball Ledge WN', DoorType.Normal, Direction.West, 0xb9, Top, High),
        small_key(create_dir_door(player, 'Eastern Cannonball Ledge Key Door EN', DoorType.Normal, Direction.East, 0xb9, Top, High)),
        create_dir_door(player, 'Eastern Courtyard Ledge S', DoorType.Normal, Direction.South, 0xa9, Mid, High),
        trap(create_dir_door(player, 'Eastern Courtyard Ledge W', DoorType.Normal, Direction.West, 0xa9, Mid, High), 0x2),
        trap(create_dir_door(player, 'Eastern Courtyard Ledge E', DoorType.Normal, Direction.East, 0xa9, Mid, High), 0x1),
        create_dir_door(player, 'Eastern Map Area W', DoorType.Normal, Direction.West, 0xaa, Mid, High),
        create_dir_door(player, 'Eastern Compass Area E', DoorType.Normal, Direction.East, 0xa8, Mid, High),
        create_dir_door(player, 'Eastern Compass Area EN', DoorType.Normal, Direction.East, 0xa8, Top, Low),
        ugly_door(small_key(create_dir_door(player, 'Eastern Compass Area SW', DoorType.Normal, Direction.South, 0xa8, Right, High))),
        create_door(player, 'Eastern Hint Tile Push Block', DoorType.Logical),
        create_dir_door(player, 'Eastern Courtyard WN', DoorType.Normal, Direction.West, 0xa9, Top, Low),
        create_dir_door(player, 'Eastern Courtyard EN', DoorType.Normal, Direction.East, 0xa9, Top, Low),
        big_key(create_dir_door(player, 'Eastern Courtyard N', DoorType.Normal, Direction.North, 0xa9, Mid, High)),
        create_door(player, 'Eastern Courtyard Potholes', DoorType.Hole),
        create_door(player, 'Eastern Fairies\' Warp', DoorType.Warp),
        create_dir_door(player, 'Eastern Map Valley WN', DoorType.Normal, Direction.West, 0xaa, Top, Low),
        create_dir_door(player, 'Eastern Map Valley SW', DoorType.Normal, Direction.South, 0xaa, Left, High),
        create_dir_door(player, 'Eastern Dark Square NW', DoorType.Normal, Direction.North, 0xba, Left, High),
        small_key(create_dir_door(player, 'Eastern Dark Square Key Door WN', DoorType.Normal, Direction.West, 0xba, Top, High)),
        create_dir_door(player, 'Eastern Big Key EN', DoorType.Normal, Direction.East, 0xb8, Top, High),
        big_key(create_dir_door(player, 'Eastern Big Key NE', DoorType.Normal, Direction.North, 0xb8, Right, High)),
        ugly_door(small_key(create_dir_door(player, 'Eastern Darkness S', DoorType.Normal, Direction.South, 0x99, Mid, High))),
        # Up is a keydoor and down is not. Only the up stairs should be considered a key door for now.
        # Todo: add key door?
        small_key(create_spiral_stairs(player, 'Eastern Darkness Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x99, 0, HTH, Z, 0x1a, 0x6c, False, True)),
        ugly_door(create_spiral_stairs(player, 'Eastern Attic Start Down Stairs', DoorType.SpiralStairs, Direction.Down, 0xda, 0, HTH, Z, 0x11, 0x80, False, True)),
        create_dir_door(player, 'Eastern Attic Start WS', DoorType.Normal, Direction.West, 0xda, Bot, High),
        create_dir_door(player, 'Eastern Attic Switches ES', DoorType.Normal, Direction.East, 0xd9, Bot, High),
        create_dir_door(player, 'Eastern Attic Switches WS', DoorType.Normal, Direction.West, 0xd9, Bot, High),
        create_dir_door(player, 'Eastern Eyegores ES', DoorType.Normal, Direction.East, 0xd8, Bot, High),
        create_dir_door(player, 'Eastern Eyegores NE', DoorType.Normal, Direction.North, 0xd8, Right, High),
        trap(blocked(create_dir_door(player, 'Eastern Boss SE', DoorType.Normal, Direction.South, 0xc8, Right, High)), 0x2),

        # Desert Palace
        create_dir_door(player, 'Desert Main Lobby NW Edge', DoorType.Open, Direction.North, 0x84, None, High),
        create_dir_door(player, 'Desert Main Lobby N Edge', DoorType.Open, Direction.North, 0x84, None, High),
        create_dir_door(player, 'Desert Main Lobby NE Edge', DoorType.Open, Direction.North, 0x84, None, High),
        create_dir_door(player, 'Desert Main Lobby E Edge', DoorType.Open, Direction.East, 0x84, None, High),
        create_dir_door(player, 'Desert Dead End Edge', DoorType.Open, Direction.South, 0x74, None, High),
        create_dir_door(player, 'Desert East Wing W Edge', DoorType.Open, Direction.West, 0x85, None, High),
        create_dir_door(player, 'Desert East Wing N Edge', DoorType.Open, Direction.North, 0x85, None, High),
        create_dir_door(player, 'Desert East Lobby WS', DoorType.Interior, Direction.West, 0x85, Bot, High),
        create_dir_door(player, 'Desert East Wing ES', DoorType.Interior, Direction.East, 0x85, Bot, High),
        small_key(create_dir_door(player, 'Desert East Wing Key Door EN', DoorType.Interior, Direction.East, 0x85, Top, High)),
        small_key(create_dir_door(player, 'Desert Compass Key Door WN', DoorType.Interior, Direction.West, 0x85, Top, High)),
        trap(create_dir_door(player, 'Desert Compass NW', DoorType.Normal, Direction.North, 0x85, Left, High), 0x2),
        create_dir_door(player, 'Desert Cannonball S', DoorType.Normal, Direction.South, 0x75, Left, High),
        create_dir_door(player, 'Desert Arrow Pot Corner S Edge', DoorType.Open, Direction.South, 0x75, None, High),
        create_dir_door(player, 'Desert Arrow Pot Corner W Edge', DoorType.Open, Direction.West, 0x75, None, High),
        create_dir_door(player, 'Desert North Hall SE Edge', DoorType.Open, Direction.South, 0x74, None, High),
        create_dir_door(player, 'Desert North Hall SW Edge', DoorType.Open, Direction.South, 0x74, None, High),
        create_dir_door(player, 'Desert North Hall W Edge', DoorType.Open, Direction.West, 0x74, None, High),
        create_dir_door(player, 'Desert North Hall E Edge', DoorType.Open, Direction.East, 0x74, None, High),
        create_dir_door(player, 'Desert North Hall NW', DoorType.Interior, Direction.North, 0x74, Left, High),
        create_dir_door(player, 'Desert Map SW', DoorType.Interior, Direction.South, 0x74, Left, High),
        create_dir_door(player, 'Desert North Hall NE', DoorType.Interior, Direction.North, 0x74, Right, High),
        create_dir_door(player, 'Desert Map SE', DoorType.Interior, Direction.South, 0x74, Right, High),
        create_dir_door(player, 'Desert Sandworm Corner S Edge', DoorType.Open, Direction.South, 0x73, None, High),
        create_dir_door(player, 'Desert Sandworm Corner E Edge', DoorType.Open, Direction.East, 0x73, None, High),
        create_dir_door(player, 'Desert Sandworm Corner NE', DoorType.Interior, Direction.North, 0x73, Right, High),
        create_dir_door(player, 'Desert Bonk Torch SE', DoorType.Interior, Direction.South, 0x73, Right, High),
        create_dir_door(player, 'Desert Sandworm Corner WS', DoorType.Interior, Direction.West, 0x73, Bot, High),
        # I don't know if I have to mark trap on interior doors yet - haven't mucked them up much
        create_dir_door(player, 'Desert Circle of Pots ES', DoorType.Interior, Direction.East, 0x73, Bot, High),
        create_dir_door(player, 'Desert Circle of Pots NW', DoorType.Interior, Direction.North, 0x73, Left, High),
        create_dir_door(player, 'Desert Big Chest SW', DoorType.Interior, Direction.South, 0x73, Left, High),
        create_dir_door(player, 'Desert West Wing N Edge', DoorType.Open, Direction.North, 0x83, None, High),
        create_dir_door(player, 'Desert West Wing WS', DoorType.Interior, Direction.West, 0x83, Bot, High),
        create_dir_door(player, 'Desert West Lobby ES', DoorType.Interior, Direction.East, 0x83, Bot, High),
        # Desert Back
        create_dir_door(player, 'Desert Back Lobby NW', DoorType.Interior, Direction.North, 0x63, Left, High),
        create_dir_door(player, 'Desert Tiles 1 SW', DoorType.Interior, Direction.South, 0x63, Left, High),
        small_key(create_spiral_stairs(player, 'Desert Tiles 1 Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x63, 0, HTH, A, 0x1b, 0x6c, True)),
        create_spiral_stairs(player, 'Desert Bridge Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x53, 0, HTH, A, 0x0f, 0x80, True),
        create_dir_door(player, 'Desert Bridge SW', DoorType.Interior, Direction.South, 0x53, Left, High),
        create_dir_door(player, 'Desert Four Statues NW', DoorType.Interior, Direction.North, 0x53, Left, High),
        create_dir_door(player, 'Desert Four Statues ES', DoorType.Interior, Direction.East, 0x53, Bot, High),
        create_dir_door(player, 'Desert Beamos Hall WS', DoorType.Interior, Direction.West, 0x53, Bot, High),
        small_key(create_dir_door(player, 'Desert Beamos Hall NE', DoorType.Normal, Direction.North, 0x53, Right, High)),
        small_key(create_dir_door(player, 'Desert Tiles 2 SE', DoorType.Normal, Direction.South, 0x43, Right, High)),
        create_dir_door(player, 'Desert Tiles 2 NE', DoorType.Interior, Direction.North, 0x43, Right, High),
        create_dir_door(player, 'Desert Wall Slide SE', DoorType.Interior, Direction.South, 0x43, Right, High),
        # todo: we need a new flag for a door that has a wall on it - you have to traverse it one particular way first
        # the above is not a problem until we get to crossed mode
        big_key(create_dir_door(player, 'Desert Wall Slide NW', DoorType.Normal, Direction.North, 0x43, Left, High)),
        trap(blocked(create_dir_door(player, 'Desert Boss SW', DoorType.Normal, Direction.South, 0x33, Left, High)), 0x2),

        # Hera
        create_spiral_stairs(player, 'Hera Lobby Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x77, 0, HTL, Z, 0x21, 0x90),
        small_key(create_spiral_stairs(player, 'Hera Lobby Key Stairs', DoorType.SpiralStairs, Direction.Down, 0x77, 0, HTL, A, 0x12, 0x80)),
        create_spiral_stairs(player, 'Hera Lobby Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x77, 0, HTL, X, 0x2b, 0x5c),
        create_spiral_stairs(player, 'Hera Basement Cage Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x87, 0, LTH, Z, 0x42, 0x7c),
        create_spiral_stairs(player, 'Hera Tile Room Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x87, 0, LTH, A, 0x32, 0x6c),
        create_dir_door(player, 'Hera Tile Room EN', DoorType.Interior, Direction.East, 0x87, Top, High),
        create_dir_door(player, 'Hera Tridorm WN', DoorType.Interior, Direction.West, 0x87, Top, High),
        create_dir_door(player, 'Hera Tridorm SE', DoorType.Interior, Direction.South, 0x87, Right, High),
        create_dir_door(player, 'Hera Torches NE', DoorType.Interior, Direction.North, 0x87, Right, High),
        create_spiral_stairs(player, 'Hera Beetles Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x31, 0, LTH, X, 0x3a, 0x70),
        create_dir_door(player, 'Hera Beetles WS', DoorType.Interior, Direction.West, 0x31, Bot, High),
        create_door(player, 'Hera Beetles Holes', DoorType.Hole),
        create_dir_door(player, 'Hera Startile Corner ES', DoorType.Interior, Direction.East, 0x31, Bot, High),
        big_key(create_dir_door(player, 'Hera Startile Corner NW', DoorType.Interior, Direction.North, 0x31, Left, High)),
        create_door(player, 'Hera Startile Corner Holes', DoorType.Hole),
        # technically ugly but causes lots of failures in basic
        create_dir_door(player, 'Hera Startile Wide SW', DoorType.Interior, Direction.South, 0x31, Left, High),
        create_spiral_stairs(player, 'Hera Startile Wide Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x31, 0, HTH, S, 0x6b, 0xac),
        create_door(player, 'Hera Startile Wide Holes', DoorType.Hole),
        create_spiral_stairs(player, 'Hera 4F Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x27, 0, HTH, S, 0x62, 0xc0),
        create_spiral_stairs(player, 'Hera 4F Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x27, 0, HTH, A, 0x6b, 0x2c),
        create_door(player, 'Hera 4F Holes', DoorType.Hole),
        create_door(player, 'Hera Big Chest Landing Exit', DoorType.Logical),
        create_door(player, 'Hera Big Chest Landing Holes', DoorType.Hole),
        create_spiral_stairs(player, 'Hera 5F Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x17, 0, HTH, A, 0x62, 0x40),
        create_spiral_stairs(player, 'Hera 5F Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x17, 0, HTH, S, 0x6a, 0x9c),
        create_door(player, 'Hera 5F Star Hole', DoorType.Hole),
        create_door(player, 'Hera 5F Pothole Chain', DoorType.Hole),
        create_door(player, 'Hera 5F Normal Holes', DoorType.Hole),
        create_door(player, 'Hera Fairies\' Warp', DoorType.Warp),
        create_spiral_stairs(player, 'Hera Boss Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x07, 0, HTH, S, 0x61, 0xb0),
        create_door(player, 'Hera Boss Outer Hole', DoorType.Hole),
        create_door(player, 'Hera Boss Inner Hole', DoorType.Hole),

        # Castle Tower
        create_dir_door(player, 'Tower Lobby NW', DoorType.Interior, Direction.North, 0xe0, Left, High),
        create_dir_door(player, 'Tower Gold Knights SW', DoorType.Interior, Direction.South, 0xe0, Left, High),
        create_dir_door(player, 'Tower Gold Knights EN', DoorType.Interior, Direction.East, 0xe0, Top, High),
        create_dir_door(player, 'Tower Room 03 WN', DoorType.Interior, Direction.West, 0xe0, Bot, High),
        small_key(create_spiral_stairs(player, 'Tower Room 03 Up Stairs', DoorType.SpiralStairs, Direction.Up, 0xe0, 0, HTH, S, 0x1a, 0x6c)),
        create_spiral_stairs(player, 'Tower Lone Statue Down Stairs', DoorType.SpiralStairs, Direction.Down, 0xd0, 0, HTH, S, 0x11, 0x80),
        create_dir_door(player, 'Tower Lone Statue WN', DoorType.Interior, Direction.West, 0xd0, Top, High),
        create_dir_door(player, 'Tower Dark Maze EN', DoorType.Interior, Direction.East, 0xd0, Top, High),
        small_key(create_dir_door(player, 'Tower Dark Maze ES', DoorType.Interior, Direction.East, 0xd0, Bot, High)),
        small_key(create_dir_door(player, 'Tower Dark Chargers WS', DoorType.Interior, Direction.West, 0xd0, Bot, High)),
        create_spiral_stairs(player, 'Tower Dark Chargers Up Stairs', DoorType.SpiralStairs, Direction.Up, 0xd0, 0, HTH, X, 0x1b, 0x8c),
        create_spiral_stairs(player, 'Tower Dual Statues Down Stairs', DoorType.SpiralStairs, Direction.Down, 0xc0, 0, HTH, X, 0x12, 0xa0),
        create_dir_door(player, 'Tower Dual Statues WS', DoorType.Interior, Direction.West, 0xc0, Bot, High),
        create_dir_door(player, 'Tower Dark Pits ES', DoorType.Interior, Direction.East, 0xc0, Bot, High),
        create_dir_door(player, 'Tower Dark Pits EN', DoorType.Interior, Direction.East, 0xc0, Top, High),
        create_dir_door(player, 'Tower Dark Archers WS', DoorType.Interior, Direction.West, 0xc0, Top, High),
        small_key(create_spiral_stairs(player, 'Tower Dark Archers Up Stairs', DoorType.SpiralStairs, Direction.Up, 0xc0, 0, HTH, S, 0x1b, 0x6c)),
        create_spiral_stairs(player, 'Tower Red Spears Down Stairs', DoorType.SpiralStairs, Direction.Down, 0xb0, 0, HTH, S, 0x12, 0x80),
        create_dir_door(player, 'Tower Red Spears WN', DoorType.Interior, Direction.West, 0xb0, Top, High),
        create_dir_door(player, 'Tower Red Guards EN', DoorType.Interior, Direction.East, 0xb0, Top, High),
        create_dir_door(player, 'Tower Red Guards SW', DoorType.Interior, Direction.South, 0xb0, Left, High),
        create_dir_door(player, 'Tower Circle of Pots NW', DoorType.Interior, Direction.North, 0xb0, Left, High),
        small_key(create_dir_door(player, 'Tower Circle of Pots WS', DoorType.Interior, Direction.West, 0xb0, Bot, High)),
        small_key(create_dir_door(player, 'Tower Pacifist Run ES', DoorType.Interior, Direction.East, 0xb0, Bot, High)),
        create_spiral_stairs(player, 'Tower Pacifist Run Up Stairs', DoorType.SpiralStairs, Direction.Up, 0xb0, 0, LTH, S, 0x33, 0x8c),
        create_spiral_stairs(player, 'Tower Push Statue Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x40, 0, HTL, X, 0x12, 0xa0),
        create_dir_door(player, 'Tower Push Statue WS', DoorType.Interior, Direction.West, 0x40, Bot, Low),
        create_dir_door(player, 'Tower Catwalk ES', DoorType.Interior, Direction.East, 0x40, Bot, Low),
        create_dir_door(player, 'Tower Catwalk North Stairs', DoorType.StraightStairs, Direction.North, 0x40, Left, High),
        create_dir_door(player, 'Tower Antechamber South Stairs', DoorType.StraightStairs, Direction.South, 0x30, Left, High),
        create_dir_door(player, 'Tower Antechamber NW', DoorType.Interior, Direction.North, 0x30, Left, High),
        create_dir_door(player, 'Tower Altar SW', DoorType.Interior, Direction.South, 0x30, Left, High),
        create_dir_door(player, 'Tower Altar NW', DoorType.Normal, Direction.North, 0x30, Left, High),
        trap(blocked(create_dir_door(player, 'Tower Agahnim 1 SW', DoorType.Normal, Direction.South, 0x20, Left, High)), 0x2),
    ]


def create_door(player, name, type):
    return Door(player, name, type, None, None, None, None)


def create_dir_door(player, name, type, direction, room, doorIndex, layer):
    d = Door(player, name, type, direction, room, doorIndex, layer)
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


def small_key(door):
    door.smallKey = True
    return door


def big_key(door):
    door.bigKey = True
    return door


def trap(door, trapFlag):
    door.trap = trapFlag
    return door


def toggle(door):
    door.toggle = True
    return door


def blocked(door):
    door.blocked = True
    return door
