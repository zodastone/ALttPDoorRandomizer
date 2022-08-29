import aioconsole
import argparse
import asyncio
import colorama
import json
import logging
import shlex
import urllib.parse
import websockets

import Items
import Regions


class ReceivedItem:
    def __init__(self, item, location, player):
        self.item = item
        self.location = location
        self.player = player

class Context:
    def __init__(self, snes_address, server_address, password):
        self.snes_address = snes_address
        self.server_address = server_address

        self.exit_event = asyncio.Event()
        self.watcher_event = asyncio.Event()

        self.input_queue = asyncio.Queue()
        self.input_requests = 0

        self.snes_socket = None
        self.snes_state = SNES_DISCONNECTED
        self.snes_attached_device = None
        self.snes_reconnect_address = None
        self.snes_recv_queue = asyncio.Queue()
        self.snes_request_lock = asyncio.Lock()
        self.is_sd2snes = False
        self.snes_write_buffer = []

        self.server_task = None
        self.socket = None
        self.password = password

        self.team = None
        self.slot = None
        self.player_names = {}
        self.locations_checked = set()
        self.locations_scouted = set()
        self.items_received = []
        self.locations_info = {}
        self.awaiting_rom = False
        self.rom = None
        self.auth = None
        self.total_locations = None
        self.mode_flags = None
        self.key_drop_mode = False
        self.shop_mode = False
        self.retro_mode = False
        self.ignore_count = 0

def color_code(*args):
    codes = {'reset': 0, 'bold': 1, 'underline': 4, 'black': 30, 'red': 31, 'green': 32, 'yellow': 33, 'blue': 34,
             'magenta': 35, 'cyan': 36, 'white': 37 , 'black_bg': 40, 'red_bg': 41, 'green_bg': 42, 'yellow_bg': 43,
             'blue_bg': 44, 'purple_bg': 45, 'cyan_bg': 46, 'white_bg': 47}
    return '\033[' + ';'.join([str(codes[arg]) for arg in args]) + 'm'

def color(text, *args):
    return color_code(*args) + text + color_code('reset')

RECONNECT_DELAY = 30

ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

ROMNAME_START = SRAM_START + 0x2000
ROMNAME_SIZE = 0x15

INGAME_MODES = {0x07, 0x09, 0x0b}

SAVEDATA_START = WRAM_START + 0xF000
SAVEDATA_SIZE = 0x500

RECV_PROGRESS_ADDR = SAVEDATA_START + 0x4D0         # 2 bytes
RECV_ITEM_ADDR = SAVEDATA_START + 0x4D2             # 1 byte
RECV_ITEM_PLAYER_ADDR = SAVEDATA_START + 0x4D3      # 1 byte
ROOMID_ADDR = SAVEDATA_START + 0x4D4                # 2 bytes
ROOMDATA_ADDR = SAVEDATA_START + 0x4D6              # 1 byte
SCOUT_LOCATION_ADDR = SAVEDATA_START + 0x4D7        # 1 byte
SCOUTREPLY_LOCATION_ADDR = SAVEDATA_START + 0x4D8   # 1 byte
SCOUTREPLY_ITEM_ADDR = SAVEDATA_START + 0x4D9       # 1 byte
SCOUTREPLY_PLAYER_ADDR = SAVEDATA_START + 0x4DA     # 1 byte
SHOP_ADDR = SAVEDATA_START + 0x302                  # 2 bytes?
DYNAMIC_TOTAL_ADDR = SAVEDATA_START + 0x33E         # 2 bytes
MODE_FLAGS = SAVEDATA_START + 0x33D         # 1 byte

SHOP_SRAM_LEN = 0x29  # 41 tracked items
location_shop_order = [Regions.shop_to_location_table.keys()] + [Regions.retro_shops.keys()]
location_shop_ids = {0x0112, 0x0110, 0x010F, 0x00FF, 0x011F, 0x0109, 0x0115}

