
from BaseClasses import Door, DoorType, Direction, CrystalBarrier
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
# Type Shortcuts
Nrml = DoorType.Normal
StrS = DoorType.StraightStairs
Hole = DoorType.Hole
Warp = DoorType.Warp
Sprl = DoorType.SpiralStairs
Lddr = DoorType.Ladder
Open = DoorType.Open
Lgcl = DoorType.Logical
Intr = DoorType.Interior


def create_doors(world, player):
    world.doors += [
        # hyrule castle
        create_door(player, 'Hyrule Castle Lobby W', Nrml).dir(Direction.West, 0x61, Mid, High).toggler().pos(0),
        create_door(player, 'Hyrule Castle Lobby E', Nrml).dir(Direction.East, 0x61, Mid, High).toggler().pos(2),
        create_door(player, 'Hyrule Castle Lobby WN', Nrml).dir(Direction.West, 0x61, Top, High).pos(1),
        create_door(player, 'Hyrule Castle Lobby North Stairs', StrS).dir(Direction.North, 0x61, Mid, High),
        create_door(player, 'Hyrule Castle West Lobby E', Nrml).dir(Direction.East, 0x60, Mid, Low).toggler().pos(1),
        create_door(player, 'Hyrule Castle West Lobby N', Nrml).dir(Direction.North, 0x60, Right, Low).pos(0),
        create_door(player, 'Hyrule Castle West Lobby EN', Nrml).dir(Direction.East, 0x60, Top, High).pos(3),
        create_door(player, 'Hyrule Castle East Lobby W', Nrml).dir(Direction.West, 0x62, Mid, Low).toggler().pos(0),
        create_door(player, 'Hyrule Castle East Lobby N', Nrml).dir(Direction.North, 0x62, Mid, High).pos(3),
        create_door(player, 'Hyrule Castle East Lobby NW', Nrml).dir(Direction.North, 0x62, Left, Low).pos(2),
        create_door(player, 'Hyrule Castle East Hall W', Nrml).dir(Direction.West, 0x52, Top, Low).pos(0),
        create_door(player, 'Hyrule Castle East Hall S', Nrml).dir(Direction.South, 0x52, Mid, High).pos(2),
        create_door(player, 'Hyrule Castle East Hall SW', Nrml).dir(Direction.South, 0x52, Left, Low).pos(1),
        create_door(player, 'Hyrule Castle West Hall E', Nrml).dir(Direction.East, 0x50, Top, Low).pos(0),
        create_door(player, 'Hyrule Castle West Hall S', Nrml).dir(Direction.South, 0x50, Right, Low).pos(1),
        create_door(player, 'Hyrule Castle Back Hall W', Nrml).dir(Direction.West, 0x01, Top, Low).pos(0),
        create_door(player, 'Hyrule Castle Back Hall E', Nrml).dir(Direction.East, 0x01, Top, Low).pos(1),
        create_door(player, 'Hyrule Castle Back Hall Down Stairs', Sprl).dir(Direction.Down, 0x01, 0, HTL).ss(A, 0x2a, 0x00),
        create_door(player, 'Hyrule Castle Throne Room N', Nrml).dir(Direction.North, 0x51, Mid, High).pos(1),
        create_door(player, 'Hyrule Castle Throne Room South Stairs', StrS).dir(Direction.South, 0x51, Mid, Low),

        # hyrule dungeon level
        create_door(player, 'Hyrule Dungeon Map Room Up Stairs', Sprl).dir(Direction.Up, 0x72, 0, LTH).ss(A, 0x4b, 0xec),
        create_door(player, 'Hyrule Dungeon Map Room Key Door S', Intr).dir(Direction.South, 0x72, Mid, High).small_key().pos(0),
        create_door(player, 'Hyrule Dungeon North Abyss Key Door N', Intr).dir(Direction.North, 0x72, Mid, High).small_key().pos(0),
        create_door(player, 'Hyrule Dungeon North Abyss South Edge', Open).dir(Direction.South, 0x72, None, Low),
        create_door(player, 'Hyrule Dungeon North Abyss Catwalk Edge', Open).dir(Direction.South, 0x72, None, High),
        create_door(player, 'Hyrule Dungeon North Abyss Catwalk Dropdown', Lgcl),
        create_door(player, 'Hyrule Dungeon South Abyss North Edge', Open).dir(Direction.North, 0x82, None, Low),
        create_door(player, 'Hyrule Dungeon South Abyss West Edge', Open).dir(Direction.West, 0x82, None, Low),
        create_door(player, 'Hyrule Dungeon South Abyss Catwalk North Edge', Open).dir(Direction.North, 0x82, None, High),
        create_door(player, 'Hyrule Dungeon South Abyss Catwalk West Edge', Open).dir(Direction.West, 0x82, None, High),
        create_door(player, 'Hyrule Dungeon Guardroom Catwalk Edge', Open).dir(Direction.East, 0x81, None, High),
        create_door(player, 'Hyrule Dungeon Guardroom Abyss Edge', Open).dir(Direction.West, 0x81, None, High),
        create_door(player, 'Hyrule Dungeon Guardroom N', Nrml).dir(Direction.North, 0x81, Left, Low).pos(0),
        create_door(player, 'Hyrule Dungeon Armory S', Nrml).dir(Direction.South, 0x71, Left, Low).trap(0x2).pos(1),
        create_door(player, 'Hyrule Dungeon Armory Interior Key Door N', Intr).dir(Direction.North, 0x71, Left, High).small_key().pos(0),
        create_door(player, 'Hyrule Dungeon Armory Interior Key Door S', Intr).dir(Direction.South, 0x71, Left, High).small_key().pos(0),
        create_door(player, 'Hyrule Dungeon Armory Down Stairs', Sprl).dir(Direction.Down, 0x71, 0, HTL).ss(A, 0x11, 0xa8, True),
        create_door(player, 'Hyrule Dungeon Staircase Up Stairs', Sprl).dir(Direction.Up, 0x70, 2, LTH).ss(A, 0x32, 0x94, True),
        create_door(player, 'Hyrule Dungeon Staircase Down Stairs', Sprl).dir(Direction.Down, 0x70, 1, HTH).ss(A, 0x11, 0x58),
        create_door(player, 'Hyrule Dungeon Cellblock Up Stairs', Sprl).dir(Direction.Up, 0x80, 0, HTH).ss(A, 0x1a, 0x44),

        # sewers
        create_door(player, 'Sewers Behind Tapestry S', Nrml).dir(Direction.South, 0x41, Mid, High).no_exit().trap(0x4).pos(0),
        create_door(player, 'Sewers Behind Tapestry Down Stairs', Sprl).dir(Direction.Down, 0x41, 0, HTH).ss(S, 0x12, 0xb0),
        create_door(player, 'Sewers Rope Room Up Stairs', Sprl).dir(Direction.Up, 0x42, 0, HTH).ss(S, 0x1b, 0x9c),
        create_door(player, 'Sewers Rope Room North Stairs', StrS).dir(Direction.North, 0x42, Mid, High),
        create_door(player, 'Sewers Dark Cross South Stairs', StrS).dir(Direction.South, 0x32, Mid, High),
        create_door(player, 'Sewers Dark Cross Key Door N', Nrml).dir(Direction.North, 0x32, Mid, High).small_key().pos(0),
        create_door(player, 'Sewers Dark Cross Key Door S', Nrml).dir(Direction.South, 0x22, Mid, High).small_key().pos(0),
        create_door(player, 'Sewers Water W', Nrml).dir(Direction.West, 0x22, Bot, High).pos(1),
        create_door(player, 'Sewers Key Rat E', Nrml).dir(Direction.East, 0x21, Bot, High).pos(1),
        create_door(player, 'Sewers Key Rat Key Door N', Nrml).dir(Direction.North, 0x21, Right, High).small_key().pos(0),
        create_door(player, 'Sewers Secret Room Key Door S', Nrml).dir(Direction.South, 0x11, Right, High).small_key().pos(2),
        create_door(player, 'Sewers Secret Room Push Block', Lgcl),
        create_door(player, 'Sewers Secret Room Up Stairs', Sprl).dir(Direction.Up, 0x11, 0, LTH).ss(S, 0x33, 0x6c, True),
        create_door(player, 'Sewers Pull Switch Down Stairs', Sprl).dir(Direction.Down, 0x02, 0, HTL).ss(S, 0x12, 0x80),
        create_door(player, 'Sewers Pull Switch S', Nrml).dir(Direction.South, 0x02, Mid, Low).trap(0x4).toggler().pos(0),
        # logically one way the sanc, but should be linked - also toggle
        create_door(player, 'Sanctuary N', Nrml).dir(Direction.North, 0x12, Mid, High).no_exit().toggler().pos(0),

        # Eastern Palace
        create_door(player, 'Eastern Lobby N', Nrml).dir(Direction.North, 0xc9, Mid, High).pos(1),
        create_door(player, 'Eastern Cannonball S', Nrml).dir(Direction.South, 0xb9, Mid, High).pos(2),
        create_door(player, 'Eastern Cannonball N', Nrml).dir(Direction.North, 0xb9, Mid, High).pos(1),
        create_door(player, 'Eastern Cannonball Ledge WN', Nrml).dir(Direction.West, 0xb9, Top, High).pos(3),
        create_door(player, 'Eastern Cannonball Ledge Key Door EN', Nrml).dir(Direction.East, 0xb9, Top, High).small_key().pos(0),
        create_door(player, 'Eastern Courtyard Ledge S', Nrml).dir(Direction.South, 0xa9, Mid, High).pos(5),
        create_door(player, 'Eastern Courtyard Ledge W', Nrml).dir(Direction.West, 0xa9, Mid, High).trap(0x4).pos(0),
        create_door(player, 'Eastern Courtyard Ledge E', Nrml).dir(Direction.East, 0xa9, Mid, High).trap(0x2).pos(1),
        create_door(player, 'Eastern Map Area W', Nrml).dir(Direction.West, 0xaa, Mid, High).pos(4),
        create_door(player, 'Eastern Compass Area E', Nrml).dir(Direction.East, 0xa8, Mid, High).pos(5),
        create_door(player, 'Eastern Compass Area EN', Nrml).dir(Direction.East, 0xa8, Top, Low).pos(4),
        ugly_door(create_door(player, 'Eastern Compass Area SW', Nrml).dir(Direction.South, 0xa8, Right, High)).small_key().pos(2),
        create_door(player, 'Eastern Hint Tile Push Block', Lgcl),
        create_door(player, 'Eastern Courtyard WN', Nrml).dir(Direction.West, 0xa9, Top, Low).pos(3),
        create_door(player, 'Eastern Courtyard EN', Nrml).dir(Direction.East, 0xa9, Top, Low).pos(4),
        create_door(player, 'Eastern Courtyard N', Nrml).dir(Direction.North, 0xa9, Mid, High).big_key().pos(2),
        create_door(player, 'Eastern Courtyard Potholes', Hole),
        create_door(player, 'Eastern Fairies\' Warp', Warp),
        create_door(player, 'Eastern Map Valley WN', Nrml).dir(Direction.West, 0xaa, Top, Low).pos(1),
        create_door(player, 'Eastern Map Valley SW', Nrml).dir(Direction.South, 0xaa, Left, High).pos(5),
        create_door(player, 'Eastern Dark Square NW', Nrml).dir(Direction.North, 0xba, Left, High).pos(1),
        create_door(player, 'Eastern Dark Square Key Door WN', Nrml).dir(Direction.West, 0xba, Top, High).small_key().pos(0),
        create_door(player, 'Eastern Big Key EN', Nrml).dir(Direction.East, 0xb8, Top, High).pos(1),
        create_door(player, 'Eastern Big Key NE', Nrml).dir(Direction.North, 0xb8, Right, High).big_key().pos(0),
        ugly_door(create_door(player, 'Eastern Darkness S', Nrml).dir(Direction.South, 0x99, Mid, High)).small_key().pos(1),
        # Up is a keydoor and down is not. Only the up stairs should be considered a key door for now.
        create_door(player, 'Eastern Darkness Up Stairs', Sprl).dir(Direction.Up, 0x99, 0, HTH).ss(Z, 0x1a, 0x6c, False, True).small_key().pos(0),
        ugly_door(create_door(player, 'Eastern Attic Start Down Stairs', Sprl).dir(Direction.Down, 0xda, 0, HTH).ss(Z, 0x11, 0x80, True, True)),
        create_door(player, 'Eastern Attic Start WS', Nrml).dir(Direction.West, 0xda, Bot, High).trap(0x4).pos(0),
        create_door(player, 'Eastern Attic Switches ES', Nrml).dir(Direction.East, 0xd9, Bot, High).trap(0x1).pos(2),
        create_door(player, 'Eastern Attic Switches WS', Nrml).dir(Direction.West, 0xd9, Bot, High).trap(0x4).pos(0),
        create_door(player, 'Eastern Eyegores ES', Nrml).dir(Direction.East, 0xd8, Bot, High).pos(2),
        create_door(player, 'Eastern Eyegores NE', Nrml).dir(Direction.North, 0xd8, Right, High).trap(0x4).pos(0),
        create_door(player, 'Eastern Boss SE', Nrml).dir(Direction.South, 0xc8, Right, High).no_exit().trap(0x4).pos(0),

        # Desert Palace
        create_door(player, 'Desert Main Lobby NW Edge', Open).dir(Direction.North, 0x84, None, High),
        create_door(player, 'Desert Main Lobby N Edge', Open).dir(Direction.North, 0x84, None, High),
        create_door(player, 'Desert Main Lobby NE Edge', Open).dir(Direction.North, 0x84, None, High),
        create_door(player, 'Desert Main Lobby E Edge', Open).dir(Direction.East, 0x84, None, High),
        create_door(player, 'Desert Dead End Edge', Open).dir(Direction.South, 0x74, None, High),
        create_door(player, 'Desert East Wing W Edge', Open).dir(Direction.West, 0x85, None, High),
        create_door(player, 'Desert East Wing N Edge', Open).dir(Direction.North, 0x85, None, High),
        create_door(player, 'Desert East Lobby WS', Intr).dir(Direction.West, 0x85, Bot, High).pos(3),
        create_door(player, 'Desert East Wing ES', Intr).dir(Direction.East, 0x85, Bot, High).pos(3),
        create_door(player, 'Desert East Wing Key Door EN', Intr).dir(Direction.East, 0x85, Top, High).small_key().pos(1),
        create_door(player, 'Desert Compass Key Door WN', Intr).dir(Direction.West, 0x85, Top, High).small_key().pos(1),
        create_door(player, 'Desert Compass NW', Nrml).dir(Direction.North, 0x85, Right, High).trap(0x4).pos(0),
        create_door(player, 'Desert Cannonball S', Nrml).dir(Direction.South, 0x75, Right, High).pos(1),
        create_door(player, 'Desert Arrow Pot Corner S Edge', Open).dir(Direction.South, 0x75, None, High),
        create_door(player, 'Desert Arrow Pot Corner W Edge', Open).dir(Direction.West, 0x75, None, High),
        create_door(player, 'Desert North Hall SE Edge', Open).dir(Direction.South, 0x74, None, High),
        create_door(player, 'Desert North Hall SW Edge', Open).dir(Direction.South, 0x74, None, High),
        create_door(player, 'Desert North Hall W Edge', Open).dir(Direction.West, 0x74, None, High),
        create_door(player, 'Desert North Hall E Edge', Open).dir(Direction.East, 0x74, None, High),
        create_door(player, 'Desert North Hall NW', Intr).dir(Direction.North, 0x74, Left, High).pos(1),
        create_door(player, 'Desert Map SW', Intr).dir(Direction.South, 0x74, Left, High).pos(1),
        create_door(player, 'Desert North Hall NE', Intr).dir(Direction.North, 0x74, Right, High).pos(0),
        create_door(player, 'Desert Map SE', Intr).dir(Direction.South, 0x74, Right, High).pos(0),
        create_door(player, 'Desert Sandworm Corner S Edge', Open).dir(Direction.South, 0x73, None, High),
        create_door(player, 'Desert Sandworm Corner E Edge', Open).dir(Direction.East, 0x73, None, High),
        create_door(player, 'Desert Sandworm Corner NE', Intr).dir(Direction.North, 0x73, Right, High).pos(2),
        create_door(player, 'Desert Bonk Torch SE', Intr).dir(Direction.South, 0x73, Right, High).pos(2),
        create_door(player, 'Desert Sandworm Corner WS', Intr).dir(Direction.West, 0x73, Bot, High).pos(1),
        # I don't know if I have to mark trap on interior doors yet - haven't mucked them up much
        create_door(player, 'Desert Circle of Pots ES', Intr).dir(Direction.East, 0x73, Bot, High).pos(1),
        create_door(player, 'Desert Circle of Pots NW', Intr).dir(Direction.North, 0x73, Left, High).pos(0),
        create_door(player, 'Desert Big Chest SW', Intr).dir(Direction.South, 0x73, Left, High).pos(0),
        create_door(player, 'Desert West Wing N Edge', Open).dir(Direction.North, 0x83, None, High),
        create_door(player, 'Desert West Wing WS', Intr).dir(Direction.West, 0x83, Bot, High).pos(2),
        create_door(player, 'Desert West Lobby ES', Intr).dir(Direction.East, 0x83, Bot, High).pos(2),
        # Desert Back
        create_door(player, 'Desert Back Lobby NW', Intr).dir(Direction.North, 0x63, Left, High).pos(1),
        create_door(player, 'Desert Tiles 1 SW', Intr).dir(Direction.South, 0x63, Left, High).pos(1),
        create_door(player, 'Desert Tiles 1 Up Stairs', Sprl).dir(Direction.Up, 0x63, 0, HTH).ss(A, 0x1b, 0x6c, True).small_key().pos(0),
        create_door(player, 'Desert Bridge Down Stairs', Sprl).dir(Direction.Down, 0x53, 0, HTH).ss(A, 0x0f, 0x80, True),
        create_door(player, 'Desert Bridge SW', Intr).dir(Direction.South, 0x53, Left, High).pos(0),
        create_door(player, 'Desert Four Statues NW', Intr).dir(Direction.North, 0x53, Left, High).pos(0),
        create_door(player, 'Desert Four Statues ES', Intr).dir(Direction.East, 0x53, Bot, High).pos(1),
        create_door(player, 'Desert Beamos Hall WS', Intr).dir(Direction.West, 0x53, Bot, High).pos(1),
        create_door(player, 'Desert Beamos Hall NE', Nrml).dir(Direction.North, 0x53, Right, High).small_key().pos(2),
        create_door(player, 'Desert Tiles 2 SE', Nrml).dir(Direction.South, 0x43, Right, High).small_key().pos(2),
        create_door(player, 'Desert Tiles 2 NE', Intr).dir(Direction.North, 0x43, Right, High).small_key().pos(1),
        create_door(player, 'Desert Wall Slide SE', Intr).dir(Direction.South, 0x43, Right, High).small_key().pos(1),
        # todo: we need a new flag for a door that has a wall on it - you have to traverse it one particular way first
        # the above is not a problem until we get to crossed mode
        create_door(player, 'Desert Wall Slide NW', Nrml).dir(Direction.North, 0x43, Left, High).big_key().pos(0),
        create_door(player, 'Desert Boss SW', Nrml).dir(Direction.South, 0x33, Left, High).no_exit().trap(0x4).pos(0),

        # Hera
        create_door(player, 'Hera Lobby Down Stairs', Sprl).dir(Direction.Down, 0x77, 3, HTL).ss(Z, 0x21, 0x90, False, True),
        create_door(player, 'Hera Lobby Key Stairs', Sprl).dir(Direction.Down, 0x77, 1, HTL).ss(A, 0x12, 0x80).small_key().pos(0),
        create_door(player, 'Hera Lobby Up Stairs', Sprl).dir(Direction.Up, 0x77, 2, HTL).ss(X, 0x2b, 0x5c, False, True),
        create_door(player, 'Hera Basement Cage Up Stairs', Sprl).dir(Direction.Up, 0x87, 3, LTH).ss(Z, 0x42, 0x7c, True, True),
        create_door(player, 'Hera Tile Room Up Stairs', Sprl).dir(Direction.Up, 0x87, 1, LTH).ss(A, 0x32, 0x6c, True, True),
        create_door(player, 'Hera Tile Room EN', Intr).dir(Direction.East, 0x87, Top, High).pos(0),
        create_door(player, 'Hera Tridorm WN', Intr).dir(Direction.West, 0x87, Top, High).pos(0),
        create_door(player, 'Hera Tridorm SE', Intr).dir(Direction.South, 0x87, Right, High).pos(1),
        create_door(player, 'Hera Torches NE', Intr).dir(Direction.North, 0x87, Right, High).pos(1),
        create_door(player, 'Hera Beetles Down Stairs', Sprl).dir(Direction.Down, 0x31, 2, LTH).ss(X, 0x3a, 0x70, True, True),
        create_door(player, 'Hera Beetles WS', Intr).dir(Direction.West, 0x31, Bot, High).pos(1),
        create_door(player, 'Hera Beetles Holes', Hole),
        create_door(player, 'Hera Startile Corner ES', Intr).dir(Direction.East, 0x31, Bot, High).pos(1),
        create_door(player, 'Hera Startile Corner NW', Intr).dir(Direction.North, 0x31, Left, High).big_key().pos(0),
        create_door(player, 'Hera Startile Corner Holes', Hole),
        # technically ugly but causes lots of failures in basic
        create_door(player, 'Hera Startile Wide SW', Intr).dir(Direction.South, 0x31, Left, High).pos(0),
        create_door(player, 'Hera Startile Wide Up Stairs', Sprl).dir(Direction.Up, 0x31, 0, HTH).ss(S, 0x6b, 0xac, False, True),
        create_door(player, 'Hera Startile Wide Holes', Hole),
        create_door(player, 'Hera 4F Down Stairs', Sprl).dir(Direction.Down, 0x27, 0, HTH).ss(S, 0x62, 0xc0),
        create_door(player, 'Hera 4F Up Stairs', Sprl).dir(Direction.Up, 0x27, 1, HTH).ss(A, 0x6b, 0x2c),
        create_door(player, 'Hera 4F Holes', Hole),
        create_door(player, 'Hera Big Chest Landing Exit', Lgcl),
        create_door(player, 'Hera Big Chest Landing Holes', Hole),
        create_door(player, 'Hera 5F Down Stairs', Sprl).dir(Direction.Down, 0x17, 1, HTH).ss(A, 0x62, 0x40),
        create_door(player, 'Hera 5F Up Stairs', Sprl).dir(Direction.Up, 0x17, 0, HTH).ss(S, 0x6a, 0x9c),
        create_door(player, 'Hera 5F Star Hole', Hole),
        create_door(player, 'Hera 5F Pothole Chain', Hole),
        create_door(player, 'Hera 5F Normal Holes', Hole),
        create_door(player, 'Hera Fairies\' Warp', Warp),
        create_door(player, 'Hera Boss Down Stairs', Sprl).dir(Direction.Down, 0x07, 0, HTH).ss(S, 0x61, 0xb0),
        create_door(player, 'Hera Boss Outer Hole', Hole),
        create_door(player, 'Hera Boss Inner Hole', Hole),

        # Castle Tower
        create_door(player, 'Tower Lobby NW', Intr).dir(Direction.North, 0xe0, Left, High).pos(1),
        create_door(player, 'Tower Gold Knights SW', Intr).dir(Direction.South, 0xe0, Left, High).pos(1),
        create_door(player, 'Tower Gold Knights EN', Intr).dir(Direction.East, 0xe0, Top, High).pos(0),
        create_door(player, 'Tower Room 03 WN', Intr).dir(Direction.West, 0xe0, Bot, High).pos(0),
        create_door(player, 'Tower Room 03 Up Stairs', Sprl).dir(Direction.Up, 0xe0, 0, HTH).ss(S, 0x1a, 0x6c, True, True).small_key().pos(2),
        create_door(player, 'Tower Lone Statue Down Stairs', Sprl).dir(Direction.Down, 0xd0, 0, HTH).ss(S, 0x11, 0x80, True, True),
        create_door(player, 'Tower Lone Statue WN', Intr).dir(Direction.West, 0xd0, Top, High).pos(1),
        create_door(player, 'Tower Dark Maze EN', Intr).dir(Direction.East, 0xd0, Top, High).pos(1),
        create_door(player, 'Tower Dark Maze ES', Intr).dir(Direction.East, 0xd0, Bot, High).small_key().pos(0),
        create_door(player, 'Tower Dark Chargers WS', Intr).dir(Direction.West, 0xd0, Bot, High).small_key().pos(0),
        create_door(player, 'Tower Dark Chargers Up Stairs', Sprl).dir(Direction.Up, 0xd0, 2, HTH).ss(X, 0x1b, 0x8c, True, True),
        create_door(player, 'Tower Dual Statues Down Stairs', Sprl).dir(Direction.Down, 0xc0, 2, HTH).ss(X, 0x12, 0xa0, True, True),
        create_door(player, 'Tower Dual Statues WS', Intr).dir(Direction.West, 0xc0, Bot, High).pos(1),
        create_door(player, 'Tower Dark Pits ES', Intr).dir(Direction.East, 0xc0, Bot, High).pos(1),
        create_door(player, 'Tower Dark Pits EN', Intr).dir(Direction.East, 0xc0, Top, High).pos(0),
        create_door(player, 'Tower Dark Archers WN', Intr).dir(Direction.West, 0xc0, Top, High).pos(0),
        create_door(player, 'Tower Dark Archers Up Stairs', Sprl).dir(Direction.Up, 0xc0, 0, HTH).ss(S, 0x1b, 0x6c, True, True).small_key().pos(2),
        create_door(player, 'Tower Red Spears Down Stairs', Sprl).dir(Direction.Down, 0xb0, 0, HTH).ss(S, 0x12, 0x80, True, True),
        create_door(player, 'Tower Red Spears WN', Intr).dir(Direction.West, 0xb0, Top, High).pos(1),
        create_door(player, 'Tower Red Guards EN', Intr).dir(Direction.East, 0xb0, Top, High).pos(1),
        create_door(player, 'Tower Red Guards SW', Intr).dir(Direction.South, 0xb0, Left, High).pos(0),
        create_door(player, 'Tower Circle of Pots NW', Intr).dir(Direction.North, 0xb0, Left, High).pos(0),
        create_door(player, 'Tower Circle of Pots WS', Intr).dir(Direction.West, 0xb0, Bot, High).small_key().pos(2),
        create_door(player, 'Tower Pacifist Run ES', Intr).dir(Direction.East, 0xb0, Bot, High).small_key().pos(2),
        create_door(player, 'Tower Pacifist Run Up Stairs', Sprl).dir(Direction.Up, 0xb0, 2, LTH).ss(X, 0x33, 0x8c, True, True),
        create_door(player, 'Tower Push Statue Down Stairs', Sprl).dir(Direction.Down, 0x40, 0, HTL).ss(X, 0x12, 0xa0, True, True),
        create_door(player, 'Tower Push Statue WS', Intr).dir(Direction.West, 0x40, Bot, Low).pos(0),
        create_door(player, 'Tower Catwalk ES', Intr).dir(Direction.East, 0x40, Bot, Low).pos(0),
        create_door(player, 'Tower Catwalk North Stairs', StrS).dir(Direction.North, 0x40, Left, High),
        create_door(player, 'Tower Antechamber South Stairs', StrS).dir(Direction.South, 0x30, Left, High),
        create_door(player, 'Tower Antechamber NW', Intr).dir(Direction.North, 0x30, Left, High).pos(1),
        create_door(player, 'Tower Altar SW', Intr).dir(Direction.South, 0x30, Left, High).pos(1),
        create_door(player, 'Tower Altar NW', Nrml).dir(Direction.North, 0x30, Left, High).pos(0),
        create_door(player, 'Tower Agahnim 1 SW', Nrml).dir(Direction.South, 0x20, Left, High).no_exit().trap(0x4).pos(0),

        # Palace of Darkness
        create_door(player, 'PoD Lobby N', Intr).dir(Direction.North, 0x4a, Mid, High).pos(2),
        create_door(player, 'PoD Lobby NW', Intr).dir(Direction.North, 0x4a, Left, High).pos(0),
        create_door(player, 'PoD Lobby NE', Intr).dir(Direction.North, 0x4a, Right, High).pos(1),
        create_door(player, 'PoD Left Cage SW', Intr).dir(Direction.North, 0x4a, Left, High).pos(0),
        create_door(player, 'PoD Middle Cage S', Intr).dir(Direction.North, 0x4a, Mid, High).pos(2),
        create_door(player, 'PoD Middle Cage SE', Intr).dir(Direction.North, 0x4a, Right, High).pos(1),
        create_door(player, 'PoD Left Cage Down Stairs', Sprl).dir(Direction.Down, 0x4a, 1, HTH).ss(A, 0x12, 0x80, False, True),
        create_door(player, 'PoD Middle Cage Down Stairs', Sprl).dir(Direction.Down, 0x4a, 0, HTH).ss(S, 0x12, 0x80, False, True),
        create_door(player, 'PoD Middle Cage N', Nrml).dir(Direction.North, 0x4a, Mid, High).small_key().pos(2),
        create_door(player, 'PoD Shooter Room Up Stairs', Sprl).dir(Direction.Up, 0x09, 1, HTH).ss(A, 0x1b, 0x6c, True, True),
        create_door(player, 'PoD Warp Room Up Stairs', Sprl).dir(Direction.Up, 0x09, 0, HTH).ss(S, 0x1a, 0x6c, True, True),
        create_door(player, 'PoD Warp Room Warp', Warp),
        create_door(player, 'PoD Pit Room S', Nrml).dir(Direction.South, 0x3a, Mid, High).small_key().pos(0),
        create_door(player, 'PoD Pit Room NW', Nrml).dir(Direction.North, 0x3a, Left, High).pos(1),
        create_door(player, 'PoD Pit Room NE', Nrml).dir(Direction.North, 0x3a, Right, High).pos(2),
        create_door(player, 'PoD Pit Room Freefall', Hole),
        create_door(player, 'PoD Pit Room Bomb Hole', Hole),
        create_door(player, 'PoD Big Key Landing Hole', Hole),
        create_door(player, 'PoD Big Key Landing Down Stairs', Sprl).dir(Direction.Down, 0x3a, 0, HTH).ss(A, 0x11, 0x00),
        create_door(player, 'PoD Basement Ledge Up Stairs', Sprl).dir(Direction.Up, 0x0a, 0, HTH).ss(A, 0x1a, 0xec).small_key().pos(0),
        create_door(player, 'PoD Basement Ledge Drop Down', Lgcl),
        create_door(player, 'PoD Stalfos Basement Warp', Warp),
        create_door(player, 'PoD Arena Main SW', Nrml).dir(Direction.South, 0x2a, Left, High).pos(4),
        create_door(player, 'PoD Arena Bridge SE', Nrml).dir(Direction.South, 0x2a, Right, High).pos(5),
        create_door(player, 'PoD Arena Main NW', Nrml).dir(Direction.North, 0x2a, Left, High).small_key().pos(1),
        create_door(player, 'PoD Arena Main NE', Nrml).dir(Direction.North, 0x2a, Right, High).no_exit().trap(0x4).pos(0),
        create_door(player, 'PoD Arena Main Crystal Path', Lgcl),
        create_door(player, 'PoD Arena Crystals E', Nrml).dir(Direction.East, 0x2a, Mid, High).pos(3),
        create_door(player, 'PoD Arena Crystal Path', Lgcl),
        create_door(player, 'PoD Arena Bridge Drop Down', Lgcl),
        create_door(player, 'PoD Arena Ledge ES', Nrml).dir(Direction.East, 0x2a, Bot, High).pos(2),
        create_door(player, 'PoD Sexy Statue W', Nrml).dir(Direction.West, 0x2b, Mid, High).pos(3),
        create_door(player, 'PoD Sexy Statue NW', Nrml).dir(Direction.North, 0x2b, Left, High).trap(0x1).pos(2),
        create_door(player, 'PoD Map Balcony Drop Down', Lgcl),
        create_door(player, 'PoD Map Balcony WS', Nrml).dir(Direction.West, 0x2b, Bot, High).pos(1),
        create_door(player, 'PoD Map Balcony South Stairs', StrS).dir(Direction.South, 0x2b, Left, High),
        create_door(player, 'PoD Conveyor North Stairs', StrS).dir(Direction.North, 0x3b, Left, High),
        create_door(player, 'PoD Conveyor SW', Nrml).dir(Direction.South, 0x3b, Left, High).pos(0),
        create_door(player, 'PoD Mimics 1 NW', Nrml).dir(Direction.North, 0x4b, Left, High).trap(0x4).pos(0),
        create_door(player, 'PoD Mimics 1 SW', Intr).dir(Direction.South, 0x4b, Left, High).pos(1),
        create_door(player, 'PoD Jelly Hall NW', Intr).dir(Direction.North, 0x4b, Left, High).pos(1),
        create_door(player, 'PoD Jelly Hall NE', Intr).dir(Direction.North, 0x4b, Right, High).pos(2),
        create_door(player, 'PoD Warp Hint SE', Intr).dir(Direction.South, 0x4b, Right, High).pos(2),
        create_door(player, 'PoD Warp Hint Warp', Warp),
        create_door(player, 'PoD Falling Bridge SW', Nrml).dir(Direction.South, 0x1a, Left, High).small_key().pos(3),
        create_door(player, 'PoD Falling Bridge WN', Nrml).dir(Direction.West, 0x1a, Top, High).small_key().pos(1),
        create_door(player, 'PoD Falling Bridge EN', Intr).dir(Direction.East, 0x1a, Top, High).pos(4),
        create_door(player, 'PoD Big Chest Balcony W', Nrml).dir(Direction.West, 0x1a, Mid, High).pos(2),
        create_door(player, 'PoD Dark Maze EN', Nrml).dir(Direction.East, 0x19, Top, High).small_key().pos(1),
        create_door(player, 'PoD Dark Maze E', Nrml).dir(Direction.East, 0x19, Mid, High).pos(0),
        create_door(player, 'PoD Compass Room WN', Intr).dir(Direction.West, 0x1a, Top, High).pos(4),
        create_door(player, 'PoD Compass Room SE', Intr).dir(Direction.North, 0x1a, Mid, High).small_key().pos(0),
        create_door(player, 'PoD Harmless Hellway NE', Intr).dir(Direction.North, 0x1a, Right, High).small_key().pos(0),
        create_door(player, 'PoD Harmless Hellway SE', Nrml).dir(Direction.South, 0x1a, Right, High).pos(5),
        create_door(player, 'PoD Compass Room W Down Stairs', Sprl).dir(Direction.Down, 0x1a, 0, HTH).ss(S, 0x12, 0x50, True, True),
        create_door(player, 'PoD Compass Room E Down Stairs', Sprl).dir(Direction.Down, 0x1a, 1, HTH).ss(S, 0x11, 0xb0, True, True),
        create_door(player, 'PoD Dark Basement W Up Stairs', Sprl).dir(Direction.Up, 0x6a, 0, HTH).ss(S, 0x1b, 0x3c, True),
        create_door(player, 'PoD Dark Basement E Up Stairs', Sprl).dir(Direction.Up, 0x6a, 1, HTH).ss(S, 0x1b, 0x9c, True),
        create_door(player, 'PoD Dark Alley NE', Nrml).dir(Direction.North, 0x6a, Right, High).big_key().pos(0),
        create_door(player, 'PoD Mimics 2 SW', Nrml).dir(Direction.South, 0x1b, Left, High).pos(1),
        create_door(player, 'PoD Mimics 2 NW', Intr).dir(Direction.North, 0x1b, Left, High).pos(0),
        create_door(player, 'PoD Bow Statue SW', Intr).dir(Direction.South, 0x1b, Left, High).pos(0),
        # todo: we need a new flag for a door that has a wall on it - you have to traverse it one particular way first
        # the above is not a problem until we get to crossed mode
        create_door(player, 'PoD Bow Statue Down Ladder', Lddr),
        create_door(player, 'PoD Dark Pegs Up Ladder', Lddr),
        create_door(player, 'PoD Dark Pegs WN', Intr).dir(Direction.West, 0x0b, Mid, High).small_key().pos(2),
        create_door(player, 'PoD Lonely Turtle SW', Intr).dir(Direction.South, 0x0b, Mid, High).pos(0),
        create_door(player, 'PoD Lonely Turtle EN', Intr).dir(Direction.East, 0x0b, Mid, High).small_key().pos(2),
        create_door(player, 'PoD Turtle Party ES', Intr).dir(Direction.East, 0x0b, Mid, High).pos(1),
        create_door(player, 'PoD Turtle Party NW', Intr).dir(Direction.North, 0x0b, Mid, High).pos(0),
        create_door(player, 'PoD Callback WS', Intr).dir(Direction.West, 0x0b, Mid, High).pos(1),
        create_door(player, 'PoD Callback Warp', Warp),
        create_door(player, 'PoD Boss SE', Nrml).dir(Direction.South, 0x5a, Right, High).no_exit().trap(0x4).pos(0),

        create_door(player, 'Swamp Lobby Moat', Lgcl),
        create_door(player, 'Swamp Entrance Down Stairs', Sprl).dir(Direction.Down, 0x28, 0, HTH).ss(A, 0x11, 0x80).small_key().pos(0),
        create_door(player, 'Swamp Entrance Moat', Lgcl),
        create_door(player, 'Swamp Pot Row Up Stairs', Sprl).dir(Direction.Up, 0x38, 0, HTH).ss(A, 0x1a, 0x6c, True),
        create_door(player, 'Swamp Pot Row WN', Nrml).dir(Direction.West, 0x38, Top, High).pos(0),
        create_door(player, 'Swamp Pot Row WS', Nrml).dir(Direction.West, 0x38, Bot, High).small_key().pos(1),
        create_door(player, 'Swamp Map Ledge EN', Nrml).dir(Direction.East, 0x37, Top, High).pos(1),
        create_door(player, 'Swamp Trench 1 Approach ES', Nrml).dir(Direction.East, 0x37, Bot, High).small_key().pos(3),
        create_door(player, 'Swamp Trench 1 Approach Dry', Lgcl),
        create_door(player, 'Swamp Trench 1 Approach Key', Lgcl),
        create_door(player, 'Swamp Trench 1 Approach Swim Depart', Lgcl),
        create_door(player, 'Swamp Trench 1 Nexus Approach', Lgcl),
        create_door(player, 'Swamp Trench 1 Nexus Key', Lgcl),
        create_door(player, 'Swamp Trench 1 Nexus N', Intr).dir(Direction.North, 0x37, Mid, Low).pos(5),
        create_door(player, 'Swamp Trench 1 Alcove S', Intr).dir(Direction.South, 0x37, Mid, Low).pos(5),
        create_door(player, 'Swamp Trench 1 Key Ledge Dry', Lgcl),
        create_door(player, 'Swamp Trench 1 Key Approach', Lgcl),
        create_door(player, 'Swamp Trench 1 Key Ledge Depart', Lgcl),
        create_door(player, 'Swamp Trench 1 Key Ledge NW', Intr).dir(Direction.North, 0x37, Left, High).small_key().pos(2),
        create_door(player, 'Swamp Trench 1 Departure Dry', Lgcl),
        create_door(player, 'Swamp Trench 1 Departure Approach', Lgcl),
        create_door(player, 'Swamp Trench 1 Departure Key', Lgcl),
        create_door(player, 'Swamp Trench 1 Departure WS', Nrml).dir(Direction.West, 0x37, Bot, High).pos(4),
        create_door(player, 'Swamp Hammer Switch SW', Intr).dir(Direction.South, 0x37, Left, High).small_key().pos(2),
        create_door(player, 'Swamp Hammer Switch WN', Nrml).dir(Direction.West, 0x37, Top, High).pos(0),
        create_door(player, 'Swamp Hub ES', Nrml).dir(Direction.East, 0x36, Bot, High).pos(4),
        create_door(player, 'Swamp Hub S', Nrml).dir(Direction.South, 0x36, Mid, High).pos(5),
        create_door(player, 'Swamp Hub WS', Nrml).dir(Direction.West, 0x36, Bot, High).pos(3),
        create_door(player, 'Swamp Hub WN', Nrml).dir(Direction.West, 0x36, Top, High).small_key().pos(2),
        create_door(player, 'Swamp Hub Hook Path', Lgcl),
        create_door(player, 'Swamp Hub Dead Ledge EN', Nrml).dir(Direction.East, 0x36, Top, High).pos(0),
        create_door(player, 'Swamp Hub North Ledge N', Nrml).dir(Direction.North, 0x36, Mid, High).small_key().pos(1),
        create_door(player, 'Swamp Hub North Ledge Drop Down', Lgcl),
        create_door(player, 'Swamp Donut Top N', Nrml).dir(Direction.North, 0x46, Mid, High).pos(0),
        create_door(player, 'Swamp Donut Top SE', Intr).dir(Direction.South, 0x46, Right, High).pos(2),
        create_door(player, 'Swamp Donut Bottom NE', Intr).dir(Direction.North, 0x46, Right, High).pos(2),
        create_door(player, 'Swamp Donut Bottom NW', Intr).dir(Direction.North, 0x46, Left, High).pos(1),
        create_door(player, 'Swamp Compass Donut SW', Intr).dir(Direction.South, 0x46, Left, High).pos(1),
        create_door(player, 'Swamp Compass Donut Push Block', Lgcl),
        create_door(player, 'Swamp Crystal Switch EN', Nrml).dir(Direction.East, 0x35, Top, High).small_key().pos(0),
        create_door(player, 'Swamp Crystal Switch SE', Intr).dir(Direction.South, 0x35, Right, High).pos(3),
        create_door(player, 'Swamp Shortcut NE', Intr).dir(Direction.North, 0x35, Right, High).pos(3),
        create_door(player, 'Swamp Shortcut Blue Barrier', Lgcl),
        create_door(player, 'Swamp Trench 2 Pots ES', Nrml).dir(Direction.East, 0x35, Bot, High).pos(4),
        create_door(player, 'Swamp Trench 2 Pots Blue Barrier', Lgcl),
        create_door(player, 'Swamp Trench 2 Pots Dry', Lgcl),
        create_door(player, 'Swamp Trench 2 Pots Wet', Lgcl),
        create_door(player, 'Swamp Trench 2 Blocks Pots', Lgcl),
        create_door(player, 'Swamp Trench 2 Blocks N', Intr).dir(Direction.North, 0x35, Mid, Low).pos(5),
        create_door(player, 'Swamp Trench 2 Alcove S', Intr).dir(Direction.South, 0x35, Mid, Low).pos(5),
        create_door(player, 'Swamp Trench 2 Departure Wet', Lgcl),
        create_door(player, 'Swamp Trench 2 Departure WS', Nrml).dir(Direction.West, 0x35, Bot, High).pos(2),
        create_door(player, 'Swamp Big Key Ledge WN', Nrml).dir(Direction.West, 0x35, Top, High).pos(1),
        create_door(player, 'Swamp West Shallows ES', Nrml).dir(Direction.East, 0x34, Bot, High).pos(1),
        create_door(player, 'Swamp West Shallows Push Blocks', Lgcl),
        create_door(player, 'Swamp West Block Path Up Stairs', Sprl).dir(Direction.Up, 0x34, 0, HTH).ss(Z, 0x1b, 0x6c, False, True),
        create_door(player, 'Swamp West Block Path Drop Down', Lgcl),
        create_door(player, 'Swamp West Ledge Drop Down', Lgcl),
        create_door(player, 'Swamp West Ledge Hook Path', Lgcl),
        create_door(player, 'Swamp Barrier Ledge Drop Down', Lgcl),
        create_door(player, 'Swamp Barrier Ledge - Orange', Lgcl),
        create_door(player, 'Swamp Barrier EN', Nrml).dir(Direction.East, 0x34, Top, High).pos(0),
        create_door(player, 'Swamp Barrier - Orange', Lgcl),
        create_door(player, 'Swamp Barrier Ledge Hook Path', Lgcl),
        create_door(player, 'Swamp Attic Down Stairs', Sprl).dir(Direction.Down, 0x54, 0, HTH).ss(Z, 0x12, 0x80, False, True),
        create_door(player, 'Swamp Attic Left Pit', Hole),
        create_door(player, 'Swamp Attic Right Pit', Hole),
        create_door(player, 'Swamp Push Statue S', Nrml).dir(Direction.South, 0x26, Mid, High).small_key().pos(0),
        create_door(player, 'Swamp Push Statue NW', Intr).dir(Direction.North, 0x26, Left, High).pos(1),
        create_door(player, 'Swamp Push Statue NE', Intr).dir(Direction.North, 0x26, Right, High).pos(2),
        create_door(player, 'Swamp Push Statue Down Stairs', Sprl).dir(Direction.Down, 0x26, 2, HTH).ss(X, 0x12, 0xc0, False, True),
        create_door(player, 'Swamp Shooters SW', Intr).dir(Direction.South, 0x26, Left, High).pos(1),
        create_door(player, 'Swamp Shooters EN', Intr).dir(Direction.East, 0x26, Top, High).pos(3),
        create_door(player, 'Swamp Left Elbow WN', Intr).dir(Direction.West, 0x26, Top, High).pos(3),
        create_door(player, 'Swamp Left Elbow Down Stairs', Sprl).dir(Direction.Down, 0x26, 0, HTH).ss(S, 0x11, 0x40, True, True),
        create_door(player, 'Swamp Right Elbow SE', Intr).dir(Direction.South, 0x26, Right, High).pos(2),
        create_door(player, 'Swamp Right Elbow Down Stairs', Sprl).dir(Direction.Down, 0x26, 1, HTH).ss(S, 0x12, 0xb0, True, True),
        create_door(player, 'Swamp Drain Left Up Stairs', Sprl).dir(Direction.Up, 0x76, 0, HTH).ss(S, 0x1b, 0x2c, True, True),
        create_door(player, 'Swamp Drain WN', Intr).dir(Direction.West, 0x76, Top, Low).pos(0),
        create_door(player, 'Swamp Drain Right Switch', Lgcl),
        create_door(player, 'Swamp Drain Right Up Stairs', Sprl).dir(Direction.Up, 0x76, 1, HTH).ss(S, 0x1b, 0x9c, True, True),
        create_door(player, 'Swamp Flooded Room Up Stairs', Sprl).dir(Direction.Up, 0x76, 2, HTH).ss(X, 0x1a, 0xac, True, True),
        create_door(player, 'Swamp Flooded Room WS', Intr).dir(Direction.West, 0x76, Bot, Low).pos(1),
        create_door(player, 'Swamp Flooded Spot Ladder', Lgcl),
        create_door(player, 'Swamp Flooded Room Ladder', Lgcl),
        create_door(player, 'Swamp Basement Shallows NW', Nrml).dir(Direction.North, 0x76, Left, High).toggler().pos(2),
        create_door(player, 'Swamp Basement Shallows EN', Intr).dir(Direction.West, 0x76, Top, High).pos(0),
        create_door(player, 'Swamp Basement Shallows ES', Intr).dir(Direction.East, 0x76, Bot, High).pos(1),
        create_door(player, 'Swamp Waterfall Room SW', Nrml).dir(Direction.South, 0x66, Left, Low).toggler().pos(1),
        create_door(player, 'Swamp Waterfall Room NW', Intr).dir(Direction.North, 0x66, Left, Low).pos(3),
        create_door(player, 'Swamp Waterfall Room NE', Intr).dir(Direction.North, 0x66, Right, Low).pos(0),
        create_door(player, 'Swamp Refill SW', Intr).dir(Direction.South, 0x66, Left, Low).pos(3),
        create_door(player, 'Swamp Behind Waterfall SE', Intr).dir(Direction.South, 0x66, Right, Low).pos(0),
        create_door(player, 'Swamp Behind Waterfall Up Stairs', Sprl).dir(Direction.Up, 0x66, 0, HTH).ss(S, 0x1a, 0x6c, True, True),
        create_door(player, 'Swamp C Down Stairs', Sprl).dir(Direction.Down, 0x16, 0, HTH).ss(S, 0x11, 0x80, True, True),
        create_door(player, 'Swamp C SE', Intr).dir(Direction.South, 0x16, Right, High).pos(2),
        create_door(player, 'Swamp Waterway NE', Intr).dir(Direction.North, 0x16, Right, High).pos(2),
        create_door(player, 'Swamp Waterway N', Intr).dir(Direction.North, 0x16, Mid, High).pos(0),
        create_door(player, 'Swamp Waterway NW', Intr).dir(Direction.North, 0x16, Left, High).small_key().pos(1),
        create_door(player, 'Swamp I S', Intr).dir(Direction.South, 0x16, Mid, High).pos(0),
        create_door(player, 'Swamp T SW', Intr).dir(Direction.South, 0x16, Left, High).small_key().pos(1),
        create_door(player, 'Swamp T NW', Nrml).dir(Direction.North, 0x16, Left, High).pos(3),
        create_door(player, 'Swamp Boss SW', Nrml).dir(Direction.South, 0x06, Left, High).trap(0x4).pos(0),

        create_door(player, 'Skull 1 Lobby WS', Nrml).dir(Direction.West, 0x58, Bot, High).small_key().pos(1),
        create_door(player, 'Skull 1 Lobby ES', Intr).dir(Direction.East, 0x58, Bot, High).pos(5),
        create_door(player, 'Skull Map Room WS', Intr).dir(Direction.West, 0x58, Bot, High).pos(5),
        create_door(player, 'Skull Map Room SE', Nrml).dir(Direction.South, 0x58, Right, High).small_key().pos(2),
        create_door(player, 'Skull Pot Circle WN', Intr).dir(Direction.West, 0x58, Top, High).pos(3),
        create_door(player, 'Skull Pull Switch EN', Intr).dir(Direction.East, 0x58, Top, High).pos(3),
        create_door(player, 'Skull Pot Circle Star Path', Lgcl),
        create_door(player, 'Skull Pull Switch S', Intr).dir(Direction.South, 0x58, Left, High).pos(0),
        create_door(player, 'Skull Big Chest N', Intr).dir(Direction.North, 0x58, Left, High).no_exit().pos(0),
        create_door(player, 'Skull Big Chest Hookpath', Lgcl),
        create_door(player, 'Skull Pinball NE', Nrml).dir(Direction.North, 0x68, Right, High).small_key().pos(1),
        create_door(player, 'Skull Pinball WS', Nrml).dir(Direction.West, 0x68, Bot, High).no_exit().trap(0x4).pos(0),
        create_door(player, 'Skull Compass Room NE', Nrml).dir(Direction.North, 0x67, Right, High).pos(0),
        create_door(player, 'Skull Compass Room ES', Nrml).dir(Direction.East, 0x67, Bot, High).pos(2),
        create_door(player, 'Skull Left Drop ES', Intr).dir(Direction.East, 0x67, Bot, High).pos(1),
        create_door(player, 'Skull Compass Room WS', Intr).dir(Direction.West, 0x67, Bot, High).pos(1),
        create_door(player, 'Skull Pot Prison ES', Nrml).dir(Direction.East, 0x57, Bot, High).small_key().pos(2),
        create_door(player, 'Skull Pot Prison SE', Nrml).dir(Direction.South, 0x57, Right, High).pos(5),
        create_door(player, 'Skull 2 East Lobby WS', Nrml).dir(Direction.West, 0x57, Bot, High).pos(4),
        create_door(player, 'Skull 2 East Lobby NW', Intr).dir(Direction.North, 0x57, Left, High).pos(1),
        create_door(player, 'Skull Big Key SW', Intr).dir(Direction.South, 0x57, Left, High).pos(1),
        create_door(player, 'Skull Big Key WN', Intr).dir(Direction.West, 0x57, Top, High).pos(0),
        create_door(player, 'Skull Lone Pot EN', Intr).dir(Direction.East, 0x57, Top, High).pos(0),
        create_door(player, 'Skull Small Hall ES', Nrml).dir(Direction.East, 0x56, Bot, High).pos(3),
        create_door(player, 'Skull Small Hall WS', Intr).dir(Direction.West, 0x56, Bot, High).pos(2),
        create_door(player, 'Skull 2 West Lobby ES', Intr).dir(Direction.East, 0x56, Bot, High).pos(2),
        create_door(player, 'Skull 2 West Lobby NW', Intr).dir(Direction.North, 0x56, Left, High).small_key().pos(0),
        create_door(player, 'Skull X Room SW', Intr).dir(Direction.South, 0x56, Left, High).small_key().pos(0),
        create_door(player, 'Skull Back Drop Star Path', Lgcl),
        create_door(player, 'Skull 3 Lobby NW', Nrml).dir(Direction.North, 0x59, Left, High).small_key().pos(0),
        create_door(player, 'Skull 3 Lobby WN', Intr).dir(Direction.West, 0x59, Top, High).pos(2),
        create_door(player, 'Skull East Bridge EN', Intr).dir(Direction.East, 0x59, Top, High).pos(2),
        create_door(player, 'Skull East Bridge ES', Intr).dir(Direction.East, 0x59, Bot, High).pos(3),
        create_door(player, 'Skull West Bridge Nook WS', Intr).dir(Direction.West, 0x59, Bot, High).pos(3),
        create_door(player, 'Skull Star Pits SW', Nrml).dir(Direction.South, 0x49, Left, High).small_key().pos(2),
        create_door(player, 'Skull Star Pits WS', Intr).dir(Direction.West, 0x49, Bot, High).pos(3),
        create_door(player, 'Skull Torch Room ES', Intr).dir(Direction.East, 0x49, Bot, High).pos(3),
        create_door(player, 'Skull Torch Room EN', Intr).dir(Direction.East, 0x49, Top, High).pos(1),
        create_door(player, 'Skull Vines WN', Intr).dir(Direction.West, 0x49, Top, High).pos(1),
        create_door(player, 'Skull Vines NW', Nrml).dir(Direction.North, 0x49, Left, High).pos(0),
        create_door(player, 'Skull Spike Corner SW', Nrml).dir(Direction.South, 0x39, Left, High).no_exit().trap(0x4).pos(0),
        create_door(player, 'Skull Spike Corner WS', Intr).dir(Direction.West, 0x39, Bot, High).small_key().pos(1),
        create_door(player, 'Skull Final Drop ES', Intr).dir(Direction.East, 0x39, Bot, High).small_key().pos(1),
        create_door(player, 'Skull Final Drop Hole', Hole),

        create_door(player, 'Thieves Lobby N Edge', Open).dir(Direction.North, 0xdb, None, Low),
        create_door(player, 'Thieves Lobby NE Edge', Open).dir(Direction.North, 0xdb, None, Low),
        create_door(player, 'Thieves Lobby E', Nrml).dir(Direction.East, 0xdb, Mid, High).no_exit().trap(0x4).pos(0),
        create_door(player, 'Thieves Big Chest Nook WS Edge', Open).dir(Direction.West, 0xdb, None, Low),
        create_door(player, 'Thieves Ambush S Edge', Open).dir(Direction.South, 0xcb, None, Low),
        create_door(player, 'Thieves Ambush SE Edge', Open).dir(Direction.South, 0xcb, None, Low),
        create_door(player, 'Thieves Ambush ES Edge', Open).dir(Direction.East, 0xcb, None, Low),
        create_door(player, 'Thieves Ambush EN Edge', Open).dir(Direction.East, 0xcb, None, Low),
        create_door(player, 'Thieves Ambush E', Nrml).dir(Direction.East, 0xcb, Mid, High).pos(0),
        create_door(player, 'Thieves BK Corner WN Edge', Open).dir(Direction.West, 0xcc, None, Low),
        create_door(player, 'Thieves BK Corner WS Edge', Open).dir(Direction.West, 0xcc, None, Low),
        create_door(player, 'Thieves BK Corner S Edge', Open).dir(Direction.South, 0xcc, None, Low),
        create_door(player, 'Thieves BK Corner SW Edge', Open).dir(Direction.South, 0xcc, None, Low),
        create_door(player, 'Thieves BK Corner W', Nrml).dir(Direction.West, 0xcc, Mid, High).pos(2),
        create_door(player, 'Thieves BK Corner NW', Nrml).dir(Direction.North, 0xcc, Left, High).pos(1),
        create_door(player, 'Thieves BK Corner NE', Nrml).dir(Direction.North, 0xcc, Right, High).big_key().pos(0),
        create_door(player, 'Thieves Compass Room NW Edge', Open).dir(Direction.North, 0xdc, None, Low),
        create_door(player, 'Thieves Compass Room N Edge', Open).dir(Direction.North, 0xdc, None, Low),
        create_door(player, 'Thieves Compass Room WS Edge', Open).dir(Direction.West, 0xdc, None, Low),
        create_door(player, 'Thieves Compass Room W', Nrml).dir(Direction.West, 0xdc, Mid, High).pos(0),
        create_door(player, 'Thieves Hallway SE', Nrml).dir(Direction.South, 0xbc, Right, High).small_key().pos(1),
        create_door(player, 'Thieves Hallway NE', Nrml).dir(Direction.North, 0xbc, Right, High).pos(7),
        create_door(player, 'Thieves Pot Alcove Mid WS', Nrml).dir(Direction.West, 0xbc, Bot, High).pos(5),
        create_door(player, 'Thieves Pot Alcove Bottom SW', Nrml).dir(Direction.South, 0xbc, Left, High).pos(3),
        create_door(player, 'Thieves Conveyor Maze WN', Nrml).dir(Direction.West, 0xbc, Top, High).pos(4),
        create_door(player, 'Thieves Hallway WS', Intr).dir(Direction.West, 0xbc, Bot, High).small_key().pos(0),
        create_door(player, 'Thieves Pot Alcove Mid ES', Intr).dir(Direction.East, 0xbc, Bot, High).small_key().pos(0),
        create_door(player, 'Thieves Conveyor Maze SW', Intr).dir(Direction.South, 0xbc, Left, High).pos(6),
        create_door(player, 'Thieves Pot Alcove Top NW', Intr).dir(Direction.North, 0xbc, Left, High).pos(6),
        create_door(player, 'Thieves Conveyor Maze EN', Intr).dir(Direction.East, 0xbc, Top, High).pos(2),
        create_door(player, 'Thieves Hallway WN', Intr).dir(Direction.West, 0xbc, Top, High).no_exit().pos(2),
        create_door(player, 'Thieves Conveyor Maze Down Stairs', Sprl).dir(Direction.Down, 0xbc, 0, HTH).ss(A, 0x11, 0x80, True, True),
        create_door(player, 'Thieves Boss SE', Nrml).dir(Direction.South, 0xac, Right, High).no_exit().trap(0x4).pos(0),
        create_door(player, 'Thieves Spike Track ES', Nrml).dir(Direction.East, 0xbb, Bot, High).pos(5),
        create_door(player, 'Thieves Hellway NW', Nrml).dir(Direction.North, 0xbb, Left, High).pos(0),
        create_door(player, 'Thieves Triple Bypass EN', Nrml).dir(Direction.East, 0xbb, Top, High).pos(4),
        create_door(player, 'Thieves Hellway Orange Barrier', Lgcl),
        create_door(player, 'Thieves Hellway Crystal Orange Barrier', Lgcl),
        create_door(player, 'Thieves Hellway Blue Barrier', Lgcl),
        create_door(player, 'Thieves Hellway Crystal Blue Barrier', Lgcl),
        create_door(player, 'Thieves Spike Track WS', Intr).dir(Direction.West, 0xbb, Bot, High).pos(2),
        create_door(player, 'Thieves Hellway Crystal ES', Intr).dir(Direction.East, 0xbb, Bot, High).pos(2),
        create_door(player, 'Thieves Spike Track NE', Intr).dir(Direction.North, 0xbb, Right, High).pos(3),
        create_door(player, 'Thieves Triple Bypass SE', Intr).dir(Direction.South, 0xbb, Right, High).pos(3),
        create_door(player, 'Thieves Hellway Crystal EN', Intr).dir(Direction.East, 0xbb, Top, High).pos(1),
        create_door(player, 'Thieves Triple Bypass WN', Intr).dir(Direction.West, 0xbb, Top, High).pos(1),
        create_door(player, 'Thieves Spike Switch SW', Nrml).dir(Direction.South, 0xab, Left, High).pos(1),
        create_door(player, 'Thieves Spike Switch Up Stairs', Sprl).dir(Direction.Up, 0xab, 0, HTH).ss(Z, 0x1a, 0x6c, True, True).small_key().pos(0),
        create_door(player, 'Thieves Attic Down Stairs', Sprl).dir(Direction.Down, 0x64, 0, HTH).ss(Z, 0x11, 0x80, True, True),
        create_door(player, 'Thieves Attic ES', Intr).dir(Direction.East, 0x64, Bot, High).pos(0),
        create_door(player, 'Thieves Cricket Hall Left WS', Intr).dir(Direction.West, 0x64, Bot, High).pos(0),
        create_door(player, 'Thieves Cricket Hall Left Edge', Open).dir(Direction.East, 0x64, None, High),
        create_door(player, 'Thieves Cricket Hall Right Edge', Open).dir(Direction.West, 0x65, None, High),
        create_door(player, 'Thieves Cricket Hall Right ES', Intr).dir(Direction.East, 0x65, Bot, High).pos(0),
        create_door(player, 'Thieves Attic Window WS', Intr).dir(Direction.West, 0x65, Bot, High).pos(0),
        create_door(player, 'Thieves Basement Block Up Stairs', Sprl).dir(Direction.Up, 0x45, 0, HTH).ss(A, 0x1a, 0x6c, True, True),
        create_door(player, 'Thieves Basement Block WN', Nrml).dir(Direction.West, 0x45, Top, High).trap(0x4).pos(0),
        create_door(player, 'Thieves Basement Block Path', Lgcl),
        create_door(player, 'Thieves Blocked Entry Path', Lgcl),
        create_door(player, 'Thieves Lonely Zazak WS', Nrml).dir(Direction.West, 0x45, Bot, High).pos(2),
        create_door(player, 'Thieves Blocked Entry SW', Intr).dir(Direction.South, 0x45, Left, High).pos(1),
        create_door(player, 'Thieves Lonely Zazak NW', Intr).dir(Direction.North, 0x45, Left, High).pos(1),
        create_door(player, 'Thieves Lonely Zazak ES', Intr).dir(Direction.East, 0x45, Right, High).pos(3),
        create_door(player, 'Thieves Blind\'s Cell WS', Intr).dir(Direction.West, 0x45, Right, High).pos(3),
        create_door(player, 'Thieves Conveyor Bridge EN', Nrml).dir(Direction.East, 0x44, Top, High).pos(2),
        create_door(player, 'Thieves Conveyor Bridge ES', Nrml).dir(Direction.East, 0x44, Bot, High).pos(3),
        create_door(player, 'Thieves Conveyor Bridge Block Path', Lgcl),
        create_door(player, 'Thieves Conveyor Block Path', Lgcl),
        create_door(player, 'Thieves Conveyor Bridge WS', Intr).dir(Direction.West, 0x44, Bot, High).small_key().pos(1),
        create_door(player, 'Thieves Big Chest Room ES', Intr).dir(Direction.East, 0x44, Bot, High).small_key().pos(1),
        create_door(player, 'Thieves Conveyor Block WN', Intr).dir(Direction.West, 0x44, Top, High).pos(0),
        create_door(player, 'Thieves Trap EN', Intr).dir(Direction.East, 0x44, Left, Top).pos(0),

        # Door Templates
        # create_door(player, '', Nrml).dir(Direction.North, 0x00, Mid, High).pos(),
        # create_door(player, '', Intr).dir(Direction.North, 0x00, Left, High).pos(),
        # create_door(player, '', Sprl).dir(Direction.North, 0x00, 0, High).ss(),
        # create_door(player, '', Open).dir(Direction.North, 0x00, None, High),
        # create_door(player, '', Lgcl),
        # create_door(player, '', Hole),
        # create_door(player, '', Warp),
    ]
    create_paired_doors(world, player)

    # swamp events
    world.get_door('Swamp Trench 1 Approach Key', player).event('Trench 1 Switch')
    world.get_door('Swamp Trench 1 Approach Swim Depart', player).event('Trench 1 Switch')
    world.get_door('Swamp Trench 1 Key Approach', player).event('Trench 1 Switch')
    world.get_door('Swamp Trench 1 Key Ledge Depart', player).event('Trench 1 Switch')
    world.get_door('Swamp Trench 1 Departure Approach', player).event('Trench 1 Switch')
    world.get_door('Swamp Trench 1 Departure Key', player).event('Trench 1 Switch')
    world.get_door('Swamp Trench 2 Pots Wet', player).event('Trench 2 Switch')
    world.get_door('Swamp Trench 2 Departure Wet', player).event('Trench 2 Switch')
    world.get_door('Swamp Drain WN', player).event('Swamp Drain')
    world.get_door('Swamp Flooded Room WS', player).event('Swamp Drain')
    world.get_door('Swamp Drain Right Switch', player).event('Swamp Drain')
    world.get_door('Swamp Flooded Room Ladder', player).event('Swamp Drain')

    # crystal switches and barriers
    world.get_door('Hera Lobby Down Stairs', player).c_switch()
    world.get_door('Hera Lobby Key Stairs', player).c_switch()
    world.get_door('Hera Lobby Up Stairs', player).c_switch()
    world.get_door('Hera Basement Cage Up Stairs', player).c_switch()
    world.get_door('Hera Tile Room Up Stairs', player).c_switch()
    world.get_door('Hera Tile Room EN', player).c_switch()
    world.get_door('Hera Tridorm WN', player).c_switch()
    world.get_door('Hera Tridorm SE', player).c_switch()
    world.get_door('Hera Beetles Down Stairs', player).c_switch()
    world.get_door('Hera Beetles WS', player).c_switch()
    world.get_door('Hera Beetles Holes', player).c_switch()
    world.get_door('Hera Startile Wide SW', player).c_switch()
    world.get_door('Hera Startile Wide Up Stairs', player).c_switch()
    world.get_door('Hera Startile Wide Holes', player).c_switch()

    world.get_door('PoD Arena Main SW', player).c_switch()
    world.get_door('PoD Arena Bridge SE', player).c_switch()
    world.get_door('PoD Arena Main NW', player).barrier(CrystalBarrier.Orange)
    world.get_door('PoD Arena Main NE', player).barrier(CrystalBarrier.Orange)
    # maybe you can cross this way with blue up??
    world.get_door('PoD Arena Main Crystal Path', player).barrier(CrystalBarrier.Blue)
    world.get_door('PoD Arena Crystals E', player).barrier(CrystalBarrier.Blue)
    world.get_door('PoD Arena Crystal Path', player).barrier(CrystalBarrier.Blue)
    world.get_door('PoD Sexy Statue W', player).c_switch()
    world.get_door('PoD Sexy Statue NW', player).c_switch()
    world.get_door('PoD Bow Statue SW', player).c_switch()
    world.get_door('PoD Bow Statue Down Ladder', player).c_switch()
    world.get_door('PoD Dark Pegs Up Ladder', player).c_switch()
    world.get_door('PoD Dark Pegs WN', player).c_switch()

    world.get_door('Swamp Crystal Switch EN', player).c_switch()
    world.get_door('Swamp Crystal Switch SE', player).c_switch()
    world.get_door('Swamp Shortcut Blue Barrier', player).barrier(CrystalBarrier.Blue)
    world.get_door('Swamp Trench 2 Pots Blue Barrier', player).barrier(CrystalBarrier.Blue)
    world.get_door('Swamp Barrier Ledge - Orange', player).barrier(CrystalBarrier.Orange)
    world.get_door('Swamp Barrier - Orange', player).barrier(CrystalBarrier.Orange)

    world.get_door('Thieves Spike Switch Up Stairs', player).c_switch()
    world.get_door('Thieves Spike Switch SW', player).c_switch()
    world.get_door('Thieves Attic ES', player).barrier(CrystalBarrier.Blue)
    world.get_door('Thieves Hellway Blue Barrier', player).barrier(CrystalBarrier.Blue)
    world.get_door('Thieves Hellway Crystal Blue Barrier', player).barrier(CrystalBarrier.Blue)
    world.get_door('Thieves Triple Bypass SE', player).barrier(CrystalBarrier.Blue)
    world.get_door('Thieves Triple Bypass WN', player).barrier(CrystalBarrier.Blue)
    world.get_door('Thieves Triple Bypass EN', player).barrier(CrystalBarrier.Blue)
    world.get_door('Thieves Hellway Orange Barrier', player).barrier(CrystalBarrier.Orange)
    world.get_door('Thieves Hellway Crystal Orange Barrier', player).barrier(CrystalBarrier.Orange)


