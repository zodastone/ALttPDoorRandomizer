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
    self.widgets = {}

    myDict = {
      ## Disable BGM
      "nobgm": {
        "type": "checkbox",
        "label": {
          "text": "Disable Music & MSU-1"
        }
      },
      ## L/R Quickswap
      "quickswap": {
        "type": "checkbox",
        "label": {
          "text": "L/R Quickswapping"
        }
      }
    }
    dictWidgets = widgets.make_widgets_from_dict(self, myDict, self)
    for key in dictWidgets:
        self.widgets[key] = dictWidgets[key]
        self.widgets[key].pack(anchor=W)

    selectOptionsFrame = Frame(self)
    leftAdjustFrame = Frame(selectOptionsFrame)
    rightAdjustFrame = Frame(selectOptionsFrame)
    bottomAdjustFrame = Frame(self)
    selectOptionsFrame.pack(fill=X, expand=True)
    leftAdjustFrame.pack(side=LEFT)
    rightAdjustFrame.pack(side=RIGHT)
    bottomAdjustFrame.pack(fill=X, expand=True)

    myDict = {
      ## Heart Color
      "heartcolor": {
        "type": "selectbox",
        "label": {
          "text": "Heart Color"
        },
        "packAttrs": {
          "label": { "side": LEFT },
          "selectbox": { "side": RIGHT }
        },
        "options": {
          "Red": "red",
          "Blue": "blue",
          "Green": "green",
          "Yellow": "yellow",
          "Random": "random"
        }
      },
      ## Heart Beep speed
      "heartbeep": {
        "type": "selectbox",
        "label": {
          "text": "Heart Beep sound rate"
        },
        "packAttrs": {
          "label": { "side": LEFT },
          "selectbox": { "side": RIGHT},
          "default": "Normal"
        },
        "options": {
          "Double": "double",
          "Normal": "normal",
          "Half": "half",
          "Quarter": "quarter",
          "Off": "off"
        }
      }
    }
    dictWidgets = widgets.make_widgets_from_dict(self, myDict, leftAdjustFrame)
    for key in dictWidgets:
        self.widgets[key] = dictWidgets[key]
        self.widgets[key].pack(anchor=E)

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

    myDict = {
      ## Menu Speed
      "menuspeed": {
        "type": "selectbox",
        "label": {
          "text": "Menu Speed"
        },
        "packAttrs": {
          "label": { "side": LEFT },
          "selectbox": { "side": RIGHT },
          "default": "Normal"
        },
        "options": {
          "Instant": "instant",
          "Quadruple": "quadruple",
          "Triple": "triple",
          "Double": "double",
          "Normal": "normal",
          "Half": "half"
        }
      },
      ## Overworld Palettes (not Enemizer)
      "owpalettes": {
        "type": "selectbox",
        "label": {
          "text": "Overworld Palettes"
        },
        "packAttrs": {
          "label": { "side": LEFT },
          "selectbox": { "side": RIGHT }
        },
        "options": {
          "Default": "default",
          "Random": "random",
          "Blackout": "blackout"
        }
      },
      ## Underworld Palettes (not Enemizer)
      "uwpalettes": {
        "type": "selectbox",
        "label": {
          "text": "Underworld Palettes"
        },
        "packAttrs": {
          "label": { "side": LEFT },
          "selectbox": { "side": RIGHT }
        },
        "options": {
          "Default": "default",
          "Random": "random",
          "Blackout": "blackout"
        }
      }
    }
    dictWidgets = widgets.make_widgets_from_dict(self, myDict, rightAdjustFrame)
    for key in dictWidgets:
        self.widgets[key] = dictWidgets[key]
        self.widgets[key].pack(anchor=E)

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

    adjustButton = Button(bottomAdjustFrame, text='Adjust Rom', command=adjustRom)
    adjustButton.pack(side=BOTTOM, padx=(5, 0))

    return self,settings
