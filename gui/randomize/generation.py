import os
from tkinter import ttk, filedialog, IntVar, StringVar, Button, Checkbutton, Entry, Frame, Label, E, W, LEFT, RIGHT, X
import gui.widgets as widgets
import json
import os

def generation_page(parent,settings):
    # Generation Setup
    self = ttk.Frame(parent)

    # Generation Setup options
    self.widgets = {}

    # Generation Setup option sections
    self.frames = {}
    self.frames["checkboxes"] = Frame(self)
    self.frames["checkboxes"].pack(anchor=W)

    with open(os.path.join("resources","app","gui","randomize","generation","checkboxes.json")) as checkboxes:
        myDict = json.load(checkboxes)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, self.frames["checkboxes"])
        for key in dictWidgets:
            self.widgets[key] = dictWidgets[key]
            self.widgets[key].pack(anchor=W)

    self.frames["baserom"] = Frame(self)
    self.frames["baserom"].pack(anchor=W, fill=X)
    ## Locate base ROM
    baseRomFrame = Frame(self.frames["baserom"])
    baseRomLabel = Label(baseRomFrame, text='Base Rom: ')
    self.romVar = StringVar()
    romEntry = Entry(baseRomFrame, textvariable=self.romVar)
    self.romVar.set(settings["rom"])

    def RomSelect():
        rom = filedialog.askopenfilename(filetypes=[("Rom Files", (".sfc", ".smc")), ("All Files", "*")], initialdir=os.path.join("."))
        self.romVar.set(rom)
    romSelectButton = Button(baseRomFrame, text='Select Rom', command=RomSelect)

    baseRomLabel.pack(side=LEFT)
    romEntry.pack(side=LEFT, fill=X, expand=True)
    romSelectButton.pack(side=LEFT)
    baseRomFrame.pack(fill=X)

    return self,settings
