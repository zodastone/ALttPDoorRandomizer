from tkinter import ttk, StringVar, Entry, Frame, Label, N, E, W, LEFT, RIGHT, X
import gui.widgets as widgets

def custom_page(top,parent):
    # Custom Item Pool
    self = ttk.Frame(parent)

    def validation(P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
    vcmd=(self.register(validation), '%P')

    # Custom Item Pool options
    self.customWidgets = {}

    itemList1 = Frame(self)
    itemList2 = Frame(self)
    itemList3 = Frame(self)
    itemList4 = Frame(self)
    itemList5 = Frame(self)

    currentList = itemList1

    myDict = {
      # Bow
      "bow": {
        "type": "textbox",
        "label": {
          "text": "Bow"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,53) },
          "textbox": { "side": RIGHT },
          "default": 0
        }
      },
      # Progressive Bow
      "progressivebow": {
        "type": "textbox",
        "label": {
          "text": "Prog.Bow"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,25) },
          "textbox": { "side": RIGHT },
          "default": 2
        }
      },
      # Boomerang
      "boomerang": {
        "type": "textbox",
        "label": {
          "text": "B.Boomerang"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,4) },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      },
      # Boomerang
      "redmerang": {
        "type": "textbox",
        "label": {
          "text": "M.Boomerang"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      },
      # Hookshot
      "hookshot": {
        "type": "textbox",
        "label": {
          "text": "Hookshot"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,24) },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      },
      # Mushroom
      "mushroom": {
        "type": "textbox",
        "label": {
          "text": "Mushroom"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,17) },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      },
      # Powder
      "powder": {
        "type": "textbox",
        "label": {
          "text": "Magic Powder"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      },
      # Fire Rod
      "firerod": {
        "type": "textbox",
        "label": {
          "text": "Fire Rod"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,33) },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      },
      # Ice Rod
      "icerod": {
        "type": "textbox",
        "label": {
          "text": "Ice Rod"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,37) },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      },
      # Bombos
      "bombos": {
        "type": "textbox",
        "label": {
          "text": "Bombos"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,32) },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      },
      # Ether
      "ether": {
        "type": "textbox",
        "label": {
          "text": "Ether"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,49) },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      },
      # Quake
      "quake": {
        "type": "textbox",
        "label": {
          "text": "Quake"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,42) },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      },
      # Lamp
      "lamp": {
        "type": "textbox",
        "label": {
          "text": "Lamp"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,46) },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      },
      # Hammer
      "hammer": {
        "type": "textbox",
        "label": {
          "text": "Hammer"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,29) },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      },
      # Shovel
      "shovel": {
        "type": "textbox",
        "label": {
          "text": "Shovel"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,41) },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      }
    }
    dictWidgets = widgets.make_widgets_from_dict(self, myDict, currentList)
    for key in dictWidgets:
        self.customWidgets[key] = dictWidgets[key]
        self.customWidgets[key].pack()

    currentList = itemList2

    myDict = {
      # Flute
      "flute": {
        "type": "textbox",
        "label": {
          "text": "Flute"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,58) },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      },
      # Bug Net
      "bugnet": {
        "type": "textbox",
        "label": {
          "text": "Bug Net"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,41) },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      },
      # Book of Mudora
      "book": {
        "type": "textbox",
        "label": {
          "text": "Book"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,57) },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      },
      # Bottle
      "bottle": {
        "type": "textbox",
        "label": {
          "text": "Bottle"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,53) },
          "textbox": { "side": RIGHT },
          "default": 4
        }
      },
      # Cane of Somaria
      "somaria": {
        "type": "textbox",
        "label": {
          "text": "C.Somaria"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,30) },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      },
      # Cane of Byrna
      "byrna": {
        "type": "textbox",
        "label": {
          "text": "C.Byrna"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,43) },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      },
      # Magic Cape
      "cape": {
        "type": "textbox",
        "label": {
          "text": "Magic Cape"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,21) },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      },
      # Magic Mirror
      "mirror": {
        "type": "textbox",
        "label": {
          "text": "Magic Mirror"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,15) },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      },
      # Pegasus Boots
      "boots": {
        "type": "textbox",
        "label": {
          "text": "Pegasus Boots"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,8) },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      },
      # Power Glove
      "powerglove": {
        "type": "textbox",
        "label": {
          "text": "Power Glove"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,18) },
          "textbox": { "side": RIGHT },
          "default": 0
        }
      },
      # Titan's Mitt
      "titansmitt": {
        "type": "textbox",
        "label": {
          "text": "Titan\'s Mitt"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,25) },
          "textbox": { "side": RIGHT },
          "default": 0
        }
      },
      # Progressive Glove
      "progressiveglove": {
        "type": "textbox",
        "label": {
          "text": "Prog.Glove"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,26) },
          "textbox": { "side": RIGHT },
          "default": 2
        }
      },
      # Flippers
      "flippers": {
        "type": "textbox",
        "label": {
          "text": "Flippers"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,43) },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      },
      # Moon Pearl
      "pearl": {
        "type": "textbox",
        "label": {
          "text": "Moon Pearl"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,23) },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      },
      # Piece of Heart
      "heartpiece": {
        "type": "textbox",
        "label": {
          "text": "Piece of Heart"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,10) },
          "textbox": { "side": RIGHT },
          "default": 24
        }
      }
    }
    dictWidgets = widgets.make_widgets_from_dict(self, myDict, currentList)
    for key in dictWidgets:
        self.customWidgets[key] = dictWidgets[key]
        self.customWidgets[key].pack()

    currentList = itemList3

    myDict = {
      # Heart Container
      "heartcontainer": {
        "type": "textbox",
        "label": {
          "text": "Heart Container"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT },
          "textbox": { "side": RIGHT },
          "default": 10
        }
      },
      # Sanctuary Heart
      "sancheart": {
        "type": "textbox",
        "label": {
          "text": "Sanctuary Heart"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      },
      # Fighters' Sword
      "sword1": {
        "type": "textbox",
        "label": {
          "text": "Sword 1"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,42) },
          "textbox": { "side": RIGHT },
          "default": 0
        }
      },
      # Master Sword
      "sword2": {
        "type": "textbox",
        "label": {
          "text": "Sword 2"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,42) },
          "textbox": { "side": RIGHT },
          "default": 0
        }
      },
      # Tempered Sword
      "sword3": {
        "type": "textbox",
        "label": {
          "text": "Sword 3"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,42) },
          "textbox": { "side": RIGHT },
          "default": 0
        }
      },
      # Gold Sword
      "sword4": {
        "type": "textbox",
        "label": {
          "text": "Sword 4"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,42) },
          "textbox": { "side": RIGHT },
          "default": 0
        }
      },
      # Progressive Sword
      "progressivesword": {
        "type": "textbox",
        "label": {
          "text": "Prog.Sword"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,23) },
          "textbox": { "side": RIGHT },
          "default": 4
        }
      },
      # Fighters' Shield
      "shield1": {
        "type": "textbox",
        "label": {
          "text": "Shield 1"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,43) },
          "textbox": { "side": RIGHT },
          "default": 0
        }
      },
      # Fire Shield
      "shield2": {
        "type": "textbox",
        "label": {
          "text": "Shield 2"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,43) },
          "textbox": { "side": RIGHT },
          "default": 0
        }
      },
      # Mirror Shield
      "shield3": {
        "type": "textbox",
        "label": {
          "text": "Shield 3"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,43) },
          "textbox": { "side": RIGHT },
          "default": 0
        }
      },
      # Progressive Shield
      "progressiveshield": {
        "type": "textbox",
        "label": {
          "text": "Prog.Shield"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,24) },
          "textbox": { "side": RIGHT },
          "default": 3
        }
      },
      # Blue Mail
      "mail2": {
        "type": "textbox",
        "label": {
          "text": "Blue Mail"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,35) },
          "textbox": { "side": RIGHT },
          "default": 0
        }
      },
      # Red Mail
      "mail3": {
        "type": "textbox",
        "label": {
          "text": "Red Mail"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,38) },
          "textbox": { "side": RIGHT },
          "default": 0
        }
      },
      # Progressive Mail
      "progressivemail": {
        "type": "textbox",
        "label": {
          "text": "Prog.Mail"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,33) },
          "textbox": { "side": RIGHT },
          "default": 2
        }
      },
      # Half Magic
      "halfmagic": {
        "type": "textbox",
        "label": {
          "text": "Half Magic"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,26) },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      }
    }
    dictWidgets = widgets.make_widgets_from_dict(self, myDict, currentList)
    for key in dictWidgets:
        self.customWidgets[key] = dictWidgets[key]
        self.customWidgets[key].pack()

    currentList = itemList4

    myDict = {
      # Quarter Magic
      "quartermagic": {
        "type": "textbox",
        "label": {
          "text": "Quarter Magic"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT },
          "textbox": { "side": RIGHT },
          "default": 0
        }
      },
      # Bomb Capacity +5
      "bombsplus5": {
        "type": "textbox",
        "label": {
          "text": "Bomb C.+5"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (1,15) },
          "textbox": { "side": RIGHT },
          "default": 0
        }
      },
      # Bomb Capacity +10
      "bombsplus10": {
        "type": "textbox",
        "label": {
          "text": "Bomb C.+10"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,10) },
          "textbox": { "side": RIGHT },
          "default": 0
        }
      },
      # Arrow Capacity + 5
      "arrowsplus5": {
        "type": "textbox",
        "label": {
          "text": "Arrow C.+5"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,16) },
          "textbox": { "side": RIGHT },
          "default": 0
        }
      },
      # Arrow Capacity +10
      "arrowsplus10": {
        "type": "textbox",
        "label": {
          "text": "Arrow C.+10"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,10) },
          "textbox": { "side": RIGHT },
          "default": 0
        }
      },
      # Arrow (1)
      "arrow1": {
        "type": "textbox",
        "label": {
          "text": "Arrow (1)"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,27) },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      },
      # Arrow (10)
      "arrow10": {
        "type": "textbox",
        "label": {
          "text": "Arrow (10)"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,21) },
          "textbox": { "side": RIGHT },
          "default": 12
        }
      },
      # Bomb (1)
      "bomb1": {
        "type": "textbox",
        "label": {
          "text": "Bomb (1)"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,27) },
          "textbox": { "side": RIGHT },
          "default": 0
        }
      },
      # Bomb (3)
      "bomb3": {
        "type": "textbox",
        "label": {
          "text": "Bomb (3)"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,27) },
          "textbox": { "side": RIGHT },
          "default": 13
        }
      },
      # Bomb (10)
      "bomb10": {
        "type": "textbox",
        "label": {
          "text": "Bomb (10)"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,21) },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      },
      # Rupee (1)
      "rupee1": {
        "type": "textbox",
        "label": {
          "text": "Rupee (1)"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,25) },
          "textbox": { "side": RIGHT },
          "default": 2
        }
      },
      # Rupee (5)
      "rupee5": {
        "type": "textbox",
        "label": {
          "text": "Rupee (5)"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,25) },
          "textbox": { "side": RIGHT },
          "default": 4
        }
      },
      # Rupee (20)
      "rupee20": {
        "type": "textbox",
        "label": {
          "text": "Rupee (20)"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,19) },
          "textbox": { "side": RIGHT },
          "default": 28
        }
      },
      # Rupee (50)
      "rupee50": {
        "type": "textbox",
        "label": {
          "text": "Rupee (50)"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,19) },
          "textbox": { "side": RIGHT },
          "default": 7
        }
      },
      # Rupee (100)
      "rupee100": {
        "type": "textbox",
        "label": {
          "text": "Rupee (100)"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,13) },
          "textbox": { "side": RIGHT },
          "default": 1
        }
      }
    }
    dictWidgets = widgets.make_widgets_from_dict(self, myDict, currentList)
    for key in dictWidgets:
        self.customWidgets[key] = dictWidgets[key]
        self.customWidgets[key].pack()

    currentList = itemList5

    myDict = {
      # Rupee (300)
      "rupee300": {
        "type": "textbox",
        "label": {
          "text": "Rupee (300)"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,54) },
          "textbox": { "side": RIGHT },
          "default": 5
        }
      },
      # Blue Clock
      "blueclock": {
        "type": "textbox",
        "label": {
          "text": "Blue Clock"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,60) },
          "textbox": { "side": RIGHT },
          "default": 0
        }
      },
      # Green Clock
      "greenclock": {
        "type": "textbox",
        "label": {
          "text": "Green Clock"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,52) },
          "textbox": { "side": RIGHT },
          "default": 0
        }
      },
      # Red Clock
      "redclock": {
        "type": "textbox",
        "label": {
          "text": "Red Clock"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,63) },
          "textbox": { "side": RIGHT },
          "default": 0
        }
      },
      # Silver Arrows Upgrade
      "silversupgrade": {
        "type": "textbox",
        "label": {
          "text": "Silver Arrows Upgrade"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT },
          "textbox": { "side": RIGHT },
          "default": 0
        }
      },
      # Generic Keys
      "generickeys": {
        "type": "textbox",
        "label": {
          "text": "Generic Keys"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,49) },
          "textbox": { "side": RIGHT },
          "default": 0
        }
      },
      # Triforce Pieces
      "triforcepieces": {
        "type": "textbox",
        "label": {
          "text": "Triforce Pieces"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,40) },
          "textbox": { "side": RIGHT },
          "default": 0
        }
      },
      # Triforce Pieces Goal
      "triforcepiecesgoal": {
        "type": "textbox",
        "label": {
          "text": "Triforce Pieces Goal"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,13) },
          "textbox": { "side": RIGHT },
          "default": 0
        }
      },
      # Triforce (win game)
      "triforce": {
        "type": "textbox",
        "label": {
          "text": "Triforce (win game)"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,13) },
          "textbox": { "side": RIGHT },
          "default": 0
        }
      },
      # Rupoor
      "rupoor": {
        "type": "textbox",
        "label": {
          "text": "Rupoor"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,77) },
          "textbox": { "side": RIGHT },
          "default": 0
        }
      },
      # Rupoor Cost
      "rupoorcost": {
        "type": "textbox",
        "label": {
          "text": "Rupoor Cost"
        },
        "packAttrs": {
          "label": { "anchor": W, "side": LEFT, "padx": (0,50) },
          "textbox": { "side": RIGHT },
          "default": 10
        }
      }
    }
    dictWidgets = widgets.make_widgets_from_dict(self, myDict, currentList)
    for key in dictWidgets:
        self.customWidgets[key] = dictWidgets[key]
        self.customWidgets[key].pack()

    itemList1.pack(side=LEFT, padx=(0,0))
    itemList2.pack(side=LEFT, padx=(0,0))
    itemList3.pack(side=LEFT, padx=(0,0))
    itemList4.pack(side=LEFT, padx=(0,0))
    itemList5.pack(side=LEFT, padx=(0,0), anchor=N)

    return self
