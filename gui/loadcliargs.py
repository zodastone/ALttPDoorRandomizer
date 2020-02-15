from classes.SpriteSelector import SpriteSelector as spriteSelector
from gui.randomize.gameoptions import set_sprite
from Rom import Sprite


def loadcliargs(gui, args):
    if args is not None:
        for k, v in vars(args).items():
            if type(v) is dict:
                setattr(args, k, v[1])  # only get values for player 1 for now
        # load values from commandline args
        gui.generationSetupWindow.generationWidgets["spoiler"].storageVar.set(int(args.create_spoiler))
        gui.generationSetupWindow.generationWidgets["suppressrom"].storageVar.set(int(args.suppress_rom))
        gui.dungeonRandoWindow.dungeonWidgets["mapshuffle"].storageVar.set(args.mapshuffle)
        gui.dungeonRandoWindow.dungeonWidgets["compassshuffle"].storageVar.set(args.compassshuffle)
        gui.dungeonRandoWindow.dungeonWidgets["smallkeyshuffle"].storageVar.set(args.keyshuffle)
        gui.dungeonRandoWindow.dungeonWidgets["bigkeyshuffle"].storageVar.set(args.bigkeyshuffle)
        gui.itemWindow.itemWidgets["retro"].storageVar.set(args.retro)
        gui.entrandoWindow.entrandoWidgets["openpyramid"].storageVar.set(args.openpyramid)
        gui.gameOptionsWindow.gameOptionsWidgets["quickswap"].storageVar.set(int(args.quickswap))
        gui.gameOptionsWindow.gameOptionsWidgets["nobgm"].storageVar.set(int(args.disablemusic))
        if args.multi:
            gui.multiworldWindow.multiworldWidgets["worlds"].storageVar.set(str(args.multi))
        if args.count:
            gui.frames["bottom"].bottomWidgets["generationcount"].storageVar.set(str(args.count))
        if args.seed:
            gui.frames["bottom"].seedVar.set(str(args.seed))
        gui.itemWindow.itemWidgets["worldstate"].storageVar.set(args.mode)
        gui.itemWindow.itemWidgets["weapons"].storageVar.set(args.swords)
        gui.itemWindow.itemWidgets["itempool"].storageVar.set(args.difficulty)
        gui.itemWindow.itemWidgets["itemfunction"].storageVar.set(args.item_functionality)
        gui.itemWindow.itemWidgets["timer"].storageVar.set(args.timer)
        gui.itemWindow.itemWidgets["progressives"].storageVar.set(args.progressive)
        gui.itemWindow.itemWidgets["accessibility"].storageVar.set(args.accessibility)
        gui.itemWindow.itemWidgets["goal"].storageVar.set(args.goal)
        gui.itemWindow.itemWidgets["crystals_gt"].storageVar.set(args.crystals_gt)
        gui.itemWindow.itemWidgets["crystals_ganon"].storageVar.set(args.crystals_ganon)
        gui.itemWindow.itemWidgets["sortingalgo"].storageVar.set(args.algorithm)
        gui.entrandoWindow.entrandoWidgets["entranceshuffle"].storageVar.set(args.shuffle)
        gui.dungeonRandoWindow.dungeonWidgets["dungeondoorshuffle"].storageVar.set(args.door_shuffle)
        gui.dungeonRandoWindow.dungeonWidgets["experimental"].storageVar.set(args.experimental)
        gui.gameOptionsWindow.gameOptionsWidgets["heartcolor"].storageVar.set(args.heartcolor)
        gui.gameOptionsWindow.gameOptionsWidgets["heartbeep"].storageVar.set(args.heartbeep)
        gui.gameOptionsWindow.gameOptionsWidgets["menuspeed"].storageVar.set(args.fastmenu)
        gui.itemWindow.itemWidgets["logiclevel"].storageVar.set(args.logic)
        gui.generationSetupWindow.romVar.set(args.rom)
        gui.entrandoWindow.entrandoWidgets["shuffleganon"].storageVar.set(args.shuffleganon)
        gui.gameOptionsWindow.gameOptionsWidgets["hints"].storageVar.set(args.hints)
        gui.enemizerWindow.enemizerCLIpathVar.set(args.enemizercli)
        gui.enemizerWindow.enemizerWidgets["potshuffle"].storageVar.set(args.shufflepots)
        gui.enemizerWindow.enemizerWidgets["enemyshuffle"].storageVar.set(args.shuffleenemies)
        gui.enemizerWindow.enemizerWidgets["bossshuffle"].storageVar.set(args.shufflebosses)
        gui.enemizerWindow.enemizerWidgets["enemydamage"].storageVar.set(args.enemy_damage)
        gui.enemizerWindow.enemizerWidgets["enemyhealth"].storageVar.set(args.enemy_health)
        gui.gameOptionsWindow.gameOptionsWidgets["owpalettes"].storageVar.set(args.ow_palettes)
        gui.gameOptionsWindow.gameOptionsWidgets["uwpalettes"].storageVar.set(args.uw_palettes)
        gui.outputPath.set(args.outputpath)

        def sprite_setter(spriteObject):
            gui.gameOptionsWindow.gameOptionsWidgets["sprite"]["spriteObject"] = spriteObject
        if args.sprite is not None:
            sprite_obj = args.sprite if isinstance(args.sprite, Sprite) else Sprite(args.sprite)
            r_sprite_flag = args.randomSprite if hasattr(args, 'randomSprite') else False
            set_sprite(sprite_obj, r_sprite_flag, spriteSetter=sprite_setter,
                       spriteNameVar=gui.gameOptionsWindow.gameOptionsWidgets["sprite"]["spriteNameVar"],
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
