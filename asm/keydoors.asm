; This is the reverse side of various key doors

org $1ff8cc ;(PC: 0ff8cc) GT 0x5b (Spikes & Switch)
dw $0081

org $0a972a ;(PC: 05172a) Eastern Darkness 0x99
dw $2060, $1e71

org $1fb759 ;(PC: 0fb759) Mire Bridges 0xa2
dw $0071

org $0a9887 ;(PC: 051887) Eastern Compass Area 0xa8
dw $3882, $3660, $1e81

org $1fd974 ;(PC: 0fd974) TT Bossway 0xbc
dw $1c82, $0081

; code to un-pair or re-pair doors

; doorlist is loaded into 19A0 but no terminator
; new room is in A0
; for "each" door do the following: (each could mean the first four doors?)
; in lookup table, grab room and corresponding position
; find the info at 7ef000, x where x is twice the paired room
; check the corresponding bit (there are only 4)
; set the bit in 068C

; Note the carry bit is used to indicate if we should aborted (set) or not
CheckIfDoorsOpen: {
    jsr TrapDoorFixer ; see normal.asm
    ; note we are 16bit mode right now
    lda $040c : cmp #$00ff ;: bne .gtg
    lda $a0 : dec : tax : and #$000f ; hijacked code
    sec : rtl ; set carry to indicate normal behavior

    .gtg
    phb : phk : plb
    stx $00 : ldy #$00 : stz $03
    .nextDoor
    lda $a0 : asl : tax
    lda KeyDoorOffset, x : beq .skipDoor
    asl : sty $05 : !add $05 : tax
    lda PairedDoorTable, x : beq .skipDoor
    sta $02 : and #$00ff : asl a : tax
    lda $7ef000, x : and #$f000 : and $03 : beq .skipDoor
    tyx : lda $068c : ora $0098c0,x  : sta $068c
    .skipDoor
    iny #2 : cpy $00 : bne .nextDoor
    plb : clc : rtl
}

; outstanding issues
; how to indicate opening for other (non-first four doors?)
; Bank01 Door Register stores the 4 bits in 068c to 400 (depending on type)
; Key collision and others depend on F0-F3 attribute not sure if extendable to other numbers
; Dungeon_ProcessTorchAndDoorInteractives.isOpenableDoor is the likely culprit fo collision problems
; Saving open status to other unused rooms is tricky -- Bank 2 13947 (line 8888)