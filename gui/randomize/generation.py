import os
from tkinter import ttk, filedialog, IntVar, StringVar, Button, Checkbutton, Entry, Frame, Label, E, W, LEFT, RIGHT, X
import gui.widgets as widgets

def generation_page(parent,settings):
    # Generation Setup
    self = ttk.Frame(parent)

    # Generation Setup options
    self.widgets = {}

    myDict = {
      ## Generate Spoiler
      "spoiler": {
        "type": "checkbox",
        "label": {
          "text": "Create Spoiler Log"
        }
      },
      ## Don't make ROM
      "suppressrom": {
        "type": "checkbox",
        "label": {
          "text": "Do not create patched ROM"
        }
      },
      ## Use Custom Item Pool as defined in Custom tab
      "usecustompool": {
        "type": "checkbox",
        "label": {
          "text": "Use custom item pool"
        }
      }
    }
    dictWidgets = widgets.make_widgets_from_dict(self, myDict, self)
    for key in dictWidgets:
        self.widgets[key] = dictWidgets[key]
        self.widgets[key].pack(anchor=W)

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
