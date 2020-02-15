import os
from tkinter import ttk, filedialog, IntVar, StringVar, Button, Checkbutton, Entry, Frame, Label, E, W, LEFT, RIGHT, X
import gui.widgets as widgets

def generation_page(parent,settings):
    # Generation Setup
    self = ttk.Frame(parent)

    # Generation Setup options
    self.generationWidgets = {}

    ## Generate Spoiler
    key = "spoiler"
    self.generationWidgets[key] = widgets.make_widget(
      self,
      "checkbox",
      self,
      "Create Spoiler Log",
      None
    )
    self.generationWidgets[key].pack(anchor=W)

    ## Don't make ROM
    key = "suppressrom"
    self.generationWidgets[key] = widgets.make_widget(
      self,
      "checkbox",
      self,
      "Do not create patched ROM",
      None
    )
    self.generationWidgets[key].pack(anchor=W)

    ## Use Custom Item Pool as defined in Custom tab
    key = "usecustompool"
    self.generationWidgets[key] = widgets.make_widget(
      self,
      "checkbox",
      self,
      "Use custom item pool",
      None
    )
    self.generationWidgets[key].pack(anchor=W)

    ## Locate base ROM
    baseRomFrame = Frame(self)
    baseRomLabel = Label(baseRomFrame, text='Base Rom: ')
    self.romVar = StringVar()
    def saveBaseRom(caller,_,mode):
        settings["rom"] = self.romVar.get()
    self.romVar.trace_add("write",saveBaseRom)
    romEntry = Entry(baseRomFrame, textvariable=self.romVar)
    self.romVar.set(settings["rom"])

    def RomSelect():
        rom = filedialog.askopenfilename(filetypes=[("Rom Files", (".sfc", ".smc")), ("All Files", "*")], initialdir=os.path.join("."))
        self.romVar.set(rom)
    romSelectButton = Button(baseRomFrame, text='Select Rom', command=RomSelect)

    baseRomLabel.pack(side=LEFT)
    romEntry.pack(side=LEFT, fill=X, expand=True)
    romSelectButton.pack(side=LEFT)
    baseRomFrame.pack(fill=X, expand=True)

    return self,settings
