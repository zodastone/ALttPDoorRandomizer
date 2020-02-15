from classes.SpriteSelector import SpriteSelector as spriteSelector
from gui.randomize.gameoptions import set_sprite
from Rom import Sprite


def loadcliargs(gui, args):
    if args is not None:
        for k, v in vars(args).items():
            if type(v) is dict:
                setattr(args, k, v[1])  # only get values for player 1 for now
        # load values from commandline args
        gui.pages["randomizer"].pages["generation"].generationWidgets["spoiler"].storageVar.set(int(args.create_spoiler))
        gui.pages["randomizer"].pages["generation"].generationWidgets["suppressrom"].storageVar.set(int(args.suppress_rom))
        gui.pages["randomizer"].pages["dungeon"].dungeonWidgets["mapshuffle"].storageVar.set(args.mapshuffle)
        gui.pages["randomizer"].pages["dungeon"].dungeonWidgets["compassshuffle"].storageVar.set(args.compassshuffle)
        gui.pages["randomizer"].pages["dungeon"].dungeonWidgets["smallkeyshuffle"].storageVar.set(args.keyshuffle)
        gui.pages["randomizer"].pages["dungeon"].dungeonWidgets["bigkeyshuffle"].storageVar.set(args.bigkeyshuffle)
        gui.pages["randomizer"].pages["item"].itemWidgets["retro"].storageVar.set(args.retro)
        gui.pages["randomizer"].pages["entrance"].entrandoWidgets["openpyramid"].storageVar.set(args.openpyramid)
        gui.pages["randomizer"].pages["gameoptions"].gameOptionsWidgets["quickswap"].storageVar.set(int(args.quickswap))
        gui.pages["randomizer"].pages["gameoptions"].gameOptionsWidgets["nobgm"].storageVar.set(int(args.disablemusic))
        if args.multi:
            gui.pages["randomizer"].pages["multiworld"].multiworldWidgets["worlds"].storageVar.set(str(args.multi))
        if args.count:
            gui.frames["bottom"].bottomWidgets["generationcount"].storageVar.set(str(args.count))
        if args.seed:
            gui.frames["bottom"].seedVar.set(str(args.seed))
        gui.pages["randomizer"].pages["item"].itemWidgets["worldstate"].storageVar.set(args.mode)
        gui.pages["randomizer"].pages["item"].itemWidgets["weapons"].storageVar.set(args.swords)
        gui.pages["randomizer"].pages["item"].itemWidgets["itempool"].storageVar.set(args.difficulty)
        gui.pages["randomizer"].pages["item"].itemWidgets["itemfunction"].storageVar.set(args.item_functionality)
        gui.pages["randomizer"].pages["item"].itemWidgets["timer"].storageVar.set(args.timer)
        gui.pages["randomizer"].pages["item"].itemWidgets["progressives"].storageVar.set(args.progressive)
        gui.pages["randomizer"].pages["item"].itemWidgets["accessibility"].storageVar.set(args.accessibility)
        gui.pages["randomizer"].pages["item"].itemWidgets["goal"].storageVar.set(args.goal)
        gui.pages["randomizer"].pages["item"].itemWidgets["crystals_gt"].storageVar.set(args.crystals_gt)
        gui.pages["randomizer"].pages["item"].itemWidgets["crystals_ganon"].storageVar.set(args.crystals_ganon)
        gui.pages["randomizer"].pages["item"].itemWidgets["sortingalgo"].storageVar.set(args.algorithm)
        gui.pages["randomizer"].pages["entrance"].entrandoWidgets["entranceshuffle"].storageVar.set(args.shuffle)
        gui.pages["randomizer"].pages["dungeon"].dungeonWidgets["dungeondoorshuffle"].storageVar.set(args.door_shuffle)
        gui.pages["randomizer"].pages["dungeon"].dungeonWidgets["experimental"].storageVar.set(args.experimental)
        gui.pages["randomizer"].pages["gameoptions"].gameOptionsWidgets["heartcolor"].storageVar.set(args.heartcolor)
        gui.pages["randomizer"].pages["gameoptions"].gameOptionsWidgets["heartbeep"].storageVar.set(args.heartbeep)
        gui.pages["randomizer"].pages["gameoptions"].gameOptionsWidgets["menuspeed"].storageVar.set(args.fastmenu)
        gui.pages["randomizer"].pages["item"].itemWidgets["logiclevel"].storageVar.set(args.logic)
        gui.pages["randomizer"].pages["generation"].romVar.set(args.rom)
        gui.pages["randomizer"].pages["entrance"].entrandoWidgets["shuffleganon"].storageVar.set(args.shuffleganon)
        gui.pages["randomizer"].pages["gameoptions"].gameOptionsWidgets["hints"].storageVar.set(args.hints)
        gui.pages["randomizer"].pages["enemizer"].enemizerCLIpathVar.set(args.enemizercli)
        gui.pages["randomizer"].pages["enemizer"].enemizerWidgets["potshuffle"].storageVar.set(args.shufflepots)
        gui.pages["randomizer"].pages["enemizer"].enemizerWidgets["enemyshuffle"].storageVar.set(args.shuffleenemies)
        gui.pages["randomizer"].pages["enemizer"].enemizerWidgets["bossshuffle"].storageVar.set(args.shufflebosses)
        gui.pages["randomizer"].pages["enemizer"].enemizerWidgets["enemydamage"].storageVar.set(args.enemy_damage)
        gui.pages["randomizer"].pages["enemizer"].enemizerWidgets["enemyhealth"].storageVar.set(args.enemy_health)
        gui.pages["randomizer"].pages["gameoptions"].gameOptionsWidgets["owpalettes"].storageVar.set(args.ow_palettes)
        gui.pages["randomizer"].pages["gameoptions"].gameOptionsWidgets["uwpalettes"].storageVar.set(args.uw_palettes)
        gui.outputPath.set(args.outputpath)

        def sprite_setter(spriteObject):
            gui.pages["randomizer"].pages["gameoptions"].gameOptionsWidgets["sprite"]["spriteObject"] = spriteObject
        if args.sprite is not None:
            sprite_obj = args.sprite if isinstance(args.sprite, Sprite) else Sprite(args.sprite)
            r_sprite_flag = args.randomSprite if hasattr(args, 'randomSprite') else False
            set_sprite(sprite_obj, r_sprite_flag, spriteSetter=sprite_setter,
                       spriteNameVar=gui.pages["randomizer"].pages["gameoptions"].gameOptionsWidgets["sprite"]["spriteNameVar"],
                       randomSpriteVar=gui.randomSprite)

        gui.adjustContent.adjustWidgets["nobgm"].storageVar.set(int(args.disablemusic))
        gui.adjustContent.adjustWidgets['quickswap'].storageVar.set(args.quickswap)
        gui.adjustContent.adjustWidgets["heartcolor"].storageVar.set(args.heartcolor)
        gui.adjustContent.adjustWidgets["heartbeep"].storageVar.set(args.heartbeep)
        gui.adjustContent.adjustWidgets["menuspeed"].storageVar.set(args.fastmenu)
        gui.adjustContent.adjustWidgets["owpalettes"].storageVar.set(args.ow_palettes)
        gui.adjustContent.adjustWidgets["uwpalettes"].storageVar.set(args.uw_palettes)

        def sprite_setter_adj(spriteObject):
            gui.adjustContent.sprite = spriteObject
        if args.sprite is not None:
            sprite_obj = args.sprite if isinstance(args.sprite, Sprite) else Sprite(args.sprite)
            r_sprite_flag = args.randomSprite if hasattr(args, 'randomSprite') else False
            set_sprite(sprite_obj, r_sprite_flag, spriteSetter=sprite_setter_adj,
                       spriteNameVar=gui.adjustContent.spriteNameVar2,
                       randomSpriteVar=gui.randomSprite)
