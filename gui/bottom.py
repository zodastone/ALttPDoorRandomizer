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
    guiargs.retro = bool(parent.pages["randomizer"].pages["item"].widgets["retro"].storageVar.get())
    guiargs.mode = parent.pages["randomizer"].pages["item"].widgets["worldstate"].storageVar.get()
    guiargs.logic = parent.pages["randomizer"].pages["item"].widgets["logiclevel"].storageVar.get()
    guiargs.goal = parent.pages["randomizer"].pages["item"].widgets["goal"].storageVar.get()
    guiargs.crystals_gt = parent.pages["randomizer"].pages["item"].widgets["crystals_gt"].storageVar.get()
    guiargs.crystals_ganon = parent.pages["randomizer"].pages["item"].widgets["crystals_ganon"].storageVar.get()
    guiargs.swords = parent.pages["randomizer"].pages["item"].widgets["weapons"].storageVar.get()
    guiargs.difficulty = parent.pages["randomizer"].pages["item"].widgets["itempool"].storageVar.get()
    guiargs.item_functionality = parent.pages["randomizer"].pages["item"].widgets["itemfunction"].storageVar.get()
    guiargs.timer = parent.pages["randomizer"].pages["item"].widgets["timer"].storageVar.get()
    guiargs.progressive = parent.pages["randomizer"].pages["item"].widgets["progressives"].storageVar.get()
    guiargs.accessibility = parent.pages["randomizer"].pages["item"].widgets["accessibility"].storageVar.get()
    guiargs.algorithm = parent.pages["randomizer"].pages["item"].widgets["sortingalgo"].storageVar.get()

    guiargs.openpyramid = bool(parent.pages["randomizer"].pages["entrance"].widgets["openpyramid"].storageVar.get())
    guiargs.shuffleganon = bool(parent.pages["randomizer"].pages["entrance"].widgets["shuffleganon"].storageVar.get())
    guiargs.shuffle = parent.pages["randomizer"].pages["entrance"].widgets["entranceshuffle"].storageVar.get()

    guiargs.multi = int(parent.pages["randomizer"].pages["multiworld"].widgets["worlds"].storageVar.get())
    guiargs.names = parent.pages["randomizer"].pages["multiworld"].namesVar.get()
    guiargs.seed = int(parent.frames["bottom"].seedVar.get()) if parent.frames["bottom"].seedVar.get() else None
    guiargs.count = int(parent.frames["bottom"].widgets["generationcount"].storageVar.get()) if parent.frames["bottom"].widgets["generationcount"].storageVar.get() != '1' else None

    guiargs.door_shuffle = parent.pages["randomizer"].pages["dungeon"].widgets["dungeondoorshuffle"].storageVar.get()
    guiargs.experimental = parent.pages["randomizer"].pages["dungeon"].widgets["experimental"].storageVar.get()
    guiargs.heartbeep = parent.pages["randomizer"].pages["gameoptions"].widgets["heartbeep"].storageVar.get()
    guiargs.heartcolor = parent.pages["randomizer"].pages["gameoptions"].widgets["heartcolor"].storageVar.get()
    guiargs.fastmenu = parent.pages["randomizer"].pages["gameoptions"].widgets["menuspeed"].storageVar.get()
    guiargs.create_spoiler = bool(parent.pages["randomizer"].pages["generation"].widgets["spoiler"].storageVar.get())
    guiargs.skip_playthrough = not bool(parent.pages["randomizer"].pages["generation"].widgets["spoiler"].storageVar.get())
    guiargs.suppress_rom = bool(parent.pages["randomizer"].pages["generation"].widgets["suppressrom"].storageVar.get())
    guiargs.mapshuffle = bool(parent.pages["randomizer"].pages["dungeon"].widgets["mapshuffle"].storageVar.get())
    guiargs.compassshuffle = bool(parent.pages["randomizer"].pages["dungeon"].widgets["compassshuffle"].storageVar.get())
    guiargs.keyshuffle = bool(parent.pages["randomizer"].pages["dungeon"].widgets["smallkeyshuffle"].storageVar.get())
    guiargs.bigkeyshuffle = bool(parent.pages["randomizer"].pages["dungeon"].widgets["bigkeyshuffle"].storageVar.get())
    guiargs.quickswap = bool(parent.pages["randomizer"].pages["gameoptions"].widgets["quickswap"].storageVar.get())
    guiargs.disablemusic = bool(parent.pages["randomizer"].pages["gameoptions"].widgets["nobgm"].storageVar.get())
    guiargs.ow_palettes = parent.pages["randomizer"].pages["gameoptions"].widgets["owpalettes"].storageVar.get()
    guiargs.uw_palettes = parent.pages["randomizer"].pages["gameoptions"].widgets["uwpalettes"].storageVar.get()
    guiargs.hints = bool(parent.pages["randomizer"].pages["gameoptions"].widgets["hints"].storageVar.get())
    guiargs.enemizercli = parent.pages["randomizer"].pages["enemizer"].enemizerCLIpathVar.get()
    guiargs.shufflebosses = parent.pages["randomizer"].pages["enemizer"].widgets["bossshuffle"].storageVar.get()
    guiargs.shuffleenemies = parent.pages["randomizer"].pages["enemizer"].widgets["enemyshuffle"].storageVar.get()
    guiargs.enemy_health = parent.pages["randomizer"].pages["enemizer"].widgets["enemyhealth"].storageVar.get()
    guiargs.enemy_damage = parent.pages["randomizer"].pages["enemizer"].widgets["enemydamage"].storageVar.get()
    guiargs.shufflepots = bool(parent.pages["randomizer"].pages["enemizer"].widgets["potshuffle"].storageVar.get())
    guiargs.custom = bool(parent.pages["randomizer"].pages["generation"].widgets["usecustompool"].storageVar.get())
    guiargs.customitemarray = [int(parent.pages["custom"].content.customWidgets["bow"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["silversupgrade"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["boomerang"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["redmerang"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["hookshot"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["mushroom"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["powder"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["firerod"].storageVar.get()),
                               int(parent.pages["custom"].content.customWidgets["icerod"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["bombos"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["ether"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["quake"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["lamp"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["hammer"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["shovel"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["flute"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["bugnet"].storageVar.get()),
                               int(parent.pages["custom"].content.customWidgets["book"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["bottle"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["somaria"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["byrna"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["cape"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["mirror"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["boots"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["powerglove"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["titansmitt"].storageVar.get()),
                               int(parent.pages["custom"].content.customWidgets["progressiveglove"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["flippers"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["pearl"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["heartpiece"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["heartcontainer"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["sancheart"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["sword1"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["sword2"].storageVar.get()),
                               int(parent.pages["custom"].content.customWidgets["sword3"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["sword4"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["progressivesword"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["shield1"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["shield2"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["shield3"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["progressiveshield"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["mail2"].storageVar.get()),
                               int(parent.pages["custom"].content.customWidgets["mail3"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["progressivemail"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["halfmagic"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["quartermagic"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["bombsplus5"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["bombsplus10"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["arrowsplus5"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["arrowsplus10"].storageVar.get()),
                               int(parent.pages["custom"].content.customWidgets["arrow1"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["arrow10"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["bomb1"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["bomb3"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["rupee1"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["rupee5"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["rupee20"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["rupee50"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["rupee100"].storageVar.get()),
                               int(parent.pages["custom"].content.customWidgets["rupee300"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["rupoor"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["blueclock"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["greenclock"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["redclock"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["progressivebow"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["bomb10"].storageVar.get()), int(parent.pages["custom"].content.customWidgets["triforcepieces"].storageVar.get()),int(parent.pages["custom"].content.customWidgets["triforcepiecesgoal"].storageVar.get()),
                               int(parent.pages["custom"].content.customWidgets["triforce"].storageVar.get()),int(parent.pages["custom"].content.customWidgets["rupoorcost"].storageVar.get()),int(parent.pages["custom"].content.customWidgets["generickeys"].storageVar.get())]
    guiargs.rom = parent.pages["randomizer"].pages["generation"].romVar.get()
    guiargs.sprite = parent.pages["randomizer"].pages["gameoptions"].widgets["sprite"]["spriteObject"]
    guiargs.randomSprite = parent.randomSprite.get()
    guiargs.outputpath = parent.outputPath.get()
    return guiargs
