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
from gui.loadcliargs import loadcliargs
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

    # load args from CLI into options
    loadcliargs(self,args)

    mainWindow.mainloop()

if __name__ == '__main__':
    args = parse_arguments(None)
    guiMain(args)
