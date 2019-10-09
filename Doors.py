
from BaseClasses import Door, DoorType, Direction
from RoomData import PairedDoor

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
        toggle(create_dir_door(player, 'Hyrule Castle Lobby W', DoorType.Normal, Direction.West, 0x61, Mid, High)).pos(0),
        toggle(create_dir_door(player, 'Hyrule Castle Lobby E', DoorType.Normal, Direction.East, 0x61, Mid, High)).pos(2),
        create_dir_door(player, 'Hyrule Castle Lobby WN', DoorType.Normal, Direction.West, 0x61, Top, High).pos(1),
        create_dir_door(player, 'Hyrule Castle Lobby North Stairs', DoorType.StraightStairs, Direction.North, 0x61, Mid, High),
        toggle(create_dir_door(player, 'Hyrule Castle West Lobby E', DoorType.Normal, Direction.East, 0x60, Mid, Low)).pos(1),
        create_dir_door(player, 'Hyrule Castle West Lobby N', DoorType.Normal, Direction.North, 0x60, Right, Low).pos(0),
        create_dir_door(player, 'Hyrule Castle West Lobby EN', DoorType.Normal, Direction.East, 0x60, Top, High).pos(3),
        toggle(create_dir_door(player, 'Hyrule Castle East Lobby W', DoorType.Normal, Direction.West, 0x62, Mid, Low)).pos(0),
        create_dir_door(player, 'Hyrule Castle East Lobby N', DoorType.Normal, Direction.North, 0x62, Mid, High).pos(3),
        create_dir_door(player, 'Hyrule Castle East Lobby NW', DoorType.Normal, Direction.North, 0x62, Left, Low).pos(2),
        create_dir_door(player, 'Hyrule Castle East Hall W', DoorType.Normal, Direction.West, 0x52, Top, Low).pos(0),
        create_dir_door(player, 'Hyrule Castle East Hall S', DoorType.Normal, Direction.South, 0x52, Mid, High).pos(2),
        create_dir_door(player, 'Hyrule Castle East Hall SW', DoorType.Normal, Direction.South, 0x52, Left, Low).pos(1),
        create_dir_door(player, 'Hyrule Castle West Hall E', DoorType.Normal, Direction.East, 0x50, Top, Low).pos(0),
        create_dir_door(player, 'Hyrule Castle West Hall S', DoorType.Normal, Direction.South, 0x50, Right, Low).pos(1),
        create_dir_door(player, 'Hyrule Castle Back Hall W', DoorType.Normal, Direction.West, 0x01, Top, Low).pos(0),
        create_dir_door(player, 'Hyrule Castle Back Hall E', DoorType.Normal, Direction.East, 0x01, Top, Low).pos(1),
        create_spiral_stairs(player, 'Hyrule Castle Back Hall Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x01, 0, HTL, A, 0x2a, 0x00),
        create_dir_door(player, 'Hyrule Castle Throne Room N', DoorType.Normal, Direction.North, 0x51, Mid, High).pos(1),
        create_dir_door(player, 'Hyrule Castle Throne Room South Stairs', DoorType.StraightStairs, Direction.South, 0x51, Mid, Low),

        # hyrule dungeon level
        create_spiral_stairs(player, 'Hyrule Dungeon Map Room Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x72, 0, LTH, A, 0x4b, 0xec),
        small_key(create_dir_door(player, 'Hyrule Dungeon Map Room Key Door S', DoorType.Interior, Direction.South, 0x72, Mid, High)).pos(0),
        small_key(create_dir_door(player, 'Hyrule Dungeon North Abyss Key Door N', DoorType.Interior, Direction.North, 0x72, Mid, High)).pos(0),
        create_dir_door(player, 'Hyrule Dungeon North Abyss South Edge', DoorType.Open, Direction.South, 0x72, None, Low),
        create_dir_door(player, 'Hyrule Dungeon North Abyss Catwalk Edge', DoorType.Open, Direction.South, 0x72, None, High),
        create_door(player, 'Hyrule Dungeon North Abyss Catwalk Dropdown', DoorType.Logical),
        create_dir_door(player, 'Hyrule Dungeon South Abyss North Edge', DoorType.Open, Direction.North, 0x82, None, Low),
        create_dir_door(player, 'Hyrule Dungeon South Abyss West Edge', DoorType.Open, Direction.West, 0x82, None, Low),
        create_dir_door(player, 'Hyrule Dungeon South Abyss Catwalk North Edge', DoorType.Open, Direction.North, 0x82, None, High),
        create_dir_door(player, 'Hyrule Dungeon South Abyss Catwalk West Edge', DoorType.Open, Direction.West, 0x82, None, High),
        create_dir_door(player, 'Hyrule Dungeon Guardroom Catwalk Edge', DoorType.Open, Direction.East, 0x81, None, High),
        create_dir_door(player, 'Hyrule Dungeon Guardroom Abyss Edge', DoorType.Open, Direction.West, 0x81, None, High),
        create_dir_door(player, 'Hyrule Dungeon Guardroom N', DoorType.Normal, Direction.North, 0x81, Left, Low).pos(0),
        trap(create_dir_door(player, 'Hyrule Dungeon Armory S', DoorType.Normal, Direction.South, 0x71, Left, Low), 0x2).pos(1),
        small_key(create_dir_door(player, 'Hyrule Dungeon Armory Interior Key Door N', DoorType.Interior, Direction.North, 0x71, Left, High)).pos(0),
        small_key(create_dir_door(player, 'Hyrule Dungeon Armory Interior Key Door S', DoorType.Interior, Direction.South, 0x71, Left, High)).pos(0),
        create_spiral_stairs(player, 'Hyrule Dungeon Armory Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x71, 0, HTL, A, 0x11, 0xa8, True),
        create_spiral_stairs(player, 'Hyrule Dungeon Staircase Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x70, 2, LTH, A, 0x32, 0x94, True),
        create_spiral_stairs(player, 'Hyrule Dungeon Staircase Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x70, 1, HTH, A, 0x11, 0x58),
        create_spiral_stairs(player, 'Hyrule Dungeon Cellblock Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x80, 0, HTH, A, 0x1a, 0x44),

        # sewers
        trap(blocked(create_dir_door(player, 'Sewers Behind Tapestry S', DoorType.Normal, Direction.South, 0x41, Mid, High)), 0x4).pos(0),
        create_spiral_stairs(player, 'Sewers Behind Tapestry Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x41, 0, HTH, S, 0x12, 0xb0),
        create_spiral_stairs(player, 'Sewers Rope Room Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x42, 0, HTH, S, 0x1b, 0x9c),
        create_dir_door(player, 'Sewers Rope Room North Stairs', DoorType.StraightStairs, Direction.North, 0x42, Mid, High),
        create_dir_door(player, 'Sewers Dark Cross South Stairs', DoorType.StraightStairs, Direction.South, 0x32, Mid, High),
        small_key(create_dir_door(player, 'Sewers Dark Cross Key Door N', DoorType.Normal, Direction.North, 0x32, Mid, High)).pos(0),
        small_key(create_dir_door(player, 'Sewers Dark Cross Key Door S', DoorType.Normal, Direction.South, 0x22, Mid, High)).pos(0),
        create_dir_door(player, 'Sewers Water W', DoorType.Normal, Direction.West, 0x22, Bot, High).pos(1),
        create_dir_door(player, 'Sewers Key Rat E', DoorType.Normal, Direction.East, 0x21, Bot, High).pos(1),
        small_key(create_dir_door(player, 'Sewers Key Rat Key Door N', DoorType.Normal, Direction.North, 0x21, Right, High)).pos(0),
        small_key(create_dir_door(player, 'Sewers Secret Room Key Door S', DoorType.Normal, Direction.South, 0x11, Right, High)).pos(2),
        create_door(player, 'Sewers Secret Room Push Block', DoorType.Logical),
        create_spiral_stairs(player, 'Sewers Secret Room Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x11, 0, LTH, S, 0x33, 0x6c, True),
        create_spiral_stairs(player, 'Sewers Pull Switch Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x02, 0, HTL, S, 0x12, 0x80),
        trap(toggle(create_dir_door(player, 'Sewers Pull Switch S', DoorType.Normal, Direction.South, 0x02, Mid, Low)), 0x4).pos(0),
        # logically one way the sanc, but should be linked - also toggle
        toggle(blocked(create_dir_door(player, 'Sanctuary N', DoorType.Normal, Direction.North, 0x12, Mid, High))).pos(0),

        # Eastern Palace
        create_dir_door(player, 'Eastern Lobby N', DoorType.Normal, Direction.North, 0xc9, Mid, High).pos(1),
        create_dir_door(player, 'Eastern Cannonball S', DoorType.Normal, Direction.South, 0xb9, Mid, High).pos(2),
        create_dir_door(player, 'Eastern Cannonball N', DoorType.Normal, Direction.North, 0xb9, Mid, High).pos(1),
        create_dir_door(player, 'Eastern Cannonball Ledge WN', DoorType.Normal, Direction.West, 0xb9, Top, High).pos(3),
        small_key(create_dir_door(player, 'Eastern Cannonball Ledge Key Door EN', DoorType.Normal, Direction.East, 0xb9, Top, High)).pos(0),
        create_dir_door(player, 'Eastern Courtyard Ledge S', DoorType.Normal, Direction.South, 0xa9, Mid, High).pos(5),
        trap(create_dir_door(player, 'Eastern Courtyard Ledge W', DoorType.Normal, Direction.West, 0xa9, Mid, High), 0x4).pos(0),
        trap(create_dir_door(player, 'Eastern Courtyard Ledge E', DoorType.Normal, Direction.East, 0xa9, Mid, High), 0x2).pos(1),
        create_dir_door(player, 'Eastern Map Area W', DoorType.Normal, Direction.West, 0xaa, Mid, High).pos(4),
        create_dir_door(player, 'Eastern Compass Area E', DoorType.Normal, Direction.East, 0xa8, Mid, High).pos(5),
        create_dir_door(player, 'Eastern Compass Area EN', DoorType.Normal, Direction.East, 0xa8, Top, Low).pos(4),
        ugly_door(small_key(create_dir_door(player, 'Eastern Compass Area SW', DoorType.Normal, Direction.South, 0xa8, Right, High))).pos(2),
        create_door(player, 'Eastern Hint Tile Push Block', DoorType.Logical),
        create_dir_door(player, 'Eastern Courtyard WN', DoorType.Normal, Direction.West, 0xa9, Top, Low).pos(3),
        create_dir_door(player, 'Eastern Courtyard EN', DoorType.Normal, Direction.East, 0xa9, Top, Low).pos(4),
        big_key(create_dir_door(player, 'Eastern Courtyard N', DoorType.Normal, Direction.North, 0xa9, Mid, High)).pos(2),
        create_door(player, 'Eastern Courtyard Potholes', DoorType.Hole),
        create_door(player, 'Eastern Fairies\' Warp', DoorType.Warp),
        create_dir_door(player, 'Eastern Map Valley WN', DoorType.Normal, Direction.West, 0xaa, Top, Low).pos(1),
        create_dir_door(player, 'Eastern Map Valley SW', DoorType.Normal, Direction.South, 0xaa, Left, High).pos(5),
        create_dir_door(player, 'Eastern Dark Square NW', DoorType.Normal, Direction.North, 0xba, Left, High).pos(1),
        small_key(create_dir_door(player, 'Eastern Dark Square Key Door WN', DoorType.Normal, Direction.West, 0xba, Top, High)).pos(0),
        create_dir_door(player, 'Eastern Big Key EN', DoorType.Normal, Direction.East, 0xb8, Top, High).pos(1),
        big_key(create_dir_door(player, 'Eastern Big Key NE', DoorType.Normal, Direction.North, 0xb8, Right, High)).pos(0),
        ugly_door(small_key(create_dir_door(player, 'Eastern Darkness S', DoorType.Normal, Direction.South, 0x99, Mid, High))).pos(1),
        # Up is a keydoor and down is not. Only the up stairs should be considered a key door for now.
        small_key(create_spiral_stairs(player, 'Eastern Darkness Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x99, 0, HTH, Z, 0x1a, 0x6c, False, True)).pos(0),
        ugly_door(create_spiral_stairs(player, 'Eastern Attic Start Down Stairs', DoorType.SpiralStairs, Direction.Down, 0xda, 0, HTH, Z, 0x11, 0x80, True, True)),
        create_dir_door(player, 'Eastern Attic Start WS', DoorType.Normal, Direction.West, 0xda, Bot, High).trap(0x4).pos(0),
        create_dir_door(player, 'Eastern Attic Switches ES', DoorType.Normal, Direction.East, 0xd9, Bot, High).trap(0x1).pos(2),
        create_dir_door(player, 'Eastern Attic Switches WS', DoorType.Normal, Direction.West, 0xd9, Bot, High).trap(0x4).pos(0),
        create_dir_door(player, 'Eastern Eyegores ES', DoorType.Normal, Direction.East, 0xd8, Bot, High).pos(2),
        create_dir_door(player, 'Eastern Eyegores NE', DoorType.Normal, Direction.North, 0xd8, Right, High).trap(0x4).pos(0),
        trap(blocked(create_dir_door(player, 'Eastern Boss SE', DoorType.Normal, Direction.South, 0xc8, Right, High)), 0x4).pos(0),

        # Desert Palace
        create_dir_door(player, 'Desert Main Lobby NW Edge', DoorType.Open, Direction.North, 0x84, None, High),
        create_dir_door(player, 'Desert Main Lobby N Edge', DoorType.Open, Direction.North, 0x84, None, High),
        create_dir_door(player, 'Desert Main Lobby NE Edge', DoorType.Open, Direction.North, 0x84, None, High),
        create_dir_door(player, 'Desert Main Lobby E Edge', DoorType.Open, Direction.East, 0x84, None, High),
        create_dir_door(player, 'Desert Dead End Edge', DoorType.Open, Direction.South, 0x74, None, High),
        create_dir_door(player, 'Desert East Wing W Edge', DoorType.Open, Direction.West, 0x85, None, High),
        create_dir_door(player, 'Desert East Wing N Edge', DoorType.Open, Direction.North, 0x85, None, High),
        create_dir_door(player, 'Desert East Lobby WS', DoorType.Interior, Direction.West, 0x85, Bot, High).pos(3),
        create_dir_door(player, 'Desert East Wing ES', DoorType.Interior, Direction.East, 0x85, Bot, High).pos(3),
        small_key(create_dir_door(player, 'Desert East Wing Key Door EN', DoorType.Interior, Direction.East, 0x85, Top, High)).pos(1),
        small_key(create_dir_door(player, 'Desert Compass Key Door WN', DoorType.Interior, Direction.West, 0x85, Top, High)).pos(1),
        trap(create_dir_door(player, 'Desert Compass NW', DoorType.Normal, Direction.North, 0x85, Left, High), 0x4).pos(0),
        create_dir_door(player, 'Desert Cannonball S', DoorType.Normal, Direction.South, 0x75, Left, High).pos(1),
        create_dir_door(player, 'Desert Arrow Pot Corner S Edge', DoorType.Open, Direction.South, 0x75, None, High),
        create_dir_door(player, 'Desert Arrow Pot Corner W Edge', DoorType.Open, Direction.West, 0x75, None, High),
        create_dir_door(player, 'Desert North Hall SE Edge', DoorType.Open, Direction.South, 0x74, None, High),
        create_dir_door(player, 'Desert North Hall SW Edge', DoorType.Open, Direction.South, 0x74, None, High),
        create_dir_door(player, 'Desert North Hall W Edge', DoorType.Open, Direction.West, 0x74, None, High),
        create_dir_door(player, 'Desert North Hall E Edge', DoorType.Open, Direction.East, 0x74, None, High),
        create_dir_door(player, 'Desert North Hall NW', DoorType.Interior, Direction.North, 0x74, Left, High).pos(1),
        create_dir_door(player, 'Desert Map SW', DoorType.Interior, Direction.South, 0x74, Left, High).pos(1),
        create_dir_door(player, 'Desert North Hall NE', DoorType.Interior, Direction.North, 0x74, Right, High).pos(0),
        create_dir_door(player, 'Desert Map SE', DoorType.Interior, Direction.South, 0x74, Right, High).pos(0),
        create_dir_door(player, 'Desert Sandworm Corner S Edge', DoorType.Open, Direction.South, 0x73, None, High),
        create_dir_door(player, 'Desert Sandworm Corner E Edge', DoorType.Open, Direction.East, 0x73, None, High),
        create_dir_door(player, 'Desert Sandworm Corner NE', DoorType.Interior, Direction.North, 0x73, Right, High).pos(2),
        create_dir_door(player, 'Desert Bonk Torch SE', DoorType.Interior, Direction.South, 0x73, Right, High).pos(2),
        create_dir_door(player, 'Desert Sandworm Corner WS', DoorType.Interior, Direction.West, 0x73, Bot, High).pos(1),
        # I don't know if I have to mark trap on interior doors yet - haven't mucked them up much
        create_dir_door(player, 'Desert Circle of Pots ES', DoorType.Interior, Direction.East, 0x73, Bot, High).pos(1),
        create_dir_door(player, 'Desert Circle of Pots NW', DoorType.Interior, Direction.North, 0x73, Left, High).pos(0),
        create_dir_door(player, 'Desert Big Chest SW', DoorType.Interior, Direction.South, 0x73, Left, High).pos(0),
        create_dir_door(player, 'Desert West Wing N Edge', DoorType.Open, Direction.North, 0x83, None, High),
        create_dir_door(player, 'Desert West Wing WS', DoorType.Interior, Direction.West, 0x83, Bot, High).pos(2),
        create_dir_door(player, 'Desert West Lobby ES', DoorType.Interior, Direction.East, 0x83, Bot, High).pos(2),
        # Desert Back
        create_dir_door(player, 'Desert Back Lobby NW', DoorType.Interior, Direction.North, 0x63, Left, High).pos(1),
        create_dir_door(player, 'Desert Tiles 1 SW', DoorType.Interior, Direction.South, 0x63, Left, High).pos(1),
        small_key(create_spiral_stairs(player, 'Desert Tiles 1 Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x63, 0, HTH, A, 0x1b, 0x6c, True)).pos(0),
        create_spiral_stairs(player, 'Desert Bridge Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x53, 0, HTH, A, 0x0f, 0x80, True),
        create_dir_door(player, 'Desert Bridge SW', DoorType.Interior, Direction.South, 0x53, Left, High).pos(0),
        create_dir_door(player, 'Desert Four Statues NW', DoorType.Interior, Direction.North, 0x53, Left, High).pos(0),
        create_dir_door(player, 'Desert Four Statues ES', DoorType.Interior, Direction.East, 0x53, Bot, High).pos(1),
        create_dir_door(player, 'Desert Beamos Hall WS', DoorType.Interior, Direction.West, 0x53, Bot, High).pos(1),
        small_key(create_dir_door(player, 'Desert Beamos Hall NE', DoorType.Normal, Direction.North, 0x53, Right, High)).pos(2),
        small_key(create_dir_door(player, 'Desert Tiles 2 SE', DoorType.Normal, Direction.South, 0x43, Right, High)).pos(2),
        create_dir_door(player, 'Desert Tiles 2 NE', DoorType.Interior, Direction.North, 0x43, Right, High).small_key().pos(1),
        create_dir_door(player, 'Desert Wall Slide SE', DoorType.Interior, Direction.South, 0x43, Right, High).small_key().pos(1),
        # todo: we need a new flag for a door that has a wall on it - you have to traverse it one particular way first
        # the above is not a problem until we get to crossed mode
        big_key(create_dir_door(player, 'Desert Wall Slide NW', DoorType.Normal, Direction.North, 0x43, Left, High)).pos(0),
        trap(blocked(create_dir_door(player, 'Desert Boss SW', DoorType.Normal, Direction.South, 0x33, Left, High)), 0x4).pos(0),

        # Hera
        create_spiral_stairs(player, 'Hera Lobby Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x77, 3, HTL, Z, 0x21, 0x90, False, True),
        small_key(create_spiral_stairs(player, 'Hera Lobby Key Stairs', DoorType.SpiralStairs, Direction.Down, 0x77, 1, HTL, A, 0x12, 0x80)).pos(0),
        create_spiral_stairs(player, 'Hera Lobby Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x77, 2, HTL, X, 0x2b, 0x5c, False, True),
        create_spiral_stairs(player, 'Hera Basement Cage Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x87, 3, LTH, Z, 0x42, 0x7c, True, True),
        create_spiral_stairs(player, 'Hera Tile Room Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x87, 1, LTH, A, 0x32, 0x6c, True, True),
        create_dir_door(player, 'Hera Tile Room EN', DoorType.Interior, Direction.East, 0x87, Top, High).pos(0),
        create_dir_door(player, 'Hera Tridorm WN', DoorType.Interior, Direction.West, 0x87, Top, High).pos(0),
        create_dir_door(player, 'Hera Tridorm SE', DoorType.Interior, Direction.South, 0x87, Right, High).pos(1),
        create_dir_door(player, 'Hera Torches NE', DoorType.Interior, Direction.North, 0x87, Right, High).pos(1),
        create_spiral_stairs(player, 'Hera Beetles Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x31, 2, LTH, X, 0x3a, 0x70, True, True),
        create_dir_door(player, 'Hera Beetles WS', DoorType.Interior, Direction.West, 0x31, Bot, High).pos(1),
        create_door(player, 'Hera Beetles Holes', DoorType.Hole),
        create_dir_door(player, 'Hera Startile Corner ES', DoorType.Interior, Direction.East, 0x31, Bot, High).pos(1),
        big_key(create_dir_door(player, 'Hera Startile Corner NW', DoorType.Interior, Direction.North, 0x31, Left, High)).pos(0),
        create_door(player, 'Hera Startile Corner Holes', DoorType.Hole),
        # technically ugly but causes lots of failures in basic
        create_dir_door(player, 'Hera Startile Wide SW', DoorType.Interior, Direction.South, 0x31, Left, High).pos(0),
        create_spiral_stairs(player, 'Hera Startile Wide Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x31, 0, HTH, S, 0x6b, 0xac, False, True),
        create_door(player, 'Hera Startile Wide Holes', DoorType.Hole),
        create_spiral_stairs(player, 'Hera 4F Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x27, 0, HTH, S, 0x62, 0xc0),
        create_spiral_stairs(player, 'Hera 4F Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x27, 1, HTH, A, 0x6b, 0x2c),
        create_door(player, 'Hera 4F Holes', DoorType.Hole),
        create_door(player, 'Hera Big Chest Landing Exit', DoorType.Logical),
        create_door(player, 'Hera Big Chest Landing Holes', DoorType.Hole),
        create_spiral_stairs(player, 'Hera 5F Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x17, 1, HTH, A, 0x62, 0x40),
        create_spiral_stairs(player, 'Hera 5F Up Stairs', DoorType.SpiralStairs, Direction.Up, 0x17, 0, HTH, S, 0x6a, 0x9c),
        create_door(player, 'Hera 5F Star Hole', DoorType.Hole),
        create_door(player, 'Hera 5F Pothole Chain', DoorType.Hole),
        create_door(player, 'Hera 5F Normal Holes', DoorType.Hole),
        create_door(player, 'Hera Fairies\' Warp', DoorType.Warp),
        create_spiral_stairs(player, 'Hera Boss Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x07, 0, HTH, S, 0x61, 0xb0),
        create_door(player, 'Hera Boss Outer Hole', DoorType.Hole),
        create_door(player, 'Hera Boss Inner Hole', DoorType.Hole),

        # Castle Tower
        create_dir_door(player, 'Tower Lobby NW', DoorType.Interior, Direction.North, 0xe0, Left, High).pos(1),
        create_dir_door(player, 'Tower Gold Knights SW', DoorType.Interior, Direction.South, 0xe0, Left, High).pos(1),
        create_dir_door(player, 'Tower Gold Knights EN', DoorType.Interior, Direction.East, 0xe0, Top, High).pos(0),
        create_dir_door(player, 'Tower Room 03 WN', DoorType.Interior, Direction.West, 0xe0, Bot, High).pos(0),
        create_spiral_stairs(player, 'Tower Room 03 Up Stairs', DoorType.SpiralStairs, Direction.Up, 0xe0, 0, HTH, S, 0x1a, 0x6c, True, True).small_key().pos(2),
        create_spiral_stairs(player, 'Tower Lone Statue Down Stairs', DoorType.SpiralStairs, Direction.Down, 0xd0, 0, HTH, S, 0x11, 0x80, True, True),
        create_dir_door(player, 'Tower Lone Statue WN', DoorType.Interior, Direction.West, 0xd0, Top, High).pos(1),
        create_dir_door(player, 'Tower Dark Maze EN', DoorType.Interior, Direction.East, 0xd0, Top, High).pos(1),
        create_dir_door(player, 'Tower Dark Maze ES', DoorType.Interior, Direction.East, 0xd0, Bot, High).small_key().pos(0),
        create_dir_door(player, 'Tower Dark Chargers WS', DoorType.Interior, Direction.West, 0xd0, Bot, High).small_key().pos(0),
        create_spiral_stairs(player, 'Tower Dark Chargers Up Stairs', DoorType.SpiralStairs, Direction.Up, 0xd0, 2, HTH, X, 0x1b, 0x8c, True, True),
        create_spiral_stairs(player, 'Tower Dual Statues Down Stairs', DoorType.SpiralStairs, Direction.Down, 0xc0, 2, HTH, X, 0x12, 0xa0, True, True),
        create_dir_door(player, 'Tower Dual Statues WS', DoorType.Interior, Direction.West, 0xc0, Bot, High).pos(1),
        create_dir_door(player, 'Tower Dark Pits ES', DoorType.Interior, Direction.East, 0xc0, Bot, High).pos(1),
        create_dir_door(player, 'Tower Dark Pits EN', DoorType.Interior, Direction.East, 0xc0, Top, High).pos(0),
        create_dir_door(player, 'Tower Dark Archers WN', DoorType.Interior, Direction.West, 0xc0, Top, High).pos(0),
        create_spiral_stairs(player, 'Tower Dark Archers Up Stairs', DoorType.SpiralStairs, Direction.Up, 0xc0, 0, HTH, S, 0x1b, 0x6c, True, True).small_key().pos(2),
        create_spiral_stairs(player, 'Tower Red Spears Down Stairs', DoorType.SpiralStairs, Direction.Down, 0xb0, 0, HTH, S, 0x12, 0x80, True, True),
        create_dir_door(player, 'Tower Red Spears WN', DoorType.Interior, Direction.West, 0xb0, Top, High).pos(1),
        create_dir_door(player, 'Tower Red Guards EN', DoorType.Interior, Direction.East, 0xb0, Top, High).pos(1),
        create_dir_door(player, 'Tower Red Guards SW', DoorType.Interior, Direction.South, 0xb0, Left, High).pos(0),
        create_dir_door(player, 'Tower Circle of Pots NW', DoorType.Interior, Direction.North, 0xb0, Left, High).pos(0),
        create_dir_door(player, 'Tower Circle of Pots WS', DoorType.Interior, Direction.West, 0xb0, Bot, High).small_key().pos(2),
        create_dir_door(player, 'Tower Pacifist Run ES', DoorType.Interior, Direction.East, 0xb0, Bot, High).small_key().pos(2),
        create_spiral_stairs(player, 'Tower Pacifist Run Up Stairs', DoorType.SpiralStairs, Direction.Up, 0xb0, 2, LTH, X, 0x33, 0x8c, True, True),
        create_spiral_stairs(player, 'Tower Push Statue Down Stairs', DoorType.SpiralStairs, Direction.Down, 0x40, 0, HTL, X, 0x12, 0xa0, True, True),
        create_dir_door(player, 'Tower Push Statue WS', DoorType.Interior, Direction.West, 0x40, Bot, Low).pos(0),
        create_dir_door(player, 'Tower Catwalk ES', DoorType.Interior, Direction.East, 0x40, Bot, Low).pos(0),
        create_dir_door(player, 'Tower Catwalk North Stairs', DoorType.StraightStairs, Direction.North, 0x40, Left, High),
        create_dir_door(player, 'Tower Antechamber South Stairs', DoorType.StraightStairs, Direction.South, 0x30, Left, High),
        create_dir_door(player, 'Tower Antechamber NW', DoorType.Interior, Direction.North, 0x30, Left, High).pos(1),
        create_dir_door(player, 'Tower Altar SW', DoorType.Interior, Direction.South, 0x30, Left, High).pos(1),
        create_dir_door(player, 'Tower Altar NW', DoorType.Normal, Direction.North, 0x30, Left, High).pos(0),
        create_dir_door(player, 'Tower Agahnim 1 SW', DoorType.Normal, Direction.South, 0x20, Left, High).no_exit().trap(0x4).pos(0),

        #Palace of Darkness
        create_door(player, 'PoD Lobby N', DoorType.Interior).dir(Direction.North, 0x4a, Mid, High).pos(2),
        create_door(player, 'PoD Lobby NW', DoorType.Interior).dir(Direction.North, 0x4a, Left, High).pos(0),
        create_door(player, 'PoD Lobby NE', DoorType.Interior).dir(Direction.North, 0x4a, Right, High).pos(1),
        create_door(player, 'PoD Left Cage SW', DoorType.Interior).dir(Direction.North, 0x4a, Left, High).pos(0),
        create_door(player, 'PoD Middle Cage S', DoorType.Interior).dir(Direction.North, 0x4a, Mid, High).pos(2),
        create_door(player, 'PoD Middle Cage SE', DoorType.Interior).dir(Direction.North, 0x4a, Right, High).pos(1),
        create_door(player, 'PoD Left Cage Down Stairs', DoorType.SpiralStairs).dir(Direction.Down, 0x4a, 1, HTH).ss(A, 0x12, 0x80, False, True),
        create_door(player, 'PoD Middle Cage Down Stairs', DoorType.SpiralStairs).dir(Direction.Down, 0x4a, 0, HTH).ss(S, 0x12, 0x80, False, True),
        create_door(player, 'PoD Middle Cage N', DoorType.Normal).dir(Direction.North, 0x4a, Mid, High).small_key().pos(2),
        create_door(player, 'PoD Shooter Room Up Stairs', DoorType.SpiralStairs).dir(Direction.Up, 0x09, 1, HTH).ss(A, 0x31, 0x69, True, True),
        create_door(player, 'PoD Warp Room Up Stairs', DoorType.SpiralStairs).dir(Direction.Up, 0x09, 0, HTH).ss(S, 0x30, 0x69, True, True),
        create_door(player, 'PoD Warp Room Warp', DoorType.Warp),
        create_door(player, 'PoD Pit Room S', DoorType.Normal).dir(Direction.South, 0x3a, Mid, High).small_key().pos(0),
        create_door(player, 'PoD Pit Room NW', DoorType.Normal).dir(Direction.North, 0x3a, Left, High).pos(1),
        create_door(player, 'PoD Pit Room NE', DoorType.Normal).dir(Direction.North, 0x3a, Right, High).pos(2),
        create_door(player, 'PoD Pit Room Freefall', DoorType.Hole),
        create_door(player, 'PoD Pit Room Bomb Hole', DoorType.Hole),
        create_door(player, 'PoD Big Key Landing Hole', DoorType.Hole),
        create_door(player, 'PoD Big Key Landing Down Stairs', DoorType.SpiralStairs).dir(Direction.Down, 0x3a, 0, HTH).ss(A, 0x11, 0x00),
        create_door(player, 'PoD Basement Ledge Up Stairs', DoorType.SpiralStairs).dir(Direction.Up, 0x0a, 0, HTH).ss(A, 0x1a, 0xec).small_key().pos(0),
        create_door(player, 'PoD Basement Ledge Drop Down', DoorType.Logical),
        create_door(player, 'PoD Stalfos Basement Warp', DoorType.Warp),
        create_door(player, 'PoD Arena Main SW', DoorType.Normal).dir(Direction.South, 0x2a, Left, High).pos(4),
        create_door(player, 'PoD Arena Bridge SE', DoorType.Normal).dir(Direction.South, 0x2a, Right, High).pos(5),
        create_door(player, 'PoD Arena Main NW', DoorType.Normal).dir(Direction.North, 0x2a, Left, High).small_key().pos(1),
        create_door(player, 'PoD Arena Main NE', DoorType.Normal).dir(Direction.North, 0x2a, Right, High).no_exit().trap(0x4).pos(0),
        create_door(player, 'PoD Arena Main Crystal Path', DoorType.Logical),
        create_door(player, 'PoD Arena Crystals E', DoorType.Normal).dir(Direction.East, 0x2a, Mid, High).pos(3),
        create_door(player, 'PoD Arena Crystal Path', DoorType.Logical),
        create_door(player, 'PoD Arena Bridge Drop Down', DoorType.Logical),
        create_door(player, 'PoD Arena Ledge ES', DoorType.Normal).dir(Direction.East, 0x2a, Bot, High).pos(2),
        create_door(player, 'PoD Sexy Statue W', DoorType.Normal).dir(Direction.West, 0x2b, Mid, High).pos(3),
        create_door(player, 'PoD Sexy Statue NW', DoorType.Normal).dir(Direction.North, 0x2b, Left, High).trap(0x1).pos(2),
        create_door(player, 'PoD Map Balcony Drop Down', DoorType.Logical),
        create_door(player, 'PoD Map Balcony WS', DoorType.Normal).dir(Direction.West, 0x2b, Bot, High).pos(1),
        create_door(player, 'PoD Map Balcony South Stairs', DoorType.StraightStairs).dir(Direction.South, 0x2b, Left, High),
        create_door(player, 'PoD Conveyor North Stairs', DoorType.StraightStairs).dir(Direction.North, 0x3b, Left, High),
        create_door(player, 'PoD Conveyor SW', DoorType.Normal).dir(Direction.South, 0x3b, Left, High).pos(0),
        create_door(player, 'PoD Mimics 1 NW', DoorType.Normal).dir(Direction.North, 0x4b, Left, High).trap(0x4).pos(0),
        create_door(player, 'PoD Mimics 1 SW', DoorType.Interior).dir(Direction.South, 0x4b, Left, High).pos(1),
        create_door(player, 'PoD Jelly Hall NW', DoorType.Interior).dir(Direction.North, 0x4b, Left, High).pos(1),
        create_door(player, 'PoD Jelly Hall NE', DoorType.Interior).dir(Direction.North, 0x4b, Right, High).pos(2),
        create_door(player, 'PoD Warp Hint SE', DoorType.Interior).dir(Direction.South, 0x4b, Right, High).pos(2),
        create_door(player, 'PoD Warp Hint Warp', DoorType.Warp),
        create_door(player, 'PoD Falling Bridge SW', DoorType.Normal).dir(Direction.South, 0x1a, Left, High).small_key().pos(3),
        create_door(player, 'PoD Falling Bridge WN', DoorType.Normal).dir(Direction.West, 0x1a, Top, High).small_key().pos(1),
        create_door(player, 'PoD Falling Bridge EN', DoorType.Interior).dir(Direction.East, 0x1a, Top, High).pos(4),
        create_door(player, 'PoD Big Chest Balcony W', DoorType.Normal).dir(Direction.West, 0x1a, Mid, High).pos(2),
        create_door(player, 'PoD Dark Maze EN', DoorType.Normal).dir(Direction.East, 0x19, Top, High).small_key().pos(1),
        create_door(player, 'PoD Dark Maze E', DoorType.Normal).dir(Direction.East, 0x19, Mid, High).pos(0),
        create_door(player, 'PoD Compass Room WN', DoorType.Interior).dir(Direction.West, 0x1a, Top, High).pos(4),
        create_door(player, 'PoD Compass Room SE', DoorType.Interior).dir(Direction.North, 0x1a, Mid, High).small_key().pos(0),
        create_door(player, 'PoD Harmless Hellway NE', DoorType.Interior).dir(Direction.North, 0x1a, Right, High).small_key().pos(0),
        create_door(player, 'PoD Harmless Hellway SE', DoorType.Normal).dir(Direction.South, 0x1a, Right, High).pos(5),
        create_door(player, 'PoD Compass Room W Down Stairs', DoorType.SpiralStairs).dir(Direction.Down, 0x1a, 0, HTH).ss(S, 0x12, 0x50, True, True),
        create_door(player, 'PoD Compass Room E Down Stairs', DoorType.SpiralStairs).dir(Direction.Down, 0x1a, 1, HTH).ss(S, 0x11, 0xb0, True, True),
        create_door(player, 'PoD Dark Basement W Up Stairs', DoorType.SpiralStairs).dir(Direction.Up, 0x6a, 0, HTH).ss(S, 0x1b, 0x3c, True),
        create_door(player, 'PoD Dark Basement E Up Stairs', DoorType.SpiralStairs).dir(Direction.Up, 0x6a, 1, HTH).ss(S, 0x1b, 0x9c, True),
        create_door(player, 'PoD Dark Alley NE', DoorType.Normal).dir(Direction.North, 0x6a, Right, High).big_key().pos(0),
        create_door(player, 'PoD Mimics 2 SW', DoorType.Normal).dir(Direction.South, 0x1b, Left, High).pos(1),
        create_door(player, 'PoD Mimics 2 NW', DoorType.Interior).dir(Direction.North, 0x1b, Left, High).pos(0),
        create_door(player, 'PoD Bow Statue SW', DoorType.Interior).dir(Direction.South, 0x1b, Left, High).pos(0),
        create_door(player, 'PoD Bow Statue Down Ladder', DoorType.Ladder),
        create_door(player, 'PoD Dark Pegs Up Ladder', DoorType.Ladder),
        create_door(player, 'PoD Dark Pegs WN', DoorType.Interior).dir(Direction.West, 0x0b, Mid, High).small_key().pos(2),
        create_door(player, 'PoD Lonely Turtle SW', DoorType.Interior).dir(Direction.South, 0x0b, Mid, High).pos(0),
        create_door(player, 'PoD Lonely Turtle EN', DoorType.Interior).dir(Direction.East, 0x0b, Mid, High).small_key().pos(2),
        create_door(player, 'PoD Turtle Party ES', DoorType.Interior).dir(Direction.East, 0x0b, Mid, High).pos(1),
        create_door(player, 'PoD Turtle Party NW', DoorType.Interior).dir(Direction.North, 0x0b, Mid, High).pos(0),
        create_door(player, 'PoD Callback WS', DoorType.Interior).dir(Direction.West, 0x0b, Mid, High).pos(1),
        create_door(player, 'PoD Callback Warp', DoorType.Warp),
        create_door(player, 'PoD Boss SE', DoorType.Normal).dir(Direction.South, 0x5a, Right, High).no_exit().trap(0x4).pos(0),
    ]
    create_paired_doors(world, player)


def create_paired_doors(world, player):
    world.paired_doors[player] = [
        PairedDoor('Sewers Secret Room Key Door S', 'Sewers Key Rat Key Door N'),
        # PairedDoor('', ''),  # TR Pokey Key
        # PairedDoor('', ''),  # TR Big key door by pipes
        PairedDoor('PoD Falling Bridge WN', 'PoD Dark Maze EN'),  # Pod Dark maze door
        PairedDoor('PoD Dark Maze E', 'PoD Big Chest Balcony W'),  # PoD Bombable by Big Chest
        PairedDoor('PoD Arena Main NW', 'PoD Falling Bridge SW'),  # Pod key door by bridge
        PairedDoor('Sewers Dark Cross Key Door N', 'Sewers Dark Cross Key Door S'),
        # PairedDoor('', ''),  # Swamp key door above big chest
        PairedDoor('PoD Map Balcony WS', 'PoD Arena Ledge ES'),  # Pod bombable by arena
        # PairedDoor('', ''),  # Swamp bombable to random pots
        # PairedDoor('', ''),  # Swamp bombable to map chest
        # PairedDoor('', ''),  # Swamp key door early room $38
        PairedDoor('PoD Middle Cage N', 'PoD Pit Room S'),
        # PairedDoor('', ''),  # GT moldorm key door
        # PairedDoor('', ''),  # Ice BJ key door
        PairedDoor('Desert Tiles 2 SE', 'Desert Beamos Hall NE'),
        # PairedDoor('', ''),  # Skull 3 key door
        # PairedDoor('', ''),  # Skull 1 key door - pot prison to big chest
        # PairedDoor('', ''),  # Skull 1 - pinball key door
        # PairedDoor('', ''),  # gt main big key door
        # PairedDoor('', ''),  # ice door to spike chest
        # PairedDoor('', ''),  # gt right side key door to cape bridge
        # PairedDoor('', ''),  # gt bombable to rando room
        # PairedDoor('', ''),  # ice's big icy room key door to lonely freezor
        PairedDoor('Eastern Courtyard N', 'Eastern Darkness S'),
        # PairedDoor('', ''),  # mire fishbone key door
        # PairedDoor('', ''),  # mire big key door to bridges
        PairedDoor('Eastern Big Key NE', 'Eastern Compass Area SW'),
        # PairedDoor('', ''),  # TR somaria hub to pokey
        PairedDoor('Eastern Dark Square Key Door WN', 'Eastern Cannonball Ledge Key Door EN'),
        # PairedDoor('', ''),  # TT random bomb to pots
        # PairedDoor('', ''),  # TT big key door
        # PairedDoor('', ''),  # Ice last key door to crystal switch
        # PairedDoor('', ''),  # mire hub key door to attic
        # PairedDoor('', ''),  # mire hub key door to map
        # PairedDoor('', ''),  # tr last key door to switch maze
        # PairedDoor('', '')  # TT dashable above
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
    door.trapFlag = trapFlag
    return door


def toggle(door):
    door.toggle = True
    return door


def blocked(door):
    door.blocked = True
    return door
