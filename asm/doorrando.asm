!add = "clc : adc"
!sub = "sec : sbc"

; Free RAM notes
; Normal doors use $0127 for scrolling indicator
; Normal doors use $AB to store the trap door indicator
; Spiral doors use $045e to store stair type
; Gfx uses $b1 to for sub-sub-sub-module thing

; Hooks into various routines

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
org $01b714
jsl TrapDoorFixer

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
;org $0ffd65 ;(PC: 07fd65)
;Dungeon_LoadCustomTileAttr:
;org $01fec1
;Dungeon_ApproachFixedColor_variable:
org $a0f432 ; Rando version -- needs to be after hooks and loadroom.asm I think?
Dungeon_LoadRoom_RANDO:
org $1bee74 ;(PC: 0dee74)
Palette_DungBgMain:
org $1bec77
Palette_SpriteAux3:
org $1becc5
Palette_SpriteAux2:
org $1bece4
Palette_SpriteAux1:

;Kill big key (1e) check for south doors - not that easy unfortunately
;org $1aa90
;nop #5

;Main Code
org $278000 ;138000
incsrc normal.asm
incsrc spiral.asm
incsrc gfx.asm

; Data Section
org $279000
OffsetTable:
dw -8, 8

; Vert 0,6,0 Horz 2,0,8
org $279010
CoordIndex: ; Horizontal 1st
db 2, 0 ; Coordinate Index $20-$23
OppCoordIndex:
db 0, 2 ; Swapped coordinate Index $20-$23 (minor optimization)
CameraIndex: ; Horizontal 1st
db 0, 6 ; Camera Index $e2-$ea
CamQuadIndex: ; Horizontal 1st
db 8, 0 ; Camera quadrants $600-$60f
ShiftQuadIndex:
db 2, 1 ; see ShiftQuad func (relates to $a9,$aa)
CamBoundIndex: ; Horizontal 1st
db 0, 4 ; Camera Bounds $0618-$61f
OppCamBoundIndex: ; Horizontal 1st
db 4, 0 ; Camera Bounds $0618-$61f
CamBoundBaseLine: ; X camera stuff is 1st column todo Y camera needs more testing
dw $007f, $0077 ; Left/Top camera bounds when at edge or layout frozen
dw $0007, $000b ; Left/Top camera bounds when not frozen + appropriate low byte $22/$20 (preadj. by #$78/#$6c)
dw $00ff, $010b ; Right/Bot camera bounds when not frozen + appropriate low byte $20/$22
dw $017f, $0187 ; Right/Bot camera bound when at edge or layout frozen

incsrc doortables.asm
