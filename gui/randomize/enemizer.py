import os
from tkinter import ttk, filedialog, IntVar, StringVar, Button, Checkbutton, Entry, Frame, Label, LabelFrame, OptionMenu, N, E, W, LEFT, RIGHT, X
import gui.widgets as widgets

def enemizer_page(parent,settings):
    # Enemizer
    self = ttk.Frame(parent)

    # Enemizer options
    self.widgets = {}

    myDict = {
      ## Pot Shuffle
      "potshuffle": {
        "type": "checkbox",
        "label": {
          "text": "Pot Shuffle"
        }
      }
    }
    dictWidgets = widgets.make_widgets_from_dict(self, myDict, self)
    for key in dictWidgets:
        self.widgets[key] = dictWidgets[key]
        self.widgets[key].pack(anchor=W)

    ## Enemizer CLI Path
    enemizerPathFrame = Frame(self)
    enemizerCLIlabel = Label(enemizerPathFrame, text="EnemizerCLI path: ")
    enemizerCLIlabel.pack(side=LEFT)
    self.enemizerCLIpathVar = StringVar(value=settings["enemizercli"])
    def saveEnemizerPath(caller,_,mode):
        settings["enemizercli"] = self.enemizerCLIpathVar.get()
    self.enemizerCLIpathVar.trace_add("write",saveEnemizerPath)
    enemizerCLIpathEntry = Entry(enemizerPathFrame, textvariable=self.enemizerCLIpathVar)
    enemizerCLIpathEntry.pack(side=LEFT, fill=X, expand=True)
    def EnemizerSelectPath():
        path = filedialog.askopenfilename(filetypes=[("EnemizerCLI executable", "*EnemizerCLI*")], initialdir=os.path.join("."))
        if path:
            self.enemizerCLIpathVar.set(path)
            settings["enemizercli"] = path
    enemizerCLIbrowseButton = Button(enemizerPathFrame, text='...', command=EnemizerSelectPath)
    enemizerCLIbrowseButton.pack(side=LEFT)
    enemizerPathFrame.pack(fill=X, expand=True)

    leftEnemizerFrame = Frame(self)
    rightEnemizerFrame = Frame(self)
    leftEnemizerFrame.pack(side=LEFT, anchor=N)
    rightEnemizerFrame.pack(side=RIGHT, anchor=N)

    myDict = {
      ## Randomize Enemies
      "enemyshuffle": {
        "type": "selectbox",
        "label": {
          "text": "Enemy Shuffle"
        },
        "packAttrs": {
          "label": { "side": LEFT },
          "selectbox": { "side": RIGHT }
        },
        "options": {
          "Vanilla": "none",
          "Shuffled": "shuffled",
          "Chaos": "chaos"
        }
      },
      ## Randomize Bosses
      "bossshuffle": {
        "type": "selectbox",
        "label": {
          "text": "Boss Shuffle"
        },
        "packAttrs": {
          "label": { "side": LEFT },
          "selectbox": { "side": RIGHT }
        },
        "options": {
          "Vanilla": "none",
          "Basic": "basic",
          "Shuffled": "shuffled",
          "Chaos": "chaos"
        }
      }
    }
    dictWidgets = widgets.make_widgets_from_dict(self, myDict, leftEnemizerFrame)
    for key in dictWidgets:
        self.widgets[key] = dictWidgets[key]
        self.widgets[key].pack(anchor=E)

    myDict = {
      ## Enemy Damage
      "enemydamage": {
        "type": "selectbox",
        "label": {
          "text": "Enemy Damage"
        },
        "packAttrs": {
          "label": { "side": LEFT },
          "selectbox": { "side": RIGHT }
        },
        "options": {
          "Vanilla": "default",
          "Shuffled": "shuffled",
          "Chaos": "chaos"
        }
      },
      ## Enemy Health
      "enemyhealth": {
        "type": "selectbox",
        "label": {
          "text": "Enemy Health"
        },
        "packAttrs": {
          "label": { "side": LEFT },
          "selectbox": { "side": RIGHT }
        },
        "options": {
          "Vanilla": "default",
          "Easy": "easy",
          "Normal": "normal",
          "Hard": "hard",
          "Expert": "expert"
        }
      }
    }
    dictWidgets = widgets.make_widgets_from_dict(self, myDict, rightEnemizerFrame)
    for key in dictWidgets:
        self.widgets[key] = dictWidgets[key]
        self.widgets[key].pack(anchor=E)

    return self,settings
