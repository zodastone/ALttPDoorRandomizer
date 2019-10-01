WarpLeft:
	lda $040c : cmp.b #$ff : beq .end
	lda $20 : ldx $aa
	jsr CalcIndex
	!add #$06 : ldy #$01 ; offsets in A, Y
	jsr LoadRoomHorz
.end
	jsr Cleanup
	rtl

WarpRight:
	lda $040c : cmp.b #$ff : beq .end
	lda $20 : ldx $aa
	jsr CalcIndex
	!add #$12 : ldy #$ff ; offsets in A, Y
	jsr LoadRoomHorz
.end
	jsr Cleanup
	rtl

WarpUp:
	lda $040c : cmp.b #$ff : beq .end
	lda $22 : ldx $a9
	jsr CalcIndex
	ldy #$02 ; offsets in A, Y
	jsr LoadRoomVert
.end
	jsr Cleanup
	rtl

WarpDown:
	lda $040c : cmp.b #$ff : beq .end
	lda $22 : ldx $a9
	jsr CalcIndex
	!add #$0c : ldy #$ff ; offsets in A, Y
	jsr LoadRoomVert
.end
	jsr Cleanup
	rtl

TrapDoorFixer:
    lda $ab : and #$0038 : beq .end
    xba : asl #2 : sta $00
    stz $0468 : lda $068c : ora $00 : sta $068c
    .end
    stz $ab ; clear our ab here because we don't need it anymore
    rts

Cleanup:
	inc $11
	lda $ef
	rts