location_table_uw = {"Blind's Hideout - Top": (0x11d, 0x10),
                     "Blind's Hideout - Left": (0x11d, 0x20),
                     "Blind's Hideout - Right": (0x11d, 0x40),
                     "Blind's Hideout - Far Left": (0x11d, 0x80),
                     "Blind's Hideout - Far Right": (0x11d, 0x100),
                     'Secret Passage': (0x55, 0x10),
                     'Waterfall Fairy - Left': (0x114, 0x10),
                     'Waterfall Fairy - Right': (0x114, 0x20),
                     "King's Tomb": (0x113, 0x10),
                     'Floodgate Chest': (0x10b, 0x10),
                     "Link's House": (0x104, 0x10),
                     'Kakariko Tavern': (0x103, 0x10),
                     'Chicken House': (0x108, 0x10),
                     "Aginah's Cave": (0x10a, 0x10),
                     "Sahasrahla's Hut - Left": (0x105, 0x10),
                     "Sahasrahla's Hut - Middle": (0x105, 0x20),
                     "Sahasrahla's Hut - Right": (0x105, 0x40),
                     'Kakariko Well - Top': (0x2f, 0x10),
                     'Kakariko Well - Left': (0x2f, 0x20),
                     'Kakariko Well - Middle': (0x2f, 0x40),
                     'Kakariko Well - Right': (0x2f, 0x80),
                     'Kakariko Well - Bottom': (0x2f, 0x100),
                     'Lost Woods Hideout': (0xe1, 0x200),
                     'Lumberjack Tree': (0xe2, 0x200),
                     'Cave 45': (0x11b, 0x400),
                     'Graveyard Cave': (0x11b, 0x200),
                     'Checkerboard Cave': (0x126, 0x200),
                     'Mini Moldorm Cave - Far Left': (0x123, 0x10),
                     'Mini Moldorm Cave - Left': (0x123, 0x20),
                     'Mini Moldorm Cave - Right': (0x123, 0x40),
                     'Mini Moldorm Cave - Far Right': (0x123, 0x80),
                     'Mini Moldorm Cave - Generous Guy': (0x123, 0x400),
                     'Ice Rod Cave': (0x120, 0x10),
                     'Bonk Rock Cave': (0x124, 0x10),
                     'Desert Palace - Big Chest': (0x73, 0x10),
                     'Desert Palace - Torch': (0x73, 0x400),
                     'Desert Palace - Map Chest': (0x74, 0x10),
                     'Desert Palace - Compass Chest': (0x85, 0x10),
                     'Desert Palace - Big Key Chest': (0x75, 0x10),
                     'Desert Palace - Desert Tiles 1 Pot Key': (0x63, 0x400),
                     'Desert Palace - Beamos Hall Pot Key': (0x53, 0x400),
                     'Desert Palace - Desert Tiles 2 Pot Key': (0x43, 0x400),
                     'Desert Palace - Boss': (0x33, 0x800),
                     'Eastern Palace - Compass Chest': (0xa8, 0x10),
                     'Eastern Palace - Big Chest': (0xa9, 0x10),
                     'Eastern Palace - Dark Square Pot Key': (0xba, 0x400),
                     'Eastern Palace - Dark Eyegore Key Drop': (0x99, 0x400),
                     'Eastern Palace - Cannonball Chest': (0xb9, 0x10),
                     'Eastern Palace - Big Key Chest': (0xb8, 0x10),
                     'Eastern Palace - Map Chest': (0xaa, 0x10),
                     'Eastern Palace - Boss': (0xc8, 0x800),
                     'Hyrule Castle - Boomerang Chest': (0x71, 0x10),
                     'Hyrule Castle - Boomerang Guard Key Drop': (0x71, 0x400),
                     'Hyrule Castle - Map Chest': (0x72, 0x10),
                     'Hyrule Castle - Map Guard Key Drop': (0x72, 0x400),
                     "Hyrule Castle - Zelda's Chest": (0x80, 0x10),
                     'Hyrule Castle - Big Key Drop': (0x80, 0x400),
                     'Sewers - Dark Cross': (0x32, 0x10),
                     'Hyrule Castle - Key Rat Key Drop': (0x21, 0x400),
                     'Sewers - Secret Room - Left': (0x11, 0x10),
                     'Sewers - Secret Room - Middle': (0x11, 0x20),
                     'Sewers - Secret Room - Right': (0x11, 0x40),
                     'Sanctuary': (0x12, 0x10),
                     'Castle Tower - Room 03': (0xe0, 0x10),
                     'Castle Tower - Dark Maze': (0xd0, 0x10),
                     'Castle Tower - Dark Archer Key Drop': (0xc0, 0x400),
                     'Castle Tower - Circle of Pots Key Drop': (0xb0, 0x400),
                     'Spectacle Rock Cave': (0xea, 0x400),
                     'Paradox Cave Lower - Far Left': (0xef, 0x10),
                     'Paradox Cave Lower - Left': (0xef, 0x20),
                     'Paradox Cave Lower - Right': (0xef, 0x40),
                     'Paradox Cave Lower - Far Right': (0xef, 0x80),
                     'Paradox Cave Lower - Middle': (0xef, 0x100),
                     'Paradox Cave Upper - Left': (0xff, 0x10),
                     'Paradox Cave Upper - Right': (0xff, 0x20),
                     'Spiral Cave': (0xfe, 0x10),
                     'Tower of Hera - Basement Cage': (0x87, 0x400),
                     'Tower of Hera - Map Chest': (0x77, 0x10),
                     'Tower of Hera - Big Key Chest': (0x87, 0x10),
                     'Tower of Hera - Compass Chest': (0x27, 0x20),
                     'Tower of Hera - Big Chest': (0x27, 0x10),
                     'Tower of Hera - Boss': (0x7, 0x800),
                     'Hype Cave - Top': (0x11e, 0x10),
                     'Hype Cave - Middle Right': (0x11e, 0x20),
                     'Hype Cave - Middle Left': (0x11e, 0x40),
                     'Hype Cave - Bottom': (0x11e, 0x80),
                     'Hype Cave - Generous Guy': (0x11e, 0x400),
                     'Peg Cave': (0x127, 0x400),
                     'Pyramid Fairy - Left': (0x116, 0x10),
                     'Pyramid Fairy - Right': (0x116, 0x20),
                     'Brewery': (0x106, 0x10),
                     'C-Shaped House': (0x11c, 0x10),
                     'Chest Game': (0x106, 0x400),
                     'Mire Shed - Left': (0x10d, 0x10),
                     'Mire Shed - Right': (0x10d, 0x20),
                     'Superbunny Cave - Top': (0xf8, 0x10),
                     'Superbunny Cave - Bottom': (0xf8, 0x20),
                     'Spike Cave': (0x117, 0x10),
                     'Hookshot Cave - Top Right': (0x3c, 0x10),
                     'Hookshot Cave - Top Left': (0x3c, 0x20),
                     'Hookshot Cave - Bottom Right': (0x3c, 0x80),
                     'Hookshot Cave - Bottom Left': (0x3c, 0x40),
                     'Mimic Cave': (0x10c, 0x10),
                     'Swamp Palace - Entrance': (0x28, 0x10),
                     'Swamp Palace - Map Chest': (0x37, 0x10),
                     'Swamp Palace - Pot Row Pot Key': (0x38, 0x400),
                     'Swamp Palace - Trench 1 Pot Key': (0x37, 0x400),
                     'Swamp Palace - Hookshot Pot Key': (0x36, 0x400),
                     'Swamp Palace - Big Chest': (0x36, 0x10),
                     'Swamp Palace - Compass Chest': (0x46, 0x10),
                     'Swamp Palace - Trench 2 Pot Key': (0x35, 0x400),
                     'Swamp Palace - Big Key Chest': (0x35, 0x10),
                     'Swamp Palace - West Chest': (0x34, 0x10),
                     'Swamp Palace - Flooded Room - Left': (0x76, 0x10),
                     'Swamp Palace - Flooded Room - Right': (0x76, 0x20),
                     'Swamp Palace - Waterfall Room': (0x66, 0x10),
                     'Swamp Palace - Waterway Pot Key': (0x16, 0x400),
                     'Swamp Palace - Boss': (0x6, 0x800),
                     "Thieves' Town - Big Key Chest": (0xdb, 0x20),
                     "Thieves' Town - Map Chest": (0xdb, 0x10),
                     "Thieves' Town - Compass Chest": (0xdc, 0x10),
                     "Thieves' Town - Ambush Chest": (0xcb, 0x10),
                     "Thieves' Town - Hallway Pot Key": (0xbc, 0x400),
                     "Thieves' Town - Spike Switch Pot Key": (0xab, 0x400),
                     "Thieves' Town - Attic": (0x65, 0x10),
                     "Thieves' Town - Big Chest": (0x44, 0x10),
                     "Thieves' Town - Blind's Cell": (0x45, 0x10),
                     "Thieves' Town - Boss": (0xac, 0x800),
                     'Skull Woods - Compass Chest': (0x67, 0x10),
                     'Skull Woods - Map Chest': (0x58, 0x20),
                     'Skull Woods - Big Chest': (0x58, 0x10),
                     'Skull Woods - Pot Prison': (0x57, 0x20),
                     'Skull Woods - Pinball Room': (0x68, 0x10),
                     'Skull Woods - Big Key Chest': (0x57, 0x10),
                     'Skull Woods - West Lobby Pot Key': (0x56, 0x400),
                     'Skull Woods - Bridge Room': (0x59, 0x10),
                     'Skull Woods - Spike Corner Key Drop': (0x39, 0x400),
                     'Skull Woods - Boss': (0x29, 0x800),
                     'Ice Palace - Jelly Key Drop': (0x0e, 0x400),
                     'Ice Palace - Compass Chest': (0x2e, 0x10),
                     'Ice Palace - Conveyor Key Drop': (0x3e, 0x400),
                     'Ice Palace - Freezor Chest': (0x7e, 0x10),
                     'Ice Palace - Big Chest': (0x9e, 0x10),
                     'Ice Palace - Iced T Room': (0xae, 0x10),
                     'Ice Palace - Many Pots Pot Key': (0x9f, 0x400),
                     'Ice Palace - Spike Room': (0x5f, 0x10),
                     'Ice Palace - Big Key Chest': (0x1f, 0x10),
                     'Ice Palace - Hammer Block Key Drop': (0x3f, 0x400),
                     'Ice Palace - Map Chest': (0x3f, 0x10),
                     'Ice Palace - Boss': (0xde, 0x800),
                     'Misery Mire - Big Chest': (0xc3, 0x10),
                     'Misery Mire - Map Chest': (0xc3, 0x20),
                     'Misery Mire - Main Lobby': (0xc2, 0x10),
                     'Misery Mire - Bridge Chest': (0xa2, 0x10),
                     'Misery Mire - Spikes Pot Key': (0xb3, 0x400),
                     'Misery Mire - Spike Chest': (0xb3, 0x10),
                     'Misery Mire - Fishbone Pot Key': (0xa1, 0x400),
                     'Misery Mire - Conveyor Crystal Key Drop': (0xc1, 0x400),
                     'Misery Mire - Compass Chest': (0xc1, 0x10),
                     'Misery Mire - Big Key Chest': (0xd1, 0x10),
                     'Misery Mire - Boss': (0x90, 0x800),
                     'Turtle Rock - Compass Chest': (0xd6, 0x10),
                     'Turtle Rock - Roller Room - Left': (0xb7, 0x10),
                     'Turtle Rock - Roller Room - Right': (0xb7, 0x20),
                     'Turtle Rock - Pokey 1 Key Drop': (0xb6, 0x400),
                     'Turtle Rock - Chain Chomps': (0xb6, 0x10),
                     'Turtle Rock - Pokey 2 Key Drop': (0x13, 0x400),
                     'Turtle Rock - Big Key Chest': (0x14, 0x10),
                     'Turtle Rock - Big Chest': (0x24, 0x10),
                     'Turtle Rock - Crystaroller Room': (0x4, 0x10),
                     'Turtle Rock - Eye Bridge - Bottom Left': (0xd5, 0x80),
                     'Turtle Rock - Eye Bridge - Bottom Right': (0xd5, 0x40),
                     'Turtle Rock - Eye Bridge - Top Left': (0xd5, 0x20),
                     'Turtle Rock - Eye Bridge - Top Right': (0xd5, 0x10),
                     'Turtle Rock - Boss': (0xa4, 0x800),
                     'Palace of Darkness - Shooter Room': (0x9, 0x10),
                     'Palace of Darkness - The Arena - Bridge': (0x2a, 0x20),
                     'Palace of Darkness - Stalfos Basement': (0xa, 0x10),
                     'Palace of Darkness - Big Key Chest': (0x3a, 0x10),
                     'Palace of Darkness - The Arena - Ledge': (0x2a, 0x10),
                     'Palace of Darkness - Map Chest': (0x2b, 0x10),
                     'Palace of Darkness - Compass Chest': (0x1a, 0x20),
                     'Palace of Darkness - Dark Basement - Left': (0x6a, 0x10),
                     'Palace of Darkness - Dark Basement - Right': (0x6a, 0x20),
                     'Palace of Darkness - Dark Maze - Top': (0x19, 0x10),
                     'Palace of Darkness - Dark Maze - Bottom': (0x19, 0x20),
                     'Palace of Darkness - Big Chest': (0x1a, 0x10),
                     'Palace of Darkness - Harmless Hellway': (0x1a, 0x40),
                     'Palace of Darkness - Boss': (0x5a, 0x800),
                     'Ganons Tower - Conveyor Cross Pot Key': (0x8b, 0x400),
                     "Ganons Tower - Bob's Torch": (0x8c, 0x400),
                     'Ganons Tower - Hope Room - Left': (0x8c, 0x20),
                     'Ganons Tower - Hope Room - Right': (0x8c, 0x40),
                     'Ganons Tower - Tile Room': (0x8d, 0x10),
                     'Ganons Tower - Compass Room - Top Left': (0x9d, 0x10),
                     'Ganons Tower - Compass Room - Top Right': (0x9d, 0x20),
                     'Ganons Tower - Compass Room - Bottom Left': (0x9d, 0x40),
                     'Ganons Tower - Compass Room - Bottom Right': (0x9d, 0x80),
                     'Ganons Tower - Conveyor Star Pits Pot Key': (0x7b, 0x400),
                     'Ganons Tower - DMs Room - Top Left': (0x7b, 0x10),
                     'Ganons Tower - DMs Room - Top Right': (0x7b, 0x20),
                     'Ganons Tower - DMs Room - Bottom Left': (0x7b, 0x40),
                     'Ganons Tower - DMs Room - Bottom Right': (0x7b, 0x80),
                     'Ganons Tower - Map Chest': (0x8b, 0x10),
                     'Ganons Tower - Double Switch Pot Key': (0x9b, 0x400),
                     'Ganons Tower - Firesnake Room': (0x7d, 0x10),
                     'Ganons Tower - Randomizer Room - Top Left': (0x7c, 0x10),
                     'Ganons Tower - Randomizer Room - Top Right': (0x7c, 0x20),
                     'Ganons Tower - Randomizer Room - Bottom Left': (0x7c, 0x40),
                     'Ganons Tower - Randomizer Room - Bottom Right': (0x7c, 0x80),
                     "Ganons Tower - Bob's Chest": (0x8c, 0x80),
                     'Ganons Tower - Big Chest': (0x8c, 0x10),
                     'Ganons Tower - Big Key Room - Left': (0x1c, 0x20),
                     'Ganons Tower - Big Key Room - Right': (0x1c, 0x40),
                     'Ganons Tower - Big Key Chest': (0x1c, 0x10),
                     'Ganons Tower - Mini Helmasaur Room - Left': (0x3d, 0x10),
                     'Ganons Tower - Mini Helmasaur Room - Right': (0x3d, 0x20),
                     'Ganons Tower - Mini Helmasaur Key Drop': (0x3d, 0x400),
                     'Ganons Tower - Pre-Moldorm Chest': (0x3d, 0x40),
                     'Ganons Tower - Validation Chest': (0x4d, 0x10)}
