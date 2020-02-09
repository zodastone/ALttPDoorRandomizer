#!/usr/bin/env python3
from argparse import Namespace
from glob import glob
import json
import logging
import random
import os
import shutil
from tkinter import Checkbutton, OptionMenu, Toplevel, LabelFrame, PhotoImage, Tk, LEFT, RIGHT, BOTTOM, TOP, StringVar, IntVar, Frame, Label, W, E, X, BOTH, Entry, Spinbox, Button, filedialog, messagebox, ttk
from urllib.parse import urlparse
from urllib.request import urlopen

from AdjusterMain import adjust
from DungeonRandomizer import parse_arguments
from gui.adjust.overview import adjust_page
from gui.custom.overview import custom_page
from gui.randomize.item import item_page
from gui.randomize.entrando import entrando_page
from gui.randomize.enemizer import enemizer_page
from gui.randomize.dungeon import dungeon_page
from gui.randomize.multiworld import multiworld_page
from gui.randomize.gameoptions import gameoptions_page
from gui.randomize.generation import generation_page
from gui.bottom import bottom_frame
from GuiUtils import ToolTips, set_icon, BackgroundTaskProgress
from Main import main, __version__ as ESVersion
from Rom import Sprite
from Utils import is_bundled, local_path, output_path, open_file


def guiMain(args=None):
    mainWindow = Tk()
    self = mainWindow
    mainWindow.wm_title("Door Shuffle %s" % ESVersion)

    set_icon(mainWindow)

    notebook = ttk.Notebook(self)
    self.randomizerWindow = ttk.Frame(notebook)
    self.adjustWindow = ttk.Frame(notebook)
    self.customWindow = ttk.Frame(notebook)
    notebook.add(self.randomizerWindow, text='Randomize')
    notebook.add(self.adjustWindow, text='Adjust')
    notebook.add(self.customWindow, text='Custom')
    notebook.pack()

    # randomizer controls

    # Randomize notebook page:
    #  make notebook pages: Item, Entrances, Enemizer, Dungeon Shuffle, Multiworld, Game Options, Generation Setup
    #   Item:             Item Randomizer settings
    #   Entrances:        Entrance Randomizer settings
    #   Enemizer:         Enemy Randomizer settings
    #   Dungeon Shuffle:  Dungeon Door Randomizer settings
    #   Multiworld:       Multiworld settings
    #   Game Options:     Cosmetic settings that don't affect logic/placement
    #   Generation Setup: Primarily one&done settings
    self.randomizerNotebook = ttk.Notebook(self.randomizerWindow)

    # Item Randomizer
    self.itemWindow = item_page(self.randomizerNotebook)
    self.randomizerNotebook.add(self.itemWindow, text="Items")

    # Entrance Randomizer
    self.entrandoWindow = entrando_page(self.randomizerNotebook)
    self.randomizerNotebook.add(self.entrandoWindow, text="Entrances")

    # Enemizer
    self.enemizerWindow = enemizer_page(self.randomizerNotebook)
    self.randomizerNotebook.add(self.enemizerWindow, text="Enemizer")

    # Dungeon Shuffle
    self.dungeonRandoWindow = dungeon_page(self.randomizerNotebook)
    self.randomizerNotebook.add(self.dungeonRandoWindow, text="Dungeon Shuffle")

    # Multiworld
    self.multiworldWindow = multiworld_page(self.randomizerNotebook)
    self.randomizerNotebook.add(self.multiworldWindow, text="Multiworld")

    # Game Options
    self.gameOptionsWindow = gameoptions_page(self.randomizerNotebook)
    self.randomizerNotebook.add(self.gameOptionsWindow, text="Game Options")

    # Generation Setup
    self.generationSetupWindow = generation_page(self.randomizerNotebook)
    self.randomizerNotebook.add(self.generationSetupWindow, text="Generation Setup")

    # add randomizer notebook to main window
    self.randomizerNotebook.pack()

    # bottom of window: Open Output Directory, Open Documentation (if exists)
    self.farBottomFrame = bottom_frame(self,self,None)
    # set bottom frame to main window
    self.farBottomFrame.pack(side=BOTTOM, fill=X, padx=5, pady=5)

    # Adjuster Controls
    self.adjustContent = adjust_page(self,self.adjustWindow)
