#!/usr/bin/env python3
import json
import os
import sys
from tkinter import Tk, BOTTOM, TOP, StringVar, BooleanVar, X, BOTH, ttk

from argparse import Namespace
from CLI import get_settings
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
    def save_settings(args):
        user_resources_path = os.path.join(".", "resources", "user")
        settings_path = os.path.join(user_resources_path)
        if not os.path.exists(settings_path):
            os.makedirs(settings_path)
        with open(os.path.join(settings_path, "settings.json"), "w+") as f:
            f.write(json.dumps(args, indent=2))
        os.chmod(os.path.join(settings_path, "settings.json"),0o755)

    # routine for exiting the app
    def guiExit():
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

    # get saved settings
    self.settings = get_settings()

    self.notebook = ttk.Notebook(self)
    self.pages["randomizer"] = ttk.Frame(self.notebook)
    self.pages["adjust"] = ttk.Frame(self.notebook)
    self.pages["custom"] = ttk.Frame(self.notebook)
    self.notebook.add(self.pages["randomizer"], text='Randomize')
    self.notebook.add(self.pages["adjust"], text='Adjust')
    self.notebook.add(self.pages["custom"], text='Custom')
    self.notebook.pack()

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
    self.pages["randomizer"].notebook = ttk.Notebook(self.pages["randomizer"])

    # Item Randomizer
    self.pages["randomizer"].pages["item"] = item_page(self.pages["randomizer"].notebook)
    self.pages["randomizer"].notebook.add(self.pages["randomizer"].pages["item"], text="Items")

    # Entrance Randomizer
    self.pages["randomizer"].pages["entrance"] = entrando_page(self.pages["randomizer"].notebook)
    self.pages["randomizer"].notebook.add(self.pages["randomizer"].pages["entrance"], text="Entrances")

    # Enemizer
    self.pages["randomizer"].pages["enemizer"],self.settings = enemizer_page(self.pages["randomizer"].notebook,self.settings)
    self.pages["randomizer"].notebook.add(self.pages["randomizer"].pages["enemizer"], text="Enemizer")

    # Dungeon Shuffle
    self.pages["randomizer"].pages["dungeon"] = dungeon_page(self.pages["randomizer"].notebook)
    self.pages["randomizer"].notebook.add(self.pages["randomizer"].pages["dungeon"], text="Dungeon Shuffle")

    # Multiworld
    self.pages["randomizer"].pages["multiworld"],self.settings = multiworld_page(self.pages["randomizer"].notebook,self.settings)
    self.pages["randomizer"].notebook.add(self.pages["randomizer"].pages["multiworld"], text="Multiworld")

    # Game Options
    self.pages["randomizer"].pages["gameoptions"] = gameoptions_page(self, self.pages["randomizer"].notebook)
    self.pages["randomizer"].notebook.add(self.pages["randomizer"].pages["gameoptions"], text="Game Options")

    # Generation Setup
    self.pages["randomizer"].pages["generation"],self.settings = generation_page(self.pages["randomizer"].notebook,self.settings)
    self.pages["randomizer"].notebook.add(self.pages["randomizer"].pages["generation"], text="Generation Setup")

    # add randomizer notebook to main window
    self.pages["randomizer"].notebook.pack()

    # bottom of window: Open Output Directory, Open Documentation (if exists)
    self.frames["bottom"] = bottom_frame(self, self, None)
    # set bottom frame to main window
    self.frames["bottom"].pack(side=BOTTOM, fill=X, padx=5, pady=5)

    self.outputPath = StringVar()
    self.randomSprite = BooleanVar()

    # Adjuster Controls
    self.pages["adjust"].content,self.settings = adjust_page(self, self.pages["adjust"], self.settings)
    self.pages["adjust"].content.pack(side=TOP, fill=BOTH, expand=True)

    # Custom Controls
    self.customContent = custom_page(self,self.pages["custom"])
    self.customContent.pack(side=TOP, pady=(17,0))

    def validation(P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
    vcmd=(self.customContent.register(validation), '%P')

    # load args from CLI into options
    loadcliargs(self, args)

    mainWindow.mainloop()


if __name__ == '__main__':
    args = parse_arguments(None)
    guiMain(args)
