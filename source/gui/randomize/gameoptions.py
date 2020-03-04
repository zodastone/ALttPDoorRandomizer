from tkinter import ttk, StringVar, Button, Entry, Frame, Label, E, W, LEFT, RIGHT
from functools import partial
import source.classes.SpriteSelector as spriteSelector
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

    ## Sprite selection
    # This one's more-complicated, build it and stuff it
    spriteDialogFrame = Frame(self.frames["leftRomOptionsFrame"])
    baseSpriteLabel = Label(spriteDialogFrame, text='Sprite:')

    self.widgets["sprite"] = {}
    self.widgets["sprite"]["spriteObject"] = None
    self.widgets["sprite"]["spriteNameVar"] = StringVar()

    self.widgets["sprite"]["spriteNameVar"].set('(unchanged)')
    spriteEntry = Label(spriteDialogFrame, textvariable=self.widgets["sprite"]["spriteNameVar"])

    def sprite_setter(spriteObject):
        self.widgets["sprite"]["spriteObject"] = spriteObject

    def sprite_select():
        spriteSelector.SpriteSelector(parent, partial(set_sprite, spriteSetter=sprite_setter,
                                                      spriteNameVar=self.widgets["sprite"]["spriteNameVar"],
                                                      randomSpriteVar=top.randomSprite))

    spriteSelectButton = Button(spriteDialogFrame, text='...', command=sprite_select)

    baseSpriteLabel.pack(side=LEFT)
    spriteEntry.pack(side=LEFT)
    spriteSelectButton.pack(side=LEFT)
    spriteDialogFrame.pack(anchor=E)

    return self


def set_sprite(sprite_param, random_sprite=False, spriteSetter=None, spriteNameVar=None, randomSpriteVar=None):
    if sprite_param is None or not sprite_param.valid:
        if spriteSetter:
            spriteSetter(None)
        if spriteNameVar is not None:
            spriteNameVar.set('(unchanged)')
    else:
        if spriteSetter:
            spriteSetter(sprite_param)
        if spriteNameVar is not None:
            spriteNameVar.set(sprite_param.name)
    if randomSpriteVar:
        randomSpriteVar.set(random_sprite)
