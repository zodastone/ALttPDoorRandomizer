from tkinter import ttk, StringVar, Entry, Frame, Label, N, E, W, LEFT, RIGHT, X
import gui.widgets as widgets
import json
import os

def custom_page(top,parent):
    # Custom Item Pool
    self = ttk.Frame(parent)

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
    self.frames["itemList1"] = Frame(self)
    self.frames["itemList1"].pack(side=LEFT, padx=(0,0), anchor=N)
    self.frames["itemList2"] = Frame(self)
    self.frames["itemList2"].pack(side=LEFT, padx=(0,0), anchor=N)
    self.frames["itemList3"] = Frame(self)
    self.frames["itemList3"].pack(side=LEFT, padx=(0,0), anchor=N)
    self.frames["itemList4"] = Frame(self)
    self.frames["itemList4"].pack(side=LEFT, padx=(0,0), anchor=N)
    self.frames["itemList5"] = Frame(self)
    self.frames["itemList5"].pack(side=LEFT, padx=(0,0), anchor=N)

    with open(os.path.join("resources","app","gui","custom","overview","itemList1.json")) as items:
        myDict = json.load(items)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, self.frames["itemList1"])
        for key in dictWidgets:
            self.customWidgets[key] = dictWidgets[key]
            self.customWidgets[key].pack()

    with open(os.path.join("resources","app","gui","custom","overview","itemList2.json")) as items:
        myDict = json.load(items)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, self.frames["itemList2"])
        for key in dictWidgets:
            self.customWidgets[key] = dictWidgets[key]
            self.customWidgets[key].pack()

    with open(os.path.join("resources","app","gui","custom","overview","itemList3.json")) as items:
        myDict = json.load(items)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, self.frames["itemList3"])
        for key in dictWidgets:
            self.customWidgets[key] = dictWidgets[key]
            self.customWidgets[key].pack()

    with open(os.path.join("resources","app","gui","custom","overview","itemList4.json")) as items:
        myDict = json.load(items)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, self.frames["itemList4"])
        for key in dictWidgets:
            self.customWidgets[key] = dictWidgets[key]
            self.customWidgets[key].pack()

    with open(os.path.join("resources","app","gui","custom","overview","itemList5.json")) as items:
        myDict = json.load(items)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, self.frames["itemList5"])
        for key in dictWidgets:
            self.customWidgets[key] = dictWidgets[key]
            self.customWidgets[key].pack()

    return self