location_table_npc = {'Mushroom': 0x1000,
                      'King Zora': 0x2,
                      'Sahasrahla': 0x10,
                      'Blacksmith': 0x400,
                      'Magic Bat': 0x8000,
                      'Sick Kid': 0x4,
                      'Library': 0x80,
                      'Potion Shop': 0x2000,
                      'Old Man': 0x1,
                      'Ether Tablet': 0x100,
                      'Catfish': 0x20,
                      'Stumpy': 0x8,
                      'Bombos Tablet': 0x200}
location_table_ow = {'Flute Spot': 0x2a,
                     'Sunken Treasure': 0x3b,
                     "Zora's Ledge": 0x81,
                     'Lake Hylia Island': 0x35,
                     'Maze Race': 0x28,
                     'Desert Ledge': 0x30,
                     'Master Sword Pedestal': 0x80,
                     'Spectacle Rock': 0x3,
                     'Pyramid': 0x5b,
                     'Digging Game': 0x68,
                     'Bumper Cave Ledge': 0x4a,
                     'Floating Island': 0x5}
location_table_misc = {'Bottle Merchant': (0x3c9, 0x2),
                       'Purple Chest': (0x3c9, 0x10),
                       "Link's Uncle": (0x3c6, 0x1),
                       'Hobo': (0x3c9, 0x1)}
