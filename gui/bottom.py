from tkinter import ttk, messagebox, StringVar, Button, Entry, Frame, Label, Spinbox, E, W, LEFT, RIGHT, X
from argparse import Namespace
import logging
import os
import random
from CLI import parse_arguments, get_working_dirs
from Main import main
from Utils import local_path, output_path, open_file

def bottom_frame(self,parent,args=None):
    self = ttk.Frame(parent)
    seedCountFrame = Frame(self)
    seedCountFrame.pack()
    ## Seed #
    seedLabel = Label(self, text='Seed #')
    savedSeed = parent.working_dirs["gen.seed"]
    self.seedVar = StringVar(value=savedSeed)
    def saveSeed(caller,_,mode):
        savedSeed = self.seedVar.get()
        parent.working_dirs["gen.seed"] = int(savedSeed) if savedSeed.isdigit() else None
    self.seedVar.trace_add("write",saveSeed)
    seedEntry = Entry(self, width=15, textvariable=self.seedVar)
    seedLabel.pack(side=LEFT)
    seedEntry.pack(side=LEFT)
    ## Number of Generation attempts
    countLabel = Label(self, text='Count')
    self.countVar = StringVar(value=parent.working_dirs["gen.count"])
    countSpinbox = Spinbox(self, from_=1, to=100, width=5, textvariable=self.countVar)
    countLabel.pack(side=LEFT)
    countSpinbox.pack(side=LEFT)

    def generateRom():
        guiargs = Namespace()
        guiargs.multi = int(parent.multiworldWindow.multiworldWidgets["worlds"].storageVar.get())
        guiargs.names = parent.multiworldWindow.namesVar.get()
        guiargs.seed = int(parent.farBottomFrame.seedVar.get()) if parent.farBottomFrame.seedVar.get() else None
        guiargs.count = int(parent.farBottomFrame.countVar.get()) if parent.farBottomFrame.countVar.get() != '1' else None
        guiargs.mode = parent.itemWindow.itemWidgets["worldstate"].storageVar.get()
        guiargs.logic = parent.itemWindow.itemWidgets["logiclevel"].storageVar.get()

        guiargs.goal = parent.itemWindow.itemWidgets["goal"].storageVar.get()
        guiargs.crystals_gt = parent.itemWindow.itemWidgets["crystals_gt"].storageVar.get()
        guiargs.crystals_ganon = parent.itemWindow.itemWidgets["crystals_ganon"].storageVar.get()
        guiargs.swords = parent.itemWindow.itemWidgets["weapons"].storageVar.get()
        guiargs.difficulty = parent.itemWindow.itemWidgets["itempool"].storageVar.get()
        guiargs.item_functionality = parent.itemWindow.itemWidgets["itemfunction"].storageVar.get()
        guiargs.timer = parent.itemWindow.itemWidgets["timer"].storageVar.get()
        guiargs.progressive = parent.itemWindow.itemWidgets["progressives"].storageVar.get()
        guiargs.accessibility = parent.itemWindow.itemWidgets["accessibility"].storageVar.get()
        guiargs.algorithm = parent.itemWindow.itemWidgets["sortingalgo"].storageVar.get()
        guiargs.shuffle = parent.entrandoWindow.entrandoWidgets["entranceshuffle"].storageVar.get()
        guiargs.door_shuffle = parent.dungeonRandoWindow.dungeonWidgets["dungeondoorshuffle"].storageVar.get()
        guiargs.heartbeep = parent.gameOptionsWindow.gameOptionsWidgets["heartbeep"].storageVar.get()
        guiargs.heartcolor = parent.gameOptionsWindow.gameOptionsWidgets["heartcolor"].storageVar.get()
        guiargs.fastmenu = parent.gameOptionsWindow.gameOptionsWidgets["menuspeed"].storageVar.get()
        guiargs.create_spoiler = bool(parent.generationSetupWindow.generationWidgets["spoiler"].storageVar.get())
        guiargs.skip_playthrough = not bool(parent.generationSetupWindow.generationWidgets["spoiler"].storageVar.get())
        guiargs.suppress_rom = bool(parent.generationSetupWindow.generationWidgets["suppressrom"].storageVar.get())
        guiargs.openpyramid = bool(parent.entrandoWindow.entrandoWidgets["openpyramid"].storageVar.get())
        guiargs.mapshuffle = bool(parent.dungeonRandoWindow.dungeonWidgets["mapshuffle"].storageVar.get())
        guiargs.compassshuffle = bool(parent.dungeonRandoWindow.dungeonWidgets["compassshuffle"].storageVar.get())
        guiargs.keyshuffle = bool(parent.dungeonRandoWindow.dungeonWidgets["smallkeyshuffle"].storageVar.get())
        guiargs.bigkeyshuffle = bool(parent.dungeonRandoWindow.dungeonWidgets["bigkeyshuffle"].storageVar.get())
        guiargs.retro = bool(parent.itemWindow.itemWidgets["retro"].storageVar.get())
        guiargs.quickswap = bool(parent.gameOptionsWindow.gameOptionsWidgets["quickswap"].storageVar.get())
        guiargs.disablemusic = bool(parent.gameOptionsWindow.gameOptionsWidgets["nobgm"].storageVar.get())
        guiargs.ow_palettes = parent.gameOptionsWindow.gameOptionsWidgets["owpalettes"].storageVar.get()
        guiargs.uw_palettes = parent.gameOptionsWindow.gameOptionsWidgets["uwpalettes"].storageVar.get()
        guiargs.shuffleganon = bool(parent.entrandoWindow.entrandoWidgets["shuffleganon"].storageVar.get())
        guiargs.hints = bool(parent.gameOptionsWindow.gameOptionsWidgets["hints"].storageVar.get())
        guiargs.enemizercli = parent.enemizerWindow.enemizerCLIpathVar.get()
        guiargs.shufflebosses = parent.enemizerWindow.enemizerWidgets["bossshuffle"].storageVar.get()
        guiargs.shuffleenemies = parent.enemizerWindow.enemizerWidgets["enemyshuffle"].storageVar.get()
        guiargs.enemy_health = parent.enemizerWindow.enemizerWidgets["enemyhealth"].storageVar.get()
        guiargs.enemy_damage = parent.enemizerWindow.enemizerWidgets["enemydamage"].storageVar.get()
        guiargs.shufflepots = bool(parent.enemizerWindow.enemizerWidgets["potshuffle"].storageVar.get())
        guiargs.custom = bool(parent.generationSetupWindow.generationWidgets["usecustompool"].storageVar.get())
        guiargs.customitemarray = [int(parent.customContent.customWidgets["bow"].storageVar.get()), int(parent.customContent.customWidgets["silversupgrade"].storageVar.get()), int(parent.customContent.customWidgets["boomerang"].storageVar.get()), int(parent.customContent.customWidgets["redmerang"].storageVar.get()), int(parent.customContent.customWidgets["hookshot"].storageVar.get()), int(parent.customContent.customWidgets["mushroom"].storageVar.get()), int(parent.customContent.customWidgets["powder"].storageVar.get()), int(parent.customContent.customWidgets["firerod"].storageVar.get()),
                                   int(parent.customContent.customWidgets["icerod"].storageVar.get()), int(parent.customContent.customWidgets["bombos"].storageVar.get()), int(parent.customContent.customWidgets["ether"].storageVar.get()), int(parent.customContent.customWidgets["quake"].storageVar.get()), int(parent.customContent.customWidgets["lamp"].storageVar.get()), int(parent.customContent.customWidgets["hammer"].storageVar.get()), int(parent.customContent.customWidgets["shovel"].storageVar.get()), int(parent.customContent.customWidgets["flute"].storageVar.get()), int(parent.customContent.customWidgets["bugnet"].storageVar.get()),
                                   int(parent.customContent.customWidgets["book"].storageVar.get()), int(parent.customContent.customWidgets["bottle"].storageVar.get()), int(parent.customContent.customWidgets["somaria"].storageVar.get()), int(parent.customContent.customWidgets["byrna"].storageVar.get()), int(parent.customContent.customWidgets["cape"].storageVar.get()), int(parent.customContent.customWidgets["mirror"].storageVar.get()), int(parent.customContent.customWidgets["boots"].storageVar.get()), int(parent.customContent.customWidgets["powerglove"].storageVar.get()), int(parent.customContent.customWidgets["titansmitt"].storageVar.get()),
                                   int(parent.customContent.customWidgets["progressiveglove"].storageVar.get()), int(parent.customContent.customWidgets["flippers"].storageVar.get()), int(parent.customContent.customWidgets["pearl"].storageVar.get()), int(parent.customContent.customWidgets["heartpiece"].storageVar.get()), int(parent.customContent.customWidgets["heartcontainer"].storageVar.get()), int(parent.customContent.customWidgets["sancheart"].storageVar.get()), int(parent.customContent.customWidgets["sword1"].storageVar.get()), int(parent.customContent.customWidgets["sword2"].storageVar.get()),
                                   int(parent.customContent.customWidgets["sword3"].storageVar.get()), int(parent.customContent.customWidgets["sword4"].storageVar.get()), int(parent.customContent.customWidgets["progressivesword"].storageVar.get()), int(parent.customContent.customWidgets["shield1"].storageVar.get()), int(parent.customContent.customWidgets["shield2"].storageVar.get()), int(parent.customContent.customWidgets["shield3"].storageVar.get()), int(parent.customContent.customWidgets["progressiveshield"].storageVar.get()), int(parent.customContent.customWidgets["mail2"].storageVar.get()),
                                   int(parent.customContent.customWidgets["mail3"].storageVar.get()), int(parent.customContent.customWidgets["progressivemail"].storageVar.get()), int(parent.customContent.customWidgets["halfmagic"].storageVar.get()), int(parent.customContent.customWidgets["quartermagic"].storageVar.get()), int(parent.customContent.customWidgets["bombsplus5"].storageVar.get()), int(parent.customContent.customWidgets["bombsplus10"].storageVar.get()), int(parent.customContent.customWidgets["arrowsplus5"].storageVar.get()), int(parent.customContent.customWidgets["arrowsplus10"].storageVar.get()),
                                   int(parent.customContent.customWidgets["arrow1"].storageVar.get()), int(parent.customContent.customWidgets["arrow10"].storageVar.get()), int(parent.customContent.customWidgets["bomb1"].storageVar.get()), int(parent.customContent.customWidgets["bomb3"].storageVar.get()), int(parent.customContent.customWidgets["rupee1"].storageVar.get()), int(parent.customContent.customWidgets["rupee5"].storageVar.get()), int(parent.customContent.customWidgets["rupee20"].storageVar.get()), int(parent.customContent.customWidgets["rupee50"].storageVar.get()), int(parent.customContent.customWidgets["rupee100"].storageVar.get()),
                                   int(parent.customContent.customWidgets["rupee300"].storageVar.get()), int(parent.customContent.customWidgets["rupoor"].storageVar.get()), int(parent.customContent.customWidgets["blueclock"].storageVar.get()), int(parent.customContent.customWidgets["greenclock"].storageVar.get()), int(parent.customContent.customWidgets["redclock"].storageVar.get()), int(parent.customContent.customWidgets["progressivebow"].storageVar.get()), int(parent.customContent.customWidgets["bomb10"].storageVar.get()), int(parent.customContent.customWidgets["triforcepieces"].storageVar.get()),
                                   #int(parent.customContent.triforcecountVar.get()),
                                   int(parent.customContent.customWidgets["triforce"].storageVar.get()),  int(parent.customContent.customWidgets["rupoorcost"].storageVar.get()), int(parent.customContent.customWidgets["generickeys"].storageVar.get())]
        guiargs.rom = parent.generationSetupWindow.romVar.get()
#        guiargs.sprite = parent.gameOptionsWindow.sprite
        guiargs.outputpath = args.outputpath if args else None
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
            open_file(output_path(parent.working_dirs["outputpath"]))

    openOutputButton = Button(self, text='Open Output Directory', command=open_output)
    openOutputButton.pack(side=RIGHT)

    if os.path.exists(local_path('README.html')):
        def open_readme():
            open_file(local_path('README.html'))
        openReadmeButton = Button(self, text='Open Documentation', command=open_readme)
        openReadmeButton.pack()

    return self
