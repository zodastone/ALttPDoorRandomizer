from source.classes.SpriteSelector import SpriteSelector as spriteSelector
from source.gui.randomize.gameoptions import set_sprite
from Rom import Sprite, get_sprite_from_name
import source.classes.constants as CONST
from source.classes.BabelFish import BabelFish
from source.classes.Empty import Empty

# Load args/settings for most tabs
def loadcliargs(gui, args, settings=None):
    if args is not None:
        fish = BabelFish()
#        for k, v in vars(args).items():
#            if type(v) is dict:
#                setattr(args, k, v[1])  # only get values for player 1 for now
        # load values from commandline args

        # set up options to get
        # Page::Subpage::GUI-id::param-id
        options = CONST.SETTINGSTOPROCESS

        # Cycle through each page
        for mainpage in options:
            # Cycle through each subpage (in case of Item Randomizer)
            for subpage in options[mainpage]:
                # Cycle through each widget
                for widget in options[mainpage][subpage]:
                    # Get the value and set it
                    arg = options[mainpage][subpage][widget]
                    label = fish.translate("gui","gui",mainpage + '.' + subpage + '.' + widget)
                    if hasattr(gui.pages[mainpage].pages[subpage].widgets[widget],"type"):
                        type = gui.pages[mainpage].pages[subpage].widgets[widget].type
                        if type == "checkbox":
                            gui.pages[mainpage].pages[subpage].widgets[widget].checkbox.configure(text=label)
                        elif type == "selectbox":
                            gui.pages[mainpage].pages[subpage].widgets[widget].label.configure(text=label)
                        elif type == "spinbox":
                            gui.pages[mainpage].pages[subpage].widgets[widget].label.configure(text=label)
                    gui.pages[mainpage].pages[subpage].widgets[widget].storageVar.set(args[arg])
                    # If we're on the Game Options page and it's not about Hints
                    if subpage == "gameoptions" and not widget == "hints":
                        # Check if we've got settings
                        # Check if we've got the widget in Adjust settings
                        hasSettings = settings is not None
                        hasWidget = ("adjust." + widget) in settings if hasSettings else None
                        label = fish.translate("gui","gui","adjust." + widget)
                        if ("adjust." + widget) in label:
                            label = fish.translate("gui","gui","randomizer.gameoptions." + widget)
                        if hasattr(gui.pages["adjust"].content.widgets[widget],"type"):
                            type = gui.pages["adjust"].content.widgets[widget].type
                            if type == "checkbox":
                                gui.pages["adjust"].content.widgets[widget].checkbox.configure(text=label)
                            elif type == "selectbox":
                                gui.pages["adjust"].content.widgets[widget].label.configure(text=label)
                        if hasWidget is None:
                            # If we've got a Game Options val and we don't have an Adjust val, use the Game Options val
                            gui.pages["adjust"].content.widgets[widget].storageVar.set(args[arg])

        # Get EnemizerCLI setting
        mainpage = "randomizer"
        subpage = "enemizer"
        widget = "enemizercli"
        setting = "enemizercli"
        # set storagevar
        gui.pages[mainpage].pages[subpage].widgets[widget].storageVar.set(args[setting])
        # set textbox/frame label
        label = fish.translate("gui","gui",mainpage + '.' + subpage + '.' + widget)
        gui.pages[mainpage].pages[subpage].widgets[widget].pieces["frame"].label.configure(text=label)
        # set get from web label
        label = fish.translate("gui","gui",mainpage + '.' + subpage + '.' + widget + ".online")
        gui.pages[mainpage].pages[subpage].widgets[widget].pieces["online"].label.configure(text=label)

        # Get baserom path
        mainpage = "randomizer"
        subpage = "generation"
        widget = "rom"
        setting = "rom"
        # set storagevar
        gui.pages[mainpage].pages[subpage].widgets[widget].storageVar.set(args[setting])
        # set textbox/frame label
        label = fish.translate("gui","gui",mainpage + '.' + subpage + '.' + widget)
        gui.pages[mainpage].pages[subpage].widgets[widget].pieces["frame"].label.configure(text=label)
        # set button label
        label = fish.translate("gui","gui",mainpage + '.' + subpage + '.' + widget + ".button")
        gui.pages[mainpage].pages[subpage].widgets[widget].pieces["button"].configure(text=label)

        # Get Multiworld Worlds count
        mainpage = "randomizer"
        subpage = "multiworld"
        widget = "worlds"
        setting = "multi"
        # set textbox/frame label
        label = fish.translate("gui","gui",mainpage + '.' + subpage + '.' + widget)
        gui.pages[mainpage].pages[subpage].widgets[widget].label.configure(text=label)
        if args[setting]:
            # set storagevar
            gui.pages[mainpage].pages[subpage].widgets[widget].storageVar.set(str(args[setting]))

        # Set Multiworld Names
        mainpage = "randomizer"
        subpage = "multiworld"
        widget = "names"
        # set textbox/frame label
        label = fish.translate("gui","gui",mainpage + '.' + subpage + '.' + widget)
        gui.pages[mainpage].pages[subpage].widgets[widget].pieces["frame"].label.configure(text=label)

        # Get Seed ID
        mainpage = "bottom"
        widget = "seed"
        setting = "seed"
        if args[setting]:
            gui.frames[mainpage].widgets[widget].storageVar.set(str(args[setting]))
        # set textbox/frame label
        label = fish.translate("gui","gui",mainpage + '.' + widget)
        gui.frames[mainpage].widgets[widget].pieces["frame"].label.configure(text=label)

        # Get number of generations to run
        mainpage = "bottom"
        widget = "generationcount"
        setting = "count"
        if args[setting]:
            gui.frames[mainpage].widgets[widget].storageVar.set(str(args[setting]))
        # set textbox/frame label
        label = fish.translate("gui","gui",mainpage + '.' + widget)
        gui.frames[mainpage].widgets[widget].label.configure(text=label)

        # Set Generate button
        mainpage = "bottom"
        widget = "go"
        # set textbox/frame label
        label = fish.translate("gui","gui",mainpage + '.' + widget)
        gui.frames[mainpage].widgets[widget].pieces["button"].configure(text=label)

        # Set Output Directory button
        mainpage = "bottom"
        widget = "outputdir"
        # set textbox/frame label
        label = fish.translate("gui","gui",mainpage + '.' + widget)
        gui.frames[mainpage].widgets[widget].pieces["button"].configure(text=label)
        # Get output path
        gui.frames[mainpage].widgets[widget].storageVar.set(args["outputpath"])

        # Set Output Directory button
        mainpage = "bottom"
        widget = "docs"
        # set textbox/frame label
        label = fish.translate("gui","gui",mainpage + '.' + widget)
        if widget in gui.frames[mainpage].widgets:
            gui.frames[mainpage].widgets[widget].pieces["button"].configure(text=label)

        # Figure out Sprite Selection
        def sprite_setter(spriteObject):
            gui.pages["randomizer"].pages["gameoptions"].widgets["sprite"]["spriteObject"] = spriteObject
        if args["sprite"] is not None:
            sprite_obj = args.sprite if isinstance(args["sprite"], Sprite) else get_sprite_from_name(args["sprite"])
            set_sprite(sprite_obj, False, spriteSetter=sprite_setter,
                       spriteNameVar=gui.pages["randomizer"].pages["gameoptions"].widgets["sprite"]["spriteNameVar"],
                       randomSpriteVar=gui.randomSprite)

        def sprite_setter_adj(spriteObject):
            gui.pages["adjust"].content.sprite = spriteObject
        if args["sprite"] is not None:
            sprite_obj = args.sprite if isinstance(args["sprite"], Sprite) else get_sprite_from_name(args["sprite"])
            set_sprite(sprite_obj, False, spriteSetter=sprite_setter_adj,
                       spriteNameVar=gui.pages["adjust"].content.spriteNameVar2,
                       randomSpriteVar=gui.randomSprite)

# Load args/settings for Adjust tab
def loadadjustargs(gui, settings):
    options = {
        "adjust": {
            "content": {
                "nobgm": "adjust.nobgm",
                "quickswap": "adjust.quickswap",
                "heartcolor": "adjust.heartcolor",
                "heartbeep": "adjust.heartbeep",
                "menuspeed": "adjust.menuspeed",
                "owpalettes": "adjust.owpalettes",
                "uwpalettes": "adjust.uwpalettes"
            }
        }
    }
    for mainpage in options:
        for subpage in options[mainpage]:
            for widget in options[mainpage][subpage]:
                key = options[mainpage][subpage][widget]
                if key in settings:
                    gui.pages[mainpage].content.widgets[widget].storageVar.set(settings[key])
