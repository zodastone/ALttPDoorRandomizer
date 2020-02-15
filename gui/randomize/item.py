from tkinter import ttk, IntVar, StringVar, Checkbutton, Frame, Label, OptionMenu, E, W, LEFT, RIGHT
import gui.widgets as widgets

def item_page(parent):
    # Item Randomizer
    self = ttk.Frame(parent)

    # Item Randomizer options
    self.widgets = {}

    myDict = {
      ## Retro (eventually needs to become a World State)
      "retro": {
        "type": "checkbox",
        "label": {
          "text": "Retro mode (universal keys)"
        }
      }
    }
    dictWidgets = widgets.make_widgets_from_dict(self, myDict, self)
    for key in dictWidgets:
        self.widgets[key] = dictWidgets[key]
        self.widgets[key].pack(anchor=W)

    leftItemFrame = Frame(self)
    rightItemFrame = Frame(self)
    leftItemFrame.pack(side=LEFT)
    rightItemFrame.pack(side=RIGHT)

    keys = [*map(str,range(0,7+1)),"Random"]
    vals = [*map(str,range(0,7+1)),"random"]
    crystalsOptions = {keys[i]: vals[i] for i in range(len(keys))}

    myDict = {
      ## World State
      "worldstate": {
        "type": "selectbox",
        "label": {
          "text": "World State"
        },
        "packAttrs": {
          "label": { "side": LEFT },
          "selectbox": { "side": RIGHT },
          "default": "Open"
        },
        "options": {
          "Standard": "standard",
          "Open": "open",
          "Inverted": "inverted"
        }
      },
      ## Logic Level
      "logiclevel": {
        "type": "selectbox",
        "label": {
          "text": "Logic Level"
        },
        "packAttrs": {
          "label": { "side": LEFT },
          "selectbox": { "side": RIGHT }
        },
        "options": {
          "No Glitches": "noglitches",
          "Minor Glitches": "minorglitches",
          "No Logic": "nologic"
        }
      },
      ## Goal
      "goal": {
        "type": "selectbox",
        "label": {
          "text": "Goal"
        },
        "packAttrs": {
          "label": { "side": LEFT },
          "selectbox": { "side": RIGHT }
        },
        "options": {
          "Defeat Ganon": "ganon",
          "Master Sword Pedestal": "pedestal",
          "All Dungeons": "dungeons",
          "Triforce Hunt": "triforcehunt",
          "Crystals": "crystals"
        }
      },
      ## Number of crystals to open GT
      "crystals_gt": {
        "type": "selectbox",
        "label": {
          "text": "Crystals to open GT"
        },
        "packAttrs": {
          "label": { "side": LEFT },
          "selectbox": { "side": RIGHT }
        },
        "options": crystalsOptions
      },
      ## Number of crystals to damage Ganon
      "crystals_ganon": {
        "type": "selectbox",
        "label": {
          "text": "Crystals to harm Ganon"
        },
        "packAttrs": {
          "label": { "side": LEFT },
          "selectbox": { "side": RIGHT }
        },
        "options": crystalsOptions
      },
      ## Weapons
      "weapons": {
        "type": "selectbox",
        "label": {
          "text": "Weapons"
        },
        "packAttrs": {
          "label": { "side": LEFT },
          "selectbox": { "side": RIGHT }
        },
        "options": {
          "Randomized": "random",
          "Assured": "assured",
          "Swordless": "swordless",
          "Vanilla": "vanilla"
        }
      }
    }
    dictWidgets = widgets.make_widgets_from_dict(self, myDict, leftItemFrame)
    for key in dictWidgets:
        self.widgets[key] = dictWidgets[key]
        self.widgets[key].pack(anchor=E)

    myDict = {
      ## Item Pool
      "itempool": {
        "type": "selectbox",
        "label": {
          "text": "Item Pool"
        },
        "packAttrs": {
          "label": { "side": LEFT },
          "selectbox": { "side": RIGHT }
        },
        "options": {
          "Normal": "normal",
          "Hard": "hard",
          "Expert": "expert"
        }
      },
      ## Item Functionality
      "itemfunction": {
        "type": "selectbox",
        "label": {
          "text": "Item Functionality"
        },
        "packAttrs": {
          "label": { "side": LEFT },
          "selectbox": { "side": RIGHT }
        },
        "options": {
          "Normal": "normal",
          "Hard": "hard",
          "Expert": "expert"
        }
      },
      ## Timer setting
      "timer": {
        "type": "selectbox",
        "label": {
          "text": "Timer Setting"
        },
        "packAttrs": {
          "label": { "side": LEFT },
          "selectbox": { "side": RIGHT }
        },
        "options": {
          "No Timer": "none",
          "Stopwatch": "display",
          "Timed": "timed",
          "Timed OHKO": "timed-ohko",
          "OHKO": "ohko",
          "Timed Countdown": "timed-countdown"
        }
      },
      ## Progressives: On/Off
      "progressives": {
        "type": "selectbox",
        "label": {
          "text": "Progressive Items"
        },
        "packAttrs": {
          "label": { "side": LEFT },
          "selectbox": { "side": RIGHT }
        },
        "options": {
          "On": "on",
          "Off": "off",
          "Random": "random"
        }
      },
      ## Accessibility
      "accessibility": {
        "type": "selectbox",
        "label": {
          "text": "Accessibility"
        },
        "packAttrs": {
          "label": { "side": LEFT },
          "selectbox": { "side": RIGHT }
        },
        "options": {
          "100% Inventory": "items",
          "100% Locations": "locations",
          "Beatable": "none"
        }
      },
      ## Item Sorting Algorithm
      "sortingalgo": {
        "type": "selectbox",
        "label": {
          "text": "Item Sorting"
        },
        "packAttrs": {
          "label": { "side": LEFT },
          "selectbox": { "side": RIGHT },
          "default": "Balanced"
        },
        "options": {
          "Freshness": "freshness",
          "Flood": "flood",
          "VT8.21": "vt21",
          "VT8.22": "vt22",
          "VT8.25": "vt25",
          "VT8.26": "vt26",
          "Balanced": "balanced"
        }
      }
    }
    dictWidgets = widgets.make_widgets_from_dict(self, myDict, rightItemFrame)
    for key in dictWidgets:
        self.widgets[key] = dictWidgets[key]
        self.widgets[key].pack(anchor=E)

    return self
