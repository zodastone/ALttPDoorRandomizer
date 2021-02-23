from tkinter import ttk, filedialog, messagebox, StringVar, Button, Entry, Frame, Label, E, W, LEFT, RIGHT, X, BOTTOM
from AdjusterMain import adjust
from argparse import Namespace
from source.classes.Empty import Empty
from source.classes.SpriteSelector import SpriteSelector
import source.gui.widgets as widgets
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

    # Adjust option frames
    self.frames["selectOptionsFrame"] = Frame(self)
    self.frames["leftAdjustFrame"] = Frame(self.frames["selectOptionsFrame"])
    self.frames["rightAdjustFrame"] = Frame(self.frames["selectOptionsFrame"])
    self.frames["bottomAdjustFrame"] = Frame(self)
    self.frames["selectOptionsFrame"].pack(fill=X)
    self.frames["leftAdjustFrame"].pack(side=LEFT)
    self.frames["rightAdjustFrame"].pack(side=RIGHT)
    self.frames["bottomAdjustFrame"].pack(fill=X)

    # Load Adjust option widgets as defined by JSON file
    # Defns include frame name, widget type, widget options, widget placement attributes
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
    # This one's more-complicated, build it and stuff it
    # widget ID
    widget = "sprite"

    # Empty object
    self.widgets[widget] = Empty()
    # pieces
    self.widgets[widget].pieces = {}

    # frame
    self.widgets[widget].pieces["frame"] = Frame(self.frames["leftAdjustFrame"])
    # frame: label
    self.widgets[widget].pieces["frame"].label = Label(self.widgets[widget].pieces["frame"], text='Sprite: ')
    # spritename: label
    self.widgets[widget].pieces["frame"].spritename = Label(self.widgets[widget].pieces["frame"], text='(unchanged)')
    # storage var
    self.widgets[widget].storageVar = StringVar()
    self.widgets[widget].storageVar.set(settings["sprite"])

		# store sprite
    self.sprite = None

    def set_sprite(sprite_param, random_sprite=False):
        top.randomSprite.set(random_sprite)

        widget = "sprite"
        sprite = {}
        sprite["object"] = sprite_param
        sprite["label"] = {
          "show": "(unchanged)",
          "store": "(unchanged)"
        }
        if sprite_param is None or not sprite_param.valid:
            self.sprite = None
        else:
            self.sprite = sprite_param
            sprite["label"]["store"] = sprite_param.name
            sprite["label"]["show"] = sprite_param.name if not random_sprite else "(random)"
        self.widgets[widget].storageVar.set(sprite["label"]["store"])
        self.widgets[widget].pieces["frame"].spritename.config(text=sprite["label"]["show"])

        print(top.randomSprite.get(),sprite["label"])

    def SpriteSelectAdjuster():
        SpriteSelector(parent, set_sprite, adjuster=True)

    # dialog button
    self.widgets[widget].pieces["button"] = Button(self.widgets[widget].pieces["frame"], text='...', command=SpriteSelectAdjuster)

    # frame label: pack
    self.widgets[widget].pieces["frame"].label.pack(side=LEFT)
    # spritename: pack
    self.widgets[widget].pieces["frame"].spritename.pack(side=LEFT)
    # button: pack
    self.widgets[widget].pieces["button"].pack(side=LEFT)
    # frame: pack
    self.widgets[widget].pieces["frame"].pack(anchor=E)

    self.frames["adjustrom"] = Frame(self.frames["bottomAdjustFrame"])
    self.frames["adjustrom"].pack(anchor=W, fill=X)
    # Path to game file to Adjust
    # This one's more-complicated, build it and stuff it
    # widget ID
    widget = "adjustrom"

    # Empty object
    self.widgets[widget] = Empty()
    # pieces
    self.widgets[widget].pieces = {}

    # frame
    self.widgets[widget].pieces["frame"] = Frame(self.frames["adjustrom"])
    # frame: label
    self.widgets[widget].pieces["frame"].label = Label(self.widgets[widget].pieces["frame"], text='Rom to Adjust: ')
    # storage var
    self.widgets[widget].storageVar = StringVar()
    # textbox
    self.widgets[widget].pieces["textbox"] = Entry(self.widgets[widget].pieces["frame"], textvariable=self.widgets[widget].storageVar)
    self.widgets[widget].storageVar.set(settings["rom"])

    # FIXME: Translate these
    def RomSelect():
        widget = "adjustrom"
        rom = filedialog.askopenfilename(filetypes=[("Rom Files", (".sfc", ".smc")), ("All Files", "*")], initialdir=os.path.join("."))
        self.widgets[widget].storageVar.set(rom)
    # dialog button
    self.widgets[widget].pieces["button"] = Button(self.widgets[widget].pieces["frame"], text='Select Rom', command=RomSelect)

    # frame label: pack
    self.widgets[widget].pieces["frame"].label.pack(side=LEFT)
    # textbox: pack
    self.widgets[widget].pieces["textbox"].pack(side=LEFT, fill=X, expand=True)
    # button: pack
    self.widgets[widget].pieces["button"].pack(side=LEFT)
    # frame: pack
    self.widgets[widget].pieces["frame"].pack(fill=X)

    # These are the options to Adjust
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
        guiargs.baserom = top.pages["randomizer"].pages["generation"].widgets["rom"].storageVar.get()
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
