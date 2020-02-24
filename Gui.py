#!/usr/bin/env python3
import json
import os
import sys
from tkinter import Tk, Button, BOTTOM, TOP, StringVar, BooleanVar, X, BOTH, RIGHT, ttk, messagebox

from argparse import Namespace
from CLI import get_settings, get_args_priority
from DungeonRandomizer import parse_arguments
from gui.adjust.overview import adjust_page
from gui.startinventory.overview import startinventory_page
from gui.custom.overview import custom_page
from gui.loadcliargs import loadcliargs, loadadjustargs
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
        for widget in self.pages["adjust"].content.widgets:
            args["adjust." + widget] = self.pages["adjust"].content.widgets[widget].storageVar.get()
        with open(os.path.join(settings_path, "settings.json"), "w+") as f:
            f.write(json.dumps(args, indent=2))
        os.chmod(os.path.join(settings_path, "settings.json"),0o755)

    def save_settings_from_gui():
        gui_args = vars(create_guiargs(self))
        if self.randomSprite.get():
            gui_args['sprite'] = 'random'
        elif gui_args['sprite']:
            gui_args['sprite'] = gui_args['sprite'].name
        save_settings(gui_args)
        messagebox.showinfo("Door Shuffle " + ESVersion,"Settings saved from GUI.")

    # routine for exiting the app
    def guiExit():
        dosave = messagebox.askyesno("Door Shuffle " + ESVersion, "Save settings before exit?")
        if dosave:
            save_settings_from_gui()
        sys.exit(0)

    # make main window
    # add program title & version number
    mainWindow = Tk()
    self = mainWindow

    mainWindow.wm_title("Door Shuffle %s" % ESVersion)
    mainWindow.protocol("WM_DELETE_WINDOW", guiExit)  # intercept when user clicks the X

    # set program icon
    set_icon(mainWindow)

    # get args
    # getting Settings & CLI (no GUI built yet)
    self.args = get_args_priority(None, None, None)

    # get saved settings
    self.settings = self.args["settings"]

    # make array for pages
    self.pages = {}

    # make array for frames
    self.frames = {}

    self.notebook = ttk.Notebook(self)
    self.pages["randomizer"] = ttk.Frame(self.notebook)
    self.pages["adjust"] = ttk.Frame(self.notebook)
    self.pages["startinventory"] = ttk.Frame(self.notebook)
    self.pages["custom"] = ttk.Frame(self.notebook)
    self.notebook.add(self.pages["randomizer"], text='Randomize')
    self.notebook.add(self.pages["adjust"], text='Adjust')
    self.notebook.add(self.pages["startinventory"], text='Starting Inventory')
    self.notebook.add(self.pages["custom"], text='Custom Item Pool')
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

    # make array for pages
    self.pages["randomizer"].pages = {}

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
    ## Save Settings Button
    savesettingsButton = Button(self.frames["bottom"], text='Save Settings to File', command=save_settings_from_gui)
    savesettingsButton.pack(side=RIGHT)

    # set bottom frame to main window
    self.frames["bottom"].pack(side=BOTTOM, fill=X, padx=5, pady=5)

    self.outputPath = StringVar()
    self.randomSprite = BooleanVar()

    # Adjuster Controls
    self.pages["adjust"].content,self.settings = adjust_page(self, self.pages["adjust"], self.settings)
    self.pages["adjust"].content.pack(side=TOP, fill=BOTH, expand=True)

    # Starting Inventory Controls
    self.pages["startinventory"].content = startinventory_page(self, self.pages["startinventory"])
    self.pages["startinventory"].content.pack(side=TOP, fill=BOTH, expand=True)

    # Custom Controls
    self.pages["custom"].content = custom_page(self,self.pages["custom"])
    self.pages["custom"].content.pack(side=TOP, fill=BOTH, expand=True)

    def validation(P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
    vcmd=(self.pages["custom"].content.register(validation), '%P')

    # load args
    loadcliargs(self, self.args["load"])

    # load adjust settings into options
    loadadjustargs(self, self.settings)

    mainWindow.mainloop()


if __name__ == '__main__':
    args = parse_arguments(None)
    guiMain(args)