def create_paired_doors(world, player):
    world.paired_doors[player] = [
        PairedDoor('Sewers Secret Room Key Door S', 'Sewers Key Rat Key Door N'),
        # PairedDoor('', ''),  # TR Pokey Key
        # PairedDoor('', ''),  # TR Big key door by pipes
        PairedDoor('PoD Falling Bridge WN', 'PoD Dark Maze EN'),  # Pod Dark maze door
        PairedDoor('PoD Dark Maze E', 'PoD Big Chest Balcony W'),  # PoD Bombable by Big Chest
        PairedDoor('PoD Arena Main NW', 'PoD Falling Bridge SW'),  # Pod key door by bridge
        PairedDoor('Sewers Dark Cross Key Door N', 'Sewers Dark Cross Key Door S'),
        PairedDoor('Swamp Hub WN', 'Swamp Crystal Switch EN'),  # Swamp key door crystal switch
        PairedDoor('Swamp Hub North Ledge N', 'Swamp Push Statue S'),  # Swamp key door above big chest
        PairedDoor('PoD Map Balcony WS', 'PoD Arena Ledge ES'),  # Pod bombable by arena
        PairedDoor('Swamp Hub Dead Ledge EN', 'Swamp Hammer Switch WN'),  # Swamp bombable to random pots
        PairedDoor('Swamp Pot Row WN', 'Swamp Map Ledge EN'),  # Swamp bombable to map chest
        PairedDoor('Swamp Pot Row WS', 'Swamp Trench 1 Approach ES'),  # Swamp key door early room $38
        PairedDoor('PoD Middle Cage N', 'PoD Pit Room S'),
        # PairedDoor('', ''),  # GT moldorm key door
        # PairedDoor('', ''),  # Ice BJ key door
        PairedDoor('Desert Tiles 2 SE', 'Desert Beamos Hall NE'),
        PairedDoor('Skull 3 Lobby NW', 'Skull Star Pits SW'),  # Skull 3 key door
        PairedDoor('Skull 1 Lobby WS', 'Skull Pot Prison ES'),  # Skull 1 key door - pot prison to big chest
        PairedDoor('Skull Map Room SE', 'Skull Pinball NE'),  # Skull 1 - pinball key door
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
        PairedDoor('Thieves BK Corner NW', 'Thieves Pot Alcove Bottom SW'),  # TT random bomb to pots
        PairedDoor('Thieves BK Corner NW', 'Thieves Hallway SE'),  # TT big key door
        # PairedDoor('', ''),  # Ice last key door to crystal switch
        # PairedDoor('', ''),  # mire hub key door to attic
        # PairedDoor('', ''),  # mire hub key door to map
        # PairedDoor('', ''),  # tr last key door to switch maze
        PairedDoor('Thieves Ambush E', 'Thieves BK Corner W')  # TT dashable above
    ]


def create_door(player, name, door_type):
    return Door(player, name, door_type)


def ugly_door(door):
    door.ugly = True
    return door
