WarpLeft:
    lda DRMode : beq .end
	lda $040c : cmp.b #$ff : beq .end
	lda $20 : ldx $aa
	jsr CalcIndex
	!add #$06 : ldy #$01 ; offsets in A, Y
	jsr LoadRoomHorz
.end
	jsr Cleanup
	rtl

WarpRight:
    lda DRMode : beq .end
	lda $040c : cmp.b #$ff : beq .end
	lda $20 : ldx $aa
	jsr CalcIndex
	!add #$12 : ldy #$ff ; offsets in A, Y
	jsr LoadRoomHorz
.end
	jsr Cleanup
	rtl

WarpUp:
    lda DRMode : beq .end
	lda $040c : cmp.b #$ff : beq .end
	lda $22 : ldx $a9
	jsr CalcIndex
	ldy #$02 ; offsets in A, Y
	jsr LoadRoomVert
.end
	jsr Cleanup
	rtl

WarpDown:
    lda DRMode : beq .end
	lda $040c : cmp.b #$ff : beq .end
	lda $22 : ldx $a9
	jsr CalcIndex
	!add #$0c : ldy #$ff ; offsets in A, Y
	jsr LoadRoomVert
.end
	jsr Cleanup
	rtl

; carry set = use link door like normal
; carry clear = we are in dr mode, never use linking doors
CheckLinkDoorR:
    lda DRMode : bne +
        lda $7ec004 : sta $a0 ; what we wrote over
        sec : rtl
    + clc : rtl

CheckLinkDoorL:
    lda DRMode : bne +
        lda $7ec003 : sta $a0 ; what we wrote over
        sec : rtl
    + clc : rtl

TrapDoorFixer:
    lda $fe : and #$0038 : beq .end
    xba : asl #2 : sta $00
    stz $0468 : lda $068c : ora $00 : sta $068c
    .end
    stz $fe ; clear our fe here because we don't need it anymore
    rts

Cleanup:
	inc $11
	lda $ef
	rts

;A needs be to the low coordinate, x needs to be either 0 for left,upper or non-zero for right,down
; This sets A (00,02,04) and stores half that at $04 for later use, (src door)
CalcIndex: ; A->low byte of Link's Coord, X-> Link's quadrant, DoorOffset x 2 -> A, DoorOffset -> $04 (vert/horz agnostic)
	cpx.b #00 : bne .largeDoor
	cmp.b #$d0 : bcc .smallDoor
	lda #$01 : bra .done ; Middle Door
	.smallDoor lda #$00 : bra .done
	.largeDoor lda #$02
	.done
	sta $04
	asl
	rts

; Y is an adjustment for main direction of travel
; A is a door table row offset
LoadRoomHorz:
{
    phb : phk : plb
	sty $06 : sta $07 : lda $a0 : pha ; Store normal room on stack
	lda $07 : jsr LookupNewRoom ; New room is in A, Room Data is in $00-$01
	lda $00 : cmp #$03 : bne .gtg
	jsr HorzEdge : pla : bcs .end
	sta $a0 : bra .end ; Restore normal room, abort (straight staircases and open edges can get in this routine)

	.gtg ;Good to Go!
	pla ; Throw away normal room (don't fill up the stack)
	lda $a0 : and.b #$0F : asl a : !sub $23 : !add $06 : sta $02
	ldy #$00 : jsr ShiftVariablesMainDir

    lda $01 : and #$80 : beq .normal
    ldy $06 : cpy #$ff : beq +
        lda $01 : jsr LoadEastMidpoint : bra ++
    + lda $01 : jsr LoadWestMidpoint
    ++ jsr PrepScrollToEdge : bra .scroll

    .normal
    jsr PrepScrollToNormal
	.scroll
	lda $01 : and #$40 : pha
	jsr ScrollY
	pla : beq .end
	    ldy #$06 : jsr ApplyScroll
	.end
	plb ; restore db register
    rts
}

; Y is an adjustment for main direction of travel (stored at $06)
; A is a door table row offset (stored a $07)
LoadRoomVert:
{
    phb : phk : plb
	sty $06 : sta $07 : lda $a0 : pha ; Store normal room on stack
	lda $07 : jsr LookupNewRoom ; New room is in A, Room Data is in $00-$01
	lda $00 : cmp #$03 : bne .gtg
	jsr VertEdge : pla : bcs .end
	sta $a0 : bra .end ; Restore normal room, abort (straight staircases and open edges can get in this routine)
	.gtg ;Good to Go!
	pla ; Throw away normal room (don't fill up the stack)
	lda $a0 : and.b #$F0 : lsr #3 : !sub $21 : !add $06 : sta $02
	ldy #$01 : jsr ShiftVariablesMainDir

	lda $01 : and #$80 : beq .normal
        ldy $06 : cpy #$ff : beq +
            lda $01 : jsr LoadSouthMidpoint : bra ++
        + lda $01 : jsr LoadNorthMidpoint
	++ jsr PrepScrollToEdge : bra .scroll

    .normal
    jsr PrepScrollToNormal
    .scroll
    lda $01 : and #$40 : pha
    jsr ScrollX
    pla : beq .end
        ldy #$00 : jsr ApplyScroll
    .end
    plb ; restore db register
    rts
}

LookupNewRoom: ; expects data offset to be in A
{
    rep #$30 : and #$00FF ;sanitize A reg (who knows what is in the high byte)
	sta $00 ; offset in 00
	lda $a2 : tax ; probably okay loading $a3 in the high byte
	lda DoorOffset,x : and #$00FF ;we only want the low byte
	asl #3 : sta $02 : !add $02 : !add $02 ;multiply by 24 (data size)
	!add $00 ; should now have the offset of the address I want to load
	tax : lda DoorTable,x : sta $00
	and #$00FF : sta $a0 ; assign new room
	sep #$30
	rts
}

; INPUTS-- Y: Direction Index , $02:  Shift Value
; Sets high bytes of various registers
ShiftVariablesMainDir:
{
	lda CoordIndex,y : tax
	lda $21,x : !add $02 : sta $21,x ; coordinate update
	lda CameraIndex,y : tax
	lda $e3,x : !add $02 : sta $e3,x ; scroll register high byte
	lda CamQuadIndex,y : tax
	lda $0605,x : !add $02 : sta $0605,x ; high bytes of these guys
	lda $0607,x : !add $02 : sta $0607,x
	lda $0601,x : !add $02 : sta $0601,x
	lda $0603,x : !add $02 : sta $0603,x
	rts
}


; Target pixel should be in A, other info in $01
; Sets $04 $05 and $ee
PrepScrollToEdge:
{
    sta $04 : lda $01 : and #$20 : beq +
        lda #01
    + sta $05
    lda $01 : and #$10 : beq +
        lda #01
    + sta $ee
    rts
}

; Normal Flags should be in $01
; Sets $04 $05 and $ee, and $fe
PrepScrollToNormal:
{
    lda $01 : sta $fe : and #$04 : lsr #2 : sta $ee ; trap door and layer
    stz $05 : lda #$78 : sta $04
    lda $01 : and #$03 : beq .end
        cmp #$02 : !bge +
            lda #$f8 : sta $04 : bra .end
        + inc $05
    .end rts
}

StraightStairsFix:
{
    lda DRMode : bne +
        !add $20 : sta $20
    + rtl
}

StraightStairLayerFix:
{
    lda DRMode : beq +
        lda $ee : rtl
    + lda $01c322, x : rtl
}