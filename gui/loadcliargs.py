def loadcliargs(gui,args):
  if args is not None:
      for k,v in vars(args).items():
          if type(v) is dict:
              setattr(args, k, v[1]) # only get values for player 1 for now
      # load values from commandline args
      gui.generationSetupWindow.createSpoilerVar.set(int(args.create_spoiler))
      gui.generationSetupWindow.suppressRomVar.set(int(args.suppress_rom))
      gui.dungeonRandoWindow.mapshuffleVar.set(args.mapshuffle)
      gui.dungeonRandoWindow.compassshuffleVar.set(args.compassshuffle)
      gui.dungeonRandoWindow.keyshuffleVar.set(args.keyshuffle)
      gui.dungeonRandoWindow.bigkeyshuffleVar.set(args.bigkeyshuffle)
      gui.itemWindow.itemWidgets["retro"].storageVar.set(args.retro)
      gui.entrandoWindow.openpyramidVar.set(args.openpyramid)
      gui.gameOptionsWindow.quickSwapVar.set(int(args.quickswap))
      gui.gameOptionsWindow.disableMusicVar.set(int(args.disablemusic))
      if args.multi:
          gui.multiworldWindow.worldVar.set(str(args.multi))
      if args.count:
          gui.farBottomFrame.countVar.set(str(args.count))
      if args.seed:
          gui.farBottomFrame.seedVar.set(str(args.seed))
      gui.itemWindow.itemWidgets["worldState"].storageVar.set(args.mode)
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
      gui.entrandoWindow.shuffleVar.set(args.shuffle)
      gui.dungeonRandoWindow.doorShuffleVar.set(args.door_shuffle)
      gui.gameOptionsWindow.heartcolorVar.set(args.heartcolor)
      gui.gameOptionsWindow.heartbeepVar.set(args.heartbeep)
      gui.gameOptionsWindow.fastMenuVar.set(args.fastmenu)
      gui.itemWindow.itemWidgets["logicLevel"].storageVar.set(args.logic)
      gui.generationSetupWindow.romVar.set(args.rom)
      gui.entrandoWindow.shuffleGanonVar.set(args.shuffleganon)
      gui.gameOptionsWindow.hintsVar.set(args.hints)
      gui.enemizerWindow.enemizerCLIpathVar.set(args.enemizercli)
      gui.enemizerWindow.potShuffleVar.set(args.shufflepots)
      gui.enemizerWindow.enemyShuffleVar.set(args.shuffleenemies)
      gui.enemizerWindow.enemizerBossVar.set(args.shufflebosses)
      gui.enemizerWindow.enemizerDamageVar.set(args.enemy_damage)
      gui.enemizerWindow.enemizerHealthVar.set(args.enemy_health)
      gui.gameOptionsWindow.owPalettesVar.set(args.ow_palettes)
      gui.gameOptionsWindow.uwPalettesVar.set(args.uw_palettes)
#        if args.sprite is not None:
#            gui.gameOptionsWindow.set_sprite(Sprite(args.sprite))