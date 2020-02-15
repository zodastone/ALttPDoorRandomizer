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
    key = "names"
    self.widgets[key] = Frame(self)
    self.widgets[key].label = Label(self.widgets[key], text='Player names')
    self.widgets[key].storageVar = StringVar(value=settings["names"])
    def saveMultiNames(caller,_,mode):
        settings["names"] = self.widgets[key].storageVar.get()
    self.widgets[key].storageVar.trace_add("write",saveMultiNames)
    self.widgets[key].textbox = Entry(self.widgets[key], textvariable=self.widgets[key].storageVar)
    self.widgets[key].label.pack(side=LEFT)
    self.widgets[key].textbox.pack(side=LEFT, fill=X, expand=True)
    self.widgets[key].pack(anchor=N, fill=X, expand=True)

    return self,settings
