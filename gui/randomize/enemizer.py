import os
from tkinter import ttk, filedialog, IntVar, StringVar, Button, Checkbutton, Entry, Frame, Label, LabelFrame, OptionMenu, N, E, W, LEFT, RIGHT, BOTTOM, X
import gui.widgets as widgets
import json
import os
import webbrowser

def enemizer_page(parent,settings):
    def open_enemizer_download(_evt):
        webbrowser.open("https://github.com/Bonta0/Enemizer/releases")

    # Enemizer
    self = ttk.Frame(parent)

    # Enemizer options
    self.widgets = {}

    # Enemizer option sections
    self.frames = {}

    self.frames["checkboxes"] = Frame(self)
    self.frames["checkboxes"].pack(anchor=W)

    self.frames["selectOptionsFrame"] = Frame(self)
    self.frames["leftEnemizerFrame"] = Frame(self.frames["selectOptionsFrame"])
    self.frames["rightEnemizerFrame"] = Frame(self.frames["selectOptionsFrame"])
    self.frames["bottomEnemizerFrame"] = Frame(self)
    self.frames["selectOptionsFrame"].pack(fill=X)
    self.frames["leftEnemizerFrame"].pack(side=LEFT)
    self.frames["rightEnemizerFrame"].pack(side=RIGHT)
    self.frames["bottomEnemizerFrame"].pack(fill=X)

    with open(os.path.join("resources","app","gui","randomize","enemizer","widgets.json")) as widgetDefns:
        myDict = json.load(widgetDefns)
        for framename,theseWidgets in myDict.items():
            dictWidgets = widgets.make_widgets_from_dict(self, theseWidgets, self.frames[framename])
            for key in dictWidgets:
                self.widgets[key] = dictWidgets[key]
                packAttrs = {"anchor":E}
                if self.widgets[key].type == "checkbox":
                    packAttrs["anchor"] = W
                self.widgets[key].pack(packAttrs)

    ## Enemizer CLI Path
    enemizerPathFrame = Frame(self.frames["bottomEnemizerFrame"])
    enemizerCLIlabel = Label(enemizerPathFrame, text="EnemizerCLI path: ")
    enemizerCLIlabel.pack(side=LEFT)
    enemizerURL = Label(enemizerPathFrame, text="(get online)", fg="blue", cursor="hand2")
    enemizerURL.pack(side=LEFT)
    enemizerURL.bind("<Button-1>", open_enemizer_download)
    self.enemizerCLIpathVar = StringVar(value=settings["enemizercli"])
    enemizerCLIpathEntry = Entry(enemizerPathFrame, textvariable=self.enemizerCLIpathVar)
    enemizerCLIpathEntry.pack(side=LEFT, fill=X, expand=True)
    def EnemizerSelectPath():
        path = filedialog.askopenfilename(filetypes=[("EnemizerCLI executable", "*EnemizerCLI*")], initialdir=os.path.join("."))
        if path:
            self.enemizerCLIpathVar.set(path)
            settings["enemizercli"] = path
    enemizerCLIbrowseButton = Button(enemizerPathFrame, text='...', command=EnemizerSelectPath)
    enemizerCLIbrowseButton.pack(side=LEFT)
    enemizerPathFrame.pack(fill=X)

    return self,settings
