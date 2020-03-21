from tkinter import ttk, messagebox, StringVar, Button, Entry, Frame, Label, Spinbox, E, W, LEFT, RIGHT, X
from argparse import Namespace
from functools import partial
import logging
import os
import random
from CLI import parse_arguments, get_settings
from Main import main
from Utils import local_path, output_path, open_file
import classes.constants as CONST
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

    ## Documentation Button
    if os.path.exists(local_path('README.html')):
        def open_readme():
            open_file(local_path('README.html'))
        openReadmeButton = Button(self, text='Open Documentation', command=open_readme)
        openReadmeButton.pack(side=RIGHT)

    return self


def create_guiargs(parent):
    guiargs = Namespace()

    # set up settings to gather
    # Page::Subpage::GUI-id::param-id
    options = CONST.SETTINGSTOPROCESS

    for mainpage in options:
        for subpage in options[mainpage]:
            for widget in options[mainpage][subpage]:
                arg = options[mainpage][subpage][widget]
                setattr(guiargs, arg, parent.pages[mainpage].pages[subpage].widgets[widget].storageVar.get())

    guiargs.enemizercli = parent.pages["randomizer"].pages["enemizer"].enemizerCLIpathVar.get()

    guiargs.multi = int(parent.pages["randomizer"].pages["multiworld"].widgets["worlds"].storageVar.get())

    guiargs.rom = parent.pages["randomizer"].pages["generation"].romVar.get()
    guiargs.custom = bool(parent.pages["randomizer"].pages["generation"].widgets["usecustompool"].storageVar.get())

    guiargs.seed = int(parent.frames["bottom"].seedVar.get()) if parent.frames["bottom"].seedVar.get() else None
    guiargs.count = int(parent.frames["bottom"].widgets["generationcount"].storageVar.get()) if parent.frames["bottom"].widgets["generationcount"].storageVar.get() != '1' else None

    adjustargs = {
      "nobgm": "disablemusic",
      "quickswap": "quickswap",
      "heartcolor": "heartcolor",
      "heartbeep": "heartbeep",
      "menuspeed": "fastmenu",
      "owpalettes": "ow_palettes",
      "uwpalettes": "uw_palettes"
    }
    for adjustarg in adjustargs:
      internal = adjustargs[adjustarg]
      setattr(guiargs,"adjust." + internal, parent.pages["adjust"].content.widgets[adjustarg].storageVar.get())

    customitems = CONST.CUSTOMITEMS
    guiargs.startinventory = []
    guiargs.customitemarray = {}
    guiargs.startinventoryarray = {}
    for customitem in customitems:
        if customitem not in ["triforcepiecesgoal", "triforce", "rupoor", "rupoorcost"]:
            amount = int(parent.pages["startinventory"].content.startingWidgets[customitem].storageVar.get())
            guiargs.startinventoryarray[customitem] = amount
            for i in range(0, amount):
                label = CONST.CUSTOMITEMLABELS[customitems.index(customitem)]
                guiargs.startinventory.append(label)
        guiargs.customitemarray[customitem] = int(parent.pages["custom"].content.customWidgets[customitem].storageVar.get())

    guiargs.startinventory = ','.join(guiargs.startinventory)

    guiargs.sprite = parent.pages["randomizer"].pages["gameoptions"].widgets["sprite"]["spriteObject"]
    guiargs.randomSprite = parent.randomSprite.get()
    guiargs.outputpath = parent.outputPath.get()
    return guiargs
