from tkinter import ttk, IntVar, StringVar, Button, Checkbutton, Entry, Frame, Label, OptionMenu, E, W, LEFT, RIGHT
from functools import partial
import classes.SpriteSelector as spriteSelector
import gui.widgets as widgets


def gameoptions_page(top, parent):
    # Game Options
    self = ttk.Frame(parent)

    # Game Options options
    self.gameOptionsWidgets = {}

    ## Hints: Useful/Not useful
    key = "hints"
    self.gameOptionsWidgets[key] = widgets.make_widget(
      self,
      "checkbox",
      self,
      "Include Helpful Hints",
      None
    )
    self.gameOptionsWidgets[key].pack(anchor=W)

    ## Disable BGM
    key = "nobgm"
    self.gameOptionsWidgets[key] = widgets.make_widget(
      self,
      "checkbox",
      self,
      "Disable Music & MSU-1",
      None
    )
    self.gameOptionsWidgets[key].pack(anchor=W)

    ## L/R Quickswap
    key = "quickswap"
    self.gameOptionsWidgets[key] = widgets.make_widget(
      self,
      "checkbox",
      self,
      "L/R Quickswapping",
      None
    )
    self.gameOptionsWidgets[key].pack(anchor=W)

    leftRomOptionsFrame = Frame(self)
    rightRomOptionsFrame = Frame(self)
    leftRomOptionsFrame.pack(side=LEFT)
    rightRomOptionsFrame.pack(side=RIGHT)

    ## Heart Color
    key = "heartcolor"
    self.gameOptionsWidgets[key] = widgets.make_widget(
      self,
      "selectbox",
      leftRomOptionsFrame,
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
    self.gameOptionsWidgets[key].pack(anchor=E)

    ## Heart Beep Speed
    key = "heartbeep"
    self.gameOptionsWidgets[key] = widgets.make_widget(
      self,
      "selectbox",
      leftRomOptionsFrame,
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
    self.gameOptionsWidgets[key].pack(anchor=W)

    ## Sprite selection
    spriteDialogFrame = Frame(leftRomOptionsFrame)
    baseSpriteLabel = Label(spriteDialogFrame, text='Sprite:')

    self.gameOptionsWidgets["sprite"] = {}
    self.gameOptionsWidgets["sprite"]["spriteObject"] = None
    self.gameOptionsWidgets["sprite"]["spriteNameVar"] = StringVar()

    self.gameOptionsWidgets["sprite"]["spriteNameVar"].set('(unchanged)')
    spriteEntry = Label(spriteDialogFrame, textvariable=self.gameOptionsWidgets["sprite"]["spriteNameVar"])

    def sprite_setter(spriteObject):
        self.gameOptionsWidgets["sprite"]["spriteObject"] = spriteObject

    def sprite_select():
        spriteSelector.SpriteSelector(parent, partial(set_sprite, spriteSetter=sprite_setter,
                                                      spriteNameVar=self.gameOptionsWidgets["sprite"]["spriteNameVar"],
                                                      randomSpriteVar=top.randomSprite))

    spriteSelectButton = Button(spriteDialogFrame, text='...', command=sprite_select)

    baseSpriteLabel.pack(side=LEFT)
    spriteEntry.pack(side=LEFT)
    spriteSelectButton.pack(side=LEFT)
    spriteDialogFrame.pack(anchor=E)

    ## Menu Speed
    key = "menuspeed"
    self.gameOptionsWidgets[key] = widgets.make_widget(
      self,
      "selectbox",
      rightRomOptionsFrame,
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
    self.gameOptionsWidgets[key].pack(anchor=E)

    ## Overworld Palettes (not Enemizer)
    key = "owpalettes"
    self.gameOptionsWidgets[key] = widgets.make_widget(
      self,
      "selectbox",
      rightRomOptionsFrame,
      "Overworld Palettes",
      None,
      {"label": {"side": LEFT}, "selectbox": {"side": RIGHT}},
      {
        "Default": "default",
        "Random": "random",
        "Blackout": "blackout"
      }
    )
    self.gameOptionsWidgets[key].pack(anchor=E)

    ## Underworld Palettes (not Enemizer)
    key = "uwpalettes"
    self.gameOptionsWidgets[key] = widgets.make_widget(
      self,
      "selectbox",
      rightRomOptionsFrame,
      "Underworld Palettes",
      None,
      {"label": {"side": LEFT}, "selectbox": {"side": RIGHT}},
      {
        "Default": "default",
        "Random": "random",
        "Blackout": "blackout"
      }
    )
    self.gameOptionsWidgets[key].pack(anchor=E)

    return self


def set_sprite(sprite_param, random_sprite, spriteSetter=None, spriteNameVar=None, randomSpriteVar=None):
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