countdown_region_table = {"Blind's Hideout - Top": "Kakariko Village",
                     "Blind's Hideout - Left": "Kakariko Village",
                     "Blind's Hideout - Right": "Kakariko Village",
                     "Blind's Hideout - Far Left": "Kakariko Village",
                     "Blind's Hideout - Far Right": "Kakariko Village",
                     'Secret Passage': "South Light World",
                     'Waterfall Fairy - Left': "East Light World",
                     'Waterfall Fairy - Right': "East Light World",
                     "King's Tomb": "North Light World",
                     'Floodgate Chest': "South Light World",
                     "Link's House": "South Light World",
                     'Kakariko Tavern': "Kakariko Village",
                     'Chicken House': "Kakariko Village",
                     "Aginah's Cave": "South Light World",
                     "Sahasrahla's Hut - Left": "East Light World",
                     "Sahasrahla's Hut - Middle": "East Light World",
                     "Sahasrahla's Hut - Right": "East Light World",
                     'Kakariko Well - Top': "Kakariko Village",
                     'Kakariko Well - Left': "Kakariko Village",
                     'Kakariko Well - Middle': "Kakariko Village",
                     'Kakariko Well - Right': "Kakariko Village",
                     'Kakariko Well - Bottom': "Kakariko Village",
                     'Lost Woods Hideout': "North Light World",
                     'Lumberjack Tree': "North Light World",
                     'Cave 45': "South Light World",
                     'Graveyard Cave': "North Light World",
                     'Checkerboard Cave': "South Light World",
                     'Mini Moldorm Cave - Far Left': "South Light World",
                     'Mini Moldorm Cave - Left': "South Light World",
                     'Mini Moldorm Cave - Right': "South Light World",
                     'Mini Moldorm Cave - Far Right': "South Light World",
                     'Mini Moldorm Cave - Generous Guy': "South Light World",
                     'Ice Rod Cave': "South Light World",
                     'Bonk Rock Cave': "North Light World",
                     'Desert Palace - Big Chest': "Desert Palace",
                     'Desert Palace - Torch': "Desert Palace",
                     'Desert Palace - Map Chest': "Desert Palace",
                     'Desert Palace - Compass Chest': "Desert Palace",
                     'Desert Palace - Big Key Chest': "Desert Palace",
                     'Desert Palace - Desert Tiles 1 Pot Key': "Desert Palace",
                     'Desert Palace - Beamos Hall Pot Key': "Desert Palace",
                     'Desert Palace - Desert Tiles 2 Pot Key': "Desert Palace",
                     'Desert Palace - Boss': "Desert Palace",
                     'Eastern Palace - Compass Chest': "Eastern Palace",
                     'Eastern Palace - Big Chest': "Eastern Palace",
                     'Eastern Palace - Dark Square Pot Key': "Eastern Palace",
                     'Eastern Palace - Dark Eyegore Key Drop': "Eastern Palace",
                     'Eastern Palace - Cannonball Chest': "Eastern Palace",
                     'Eastern Palace - Big Key Chest': "Eastern Palace",
                     'Eastern Palace - Map Chest': "Eastern Palace",
                     'Eastern Palace - Boss': "Eastern Palace",
                     'Hyrule Castle - Boomerang Chest': "Hyrule Castle",
                     'Hyrule Castle - Boomerang Guard Key Drop': "Hyrule Castle",
                     'Hyrule Castle - Map Chest': "Hyrule Castle",
                     'Hyrule Castle - Map Guard Key Drop': "Hyrule Castle",
                     "Hyrule Castle - Zelda's Chest": "Hyrule Castle",
                     'Hyrule Castle - Big Key Drop': "Hyrule Castle",
                     'Sewers - Dark Cross': "Hyrule Castle",
                     'Hyrule Castle - Key Rat Key Drop': "Hyrule Castle",
                     'Sewers - Secret Room - Left': "Hyrule Castle",
                     'Sewers - Secret Room - Middle': "Hyrule Castle",
                     'Sewers - Secret Room - Right': "Hyrule Castle",
                     'Sanctuary': "Hyrule Castle",
                     'Castle Tower - Room 03': "Castle Tower",
                     'Castle Tower - Dark Maze': "Castle Tower",
                     'Castle Tower - Dark Archer Key Drop': "Castle Tower",
                     'Castle Tower - Circle of Pots Key Drop': "Castle Tower",
                     'Spectacle Rock Cave': "Death Mountain",
                     'Paradox Cave Lower - Far Left': "Death Mountain",
                     'Paradox Cave Lower - Left': "Death Mountain",
                     'Paradox Cave Lower - Right': "Death Mountain",
                     'Paradox Cave Lower - Far Right': "Death Mountain",
                     'Paradox Cave Lower - Middle': "Death Mountain",
                     'Paradox Cave Upper - Left': "Death Mountain",
                     'Paradox Cave Upper - Right': "Death Mountain",
                     'Spiral Cave': "Death Mountain",
                     'Tower of Hera - Basement Cage': "Tower of Hera",
                     'Tower of Hera - Map Chest': "Tower of Hera",
                     'Tower of Hera - Big Key Chest': "Tower of Hera",
                     'Tower of Hera - Compass Chest': "Tower of Hera",
                     'Tower of Hera - Big Chest': "Tower of Hera",
                     'Tower of Hera - Boss': "Tower of Hera",
                     'Hype Cave - Top': "South Dark World",
                     'Hype Cave - Middle Right': "South Dark World",
                     'Hype Cave - Middle Left': "South Dark World",
                     'Hype Cave - Bottom': "South Dark World",
                     'Hype Cave - Generous Guy': "South Dark World",
                     'Peg Cave': "Village of Outcasts",
                     'Pyramid Fairy - Left': "South Dark World",
                     'Pyramid Fairy - Right': "South Dark World",
                     'Brewery': "Village of Outcasts",
                     'C-Shaped House': "Village of Outcasts",
                     'Chest Game': "Village of Outcasts",
                     'Mire Shed - Left': "South Dark World",
                     'Mire Shed - Right': "South Dark World",
                     'Superbunny Cave - Top': "Dark Death Mountain",
                     'Superbunny Cave - Bottom': "Dark Death Mountain",
                     'Spike Cave': "Dark Death Mountain",
                     'Hookshot Cave - Top Right': "Dark Death Mountain",
                     'Hookshot Cave - Top Left': "Dark Death Mountain",
                     'Hookshot Cave - Bottom Right': "Dark Death Mountain",
                     'Hookshot Cave - Bottom Left': "Dark Death Mountain",
                     'Mimic Cave': "Death Mountain",
                     'Swamp Palace - Entrance': "Swamp Palace",
                     'Swamp Palace - Map Chest': "Swamp Palace",
                     'Swamp Palace - Pot Row Pot Key': "Swamp Palace",
                     'Swamp Palace - Trench 1 Pot Key': "Swamp Palace",
                     'Swamp Palace - Hookshot Pot Key': "Swamp Palace",
                     'Swamp Palace - Big Chest': "Swamp Palace",
                     'Swamp Palace - Compass Chest': "Swamp Palace",
                     'Swamp Palace - Trench 2 Pot Key': "Swamp Palace",
                     'Swamp Palace - Big Key Chest': "Swamp Palace",
                     'Swamp Palace - West Chest': "Swamp Palace",
                     'Swamp Palace - Flooded Room - Left': "Swamp Palace",
                     'Swamp Palace - Flooded Room - Right': "Swamp Palace",
                     'Swamp Palace - Waterfall Room': "Swamp Palace",
                     'Swamp Palace - Waterway Pot Key': "Swamp Palace",
                     'Swamp Palace - Boss': "Swamp Palace",
                     "Thieves' Town - Big Key Chest": "Thieves' Town",
                     "Thieves' Town - Map Chest": "Thieves' Town",
                     "Thieves' Town - Compass Chest": "Thieves' Town",
                     "Thieves' Town - Ambush Chest": "Thieves' Town",
                     "Thieves' Town - Hallway Pot Key": "Thieves' Town",
                     "Thieves' Town - Spike Switch Pot Key": "Thieves' Town",
                     "Thieves' Town - Attic": "Thieves' Town",
                     "Thieves' Town - Big Chest": "Thieves' Town",
                     "Thieves' Town - Blind's Cell": "Thieves' Town",
                     "Thieves' Town - Boss": "Thieves' Town",
                     'Skull Woods - Compass Chest': "Skull Woods",
                     'Skull Woods - Map Chest': "Skull Woods",
                     'Skull Woods - Big Chest': "Skull Woods",
                     'Skull Woods - Pot Prison': "Skull Woods",
                     'Skull Woods - Pinball Room': "Skull Woods",
                     'Skull Woods - Big Key Chest': "Skull Woods",
                     'Skull Woods - West Lobby Pot Key': "Skull Woods",
                     'Skull Woods - Bridge Room': "Skull Woods",
                     'Skull Woods - Spike Corner Key Drop': "Skull Woods",
                     'Skull Woods - Boss': "Skull Woods",
                     'Ice Palace - Jelly Key Drop': "Ice Palace",
                     'Ice Palace - Compass Chest': "Ice Palace",
                     'Ice Palace - Conveyor Key Drop': "Ice Palace",
                     'Ice Palace - Freezor Chest': "Ice Palace",
                     'Ice Palace - Big Chest': "Ice Palace",
                     'Ice Palace - Iced T Room': "Ice Palace",
                     'Ice Palace - Many Pots Pot Key': "Ice Palace",
                     'Ice Palace - Spike Room': "Ice Palace",
                     'Ice Palace - Big Key Chest': "Ice Palace",
                     'Ice Palace - Hammer Block Key Drop': "Ice Palace",
                     'Ice Palace - Map Chest': "Ice Palace",
                     'Ice Palace - Boss': "Ice Palace",
                     'Misery Mire - Big Chest': "Misery Mire",
                     'Misery Mire - Map Chest': "Misery Mire",
                     'Misery Mire - Main Lobby': "Misery Mire",
                     'Misery Mire - Bridge Chest': "Misery Mire",
                     'Misery Mire - Spikes Pot Key': "Misery Mire",
                     'Misery Mire - Spike Chest': "Misery Mire",
                     'Misery Mire - Fishbone Pot Key': "Misery Mire",
                     'Misery Mire - Conveyor Crystal Key Drop': "Misery Mire",
                     'Misery Mire - Compass Chest': "Misery Mire",
                     'Misery Mire - Big Key Chest': "Misery Mire",
                     'Misery Mire - Boss': "Misery Mire",
                     'Turtle Rock - Compass Chest': "Turtle Rock",
                     'Turtle Rock - Roller Room - Left': "Turtle Rock",
                     'Turtle Rock - Roller Room - Right': "Turtle Rock",
                     'Turtle Rock - Pokey 1 Key Drop': "Turtle Rock",
                     'Turtle Rock - Chain Chomps': "Turtle Rock",
                     'Turtle Rock - Pokey 2 Key Drop': "Turtle Rock",
                     'Turtle Rock - Big Key Chest': "Turtle Rock",
                     'Turtle Rock - Big Chest': "Turtle Rock",
                     'Turtle Rock - Crystaroller Room': "Turtle Rock",
                     'Turtle Rock - Eye Bridge - Bottom Left': "Turtle Rock",
                     'Turtle Rock - Eye Bridge - Bottom Right': "Turtle Rock",
                     'Turtle Rock - Eye Bridge - Top Left': "Turtle Rock",
                     'Turtle Rock - Eye Bridge - Top Right': "Turtle Rock",
                     'Turtle Rock - Boss': "Turtle Rock",
                     'Palace of Darkness - Shooter Room': "Palace of Darkness",
                     'Palace of Darkness - The Arena - Bridge': "Palace of Darkness",
                     'Palace of Darkness - Stalfos Basement': "Palace of Darkness",
                     'Palace of Darkness - Big Key Chest': "Palace of Darkness",
                     'Palace of Darkness - The Arena - Ledge': "Palace of Darkness",
                     'Palace of Darkness - Map Chest': "Palace of Darkness",
                     'Palace of Darkness - Compass Chest': "Palace of Darkness",
                     'Palace of Darkness - Dark Basement - Left': "Palace of Darkness",
                     'Palace of Darkness - Dark Basement - Right': "Palace of Darkness",
                     'Palace of Darkness - Dark Maze - Top': "Palace of Darkness",
                     'Palace of Darkness - Dark Maze - Bottom': "Palace of Darkness",
                     'Palace of Darkness - Big Chest': "Palace of Darkness",
                     'Palace of Darkness - Harmless Hellway': "Palace of Darkness",
                     'Palace of Darkness - Boss': "Palace of Darkness",
                     'Ganons Tower - Conveyor Cross Pot Key': "Ganon's Tower",
                     "Ganons Tower - Bob's Torch": "Ganon's Tower",
                     'Ganons Tower - Hope Room - Left': "Ganon's Tower",
                     'Ganons Tower - Hope Room - Right': "Ganon's Tower",
                     'Ganons Tower - Tile Room': "Ganon's Tower",
                     'Ganons Tower - Compass Room - Top Left': "Ganon's Tower",
                     'Ganons Tower - Compass Room - Top Right': "Ganon's Tower",
                     'Ganons Tower - Compass Room - Bottom Left': "Ganon's Tower",
                     'Ganons Tower - Compass Room - Bottom Right': "Ganon's Tower",
                     'Ganons Tower - Conveyor Star Pits Pot Key': "Ganon's Tower",
                     'Ganons Tower - DMs Room - Top Left': "Ganon's Tower",
                     'Ganons Tower - DMs Room - Top Right': "Ganon's Tower",
                     'Ganons Tower - DMs Room - Bottom Left': "Ganon's Tower",
                     'Ganons Tower - DMs Room - Bottom Right': "Ganon's Tower",
                     'Ganons Tower - Map Chest': "Ganon's Tower",
                     'Ganons Tower - Double Switch Pot Key': "Ganon's Tower",
                     'Ganons Tower - Firesnake Room': "Ganon's Tower",
                     'Ganons Tower - Randomizer Room - Top Left': "Ganon's Tower",
                     'Ganons Tower - Randomizer Room - Top Right': "Ganon's Tower",
                     'Ganons Tower - Randomizer Room - Bottom Left': "Ganon's Tower",
                     'Ganons Tower - Randomizer Room - Bottom Right': "Ganon's Tower",
                     "Ganons Tower - Bob's Chest": "Ganon's Tower",
                     'Ganons Tower - Big Chest': "Ganon's Tower",
                     'Ganons Tower - Big Key Room - Left': "Ganon's Tower",
                     'Ganons Tower - Big Key Room - Right': "Ganon's Tower",
                     'Ganons Tower - Big Key Chest': "Ganon's Tower",
                     'Ganons Tower - Mini Helmasaur Room - Left': "Ganon's Tower",
                     'Ganons Tower - Mini Helmasaur Room - Right': "Ganon's Tower",
                     'Ganons Tower - Mini Helmasaur Key Drop': "Ganon's Tower",
                     'Ganons Tower - Pre-Moldorm Chest': "Ganon's Tower",
                     'Ganons Tower - Validation Chest': "Ganon's Tower",
                     'Mushroom': "North Light World",
                     'King Zora': "East Light World",
                     'Sahasrahla': "East Light World",
                     'Blacksmith': "Kakariko Village",
                     'Magic Bat': "Kakariko Village",
                     'Sick Kid': "Kakariko Village",
                     'Library': "Kakariko Village",
                     'Potion Shop': "East Light World",
                     'Old Man': "Death Mountain",
                     'Ether Tablet': "Death Mountain",
                     'Catfish': "East Dark World",
                     'Stumpy': "South Dark World",
                     'Bombos Tablet': "South Light World",
                     'Flute Spot': "South Light World",
                     'Sunken Treasure': "South Light World",
                     "Zora's Ledge": "East Light World",
                     'Lake Hylia Island': "South Light World",
                     'Maze Race': "Kakariko Village",
                     'Desert Ledge': "South Light World",
                     'Master Sword Pedestal': "North Light World",
                     'Spectacle Rock': "Death Mountain",
                     'Pyramid': "South Dark World",
                     'Digging Game': "Village of Outcasts",
                     'Bumper Cave Ledge': "North Dark World",
                     'Floating Island': "Death Mountain",
                     'Bottle Merchant': "Kakariko Village",
                     'Purple Chest': "Village of Outcasts",
                     "Link's Uncle": "South Light World",
                     'Hobo': "South Light World",
                     "Kakariko Shop - Left": "Kakariko Village",
                     "Kakariko Shop - Middle": "Kakariko Village",
                     "Kakariko Shop - Right": "Kakariko Village",
                     "Lake Hylia Shop - Left": "South Light World",
                     "Lake Hylia Shop - Middle": "South Light World",
                     "Lake Hylia Shop - Right": "South Light World",
                     "Dark Death Mountain Shop - Left": "Dark Death Mountain",
                     "Dark Death Mountain Shop - Middle": "Dark Death Mountain",
                     "Dark Death Mountain Shop - Right": "Dark Death Mountain",
                     "Potion Shop - Left": "East Light World",
                     "Potion Shop - Middle": "East Light World",
                     "Potion Shop - Right": "East Light World",
                     "Capacity Upgrade - Left": "South Light World",
                     "Capacity Upgrade - Right": "South Light World",
                     "Paradox Shop - Left": "Death Mountain",
                     "Paradox Shop - Middle": "Death Mountain",
                     "Paradox Shop - Right": "Death Mountain",
                     "Village of Outcasts Shop - Left": "Village of Outcasts",
                     "Village of Outcasts Shop - Middle": "Village of Outcasts",
                     "Village of Outcasts Shop - Right": "Village of Outcasts",
                     "Dark Lake Hylia Shop - Left": "South Dark World",
                     "Dark Lake Hylia Shop - Middle": "South Dark World",
                     "Dark Lake Hylia Shop - Right": "South Dark World",
                     "Dark Lumberjack Shop - Left": "North Dark World",
                     "Dark Lumberjack Shop - Middle": "North Dark World",
                     "Dark Lumberjack Shop - Right": "North Dark World",
                     "Dark Potion Shop - Left": "East Dark World",
                     "Dark Potion Shop - Middle": "East Dark World",
                     "Dark Potion Shop - Right": "East Dark World",
                     "Red Shield Shop - Left": "North Dark World",
                     "Red Shield Shop - Middle": "North Dark World",
                     "Red Shield Shop - Right": "North Dark World"}
