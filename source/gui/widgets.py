from tkinter import Checkbutton, Entry, Frame, IntVar, Label, OptionMenu, Spinbox, StringVar, RIGHT, X

class Empty():
    pass

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

def make_checkbox(self, parent, label, storageVar, manager, managerAttrs):
    self = Frame(parent, name="checkframe-" + label.lower())
    self.storageVar = storageVar
    self.checkbox = Checkbutton(self, text=label, variable=self.storageVar, name="checkbox-" + label.lower())
    if managerAttrs is not None:
        self.checkbox.pack(managerAttrs)
    else:
        self.checkbox.pack()
    return self

def make_selectbox(self, parent, label, options, storageVar, manager, managerAttrs):
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
    if managerAttrs is not None and "label" in managerAttrs:
        self.label.pack(managerAttrs["label"])
    else:
        self.label.pack()
    self.selectbox = OptionMenu(self, self.labelVar, *options.keys())
    self.selectbox.config(width=20)
    self.labelVar.set(managerAttrs["default"] if "default" in managerAttrs else list(options.keys())[0])
    if managerAttrs is not None and "selectbox" in managerAttrs:
        self.selectbox.pack(managerAttrs["selectbox"])
    else:
        self.selectbox.pack()
    return self

def make_spinbox(self, parent, label, storageVar, manager, managerAttrs):
    self = Frame(parent, name="spinframe-" + label.lower())
    self.storageVar = storageVar
    self.label = Label(self, text=label)
    if managerAttrs is not None and "label" in managerAttrs:
        self.label.pack(managerAttrs["label"])
    else:
        self.label.pack()
    fromNum = 1
    toNum = 100
    if "spinbox" in managerAttrs:
        if "from" in managerAttrs:
            fromNum = managerAttrs["spinbox"]["from"]
        if "to" in managerAttrs:
            toNum = managerAttrs["spinbox"]["to"]
    self.spinbox = mySpinbox(self, from_=fromNum, to=toNum, width=5, textvariable=self.storageVar, name="spinbox-" + label.lower())
    if managerAttrs is not None and "spinbox" in managerAttrs:
        self.spinbox.pack(managerAttrs["spinbox"])
    else:
        self.spinbox.pack()
    return self

def make_textbox(self, parent, label, storageVar, manager, managerAttrs):
    widget = Empty()
    widget.storageVar = storageVar
    widget.label = Label(parent, text=label)
    widget.textbox = Entry(parent, justify=RIGHT, textvariable=widget.storageVar, width=3)
    if "default" in managerAttrs:
        widget.storageVar.set(managerAttrs["default"])

    # grid
    if manager == "grid":
        widget.label.grid(managerAttrs["label"] if managerAttrs is not None and "label" in managerAttrs else None, row=parent.thisRow, column=parent.thisCol)
        parent.thisCol += 1
        widget.textbox.grid(managerAttrs["textbox"] if managerAttrs is not None and "textbox" in managerAttrs else None, row=parent.thisRow, column=parent.thisCol)
        parent.thisRow += 1
        parent.thisCol = 0

    # pack
    elif manager == "pack":
        widget.label.pack(managerAttrs["label"] if managerAttrs is not None and "label" in managerAttrs else None)
        widget.textbox.pack(managerAttrs["textbox"] if managerAttrs is not None and "textbox" in managerAttrs else None)
    return widget


def make_widget(self, type, parent, label, storageVar=None, manager=None, managerAttrs=dict(), options=None):
    widget = None
    if manager is None:
        manager = "pack"
    thisStorageVar = storageVar
    if isinstance(storageVar,str):
        if storageVar == "int" or storageVar == "integer":
            thisStorageVar = IntVar()
        elif storageVar == "str" or storageVar == "string":
            thisStorageVar = StringVar()

    if type == "checkbox":
        if thisStorageVar is None:
            thisStorageVar = IntVar()
        widget = make_checkbox(self, parent, label, thisStorageVar, manager, managerAttrs)
    elif type == "selectbox":
        if thisStorageVar is None:
            thisStorageVar = StringVar()
        widget = make_selectbox(self, parent, label, options, thisStorageVar, manager, managerAttrs)
    elif type == "spinbox":
        if thisStorageVar is None:
            thisStorageVar = StringVar()
        widget = make_spinbox(self, parent, label, thisStorageVar, manager, managerAttrs)
    elif type == "textbox":
        if thisStorageVar is None:
            thisStorageVar = StringVar()
        widget = make_textbox(self, parent, label, thisStorageVar, manager, managerAttrs)
    widget.type = type
    return widget

def make_widget_from_dict(self, defn, parent):
    type = defn["type"] if "type" in defn else None
    label = defn["label"]["text"] if "label" in defn and "text" in defn["label"] else ""
    manager = defn["manager"] if "manager" in defn else None
    managerAttrs = defn["managerAttrs"] if "managerAttrs" in defn else None
    options = defn["options"] if "options" in defn else None
    widget = make_widget(self, type, parent, label, None, manager, managerAttrs, options)
    return widget

def make_widgets_from_dict(self, defns, parent):
    widgets = {}
    for key,defn in defns.items():
        widgets[key] = make_widget_from_dict(self, defn, parent)
    return widgets   
