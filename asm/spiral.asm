RecordStairType: {
    pha
    lda DRMode : beq .norm
    lda $040c : cmp #$ff : beq .norm
         lda $0e : sta $045e
         cmp #$26 : beq .norm ; skipping in-floor staircases
            pla : bra +
    .norm pla : sta $a0
    + lda $063d, x
    rtl
}

SpiralWarp: {
    lda DRMode : beq .abort ; abort if not DR
    lda $040c : cmp.b #$ff : beq .abort ; abort if not in dungeon
    lda $045e : cmp #$5e : beq .gtg ; abort if not spiral - intended room is in A!
    cmp #$5f : beq .gtg
    .abort
    stz $045e : lda $a2 : and #$0f : rtl ; clear,run hijacked code and get out

    .gtg
    phb : phk : plb : phx : phy ; push stuff
    jsr LookupSpiralOffset
    rep #$30 : and #$00FF : asl #2 : tax
    lda SpiralTable, x : sta $00
    lda SpiralTable+2, x : sta $02
    sep #$30
    lda $00 : sta $a0
    ; shift quadrant if necessary
    stz $07 ; this is a x quad adjuster for those blasted staircase on the edges
    lda $01 : and #$01 : !sub $a9
    bne .xQuad
    lda $0462 : and #$04 : bne .xqCont
    inc $07
    .xqCont lda $22 : bne .skipXQuad ; this is an edge case
    dec $23 : bra .skipXQuad ; need to -1 if $22 is 0
    .xQuad sta $06 : !add $a9 : sta $a9
    lda $0462 : and #$04 : bne .xCont
    inc $07 ; up stairs are going to -1 the quad anyway during transition, need to add this back
    .xCont ldy #$00 : jsr ShiftQuadSimple

    .skipXQuad
    lda $aa : lsr : sta $06 : lda $01 : and #$02 : lsr : !sub $06
    beq .skipYQuad
    sta $06 : asl : !add $aa : sta $aa
    ldy #$01 : jsr ShiftQuadSimple

    .skipYQuad
    lda $01 : and #$04 : lsr : sta $048a ;fix layer calc 0->0 2->1
    lda $01 : and #$08 : lsr #2 : sta $0492 ;fix from layer calc 0->0 2->1
    ; shift lower coordinates
    lda $02 : sta $22 : bne .adjY : lda $23 : !add $07 : sta $23
    .adjY lda $03 : sta $20 : bne .upDownAdj : inc $21
    .upDownAdj ldx #$08
    lda $0462 : and #$04 : beq .upStairs
    ldx #$fd
    lda $01 : and #$80 : bne .set53
    ; if target is also down adjust by (6,-15)
    lda #$06 : !add $20 : sta $20 : lda #$eb : !add $22 : sta $22 : bra .set53
    .upStairs
    lda $01 : and #$80 : beq .set53
    ; if target is also up adjust by (-6, 14)
    lda #$fa : !add $20 : sta $20 : lda #$14 : !add $22 : sta $22
    bne .set53 : inc $23
    .set53
    txa : !add $22 : sta $53

    lda $01 : and #$10 : sta $07 ; zeroHzCam check
    ldy #$00 : jsr SetCamera
    lda $01 : and #$20 : sta $07 ; zeroVtCam check
    ldy #$01 : jsr SetCamera

    stz $045e ; clear the staircase flag

    ; animated tiles fix
    lda DRMode : cmp #$02 : bne + ; only do this in crossed mode
        ldx $a0 : lda TilesetTable, x
        cmp $0aa1 : beq + ; already eq no need to decomp
            sta $0aa1
            tax : lda $02802e, x : tay
            jsl DecompDungAnimatedTiles
    +
    stz $047a
    ply : plx : plb ; pull the stuff we pushed
    lda $a2 : and #$0f ; this is the code we are hijacking
    rtl
}

