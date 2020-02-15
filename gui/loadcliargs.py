from classes.SpriteSelector import SpriteSelector as spriteSelector
from gui.randomize.gameoptions import set_sprite
from Rom import Sprite


def loadcliargs(gui, args):
    if args is not None:
        for k, v in vars(args).items():
            if type(v) is dict:
                setattr(args, k, v[1])  # only get values for player 1 for now
        # load values from commandline args
        gui.pages["randomizer"].pages["item"].widgets["retro"].storageVar.set(args.retro)
        gui.pages["randomizer"].pages["item"].widgets["worldstate"].storageVar.set(args.mode)
        gui.pages["randomizer"].pages["item"].widgets["logiclevel"].storageVar.set(args.logic)
        gui.pages["randomizer"].pages["item"].widgets["goal"].storageVar.set(args.goal)
        gui.pages["randomizer"].pages["item"].widgets["crystals_gt"].storageVar.set(args.crystals_gt)
        gui.pages["randomizer"].pages["item"].widgets["crystals_ganon"].storageVar.set(args.crystals_ganon)
        gui.pages["randomizer"].pages["item"].widgets["weapons"].storageVar.set(args.swords)
        gui.pages["randomizer"].pages["item"].widgets["itempool"].storageVar.set(args.difficulty)
        gui.pages["randomizer"].pages["item"].widgets["itemfunction"].storageVar.set(args.item_functionality)
        gui.pages["randomizer"].pages["item"].widgets["timer"].storageVar.set(args.timer)
        gui.pages["randomizer"].pages["item"].widgets["progressives"].storageVar.set(args.progressive)
        gui.pages["randomizer"].pages["item"].widgets["accessibility"].storageVar.set(args.accessibility)
        gui.pages["randomizer"].pages["item"].widgets["sortingalgo"].storageVar.set(args.algorithm)

        gui.pages["randomizer"].pages["entrance"].widgets["openpyramid"].storageVar.set(args.openpyramid)
        gui.pages["randomizer"].pages["entrance"].widgets["shuffleganon"].storageVar.set(args.shuffleganon)
        gui.pages["randomizer"].pages["entrance"].widgets["entranceshuffle"].storageVar.set(args.shuffle)

        gui.pages["randomizer"].pages["generation"].widgets["spoiler"].storageVar.set(int(args.create_spoiler))
        gui.pages["randomizer"].pages["generation"].widgets["suppressrom"].storageVar.set(int(args.suppress_rom))
        gui.pages["randomizer"].pages["dungeon"].widgets["mapshuffle"].storageVar.set(args.mapshuffle)
        gui.pages["randomizer"].pages["dungeon"].widgets["compassshuffle"].storageVar.set(args.compassshuffle)
        gui.pages["randomizer"].pages["dungeon"].widgets["smallkeyshuffle"].storageVar.set(args.keyshuffle)
        gui.pages["randomizer"].pages["dungeon"].widgets["bigkeyshuffle"].storageVar.set(args.bigkeyshuffle)
        gui.pages["randomizer"].pages["gameoptions"].widgets["quickswap"].storageVar.set(int(args.quickswap))
        gui.pages["randomizer"].pages["gameoptions"].widgets["nobgm"].storageVar.set(int(args.disablemusic))
        if args.multi:
            gui.pages["randomizer"].pages["multiworld"].widgets["worlds"].storageVar.set(str(args.multi))
        if args.count:
            gui.frames["bottom"].widgets["generationcount"].storageVar.set(str(args.count))
        if args.seed:
            gui.frames["bottom"].seedVar.set(str(args.seed))
        gui.pages["randomizer"].pages["dungeon"].widgets["dungeondoorshuffle"].storageVar.set(args.door_shuffle)
        gui.pages["randomizer"].pages["dungeon"].widgets["experimental"].storageVar.set(args.experimental)
        gui.pages["randomizer"].pages["gameoptions"].widgets["heartcolor"].storageVar.set(args.heartcolor)
        gui.pages["randomizer"].pages["gameoptions"].widgets["heartbeep"].storageVar.set(args.heartbeep)
        gui.pages["randomizer"].pages["gameoptions"].widgets["menuspeed"].storageVar.set(args.fastmenu)
        gui.pages["randomizer"].pages["generation"].romVar.set(args.rom)
        gui.pages["randomizer"].pages["gameoptions"].widgets["hints"].storageVar.set(args.hints)
        gui.pages["randomizer"].pages["enemizer"].enemizerCLIpathVar.set(args.enemizercli)
        gui.pages["randomizer"].pages["enemizer"].widgets["potshuffle"].storageVar.set(args.shufflepots)
        gui.pages["randomizer"].pages["enemizer"].widgets["enemyshuffle"].storageVar.set(args.shuffleenemies)
        gui.pages["randomizer"].pages["enemizer"].widgets["bossshuffle"].storageVar.set(args.shufflebosses)
        gui.pages["randomizer"].pages["enemizer"].widgets["enemydamage"].storageVar.set(args.enemy_damage)
        gui.pages["randomizer"].pages["enemizer"].widgets["enemyhealth"].storageVar.set(args.enemy_health)
        gui.pages["randomizer"].pages["gameoptions"].widgets["owpalettes"].storageVar.set(args.ow_palettes)
        gui.pages["randomizer"].pages["gameoptions"].widgets["uwpalettes"].storageVar.set(args.uw_palettes)
        gui.outputPath.set(args.outputpath)

        def sprite_setter(spriteObject):
            gui.pages["randomizer"].pages["gameoptions"].widgets["sprite"]["spriteObject"] = spriteObject
        if args.sprite is not None:
            sprite_obj = args.sprite if isinstance(args.sprite, Sprite) else Sprite(args.sprite)
            r_sprite_flag = args.randomSprite if hasattr(args, 'randomSprite') else False
            set_sprite(sprite_obj, r_sprite_flag, spriteSetter=sprite_setter,
                       spriteNameVar=gui.pages["randomizer"].pages["gameoptions"].widgets["sprite"]["spriteNameVar"],
                       randomSpriteVar=gui.randomSprite)

        gui.pages["adjust"].content.adjustWidgets["nobgm"].storageVar.set(int(args.disablemusic))
        gui.pages["adjust"].content.adjustWidgets['quickswap'].storageVar.set(args.quickswap)
        gui.pages["adjust"].content.adjustWidgets["heartcolor"].storageVar.set(args.heartcolor)
        gui.pages["adjust"].content.adjustWidgets["heartbeep"].storageVar.set(args.heartbeep)
        gui.pages["adjust"].content.adjustWidgets["menuspeed"].storageVar.set(args.fastmenu)
        gui.pages["adjust"].content.adjustWidgets["owpalettes"].storageVar.set(args.ow_palettes)
        gui.pages["adjust"].content.adjustWidgets["uwpalettes"].storageVar.set(args.uw_palettes)

        def sprite_setter_adj(spriteObject):
            gui.pages["adjust"].content.sprite = spriteObject
        if args.sprite is not None:
            sprite_obj = args.sprite if isinstance(args.sprite, Sprite) else Sprite(args.sprite)
            r_sprite_flag = args.randomSprite if hasattr(args, 'randomSprite') else False
            set_sprite(sprite_obj, r_sprite_flag, spriteSetter=sprite_setter_adj,
                       spriteNameVar=gui.pages["adjust"].content.spriteNameVar2,
                       randomSpriteVar=gui.randomSprite)
