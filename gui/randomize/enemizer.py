import os
from tkinter import ttk, filedialog, IntVar, StringVar, Button, Checkbutton, Entry, Frame, Label, LabelFrame, OptionMenu, N, E, W, LEFT, RIGHT, X
import gui.widgets as widgets
import json
import os

def enemizer_page(parent,settings):
    # Enemizer
    self = ttk.Frame(parent)

    # Enemizer options
    self.widgets = {}

    with open(os.path.join("resources","app","gui","randomize","enemizer","checkboxes.json")) as checkboxes:
        myDict = json.load(checkboxes)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, self)
        for key in dictWidgets:
            self.widgets[key] = dictWidgets[key]
            self.widgets[key].pack(anchor=W)

    ## Enemizer CLI Path
    enemizerPathFrame = Frame(self)
    enemizerCLIlabel = Label(enemizerPathFrame, text="EnemizerCLI path: ")
    enemizerCLIlabel.pack(side=LEFT)
    self.enemizerCLIpathVar = StringVar(value=settings["enemizercli"])
    def saveEnemizerPath(caller,_,mode):
        settings["enemizercli"] = self.enemizerCLIpathVar.get()
    self.enemizerCLIpathVar.trace_add("write",saveEnemizerPath)
    enemizerCLIpathEntry = Entry(enemizerPathFrame, textvariable=self.enemizerCLIpathVar)
    enemizerCLIpathEntry.pack(side=LEFT, fill=X, expand=True)
    def EnemizerSelectPath():
        path = filedialog.askopenfilename(filetypes=[("EnemizerCLI executable", "*EnemizerCLI*")], initialdir=os.path.join("."))
        if path:
            self.enemizerCLIpathVar.set(path)
            settings["enemizercli"] = path
    enemizerCLIbrowseButton = Button(enemizerPathFrame, text='...', command=EnemizerSelectPath)
    enemizerCLIbrowseButton.pack(side=LEFT)
    enemizerPathFrame.pack(fill=X, expand=True)

    leftEnemizerFrame = Frame(self)
    rightEnemizerFrame = Frame(self)
    leftEnemizerFrame.pack(side=LEFT, anchor=N)
    rightEnemizerFrame.pack(side=RIGHT, anchor=N)

    with open(os.path.join("resources","app","gui","randomize","enemizer","leftEnemizerFrame.json")) as leftEnemizerFrameItems:
        myDict = json.load(leftEnemizerFrameItems)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, leftEnemizerFrame)
        for key in dictWidgets:
            self.widgets[key] = dictWidgets[key]
            self.widgets[key].pack(anchor=E)

    with open(os.path.join("resources","app","gui","randomize","enemizer","rightEnemizerFrame.json")) as rightEnemizerFrameItems:
        myDict = json.load(rightEnemizerFrameItems)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, rightEnemizerFrame)
        for key in dictWidgets:
            self.widgets[key] = dictWidgets[key]
            self.widgets[key].pack(anchor=E)

    return self,settings
