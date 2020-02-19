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

    itemList1 = Frame(self)
    itemList2 = Frame(self)
    itemList3 = Frame(self)
    itemList4 = Frame(self)
    itemList5 = Frame(self)

    currentList = itemList1
    with open(os.path.join("resources","app","gui","custom","overview","itemList1.json")) as items:
        myDict = json.load(items)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, currentList)
        for key in dictWidgets:
            self.customWidgets[key] = dictWidgets[key]
            self.customWidgets[key].pack()

    currentList = itemList2
    with open(os.path.join("resources","app","gui","custom","overview","itemList2.json")) as items:
        myDict = json.load(items)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, currentList)
        for key in dictWidgets:
            self.customWidgets[key] = dictWidgets[key]
            self.customWidgets[key].pack()

    currentList = itemList3
    with open(os.path.join("resources","app","gui","custom","overview","itemList3.json")) as items:
        myDict = json.load(items)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, currentList)
        for key in dictWidgets:
            self.customWidgets[key] = dictWidgets[key]
            self.customWidgets[key].pack()

    currentList = itemList4
    with open(os.path.join("resources","app","gui","custom","overview","itemList4.json")) as items:
        myDict = json.load(items)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, currentList)
        for key in dictWidgets:
            self.customWidgets[key] = dictWidgets[key]
            self.customWidgets[key].pack()

    currentList = itemList5
    with open(os.path.join("resources","app","gui","custom","overview","itemList5.json")) as items:
        myDict = json.load(items)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, currentList)
        for key in dictWidgets:
            self.customWidgets[key] = dictWidgets[key]
            self.customWidgets[key].pack()

    itemList1.pack(side=LEFT, padx=(0,0))
    itemList2.pack(side=LEFT, padx=(0,0))
    itemList3.pack(side=LEFT, padx=(0,0))
    itemList4.pack(side=LEFT, padx=(0,0))
    itemList5.pack(side=LEFT, padx=(0,0), anchor=N)

    return self
