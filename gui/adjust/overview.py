from tkinter import ttk, filedialog, messagebox, IntVar, StringVar, Button, Checkbutton, Entry, Frame, Label, OptionMenu, E, W, LEFT, RIGHT, X, BOTTOM
from AdjusterMain import adjust
from argparse import Namespace
from classes.SpriteSelector import SpriteSelector
import gui.widgets as widgets
import json
import logging
import os

def adjust_page(top, parent, settings):
    # Adjust page
    self = ttk.Frame(parent)

    # Adjust options
    self.widgets = {}

    # Adjust option sections
    self.frames = {}
    self.frames["checkboxes"] = Frame(self)
    self.frames["checkboxes"].pack(anchor=W)

    self.frames["selectOptionsFrame"] = Frame(self)
    self.frames["leftAdjustFrame"] = Frame(self.frames["selectOptionsFrame"])
    self.frames["rightAdjustFrame"] = Frame(self.frames["selectOptionsFrame"])
    self.frames["bottomAdjustFrame"] = Frame(self)
    self.frames["selectOptionsFrame"].pack(fill=X)
    self.frames["leftAdjustFrame"].pack(side=LEFT)
    self.frames["rightAdjustFrame"].pack(side=RIGHT)
    self.frames["bottomAdjustFrame"].pack(fill=X)

    with open(os.path.join("resources","app","gui","adjust","overview","widgets.json")) as widgetDefns:
        myDict = json.load(widgetDefns)
        for framename,theseWidgets in myDict.items():
            dictWidgets = widgets.make_widgets_from_dict(self, theseWidgets, self.frames[framename])
            for key in dictWidgets:
                self.widgets[key] = dictWidgets[key]
                packAttrs = {"anchor":E}
                if self.widgets[key].type == "checkbox":
                    packAttrs["anchor"] = W
                self.widgets[key].pack(packAttrs)

    # Sprite Selection
    self.spriteNameVar2 = StringVar()
    spriteDialogFrame2 = Frame(self.frames["leftAdjustFrame"])
    baseSpriteLabel2 = Label(spriteDialogFrame2, text='Sprite:')
    spriteEntry2 = Label(spriteDialogFrame2, textvariable=self.spriteNameVar2)
    self.sprite = None

    def set_sprite(sprite_param, random_sprite=False):
        if sprite_param is None or not sprite_param.valid:
            self.sprite = None
            self.spriteNameVar2.set('(unchanged)')
        else:
            self.sprite = sprite_param
            self.spriteNameVar2.set(self.sprite.name)
        top.randomSprite.set(random_sprite)

    def SpriteSelectAdjuster():
        SpriteSelector(parent, set_sprite, adjuster=True)

    spriteSelectButton2 = Button(spriteDialogFrame2, text='...', command=SpriteSelectAdjuster)

    baseSpriteLabel2.pack(side=LEFT)
    spriteEntry2.pack(side=LEFT)
    spriteSelectButton2.pack(side=LEFT)
    spriteDialogFrame2.pack(anchor=E)

    adjustRomFrame = Frame(self.frames["bottomAdjustFrame"])
    adjustRomLabel = Label(adjustRomFrame, text='Rom to adjust: ')
    self.romVar2 = StringVar(value=settings["rom"])
    romEntry2 = Entry(adjustRomFrame, textvariable=self.romVar2)

    def RomSelect2():
        rom = filedialog.askopenfilename(filetypes=[("Rom Files", (".sfc", ".smc")), ("All Files", "*")])
        if rom:
            settings["rom"] = rom
            self.romVar2.set(rom)
    romSelectButton2 = Button(adjustRomFrame, text='Select Rom', command=RomSelect2)

    adjustRomLabel.pack(side=LEFT)
    romEntry2.pack(side=LEFT, fill=X, expand=True)
    romSelectButton2.pack(side=LEFT)
    adjustRomFrame.pack(fill=X)

    def adjustRom():
        options = {
          "heartbeep": "heartbeep",
          "heartcolor": "heartcolor",
          "menuspeed": "fastmenu",
          "owpalettes": "ow_palettes",
          "uwpalettes": "uw_palettes",
          "quickswap": "quickswap",
          "nobgm": "disablemusic"
        }
        guiargs = Namespace()
        for option in options:
            arg = options[option]
            setattr(guiargs, arg, self.widgets[option].storageVar.get())
        guiargs.rom = self.romVar2.get()
        guiargs.baserom = top.pages["randomizer"].pages["generation"].romVar.get()
        guiargs.sprite = self.sprite
        try:
            adjust(args=guiargs)
        except Exception as e:
            logging.exception(e)
            messagebox.showerror(title="Error while creating seed", message=str(e))
        else:
            messagebox.showinfo(title="Success", message="Rom patched successfully")

    adjustButton = Button(self.frames["bottomAdjustFrame"], text='Adjust Rom', command=adjustRom)
    adjustButton.pack(side=BOTTOM, padx=(5, 0))

    return self,settings
