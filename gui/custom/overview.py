from tkinter import ttk, StringVar, Entry, Frame, Label, N, E, W, LEFT, RIGHT, X, VERTICAL, Y
import gui.widgets as widgets
import json
import os

def custom_page(top,parent):
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
    create_list_frame(self,"itemList1")
    create_vertical_rule(2)
    create_list_frame(self,"itemList2")
    create_vertical_rule(2)
    create_list_frame(self,"itemList3")
    create_vertical_rule(2)
    create_list_frame(self,"itemList4")
    create_vertical_rule(2)
    create_list_frame(self,"itemList5")

    with open(os.path.join("resources","app","gui","custom","overview","itemList1.json")) as items:
        myDict = json.load(items)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, self.frames["itemList1"])
        for key in dictWidgets:
            self.customWidgets[key] = dictWidgets[key]

    with open(os.path.join("resources","app","gui","custom","overview","itemList2.json")) as items:
        myDict = json.load(items)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, self.frames["itemList2"])
        for key in dictWidgets:
            self.customWidgets[key] = dictWidgets[key]

    with open(os.path.join("resources","app","gui","custom","overview","itemList3.json")) as items:
        myDict = json.load(items)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, self.frames["itemList3"])
        for key in dictWidgets:
            self.customWidgets[key] = dictWidgets[key]

    with open(os.path.join("resources","app","gui","custom","overview","itemList4.json")) as items:
        myDict = json.load(items)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, self.frames["itemList4"])
        for key in dictWidgets:
            self.customWidgets[key] = dictWidgets[key]

    with open(os.path.join("resources","app","gui","custom","overview","itemList5.json")) as items:
        myDict = json.load(items)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, self.frames["itemList5"])
        for key in dictWidgets:
            self.customWidgets[key] = dictWidgets[key]

    keys = list(self.customWidgets.keys())
    for i in range(0, len(keys)):
        self.customWidgets[keys[i]].storageVar.set(top.settings["customitemarray"][i])

    return self
