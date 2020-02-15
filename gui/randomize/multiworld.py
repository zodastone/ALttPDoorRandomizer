from tkinter import ttk, StringVar, Entry, Frame, Label, Spinbox, N, E, W, X, LEFT, RIGHT
import gui.widgets as widgets

def multiworld_page(parent,settings):
    # Multiworld
    self = ttk.Frame(parent)

    # Multiworld options
    self.widgets = {}

    ## Number of Worlds
    key = "worlds"
    self.widgets[key] = widgets.make_widget(
      self,
      "spinbox",
      self,
      "Worlds",
      None,
      {"label": {"side": LEFT}, "spinbox": {"side": RIGHT}}
    )
    self.widgets[key].pack(side=LEFT, anchor=N)

    ## List of Player Names
    namesFrame = Frame(self)
    namesLabel = Label(namesFrame, text='Player names')
    self.namesVar = StringVar(value=settings["names"])
    def saveMultiNames(caller,_,mode):
        settings["names"] = self.namesVar.get()
    self.namesVar.trace_add("write",saveMultiNames)
    namesEntry = Entry(namesFrame, textvariable=self.namesVar)
    namesLabel.pack(side=LEFT)
    namesEntry.pack(side=LEFT, fill=X, expand=True)
    namesFrame.pack(anchor=N, fill=X, expand=True)

    return self,settings