countdown_items = {"North Light World": 0,
                   "East Light World": 0,
                   "South Light World": 0,
                   "Kakariko Village": 0,
                   "Death Mountain": 0,
                   "North Dark World": 0,
                   "East Dark World": 0,
                   "South Dark World": 0,
                   "Village of Outcasts": 0,
                   "Dark Death Mountain": 0,
                   "Hyrule Castle": 0,
                   "Eastern Palace": 0,
                   "Desert Palace": 0,
                   "Tower of Hera": 0,
                   "Castle Tower": 0,
                   "Palace of Darkness": 0,
                   "Swamp Palace": 0,
                   "Skull Woods": 0,
                   "Thieves' Town": 0,
                   "Ice Palace": 0,
                   "Misery Mire": 0,
                   "Turtle Rock": 0,
                   "Ganon's Tower": 0}
countdown_keys = {"North Light World": 0,
                   "East Light World": 0,
                   "South Light World": 0,
                   "Kakariko Village": 0,
                   "Death Mountain": 0,
                   "North Dark World": 0,
                   "East Dark World": 0,
                   "South Dark World": 0,
                   "Village of Outcasts": 0,
                   "Dark Death Mountain": 0,
                   "Hyrule Castle": 0,
                   "Eastern Palace": 0,
                   "Desert Palace": 0,
                   "Tower of Hera": 0,
                   "Castle Tower": 0,
                   "Palace of Darkness": 0,
                   "Swamp Palace": 0,
                   "Skull Woods": 0,
                   "Thieves' Town": 0,
                   "Ice Palace": 0,
                   "Misery Mire": 0,
                   "Turtle Rock": 0,
                   "Ganon's Tower": 0}
countdown_triforces = {"North Light World": 0,
                   "East Light World": 0,
                   "South Light World": 0,
                   "Kakariko Village": 0,
                   "Death Mountain": 0,
                   "North Dark World": 0,
                   "East Dark World": 0,
                   "South Dark World": 0,
                   "Village of Outcasts": 0,
                   "Dark Death Mountain": 0,
                   "Hyrule Castle": 0,
                   "Eastern Palace": 0,
                   "Desert Palace": 0,
                   "Tower of Hera": 0,
                   "Castle Tower": 0,
                   "Palace of Darkness": 0,
                   "Swamp Palace": 0,
                   "Skull Woods": 0,
                   "Thieves' Town": 0,
                   "Ice Palace": 0,
                   "Misery Mire": 0,
                   "Turtle Rock": 0,
                   "Ganon's Tower": 0}
countdown_item_names = {'Progressive', 'Boomerang', 'Hookshot', 'Mushroom', 'Magic Powder', 'Fire Rod', 'Ice Rod', 'Bombos', 'Ether', 'Quake', 'Lamp', 'Hammer', 'Shovel', 'Ocarina', 'Bug Catching Net', 'Book of Mudora', 'Bottle', 'Cane of Somaria', 'Cane of Byrna', 'Cape', 'Magic Mirror', 'Magic Upgrade', 'Boots', 'Flippers', 'Moon Pearl'}
countdown_item_locs = set()
countdown_key_locs = set()
countdown_triforce_locs = set()
countdown_use_triforces = False
countdown_use_keys = False
countdown_use_keydrops = False
countdown_last_msg = "Blah"

SNES_DISCONNECTED = 0
SNES_CONNECTING = 1
SNES_CONNECTED = 2
SNES_ATTACHED = 3

async def snes_connect(ctx : Context, address):
    if ctx.snes_socket is not None:
        logging.error('Already connected to snes')
        return

    ctx.snes_state = SNES_CONNECTING
    recv_task = None

    address = f"ws://{address}" if "://" not in address else address

    logging.info("Connecting to QUsb2snes at %s ..." % address)

    try:
        ctx.snes_socket = await websockets.connect(address, ping_timeout=None, ping_interval=None)
        ctx.snes_state = SNES_CONNECTED

        DeviceList_Request = {
            "Opcode" : "DeviceList",
            "Space" : "SNES"
        }
        await ctx.snes_socket.send(json.dumps(DeviceList_Request))

        reply = json.loads(await ctx.snes_socket.recv())
        devices = reply['Results'] if 'Results' in reply and len(reply['Results']) > 0 else None

        if not devices:
            raise Exception('No device found')

        logging.info("Available devices:")
        for id, device in enumerate(devices):
            logging.info("[%d] %s" % (id + 1, device))

        device = None
        if len(devices) == 1:
            device = devices[0]
        elif ctx.snes_reconnect_address:
            if ctx.snes_attached_device[1] in devices:
                device = ctx.snes_attached_device[1]
            else:
                device = devices[ctx.snes_attached_device[0]]
        else:
            while True:
                logging.info("Select a device:")
                choice = await console_input(ctx)
                if choice is None:
                    raise Exception('Abort input')
                if not choice.isdigit() or int(choice) < 1 or int(choice) > len(devices):
                    logging.warning("Invalid choice (%s)" % choice)
                    continue

                device = devices[int(choice) - 1]
                break

        logging.info("Attaching to " + device)

        Attach_Request = {
            "Opcode" : "Attach",
            "Space" : "SNES",
            "Operands" : [device]
        }
        await ctx.snes_socket.send(json.dumps(Attach_Request))
        ctx.snes_state = SNES_ATTACHED
        ctx.snes_attached_device = (devices.index(device), device)

        if 'SD2SNES'.lower() in device.lower() or (len(device) == 4 and device[:3] == 'COM'):
            logging.info("SD2SNES Detected")
            ctx.is_sd2snes = True
            await ctx.snes_socket.send(json.dumps({"Opcode" : "Info", "Space" : "SNES"}))
            reply = json.loads(await ctx.snes_socket.recv())
            if reply and 'Results' in reply:
                logging.info(reply['Results'])
        else:
            ctx.is_sd2snes = False

        ctx.snes_reconnect_address = address
        recv_task = asyncio.create_task(snes_recv_loop(ctx))

    except Exception as e:
        if recv_task is not None:
            if not ctx.snes_socket.closed:
                await ctx.snes_socket.close()
        else:
            if ctx.snes_socket is not None:
                if not ctx.snes_socket.closed:
                    await ctx.snes_socket.close()
                ctx.snes_socket = None
            ctx.snes_state = SNES_DISCONNECTED
        if not ctx.snes_reconnect_address:
            logging.error("Error connecting to snes (%s)" % e)
        else:
            logging.error(f"Error connecting to snes, attempt again in {RECONNECT_DELAY}s")
            asyncio.create_task(snes_autoreconnect(ctx))

