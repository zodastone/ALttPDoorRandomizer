from tkinter import ttk, StringVar, Entry, Frame, Label, N, E, W, LEFT, RIGHT, X, VERTICAL, Y
import gui.widgets as widgets
import json
import os

import classes.constants as CONST

def startinventory_page(top,parent):
    # Starting Inventory
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

    # Starting Inventory options
    self.startingWidgets = {}

    # Starting Inventory option sections
    self.frames = {}
    create_list_frame(self,"itemList1")
    create_vertical_rule(2)
    create_list_frame(self,"itemList2")
    create_vertical_rule(2)
    create_list_frame(self,"itemList3")
    create_vertical_rule(2)
    create_list_frame(self,"itemList4")
    create_vertical_rule(2)
    create_list_frame(self,"itemList5")

    with open(os.path.join("resources","app","gui","custom","overview","widgets.json")) as widgetDefns:
        myDict = json.load(widgetDefns)
        for key in CONST.CANTSTARTWITH:
            for num in range(1, 5 + 1):
                thisList = "itemList" + str(num)
                if key in myDict[thisList]:
                    del myDict[thisList][key]
        for framename,theseWidgets in myDict.items():
            dictWidgets = widgets.make_widgets_from_dict(self, theseWidgets, self.frames[framename])
            for key in dictWidgets:
                self.startingWidgets[key] = dictWidgets[key]

    for key in CONST.CUSTOMITEMS:
        if key not in CONST.CANTSTARTWITH:
            val = 0
            if key in top.settings["startinventoryarray"]:
                val = top.settings["startinventoryarray"][key]
            self.startingWidgets[key].storageVar.set(val)

    return self
