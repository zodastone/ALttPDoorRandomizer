from tkinter import Checkbutton, Entry, Frame, IntVar, Label, OptionMenu, Spinbox, StringVar, RIGHT

class mySpinbox(Spinbox):
    def __init__(self, *args, **kwargs):
        Spinbox.__init__(self, *args, **kwargs)
        self.bind('<MouseWheel>', self.mouseWheel)
        self.bind('<Button-4>', self.mouseWheel)
        self.bind('<Button-5>', self.mouseWheel)

    def mouseWheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.invoke('buttondown')
        elif event.num == 4 or event.delta == 120:
            self.invoke('buttonup')

def make_checkbox(self, parent, label, storageVar, packAttrs):
    self = Frame(parent, name="checkframe-" + label.lower())
    self.storageVar = storageVar
    self.checkbox = Checkbutton(self, text=label, variable=self.storageVar, name="checkbox-" + label.lower())
    if packAttrs is not None:
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
    self = Frame(parent, name="selectframe-" + label.lower())
    self.storageVar = storageVar
    self.storageVar.trace_add("write",change_selected)
    self.labelVar = StringVar()
    self.labelVar.trace_add("write",change_storage)
    self.label = Label(self, text=label)
    if packAttrs is not None and "label" in packAttrs:
        self.label.pack(packAttrs["label"])
    self.selectbox = OptionMenu(self, self.labelVar, *options.keys())
    self.selectbox.config(width=20)
    self.labelVar.set(packAttrs["default"] if "default" in packAttrs else list(options.keys())[0])
    if packAttrs is not None and "selectbox" in packAttrs:
        self.selectbox.pack(packAttrs["selectbox"])
    return self

def make_spinbox(self, parent, label, storageVar, packAttrs):
    self = Frame(parent, name="spinframe-" + label.lower())
    self.storageVar = storageVar
    self.label = Label(self, text=label)
    if packAttrs is not None and "label" in packAttrs:
        self.label.pack(packAttrs["label"])
    fromNum = 1
    toNum = 100
    if "spinbox" in packAttrs:
        if "from" in packAttrs:
            fromNum = packAttrs["spinbox"]["from"]
        if "to" in packAttrs:
            toNum = packAttrs["spinbox"]["to"]
    self.spinbox = mySpinbox(self, from_=fromNum, to=toNum, width=5, textvariable=self.storageVar, name="spinbox-" + label.lower())
    if packAttrs is not None and "spinbox" in packAttrs:
        self.spinbox.pack(packAttrs["spinbox"])
    return self

def make_textbox(self, parent, label, storageVar, packAttrs):
    self = Frame(parent)
    self.storageVar = storageVar
    self.label = Label(self, text=label)
    if packAttrs is not None and "label" in packAttrs:
        self.label.pack(packAttrs["label"])
    self.textbox = Entry(self, justify=RIGHT, textvariable=self.storageVar, width=3)
    if "default" in packAttrs:
        self.storageVar.set(packAttrs["default"])
    if packAttrs is not None and "textbox" in packAttrs:
        self.textbox.pack(packAttrs["textbox"])
    return self


def make_widget(self, type, parent, label, storageVar=None, packAttrs=dict(), options=None):
    widget = None
    thisStorageVar = storageVar
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
    elif type == "spinbox":
        if thisStorageVar is None:
            thisStorageVar = StringVar()
        widget = make_spinbox(self, parent, label, thisStorageVar, packAttrs)
    elif type == "textbox":
        if thisStorageVar is None:
            thisStorageVar = StringVar()
        widget = make_textbox(self, parent, label, thisStorageVar, packAttrs)
    return widget
