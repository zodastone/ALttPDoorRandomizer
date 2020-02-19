from tkinter import ttk, IntVar, StringVar, Button, Checkbutton, Entry, Frame, Label, OptionMenu, E, W, LEFT, RIGHT
from functools import partial
import classes.SpriteSelector as spriteSelector
import gui.widgets as widgets
import json
import os

def gameoptions_page(top, parent):
    # Game Options
    self = ttk.Frame(parent)

    # Game Options options
    self.widgets = {}

    with open(os.path.join("resources","app","gui","randomize","gameoptions","checkboxes.json")) as checkboxes:
        myDict = json.load(checkboxes)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, self)
        for key in dictWidgets:
            self.widgets[key] = dictWidgets[key]
            self.widgets[key].pack(anchor=W)

    leftRomOptionsFrame = Frame(self)
    rightRomOptionsFrame = Frame(self)
    leftRomOptionsFrame.pack(side=LEFT)
    rightRomOptionsFrame.pack(side=RIGHT)

    with open(os.path.join("resources","app","gui","randomize","gameoptions","leftRomOptionsFrame.json")) as leftRomOptionsFrameItems:
        myDict = json.load(leftRomOptionsFrameItems)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, leftRomOptionsFrame)
        for key in dictWidgets:
            self.widgets[key] = dictWidgets[key]
            self.widgets[key].pack(anchor=E)

    ## Sprite selection
    spriteDialogFrame = Frame(leftRomOptionsFrame)
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

    with open(os.path.join("resources","app","gui","randomize","gameoptions","rightRomOptionsFrame.json")) as rightRomOptionsFrameItems:
        myDict = json.load(rightRomOptionsFrameItems)
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, rightRomOptionsFrame)
        for key in dictWidgets:
            self.widgets[key] = dictWidgets[key]
            self.widgets[key].pack(anchor=E)

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

