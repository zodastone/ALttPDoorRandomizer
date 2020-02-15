from tkinter import ttk, IntVar, StringVar, Checkbutton, Frame, Label, OptionMenu, E, W, LEFT, RIGHT
import gui.widgets as widgets

def dungeon_page(parent):
    # Dungeon Shuffle
    self = ttk.Frame(parent)

    # Dungeon Shuffle options
    self.widgets = {}

    ## Dungeon Item Shuffle
    mcsbshuffleFrame = Frame(self)
    mcsbshuffleFrame.pack(anchor=W)
    mscbLabel = Label(mcsbshuffleFrame, text="Shuffle: ")
    mscbLabel.pack(side=LEFT)

    myDict = {
      ## Map Shuffle
      "mapshuffle": {
        "type": "checkbox",
        "label": {
          "text": "Maps"
        }
      },
      ## Compass Shuffle
      "compassshuffle": {
        "type": "checkbox",
        "label": {
          "text": "Compasses"
        }
      },
      ## Small Key Shuffle
      "smallkeyshuffle": {
        "type": "checkbox",
        "label": {
          "text": "Small Keys"
        }
      },
      ## Big Key Shuffle
      "bigkeyshuffle": {
        "type": "checkbox",
        "label": {
          "text": "Small Keys"
        }
      }
    }

    dictWidgets = widgets.make_widgets_from_dict(self, myDict, mcsbshuffleFrame)

    for key in dictWidgets:
        self.widgets[key] = dictWidgets[key]
        self.widgets[key].pack(side=LEFT)

    myDict = {
      "dungeondoorshuffle": {
        "type": "selectbox",
        "label": {
          "text": "Dungeon Door Shuffle"
        },
        "packAttrs": {
          "label": { "side": LEFT },
          "selectbox": {"side": RIGHT},
          "default": "Basic"
        },
        "options": {
          "Vanilla": "vanilla",
          "Basic": "basic",
          "Crossed": "crossed"
        }
      },
      ## Experiemental features
      "experimental": {
        "type": "checkbox",
        "label": {
          "text": "Enable Experimental Features"
        }
      }
    }

    dictWidgets = widgets.make_widgets_from_dict(self, myDict, self)

    for key in dictWidgets:
        self.widgets[key] = dictWidgets[key]
        self.widgets[key].pack(anchor=W)

    return self
