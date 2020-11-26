from collections import defaultdict

from BaseClasses import PotItem, Pot, PotFlags, CrystalBarrier
from Regions import key_drop_data

movable_switch_rooms = defaultdict(lambda: [],
                                   {'PoD Stalfos Basement': ['PoD Basement Ledge'],
                                    'Thieves Attic': ['Thieves Attic Hint'],
                                    'Mire Hub Switch': ['Mire Hub', 'Mire Hub Right']})

invalid_key_rooms = {
    'Swamp Big Key Ledge',
    'Swamp Trench 2 Departure',
    'Desert Wall Slide',
    'Skull X Room',  # only required for 100% locations
    'GT Map Room',
    'GT Warp Maze - Mid Section'
}

vanilla_pots = {
    2: [Pot(80, 6, PotItem.Nothing, 'Sewers Yet More Rats'), Pot(80, 8, PotItem.Nothing, 'Sewers Yet More Rats'), Pot(44, 8, PotItem.Nothing, 'Sewers Yet More Rats'), Pot(44, 10, PotItem.Nothing, 'Sewers Yet More Rats')],
    4: [Pot(162, 25, PotItem.Nothing, 'TR Dash Room'), Pot(152, 25, PotItem.Nothing, 'TR Dash Room'), Pot(152, 22, PotItem.Nothing, 'TR Dash Room'), Pot(162, 22, PotItem.Nothing, 'TR Dash Room'), Pot(204, 19, PotItem.Bomb, 'TR Tongue Pull'),
        Pot(240, 19, PotItem.Bomb, 'TR Tongue Pull')],
    9: [Pot(12, 4, PotItem.OneRupee, 'PoD Shooter Room'), Pot(48, 4, PotItem.Heart, 'PoD Shooter Room'), Pot(12, 12, PotItem.Switch, 'PoD Shooter Room')],
    10: [Pot(96, 8, PotItem.Heart, 'PoD Stalfos Basement'), Pot(104, 8, PotItem.Heart, 'PoD Stalfos Basement'), Pot(204, 11, PotItem.Switch, 'PoD Stalfos Basement'), Pot(100, 9, PotItem.Nothing, 'PoD Stalfos Basement'),
         Pot(156, 17, PotItem.Bomb, 'PoD Basement Ledge', PotFlags.SwitchLogicChange), Pot(160, 17, PotItem.FiveArrows, 'PoD Basement Ledge', PotFlags.SwitchLogicChange)],
    11: [Pot(202, 3, PotItem.Bomb, 'PoD Dark Pegs'), Pot(202, 12, PotItem.Bomb, 'PoD Dark Pegs')],
    17: [Pot(152, 19, PotItem.Nothing, 'Sewers Secret Room'), Pot(152, 15, PotItem.Nothing, 'Sewers Secret Room'), Pot(144, 15, PotItem.Heart, 'Sewers Secret Room'), Pot(160, 15, PotItem.Heart, 'Sewers Secret Room'),
         Pot(144, 19, PotItem.Heart, 'Sewers Secret Room'), Pot(160, 19, PotItem.Heart, 'Sewers Secret Room')],
    21: [Pot(96, 4, PotItem.Bomb, 'TR Pipe Pit'), Pot(100, 4, PotItem.SmallMagic, 'TR Pipe Pit'), Pot(104, 4, PotItem.Heart, 'TR Pipe Pit'), Pot(108, 4, PotItem.SmallMagic, 'TR Pipe Pit'), Pot(112, 4, PotItem.FiveArrows, 'TR Pipe Pit'),
         Pot(12, 6, PotItem.OneRupee, 'TR Pipe Pit'), Pot(16, 6, PotItem.FiveArrows, 'TR Pipe Pit'), Pot(20, 6, PotItem.FiveRupees, 'TR Pipe Pit'), Pot(70, 11, PotItem.BigMagic, 'TR Pipe Ledge')],
    22: [Pot(188, 3, PotItem.Heart, 'Swamp I'), Pot(192, 3, PotItem.Heart, 'Swamp I'), Pot(188, 4, PotItem.SmallMagic, 'Swamp I'), Pot(192, 4, PotItem.SmallMagic, 'Swamp I'), Pot(188, 5, PotItem.FiveArrows, 'Swamp I'),
         Pot(192, 5, PotItem.FiveArrows, 'Swamp I'), Pot(188, 6, PotItem.Bomb, 'Swamp I'), Pot(192, 6, PotItem.Bomb, 'Swamp I'), Pot(240, 19, PotItem.Key, 'Swamp Waterway')],
    23: [Pot(100, 13, PotItem.Heart, 'Hera 5F'), Pot(100, 14, PotItem.Heart, 'Hera 5F'), Pot(100, 15, PotItem.Heart, 'Hera 5F'), Pot(100, 16, PotItem.Heart, 'Hera 5F'), Pot(100, 17, PotItem.Heart, 'Hera 5F'), Pot(100, 18, PotItem.Heart, 'Hera 5F'),
         Pot(104, 13, PotItem.Heart, 'Hera 5F'), Pot(104, 14, PotItem.Heart, 'Hera 5F'), Pot(104, 15, PotItem.Heart, 'Hera 5F'), Pot(104, 16, PotItem.Heart, 'Hera 5F'), Pot(104, 17, PotItem.Heart, 'Hera 5F'), Pot(104, 18, PotItem.Heart, 'Hera 5F')],
    26: [Pot(28, 5, PotItem.Bomb, 'PoD Falling Bridge Ledge'), Pot(32, 5, PotItem.Bomb, 'PoD Falling Bridge Ledge'), Pot(28, 27, PotItem.Bomb, 'PoD Falling Bridge'), Pot(32, 27, PotItem.Bomb, 'PoD Falling Bridge'),
         Pot(232, 19, PotItem.Nothing, 'PoD Harmless Hellway'), Pot(212, 19, PotItem.Nothing, 'PoD Harmless Hellway')],
    27: [Pot(20, 23, PotItem.FiveArrows, 'PoD Mimics 2'), Pot(40, 23, PotItem.FiveArrows, 'PoD Mimics 2')],
    30: [Pot(84, 9, PotItem.Bomb, 'Ice Bomb Drop')],
    31: [Pot(28, 25, PotItem.Switch, 'Ice Pengator Switch'), Pot(28, 23, PotItem.Nothing, 'Ice Pengator Switch'), Pot(86, 26, PotItem.Nothing, 'Ice Big Key'), Pot(86, 27, PotItem.Nothing, 'Ice Big Key')],
    33: [Pot(160, 20, PotItem.Nothing, 'Sewers Key Rat'), Pot(168, 24, PotItem.SmallMagic, 'Sewers Key Rat'), Pot(48, 28, PotItem.Heart, 'Sewers Key Rat'), Pot(82, 28, PotItem.SmallMagic, 'Sewers Key Rat'),
         Pot(100, 28, PotItem.Nothing, 'Sewers Key Rat'), Pot(104, 28, PotItem.Nothing, 'Sewers Key Rat')],
    35: [Pot(86, 26, PotItem.OneRupee, 'TR Lazy Eyes'), Pot(90, 26, PotItem.Heart, 'TR Lazy Eyes'), Pot(94, 26, PotItem.OneRupee, 'TR Lazy Eyes'), Pot(98, 26, PotItem.Bomb, 'TR Lazy Eyes'), Pot(102, 26, PotItem.OneRupee, 'TR Lazy Eyes')],
    36: [Pot(12, 4, PotItem.FiveRupees, 'TR Twin Pokeys'), Pot(48, 4, PotItem.Heart, 'TR Twin Pokeys'), Pot(12, 12, PotItem.SmallMagic, 'TR Twin Pokeys'), Pot(48, 12, PotItem.OneRupee, 'TR Twin Pokeys')],
    38: [Pot(28, 4, PotItem.Bomb, 'Swamp Shooters'), Pot(12, 8, PotItem.SmallMagic, 'Swamp Shooters'), Pot(150, 19, PotItem.Switch, 'Swamp Push Statue'), Pot(22, 26, PotItem.FiveRupees, 'Swamp Push Statue'),
         Pot(220, 26, PotItem.FiveArrows, 'Swamp Push Statue', PotFlags.SwitchLogicChange)],
    39: [Pot(214, 19, PotItem.Nothing, 'Hera 4F'), Pot(214, 20, PotItem.Nothing, 'Hera 4F'), Pot(166, 20, PotItem.Bomb, 'Hera 4F'), Pot(214, 21, PotItem.Heart, 'Hera 4F'), Pot(40, 28, PotItem.OneRupee, 'Hera 4F'),
         Pot(44, 28, PotItem.OneRupee, 'Hera 4F'), Pot(80, 28, PotItem.FiveRupees, 'Hera 4F'), Pot(84, 28, PotItem.FiveRupees, 'Hera 4F'), Pot(102, 17, PotItem.Nothing, 'Hera 4F'), Pot(98, 17, PotItem.Nothing, 'Hera 4F'),
         Pot(106, 17, PotItem.Nothing, 'Hera 4F'), Pot(166, 21, PotItem.Nothing, 'Hera 4F'), Pot(166, 19, PotItem.Nothing, 'Hera 4F'), Pot(92, 12, PotItem.Nothing, 'Hera 4F'), Pot(160, 12, PotItem.Nothing, 'Hera 4F')],
    42: [Pot(80, 12, PotItem.OneRupee, 'PoD Arena Main'), Pot(80, 19, PotItem.Heart, 'PoD Arena Main')],
    43: [Pot(16, 5, PotItem.Heart, 'PoD Sexy Statue'), Pot(44, 5, PotItem.Switch, 'PoD Sexy Statue'), Pot(16, 6, PotItem.Heart, 'PoD Sexy Statue'), Pot(44, 6, PotItem.Bomb, 'PoD Sexy Statue'), Pot(16, 7, PotItem.Heart, 'PoD Sexy Statue'),
         Pot(44, 7, PotItem.Bomb, 'PoD Sexy Statue'), Pot(146, 21, PotItem.Bomb, 'PoD Map Balcony'), Pot(170, 21, PotItem.FiveArrows, 'PoD Map Balcony'), Pot(146, 22, PotItem.Bomb, 'PoD Map Balcony'),
         Pot(170, 22, PotItem.FiveArrows, 'PoD Map Balcony')],
    44: [Pot(108, 24, PotItem.Heart, 'Hookshot Cave'), Pot(112, 24, PotItem.Heart, 'Hookshot Cave')],
    47: [Pot(28, 7, PotItem.Heart, 'Kakariko Well (top)'), Pot(32, 7, PotItem.Heart, 'Kakariko Well (top)'), Pot(28, 9, PotItem.FiveRupees, 'Kakariko Well (top)'), Pot(32, 9, PotItem.FiveRupees, 'Kakariko Well (top)'),
         Pot(172, 19, PotItem.FiveRupees, 'Kakariko Well (top)'), Pot(180, 19, PotItem.FiveRupees, 'Kakariko Well (top)'), Pot(104, 27, PotItem.Heart, 'Kakariko Well (bottom)'), Pot(104, 28, PotItem.Heart, 'Kakariko Well (bottom)')],
    49: [Pot(92, 28, PotItem.Bomb, 'Hera Beetles'), Pot(96, 28, PotItem.Nothing, 'Hera Beetles')],
    50: [Pot(28, 13, PotItem.SmallMagic, 'Sewers Dark Cross')],
    52: [Pot(78, 8, PotItem.FiveRupees, 'Swamp Barrier Ledge'), Pot(92, 8, PotItem.FiveRupees, 'Swamp Barrier Ledge')],
    53: [Pot(60, 6, PotItem.Key, 'Swamp Trench 2 Alcove'), Pot(20, 8, PotItem.FiveRupees, 'Swamp Big Key Ledge'), Pot(24, 8, PotItem.FiveRupees, 'Swamp Big Key Ledge'), Pot(28, 8, PotItem.FiveRupees, 'Swamp Big Key Ledge'),
         Pot(32, 8, PotItem.FiveRupees, 'Swamp Big Key Ledge'), Pot(36, 8, PotItem.FiveRupees, 'Swamp Big Key Ledge'), Pot(48, 20, PotItem.Heart, 'Swamp Trench 2 Departure'), Pot(76, 23, PotItem.Nothing, 'Swamp Trench 2 Pots'),
         Pot(88, 23, PotItem.Nothing, 'Swamp Trench 2 Pots'), Pot(100, 27, PotItem.Nothing, 'Swamp Trench 2 Pots'), Pot(242, 28, PotItem.Nothing, 'Swamp Trench 2 Pots'), Pot(240, 22, PotItem.Heart, 'Swamp Trench 2 Pots'),
         Pot(76, 28, PotItem.Heart, 'Swamp Trench 2 Pots')],
    54: [Pot(108, 4, PotItem.Bomb, 'Swamp Hub Dead Ledge'), Pot(112, 4, PotItem.FiveRupees, 'Swamp Hub Dead Ledge'), Pot(10, 16, PotItem.Heart, 'Swamp Hub'), Pot(154, 15, PotItem.Nothing, 'Swamp Hub'), Pot(114, 16, PotItem.Key, 'Swamp Hub'),
         Pot(222, 15, PotItem.Nothing, 'Swamp Hub'), Pot(188, 5, PotItem.Nothing, 'Swamp Hub North Ledge'), Pot(192, 5, PotItem.Nothing, 'Swamp Hub North Ledge')],
    55: [Pot(60, 6, PotItem.Key, 'Swamp Trench 1 Alcove'), Pot(48, 20, PotItem.Nothing, 'Swamp Trench 1 Key Ledge')],
    56: [Pot(164, 12, PotItem.Bomb, 'Swamp Pot Row'), Pot(164, 13, PotItem.FiveRupees, 'Swamp Pot Row'), Pot(164, 18, PotItem.Bomb, 'Swamp Pot Row'), Pot(164, 19, PotItem.Key, 'Swamp Pot Row')],
    57: [Pot(12, 20, PotItem.Heart, 'Skull Spike Corner'), Pot(48, 28, PotItem.FiveArrows, 'Skull Spike Corner'), Pot(100, 22, PotItem.SmallMagic, 'Skull Final Drop'), Pot(100, 26, PotItem.FiveArrows, 'Skull Final Drop')],
    60: [Pot(24, 8, PotItem.SmallMagic, 'Hookshot Cave'), Pot(64, 12, PotItem.FiveRupees, 'Hookshot Cave'), Pot(20, 14, PotItem.OneRupee, 'Hookshot Cave'), Pot(20, 19, PotItem.Nothing, 'Hookshot Cave'),
         Pot(68, 18, PotItem.FiveRupees, 'Hookshot Cave'), Pot(96, 19, PotItem.Heart, 'Hookshot Cave'), Pot(64, 20, PotItem.FiveRupees, 'Hookshot Cave'), Pot(64, 26, PotItem.FiveRupees, 'Hookshot Cave')],
    61: [Pot(76, 12, PotItem.Bomb, 'GT Mini Helmasaur Room'), Pot(112, 12, PotItem.Bomb, 'GT Mini Helmasaur Room'), Pot(24, 22, PotItem.Heart, 'GT Crystal Circles'), Pot(40, 22, PotItem.FiveArrows, 'GT Crystal Circles'),
         Pot(32, 24, PotItem.Heart, 'GT Crystal Circles'), Pot(20, 26, PotItem.FiveRupees, 'GT Crystal Circles'), Pot(36, 26, PotItem.BigMagic, 'GT Crystal Circles')],
    62: [Pot(96, 6, PotItem.Bomb, 'Ice Stalfos Hint'), Pot(100, 6, PotItem.SmallMagic, 'Ice Stalfos Hint'), Pot(88, 10, PotItem.Heart, 'Ice Stalfos Hint'), Pot(92, 10, PotItem.SmallMagic, 'Ice Stalfos Hint')],
    63: [Pot(12, 25, PotItem.OneRupee, 'Ice Hammer Block'), Pot(20, 25, PotItem.OneRupee, 'Ice Hammer Block'), Pot(12, 26, PotItem.Bomb, 'Ice Hammer Block'), Pot(20, 26, PotItem.Bomb, 'Ice Hammer Block'),
         Pot(12, 27, PotItem.Switch, 'Ice Hammer Block'), Pot(20, 27, PotItem.Heart, 'Ice Hammer Block'), Pot(28, 23, PotItem.Key, 'Ice Hammer Block')],
    65: [Pot(100, 10, PotItem.Heart, 'Sewers Behind Tapestry'), Pot(52, 15, PotItem.OneRupee, 'Sewers Behind Tapestry'), Pot(52, 16, PotItem.SmallMagic, 'Sewers Behind Tapestry'), Pot(148, 22, PotItem.SmallMagic, 'Sewers Behind Tapestry')],
    67: [Pot(66, 4, PotItem.FiveArrows, 'Desert Wall Slide'), Pot(78, 4, PotItem.SmallMagic, 'Desert Wall Slide'), Pot(66, 9, PotItem.Heart, 'Desert Wall Slide'), Pot(78, 9, PotItem.Heart, 'Desert Wall Slide'),
         Pot(112, 28, PotItem.Nothing, 'Desert Tiles 2'), Pot(76, 28, PotItem.Nothing, 'Desert Tiles 2'), Pot(76, 20, PotItem.Nothing, 'Desert Tiles 2'), Pot(112, 20, PotItem.Key, 'Desert Tiles 2')],
    69: [Pot(12, 4, PotItem.FiveArrows, 'Thieves Basement Block'), Pot(48, 12, PotItem.FiveArrows, 'Thieves Basement Block'), Pot(92, 11, PotItem.Nothing, "Thieves Blind's Cell"), Pot(108, 11, PotItem.Heart, "Thieves Blind's Cell"),
         Pot(220, 16, PotItem.SmallMagic, "Thieves Blind's Cell"), Pot(236, 16, PotItem.Heart, "Thieves Blind's Cell")],
    70: [Pot(96, 5, PotItem.Heart, 'Swamp Donut Top'), Pot(28, 27, PotItem.Heart, 'Swamp Donut Bottom')],
    73: [Pot(104, 15, PotItem.SmallMagic, 'Skull Torch Room'), Pot(104, 16, PotItem.SmallMagic, 'Skull Torch Room'), Pot(156, 27, PotItem.Nothing, 'Skull Star Pits'), Pot(172, 24, PotItem.Nothing, 'Skull Star Pits'),
         Pot(172, 23, PotItem.Nothing, 'Skull Star Pits'), Pot(144, 20, PotItem.Nothing, 'Skull Star Pits'), Pot(144, 19, PotItem.SmallMagic, 'Skull Star Pits'), Pot(172, 20, PotItem.Heart, 'Skull Star Pits'),
         Pot(144, 27, PotItem.Heart, 'Skull Star Pits'), Pot(172, 28, PotItem.SmallMagic, 'Skull Star Pits'), Pot(160, 27, PotItem.Nothing, 'Skull Star Pits')],
    74: [Pot(14, 5, PotItem.Switch, 'PoD Left Cage'), Pot(32, 5, PotItem.Bomb, 'PoD Left Cage'), Pot(14, 11, PotItem.Heart, 'PoD Left Cage'), Pot(32, 11, PotItem.OneRupee, 'PoD Left Cage'), Pot(56, 8, PotItem.Bomb, 'PoD Middle Cage'),
         Pot(68, 8, PotItem.Bomb, 'PoD Middle Cage'), Pot(92, 5, PotItem.Bomb, 'PoD Middle Cage'), Pot(110, 5, PotItem.Switch, 'PoD Middle Cage'), Pot(92, 11, PotItem.OneRupee, 'PoD Middle Cage'), Pot(110, 11, PotItem.Heart, 'PoD Middle Cage')],
    75: [Pot(20, 6, PotItem.FiveArrows, 'PoD Mimics 1'), Pot(40, 6, PotItem.Heart, 'PoD Mimics 1')],
    78: [Pot(140, 7, PotItem.Nothing, 'Ice Bomb Jump Catwalk'), Pot(48, 10, PotItem.Nothing, 'Ice Bomb Jump Catwalk'), Pot(140, 11, PotItem.Switch, 'Ice Bomb Jump Catwalk'), Pot(28, 12, PotItem.Heart, 'Ice Bomb Jump Catwalk'),
         Pot(112, 12, PotItem.SmallMagic, 'Ice Narrow Corridor')],
    80: [Pot(96, 38, PotItem.Heart, 'Hyrule Castle West Hall'), Pot(100, 38, PotItem.Heart, 'Hyrule Castle West Hall')],
    82: [Pot(138, 3, PotItem.Heart, 'Hyrule Castle East Hall'), Pot(194, 26, PotItem.Heart, 'Hyrule Castle East Hall')],
    83: [Pot(92, 11, PotItem.Heart, 'Desert Beamos Hall'), Pot(96, 11, PotItem.SmallMagic, 'Desert Beamos Hall'), Pot(100, 11, PotItem.Key, 'Desert Beamos Hall'), Pot(104, 11, PotItem.Heart, 'Desert Beamos Hall')],
    84: [Pot(186, 25, PotItem.FiveRupees, 'Swamp Attic'), Pot(186, 26, PotItem.Heart, 'Swamp Attic'), Pot(186, 27, PotItem.Heart, 'Swamp Attic'), Pot(186, 28, PotItem.Heart, 'Swamp Attic')],
    85: [Pot(230, 24, PotItem.SmallMagic, 'Secret Passage'), Pot(230, 25, PotItem.SmallMagic, 'Secret Passage')],
    86: [Pot(100, 6, PotItem.Nothing, 'Skull Back Drop'), Pot(96, 10, PotItem.Nothing, 'Skull Back Drop'), Pot(92, 10, PotItem.Nothing, 'Skull Back Drop'), Pot(20, 6, PotItem.SmallMagic, 'Skull X Room'),
         Pot(40, 6, PotItem.SmallMagic, 'Skull X Room'), Pot(24, 7, PotItem.SmallMagic, 'Skull X Room'), Pot(36, 7, PotItem.SmallMagic, 'Skull X Room'), Pot(12, 8, PotItem.Heart, 'Skull X Room'), Pot(48, 8, PotItem.Heart, 'Skull X Room'),
         Pot(24, 9, PotItem.SmallMagic, 'Skull X Room'), Pot(36, 9, PotItem.SmallMagic, 'Skull X Room'), Pot(20, 10, PotItem.FiveRupees, 'Skull X Room'), Pot(40, 10, PotItem.FiveRupees, 'Skull X Room'), Pot(12, 20, PotItem.Key, 'Skull 2 West Lobby'),
         Pot(48, 20, PotItem.Nothing, 'Skull 2 West Lobby')],
    87: [Pot(92, 7, PotItem.BigMagic, 'Skull Lone Pot'), Pot(32, 4, PotItem.Nothing, 'Skull Big Key'), Pot(92, 23, PotItem.Bomb, 'Skull Pot Prison'), Pot(100, 23, PotItem.SmallMagic, 'Skull Pot Prison'),
         Pot(84, 25, PotItem.FiveRupees, 'Skull Pot Prison'), Pot(76, 27, PotItem.Heart, 'Skull Pot Prison'), Pot(12, 20, PotItem.SmallMagic, 'Skull 2 East Lobby'), Pot(48, 20, PotItem.SmallMagic, 'Skull 2 East Lobby'),
         Pot(30, 22, PotItem.Switch, 'Skull 2 East Lobby')],
    88: [Pot(12, 7, PotItem.SmallMagic, 'Skull Pull Switch'), Pot(16, 7, PotItem.Nothing, 'Skull Pull Switch'), Pot(16, 8, PotItem.SmallMagic, 'Skull Pull Switch'), Pot(12, 12, PotItem.Nothing, 'Skull Pull Switch'),
         Pot(96, 9, PotItem.Nothing, 'Skull Pot Circle'), Pot(92, 8, PotItem.Nothing, 'Skull Pot Circle'), Pot(108, 8, PotItem.Nothing, 'Skull Pot Circle'), Pot(108, 6, PotItem.Nothing, 'Skull Pot Circle'),
         Pot(104, 5, PotItem.Nothing, 'Skull Pot Circle'), Pot(92, 6, PotItem.Nothing, 'Skull Pot Circle'), Pot(96, 5, PotItem.Bomb, 'Skull Pot Circle'), Pot(100, 5, PotItem.SmallMagic, 'Skull Pot Circle'),
         Pot(92, 7, PotItem.Heart, 'Skull Pot Circle'), Pot(108, 7, PotItem.Heart, 'Skull Pot Circle'), Pot(100, 9, PotItem.SmallMagic, 'Skull Pot Circle'), Pot(104, 9, PotItem.Bomb, 'Skull Pot Circle')],
    89: [Pot(26, 43, PotItem.Heart, 'Skull 3 Lobby'), Pot(32, 40, PotItem.Nothing, 'Skull 3 Lobby'), Pot(76, 28, PotItem.Nothing, 'Skull East Bridge'), Pot(112, 28, PotItem.Nothing, 'Skull East Bridge')],
    91: [Pot(218, 37, PotItem.Nothing, 'GT Hidden Spikes'), Pot(222, 37, PotItem.Switch, 'GT Hidden Spikes'), Pot(226, 37, PotItem.Nothing, 'GT Hidden Spikes')],
    92: [Pot(228, 25, PotItem.Nothing, 'GT Refill'), Pot(104, 24, PotItem.Nothing, 'GT Refill'), Pot(228, 22, PotItem.Nothing, 'GT Refill'), Pot(216, 25, PotItem.Nothing, 'GT Refill'), Pot(84, 24, PotItem.Nothing, 'GT Refill'),
         Pot(216, 22, PotItem.Nothing, 'GT Refill'), Pot(94, 22, PotItem.Bomb, 'GT Refill'), Pot(94, 26, PotItem.BigMagic, 'GT Refill')],
    93: [Pot(16, 5, PotItem.Bomb, 'GT Gauntlet 2'), Pot(44, 5, PotItem.FiveRupees, 'GT Gauntlet 2'), Pot(16, 11, PotItem.OneRupee, 'GT Gauntlet 2'), Pot(44, 11, PotItem.FiveArrows, 'GT Gauntlet 2'), Pot(12, 20, PotItem.FiveArrows, 'GT Gauntlet 3'),
         Pot(48, 20, PotItem.Bomb, 'GT Gauntlet 3'), Pot(12, 28, PotItem.SmallMagic, 'GT Gauntlet 3'), Pot(48, 28, PotItem.Bomb, 'GT Gauntlet 3')],
    94: [Pot(92, 4, PotItem.SmallMagic, 'Ice Falling Square'), Pot(96, 4, PotItem.SmallMagic, 'Ice Falling Square'), Pot(76, 8, PotItem.Heart, 'Ice Falling Square'), Pot(112, 8, PotItem.Heart, 'Ice Falling Square')],
    95: [Pot(44, 27, PotItem.Switch, 'Ice Spike Room')],
    96: [Pot(76, 4, PotItem.Heart, 'Hyrule Castle West Lobby'), Pot(112, 4, PotItem.Heart, 'Hyrule Castle West Lobby')],
    98: [Pot(208, 21, PotItem.Heart, 'Hyrule Castle East Lobby')],
    99: [Pot(48, 4, PotItem.Nothing, 'Desert Tiles 1'), Pot(12, 4, PotItem.Nothing, 'Desert Tiles 1'), Pot(12, 8, PotItem.Nothing, 'Desert Tiles 1'), Pot(48, 12, PotItem.Nothing, 'Desert Tiles 1'), Pot(48, 8, PotItem.Heart, 'Desert Tiles 1'),
         Pot(12, 12, PotItem.Key, 'Desert Tiles 1')],
    100: [Pot(12, 22, PotItem.Bomb, 'Thieves Attic Hint', PotFlags.SwitchLogicChange), Pot(16, 22, PotItem.Bomb, 'Thieves Attic Hint', PotFlags.SwitchLogicChange), Pot(20, 22, PotItem.Bomb, 'Thieves Attic Hint', PotFlags.SwitchLogicChange),
          Pot(36, 28, PotItem.Bomb, 'Thieves Attic'), Pot(40, 28, PotItem.SmallMagic, 'Thieves Attic'),
          Pot(44, 28, PotItem.SmallMagic, 'Thieves Attic'), Pot(48, 28, PotItem.Switch, 'Thieves Attic')],
    101: [Pot(100, 28, PotItem.Bomb, 'Thieves Attic Window'), Pot(104, 28, PotItem.Bomb, 'Thieves Attic Window')],
    102: [Pot(48, 37, PotItem.FiveArrows, 'Swamp Refill'), Pot(52, 37, PotItem.Bomb, 'Swamp Refill'), Pot(56, 37, PotItem.FiveRupees, 'Swamp Refill'), Pot(48, 38, PotItem.FiveArrows, 'Swamp Refill'), Pot(52, 38, PotItem.Bomb, 'Swamp Refill'),
          Pot(56, 38, PotItem.FiveRupees, 'Swamp Refill'), Pot(84, 5, PotItem.Heart, 'Swamp Behind Waterfall'), Pot(104, 5, PotItem.FiveArrows, 'Swamp Behind Waterfall'), Pot(84, 6, PotItem.Heart, 'Swamp Behind Waterfall'),
          Pot(104, 6, PotItem.Bomb, 'Swamp Behind Waterfall')],
    103: [Pot(22, 26, PotItem.Nothing, 'Skull Left Drop'), Pot(18, 22, PotItem.Nothing, 'Skull Left Drop'), Pot(12, 7, PotItem.FiveArrows, 'Skull Left Drop'), Pot(48, 7, PotItem.SmallMagic, 'Skull Left Drop'),
          Pot(18, 23, PotItem.SmallMagic, 'Skull Left Drop'), Pot(18, 26, PotItem.Heart, 'Skull Left Drop'), Pot(96, 19, PotItem.Heart, 'Skull Compass Room'), Pot(74, 20, PotItem.SmallMagic, 'Skull Compass Room'),
          Pot(92, 9, PotItem.Nothing, 'Skull Compass Room'), Pot(84, 28, PotItem.Nothing, 'Skull Compass Room'), Pot(104, 28, PotItem.Heart, 'Skull Compass Room')],
    104: [Pot(84, 14, PotItem.Nothing, 'Skull Pinball'), Pot(84, 13, PotItem.Nothing, 'Skull Pinball'), Pot(88, 12, PotItem.Nothing, 'Skull Pinball'), Pot(88, 6, PotItem.Nothing, 'Skull Pinball'), Pot(88, 5, PotItem.Nothing, 'Skull Pinball'),
          Pot(88, 4, PotItem.Nothing, 'Skull Pinball'), Pot(64, 17, PotItem.Nothing, 'Skull Pinball'), Pot(64, 15, PotItem.Nothing, 'Skull Pinball'), Pot(64, 7, PotItem.Heart, 'Skull Pinball'), Pot(88, 7, PotItem.SmallMagic, 'Skull Pinball'),
          Pot(64, 16, PotItem.Heart, 'Skull Pinball'), Pot(64, 24, PotItem.SmallMagic, 'Skull Pinball'), Pot(64, 25, PotItem.Heart, 'Skull Pinball')],
    107: [Pot(28, 5, PotItem.Heart, 'GT Crystal Paths'), Pot(44, 5, PotItem.Nothing, 'GT Crystal Paths'), Pot(28, 8, PotItem.Nothing, 'GT Crystal Paths'), Pot(44, 8, PotItem.SmallMagic, 'GT Crystal Paths'),
          Pot(28, 11, PotItem.SmallMagic, 'GT Crystal Paths'), Pot(44, 11, PotItem.Nothing, 'GT Crystal Paths'), Pot(94, 25, PotItem.Nothing, 'GT Mimics 2'), Pot(98, 25, PotItem.FiveArrows, 'GT Mimics 2')],
    108: [Pot(20, 6, PotItem.Heart, 'GT Quad Pot'), Pot(40, 6, PotItem.FiveArrows, 'GT Quad Pot'), Pot(20, 10, PotItem.Bomb, 'GT Quad Pot'), Pot(40, 10, PotItem.SmallMagic, 'GT Quad Pot')],
    109: [Pot(28, 26, PotItem.Heart, 'GT Gauntlet 5'), Pot(32, 26, PotItem.Heart, 'GT Gauntlet 5'), Pot(28, 27, PotItem.SmallMagic, 'GT Gauntlet 5'), Pot(32, 27, PotItem.SmallMagic, 'GT Gauntlet 5')],
    115: [Pot(154, 21, PotItem.FiveArrows, 'Desert Circle of Pots'), Pot(158, 21, PotItem.OneRupee, 'Desert Circle of Pots'), Pot(20, 23, PotItem.Switch, 'Desert Circle of Pots'), Pot(36, 23, PotItem.FiveRupees, 'Desert Circle of Pots'),
          Pot(144, 24, PotItem.Heart, 'Desert Circle of Pots'), Pot(168, 24, PotItem.FiveArrows, 'Desert Circle of Pots'), Pot(20, 26, PotItem.SmallMagic, 'Desert Circle of Pots'), Pot(36, 26, PotItem.Heart, 'Desert Circle of Pots'),
          Pot(154, 27, PotItem.OneRupee, 'Desert Circle of Pots'), Pot(158, 27, PotItem.FiveRupees, 'Desert Circle of Pots')],
    116: [Pot(30, 5, PotItem.SmallMagic, 'Desert Map Room'), Pot(62, 5, PotItem.Switch, 'Desert Map Room'), Pot(94, 5, PotItem.SmallMagic, 'Desert Map Room'), Pot(14, 11, PotItem.Heart, 'Desert Map Room'),
          Pot(46, 11, PotItem.FiveArrows, 'Desert Map Room'), Pot(78, 11, PotItem.FiveArrows, 'Desert Map Room'), Pot(110, 11, PotItem.Heart, 'Desert Map Room')],
    117: [Pot(148, 22, PotItem.SmallMagic, 'Desert Arrow Pot Corner'), Pot(160, 22, PotItem.FiveArrows, 'Desert Arrow Pot Corner'), Pot(172, 22, PotItem.Heart, 'Desert Arrow Pot Corner')],
    118: [Pot(112, 12, PotItem.Heart, 'Swamp Drain Right'), Pot(84, 23, PotItem.Heart, 'Swamp Flooded Spot'), Pot(96, 23, PotItem.Heart, 'Swamp Flooded Spot')],
    123: [Pot(48, 10, PotItem.Nothing, 'GT Conveyor Star Pits'), Pot(88, 10, PotItem.Nothing, 'GT Conveyor Star Pits'), Pot(76, 7, PotItem.Nothing, 'GT Conveyor Star Pits'), Pot(60, 4, PotItem.Heart, 'GT Conveyor Star Pits'),
          Pot(64, 4, PotItem.Key, 'GT Conveyor Star Pits')],
    124: [Pot(36, 21, PotItem.Nothing, 'GT Falling Bridge'), Pot(24, 11, PotItem.Nothing, 'GT Falling Bridge'), Pot(28, 4, PotItem.Heart, 'GT Falling Bridge'), Pot(32, 4, PotItem.Heart, 'GT Falling Bridge')],
    125: [Pot(44, 12, PotItem.Nothing, 'GT Firesnake Room'), Pot(44, 6, PotItem.Nothing, 'GT Firesnake Room'), Pot(112, 6, PotItem.Heart, 'GT Firesnake Room'), Pot(108, 20, PotItem.FiveArrows, 'GT Warp Maze - Pot Rail'),
          Pot(114, 20, PotItem.Bomb, 'GT Petting Zoo'), Pot(76, 28, PotItem.Bomb, 'GT Petting Zoo')],
    126: [Pot(86, 15, PotItem.Heart, 'Ice Tall Hint'), Pot(82, 26, PotItem.SmallMagic, 'Ice Tall Hint'), Pot(100, 26, PotItem.Switch, 'Ice Tall Hint'), Pot(104, 26, PotItem.Nothing, 'Ice Tall Hint')],
    128: [Pot(48, 4, PotItem.Heart, 'Hyrule Dungeon Cellblock'), Pot(52, 4, PotItem.Heart, 'Hyrule Dungeon Cellblock'), Pot(56, 4, PotItem.Heart, 'Hyrule Dungeon Cellblock')],
    130: [Pot(50, 5, PotItem.Nothing, 'Hyrule Dungeon South Abyss'), Pot(50, 10, PotItem.Nothing, 'Hyrule Dungeon South Abyss'), Pot(76, 50, PotItem.Heart, 'Hyrule Dungeon South Abyss')],
    131: [Pot(76, 4, PotItem.FiveArrows, 'Desert West Wing'), Pot(80, 4, PotItem.OneRupee, 'Desert West Wing'), Pot(76, 28, PotItem.FiveRupees, 'Desert West Wing'), Pot(80, 28, PotItem.FiveArrows, 'Desert West Wing')],
    132: [Pot(64, 17, PotItem.Nothing, 'Desert Main Lobby'), Pot(60, 17, PotItem.Nothing, 'Desert Main Lobby'), Pot(80, 14, PotItem.Nothing, 'Desert Main Lobby'), Pot(44, 14, PotItem.Nothing, 'Desert Main Lobby'),
          Pot(100, 6, PotItem.Nothing, 'Desert Main Lobby'), Pot(24, 6, PotItem.Nothing, 'Desert Main Lobby'), Pot(24, 7, PotItem.FiveArrows, 'Desert Main Lobby'), Pot(100, 7, PotItem.FiveArrows, 'Desert Main Lobby')],
    133: [Pot(44, 28, PotItem.Heart, 'Desert East Wing'), Pot(48, 28, PotItem.FiveArrows, 'Desert East Wing')],
    135: [Pot(12, 11, PotItem.Nothing, 'Hera Tile Room'), Pot(16, 12, PotItem.Nothing, 'Hera Tile Room'), Pot(40, 12, PotItem.Nothing, 'Hera Tile Room'), Pot(32, 12, PotItem.Nothing, 'Hera Tile Room'), Pot(24, 12, PotItem.Nothing, 'Hera Tile Room'),
          Pot(16, 11, PotItem.Nothing, 'Hera Tile Room'), Pot(76, 20, PotItem.SmallMagic, 'Hera Torches'), Pot(112, 20, PotItem.BigMagic, 'Hera Torches')],
    139: [Pot(76, 12, PotItem.Nothing, 'GT Conveyor Cross'), Pot(112, 12, PotItem.Key, 'GT Conveyor Cross'), Pot(32, 23, PotItem.Nothing, 'GT Hookshot South Platform'), Pot(28, 23, PotItem.Nothing, 'GT Hookshot South Platform'),
          Pot(32, 9, PotItem.SmallMagic, 'GT Hookshot East Platform'), Pot(76, 20, PotItem.Nothing, 'GT Map Room'), Pot(76, 28, PotItem.Heart, 'GT Map Room')],
    140: [Pot(76, 12, PotItem.Switch, 'GT Hope Room'), Pot(112, 12, PotItem.SmallMagic, 'GT Hope Room'), Pot(76, 20, PotItem.Bomb, "GT Bob's Room"), Pot(92, 20, PotItem.Bomb, "GT Bob's Room"), Pot(100, 21, PotItem.FiveArrows, "GT Bob's Room"),
          Pot(104, 26, PotItem.Bomb, "GT Bob's Room"), Pot(88, 27, PotItem.Bomb, "GT Bob's Room")],
    141: [Pot(204, 11, PotItem.Nothing, 'GT Speed Torch Upper'), Pot(204, 14, PotItem.BigMagic, 'GT Speed Torch Upper'), Pot(28, 23, PotItem.Heart, 'GT Pots n Blocks'), Pot(36, 23, PotItem.Heart, 'GT Pots n Blocks'),
          Pot(32, 24, PotItem.BigMagic, 'GT Pots n Blocks')],
    142: [Pot(80, 5, PotItem.FiveArrows, 'Ice Lonely Freezor'), Pot(80, 6, PotItem.Nothing, 'Ice Lonely Freezor')],
    145: [Pot(84, 4, PotItem.Heart, 'Mire Falling Foes'), Pot(104, 4, PotItem.SmallMagic, 'Mire Falling Foes')],
    146: [Pot(86, 23, PotItem.Nothing, 'Mire Tall Dark and Roomy'), Pot(92, 23, PotItem.Nothing, 'Mire Tall Dark and Roomy'), Pot(98, 23, PotItem.Nothing, 'Mire Tall Dark and Roomy'), Pot(104, 23, PotItem.Nothing, 'Mire Tall Dark and Roomy')],
    147: [Pot(28, 7, PotItem.Switch, 'Mire Dark Shooters'), Pot(96, 7, PotItem.Heart, 'Mire Dark Shooters', PotFlags.NoSwitch)],
    150: [Pot(14, 18, PotItem.Nothing, 'GT Torch Cross'), Pot(32, 5, PotItem.Nothing, 'GT Torch Cross'), Pot(32, 17, PotItem.SmallMagic, 'GT Torch Cross'), Pot(32, 24, PotItem.SmallMagic, 'GT Torch Cross'),
          Pot(14, 24, PotItem.Nothing, 'GT Torch Cross'), Pot(76, 21, PotItem.Heart, 'GT Staredown'), Pot(112, 21, PotItem.BigMagic, 'GT Staredown')],
    153: [Pot(40, 20, PotItem.SmallMagic, 'Eastern Darkness'), Pot(84, 20, PotItem.Heart, 'Eastern Darkness')],
    155: [Pot(48, 4, PotItem.SmallMagic, 'GT Double Switch Key Spot'), Pot(48, 12, PotItem.Key, 'GT Double Switch Key Spot'), Pot(28, 24, PotItem.Nothing, 'GT Warp Maze - Mid Section'), Pot(32, 24, PotItem.Nothing, 'GT Warp Maze - Mid Section')],
    156: [Pot(56, 8, PotItem.SmallMagic, 'GT Invisible Catwalk'), Pot(56, 9, PotItem.FiveArrows, 'GT Invisible Catwalk')],
    157: [Pot(76, 4, PotItem.Bomb, 'GT Crystal Conveyor'), Pot(84, 4, PotItem.SmallMagic, 'GT Crystal Conveyor'), Pot(32, 7, PotItem.Nothing, 'GT Compass Room'), Pot(40, 9, PotItem.Nothing, 'GT Compass Room')],
    159: [Pot(138, 20, PotItem.Nothing, 'Ice Many Pots'), Pot(138, 19, PotItem.Heart, 'Ice Many Pots'), Pot(178, 19, PotItem.Heart, 'Ice Many Pots'), Pot(40, 21, PotItem.Switch, 'Ice Many Pots'), Pot(138, 21, PotItem.Key, 'Ice Many Pots'),
          Pot(20, 27, PotItem.Heart, 'Ice Many Pots'), Pot(138, 27, PotItem.Heart, 'Ice Many Pots'), Pot(178, 28, PotItem.Heart, 'Ice Many Pots'), Pot(178, 21, PotItem.Nothing, 'Ice Many Pots'), Pot(178, 20, PotItem.Nothing, 'Ice Many Pots'),
          Pot(40, 27, PotItem.Nothing, 'Ice Many Pots'), Pot(178, 27, PotItem.Nothing, 'Ice Many Pots'), Pot(178, 26, PotItem.Nothing, 'Ice Many Pots'), Pot(138, 28, PotItem.Nothing, 'Ice Many Pots'), Pot(138, 26, PotItem.Nothing, 'Ice Many Pots'),
          Pot(20, 21, PotItem.Nothing, 'Ice Many Pots')],
    161: [Pot(150, 6, PotItem.Key, 'Mire Fishbone'), Pot(100, 11, PotItem.SmallMagic, 'Mire Fishbone'), Pot(104, 12, PotItem.Heart, 'Mire Fishbone'), Pot(108, 13, PotItem.SmallMagic, 'Mire Fishbone'), Pot(112, 14, PotItem.Heart, 'Mire Fishbone'),
          Pot(96, 27, PotItem.Nothing, 'Mire South Fish'), Pot(92, 21, PotItem.Nothing, 'Mire South Fish'), Pot(96, 23, PotItem.Heart, 'Mire South Fish'), Pot(92, 25, PotItem.Nothing, 'Mire South Fish'),
          Pot(76, 28, PotItem.Nothing, 'Mire South Fish'), Pot(112, 28, PotItem.Nothing, 'Mire South Fish')],
    162: [Pot(12, 28, PotItem.BigMagic, 'Mire Left Bridge')],
    168: [Pot(138, 28, PotItem.Nothing, 'Eastern Stalfos Spawn'), Pot(178, 28, PotItem.Nothing, 'Eastern Stalfos Spawn'), Pot(178, 19, PotItem.Nothing, 'Eastern Stalfos Spawn'), Pot(138, 19, PotItem.Heart, 'Eastern Stalfos Spawn'),
          Pot(30, 24, PotItem.OneRupee, 'Eastern Stalfos Spawn')],
    169: [Pot(144, 43, PotItem.FiveArrows, 'Eastern Courtyard'), Pot(236, 43, PotItem.FiveArrows, 'Eastern Courtyard'), Pot(144, 44, PotItem.FiveArrows, 'Eastern Courtyard'), Pot(236, 44, PotItem.Heart, 'Eastern Courtyard'),
          Pot(12, 19, PotItem.Nothing, 'Eastern Courtyard Ledge'), Pot(112, 19, PotItem.Nothing, 'Eastern Courtyard Ledge'), Pot(16, 20, PotItem.Heart, 'Eastern Courtyard Ledge'), Pot(108, 20, PotItem.Heart, 'Eastern Courtyard Ledge')],
    170: [Pot(212, 10, PotItem.Nothing, 'Eastern Pot Switch'), Pot(232, 10, PotItem.Nothing, 'Eastern Pot Switch'), Pot(232, 5, PotItem.Nothing, 'Eastern Pot Switch'), Pot(212, 5, PotItem.Heart, 'Eastern Pot Switch'),
          Pot(94, 8, PotItem.Switch, 'Eastern Pot Switch'), Pot(108, 55, PotItem.Heart, 'Eastern Map Balcony'), Pot(108, 56, PotItem.Heart, 'Eastern Map Balcony'), Pot(108, 57, PotItem.Heart, 'Eastern Map Balcony')],
    171: [Pot(20, 24, PotItem.Key, 'Thieves Spike Switch')],
    174: [Pot(76, 12, PotItem.Switch, 'Iced T')],
    176: [Pot(20, 27, PotItem.Nothing, 'Tower Circle of Pots'), Pot(24, 24, PotItem.Nothing, 'Tower Circle of Pots'), Pot(44, 25, PotItem.Nothing, 'Tower Circle of Pots'), Pot(20, 21, PotItem.Bomb, 'Tower Circle of Pots'),
          Pot(28, 21, PotItem.OneRupee, 'Tower Circle of Pots'), Pot(32, 21, PotItem.FiveRupees, 'Tower Circle of Pots'), Pot(40, 21, PotItem.FiveArrows, 'Tower Circle of Pots'), Pot(16, 23, PotItem.FiveRupees, 'Tower Circle of Pots'),
          Pot(44, 23, PotItem.OneRupee, 'Tower Circle of Pots'), Pot(36, 24, PotItem.Heart, 'Tower Circle of Pots'), Pot(16, 25, PotItem.Heart, 'Tower Circle of Pots'), Pot(28, 27, PotItem.FiveArrows, 'Tower Circle of Pots'),
          Pot(40, 27, PotItem.Bomb, 'Tower Circle of Pots'), Pot(32, 27, PotItem.Nothing, 'Tower Circle of Pots')],
    177: [Pot(76, 4, PotItem.Heart, 'Mire Spike Barrier'), Pot(112, 4, PotItem.OneRupee, 'Mire Spike Barrier')],
    178: [Pot(48, 40, PotItem.OneRupee, 'Mire BK Door Room'), Pot(76, 40, PotItem.OneRupee, 'Mire BK Door Room'), Pot(48, 41, PotItem.Nothing, 'Mire BK Door Room'), Pot(76, 41, PotItem.Heart, 'Mire BK Door Room'),
          Pot(48, 42, PotItem.Nothing, 'Mire BK Door Room'), Pot(76, 40, PotItem.Nothing, 'Mire BK Door Room')],
    179: [Pot(12, 20, PotItem.Key, 'Mire Spikes'), Pot(48, 20, PotItem.SmallMagic, 'Mire Spikes'), Pot(48, 28, PotItem.Switch, 'Mire Spikes')],
    180: [Pot(44, 28, PotItem.BigMagic, 'TR Final Abyss'), Pot(48, 28, PotItem.Heart, 'TR Final Abyss')],
    181: [Pot(112, 4, PotItem.FiveRupees, 'TR Dark Ride'), Pot(112, 15, PotItem.Heart, 'TR Dark Ride'), Pot(76, 16, PotItem.Switch, 'TR Dark Ride'), Pot(112, 16, PotItem.BigMagic, 'TR Dark Ride'), Pot(112, 17, PotItem.Heart, 'TR Dark Ride'),
          Pot(112, 28, PotItem.Bomb, 'TR Dark Ride')],
    182: [Pot(94, 9, PotItem.BigMagic, 'TR Refill')],
    183: [Pot(30, 5, PotItem.SmallMagic, 'TR Roller Room')],
    184: [Pot(96, 13, PotItem.Switch, 'Eastern Big Key'), Pot(88, 16, PotItem.Heart, 'Eastern Big Key'), Pot(104, 16, PotItem.Heart, 'Eastern Big Key')],
    185: [Pot(92, 18, PotItem.OneRupee, 'Eastern Cannonball'), Pot(96, 18, PotItem.FiveRupees, 'Eastern Cannonball'), Pot(104, 18, PotItem.FiveRupees, 'Eastern Cannonball'), Pot(108, 18, PotItem.OneRupee, 'Eastern Cannonball')],
    186: [Pot(100, 8, PotItem.Nothing, 'Eastern Dark Pots'), Pot(88, 8, PotItem.Nothing, 'Eastern Dark Pots'), Pot(94, 4, PotItem.OneRupee, 'Eastern Dark Pots'), Pot(76, 6, PotItem.Heart, 'Eastern Dark Pots'),
          Pot(112, 6, PotItem.Key, 'Eastern Dark Pots'), Pot(76, 10, PotItem.Heart, 'Eastern Dark Pots'), Pot(112, 10, PotItem.SmallMagic, 'Eastern Dark Pots'), Pot(94, 12, PotItem.OneRupee, 'Eastern Dark Pots')],
    188: [Pot(86, 4, PotItem.Heart, 'Thieves Hallway'), Pot(102, 4, PotItem.Key, 'Thieves Hallway'), Pot(138, 3, PotItem.Bomb, 'Thieves Conveyor Maze'), Pot(178, 3, PotItem.Switch, 'Thieves Conveyor Maze'),
          Pot(138, 12, PotItem.Heart, 'Thieves Conveyor Maze'), Pot(178, 12, PotItem.Bomb, 'Thieves Conveyor Maze'), Pot(12, 20, PotItem.Nothing, 'Thieves Pot Alcove Mid'), Pot(48, 20, PotItem.Bomb, 'Thieves Pot Alcove Mid'),
          Pot(12, 28, PotItem.Bomb, 'Thieves Pot Alcove Mid'), Pot(48, 28, PotItem.Bomb, 'Thieves Pot Alcove Mid'), Pot(28, 21, PotItem.FiveRupees, 'Thieves Pot Alcove Top'), Pot(32, 21, PotItem.FiveRupees, 'Thieves Pot Alcove Top'),
          Pot(28, 27, PotItem.FiveRupees, 'Thieves Pot Alcove Bottom'), Pot(32, 27, PotItem.FiveRupees, 'Thieves Pot Alcove Bottom')],
    190: [Pot(92, 25, PotItem.Switch, 'Ice Switch Room')],
    191: [Pot(40, 20, PotItem.FiveArrows, 'Ice Refill'), Pot(44, 20, PotItem.Heart, 'Ice Refill'), Pot(48, 20, PotItem.Bomb, 'Ice Refill'), Pot(40, 28, PotItem.SmallMagic, 'Ice Refill'), Pot(44, 28, PotItem.SmallMagic, 'Ice Refill'),
          Pot(48, 28, PotItem.SmallMagic, 'Ice Refill')],
    192: [Pot(48, 10, PotItem.Bomb, 'Tower Dark Pits'), Pot(12, 14, PotItem.FiveRupees, 'Tower Dark Pits'), Pot(12, 26, PotItem.Heart, 'Tower Dark Pits'), Pot(28, 27, PotItem.OneRupee, 'Tower Dark Pits')],
    194: [Pot(180, 7, PotItem.Switch, 'Mire Hub Switch'), Pot(100, 46, PotItem.SmallMagic, 'Mire Hub Right'), Pot(68, 48, PotItem.OneRupee, 'Mire Hub'), Pot(64, 52, PotItem.FiveArrows, 'Mire Hub')],
    196: [Pot(84, 9, PotItem.Bomb, 'TR Crystal Maze'), Pot(24, 14, PotItem.Heart, 'TR Crystal Maze'), Pot(56, 17, PotItem.FiveRupees, 'TR Crystal Maze'), Pot(84, 17, PotItem.Bomb, 'TR Crystal Maze'),
          Pot(12, 21, PotItem.FiveArrows, 'TR Crystal Maze'), Pot(76, 23, PotItem.OneRupee, 'TR Crystal Maze'), Pot(48, 25, PotItem.SmallMagic, 'TR Crystal Maze'), Pot(12, 26, PotItem.Heart, 'TR Crystal Maze')],
    198: [Pot(12, 7, PotItem.BigMagic, 'TR Hub'), Pot(12, 25, PotItem.Heart, 'TR Hub')],
    199: [Pot(12, 10, PotItem.Heart, 'TR Torches'), Pot(12, 11, PotItem.BigMagic, 'TR Torches'), Pot(12, 22, PotItem.SmallMagic, 'TR Torches Ledge'), Pot(12, 28, PotItem.FiveArrows, 'TR Torches Ledge')],
    201: [Pot(30, 22, PotItem.OneRupee, 'Eastern Lobby'), Pot(94, 22, PotItem.OneRupee, 'Eastern Lobby'), Pot(60, 22, PotItem.Switch, 'Eastern Lobby')],
    203: [Pot(80, 4, PotItem.Nothing, 'Thieves Ambush'), Pot(80, 28, PotItem.Nothing, 'Thieves Ambush'), Pot(88, 16, PotItem.Heart, 'Thieves Ambush'), Pot(88, 28, PotItem.FiveRupees, 'Thieves Ambush')],
    204: [Pot(36, 4, PotItem.FiveRupees, 'Thieves Rail Ledge'), Pot(36, 28, PotItem.FiveRupees, 'Thieves Rail Ledge'), Pot(112, 4, PotItem.Heart, 'Thieves BK Corner'), Pot(112, 28, PotItem.Bomb, 'Thieves BK Corner')],
    206: [Pot(76, 8, PotItem.SmallMagic, 'Ice Antechamber'), Pot(80, 8, PotItem.SmallMagic, 'Ice Antechamber'), Pot(108, 12, PotItem.Bomb, 'Ice Antechamber'), Pot(112, 12, PotItem.FiveArrows, 'Ice Antechamber'),
          Pot(204, 11, PotItem.Hole, 'Ice Antechamber')],
    208: [Pot(158, 5, PotItem.SmallMagic, 'Tower Dark Maze'), Pot(140, 11, PotItem.OneRupee, 'Tower Dark Maze'), Pot(42, 13, PotItem.SmallMagic, 'Tower Dark Maze'), Pot(48, 16, PotItem.Heart, 'Tower Dark Maze'),
          Pot(176, 20, PotItem.OneRupee, 'Tower Dark Maze'), Pot(146, 23, PotItem.FiveRupees, 'Tower Dark Maze'), Pot(12, 28, PotItem.Heart, 'Tower Dark Maze')],
    209: [Pot(48, 4, PotItem.BigMagic, 'Mire Conveyor Barrier'), Pot(168, 7, PotItem.OneRupee, 'Mire Conveyor Barrier'), Pot(76, 4, PotItem.OneRupee, 'Mire Neglected Room'), Pot(112, 4, PotItem.FiveArrows, 'Mire Neglected Room'),
          Pot(76, 12, PotItem.Nothing, 'Mire Neglected Room'), Pot(112, 12, PotItem.OneRupee, 'Mire Neglected Room')],
    214: [Pot(92, 22, PotItem.BigMagic, 'TR Main Lobby'), Pot(96, 22, PotItem.Bomb, 'TR Main Lobby')],
    216: [Pot(202, 8, PotItem.Heart, 'Eastern Duo Eyegores'), Pot(242, 8, PotItem.FiveArrows, 'Eastern Duo Eyegores'), Pot(202, 10, PotItem.FiveArrows, 'Eastern Duo Eyegores'), Pot(242, 10, PotItem.FiveArrows, 'Eastern Duo Eyegores'),
          Pot(202, 12, PotItem.FiveArrows, 'Eastern Duo Eyegores'), Pot(242, 12, PotItem.Heart, 'Eastern Duo Eyegores'), Pot(92, 24, PotItem.Heart, 'Eastern Single Eyegore'), Pot(96, 24, PotItem.FiveArrows, 'Eastern Single Eyegore')],
    217: [Pot(92, 20, PotItem.FiveArrows, 'Eastern False Switches'), Pot(92, 28, PotItem.Heart, 'Eastern False Switches')],
    218: [Pot(24, 23, PotItem.FiveArrows, 'Eastern Attic Start'), Pot(36, 23, PotItem.FiveArrows, 'Eastern Attic Start'), Pot(24, 25, PotItem.Switch, 'Eastern Attic Start'), Pot(36, 25, PotItem.Heart, 'Eastern Attic Start')],
    219: [Pot(12, 4, PotItem.Nothing, 'Thieves Lobby'), Pot(62, 19, PotItem.Nothing, 'Thieves Lobby'), Pot(112, 4, PotItem.FiveRupees, 'Thieves Lobby'), Pot(88, 16, PotItem.Heart, 'Thieves Lobby')],
    220: [Pot(56, 4, PotItem.FiveRupees, 'Thieves Compass Room'), Pot(112, 4, PotItem.Bomb, 'Thieves Compass Room'), Pot(68, 16, PotItem.Heart, 'Thieves Compass Room'), Pot(12, 28, PotItem.FiveArrows, 'Thieves Compass Room')],
    227: [Pot(88, 55, PotItem.Nothing, 'Bat Cave (right)'), Pot(100, 57, PotItem.OneRupee, 'Bat Cave (right)')],
    228: [Pot(32, 9, PotItem.FiveRupees, 'Old Man House'), Pot(112, 10, PotItem.OneRupee, 'Old Man House')],
    229: [Pot(48, 4, PotItem.OneRupee, 'Old Man House Back'), Pot(76, 4, PotItem.OneRupee, 'Old Man House Back'), Pot(112, 16, PotItem.OneRupee, 'Old Man House Back'), Pot(64, 18, PotItem.FiveRupees, 'Old Man House Back')],
    230: [Pot(108, 12, PotItem.FiveArrows, 'Death Mountain Return Cave'), Pot(88, 16, PotItem.Heart, 'Death Mountain Return Cave'), Pot(72, 20, PotItem.Nothing, 'Death Mountain Return Cave'),
          Pot(56, 24, PotItem.OneRupee, 'Death Mountain Return Cave')],
    231: [Pot(68, 5, PotItem.OneRupee, 'Death Mountain Return Cave'), Pot(72, 5, PotItem.OneRupee, 'Death Mountain Return Cave')],
    232: [Pot(96, 4, PotItem.Heart, 'Superbunny Cave')],
    235: [Pot(206, 8, PotItem.FiveRupees, 'Bumper Cave'), Pot(210, 8, PotItem.FiveRupees, 'Bumper Cave'), Pot(88, 14, PotItem.SmallMagic, 'Bumper Cave'), Pot(92, 14, PotItem.Heart, 'Bumper Cave'), Pot(96, 14, PotItem.SmallMagic, 'Bumper Cave')],
    241: [Pot(64, 5, PotItem.Heart, 'Old Man Cave')],
    248: [Pot(242, 13, PotItem.BigMagic, 'Superbunny Cave')],
    253: [Pot(88, 6, PotItem.FiveRupees, 'Fairy Ascension Cave (Top)'), Pot(100, 6, PotItem.FiveRupees, 'Fairy Ascension Cave (Top)'), Pot(84, 23, PotItem.FiveRupees, 'Fairy Ascension Cave (Bottom)'),
          Pot(84, 24, PotItem.FiveRupees, 'Fairy Ascension Cave (Bottom)')],
    255: [Pot(92, 8, PotItem.Heart, 'Paradox Cave'), Pot(96, 8, PotItem.Heart, 'Paradox Cave'), Pot(112, 28, PotItem.OneRupee, 'Paradox Cave Front')],
    257: [Pot(12, 20, PotItem.Heart, 'Snitch Lady (East)'), Pot(224, 19, PotItem.Chicken, 'Snitch Lady (West)'), Pot(228, 19, PotItem.Heart, 'Snitch Lady (West)')],
    258: [Pot(146, 19, PotItem.Heart, 'Sick Kids House'), Pot(150, 19, PotItem.Heart, 'Sick Kids House')],
    259: [Pot(140, 7, PotItem.Chicken, 'Tavern'), Pot(140, 9, PotItem.Nothing, 'Tavern'), Pot(12, 12, PotItem.Heart, 'Tavern (Front)')],
    260: [Pot(202, 21, PotItem.Heart, 'Links House'), Pot(202, 22, PotItem.Heart, 'Links House'), Pot(202, 23, PotItem.Heart, 'Links House')],
    261: [Pot(30, 20, PotItem.Heart, 'Sahasrahlas Hut'), Pot(28, 21, PotItem.Heart, 'Sahasrahlas Hut'), Pot(32, 21, PotItem.Heart, 'Sahasrahlas Hut')],
    263: [Pot(214, 23, PotItem.Bomb, 'Light World Bomb Hut'), Pot(222, 23, PotItem.FiveArrows, 'Light World Bomb Hut'), Pot(230, 23, PotItem.Bomb, 'Light World Bomb Hut'), Pot(214, 25, PotItem.OneRupee, 'Light World Bomb Hut'),
          Pot(222, 25, PotItem.Nothing, 'Light World Bomb Hut'), Pot(230, 25, PotItem.OneRupee, 'Light World Bomb Hut'), Pot(214, 27, PotItem.Bomb, 'Light World Bomb Hut'), Pot(230, 27, PotItem.Bomb, 'Light World Bomb Hut')],
    264: [Pot(166, 19, PotItem.Chicken, 'Chicken House')],
    268: [Pot(88, 14, PotItem.Heart, 'Hookshot Fairy')],
    276: [Pot(92, 4, PotItem.Heart, 'Dark Desert Hint'), Pot(96, 4, PotItem.Heart, 'Dark Desert Hint'), Pot(92, 5, PotItem.Bomb, 'Dark Desert Hint'), Pot(96, 5, PotItem.Bomb, 'Dark Desert Hint'), Pot(92, 10, PotItem.FiveArrows, 'Dark Desert Hint'),
          Pot(96, 10, PotItem.Heart, 'Dark Desert Hint')],
    279: [Pot(138, 3, PotItem.Heart, 'Spike Cave'), Pot(142, 3, PotItem.Heart, 'Spike Cave'), Pot(166, 3, PotItem.Heart, 'Spike Cave'), Pot(170, 3, PotItem.Heart, 'Spike Cave'), Pot(138, 4, PotItem.Heart, 'Spike Cave'),
          Pot(142, 4, PotItem.Heart, 'Spike Cave'), Pot(166, 4, PotItem.Heart, 'Spike Cave'), Pot(170, 4, PotItem.Heart, 'Spike Cave')],
    281: [Pot(44, 28, PotItem.Heart, 'Blinds Hideout'), Pot(48, 28, PotItem.OneRupee, 'Blinds Hideout'), Pot(76, 28, PotItem.Heart, 'Blinds Hideout'), Pot(80, 28, PotItem.Heart, 'Blinds Hideout')],
    282: [Pot(214, 10, PotItem.Heart, 'Palace of Darkness Hint'), Pot(218, 10, PotItem.Heart, 'Palace of Darkness Hint'), Pot(226, 10, PotItem.Heart, 'Palace of Darkness Hint'), Pot(230, 10, PotItem.Heart, 'Palace of Darkness Hint')],
    283: [Pot(24, 53, PotItem.Nothing, 'Cave 45'), Pot(24, 54, PotItem.Heart, 'Cave 45'), Pot(32, 54, PotItem.Heart, 'Cave 45'), Pot(40, 54, PotItem.Heart, 'Cave 45'), Pot(24, 55, PotItem.Heart, 'Cave 45'), Pot(28, 56, PotItem.Heart, 'Cave 45'),
          Pot(92, 22, PotItem.Bomb, 'Graveyard Cave'), Pot(96, 22, PotItem.Heart, 'Graveyard Cave'), Pot(92, 23, PotItem.Bomb, 'Graveyard Cave'), Pot(96, 23, PotItem.Heart, 'Graveyard Cave'), Pot(92, 24, PotItem.Bomb, 'Graveyard Cave'),
          Pot(96, 24, PotItem.Heart, 'Graveyard Cave'), Pot(92, 25, PotItem.Bomb, 'Graveyard Cave'), Pot(96, 25, PotItem.Heart, 'Graveyard Cave')],
    285: [Pot(60, 6, PotItem.FiveRupees, 'Blinds Hideout'), Pot(64, 6, PotItem.FiveRupees, 'Blinds Hideout'), Pot(60, 7, PotItem.FiveRupees, 'Blinds Hideout'), Pot(64, 7, PotItem.FiveRupees, 'Blinds Hideout'),
          Pot(60, 8, PotItem.FiveRupees, 'Blinds Hideout'), Pot(64, 8, PotItem.FiveRupees, 'Blinds Hideout')],
    287: [Pot(174, 28, PotItem.Heart, 'Lumberjack House'), Pot(178, 28, PotItem.Heart, 'Lumberjack House')],
    292: [Pot(20, 20, PotItem.FiveRupees, '50 Rupee Cave'), Pot(40, 20, PotItem.FiveRupees, '50 Rupee Cave'), Pot(20, 21, PotItem.FiveRupees, '50 Rupee Cave'), Pot(40, 21, PotItem.FiveRupees, '50 Rupee Cave'),
          Pot(20, 22, PotItem.FiveRupees, '50 Rupee Cave'), Pot(40, 22, PotItem.FiveRupees, '50 Rupee Cave'), Pot(24, 24, PotItem.FiveRupees, '50 Rupee Cave'), Pot(28, 24, PotItem.FiveRupees, '50 Rupee Cave'),
          Pot(32, 24, PotItem.FiveRupees, '50 Rupee Cave'), Pot(36, 24, PotItem.FiveRupees, '50 Rupee Cave')],
    293: [Pot(24, 25, PotItem.FiveRupees, '20 Rupee Cave'), Pot(28, 25, PotItem.FiveRupees, '20 Rupee Cave'), Pot(32, 25, PotItem.FiveRupees, '20 Rupee Cave'), Pot(36, 25, PotItem.FiveRupees, '20 Rupee Cave'),
          Pot(88, 22, PotItem.Heart, 'Dev Cave Hint'), Pot(100, 22, PotItem.Heart, 'Dev Cave Hint'), Pot(88, 28, PotItem.Heart, 'Dev Cave Hint'), Pot(100, 28, PotItem.Heart, 'Dev Cave Hint')],
    295: [Pot(24, 25, PotItem.Nothing, 'Hammer Pegs Cave'), Pot(28, 25, PotItem.Nothing, 'Hammer Pegs Cave'), Pot(32, 25, PotItem.Nothing, 'Hammer Pegs Cave'), Pot(36, 25, PotItem.Nothing, 'Hammer Pegs Cave')],
}


