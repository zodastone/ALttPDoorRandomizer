from tkinter import ttk, filedialog, messagebox, IntVar, StringVar, Button, Checkbutton, Entry, Frame, Label, OptionMenu, E, W, LEFT, RIGHT, X, BOTTOM
from AdjusterMain import adjust
from argparse import Namespace
from classes.SpriteSelector import SpriteSelector
import gui.widgets as widgets
import logging

def adjust_page(top,parent,working_dirs):
    # Adjust page
    self = ttk.Frame(parent)

    # Adjust options
    self.adjustWidgets = {}

    ## Disable BGM
    key = "nobgm"
    self.adjustWidgets[key] = widgets.make_widget(
      self,
      "checkbox",
      self,
      "Disable Music & MSU-1",
      None
    )
    self.adjustWidgets[key].pack(anchor=W)

    ## L/R Quickswap
    key = "quickswap"
    self.adjustWidgets[key] = widgets.make_widget(
      self,
      "checkbox",
      self,
      "L/R Quickswapping",
      None
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
      None,
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
      None,
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
    self.spriteNameVar2.set('(unchanged)')
    spriteEntry2 = Label(spriteDialogFrame2, textvariable=self.spriteNameVar2)

    def set_sprite(sprite_param):
        if sprite_param is None or not sprite_param.valid:
            sprite = None
            self.spriteNameVar2.set('(unchanged)')
        else:
            sprite = sprite_param
            self.spriteNameVar2.set(sprite.name)

    def SpriteSelectAdjuster():
        SpriteSelector(parent, set_sprite, adjuster=True)

    spriteSelectButton2 = Button(spriteDialogFrame2, text='...', command=SpriteSelectAdjuster)

    baseSpriteLabel2.pack(side=LEFT)
    spriteEntry2.pack(side=LEFT)
    spriteSelectButton2.pack(side=LEFT)
    spriteDialogFrame2.pack(anchor=E)

    ## Menu Speed
    key = "menuspeed"
    self.adjustWidgets[key] = widgets.make_widget(
      self,
      "selectbox",
      rightAdjustFrame,
      "Menu Speed",
      None,
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

    ## Overworld Palettes (not Enemizer)
    key = "owpalettes"
    self.adjustWidgets[key] = widgets.make_widget(
      self,
      "selectbox",
      rightAdjustFrame,
      "Overworld Palettes",
      None,
      {"label": {"side": LEFT}, "selectbox": {"side": RIGHT}},
      {
        "Default": "default",
        "Random": "random",
        "Blackout": "blackout"
      }
    )
    self.adjustWidgets[key].pack(anchor=E)

    ## Underworld Palettes (not Enemizer)
    key = "uwpalettes"
    self.adjustWidgets[key] = widgets.make_widget(
      self,
      "selectbox",
      rightAdjustFrame,
      "Underworld Palettes",
      None,
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
    self.romVar2 = StringVar(value=working_dirs["adjust.rom"])
    romEntry2 = Entry(adjustRomFrame, textvariable=self.romVar2)

    def RomSelect2():
        rom = filedialog.askopenfilename(filetypes=[("Rom Files", (".sfc", ".smc")), ("All Files", "*")])
        if rom:
            working_dirs["adjust.rom"] = rom
            self.romVar2.set(rom)
    romSelectButton2 = Button(adjustRomFrame, text='Select Rom', command=RomSelect2)

    adjustRomLabel.pack(side=LEFT)
    romEntry2.pack(side=LEFT, fill=X, expand=True)
    romSelectButton2.pack(side=LEFT)
    adjustRomFrame.pack(fill=X, expand=True)

    def adjustRom():
        guiargs = Namespace()
        guiargs.heartbeep = self.adjustWidgets["heartbeep"].get()
        guiargs.heartcolor = self.adjustWidgets["heartcolor"].get()
        guiargs.fastmenu = self.adjustWidgets["menuspeed"].get()
        guiargs.ow_palettes = self.adjustWidgets["owpalettes"].get()
        guiargs.uw_palettes = self.adjustWidgets["uwpalettes"].get()
        guiargs.quickswap = bool(self.adjustWidgets["quickswap"].get())
        guiargs.disablemusic = bool(self.adjustWidgets["nobgm"].get())
        guiargs.rom = self.romVar2.get()
        guiargs.baserom = top.generationSetupWindow.romVar.get()
#        guiargs.sprite = sprite
        try:
            adjust(args=guiargs)
        except Exception as e:
            logging.exception(e)
            messagebox.showerror(title="Error while creating seed", message=str(e))
        else:
            messagebox.showinfo(title="Success", message="Rom patched successfully")

    adjustButton = Button(bottomAdjustFrame, text='Adjust Rom', command=adjustRom)
    adjustButton.pack(side=BOTTOM, padx=(5, 0))

    return self,working_dirs
