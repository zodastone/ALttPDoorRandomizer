from tkinter import Checkbutton, Entry, Frame, IntVar, Label, OptionMenu, StringVar

def make_checkbox(self, parent, label, storageVar, packAttrs):
    self = Frame(parent)
    self.storageVar = storageVar
    self.checkbox = Checkbutton(self, text=label, variable=self.storageVar)
    self.checkbox.pack(packAttrs)
    return self

def make_selectbox(self, parent, label, options, storageVar, packAttrs):
    def change_storage(*args):
        self.storageVar.set(options[self.labelVar.get()])
    def change_selected(*args):
        keys = options.keys()
        vals = options.values()
        keysList = list(keys)
        valsList = list(vals)
        self.labelVar.set(keysList[valsList.index(str(self.storageVar.get()))])
    self = Frame(parent)
    self.storageVar = storageVar
    self.storageVar.trace_add("write",change_selected)
    self.labelVar = StringVar()
    self.labelVar.trace_add("write",change_storage)
    self.label = Label(self, text=label)
    self.label.pack(packAttrs["label"])
    self.selectbox = OptionMenu(self, self.labelVar, *options.keys())
    self.labelVar.set(packAttrs["default"] if "default" in packAttrs else list(options.keys())[0])
    self.selectbox.pack(packAttrs["selectbox"])
    return self

def make_textbox(self, parent, label, storageVar, packAttrs):
    self = Frame(parent)
    self.storageVar = storageVar
    self.label = Label(self, text=label)
    self.label.pack(packAttrs["label"])
    self.textbox = Entry(self)
    self.textbox.pack(packAttrs["textbox"])
    return self

def make_widget(self, type, parent, label, storageVar=None, packAttrs=dict(), options=None):
    widget = None
    thisStorageVar = None
    if isinstance(storageVar,str):
        if storageVar == "int" or storageVar == "integer":
            thisStorageVar = IntVar()
        elif storageVar == "str" or storageVar == "string":
            thisStorageVar = StringVar()

    if type == "checkbox":
        if thisStorageVar is None:
            thisStorageVar = IntVar()
        widget = make_checkbox(self, parent, label, thisStorageVar, packAttrs)
    elif type == "selectbox":
        if thisStorageVar is None:
            thisStorageVar = StringVar()
        widget = make_selectbox(self, parent, label, options, thisStorageVar, packAttrs)
    elif type == "textbox":
        if thisStorageVar is None:
            thisStorageVar = StringVar()
        widget = make_textbox(self, parent, label, thisStorageVar, packAttrs)
    return widget