;A needs be to the low coordinate, x needs to be either 0 for left,upper or non-zero for right,down
; This sets A (00,02,04) and stores half that at $04 for later use, (src door)
CalcIndex: ; A->low byte of Link's Coord, X-> Link's quadrant, DoorOffset x 2 -> A, DoorOffset -> $04 (vert/horz agnostic)
	cpx.b #00 : bne .largeDoor
	cmp.b #$90 : bcc .smallDoor
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
	lda $07 : jsr LookupNewRoom ; New room is in A, Room Data is in $00
	lda $01 : and.b #$80 : cmp #$80 : bne .gtg
	pla : sta $a0 : bra .end ; Restore normal room, abort (straight staircases and open edges can get in this routine)

	.gtg ;Good to Go!
	pla ; Throw away normal room (don't fill up the stack)
	lda $a0 : and.b #$0F : asl a : !sub $23 : !add $06 : sta $02
	ldy #$00 : jsr ShiftVariablesMainDir
	lda $aa : lsr : sta $07
	lda $a0 : and.b #$F0 : lsr #3 : !add $07 : !sub $21 : sta $02 : sta $03
	jsr ShiftLowCoord
	jsr ShiftQuad
	jsr ShiftCameraBounds
	ldy #$01 : jsr ShiftVariablesSubDir ; flip direction
	lda $01 : sta $ab : and #$04 : lsr #2
	sta $ee
	lda $01 : and #$10 : beq .end : stz $0468
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
	lda $07 : jsr LookupNewRoom ; New room is in A, Room Data is in $00
	lda $01 : and.b #$80 : cmp #$80 : bne .gtg
	pla : sta $a0 : bra .end ; Restore normal room, abort (straight staircases and open edges can get in this routine)

	.gtg ;Good to Go!
	pla ; Throw away normal room (don't fill up the stack)
	lda $a0 : and.b #$F0 : lsr #3 : !sub $21 : !add $06 : sta $02
	ldy #$01 : jsr ShiftVariablesMainDir
	lda $a0 : and.b #$0F : asl a : !add $a9 : !sub $23 : sta $02 : sta $03
	jsr ShiftLowCoord
	jsr ShiftQuad
	jsr ShiftCameraBounds
	ldy #$00 : jsr ShiftVariablesSubDir ; flip direction
	lda $01 : sta $ab : and #$04 : lsr #2
	sta $ee
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

; INPUTS-- X: Direction Index , $02:  Shift Value
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

ShiftLowCoord:
{
	lda $01 : and.b #$03 ; high byte index
	jsr CalcOpposingShift
	lda $0127 : and.b #$f0 : cmp.b #$20 : bne .lowDone
	lda OppCoordIndex,y : tax
	lda #$80 : !add $20,x : sta $20,x
	.lowDone
	rts
}

; expects A to be (0,1,2) (dest number) and (0,1,2) (src door number) to be stored in $04
; $0127 will be set to a bitmask aaaa qxxf
; a - amount of adjust
; f - flag, if set, then amount is pos, otherwise neg.
; q - quadrant, if set, then quadrant needs to be modified
CalcOpposingShift:
{
	stz $0127 ; set up (can you zero out 127 alone?)
	cmp.b $04 : beq .noOffset ; (equal, no shifts to do)
	phy : tay ; reserve these
	lda $04 : tax : tya : !sub $04 : sta $04 : cmp.b #$00 : bpl .shiftPos
	lda #$40
	cpx.b #$01 : beq .skipNegQuad
	ora #$08
	.skipNegQuad
	sta $0127 : lda $04 : cmp.b #$FE : beq .done ;already set $0127
	lda $0127 : eor #$60
	bra .setDone

	.shiftPos
	lda #$41
	cpy.b #$01 : beq .skipPosQuad
	ora #$08
	.skipPosQuad
	sta $0127 : lda $04 : cmp.b #$02 : bcs .done ;already set $0127
	lda $0127 : eor #$60

	.setDone  sta $0127
	.done     ply
	.noOffset rts
}


ShiftQuad:
{
	lda $0127 : and #$08 : cmp.b #$00 : beq .quadDone
	lda ShiftQuadIndex,y : tax ; X should be set to either 1 (vertical) or 2 (horizontal) (for a9,aa quadrant)
	lda $0127 : and #$01 : cmp.b #$00 : beq .decQuad
	inc $02
	txa : sta $a8, x ; alter a9/aa
	bra .quadDone
	.decQuad
	dec $02
	lda #$00 : sta $a8, x ; alter a9/aa
	.quadDone rts
}

ShiftVariablesSubDir:
{
	lda CoordIndex,y : tax
	lda $21,x : !add $02 : sta $21,x ; coordinate update
	lda CameraIndex,y : tax
	lda $e3,x : !add $03 : sta $e3,x ; scroll register high byte
	lda CamQuadIndex,y : tax
	lda $0601,x : !add $02 : sta $0601,x
	lda $0605,x : !add $02 : sta $0605,x ; high bytes of these guys
	lda $0603,x : !add $03 : sta $0603,x
	lda $0607,x : !add $03 : sta $0607,x
	rts
}

ShiftCameraBounds:
{
	lda CamBoundIndex,y : tax ; should be 0 for horz travel (vert bounds) or 4 for vert travel (horz bounds)
	rep #$30
	lda $0127 : and #$00f0 : asl #2 : sta $06
	lda $0127 : and #$0001 : cmp #$0000 : beq .subIt
	lda $0618, x : !add $06 : sta $0618, x
	lda $061A, x : !add $06 : sta $061A, x
	sep #$30
	rts
	.subIt
	lda $0618, x : !sub $06 : sta $0618, x
	lda $061A, x : !sub $06 : sta $061A, x
	sep #$30
	rts
}

AdjustTransition:
{
	lda $0127 : and #$00F0 : lsr
	sep #$20 : cmp $0126 : bcc .reset
	rep #$20
	phy : ldy #$06 ; operating on vertical registers during horizontal trans
	cpx.b #$02 : bcs .horizontalScrolling
	ldy #$00  ; operate on horizontal regs during vert trans
	.horizontalScrolling
	lda $0127 : and #$0001 : asl : tax
	lda.l OffsetTable,x : adc $00E2,y : and.w #$FFFE : sta $00E2,y : sta $00E0,y
	ply : bra .done
	.reset ; clear the 0127 variable so to not disturb intra-tile doors
	stz $0127
	.done
	rep #$20 : lda $00 : and #$01fc
	rtl
}