;Sets the offset in A
LookupSpiralOffset: {
    ;where link currently is in $a2: quad in a8 & #$03
    ;count doors
    stz $00 : ldx #$00 : stz $01

    .loop
    lda $047e, x : cmp $00 : bcc .continue
    sta $00
    .continue inx #2
    cpx #$08 : bcc .loop

    lda $00 : lsr
    cmp #$01 : beq .done

    ; look up the quad
    lda $a9 : ora $aa : and #$03 : beq .quad0
    cmp #$01 : beq .quad1
    cmp #$02 : beq .quad2
    cmp #$03 : beq .quad3
    .quad0
    inc $01 : lda $a2
    cmp #$0c : beq .q0diff ;gt ent
    cmp #$70 : bne .done   ;hc stairwell
    .q0diff lda $22 : cmp #$00 : beq .secondDoor
    cmp #$98 : bcc .done ;gt ent and hc stairwell
    .secondDoor inc $01 : bra .done
    .quad1
    lda $a2
    cmp #$1a : beq .q1diff ;pod compass
    cmp #$26 : beq .q1diff ;swamp elbows
    cmp #$6a : beq .q1diff ;pod dark basement
    cmp #$76 : bne .done   ;swamp drain
    .q1diff lda $22 : cmp #$98 : bcc .done
    inc $01 : bra .done
    .quad2
    lda #$03 : sta $01 : lda $a2
    cmp #$5f : beq .iceu ;ice u room
    cmp #$3f : bne .done ;hammer ice exception
    stz $01 : bra .done
    .iceu lda $22 : cmp #$78 : bcc .done
    inc $01 : bra .done
    .quad3
    lda $a2 : cmp #$40 : beq .done ; top of aga exception
    lda #$02 : sta $01 ; always 2

    .done
    lda $a2 : tax : lda SpiralOffset,x
    !add $01 ;add a thing (0 in easy case)
    rts
}

ShiftQuadSimple: {
	lda CoordIndex,y : tax
	lda $20,x : beq .skip
	lda $21,x : !add $06 : sta $21,x ; coordinate update
	.skip
	lda CamQuadIndex,y : tax
	lda $0601,x : !add $06 : sta $0601,x
	lda $0605,x : !add $06 : sta $0605,x ; high bytes of these guys
	rts
}

SetCamera: {
    stz $04
    tyx : lda $a9,x : bne .nonZeroHalf
    lda CamQuadIndex,y : tax : lda $607,x : pha
    lda CameraIndex,y : tax : pla : cmp $e3, x : bne .noQuadAdj
    dec $e3,x

    .noQuadAdj
    lda $07 : bne .adj0
    lda CoordIndex,y : tax
    lda $20,x : beq .oddQuad
    cmp #$79 : bcc .adj0
    !sub #$78 : sta $04
    tya : asl : !add #$04 : tax : jsr AdjCamBounds : bra .done
    .oddQuad
    lda #$80 : sta $04 : bra .adj1 ; this is such a weird case - quad cross boundary
    .adj0
    tya : asl : tax : jsr AdjCamBounds : bra .done

    .nonZeroHalf ;meaning either right half or bottom half
    lda $07 : bne .setQuad
    lda CoordIndex,y : tax
    lda $20,x : cmp #$78 : bcs .setQuad
    !add #$78 : sta $04
    lda CamQuadIndex,y : tax : lda $0603, x : pha
    lda CameraIndex,y : tax : pla : sta $e3, x
    .adj1
    tya : asl : !add #$08 : tax : jsr AdjCamBounds : bra .done

    .setQuad
    lda CamQuadIndex,y : tax : lda $0607, x : pha
    lda CameraIndex,y : tax : pla : sta $e3, x
    tya : asl : !add #$0c : tax : jsr AdjCamBounds : bra .done

    .done
    lda CameraIndex,y : tax
    lda $04 : sta $e2, x
    rts
}

; input, expects X to be an appropriate offset into the CamBoundBaseLine table
; when $04 is 0 no coordinate are added
AdjCamBounds: {
    rep #$20 : lda CamBoundBaseLine, x : sta $05
    lda $04 : and #$00ff : beq .common
    lda CoordIndex,y : tax
    lda $20, x : and #$00ff : !add $05 : sta $05
    .common
    lda OppCamBoundIndex,y : tax
    lda $05 : sta $0618, x
    inc #2 : sta $061A, x : sep #$20
    rts
}