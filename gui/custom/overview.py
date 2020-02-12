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

    # Bow
    key = "bow"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Bow",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,53)}, "textbox": {"side": RIGHT}, "default": 0}
    )
    self.customWidgets[key].pack()

    # Progressive Bow
    key = "progressivebow"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Prog.Bow",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,25)}, "textbox": {"side": RIGHT}, "default": 2}
    )
    self.customWidgets[key].pack()

    # Boomerang
    key = "boomerang"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "B.Boomerang",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,4)}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    # Redmerang
    key = "redmerang"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "M.Boomerang",
      None,
      {"label": {"anchor": W, "side": LEFT}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    # Hookshot
    key = "hookshot"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Hookshot",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,24)}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    # Mushroom
    key = "mushroom"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Mushroom",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,17)}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    # Powder
    key = "powder"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Magic Powder",
      None,
      {"label": {"anchor": W, "side": LEFT}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    # Fire Rod
    key = "firerod"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Fire Rod",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,33)}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    # Ice Rod
    key = "icerod"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Ice Rod",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,37)}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    # Bombos
    key = "bombos"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Bombos",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,32)}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    # Ether
    key = "ether"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Ether",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,49)}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    # Quake
    key = "quake"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Quake",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,42)}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    # Lamp
    key = "lamp"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Lamp",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,46)}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    # Hammer
    key = "hammer"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Hammer",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,29)}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    # Shovel
    key = "shovel"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Shovel",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,41)}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    currentList = itemList2

    # Flute
    key = "flute"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Flute",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,58)}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    # Bug Net
    key = "bugnet"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Bug Net",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,41)}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    # Book of Mudora
    key = "book"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Book",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,57)}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    # Bottle
    key = "bottle"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Bottle",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,53)}, "textbox": {"side": RIGHT}, "default": 4}
    )
    self.customWidgets[key].pack()

    # Cane of Somaria
    key = "somaria"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "C.Somaria",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,30)}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    # Cane of Byrna
    key = "byrna"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "C.Byrna",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,43)}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    # Magic Cape
    key = "cape"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Magic Cape",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,21)}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    # Magic Mirror
    key = "mirror"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Magic Mirror",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,15)}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    # Pegasus Boots
    key = "boots"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Pegasus Boots",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,8)}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    # Power Glove
    key = "powerglove"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Power Glove",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,18)}, "textbox": {"side": RIGHT}, "default": 0}
    )
    self.customWidgets[key].pack()

    # Titan's Mitt
    key = "titansmitt"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Titan\'s Mitt",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,24)}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    # Progressive Glove
    key = "progressiveglove"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Prog.Glove",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,26)}, "textbox": {"side": RIGHT}, "default": 2}
    )
    self.customWidgets[key].pack()

    # Flippers
    key = "flippers"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Flippers",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,43)}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    # Moon Pearl
    key = "pearl"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Moon Pearl",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,23)}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    # Piece of Heart
    key = "heartpiece"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Piece of Heart",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,10)}, "textbox": {"side": RIGHT}, "default": 24}
    )
    self.customWidgets[key].pack()

    currentList = itemList3

    # Heart Container
    key = "heartcontainer"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Heart Container",
      None,
      {"label": {"anchor": W, "side": LEFT}, "textbox": {"side": RIGHT}, "default": 10}
    )
    self.customWidgets[key].pack()

    # Sanctuary Heart
    key = "sancheart"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Sanctuary Heart",
      None,
      {"label": {"anchor": W, "side": LEFT}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    # Fighters' Sword
    key = "sword1"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Sword 1",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,42)}, "textbox": {"side": RIGHT}, "default": 0}
    )
    self.customWidgets[key].pack()

    # Master Sword
    key = "sword2"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Sword 2",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,42)}, "textbox": {"side": RIGHT}, "default": 0}
    )
    self.customWidgets[key].pack()

    # Tempered Sword
    key = "sword3"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Sword 3",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,42)}, "textbox": {"side": RIGHT}, "default": 0}
    )
    self.customWidgets[key].pack()

    # Gold Sword
    key = "sword4"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Sword 4",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,42)}, "textbox": {"side": RIGHT}, "default": 0}
    )
    self.customWidgets[key].pack()

    # Progressive Sword
    key = "progressivesword"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Prog.Sword",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,23)}, "textbox": {"side": RIGHT}, "default": 4}
    )
    self.customWidgets[key].pack()

    # Fighters' Shield
    key = "shield1"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Shield 1",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,43)}, "textbox": {"side": RIGHT}, "default": 0}
    )
    self.customWidgets[key].pack()

    # Fire Shield
    key = "shield2"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Shield 2",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,43)}, "textbox": {"side": RIGHT}, "default": 0}
    )
    self.customWidgets[key].pack()

    # Mirror Shield
    key = "shield3"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Shield 3",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,43)}, "textbox": {"side": RIGHT}, "default": 0}
    )
    self.customWidgets[key].pack()

    # Progressive Shield
    key = "progressiveshield"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Prog.Shield",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,24)}, "textbox": {"side": RIGHT}, "default": 3}
    )
    self.customWidgets[key].pack()

    # Blue Mail
    key = "mail2"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Blue Mail",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,35)}, "textbox": {"side": RIGHT}, "default": 0}
    )
    self.customWidgets[key].pack()

    # Red Mail
    key = "mail3"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Red Mail",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,38)}, "textbox": {"side": RIGHT}, "default": 0}
    )
    self.customWidgets[key].pack()

    # Progressive Mail
    key = "progressivemail"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Prog.Mail",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,33)}, "textbox": {"side": RIGHT}, "default": 2}
    )
    self.customWidgets[key].pack()

    # Half Magic
    key = "halfmagic"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Half Magic",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,26)}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    currentList = itemList4

    # Quarter Magic
    key = "quartermagic"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Quarter Magic",
      None,
      {"label": {"anchor": W, "side": LEFT}, "textbox": {"side": RIGHT}, "default": 0}
    )
    self.customWidgets[key].pack()

    # Bomb Capacity +5
    key = "bombsplus5"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Bomb C.+5",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,16)}, "textbox": {"side": RIGHT}, "default": 0}
    )
    self.customWidgets[key].pack()

    # Bomb Capacity +10
    key = "bombsplus10"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Bomb C.+10",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,10)}, "textbox": {"side": RIGHT}, "default": 0}
    )
    self.customWidgets[key].pack()

    # Arrow Capacity +5
    key = "arrowsplus5"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Arrow C.+5",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,16)}, "textbox": {"side": RIGHT}, "default": 0}
    )
    self.customWidgets[key].pack()

    # Arrow Capacity +10
    key = "arrowsplus10"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Arrow C.+10",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,10)}, "textbox": {"side": RIGHT}, "default": 0}
    )
    self.customWidgets[key].pack()

    # Arrow (1)
    key = "arrow1"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Arrow (1)",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,27)}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    # Arrow (10)
    key = "arrow10"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Arrow (10)",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,21)}, "textbox": {"side": RIGHT}, "default": 12}
    )
    self.customWidgets[key].pack()

    # Bomb (1)
    key = "bomb1"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Bomb (1)",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,26)}, "textbox": {"side": RIGHT}, "default": 0}
    )
    self.customWidgets[key].pack()

    # Bomb (3)
    key = "bomb3"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Bomb (3)",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,25)}, "textbox": {"side": RIGHT}, "default": 13}
    )
    self.customWidgets[key].pack()

    # Bomb (10)
    key = "bomb10"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Bomb (10)",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,20)}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    # Rupee (1)
    key = "rupee1"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Rupee (1)",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,24)}, "textbox": {"side": RIGHT}, "default": 2}
    )
    self.customWidgets[key].pack()

    # Rupee (5)
    key = "rupee5"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Rupee (5)",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,24)}, "textbox": {"side": RIGHT}, "default": 4}
    )
    self.customWidgets[key].pack()

    # Rupee (20)
    key = "rupee20"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Rupee (20)",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,18)}, "textbox": {"side": RIGHT}, "default": 28}
    )
    self.customWidgets[key].pack()

    # Rupee (50)
    key = "rupee50"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Rupee (50)",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,18)}, "textbox": {"side": RIGHT}, "default": 7}
    )
    self.customWidgets[key].pack()

    # Rupee (100)
    key = "rupee100"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Rupee (100)",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,12)}, "textbox": {"side": RIGHT}, "default": 1}
    )
    self.customWidgets[key].pack()

    currentList = itemList5

    # Rupee (300)
    key = "rupee300"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Rupee (300)",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,54)}, "textbox": {"side": RIGHT}, "default": 5}
    )
    self.customWidgets[key].pack()

    # Blue Clock
    key = "blueclock"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Blue Clock",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,60)}, "textbox": {"side": RIGHT}, "default": 0}
    )
    self.customWidgets[key].pack()

    # Green Clock
    key = "greenclock"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Green Clock",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,52)}, "textbox": {"side": RIGHT}, "default": 0}
    )
    self.customWidgets[key].pack()

    # Red Clock
    key = "redclock"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Red Clock",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,63)}, "textbox": {"side": RIGHT}, "default": 0}
    )
    self.customWidgets[key].pack()

    # Silver Arrows Upgrade
    key = "silversupgrade"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Silver Arrows Upgrade",
      None,
      {"label": {"anchor": W, "side": LEFT}, "textbox": {"side": RIGHT}, "default": 0}
    )
    self.customWidgets[key].pack()

    # Generic Keys
    key = "generickeys"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Generic Keys",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,49)}, "textbox": {"side": RIGHT}, "default": 0}
    )
    self.customWidgets[key].pack()

    # Triforce Pieces
    key = "triforcepieces"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Triforce Pieces",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,40)}, "textbox": {"side": RIGHT}, "default": 0}
    )
    self.customWidgets[key].pack()

    # Triforce Pieces Required
    key = "triforcepiecesgoal"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Triforce Pieces Required",
      None,
      {"label": {"anchor": W, "side": LEFT}, "textbox": {"side": RIGHT}, "default": 0}
    )
    self.customWidgets[key].pack()

    # Triforce (win game)
    key = "triforce"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Triforce (win game)",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,13)}, "textbox": {"side": RIGHT}, "default": 0}
    )
    self.customWidgets[key].pack()

    # Rupoor
    key = "rupoor"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Rupoor",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,77)}, "textbox": {"side": RIGHT}, "default": 0}
    )
    self.customWidgets[key].pack()

    # Rupoor Cost
    key = "rupoorcost"
    self.customWidgets[key] = widgets.make_widget(self,"textbox",currentList,
      "Rupoor Cost",
      None,
      {"label": {"anchor": W, "side": LEFT, "padx": (0,50)}, "textbox": {"side": RIGHT}, "default": 10}
    )
    self.customWidgets[key].pack()

    itemList1.pack(side=LEFT, padx=(0,0))
    itemList2.pack(side=LEFT, padx=(0,0))
    itemList3.pack(side=LEFT, padx=(0,0))
    itemList4.pack(side=LEFT, padx=(0,0))
    itemList5.pack(side=LEFT, padx=(0,0), anchor=N)

    return self
