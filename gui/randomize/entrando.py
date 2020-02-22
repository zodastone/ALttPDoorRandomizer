from tkinter import ttk, IntVar, StringVar, Checkbutton, Frame, Label, OptionMenu, E, W, LEFT, RIGHT
import gui.widgets as widgets
import json
import os

def entrando_page(parent):
    # Entrance Randomizer
    self = ttk.Frame(parent)

    # Entrance Randomizer options
    self.widgets = {}

    # Entrance Randomizer option sections
    self.frames = {}
    self.frames["widgets"] = Frame(self)
    self.frames["widgets"].pack(anchor=W)

    with open(os.path.join("resources","app","gui","randomize","entrando","widgets.json")) as widgetDefns:
        myDict = json.load(widgetDefns)
        for framename,theseWidgets in myDict.items():
            dictWidgets = widgets.make_widgets_from_dict(self, theseWidgets, self.frames[framename])
            for key in dictWidgets:
                self.widgets[key] = dictWidgets[key]
                packAttrs = {"anchor":E}
                if self.widgets[key].type == "checkbox":
                    packAttrs["anchor"] = W
                self.widgets[key].pack(packAttrs)

    return self