async def snes_autoreconnect(ctx: Context):
    await asyncio.sleep(RECONNECT_DELAY)
    if ctx.snes_reconnect_address and ctx.snes_socket is None:
        await snes_connect(ctx, ctx.snes_reconnect_address)

async def snes_recv_loop(ctx : Context):
    try:
        async for msg in ctx.snes_socket:
            ctx.snes_recv_queue.put_nowait(msg)
        logging.warning("Snes disconnected")
    except Exception as e:
        if not isinstance(e, websockets.WebSocketException):
            logging.exception(e)
        logging.error("Lost connection to the snes, type /snes to reconnect")
    finally:
        socket, ctx.snes_socket = ctx.snes_socket, None
        if socket is not None and not socket.closed:
            await socket.close()

        ctx.snes_state = SNES_DISCONNECTED
        ctx.snes_recv_queue = asyncio.Queue()
        ctx.hud_message_queue = []

        ctx.rom = None

        if ctx.snes_reconnect_address:
            logging.info(f"...reconnecting in {RECONNECT_DELAY}s")
            asyncio.create_task(snes_autoreconnect(ctx))

async def snes_read(ctx : Context, address, size):
    try:
        await ctx.snes_request_lock.acquire()

        if ctx.snes_state != SNES_ATTACHED or ctx.snes_socket is None or not ctx.snes_socket.open or ctx.snes_socket.closed:
            return None

        GetAddress_Request = {
            "Opcode" : "GetAddress",
            "Space" : "SNES",
            "Operands" : [hex(address)[2:], hex(size)[2:]]
        }
        try:
            await ctx.snes_socket.send(json.dumps(GetAddress_Request))
        except websockets.ConnectionClosed:
            return None

        data = bytes()
        while len(data) < size:
            try:
                data += await asyncio.wait_for(ctx.snes_recv_queue.get(), 5)
            except asyncio.TimeoutError:
                break

        if len(data) != size:
            logging.error('Error reading %s, requested %d bytes, received %d' % (hex(address), size, len(data)))
            if len(data):
                logging.error(str(data))
            if ctx.snes_socket is not None and not ctx.snes_socket.closed:
                await ctx.snes_socket.close()
            return None

        return data
    finally:
        ctx.snes_request_lock.release()

async def snes_write(ctx : Context, write_list):
    try:
        await ctx.snes_request_lock.acquire()

        if ctx.snes_state != SNES_ATTACHED or ctx.snes_socket is None or not ctx.snes_socket.open or ctx.snes_socket.closed:
            return False

        PutAddress_Request = {
            "Opcode" : "PutAddress",
            "Operands" : []
        }

        if ctx.is_sd2snes:
            cmd = b'\x00\xE2\x20\x48\xEB\x48'

            for address, data in write_list:
                if (address < WRAM_START) or ((address + len(data)) > (WRAM_START + WRAM_SIZE)):
                    logging.error("SD2SNES: Write out of range %s (%d)" % (hex(address), len(data)))
                    return False
                for ptr, byte in enumerate(data, address + 0x7E0000 - WRAM_START):
                    cmd += b'\xA9' # LDA
                    cmd += bytes([byte])
                    cmd += b'\x8F' # STA.l
                    cmd += bytes([ptr & 0xFF, (ptr >> 8) & 0xFF, (ptr >> 16) & 0xFF])

            cmd += b'\xA9\x00\x8F\x00\x2C\x00\x68\xEB\x68\x28\x6C\xEA\xFF\x08'

            PutAddress_Request['Space'] = 'CMD'
            PutAddress_Request['Operands'] = ["2C00", hex(len(cmd)-1)[2:], "2C00", "1"]
            try:
                if ctx.snes_socket is not None:
                    await ctx.snes_socket.send(json.dumps(PutAddress_Request))
                if ctx.snes_socket is not None:
                    await ctx.snes_socket.send(cmd)
            except websockets.ConnectionClosed:
                return False
        else:
            PutAddress_Request['Space'] = 'SNES'
            try:
                #will pack those requests as soon as qusb2snes actually supports that for real
                for address, data in write_list:
                    PutAddress_Request['Operands'] = [hex(address)[2:], hex(len(data))[2:]]
                    if ctx.snes_socket is not None:
                        await ctx.snes_socket.send(json.dumps(PutAddress_Request))
                    if ctx.snes_socket is not None:
                        await ctx.snes_socket.send(data)
            except websockets.ConnectionClosed:
                return False

        return True
    finally:
        ctx.snes_request_lock.release()

def snes_buffered_write(ctx : Context, address, data):
    if len(ctx.snes_write_buffer) > 0 and (ctx.snes_write_buffer[-1][0] + len(ctx.snes_write_buffer[-1][1])) == address:
        ctx.snes_write_buffer[-1] = (ctx.snes_write_buffer[-1][0], ctx.snes_write_buffer[-1][1] + data)
    else:
        ctx.snes_write_buffer.append((address, data))

async def snes_flush_writes(ctx : Context):
    if not ctx.snes_write_buffer:
        return

    await snes_write(ctx, ctx.snes_write_buffer)
    ctx.snes_write_buffer = []

async def send_msgs(websocket, msgs):
    if not websocket or not websocket.open or websocket.closed:
        return
    try:
        await websocket.send(json.dumps(msgs))
    except websockets.ConnectionClosed:
        pass

async def server_loop(ctx : Context, address = None):
    if ctx.socket is not None:
        logging.error('Already connected')
        return

    if address is None:
        address = ctx.server_address

    while not address:
        logging.info('Enter multiworld server address')
        address = await console_input(ctx)

    address = f"ws://{address}" if "://" not in address else address
    port = urllib.parse.urlparse(address).port or 38281

    logging.info('Connecting to multiworld server at %s' % address)
    try:
        ctx.socket = await websockets.connect(address, port=port, ping_timeout=None, ping_interval=None)
        logging.info('Connected')
        ctx.server_address = address

        async for data in ctx.socket:
            for msg in json.loads(data):
                cmd, args = (msg[0], msg[1]) if len(msg) > 1 else (msg, None)
                await process_server_cmd(ctx, cmd, args)
        logging.warning('Disconnected from multiworld server, type /connect to reconnect')
    except ConnectionRefusedError:
        logging.error('Connection refused by the multiworld server')
    except (OSError, websockets.InvalidURI):
        logging.error('Failed to connect to the multiworld server')
    except Exception as e:
        logging.error('Lost connection to the multiworld server, type /connect to reconnect')
        if not isinstance(e, websockets.WebSocketException):
            logging.exception(e)
    finally:
        ctx.awaiting_rom = False
        ctx.auth = None
        ctx.items_received = []
        ctx.locations_info = {}
        socket, ctx.socket = ctx.socket, None
        if socket is not None and not socket.closed:
            await socket.close()
        ctx.server_task = None
        if ctx.server_address:
            logging.info(f"... reconnecting in {RECONNECT_DELAY}s")
            asyncio.create_task(server_autoreconnect(ctx))

async def server_autoreconnect(ctx: Context):
    await asyncio.sleep(RECONNECT_DELAY)
    if ctx.server_address and ctx.server_task is None:
        ctx.server_task = asyncio.create_task(server_loop(ctx))

async def process_server_cmd(ctx : Context, cmd, args):
    if cmd == 'RoomInfo':
        logging.info('--------------------------------')
        logging.info('Room Information:')
        logging.info('--------------------------------')
        if args['password']:
            logging.info('Password required')
        if len(args['players']) < 1:
            logging.info('No player connected')
        else:
            args['players'].sort()
            current_team = 0
            logging.info('Connected players:')
            logging.info('  Team #1')
            for team, slot, name in args['players']:
                if team != current_team:
                    logging.info(f'  Team #{team + 1}')
                    current_team = team
                logging.info('    %s (Player %d)' % (name, slot))
        await server_auth(ctx, args['password'])

    if cmd == 'ConnectionRefused':
        if 'InvalidPassword' in args:
            logging.error('Invalid password')
            ctx.password = None
            await server_auth(ctx, True)
        if 'InvalidRom' in args:
            raise Exception('Invalid ROM detected, please verify that you have loaded the correct rom and reconnect your snes')
        if 'SlotAlreadyTaken' in args:
            raise Exception('Player slot already in use for that team')
        raise Exception('Connection refused by the multiworld host')

    if cmd == 'Connected':
        ctx.team, ctx.slot = args[0]
        ctx.player_names = {p: n for p, n in args[1]}
        msgs = []
        if ctx.locations_checked:
            msgs.append(['LocationChecks', [Regions.lookup_name_to_id[loc] for loc in ctx.locations_checked]])
        if ctx.locations_scouted:
            msgs.append(['LocationScouts', list(ctx.locations_scouted)])
        if msgs:
            await send_msgs(ctx.socket, msgs)

    if cmd == 'ReceivedItems':
        start_index, items = args
        if start_index == 0:
            ctx.items_received = []
        elif start_index != len(ctx.items_received):
            sync_msg = [['Sync']]
            if ctx.locations_checked:
                sync_msg.append(['LocationChecks', [Regions.lookup_name_to_id[loc] for loc in ctx.locations_checked]])
            await send_msgs(ctx.socket, sync_msg)
        if start_index == len(ctx.items_received):
            for item in items:
                ctx.items_received.append(ReceivedItem(*item))
        ctx.watcher_event.set()

    if cmd == 'LocationInfo':
        for location, item, player in args:
            if location not in ctx.locations_info:
                replacements = {0xA2: 'Small Key', 0x9D: 'Big Key', 0x8D: 'Compass', 0x7D: 'Map'}
                item_name = replacements.get(item, get_item_name_from_id(item))
                logging.info(f"Saw {color(item_name, 'red', 'bold')} at {list(Regions.lookup_id_to_name.keys())[location - 1]}")
                ctx.locations_info[location] = (item, player)
        ctx.watcher_event.set()

    if cmd == 'ItemSent':
        player_sent, location, player_recvd, item = args
        item = color(get_item_name_from_id(item), 'cyan' if player_sent != ctx.slot else 'green')
        player_sent = color(ctx.player_names[player_sent], 'yellow' if player_sent != ctx.slot else 'magenta')
        player_recvd = color(ctx.player_names[player_recvd], 'yellow' if player_recvd != ctx.slot else 'magenta')
        logging.info('%s sent %s to %s (%s)' % (player_sent, item, player_recvd, get_location_name_from_address(location)))

    if cmd == 'Print':
        logging.info(args)

