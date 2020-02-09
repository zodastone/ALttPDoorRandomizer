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

    topFrame3 = Frame(self.customWindow)

    def validation(P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
    vcmd=(topFrame3.register(validation), '%P')

    itemList1 = Frame(topFrame3)
    itemList2 = Frame(topFrame3)
    itemList3 = Frame(topFrame3)
    itemList4 = Frame(topFrame3)
    itemList5 = Frame(topFrame3)

    bowFrame = Frame(itemList1)
    bowLabel = Label(bowFrame, text='Bow')
    self.customWindow.bowVar = StringVar(value='0')
    bowEntry = Entry(bowFrame, textvariable=self.customWindow.bowVar, width=3, validate='all', vcmd=vcmd)
    bowFrame.pack()
    bowLabel.pack(anchor=W, side=LEFT, padx=(0,53))
    bowEntry.pack(anchor=E)

    progbowFrame = Frame(itemList1)
    progbowLabel = Label(progbowFrame, text='Prog.Bow')
    self.customWindow.progbowVar = StringVar(value='2')
    progbowEntry = Entry(progbowFrame, textvariable=self.customWindow.progbowVar, width=3, validate='all', vcmd=vcmd)
    progbowFrame.pack()
    progbowLabel.pack(anchor=W, side=LEFT, padx=(0,25))
    progbowEntry.pack(anchor=E)

    boomerangFrame = Frame(itemList1)
    boomerangLabel = Label(boomerangFrame, text='Boomerang')
    self.customWindow.boomerangVar = StringVar(value='1')
    boomerangEntry = Entry(boomerangFrame, textvariable=self.customWindow.boomerangVar, width=3, validate='all', vcmd=vcmd)
    boomerangFrame.pack()
    boomerangLabel.pack(anchor=W, side=LEFT, padx=(0,14))
    boomerangEntry.pack(anchor=E)

    magicboomerangFrame = Frame(itemList1)
    magicboomerangLabel = Label(magicboomerangFrame, text='M.Boomerang')
    self.customWindow.magicboomerangVar = StringVar(value='1')
    magicboomerangEntry = Entry(magicboomerangFrame, textvariable=self.customWindow.magicboomerangVar, width=3, validate='all', vcmd=vcmd)
    magicboomerangFrame.pack()
    magicboomerangLabel.pack(anchor=W, side=LEFT)
    magicboomerangEntry.pack(anchor=E)

    hookshotFrame = Frame(itemList1)
    hookshotLabel = Label(hookshotFrame, text='Hookshot')
    self.customWindow.hookshotVar = StringVar(value='1')
    hookshotEntry = Entry(hookshotFrame, textvariable=self.customWindow.hookshotVar, width=3, validate='all', vcmd=vcmd)
    hookshotFrame.pack()
    hookshotLabel.pack(anchor=W, side=LEFT, padx=(0,24))
    hookshotEntry.pack(anchor=E)

    mushroomFrame = Frame(itemList1)
    mushroomLabel = Label(mushroomFrame, text='Mushroom')
    self.customWindow.mushroomVar = StringVar(value='1')
    mushroomEntry = Entry(mushroomFrame, textvariable=self.customWindow.mushroomVar, width=3, validate='all', vcmd=vcmd)
    mushroomFrame.pack()
    mushroomLabel.pack(anchor=W, side=LEFT, padx=(0,17))
    mushroomEntry.pack(anchor=E)

    magicpowderFrame = Frame(itemList1)
    magicpowderLabel = Label(magicpowderFrame, text='Magic Powder')
    self.customWindow.magicpowderVar = StringVar(value='1')
    magicpowderEntry = Entry(magicpowderFrame, textvariable=self.customWindow.magicpowderVar, width=3, validate='all', vcmd=vcmd)
    magicpowderFrame.pack()
    magicpowderLabel.pack(anchor=W, side=LEFT)
    magicpowderEntry.pack(anchor=E)

    firerodFrame = Frame(itemList1)
    firerodLabel = Label(firerodFrame, text='Fire Rod')
    self.customWindow.firerodVar = StringVar(value='1')
    firerodEntry = Entry(firerodFrame, textvariable=self.customWindow.firerodVar, width=3, validate='all', vcmd=vcmd)
    firerodFrame.pack()
    firerodLabel.pack(anchor=W, side=LEFT, padx=(0,33))
    firerodEntry.pack(anchor=E)

    icerodFrame = Frame(itemList1)
    icerodLabel = Label(icerodFrame, text='Ice Rod')
    self.customWindow.icerodVar = StringVar(value='1')
    icerodEntry = Entry(icerodFrame, textvariable=self.customWindow.icerodVar, width=3, validate='all', vcmd=vcmd)
    icerodFrame.pack()
    icerodLabel.pack(anchor=W, side=LEFT, padx=(0,37))
    icerodEntry.pack(anchor=E)

    bombosFrame = Frame(itemList1)
    bombosLabel = Label(bombosFrame, text='Bombos')
    self.customWindow.bombosVar = StringVar(value='1')
    bombosEntry = Entry(bombosFrame, textvariable=self.customWindow.bombosVar, width=3, validate='all', vcmd=vcmd)
    bombosFrame.pack()
    bombosLabel.pack(anchor=W, side=LEFT, padx=(0,32))
    bombosEntry.pack(anchor=E)

    etherFrame = Frame(itemList1)
    etherLabel = Label(etherFrame, text='Ether')
    self.customWindow.etherVar = StringVar(value='1')
    etherEntry = Entry(etherFrame, textvariable=self.customWindow.etherVar, width=3, validate='all', vcmd=vcmd)
    etherFrame.pack()
    etherLabel.pack(anchor=W, side=LEFT, padx=(0,49))
    etherEntry.pack(anchor=E)

    quakeFrame = Frame(itemList1)
    quakeLabel = Label(quakeFrame, text='Quake')
    self.customWindow.quakeVar = StringVar(value='1')
    quakeEntry = Entry(quakeFrame, textvariable=self.customWindow.quakeVar, width=3, validate='all', vcmd=vcmd)
    quakeFrame.pack()
    quakeLabel.pack(anchor=W, side=LEFT, padx=(0,42))
    quakeEntry.pack(anchor=E)

    lampFrame = Frame(itemList1)
    lampLabel = Label(lampFrame, text='Lamp')
    self.customWindow.lampVar = StringVar(value='1')
    lampEntry = Entry(lampFrame, textvariable=self.customWindow.lampVar, width=3, validate='all', vcmd=vcmd)
    lampFrame.pack()
    lampLabel.pack(anchor=W, side=LEFT, padx=(0,46))
    lampEntry.pack(anchor=E)

    hammerFrame = Frame(itemList1)
    hammerLabel = Label(hammerFrame, text='Hammer')
    self.customWindow.hammerVar = StringVar(value='1')
    hammerEntry = Entry(hammerFrame, textvariable=self.customWindow.hammerVar, width=3, validate='all', vcmd=vcmd)
    hammerFrame.pack()
    hammerLabel.pack(anchor=W, side=LEFT, padx=(0,29))
    hammerEntry.pack(anchor=E)

    shovelFrame = Frame(itemList1)
    shovelLabel = Label(shovelFrame, text='Shovel')
    self.customWindow.shovelVar = StringVar(value='1')
    shovelEntry = Entry(shovelFrame, textvariable=self.customWindow.shovelVar, width=3, validate='all', vcmd=vcmd)
    shovelFrame.pack()
    shovelLabel.pack(anchor=W, side=LEFT, padx=(0,41))
    shovelEntry.pack(anchor=E)

    fluteFrame = Frame(itemList1)
    fluteLabel = Label(fluteFrame, text='Flute')
    self.customWindow.fluteVar = StringVar(value='1')
    fluteEntry = Entry(fluteFrame, textvariable=self.customWindow.fluteVar, width=3, validate='all', vcmd=vcmd)
    fluteFrame.pack()
    fluteLabel.pack(anchor=W, side=LEFT, padx=(0,50))
    fluteEntry.pack(anchor=E)

    bugnetFrame = Frame(itemList2)
    bugnetLabel = Label(bugnetFrame, text='Bug Net')
    self.customWindow.bugnetVar = StringVar(value='1')
    bugnetEntry = Entry(bugnetFrame, textvariable=self.customWindow.bugnetVar, width=3, validate='all', vcmd=vcmd)
    bugnetFrame.pack()
    bugnetLabel.pack(anchor=W, side=LEFT, padx=(0,41))
    bugnetEntry.pack(anchor=E)

    bookFrame = Frame(itemList2)
    bookLabel = Label(bookFrame, text='Book')
    self.customWindow.bookVar = StringVar(value='1')
    bookEntry = Entry(bookFrame, textvariable=self.customWindow.bookVar, width=3, validate='all', vcmd=vcmd)
    bookFrame.pack()
    bookLabel.pack(anchor=W, side=LEFT, padx=(0,57))
    bookEntry.pack(anchor=E)

    bottleFrame = Frame(itemList2)
    bottleLabel = Label(bottleFrame, text='Bottle')
    self.customWindow.bottleVar = StringVar(value='4')
    bottleEntry = Entry(bottleFrame, textvariable=self.customWindow.bottleVar, width=3, validate='all', vcmd=vcmd)
    bottleFrame.pack()
    bottleLabel.pack(anchor=W, side=LEFT, padx=(0,53))
    bottleEntry.pack(anchor=E)

    somariaFrame = Frame(itemList2)
    somariaLabel = Label(somariaFrame, text='C.Somaria')
    self.customWindow.somariaVar = StringVar(value='1')
    somariaEntry = Entry(somariaFrame, textvariable=self.customWindow.somariaVar, width=3, validate='all', vcmd=vcmd)
    somariaFrame.pack()
    somariaLabel.pack(anchor=W, side=LEFT, padx=(0,30))
    somariaEntry.pack(anchor=E)

    byrnaFrame = Frame(itemList2)
    byrnaLabel = Label(byrnaFrame, text='C.Byrna')
    self.customWindow.byrnaVar = StringVar(value='1')
    byrnaEntry = Entry(byrnaFrame, textvariable=self.customWindow.byrnaVar, width=3, validate='all', vcmd=vcmd)
    byrnaFrame.pack()
    byrnaLabel.pack(anchor=W, side=LEFT, padx=(0,43))
    byrnaEntry.pack(anchor=E)

    capeFrame = Frame(itemList2)
    capeLabel = Label(capeFrame, text='Magic Cape')
    self.customWindow.capeVar = StringVar(value='1')
    capeEntry = Entry(capeFrame, textvariable=self.customWindow.capeVar, width=3, validate='all', vcmd=vcmd)
    capeFrame.pack()
    capeLabel.pack(anchor=W, side=LEFT, padx=(0,21))
    capeEntry.pack(anchor=E)

    mirrorFrame = Frame(itemList2)
    mirrorLabel = Label(mirrorFrame, text='Magic Mirror')
    self.customWindow.mirrorVar = StringVar(value='1')
    mirrorEntry = Entry(mirrorFrame, textvariable=self.customWindow.mirrorVar, width=3, validate='all', vcmd=vcmd)
    mirrorFrame.pack()
    mirrorLabel.pack(anchor=W, side=LEFT, padx=(0,15))
    mirrorEntry.pack(anchor=E)

    bootsFrame = Frame(itemList2)
    bootsLabel = Label(bootsFrame, text='Pegasus Boots')
    self.customWindow.bootsVar = StringVar(value='1')
    bootsEntry = Entry(bootsFrame, textvariable=self.customWindow.bootsVar, width=3, validate='all', vcmd=vcmd)
    bootsFrame.pack()
    bootsLabel.pack(anchor=W, side=LEFT, padx=(0,8))
    bootsEntry.pack(anchor=E)

    powergloveFrame = Frame(itemList2)
    powergloveLabel = Label(powergloveFrame, text='Power Glove')
    self.customWindow.powergloveVar = StringVar(value='0')
    powergloveEntry = Entry(powergloveFrame, textvariable=self.customWindow.powergloveVar, width=3, validate='all', vcmd=vcmd)
    powergloveFrame.pack()
    powergloveLabel.pack(anchor=W, side=LEFT, padx=(0,18))
    powergloveEntry.pack(anchor=E)

    titansmittFrame = Frame(itemList2)
    titansmittLabel = Label(titansmittFrame, text='Titan\'s Mitt')
    self.customWindow.titansmittVar = StringVar(value='0')
    titansmittEntry = Entry(titansmittFrame, textvariable=self.customWindow.titansmittVar, width=3, validate='all', vcmd=vcmd)
    titansmittFrame.pack()
    titansmittLabel.pack(anchor=W, side=LEFT, padx=(0,24))
    titansmittEntry.pack(anchor=E)

    proggloveFrame = Frame(itemList2)
    proggloveLabel = Label(proggloveFrame, text='Prog.Glove')
    self.customWindow.proggloveVar = StringVar(value='2')
    proggloveEntry = Entry(proggloveFrame, textvariable=self.customWindow.proggloveVar, width=3, validate='all', vcmd=vcmd)
    proggloveFrame.pack()
    proggloveLabel.pack(anchor=W, side=LEFT, padx=(0,26))
    proggloveEntry.pack(anchor=E)

    flippersFrame = Frame(itemList2)
    flippersLabel = Label(flippersFrame, text='Flippers')
    self.customWindow.flippersVar = StringVar(value='1')
    flippersEntry = Entry(flippersFrame, textvariable=self.customWindow.flippersVar, width=3, validate='all', vcmd=vcmd)
    flippersFrame.pack()
    flippersLabel.pack(anchor=W, side=LEFT, padx=(0,43))
    flippersEntry.pack(anchor=E)

    pearlFrame = Frame(itemList2)
    pearlLabel = Label(pearlFrame, text='Moon Pearl')
    self.customWindow.pearlVar = StringVar(value='1')
    pearlEntry = Entry(pearlFrame, textvariable=self.customWindow.pearlVar, width=3, validate='all', vcmd=vcmd)
    pearlFrame.pack()
    pearlLabel.pack(anchor=W, side=LEFT, padx=(0,23))
    pearlEntry.pack(anchor=E)

    heartpieceFrame = Frame(itemList2)
    heartpieceLabel = Label(heartpieceFrame, text='Piece of Heart')
    self.customWindow.heartpieceVar = StringVar(value='24')
    heartpieceEntry = Entry(heartpieceFrame, textvariable=self.customWindow.heartpieceVar, width=3, validate='all', vcmd=vcmd)
    heartpieceFrame.pack()
    heartpieceLabel.pack(anchor=W, side=LEFT, padx=(0,10))
    heartpieceEntry.pack(anchor=E)

    fullheartFrame = Frame(itemList2)
    fullheartLabel = Label(fullheartFrame, text='Heart Container')
    self.customWindow.fullheartVar = StringVar(value='10')
    fullheartEntry = Entry(fullheartFrame, textvariable=self.customWindow.fullheartVar, width=3, validate='all', vcmd=vcmd)
    fullheartFrame.pack()
    fullheartLabel.pack(anchor=W, side=LEFT)
    fullheartEntry.pack(anchor=E)

    sancheartFrame = Frame(itemList2)
    sancheartLabel = Label(sancheartFrame, text='Sanctuary Heart')
    self.customWindow.sancheartVar = StringVar(value='1')
    sancheartEntry = Entry(sancheartFrame, textvariable=self.customWindow.sancheartVar, width=3, validate='all', vcmd=vcmd)
    sancheartFrame.pack()
    sancheartLabel.pack(anchor=W, side=LEFT)
    sancheartEntry.pack(anchor=E)

    sword1Frame = Frame(itemList3)
    sword1Label = Label(sword1Frame, text='Sword 1')
    self.customWindow.sword1Var = StringVar(value='0')
    sword1Entry = Entry(sword1Frame, textvariable=self.customWindow.sword1Var, width=3, validate='all', vcmd=vcmd)
    sword1Frame.pack()
    sword1Label.pack(anchor=W, side=LEFT, padx=(0,34))
    sword1Entry.pack(anchor=E)

    sword2Frame = Frame(itemList3)
    sword2Label = Label(sword2Frame, text='Sword 2')
    self.customWindow.sword2Var = StringVar(value='0')
    sword2Entry = Entry(sword2Frame, textvariable=self.customWindow.sword2Var, width=3, validate='all', vcmd=vcmd)
    sword2Frame.pack()
    sword2Label.pack(anchor=W, side=LEFT, padx=(0,34))
    sword2Entry.pack(anchor=E)

    sword3Frame = Frame(itemList3)
    sword3Label = Label(sword3Frame, text='Sword 3')
    self.customWindow.sword3Var = StringVar(value='0')
    sword3Entry = Entry(sword3Frame, textvariable=self.customWindow.sword3Var, width=3, validate='all', vcmd=vcmd)
    sword3Frame.pack()
    sword3Label.pack(anchor=W, side=LEFT, padx=(0,34))
    sword3Entry.pack(anchor=E)

    sword4Frame = Frame(itemList3)
    sword4Label = Label(sword4Frame, text='Sword 4')
    self.customWindow.sword4Var = StringVar(value='0')
    sword4Entry = Entry(sword4Frame, textvariable=self.customWindow.sword4Var, width=3, validate='all', vcmd=vcmd)
    sword4Frame.pack()
    sword4Label.pack(anchor=W, side=LEFT, padx=(0,34))
    sword4Entry.pack(anchor=E)

    progswordFrame = Frame(itemList3)
    progswordLabel = Label(progswordFrame, text='Prog.Sword')
    self.customWindow.progswordVar = StringVar(value='4')
    progswordEntry = Entry(progswordFrame, textvariable=self.customWindow.progswordVar, width=3, validate='all', vcmd=vcmd)
    progswordFrame.pack()
    progswordLabel.pack(anchor=W, side=LEFT, padx=(0,15))
    progswordEntry.pack(anchor=E)

    shield1Frame = Frame(itemList3)
    shield1Label = Label(shield1Frame, text='Shield 1')
    self.customWindow.shield1Var = StringVar(value='0')
    shield1Entry = Entry(shield1Frame, textvariable=self.customWindow.shield1Var, width=3, validate='all', vcmd=vcmd)
    shield1Frame.pack()
    shield1Label.pack(anchor=W, side=LEFT, padx=(0,35))
    shield1Entry.pack(anchor=E)

    shield2Frame = Frame(itemList3)
    shield2Label = Label(shield2Frame, text='Shield 2')
    self.customWindow.shield2Var = StringVar(value='0')
    shield2Entry = Entry(shield2Frame, textvariable=self.customWindow.shield2Var, width=3, validate='all', vcmd=vcmd)
    shield2Frame.pack()
    shield2Label.pack(anchor=W, side=LEFT, padx=(0,35))
    shield2Entry.pack(anchor=E)

    shield3Frame = Frame(itemList3)
    shield3Label = Label(shield3Frame, text='Shield 3')
    self.customWindow.shield3Var = StringVar(value='0')
    shield3Entry = Entry(shield3Frame, textvariable=self.customWindow.shield3Var, width=3, validate='all', vcmd=vcmd)
    shield3Frame.pack()
    shield3Label.pack(anchor=W, side=LEFT, padx=(0,35))
    shield3Entry.pack(anchor=E)

    progshieldFrame = Frame(itemList3)
    progshieldLabel = Label(progshieldFrame, text='Prog.Shield')
    self.customWindow.progshieldVar = StringVar(value='3')
    progshieldEntry = Entry(progshieldFrame, textvariable=self.customWindow.progshieldVar, width=3, validate='all', vcmd=vcmd)
    progshieldFrame.pack()
    progshieldLabel.pack(anchor=W, side=LEFT, padx=(0,16))
    progshieldEntry.pack(anchor=E)

    bluemailFrame = Frame(itemList3)
    bluemailLabel = Label(bluemailFrame, text='Blue Mail')
    self.customWindow.bluemailVar = StringVar(value='0')
    bluemailEntry = Entry(bluemailFrame, textvariable=self.customWindow.bluemailVar, width=3, validate='all', vcmd=vcmd)
    bluemailFrame.pack()
    bluemailLabel.pack(anchor=W, side=LEFT, padx=(0,27))
    bluemailEntry.pack(anchor=E)

    redmailFrame = Frame(itemList3)
    redmailLabel = Label(redmailFrame, text='Red Mail')
    self.customWindow.redmailVar = StringVar(value='0')
    redmailEntry = Entry(redmailFrame, textvariable=self.customWindow.redmailVar, width=3, validate='all', vcmd=vcmd)
    redmailFrame.pack()
    redmailLabel.pack(anchor=W, side=LEFT, padx=(0,30))
    redmailEntry.pack(anchor=E)

    progmailFrame = Frame(itemList3)
    progmailLabel = Label(progmailFrame, text='Prog.Mail')
    self.customWindow.progmailVar = StringVar(value='2')
    progmailEntry = Entry(progmailFrame, textvariable=self.customWindow.progmailVar, width=3, validate='all', vcmd=vcmd)
    progmailFrame.pack()
    progmailLabel.pack(anchor=W, side=LEFT, padx=(0,25))
    progmailEntry.pack(anchor=E)

    halfmagicFrame = Frame(itemList3)
    halfmagicLabel = Label(halfmagicFrame, text='Half Magic')
    self.customWindow.halfmagicVar = StringVar(value='1')
    halfmagicEntry = Entry(halfmagicFrame, textvariable=self.customWindow.halfmagicVar, width=3, validate='all', vcmd=vcmd)
    halfmagicFrame.pack()
    halfmagicLabel.pack(anchor=W, side=LEFT, padx=(0,18))
    halfmagicEntry.pack(anchor=E)

    quartermagicFrame = Frame(itemList3)
    quartermagicLabel = Label(quartermagicFrame, text='Quarter Magic')
    self.customWindow.quartermagicVar = StringVar(value='0')
    quartermagicEntry = Entry(quartermagicFrame, textvariable=self.customWindow.quartermagicVar, width=3, validate='all', vcmd=vcmd)
    quartermagicFrame.pack()
    quartermagicLabel.pack(anchor=W, side=LEFT)
    quartermagicEntry.pack(anchor=E)

    bcap5Frame = Frame(itemList3)
    bcap5Label = Label(bcap5Frame, text='Bomb C.+5')
    self.customWindow.bcap5Var = StringVar(value='0')
    bcap5Entry = Entry(bcap5Frame, textvariable=self.customWindow.bcap5Var, width=3, validate='all', vcmd=vcmd)
    bcap5Frame.pack()
    bcap5Label.pack(anchor=W, side=LEFT, padx=(0,16))
    bcap5Entry.pack(anchor=E)

    bcap10Frame = Frame(itemList3)
    bcap10Label = Label(bcap10Frame, text='Bomb C.+10')
    self.customWindow.bcap10Var = StringVar(value='0')
    bcap10Entry = Entry(bcap10Frame, textvariable=self.customWindow.bcap10Var, width=3, validate='all', vcmd=vcmd)
    bcap10Frame.pack()
    bcap10Label.pack(anchor=W, side=LEFT, padx=(0,10))
    bcap10Entry.pack(anchor=E)

    acap5Frame = Frame(itemList4)
    acap5Label = Label(acap5Frame, text='Arrow C.+5')
    self.customWindow.acap5Var = StringVar(value='0')
    acap5Entry = Entry(acap5Frame, textvariable=self.customWindow.acap5Var, width=3, validate='all', vcmd=vcmd)
    acap5Frame.pack()
    acap5Label.pack(anchor=W, side=LEFT, padx=(0,7))
    acap5Entry.pack(anchor=E)

    acap10Frame = Frame(itemList4)
    acap10Label = Label(acap10Frame, text='Arrow C.+10')
    self.customWindow.acap10Var = StringVar(value='0')
    acap10Entry = Entry(acap10Frame, textvariable=self.customWindow.acap10Var, width=3, validate='all', vcmd=vcmd)
    acap10Frame.pack()
    acap10Label.pack(anchor=W, side=LEFT, padx=(0,1))
    acap10Entry.pack(anchor=E)

    arrow1Frame = Frame(itemList4)
    arrow1Label = Label(arrow1Frame, text='Arrow (1)')
    self.customWindow.arrow1Var = StringVar(value='1')
    arrow1Entry = Entry(arrow1Frame, textvariable=self.customWindow.arrow1Var, width=3, validate='all', vcmd=vcmd)
    arrow1Frame.pack()
    arrow1Label.pack(anchor=W, side=LEFT, padx=(0,18))
    arrow1Entry.pack(anchor=E)

    arrow10Frame = Frame(itemList4)
    arrow10Label = Label(arrow10Frame, text='Arrows (10)')
    self.customWindow.arrow10Var = StringVar(value='12')
    arrow10Entry = Entry(arrow10Frame, textvariable=self.customWindow.arrow10Var, width=3, validate='all', vcmd=vcmd)
    arrow10Frame.pack()
    arrow10Label.pack(anchor=W, side=LEFT, padx=(0,7))
    arrow10Entry.pack(anchor=E)

    bomb1Frame = Frame(itemList4)
    bomb1Label = Label(bomb1Frame, text='Bomb (1)')
    self.customWindow.bomb1Var = StringVar(value='0')
    bomb1Entry = Entry(bomb1Frame, textvariable=self.customWindow.bomb1Var, width=3, validate='all', vcmd=vcmd)
    bomb1Frame.pack()
    bomb1Label.pack(anchor=W, side=LEFT, padx=(0,18))
    bomb1Entry.pack(anchor=E)

    bomb3Frame = Frame(itemList4)
    bomb3Label = Label(bomb3Frame, text='Bombs (3)')
    self.customWindow.bomb3Var = StringVar(value='16')
    bomb3Entry = Entry(bomb3Frame, textvariable=self.customWindow.bomb3Var, width=3, validate='all', vcmd=vcmd)
    bomb3Frame.pack()
    bomb3Label.pack(anchor=W, side=LEFT, padx=(0,13))
    bomb3Entry.pack(anchor=E)

    bomb10Frame = Frame(itemList4)
    bomb10Label = Label(bomb10Frame, text='Bombs (10)')
    self.customWindow.bomb10Var = StringVar(value='1')
    bomb10Entry = Entry(bomb10Frame, textvariable=self.customWindow.bomb10Var, width=3, validate='all', vcmd=vcmd)
    bomb10Frame.pack()
    bomb10Label.pack(anchor=W, side=LEFT, padx=(0,7))
    bomb10Entry.pack(anchor=E)

    rupee1Frame = Frame(itemList4)
    rupee1Label = Label(rupee1Frame, text='Rupee (1)')
    self.customWindow.rupee1Var = StringVar(value='2')
    rupee1Entry = Entry(rupee1Frame, textvariable=self.customWindow.rupee1Var, width=3, validate='all', vcmd=vcmd)
    rupee1Frame.pack()
    rupee1Label.pack(anchor=W, side=LEFT, padx=(0,17))
    rupee1Entry.pack(anchor=E)

    rupee5Frame = Frame(itemList4)
    rupee5Label = Label(rupee5Frame, text='Rupees (5)')
    self.customWindow.rupee5Var = StringVar(value='4')
    rupee5Entry = Entry(rupee5Frame, textvariable=self.customWindow.rupee5Var, width=3, validate='all', vcmd=vcmd)
    rupee5Frame.pack()
    rupee5Label.pack(anchor=W, side=LEFT, padx=(0,12))
    rupee5Entry.pack(anchor=E)

    rupee20Frame = Frame(itemList4)
    rupee20Label = Label(rupee20Frame, text='Rupees (20)')
    self.customWindow.rupee20Var = StringVar(value='28')
    rupee20Entry = Entry(rupee20Frame, textvariable=self.customWindow.rupee20Var, width=3, validate='all', vcmd=vcmd)
    rupee20Frame.pack()
    rupee20Label.pack(anchor=W, side=LEFT, padx=(0,6))
    rupee20Entry.pack(anchor=E)

    rupee50Frame = Frame(itemList4)
    rupee50Label = Label(rupee50Frame, text='Rupees (50)')
    self.customWindow.rupee50Var = StringVar(value='7')
    rupee50Entry = Entry(rupee50Frame, textvariable=self.customWindow.rupee50Var, width=3, validate='all', vcmd=vcmd)
    rupee50Frame.pack()
    rupee50Label.pack(anchor=W, side=LEFT, padx=(0,6))
    rupee50Entry.pack(anchor=E)

    rupee100Frame = Frame(itemList4)
    rupee100Label = Label(rupee100Frame, text='Rupees (100)')
    self.customWindow.rupee100Var = StringVar(value='1')
    rupee100Entry = Entry(rupee100Frame, textvariable=self.customWindow.rupee100Var, width=3, validate='all', vcmd=vcmd)
    rupee100Frame.pack()
    rupee100Label.pack(anchor=W, side=LEFT, padx=(0,0))
    rupee100Entry.pack(anchor=E)

    rupee300Frame = Frame(itemList4)
    rupee300Label = Label(rupee300Frame, text='Rupees (300)')
    self.customWindow.rupee300Var = StringVar(value='5')
    rupee300Entry = Entry(rupee300Frame, textvariable=self.customWindow.rupee300Var, width=3, validate='all', vcmd=vcmd)
    rupee300Frame.pack()
    rupee300Label.pack(anchor=W, side=LEFT, padx=(0,0))
    rupee300Entry.pack(anchor=E)

    blueclockFrame = Frame(itemList4)
    blueclockLabel = Label(blueclockFrame, text='Blue Clock')
    self.customWindow.blueclockVar = StringVar(value='0')
    blueclockEntry = Entry(blueclockFrame, textvariable=self.customWindow.blueclockVar, width=3, validate='all', vcmd=vcmd)
    blueclockFrame.pack()
    blueclockLabel.pack(anchor=W, side=LEFT, padx=(0,11))
    blueclockEntry.pack(anchor=E)

    greenclockFrame = Frame(itemList4)
    greenclockLabel = Label(greenclockFrame, text='Green Clock')
    self.customWindow.greenclockVar = StringVar(value='0')
    greenclockEntry = Entry(greenclockFrame, textvariable=self.customWindow.greenclockVar, width=3, validate='all', vcmd=vcmd)
    greenclockFrame.pack()
    greenclockLabel.pack(anchor=W, side=LEFT, padx=(0,3))
    greenclockEntry.pack(anchor=E)

    redclockFrame = Frame(itemList4)
    redclockLabel = Label(redclockFrame, text='Red Clock')
    self.customWindow.redclockVar = StringVar(value='0')
    redclockEntry = Entry(redclockFrame, textvariable=self.customWindow.redclockVar, width=3, validate='all', vcmd=vcmd)
    redclockFrame.pack()
    redclockLabel.pack(anchor=W, side=LEFT, padx=(0,14))
    redclockEntry.pack(anchor=E)

    silverarrowFrame = Frame(itemList5)
    silverarrowLabel = Label(silverarrowFrame, text='Silver Arrow')
    self.customWindow.silverarrowVar = StringVar(value='0')
    silverarrowEntry = Entry(silverarrowFrame, textvariable=self.customWindow.silverarrowVar, width=3, validate='all', vcmd=vcmd)
    silverarrowFrame.pack()
    silverarrowLabel.pack(anchor=W, side=LEFT, padx=(0,64))
    silverarrowEntry.pack(anchor=E)

    universalkeyFrame = Frame(itemList5)
    universalkeyLabel = Label(universalkeyFrame, text='Universal Key')
    self.customWindow.universalkeyVar = StringVar(value='0')
    universalkeyEntry = Entry(universalkeyFrame, textvariable=self.customWindow.universalkeyVar, width=3, validate='all', vcmd=vcmd)
    universalkeyFrame.pack()
    universalkeyLabel.pack(anchor=W, side=LEFT, padx=(0,57))
    universalkeyEntry.pack(anchor=E)

    triforcepieceFrame = Frame(itemList5)
    triforcepieceLabel = Label(triforcepieceFrame, text='Triforce Piece')
    self.customWindow.triforcepieceVar = StringVar(value='0')
    triforcepieceEntry = Entry(triforcepieceFrame, textvariable=self.customWindow.triforcepieceVar, width=3, validate='all', vcmd=vcmd)
    triforcepieceFrame.pack()
    triforcepieceLabel.pack(anchor=W, side=LEFT, padx=(0,55))
    triforcepieceEntry.pack(anchor=E)

    triforcecountFrame = Frame(itemList5)
    triforcecountLabel = Label(triforcecountFrame, text='Triforce Pieces Required')
    self.customWindow.triforcecountVar = StringVar(value='0')
    triforcecountEntry = Entry(triforcecountFrame, textvariable=self.customWindow.triforcecountVar, width=3, validate='all', vcmd=vcmd)
    triforcecountFrame.pack()
    triforcecountLabel.pack(anchor=W, side=LEFT, padx=(0,0))
    triforcecountEntry.pack(anchor=E)

    triforceFrame = Frame(itemList5)
    triforceLabel = Label(triforceFrame, text='Triforce (win game)')
    self.customWindow.triforceVar = StringVar(value='0')
    triforceEntry = Entry(triforceFrame, textvariable=self.customWindow.triforceVar, width=3, validate='all', vcmd=vcmd)
    triforceFrame.pack()
    triforceLabel.pack(anchor=W, side=LEFT, padx=(0,23))
    triforceEntry.pack(anchor=E)

    rupoorFrame = Frame(itemList5)
    rupoorLabel = Label(rupoorFrame, text='Rupoor')
    self.customWindow.rupoorVar = StringVar(value='0')
    rupoorEntry = Entry(rupoorFrame, textvariable=self.customWindow.rupoorVar, width=3, validate='all', vcmd=vcmd)
    rupoorFrame.pack()
    rupoorLabel.pack(anchor=W, side=LEFT, padx=(0,87))
    rupoorEntry.pack(anchor=E)

    rupoorcostFrame = Frame(itemList5)
    rupoorcostLabel = Label(rupoorcostFrame, text='Rupoor Cost')
    self.customWindow.rupoorcostVar = StringVar(value='10')
    rupoorcostEntry = Entry(rupoorcostFrame, textvariable=self.customWindow.rupoorcostVar, width=6, validate='all', vcmd=vcmd)
    rupoorcostFrame.pack()
    rupoorcostLabel.pack(anchor=W, side=LEFT, padx=(0,43))
    rupoorcostEntry.pack(anchor=E)

    itemList1.pack(side=LEFT, padx=(0,0))
    itemList2.pack(side=LEFT, padx=(0,0))
    itemList3.pack(side=LEFT, padx=(0,0))
    itemList4.pack(side=LEFT, padx=(0,0))
    itemList5.pack(side=LEFT, padx=(0,0))
    topFrame3.pack(side=TOP, pady=(17,0))

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
