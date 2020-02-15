from tkinter import ttk, IntVar, StringVar, Checkbutton, Frame, Label, OptionMenu, E, W, LEFT, RIGHT
import gui.widgets as widgets

def entrando_page(parent):
    # Entrance Randomizer
    self = ttk.Frame(parent)

    # Entrance Randomizer options
    self.widgets = {}

    myDict = {
      ## Pyramid pre-opened
      "openpyramid": {
        "type": "checkbox",
        "label": {
          "text": "Pre-open Pyramid Hole"
        }
      },
      ## Shuffle Ganon
      "shuffleganon": {
        "type": "checkbox",
        "label": {
          "text": "Include Ganon's Tower and Pyramid Hole in shuffle pool"
        }
      },
      ## Entrance Shuffle
      "entranceshuffle": {
        "type": "selectbox",
        "label": {
          "text": "Entrance Shuffle"
        },
        "packAttrs": {
          "label": { "side": LEFT },
          "selectbox": { "side": RIGHT }
        },
        "options": {
          "Vanilla": "vanilla",
          "Simple": "simple",
          "Restricted": "restricted",
          "Full": "full",
          "Crossed": "crossed",
          "Insanity": "insanity",
          "Restricted (Legacy)": "restricted_legacy",
          "Full (Legacy)": "full_legacy",
          "Madness (Legacy)": "madness_legacy",
          "Insanity (Legacy)": "insanity_legacy",
          "Dungeons + Full": "dungeonsfull",
          "Dungeons + Simple": "dungeonssimple"
        }
      }
    }
    dictWidgets = widgets.make_widgets_from_dict(self, myDict, self)
    for key in dictWidgets:
        self.widgets[key] = dictWidgets[key]
        self.widgets[key].pack(anchor=W)

    return self