async def server_auth(ctx : Context, password_requested):
    if password_requested and not ctx.password:
        logging.info('Enter the password required to join this game:')
        ctx.password = await console_input(ctx)
    if ctx.rom is None:
        ctx.awaiting_rom = True
        logging.info('No ROM detected, awaiting snes connection to authenticate to the multiworld server')
        return
    ctx.awaiting_rom = False
    ctx.auth = ctx.rom.copy()
    await send_msgs(ctx.socket, [['Connect', {'password': ctx.password, 'rom': ctx.auth}]])

async def console_input(ctx : Context):
    ctx.input_requests += 1
    return await ctx.input_queue.get()

async def disconnect(ctx: Context):
    if ctx.socket is not None and not ctx.socket.closed:
        await ctx.socket.close()
    if ctx.server_task is not None:
        await ctx.server_task

async def connect(ctx: Context, address=None):
    await disconnect(ctx)
    ctx.server_task = asyncio.create_task(server_loop(ctx, address))

async def console_loop(ctx : Context):
    while not ctx.exit_event.is_set():
        input = await aioconsole.ainput()

        if ctx.input_requests > 0:
            ctx.input_requests -= 1
            ctx.input_queue.put_nowait(input)
            continue

        command = shlex.split(input)
        if not command:
            continue

        if command[0] == '/exit':
            ctx.exit_event.set()

        if command[0] == '/snes':
            ctx.snes_reconnect_address = None
            asyncio.create_task(snes_connect(ctx, command[1] if len(command) > 1 else ctx.snes_address))
        if command[0] in ['/snes_close', '/snes_quit']:
            ctx.snes_reconnect_address = None
            if ctx.snes_socket is not None and not ctx.snes_socket.closed:
                await ctx.snes_socket.close()

        if command[0] in ['/connect', '/reconnect']:
            ctx.server_address = None
            asyncio.create_task(connect(ctx, command[1] if len(command) > 1 else None))
        if command[0] == '/disconnect':
            ctx.server_address = None
            asyncio.create_task(disconnect(ctx))
        if command[0][:1] != '/':
            asyncio.create_task(send_msgs(ctx.socket, [['Say', input]]))

        if command[0] == '/received':
            logging.info('Received items:')
            for index, item in enumerate(ctx.items_received, 1):
                logging.info('%s from %s (%s) (%d/%d in list)' % (
                    color(get_item_name_from_id(item.item), 'red', 'bold'), color(ctx.player_names[item.player], 'yellow'),
                    get_location_name_from_address(item.location), index, len(ctx.items_received)))

        if command[0] == '/missing':
            for location in [k for k, v in Regions.lookup_name_to_id.items()
                             if type(v) is int and not filter_location(ctx, k)]:
                if location not in ctx.locations_checked:
                    logging.info('Missing: ' + location)
        if command[0] == '/getitem' and len(command) > 1:
            item = input[9:]
            item_id = Items.item_table[item][3] if item in Items.item_table else None
            if type(item_id) is int and item_id in range(0x100):
                logging.info('Sending item: ' + item)
                snes_buffered_write(ctx, RECV_ITEM_ADDR, bytes([item_id]))
                snes_buffered_write(ctx, RECV_ITEM_PLAYER_ADDR, bytes([0]))
            else:
                logging.info('Invalid item: ' + item)

        await snes_flush_writes(ctx)


def get_item_name_from_id(code):
    items = [k for k, i in Items.item_table.items() if type(i[3]) is int and i[3] == code]
    return items[0] if items else f'Unknown item (ID:{code})'


def get_location_name_from_address(address):
    if type(address) is str:
        return address

    return Regions.lookup_id_to_name.get(address, f'Unknown location (ID:{address})')


def filter_location(ctx, location):
    if not ctx.key_drop_mode and ('Key Drop' in location or 'Pot Key' in location):
        return True
    if not ctx.shop_mode and location in Regions.flat_normal_shops:
        return True
    if not ctx.retro_mode and location in Regions.flat_retro_shops:
        return True
    return False


async def track_locations(ctx : Context, roomid, roomdata):
    global countdown_items, countdown_triforces, countdown_use_triforces, countdown_region_table, countdown_item_locs, countdown_triforce_locs
    new_locations = []

    if ctx.total_locations is None:
        total_data = await snes_read(ctx, DYNAMIC_TOTAL_ADDR, 2)
        ttl = total_data[0] | (total_data[1] << 8)
        if ttl > 0:
            ctx.total_locations = ttl

    if ctx.mode_flags is None:
        flags = await snes_read(ctx, MODE_FLAGS, 1)
        ctx.key_drop_mode = flags[0] & 0x1
        ctx.shop_mode = flags[0] & 0x2
        ctx.retro_mode = flags[0] & 0x4

    def new_check(location):
        global countdown_last_msg, countdown_use_keys, countdown_key_locs, countdown_keys
        ctx.locations_checked.add(location)
        ignored = filter_location(ctx, location)
        if ignored:
            ctx.ignore_count += 1
        else:
#            logging.info(f"New check: {location} ({len(ctx.locations_checked)-ctx.ignore_count}/{ctx.total_locations})")
            try:
                new_locations.append(Regions.lookup_name_to_id[location])
                regionName = countdown_region_table.get(location)
                if regionName is not None:
                    if location in countdown_item_locs:
                        countdown_items[regionName] = countdown_items[regionName] - 1
                    itemsLeft = countdown_items[regionName]
                    outStr = regionName + ": " + str(itemsLeft)
                    if (countdown_use_triforces or countdown_use_keys):
                        if itemsLeft == 1:
                            outStr = outStr + " Item"
                        else:
                            outStr = outStr + " Items"
                        if countdown_use_keys:
                            if location in countdown_key_locs:
                                countdown_keys[regionName] = countdown_keys[regionName] - 1
                            keysLeft = countdown_keys[regionName]
                            if keysLeft == 1:
                                outStr = outStr + ", " + str(keysLeft) + " Key"
                            else:
                                outStr = outStr + ", " + str(keysLeft) + " Keys"
                        if countdown_use_triforces:
                            if location in countdown_triforce_locs:
                                countdown_triforces[regionName] = countdown_triforces[regionName] - 1
                            triforcesLeft = countdown_triforces[regionName]
                            if triforcesLeft == 1:
                                outStr = outStr + ", " + str(triforcesLeft) + " Triforce"
                            else:
                                outStr = outStr + ", " + str(triforcesLeft) + " Triforces"
                    if outStr != countdown_last_msg:
                        logging.info('  ' + outStr)
                        file1 = open("countdown_display.txt", "w")
                        file1.write(outStr)
                        file1.close()
                    countdown_last_msg = outStr
                    del countdown_region_table[location]
            except Exception as e:
                print(e)
                logging.warning(e)
    try:
        if ctx.shop_mode or ctx.retro_mode:
            misc_data = await snes_read(ctx, SHOP_ADDR, SHOP_SRAM_LEN)
            for cnt, b in enumerate(misc_data):
                my_check = Regions.shop_table_by_location_id[0x400000 + cnt]
                if int(b) > 0 and my_check not in ctx.locations_checked:
                    new_check(my_check)
    except Exception as e:
        print(e)
        logging.warning(e)

    for location, (loc_roomid, loc_mask) in location_table_uw.items():
        if location not in ctx.locations_checked and loc_roomid == roomid and (roomdata << 4) & loc_mask != 0:
            new_check(location)

    uw_begin = 0x129
    uw_end = 0
    uw_unchecked = {}
    for location, (roomid, mask) in location_table_uw.items():
        if location not in ctx.locations_checked:
            uw_unchecked[location] = (roomid, mask)
            uw_begin = min(uw_begin, roomid)
            uw_end = max(uw_end, roomid + 1)
    if uw_begin < uw_end:
        uw_data = await snes_read(ctx, SAVEDATA_START + (uw_begin * 2), (uw_end - uw_begin) * 2)
        if uw_data is not None:
            for location, (roomid, mask) in uw_unchecked.items():
                offset = (roomid - uw_begin) * 2
                roomdata = uw_data[offset] | (uw_data[offset + 1] << 8)
                if roomdata & mask != 0:
                    new_check(location)

    ow_begin = 0x82
    ow_end = 0
    ow_unchecked = {}
    for location, screenid in location_table_ow.items():
        if location not in ctx.locations_checked:
            ow_unchecked[location] = screenid
            ow_begin = min(ow_begin, screenid)
            ow_end = max(ow_end, screenid + 1)
    if ow_begin < ow_end:
        ow_data = await snes_read(ctx, SAVEDATA_START + 0x280 + ow_begin, ow_end - ow_begin)
        if ow_data is not None:
            for location, screenid in ow_unchecked.items():
                if ow_data[screenid - ow_begin] & 0x40 != 0:
                    new_check(location)

    if not all([location in ctx.locations_checked for location in location_table_npc.keys()]):
        npc_data = await snes_read(ctx, SAVEDATA_START + 0x410, 2)
        if npc_data is not None:
            npc_value = npc_data[0] | (npc_data[1] << 8)
            for location, mask in location_table_npc.items():
                if npc_value & mask != 0 and location not in ctx.locations_checked:
                    new_check(location)

    if not all([location in ctx.locations_checked for location in location_table_misc.keys()]):
        misc_data = await snes_read(ctx, SAVEDATA_START + 0x3c6, 4)
        if misc_data is not None:
            for location, (offset, mask) in location_table_misc.items():
                assert(0x3c6 <= offset <= 0x3c9)
                if misc_data[offset - 0x3c6] & mask != 0 and location not in ctx.locations_checked:
                    new_check(location)

    await send_msgs(ctx.socket, [['LocationChecks', new_locations]])

