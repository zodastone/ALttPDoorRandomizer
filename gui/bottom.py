from tkinter import ttk, messagebox, StringVar, Button, Entry, Frame, Label, Spinbox, E, W, LEFT, RIGHT, X
from argparse import Namespace
import logging
import os
import random
from CLI import parse_arguments, get_settings
from Main import main
from Utils import local_path, output_path, open_file
import gui.widgets as widgets


def bottom_frame(self, parent, args=None):
    # Bottom Frame
    self = ttk.Frame(parent)

    # Bottom Frame options
    self.widgets = {}

    seedCountFrame = Frame(self)
    seedCountFrame.pack()
    ## Seed #
    seedLabel = Label(self, text='Seed #')
    savedSeed = parent.settings["seed"]
    self.seedVar = StringVar(value=savedSeed)
    def saveSeed(caller,_,mode):
        savedSeed = self.seedVar.get()
        parent.settings["seed"] = int(savedSeed) if savedSeed.isdigit() else None
    self.seedVar.trace_add("write",saveSeed)
    seedEntry = Entry(self, width=15, textvariable=self.seedVar)
    seedLabel.pack(side=LEFT)
    seedEntry.pack(side=LEFT)

    ## Number of Generation attempts
    key = "generationcount"
    self.widgets[key] = widgets.make_widget(
      self,
      "spinbox",
      self,
      "Count",
      None,
      {"label": {"side": LEFT}, "spinbox": {"side": RIGHT}}
    )
    self.widgets[key].pack(side=LEFT)

    def generateRom():
        guiargs = create_guiargs(parent)
        # get default values for missing parameters
        for k,v in vars(parse_arguments(['--multi', str(guiargs.multi)])).items():
            if k not in vars(guiargs):
                setattr(guiargs, k, v)
            elif type(v) is dict: # use same settings for every player
                setattr(guiargs, k, {player: getattr(guiargs, k) for player in range(1, guiargs.multi + 1)})
        try:
            if guiargs.count is not None:
                seed = guiargs.seed
                for _ in range(guiargs.count):
                    main(seed=seed, args=guiargs)
                    seed = random.randint(0, 999999999)
            else:
                main(seed=guiargs.seed, args=guiargs)
        except Exception as e:
            logging.exception(e)
            messagebox.showerror(title="Error while creating seed", message=str(e))
        else:
            messagebox.showinfo(title="Success", message="Rom patched successfully")

    ## Generate Button
    generateButton = Button(self, text='Generate Patched Rom', command=generateRom)
    generateButton.pack(side=LEFT)

    def open_output():
        if args and args.outputpath:
            open_file(output_path(args.outputpath))
        else:
            open_file(output_path(parent.settings["outputpath"]))

    openOutputButton = Button(self, text='Open Output Directory', command=open_output)
    openOutputButton.pack(side=RIGHT)

    if os.path.exists(local_path('README.html')):
        def open_readme():
            open_file(local_path('README.html'))
        openReadmeButton = Button(self, text='Open Documentation', command=open_readme)
        openReadmeButton.pack()

    return self


def create_guiargs(parent):
    guiargs = Namespace()

    # set up settings to gather
    # Page::Subpage::GUI-id::param-id
    options = {
      "randomizer": {
        "item": {
          "retro": "retro",
          "worldstate": "mode",
          "logiclevel": "logic",
          "goal": "goal",
          "crystals_gt": "crystals_gt",
          "crystals_ganon": "crystals_ganon",
          "weapons": "swords",
          "itempool": "difficulty",
          "itemfunction": "item_functionality",
          "timer": "timer",
          "progressives": "progressive",
          "accessibility": "accessibility",
          "sortingalgo": "algorithm"
        },
        "entrance": {
          "openpyramid": "openpyramid",
          "shuffleganon": "shuffleganon",
          "entranceshuffle": "shuffle"
        },
        "enemizer": {
          "potshuffle": "shufflepots",
          "enemyshuffle": "shuffleenemies",
          "bossshuffle": "shufflebosses",
          "enemydamage": "enemy_damage",
          "enemyhealth": "enemy_health"
        },
        "dungeon": {
          "mapshuffle": "mapshuffle",
          "compassshuffle": "compassshuffle",
          "smallkeyshuffle": "keyshuffle",
          "bigkeyshuffle": "bigkeyshuffle",
          "dungeondoorshuffle": "door_shuffle",
          "experimental": "experimental"
        },
        "multiworld": {
          "names": "names"
        },
        "gameoptions": {
          "hints": "hints",
          "nobgm": "disablemusic",
          "quickswap": "quickswap",
          "heartcolor": "heartcolor",
          "heartbeep": "heartbeep",
          "menuspeed": "fastmenu",
          "owpalettes": "ow_palettes",
          "uwpalettes": "uw_palettes"
        },
        "generation": {
          "spoiler": "create_spoiler",
          "suppressrom": "suppress_rom"
        } 
      }
    }
    for mainpage in options:
        for subpage in options[mainpage]:
            for widget in options[mainpage][subpage]:
                arg = options[mainpage][subpage][widget]
                setattr(guiargs, arg, parent.pages[mainpage].pages[subpage].widgets[widget].storageVar.get())

    guiargs.multi = int(parent.pages["randomizer"].pages["multiworld"].widgets["worlds"].storageVar.get())

    guiargs.rom = parent.pages["randomizer"].pages["generation"].romVar.get()
    guiargs.custom = bool(parent.pages["randomizer"].pages["generation"].widgets["usecustompool"].storageVar.get())

    guiargs.seed = int(parent.frames["bottom"].seedVar.get()) if parent.frames["bottom"].seedVar.get() else None
    guiargs.count = int(parent.frames["bottom"].widgets["generationcount"].storageVar.get()) if parent.frames["bottom"].widgets["generationcount"].storageVar.get() != '1' else None

    customitems = [
      "bow", "silversupgrade", "boomerang", "redmerang", "hookshot", "mushroom", "powder", "firerod",
      "icerod", "bombos", "ether", "quake", "lamp", "hammer", "shovel", "flute", "bugnet",
      "book", "bottle", "somaria", "byrna", "cape", "mirror", "boots", "powerglove", "titansmitt",
      "progressiveglove", "flippers", "pearl", "heartpiece", "heartcontainer", "sancheart", "sword1", "sword2",
      "sword3", "sword4", "progressivesword", "shield1", "shield2", "shield3", "progressiveshield", "mail2",
      "mail3", "progressivemail", "halfmagic", "quartermagic", "bombsplus5", "bombsplus10", "arrowsplus5", "arrowsplus10",
      "arrow1", "arrow10", "bomb1", "bomb3", "rupee1", "rupee5", "rupee20", "rupee50", "rupee100",
      "rupee300", "rupoor", "blueclock", "greenclock", "redclock", "progressivebow", "bomb10", "triforcepieces", "triforcepiecesgoal",
      "triforce", "rupoorcost", "generickeys"
    ]
    guiargs.customitemarray = []
    for customitem in customitems:
        guiargs.customitemarray.append(int(parent.pages["custom"].content.customWidgets[customitem].storageVar.get()))

    guiargs.sprite = parent.pages["randomizer"].pages["gameoptions"].widgets["sprite"]["spriteObject"]
    guiargs.randomSprite = parent.randomSprite.get()
    guiargs.outputpath = parent.outputPath.get()
    return guiargs
