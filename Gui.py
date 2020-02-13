#!/usr/bin/env python3
import json
import os
import sys
from tkinter import Tk, BOTTOM, TOP, StringVar, BooleanVar, X, BOTH, ttk

from argparse import Namespace
from CLI import get_working_dirs
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
from gui.bottom import bottom_frame, create_guiargs
from GuiUtils import set_icon
from Main import __version__ as ESVersion
from Rom import get_sprite_from_name


def guiMain(args=None):
    # save working dirs
    def save_working_dirs():
        user_resources_path = os.path.join(".","resources","user")
        working_dirs_path = os.path.join(user_resources_path)
        if not os.path.exists(working_dirs_path):
            os.makedirs(working_dirs_path)
        with open(os.path.join(working_dirs_path, "working_dirs.json"),"w+") as f:
            f.write(json.dumps(self.working_dirs, indent=2))
        os.chmod(os.path.join(working_dirs_path, "working_dirs.json"),0o755)

    def save_settings(args):
        user_resources_path = os.path.join(".", "resources", "user")
        settings_path = os.path.join(user_resources_path)
        if not os.path.exists(settings_path):
            os.makedirs(settings_path)
        with open(os.path.join(settings_path, "settings.json"), "w+") as f:
            f.write(json.dumps(args, indent=2))

    # routine for exiting the app
    def guiExit():
        save_working_dirs()
        gui_args = vars(create_guiargs(self))
        if self.randomSprite.get():
            gui_args['sprite'] = 'random'
        elif gui_args['sprite']:
            gui_args['sprite'] = gui_args['sprite'].name
        save_settings(gui_args)
        sys.exit(0)

    # make main window
    # add program title & version number
    mainWindow = Tk()
    self = mainWindow
    mainWindow.wm_title("Door Shuffle %s" % ESVersion)
    mainWindow.protocol("WM_DELETE_WINDOW", guiExit)  # intercept when user clicks the X

    # set program icon
    set_icon(mainWindow)

    # get working dirs
    self.working_dirs = get_working_dirs()

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
    self.enemizerWindow,self.working_dirs = enemizer_page(self.randomizerNotebook,self.working_dirs)
    self.randomizerNotebook.add(self.enemizerWindow, text="Enemizer")

    # Dungeon Shuffle
    self.dungeonRandoWindow = dungeon_page(self.randomizerNotebook)
    self.randomizerNotebook.add(self.dungeonRandoWindow, text="Dungeon Shuffle")

    # Multiworld
    self.multiworldWindow,self.working_dirs = multiworld_page(self.randomizerNotebook,self.working_dirs)
    self.randomizerNotebook.add(self.multiworldWindow, text="Multiworld")

    # Game Options
    self.gameOptionsWindow = gameoptions_page(self, self.randomizerNotebook)
    self.randomizerNotebook.add(self.gameOptionsWindow, text="Game Options")

    # Generation Setup
    self.generationSetupWindow,self.working_dirs = generation_page(self.randomizerNotebook,self.working_dirs)
    self.randomizerNotebook.add(self.generationSetupWindow, text="Generation Setup")

    # add randomizer notebook to main window
    self.randomizerNotebook.pack()

    # bottom of window: Open Output Directory, Open Documentation (if exists)
    self.farBottomFrame = bottom_frame(self, self, None)
    # set bottom frame to main window
    self.farBottomFrame.pack(side=BOTTOM, fill=X, padx=5, pady=5)

    self.outputPath = StringVar()
    self.randomSprite = BooleanVar()

    # Adjuster Controls
    self.adjustContent,self.working_dirs = adjust_page(self, self.adjustWindow, self.working_dirs)
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
    loadcliargs(self, args)

    # load settings second
    settings_path = os.path.join(".", "resources", "user", "settings.json")
    if os.path.exists(settings_path):
        with(open(settings_path)) as json_file:
            data = json.load(json_file)
            if 'sprite' in data.keys() and data['sprite']:
                data['sprite'] = get_sprite_from_name(data['sprite'])
            settings_args = Namespace(**data)
            loadcliargs(self, settings_args)

    mainWindow.mainloop()


if __name__ == '__main__':
    args = parse_arguments(None)
    guiMain(args)