#    self.adjustContent,self.working_dirs = adjust_page(self,self.adjustWindow,self.working_dirs)
    self.adjustContent.pack(side=TOP, fill=BOTH, expand=True)

    # Custom Controls
    self.customContent = custom_page(self,self.customWindow)
    self.customContent.pack(side=TOP, pady=(17,0))

    def validation(P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
    vcmd=(self.customContent.register(validation), '%P')

    if args is not None:
        for k,v in vars(args).items():
            if type(v) is dict:
                setattr(args, k, v[1]) # only get values for player 1 for now
        # load values from commandline args
        self.generationSetupWindow.createSpoilerVar.set(int(args.create_spoiler))
        self.generationSetupWindow.suppressRomVar.set(int(args.suppress_rom))
        self.dungeonRandoWindow.mapshuffleVar.set(args.mapshuffle)
        self.dungeonRandoWindow.compassshuffleVar.set(args.compassshuffle)
        self.dungeonRandoWindow.keyshuffleVar.set(args.keyshuffle)
        self.dungeonRandoWindow.bigkeyshuffleVar.set(args.bigkeyshuffle)
        self.itemWindow.retroVar.set(args.retro)
        self.entrandoWindow.openpyramidVar.set(args.openpyramid)
        self.gameOptionsWindow.quickSwapVar.set(int(args.quickswap))
        self.gameOptionsWindow.disableMusicVar.set(int(args.disablemusic))
        if args.multi:
            self.multiworldWindow.worldVar.set(str(args.multi))
        if args.count:
            self.farBottomFrame.countVar.set(str(args.count))
        if args.seed:
            self.farBottomFrame.seedVar.set(str(args.seed))
        self.itemWindow.modeVar.set(args.mode)
        self.itemWindow.swordVar.set(args.swords)
        self.itemWindow.difficultyVar.set(args.difficulty)
        self.itemWindow.itemfunctionVar.set(args.item_functionality)
        self.itemWindow.timerVar.set(args.timer)
        self.itemWindow.progressiveVar.set(args.progressive)
        self.itemWindow.accessibilityVar.set(args.accessibility)
        self.itemWindow.goalVar.set(args.goal)
        self.itemWindow.crystalsGTVar.set(args.crystals_gt)
        self.itemWindow.crystalsGanonVar.set(args.crystals_ganon)
        self.itemWindow.algorithmVar.set(args.algorithm)
        self.entrandoWindow.shuffleVar.set(args.shuffle)
        self.dungeonRandoWindow.doorShuffleVar.set(args.door_shuffle)
        self.gameOptionsWindow.heartcolorVar.set(args.heartcolor)
        self.gameOptionsWindow.heartbeepVar.set(args.heartbeep)
        self.gameOptionsWindow.fastMenuVar.set(args.fastmenu)
        self.itemWindow.logicVar.set(args.logic)
        self.generationSetupWindow.romVar.set(args.rom)
        self.entrandoWindow.shuffleGanonVar.set(args.shuffleganon)
        self.gameOptionsWindow.hintsVar.set(args.hints)
        self.enemizerWindow.enemizerCLIpathVar.set(args.enemizercli)
        self.enemizerWindow.potShuffleVar.set(args.shufflepots)
        self.enemizerWindow.enemyShuffleVar.set(args.shuffleenemies)
        self.enemizerWindow.enemizerBossVar.set(args.shufflebosses)
        self.enemizerWindow.enemizerDamageVar.set(args.enemy_damage)
        self.enemizerWindow.enemizerHealthVar.set(args.enemy_health)
        self.gameOptionsWindow.owPalettesVar.set(args.ow_palettes)
        self.gameOptionsWindow.uwPalettesVar.set(args.uw_palettes)
#        if args.sprite is not None:
#            self.gameOptionsWindow.set_sprite(Sprite(args.sprite))

    mainWindow.mainloop()

if __name__ == '__main__':
    guiMain()
