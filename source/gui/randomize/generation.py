from tkinter import ttk, filedialog, StringVar, Button, Entry, Frame, Label, E, W, LEFT, X
import source.gui.widgets as widgets
import json
import os
from source.classes.Empty import Empty

def generation_page(parent,settings):
    # Generation Setup
    self = ttk.Frame(parent)

    # Generation Setup options
    self.widgets = {}

    # Generation Setup option sections
    self.frames = {}
    self.frames["checkboxes"] = Frame(self)
    self.frames["checkboxes"].pack(anchor=W)

    # Load Generation Setup option widgets as defined by JSON file
    # Defns include frame name, widget type, widget options, widget placement attributes
    with open(os.path.join("resources","app","gui","randomize","generation","checkboxes.json")) as checkboxes:
        myDict = json.load(checkboxes)
        myDict = myDict["checkboxes"]
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, self.frames["checkboxes"])
        for key in dictWidgets:
            self.widgets[key] = dictWidgets[key]
            self.widgets[key].pack(anchor=W)

    self.frames["widgets"] = Frame(self)
    self.frames["widgets"].pack(anchor=W)
    # Load Generation Setup option widgets as defined by JSON file
    # Defns include frame name, widget type, widget options, widget placement attributes
    with open(os.path.join("resources","app","gui","randomize","generation","widgets.json")) as items:
        myDict = json.load(items)
        myDict = myDict["widgets"]
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, self.frames["widgets"])
        for key in dictWidgets:
            self.widgets[key] = dictWidgets[key]
            self.widgets[key].pack(anchor=W)

    self.frames["baserom"] = Frame(self)
    self.frames["baserom"].pack(anchor=W, fill=X)
    ## Locate base ROM
    # This one's more-complicated, build it and stuff it
    # widget ID
    widget = "rom"

    # Empty object
    self.widgets[widget] = Empty()
    # pieces
    self.widgets[widget].pieces = {}

    # frame
    self.widgets[widget].pieces["frame"] = Frame(self.frames["baserom"])
    # frame: label
    self.widgets[widget].pieces["frame"].label = Label(self.widgets[widget].pieces["frame"], text='Base Rom: ')
    # storage var
    self.widgets[widget].storageVar = StringVar()
    # textbox
    self.widgets[widget].pieces["textbox"] = Entry(self.widgets[widget].pieces["frame"], textvariable=self.widgets[widget].storageVar)
    self.widgets[widget].storageVar.set(settings["rom"])

    # FIXME: Translate these
    def RomSelect():
        rom = filedialog.askopenfilename(filetypes=[("Rom Files", (".sfc", ".smc")), ("All Files", "*")], initialdir=os.path.join("."))
        self.widgets[widget].storageVar.set(rom)
    # dialog button
    self.widgets[widget].pieces["button"] = Button(self.widgets[widget].pieces["frame"], text='Select Rom', command=RomSelect)

    # frame label: pack
    self.widgets[widget].pieces["frame"].label.pack(side=LEFT)
    # textbox: pack
    self.widgets[widget].pieces["textbox"].pack(side=LEFT, fill=X, expand=True)
    # button: pack
    self.widgets[widget].pieces["button"].pack(side=LEFT)
    # frame: pack
    self.widgets[widget].pieces["frame"].pack(fill=X)

    return self,settings
