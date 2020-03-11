from tkinter import ttk, Frame, N, LEFT, VERTICAL, Y
import gui.widgets as widgets
import json
import os

import classes.constants as CONST


def custom_page(top, parent):
    # Custom Item Pool
    self = ttk.Frame(parent)

    def create_list_frame(parent, framename):
        parent.frames[framename] = Frame(parent)
        parent.frames[framename].pack(side=LEFT, padx=(0,0), anchor=N)
        parent.frames[framename].thisRow = 0
        parent.frames[framename].thisCol = 0

    def create_vertical_rule(num=1):
        for i in range(0,num):
            ttk.Separator(self, orient=VERTICAL).pack(side=LEFT, anchor=N, fill=Y)

    def validation(P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
    vcmd=(self.register(validation), '%P')

    # Custom Item Pool options
    self.customWidgets = {}

    # Custom Item Pool option sections
    self.frames = {}
    create_list_frame(self, "itemList1")
    create_vertical_rule(2)
    create_list_frame(self, "itemList2")
    create_vertical_rule(2)
    create_list_frame(self, "itemList3")
    create_vertical_rule(2)
    create_list_frame(self, "itemList4")
    create_vertical_rule(2)
    create_list_frame(self, "itemList5")

    with open(os.path.join("resources", "app", "gui", "custom", "overview", "widgets.json")) as widgetDefns:
        myDict = json.load(widgetDefns)
        for framename,theseWidgets in myDict.items():
            dictWidgets = widgets.make_widgets_from_dict(self, theseWidgets, self.frames[framename])
            for key in dictWidgets:
                self.customWidgets[key] = dictWidgets[key]

    for key in CONST.CUSTOMITEMS:
        self.customWidgets[key].storageVar.set(top.settings["customitemarray"][key])

    return self
