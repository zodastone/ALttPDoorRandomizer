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

    ## Map Shuffle
    key = "mapshuffle"
    self.widgets[key] = widgets.make_widget(
      self,
      "checkbox",
      mcsbshuffleFrame,
      "Maps",
      None
    )
    self.widgets[key].pack(side=LEFT)

    ## Compass Shuffle
    key = "compassshuffle"
    self.widgets[key] = widgets.make_widget(
      self,
      "checkbox",
      mcsbshuffleFrame,
      "Compasses",
      None
    )
    self.widgets[key].pack(side=LEFT)

    ## Small Key Shuffle
    key = "smallkeyshuffle"
    self.widgets[key] = widgets.make_widget(
      self,
      "checkbox",
      mcsbshuffleFrame,
      "Small Keys",
      None
    )
    self.widgets[key].pack(side=LEFT)

    ## Big Key Shuffle
    key = "bigkeyshuffle"
    self.widgets[key] = widgets.make_widget(
      self,
      "checkbox",
      mcsbshuffleFrame,
      "Big Keys",
      None
    )
    self.widgets[key].pack(side=LEFT)

    ## Dungeon Door Shuffle
    key = "dungeondoorshuffle"
    self.widgets[key] = widgets.make_widget(
      self,
      "selectbox",
      self,
      "Dungeon Door Shuffle",
      None,
      {"label": {"side": LEFT}, "selectbox": {"side": RIGHT}, "default": "Basic"},
      {
        "Vanilla": "vanilla",
        "Basic": "basic",
        "Crossed": "crossed"
      }
    )
    self.widgets[key].pack(anchor=W)

    # Experimental features
    key = "experimental"
    self.widgets[key] = widgets.make_widget(
        self,
        "checkbox",
        self,
        "Enable Experimental Features",
        None
    )
    self.widgets[key].pack(anchor=W)

    return self
