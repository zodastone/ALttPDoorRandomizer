!add = "clc : adc"
!addl = "clc : adc.l"
!sub = "sec : sbc"
!bge = "bcs"
!blt = "bcc"

; Free RAM notes
; Normal doors use $AB-AC for scrolling indicator
; Normal doors use $FE to store the trap door indicator
; Spiral doors use $045e to store stair type
; Gfx uses $b1 to for sub-sub-sub-module thing

; Hooks into various routines
incsrc drhooks.asm

;Main Code
org $278000 ;138000
db $44, $52 ;DR
DRMode:
dw 0
DRFlags:
dw 0
DRScroll:
db 0
OffsetTable:
dw -8, 8

incsrc normal.asm
incsrc scroll.asm
incsrc spiral.asm
incsrc gfx.asm
incsrc keydoors.asm
incsrc overrides.asm
incsrc edges.asm
incsrc math.asm
incsrc hudadditions.asm
warnpc $279700

incsrc doortables.asm
warnpc $288000

; deals with own hooks
incsrc keydropshuffle.asm
