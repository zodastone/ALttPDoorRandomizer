def loadcliargs(gui,args):
  if args is not None:
      for k,v in vars(args).items():
          if type(v) is dict:
              setattr(args, k, v[1]) # only get values for player 1 for now
      # load values from commandline args
      gui.generationSetupWindow.createSpoilerVar.set(int(args.create_spoiler))
      gui.generationSetupWindow.suppressRomVar.set(int(args.suppress_rom))
      gui.dungeonRandoWindow.dungeonWidgets["mapshuffle"].storageVar.set(args.mapshuffle)
      gui.dungeonRandoWindow.dungeonWidgets["compassshuffle"].storageVar.set(args.compassshuffle)
      gui.dungeonRandoWindow.dungeonWidgets["smallkeyshuffle"].storageVar.set(args.keyshuffle)
      gui.dungeonRandoWindow.dungeonWidgets["bigkeyshuffle"].storageVar.set(args.bigkeyshuffle)
      gui.itemWindow.itemWidgets["retro"].storageVar.set(args.retro)
      gui.entrandoWindow.entrandoWidgets["openpyramid"].storageVar.set(args.openpyramid)
      gui.gameOptionsWindow.quickSwapVar.set(int(args.quickswap))
      gui.gameOptionsWindow.disableMusicVar.set(int(args.disablemusic))
      if args.multi:
          gui.multiworldWindow.multiworldWidgets["worlds"].storageVar.set(str(args.multi))
      if args.count:
          gui.farBottomFrame.countVar.set(str(args.count))
      if args.seed:
          gui.farBottomFrame.seedVar.set(str(args.seed))
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
      gui.gameOptionsWindow.heartcolorVar.set(args.heartcolor)
      gui.gameOptionsWindow.heartbeepVar.set(args.heartbeep)
      gui.gameOptionsWindow.fastMenuVar.set(args.fastmenu)
      gui.itemWindow.itemWidgets["logiclevel"].storageVar.set(args.logic)
      gui.generationSetupWindow.romVar.set(args.rom)
      gui.entrandoWindow.entrandoWidgets["shuffleganon"].storageVar.set(args.shuffleganon)
      gui.gameOptionsWindow.hintsVar.set(args.hints)
      gui.enemizerWindow.enemizerCLIpathVar.set(args.enemizercli)
      gui.enemizerWindow.enemizerWidgets["potshuffle"].storageVar.set(args.shufflepots)
      gui.enemizerWindow.enemizerWidgets["enemyshuffle"].storageVar.set(args.shuffleenemies)
      gui.enemizerWindow.enemizerWidgets["bossshuffle"].storageVar.set(args.shufflebosses)
      gui.enemizerWindow.enemizerWidgets["enemydamage"].storageVar.set(args.enemy_damage)
      gui.enemizerWindow.enemizerWidgets["enemyhealth"].storageVar.set(args.enemy_health)
      gui.gameOptionsWindow.owPalettesVar.set(args.ow_palettes)
      gui.gameOptionsWindow.uwPalettesVar.set(args.uw_palettes)
#        if args.sprite is not None:
#            gui.gameOptionsWindow.set_sprite(Sprite(args.sprite))