def shuffle_pots(world, player):
    import random

    new_pot_contents = {}

    for supertile in vanilla_pots:
        old_pots = vanilla_pots[supertile]
        new_pots = [Pot(pot.x, pot.y, PotItem.Nothing, pot.room, pot.flags) for pot in old_pots]
        # sort in the order Hole, Switch, Key, Other, Nothing
        sort_order = {PotItem.Hole: 4, PotItem.Switch: 3, PotItem.Key: 2, PotItem.Nothing: 0}
        old_pots = sorted(old_pots, key=lambda pot: sort_order.get(pot.item, 1), reverse=True)

        for old_pot in old_pots:
            if old_pot.item == PotItem.Nothing:
                break
            elif old_pot.item == PotItem.Hole:
                # Can only go in vanilla position (or the other big rock)
                available_pots = (pot for pot in new_pots if pot.x == old_pot.x and pot.y == old_pot.y)
            elif old_pot.item == PotItem.Switch:
                available_pots = (pot for pot in new_pots if (pot.room == old_pot.room or pot.room in movable_switch_rooms[old_pot.room]) and not (pot.flags & PotFlags.NoSwitch))
            elif old_pot.item == PotItem.Key:
                if world.doorShuffle[player] == 'vanilla' and not world.retro[player] and not world.keydropshuffle[player] and world.logic != 'nologic':
                    available_pots = (pot for pot in new_pots if pot.room not in invalid_key_rooms)
                else:
                    available_pots = new_pots
            else:
                available_pots = new_pots

            available_pots = [pot for pot in available_pots if pot.item == PotItem.Nothing]

            new_pot = random.choice(available_pots)
            new_pot.item = old_pot.item
            if world.retro[player] and new_pot.item == PotItem.FiveArrows:
                new_pot.item = PotItem.FiveRupees

            if new_pot.item == PotItem.Key and new_pot.room != old_pot.room:
                # Move pot key to new room
                key = next(location for location in world.get_region(old_pot.room, player).locations if location.name in key_drop_data)
                world.get_region(old_pot.room, player).locations.remove(key)
                world.get_region(new_pot.room, player).locations.append(key)
                key.parent_region = world.get_region(new_pot.room, player)
            elif new_pot.item == PotItem.Switch and (new_pot.flags & PotFlags.SwitchLogicChange):
                if new_pot.room == 'PoD Basement Ledge':
                    basement = world.get_region(old_pot.room, player)
                    ledge = world.get_region(new_pot.room, player)
                    ledge.locations.append(basement.locations.pop())
                elif new_pot.room == 'Swamp Push Statue':
                    from Rules import set_rule
                    set_rule(world.get_entrance('Swamp Push Statue NE', player), lambda state: state.has('Cane of Somaria', player))
                    world.get_door('Swamp Push Statue NW', player).blocked = True
                elif new_pot.room == 'Thieves Attic Hint':
                    # Rule is created based on barrier
                    world.get_door('Thieves Attic ES', player).barrier(CrystalBarrier.Orange)
                else:
                    raise Exception("Switch locattion in room %s requires logic change" % new_pot.room)

        new_pot_contents[supertile] = new_pots

    world.pot_contents[player] = new_pot_contents
