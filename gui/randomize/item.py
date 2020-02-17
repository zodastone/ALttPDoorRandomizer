from tkinter import ttk, IntVar, StringVar, Checkbutton, Frame, Label, OptionMenu, E, W, LEFT, RIGHT
import gui.widgets as widgets
import json
import os

def item_page(parent):
    # Item Randomizer
    self = ttk.Frame(parent)

    # Item Randomizer options
    self.widgets = {}

    with open(os.path.join("resources","app","gui","randomize","item","checkboxes.json")) as checkboxes:
        myDict = json.load(checkboxes)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, self)
        for key in dictWidgets:
            self.widgets[key] = dictWidgets[key]
            self.widgets[key].pack(anchor=W)

    leftItemFrame = Frame(self)
    rightItemFrame = Frame(self)
    leftItemFrame.pack(side=LEFT)
    rightItemFrame.pack(side=RIGHT)

    keys = [*map(str,range(0,7+1)),"Random"]
    vals = [*map(str,range(0,7+1)),"random"]
    crystalsOptions = {keys[i]: vals[i] for i in range(len(keys))}

    with open(os.path.join("resources","app","gui","randomize","item","leftItemFrame.json")) as leftItemFrameItems:
        myDict = json.load(leftItemFrameItems)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, leftItemFrame)
        for key in dictWidgets:
            self.widgets[key] = dictWidgets[key]
            self.widgets[key].pack(anchor=E)

    with open(os.path.join("resources","app","gui","randomize","item","rightItemFrame.json")) as rightItemFrameItems:
        myDict = json.load(rightItemFrameItems)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, rightItemFrame)
        for key in dictWidgets:
            self.widgets[key] = dictWidgets[key]
            self.widgets[key].pack(anchor=E)

    return self
