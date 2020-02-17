from tkinter import ttk, IntVar, StringVar, Checkbutton, Frame, Label, OptionMenu, E, W, LEFT, RIGHT
import gui.widgets as widgets
import json
import os

def dungeon_page(parent):
    # Dungeon Shuffle
    self = ttk.Frame(parent)

    # Dungeon Shuffle options
    self.widgets = {}

    ## Dungeon Item Shuffle
    mcsbshuffleFrame = Frame(self)
    mcsbshuffleFrame.pack(anchor=W)
    mscbLabel = Label(mcsbshuffleFrame, text="Shuffle: ")
    mscbLabel.pack(side=LEFT)

    with open(os.path.join("resources","app","gui","randomize","dungeon","keysanity.json")) as keysanityItems:
        myDict = json.load(keysanityItems)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, mcsbshuffleFrame)
        for key in dictWidgets:
            self.widgets[key] = dictWidgets[key]
            self.widgets[key].pack(side=LEFT)

    with open(os.path.join("resources","app","gui","randomize","dungeon","widgets.json")) as dungeonWidgets:
        myDict = json.load(dungeonWidgets)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, self)
        for key in dictWidgets:
            self.widgets[key] = dictWidgets[key]
            self.widgets[key].pack(anchor=W)

    return self
