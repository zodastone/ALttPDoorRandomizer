from tkinter import ttk, IntVar, StringVar, Checkbutton, Frame, Label, OptionMenu, E, W, LEFT, RIGHT
import gui.widgets as widgets
import json
import os
 
def item_page(parent):
    # Item Randomizer
    self = ttk.Frame(parent)

    # Item Randomizer options
    self.widgets = {}

    # Item Randomizer option sections
    self.frames = {}

    self.frames["checkboxes"] = Frame(self)
    self.frames["checkboxes"].pack(anchor=W)
    with open(os.path.join("resources","app","gui","randomize","item","checkboxes.json")) as checkboxes:
        myDict = json.load(checkboxes)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, self.frames["checkboxes"])
        for key in dictWidgets:
            self.widgets[key] = dictWidgets[key]
            self.widgets[key].pack(anchor=W)

    self.frames["leftItemFrame"] = Frame(self)
    self.frames["rightItemFrame"] = Frame(self)
    self.frames["leftItemFrame"].pack(side=LEFT)
    self.frames["rightItemFrame"].pack(side=RIGHT)

    with open(os.path.join("resources","app","gui","randomize","item","leftItemFrame.json")) as leftItemFrameItems:
        myDict = json.load(leftItemFrameItems)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, self.frames["leftItemFrame"])
        for key in dictWidgets:
            self.widgets[key] = dictWidgets[key]
            self.widgets[key].pack(anchor=E)

    with open(os.path.join("resources","app","gui","randomize","item","rightItemFrame.json")) as rightItemFrameItems:
        myDict = json.load(rightItemFrameItems)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, self.frames["rightItemFrame"])
        for key in dictWidgets:
            self.widgets[key] = dictWidgets[key]
            self.widgets[key].pack(anchor=E)

    return self
