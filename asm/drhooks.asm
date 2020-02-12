org $02b5c4 ; -- moving right routine 135c4
jsl WarpRight
org $02b665 ; -- moving left routine
jsl WarpLeft
org $02b713 ; -- moving down routine
jsl WarpDown
org $02b7b4 ; -- moving up routine
jsl WarpUp
org $02bd80
jsl AdjustTransition
nop

;turn off linking doors -- see .notRoomLinkDoor label in Bank02.asm
org $02b5a6
bra NotLinkDoor1
org $02b5b6
NotLinkDoor1:
org $02b647
bra NotLinkDoor2
org $02b657
NotLinkDoor2:


; Staircase routine
org $01c3d4 ;(PC: c3d4)
jsl RecordStairType : nop
org $02a1e7 ;(PC: 121e7)
jsl SpiralWarp


; Graphics fix
org $02895d
Splicer:
jsl GfxFixer
lda $b1 : beq .done
rts
nop #5
.done

org $00fda4
Dungeon_InitStarTileCh:
org $00d6ae ;(PC: 56ae)
LoadTransAuxGfx:
org $00df5a ;(PC: 5f5a)
PrepTransAuxGfx:
org $0ffd65 ;(PC: 07fd65)
Dungeon_LoadCustomTileAttr:
;org $01fec1
;Dungeon_ApproachFixedColor_variable:
;org $a0f972 ; Rando version
;LoadRoomHook:
org $1bee74 ;(PC: 0dee74)
Palette_DungBgMain:
org $1bec77
Palette_SpriteAux3:
org $1becc5
Palette_SpriteAux2:
org $1bece4
Palette_SpriteAux1:


org $0DFA53
jsl.l LampCheckOverride
org $028046 ; <- 10046 - Bank02.asm : 217 (JSL EnableForceBlank) (Start of Module_LoadFile)
jsl.l OnFileLoadOverride
org $07A93F  ; < 3A93F - Bank07.asm 6548 (LDA $8A : AND.b #$40 - Mirror checks)
jsl.l MirrorCheckOverride

org $05ef47
Sprite_HeartContainer_Override: ;sprite_heart_upgrades.asm : 96-100 (LDA $040C : CMP.b #$1A : BNE .not_in_ganons_tower)
jsl GtBossHeartCheckOverride : bcs .not_in_ganons_tower
nop : stz $0dd0, X : rts
.not_in_ganons_tower

; These two, if enabled together, have implications for vanilla BK doors in IP/Hera/Mire
; IPBJ is common enough to consider not doing this. Mire is not a concern for vanilla - maybe glitched modes
; Hera BK door back can be seen with Pot clipping - likely useful for no logic seeds

;Kill big key (1e) check for south doors
;org $1aa90
;DontCheck:
;bra .done
;nop #3
;.done

;Enable south facing bk graphic
;org $4e24
;dw $2ac8

org $01b714 ; PC: b714
OpenableDoors:
jsl CheckIfDoorsOpen
bcs .normal
rts
.normal