async def game_watcher(ctx : Context):
    while not ctx.exit_event.is_set():
        try:
            await asyncio.wait_for(ctx.watcher_event.wait(), 2)
        except asyncio.TimeoutError:
            pass
        ctx.watcher_event.clear()

        if not ctx.rom:
            rom = await snes_read(ctx, ROMNAME_START, ROMNAME_SIZE)
            if rom is None or rom == bytes([0] * ROMNAME_SIZE):
                continue

            ctx.rom = list(rom)
            ctx.locations_checked = set()
            ctx.locations_scouted = set()
            if ctx.awaiting_rom:
                await server_auth(ctx, False)

        if ctx.auth and ctx.auth != ctx.rom:
            logging.warning("ROM change detected, please reconnect to the multiworld server")
            await disconnect(ctx)

        gamemode = await snes_read(ctx, WRAM_START + 0x10, 1)
        if gamemode is None or gamemode[0] not in INGAME_MODES:
            continue

        data = await snes_read(ctx, RECV_PROGRESS_ADDR, 8)
        if data is None:
            continue

        recv_index = data[0] | (data[1] << 8)
        assert RECV_ITEM_ADDR == RECV_PROGRESS_ADDR + 2
        recv_item = data[2]
        assert ROOMID_ADDR == RECV_PROGRESS_ADDR + 4
        roomid = data[4] | (data[5] << 8)
        assert ROOMDATA_ADDR == RECV_PROGRESS_ADDR + 6
        roomdata = data[6]
        assert SCOUT_LOCATION_ADDR == RECV_PROGRESS_ADDR + 7
        scout_location = data[7]

        if recv_index < len(ctx.items_received) and recv_item == 0:
            item = ctx.items_received[recv_index]
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(get_item_name_from_id(item.item), 'red', 'bold'), color(ctx.player_names[item.player], 'yellow'),
                get_location_name_from_address(item.location), recv_index + 1, len(ctx.items_received)))
            recv_index += 1
            snes_buffered_write(ctx, RECV_PROGRESS_ADDR, bytes([recv_index & 0xFF, (recv_index >> 8) & 0xFF]))
            snes_buffered_write(ctx, RECV_ITEM_ADDR, bytes([item.item]))
            snes_buffered_write(ctx, RECV_ITEM_PLAYER_ADDR, bytes([item.player if item.player != ctx.slot else 0]))
        if scout_location > 0 and scout_location in ctx.locations_info:
            snes_buffered_write(ctx, SCOUTREPLY_LOCATION_ADDR, bytes([scout_location]))
            snes_buffered_write(ctx, SCOUTREPLY_ITEM_ADDR, bytes([ctx.locations_info[scout_location][0]]))
            snes_buffered_write(ctx, SCOUTREPLY_PLAYER_ADDR, bytes([ctx.locations_info[scout_location][1]]))

        await snes_flush_writes(ctx)

        if scout_location > 0 and scout_location not in ctx.locations_scouted:
            ctx.locations_scouted.add(scout_location)
            logging.info(f'Scouting item at {list(Regions.lookup_id_to_name.keys())[scout_location - 1]}')
            await send_msgs(ctx.socket, [['LocationScouts', [scout_location]]])
        await track_locations(ctx, roomid, roomdata)

def processSpoiler(ctx : Context):
    global countdown_use_triforces, countdown_use_keys, countdown_region_table, countdown_triforce_locs, countdown_triforces, countdown_item_locs, countdown_items, countdown_key_locs, countdown_keys
    file1 = open('countdown_spoiler.txt', 'r')
    lines = file1.readlines()
    file1.close()
    playerName = 'Blah'
    if ctx.slot is not None:
        playerName = ' (' + ctx.player_names[ctx.slot] + ')'
    locationsFound = False
    isMultiworld = False
    isMultiworldChecked = False
    for line in lines:
        if not locationsFound:
            if not countdown_use_triforces and ('triforcehunt' in line):
                countdown_use_triforces = True
            elif not countdown_use_keys and (('Small Key shuffle:' in line) or ('Big Key shuffle:' in line)) and ('Yes' in line):
                countdown_use_keys = True
            elif not isMultiworldChecked and ('Players:' in line):
                isMultiworldChecked = True
                tokens = line.split()
                try:
                    numPlayers = int(tokens[1])
                    if numPlayers > 1:
                        isMultiworld = True
                except Exception as e:
                    print(e)
                    logging.warning(e)
                
            elif 'Locations:' in line:
                locationsFound = True
            # TODO: key drops
        elif 'Shops:' in line:
            break
        elif ': ' in line:
            tokens = line.split(': ')
            locationName = tokens[0]
            itemName = tokens[1]
            isMyLocation = True
            if isMultiworld:
                playerNameIndex = locationName.find(playerName)
                isMyLocation = (playerNameIndex > -1)
                if isMyLocation:
                    locationName = locationName[0:playerNameIndex]
            if isMyLocation:
                regionName = countdown_region_table.get(locationName)
                if regionName is not None:
                    if countdown_use_triforces and ('Triforce Piece' in itemName):
                        countdown_triforce_locs.add(locationName)
                        countdown_triforces[regionName] = countdown_triforces[regionName] + 1
                    elif countdown_use_keys and ('Key' in itemName) and (countdown_use_keydrops or (not(('Key Drop' in locationName) or ('Pot Key' in locationName)))):
                        countdown_key_locs.add(locationName)
                        countdown_keys[regionName] = countdown_keys[regionName] + 1
                    else:
                        for val in countdown_item_names:
                            if val in itemName:
                                countdown_item_locs.add(locationName)
                                countdown_items[regionName] = countdown_items[regionName] + 1
                                break
    print("Finished parsing spoiler log.")

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--snes', default='localhost:8080', help='Address of the QUsb2snes server.')
    parser.add_argument('--connect', default=None, help='Address of the multiworld host.')
    parser.add_argument('--password', default=None, help='Password of the multiworld host.')
    parser.add_argument('--loglevel', default='info', choices=['debug', 'info', 'warning', 'error', 'critical'])
    args = parser.parse_args()

    logging.basicConfig(format='%(message)s', level=getattr(logging, args.loglevel.upper(), logging.INFO))

    ctx = Context(args.snes, args.connect, args.password)

    input_task = asyncio.create_task(console_loop(ctx))

    await snes_connect(ctx, ctx.snes_address)
    processSpoiler(ctx)

#    if ctx.server_task is None:
#        ctx.server_task = asyncio.create_task(server_loop(ctx))

    watcher_task = asyncio.create_task(game_watcher(ctx))


    await ctx.exit_event.wait()
    ctx.server_address = None
    ctx.snes_reconnect_address = None

    await watcher_task

#    if ctx.socket is not None and not ctx.socket.closed:
#        await ctx.socket.close()
#    if ctx.server_task is not None:
#        await ctx.server_task

    if ctx.snes_socket is not None and not ctx.snes_socket.closed:
        await ctx.snes_socket.close()

    while ctx.input_requests > 0:
        ctx.input_queue.put_nowait(None)
        ctx.input_requests -= 1

    await input_task

if __name__ == '__main__':
    colorama.init()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_until_complete(asyncio.gather(*asyncio.Task.all_tasks()))
    loop.close()
    colorama.deinit()
