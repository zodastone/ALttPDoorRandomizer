from tkinter import ttk, IntVar, StringVar, Checkbutton, Frame, Label, OptionMenu, E, W, LEFT, RIGHT
import gui.widgets as widgets

def item_page(parent):
    # Item Randomizer
    self = ttk.Frame(parent)

    # Item Randomizer options
    self.widgets = {}

    ## Retro (eventually needs to become a World State)
    key = "retro"
    self.widgets[key] = widgets.make_widget(
      self,
      "checkbox",
      self,
      "Retro mode (universal keys)",
      None
    )
    self.widgets[key].pack(anchor=W)

    leftItemFrame = Frame(self)
    rightItemFrame = Frame(self)
    leftItemFrame.pack(side=LEFT)
    rightItemFrame.pack(side=RIGHT)

    ## World State
    key = "worldstate"
    self.widgets[key] = widgets.make_widget(
      self,
      "selectbox",
      leftItemFrame,
      "World State",
      None,
      {"label": {"side": LEFT}, "selectbox": {"side": RIGHT}, "default": "Open"},
      {
        "Standard": "standard",
        "Open": "open",
        "Inverted": "inverted"
      }
    )
    self.widgets[key].pack(anchor=E)

    ## Logic Level
    key = "logiclevel"
    self.widgets[key] = widgets.make_widget(
      self,
      "selectbox",
      leftItemFrame,
      "Logic Level",
      None,
      {"label": {"side": LEFT}, "selectbox": {"side": RIGHT}},
      {
        "No Glitches": "noglitches",
        "Minor Glitches": "minorglitches",
        "No Logic": "nologic"
      }
    )
    self.widgets[key].pack(anchor=E)

    ## Goal
    key = "goal"
    self.widgets[key] = widgets.make_widget(
      self,
      "selectbox",
      leftItemFrame,
      "Goal",
      None,
      {"label": {"side": LEFT}, "selectbox": {"side": RIGHT}},
      {
        "Defeat Ganon": "ganon",
        "Master Sword Pedestal": "pedestal",
        "All Dungeons": "dungeons",
        "Triforce Hunt": "triforcehunt",
        "Crystals": "crystals"
      }
    )
    self.widgets[key].pack(anchor=E)

    ## Number of crystals to open GT
    key = "crystals_gt"
    keys = [*map(str,range(0,7+1)),"Random"]
    vals = [*map(str,range(0,7+1)),"random"]
    options = {keys[i]: vals[i] for i in range(len(keys))}
    self.widgets[key] = widgets.make_widget(
      self,
      "selectbox",
      leftItemFrame,
      "Crystals to open GT",
      None,
      {"label": {"side": LEFT}, "selectbox": {"side": RIGHT}},
      options
    )
    self.widgets[key].pack(anchor=E)

    ## Number of crystals to damage Ganon
    key = "crystals_ganon"
    keys = [*map(str,range(0,7+1)),"Random"]
    vals = [*map(str,range(0,7+1)),"random"]
    options = {keys[i]: vals[i] for i in range(len(keys))}
    self.widgets[key] = widgets.make_widget(
      self,
      "selectbox",
      leftItemFrame,
      "Crystals to harm Ganon",
      None,
      {"label": {"side": LEFT}, "selectbox": {"side": RIGHT}},
      options
    )
    self.widgets[key].pack(anchor=E)

    ## Weapons
    key = "weapons"
    self.widgets[key] = widgets.make_widget(
      self,
      "selectbox",
      leftItemFrame,
      "Weapons",
      None,
      {"label": {"side": LEFT}, "selectbox": {"side": RIGHT}},
      {
        "Randomized": "random",
        "Assured": "assured",
        "Swordless": "swordless",
        "Vanilla": "vanilla"
      }
    )
    self.widgets[key].pack(anchor=E)

    ## Item Pool
    key = "itempool"
    self.widgets[key] = widgets.make_widget(
      self,
      "selectbox",
      rightItemFrame,
      "Item Pool",
      None,
      {"label": {"side": LEFT}, "selectbox": {"side": RIGHT}},
      {
        "Normal": "normal",
        "Hard": "hard",
        "Expert": "expert"
      }
    )
    self.widgets[key].pack(anchor=E)

    ## Item Functionality
    key = "itemfunction"
    self.widgets[key] = widgets.make_widget(
      self,
      "selectbox",
      rightItemFrame,
      "Item Functionality",
      None,
      {"label": {"side": LEFT}, "selectbox": {"side": RIGHT}},
      {
        "Normal": "normal",
        "Hard": "hard",
        "Expert": "expert"
      }
    )
    self.widgets[key].pack(anchor=E)

    ## Timer setting
    key = "timer"
    self.widgets[key] = widgets.make_widget(
      self,
      "selectbox",
      rightItemFrame,
      "Timer Setting",
      None,
      {"label": {"side": LEFT}, "selectbox": {"side": RIGHT}},
      {
        "No Timer": "none",
        "Stopwatch": "display",
        "Timed": "timed",
        "Timed OHKO": "timed-ohko",
        "OHKO": "ohko",
        "Timed Countdown": "timed-countdown"
      }
    )
    self.widgets[key].pack(anchor=E)

    ## Progressives: On/Off
    key = "progressives"
    self.widgets[key] = widgets.make_widget(
      self,
      "selectbox",
      rightItemFrame,
      "Progressive Items",
      None,
      {"label": {"side": LEFT}, "selectbox": {"side": RIGHT}},
      {
        "On": "on",
        "Off": "off",
        "Random": "random"
      }
    )
    self.widgets[key].pack(anchor=E)

    ## Accessibilty
    key = "accessibility"
    self.widgets[key] = widgets.make_widget(
      self,
      "selectbox",
      rightItemFrame,
      "Accessibility",
      None,
      {"label": {"side": LEFT}, "selectbox": {"side": RIGHT}},
      {
        "100% Inventory": "items",
        "100% Locations": "locations",
        "Beatable": "none"
      }
    )
    self.widgets[key].pack(anchor=E)

    ## Item Sorting Algorithm
    key = "sortingalgo"
    self.widgets[key] = widgets.make_widget(
      self,
      "selectbox",
      rightItemFrame,
      "Item Sorting",
      None,
      {"label": {"side": LEFT}, "selectbox": {"side": RIGHT}, "default": "Balanced"},
      {
        "Freshness": "freshness",
        "Flood": "flood",
        "VT8.21": "vt21",
        "VT8.22": "vt22",
        "VT8.25": "vt25",
        "VT8.26": "vt26",
        "Balanced": "balanced"
      }
    )
    self.widgets[key].pack(anchor=E)

    return self
