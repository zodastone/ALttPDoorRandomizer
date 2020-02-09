from tkinter import ttk, filedialog, messagebox, IntVar, StringVar, Button, Checkbutton, Entry, Frame, Label, OptionMenu, E, W, LEFT, RIGHT, X, BOTTOM
from AdjusterMain import adjust
from argparse import Namespace
from classes.SpriteSelector import SpriteSelector
import logging

def adjust_page(top,parent,working_dirs):
    self = ttk.Frame(parent)

    # Disable BGM
    self.disableMusicVar2 = IntVar()
    disableMusicCheckbutton2 = Checkbutton(self, text="Disable music", variable=self.disableMusicVar2)
    disableMusicCheckbutton2.pack(anchor=W)

    # L/R Quickswap
    self.quickSwapVar2 = IntVar()
    quickSwapCheckbutton2 = Checkbutton(self, text="L/R Quickswapping", variable=self.quickSwapVar2)
    quickSwapCheckbutton2.pack(anchor=W)

    selectOptionsFrame = Frame(self)
    leftAdjustFrame = Frame(selectOptionsFrame)
    rightAdjustFrame = Frame(selectOptionsFrame)
    bottomAdjustFrame = Frame(self)
    selectOptionsFrame.pack(fill=X, expand=True)
    leftAdjustFrame.pack(side=LEFT)
    rightAdjustFrame.pack(side=RIGHT)
    bottomAdjustFrame.pack(fill=X, expand=True)

    # Heart Color
    heartcolorFrame2 = Frame(leftAdjustFrame)
    heartcolorLabel2 = Label(heartcolorFrame2, text='Heart color')
    heartcolorLabel2.pack(side=LEFT)
    self.heartcolorVar2 = StringVar()
    self.heartcolorVar2.set('red')
    heartcolorOptionMenu2 = OptionMenu(heartcolorFrame2, self.heartcolorVar2, 'red', 'blue', 'green', 'yellow', 'random')
    heartcolorOptionMenu2.pack(side=RIGHT)
    heartcolorFrame2.pack(anchor=E)

    # Heart Beep Speed
    heartbeepFrame2 = Frame(leftAdjustFrame)
    heartbeepLabel2 = Label(heartbeepFrame2, text='Heart Beep sound rate')
    heartbeepLabel2.pack(side=LEFT)
    self.heartbeepVar2 = StringVar()
    self.heartbeepVar2.set('normal')
    heartbeepOptionMenu2 = OptionMenu(heartbeepFrame2, self.heartbeepVar2, 'double', 'normal', 'half', 'quarter', 'off')
    heartbeepOptionMenu2.pack(side=RIGHT)
    heartbeepFrame2.pack(anchor=E)

    # Sprite Selection
    self.spriteNameVar2 = StringVar()
    spriteDialogFrame2 = Frame(leftAdjustFrame)
    baseSpriteLabel2 = Label(spriteDialogFrame2, text='Sprite:')
    self.spriteNameVar2.set('(unchanged)')
    spriteEntry2 = Label(spriteDialogFrame2, textvariable=self.spriteNameVar2)

    def set_sprite(sprite_param):
        if sprite_param is None or not sprite_param.valid:
            sprite = None
            self.spriteNameVar2.set('(unchanged)')
        else:
            sprite = sprite_param
            self.spriteNameVar2.set(sprite.name)

    def SpriteSelectAdjuster():
        SpriteSelector(parent, set_sprite, adjuster=True)

    spriteSelectButton2 = Button(spriteDialogFrame2, text='...', command=SpriteSelectAdjuster)

    baseSpriteLabel2.pack(side=LEFT)
    spriteEntry2.pack(side=LEFT)
    spriteSelectButton2.pack(side=LEFT)
    spriteDialogFrame2.pack(anchor=E)

    # Menu Speed
    fastMenuFrame2 = Frame(rightAdjustFrame)
    fastMenuLabel2 = Label(fastMenuFrame2, text='Menu speed')
    fastMenuLabel2.pack(side=LEFT)
    self.fastMenuVar2 = StringVar()
    self.fastMenuVar2.set("normal")
    fastMenuOptionMenu2 = OptionMenu(fastMenuFrame2, self.fastMenuVar2, 'normal', 'instant', 'double', 'triple', 'quadruple', 'half')
    fastMenuOptionMenu2.pack(side=RIGHT)
    fastMenuFrame2.pack(anchor=E)

    owPalettesFrame2 = Frame(rightAdjustFrame)
    owPalettesLabel2 = Label(owPalettesFrame2, text='Overworld palettes')
    owPalettesLabel2.pack(side=LEFT)
    self.owPalettesVar2 = StringVar()
    self.owPalettesVar2.set("default")
    owPalettesOptionMenu2 = OptionMenu(owPalettesFrame2, self.owPalettesVar2, 'default', 'random', 'blackout')
    owPalettesOptionMenu2.pack(side=RIGHT)
    owPalettesFrame2.pack(anchor=E)

    uwPalettesFrame2 = Frame(rightAdjustFrame)
    uwPalettesLabel2 = Label(uwPalettesFrame2, text='Dungeon palettes')
    uwPalettesLabel2.pack(side=LEFT)
    self.uwPalettesVar2 = StringVar()
    self.uwPalettesVar2.set("default")
    uwPalettesOptionMenu2 = OptionMenu(uwPalettesFrame2, self.uwPalettesVar2, 'default', 'random', 'blackout')
    uwPalettesOptionMenu2.pack(side=RIGHT)
    uwPalettesFrame2.pack(anchor=E)

    adjustRomFrame = Frame(bottomAdjustFrame)
    adjustRomLabel = Label(adjustRomFrame, text='Rom to adjust: ')
    self.romVar2 = StringVar(value=working_dirs["adjust.rom"])
    romEntry2 = Entry(adjustRomFrame, textvariable=self.romVar2)

    def RomSelect2():
        rom = filedialog.askopenfilename(filetypes=[("Rom Files", (".sfc", ".smc")), ("All Files", "*")])
        if rom:
            working_dirs["adjust.rom"] = rom
            self.romVar2.set(rom)
    romSelectButton2 = Button(adjustRomFrame, text='Select Rom', command=RomSelect2)

    adjustRomLabel.pack(side=LEFT)
    romEntry2.pack(side=LEFT, fill=X, expand=True)
    romSelectButton2.pack(side=LEFT)
    adjustRomFrame.pack(fill=X, expand=True)

    def adjustRom():
        guiargs = Namespace()
        guiargs.heartbeep = self.heartbeepVar2.get()
        guiargs.heartcolor = self.heartcolorVar2.get()
        guiargs.fastmenu = self.fastMenuVar2.get()
        guiargs.ow_palettes = self.owPalettesVar2.get()
        guiargs.uw_palettes = self.uwPalettesVar2.get()
        guiargs.quickswap = bool(self.quickSwapVar2.get())
        guiargs.disablemusic = bool(self.disableMusicVar2.get())
        guiargs.rom = self.romVar2.get()
        guiargs.baserom = top.generationSetupWindow.romVar.get()
#        guiargs.sprite = sprite
        try:
            adjust(args=guiargs)
        except Exception as e:
            logging.exception(e)
            messagebox.showerror(title="Error while creating seed", message=str(e))
        else:
            messagebox.showinfo(title="Success", message="Rom patched successfully")

    adjustButton = Button(bottomAdjustFrame, text='Adjust Rom', command=adjustRom)
    adjustButton.pack(side=BOTTOM, padx=(5, 0))

    return self,working_dirs
