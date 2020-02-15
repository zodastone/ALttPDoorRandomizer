from tkinter import ttk, filedialog, messagebox, IntVar, StringVar, Button, Checkbutton, Entry, Frame, Label, OptionMenu, E, W, LEFT, RIGHT, X, BOTTOM
from AdjusterMain import adjust
from argparse import Namespace
from classes.SpriteSelector import SpriteSelector
import gui.widgets as widgets
import logging


def adjust_page(top, parent, settings):
    # Adjust page
    self = ttk.Frame(parent)

    # Adjust options
    self.adjustWidgets = {}

    # Disable BGM
    key = "nobgm"
    self.adjustWidgets[key] = widgets.make_widget(
      self,
      "checkbox",
      self,
      "Disable Music & MSU-1",
      top.pages["randomizer"].pages["gameoptions"].gameOptionsWidgets["nobgm"].storageVar
    )
    self.adjustWidgets[key].pack(anchor=W)

    # L/R Quickswap
    key = "quickswap"
    self.adjustWidgets[key] = widgets.make_widget(
      self,
      "checkbox",
      self,
      "L/R Quickswapping",
      top.pages["randomizer"].pages["gameoptions"].gameOptionsWidgets["quickswap"].storageVar
    )
    self.adjustWidgets[key].pack(anchor=W)

    selectOptionsFrame = Frame(self)
    leftAdjustFrame = Frame(selectOptionsFrame)
    rightAdjustFrame = Frame(selectOptionsFrame)
    bottomAdjustFrame = Frame(self)
    selectOptionsFrame.pack(fill=X, expand=True)
    leftAdjustFrame.pack(side=LEFT)
    rightAdjustFrame.pack(side=RIGHT)
    bottomAdjustFrame.pack(fill=X, expand=True)

    ## Heart Color
    key = "heartcolor"
    self.adjustWidgets[key] = widgets.make_widget(
      self,
      "selectbox",
      leftAdjustFrame,
      "Heart Color",
      top.pages["randomizer"].pages["gameoptions"].gameOptionsWidgets["heartcolor"].storageVar,
      {"label": {"side": LEFT}, "selectbox": {"side": RIGHT}},
      {
        "Red": "red",
        "Blue": "blue",
        "Green": "green",
        "Yellow": "yellow",
        "Random": "random"
      }
    )
    self.adjustWidgets[key].pack(anchor=E)

    ## Heart Beep Speed
    key = "heartbeep"
    self.adjustWidgets[key] = widgets.make_widget(
      self,
      "selectbox",
      leftAdjustFrame,
      "Heart Beep sound rate",
      top.pages["randomizer"].pages["gameoptions"].gameOptionsWidgets["heartbeep"].storageVar,
      {"label": {"side": LEFT}, "selectbox": {"side": RIGHT}, "default": "Normal"},
      {
        "Double": "double",
        "Normal": "normal",
        "Half": "half",
        "Quarter": "quarter",
        "Off": "off"
      }
    )
    self.adjustWidgets[key].pack(anchor=W)

    # Sprite Selection
    self.spriteNameVar2 = StringVar()
    spriteDialogFrame2 = Frame(leftAdjustFrame)
    baseSpriteLabel2 = Label(spriteDialogFrame2, text='Sprite:')
    spriteEntry2 = Label(spriteDialogFrame2, textvariable=self.spriteNameVar2)
    self.sprite = None

    def set_sprite(sprite_param, random_sprite):
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

    # Menu Speed
    key = "menuspeed"
    self.adjustWidgets[key] = widgets.make_widget(
      self,
      "selectbox",
      rightAdjustFrame,
      "Menu Speed",
      top.pages["randomizer"].pages["gameoptions"].gameOptionsWidgets["menuspeed"].storageVar,
      {"label": {"side": LEFT}, "selectbox": {"side": RIGHT}, "default": "Normal"},
      {
        "Instant": "instant",
        "Quadruple": "quadruple",
        "Triple": "triple",
        "Double": "double",
        "Normal": "normal",
        "Half": "half"
      }
    )
    self.adjustWidgets[key].pack(anchor=E)

    # Overworld Palettes (not Enemizer)
    key = "owpalettes"
    self.adjustWidgets[key] = widgets.make_widget(
      self,
      "selectbox",
      rightAdjustFrame,
      "Overworld Palettes",
      top.pages["randomizer"].pages["gameoptions"].gameOptionsWidgets["owpalettes"].storageVar,
      {"label": {"side": LEFT}, "selectbox": {"side": RIGHT}},
      {
        "Default": "default",
        "Random": "random",
        "Blackout": "blackout"
      }
    )
    self.adjustWidgets[key].pack(anchor=E)

    # Underworld Palettes (not Enemizer)
    key = "uwpalettes"
    self.adjustWidgets[key] = widgets.make_widget(
      self,
      "selectbox",
      rightAdjustFrame,
      "Underworld Palettes",
      top.pages["randomizer"].pages["gameoptions"].gameOptionsWidgets["uwpalettes"].storageVar,
      {"label": {"side": LEFT}, "selectbox": {"side": RIGHT}},
      {
        "Default": "default",
        "Random": "random",
        "Blackout": "blackout"
      }
    )
    self.adjustWidgets[key].pack(anchor=E)

    adjustRomFrame = Frame(bottomAdjustFrame)
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
    adjustRomFrame.pack(fill=X, expand=True)

    def adjustRom():
        guiargs = Namespace()
        guiargs.heartbeep = self.adjustWidgets["heartbeep"].storageVar.get()
        guiargs.heartcolor = self.adjustWidgets["heartcolor"].storageVar.get()
        guiargs.fastmenu = self.adjustWidgets["menuspeed"].storageVar.get()
        guiargs.ow_palettes = self.adjustWidgets["owpalettes"].storageVar.get()
        guiargs.uw_palettes = self.adjustWidgets["uwpalettes"].storageVar.get()
        guiargs.quickswap = bool(self.adjustWidgets["quickswap"].storageVar.get())
        guiargs.disablemusic = bool(self.adjustWidgets["nobgm"].storageVar.get())
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

    adjustButton = Button(bottomAdjustFrame, text='Adjust Rom', command=adjustRom)
    adjustButton.pack(side=BOTTOM, padx=(5, 0))

    return self,settings
