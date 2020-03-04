from source.classes.SpriteSelector import SpriteSelector as spriteSelector
from source.gui.randomize.gameoptions import set_sprite
from Rom import Sprite, get_sprite_from_name
import source.classes.constants as CONST

# Load args/settings for most tabs
def loadcliargs(gui, args, settings=None):
    if args is not None:
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
                    gui.pages[mainpage].pages[subpage].widgets[widget].storageVar.set(args[arg])
                    # If we're on the Game Options page and it's not about Hints
                    if subpage == "gameoptions" and not widget == "hints":
                        # Check if we've got settings
                        # Check if we've got the widget in Adjust settings
                        hasSettings = settings is not None
                        hasWidget = ("adjust." + widget) in settings if hasSettings else None
                        if hasWidget is None:
                            # If we've got a Game Options val and we don't have an Adjust val, use the Game Options val
                            gui.pages["adjust"].content.widgets[widget].storageVar.set(args[arg])

        # Get EnemizerCLI setting
        gui.pages["randomizer"].pages["enemizer"].enemizerCLIpathVar.set(args["enemizercli"])

        # Get baserom path
        gui.pages["randomizer"].pages["generation"].romVar.set(args["rom"])

        # Get Multiworld Worlds count
        if args["multi"]:
            gui.pages["randomizer"].pages["multiworld"].widgets["worlds"].storageVar.set(str(args["multi"]))

        # Get Seed ID
        if args["seed"]:
            gui.frames["bottom"].seedVar.set(str(args["seed"]))

        # Get number of generations to run
        if args["count"]:
            gui.frames["bottom"].widgets["generationcount"].storageVar.set(str(args["count"]))

        # Get output path
        gui.outputPath.set(args["outputpath"])

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
