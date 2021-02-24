from tkinter import ttk, StringVar, Button, Entry, Frame, Label, E, W, LEFT, RIGHT
from functools import partial
from source.classes.Empty import Empty
from source.classes.SpriteSelector import SpriteSelector
import source.gui.widgets as widgets
import json
import os

def gameoptions_page(top, parent):
    # Game Options
    self = ttk.Frame(parent)

    # Game Options options
    self.widgets = {}

    # Game Options option sections
    self.frames = {}
    self.frames["checkboxes"] = Frame(self)
    self.frames["checkboxes"].pack(anchor=W)

    # Game Options frames
    self.frames["leftRomOptionsFrame"] = Frame(self)
    self.frames["rightRomOptionsFrame"] = Frame(self)
    self.frames["leftRomOptionsFrame"].pack(side=LEFT)
    self.frames["rightRomOptionsFrame"].pack(side=RIGHT)

    # Load Game Options widgets as defined by JSON file
    # Defns include frame name, widget type, widget options, widget placement attributes
    # Checkboxes go West
    # Everything else goes East
    # They also get split left & right
    with open(os.path.join("resources","app","gui","randomize","gameoptions","widgets.json")) as widgetDefns:
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
    self.widgets[widget].pieces["frame"] = Frame(self.frames["leftRomOptionsFrame"])
    # frame: label
    self.widgets[widget].pieces["frame"].label = Label(self.widgets[widget].pieces["frame"], text='Sprite: ')
    # spritename: label
    self.widgets[widget].pieces["frame"].spritename = Label(self.widgets[widget].pieces["frame"], text='(unchanged)')
    # storage var
    self.widgets[widget].storageVar = StringVar()

    # store sprite
    self.sprite = None

    def SpriteSetter(spriteObject):
        sprite = {}
        sprite["object"] = spriteObject
        sprite["label"] = {
          "show": "(unchanged)",
          "store": "(unchanged)"
        }
        sprite["label"]["store"] = sprite["object"].name
        sprite["label"]["show"] = sprite["object"].name if not top.randomSprite.get() else "(random)"

        print(top.randomSprite.get(),sprite["label"])

        self.sprite = sprite["object"]
        self.widgets[widget].pieces["frame"].spritename.config(text=sprite["label"]["show"])
    def SpriteSelect():
        SpriteSelector(parent, partial(set_sprite, spriteSetter=SpriteSetter,spriteNameVar=self.widgets[widget].storageVar,randomSpriteVar=top.randomSprite))

    # dialog button
    self.widgets[widget].pieces["button"] = Button(self.widgets[widget].pieces["frame"], text='...', command=SpriteSelect)

    # frame label: pack
    self.widgets[widget].pieces["frame"].label.pack(side=LEFT)
    # spritename: pack
    self.widgets[widget].pieces["frame"].spritename.pack(side=LEFT)
    # button: pack
    self.widgets[widget].pieces["button"].pack(side=LEFT)
    # frame: pack
    self.widgets[widget].pieces["frame"].pack(anchor=E)

    return self

def set_sprite(sprite_param, random_sprite=False, spriteSetter=None, spriteNameVar=None, randomSpriteVar=None):
    if randomSpriteVar:
        randomSpriteVar.set(random_sprite)

    widget = "sprite"
    sprite = {}
    sprite["object"] = sprite_param
    sprite["label"] = {
        "show": "(unchanged)",
        "store": "(unchanged)"
    }
    if sprite["object"] is None or not sprite["object"].valid:
        if spriteSetter:
            spriteSetter(None)
        if spriteNameVar is not None:
            spriteNameVar.set(sprite["store"])
    else:
        if spriteSetter:
            spriteSetter(sprite["object"])
        if spriteNameVar is not None:
            spriteNameVar.set(sprite["label"]["store"])
        sprite["label"]["store"] = sprite["object"].name
        sprite["label"]["show"] = sprite["object"].name if not random_sprite else "(random)"
