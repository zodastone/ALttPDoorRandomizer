HorzEdge:
    cpy #$ff : beq +
        jsr DetectWestEdge : bra ++
    + jsr DetectEastEdge
    ++ cmp #$ff : beq +
        sta $00 : asl : !add $00 : tax
        cpy #$ff : beq ++
            jsr LoadWestData : bra .main
        ++ jsr LoadEastData
        .main
        jsr LoadEdgeRoomHorz
        sec : rts
    + clc : rts

VertEdge:
    cpy #$ff : beq +
        jsr DetectNorthEdge : bra ++
    + jsr DetectSouthEdge
    ++ cmp #$ff : beq +
        sta $00 : asl : !add $00 : tax
        cpy #$ff : beq ++
            jsr LoadNorthData : bra .main
        ++ jsr LoadSouthData
        .main
        jsr LoadEdgeRoomVert
        sec : rts
    + clc : rts

LoadEdgeRoomHorz:
    lda $03 : sta $a0
    sty $09
    and.b #$0f : asl a : !sub $23 : !add $09 : sta $02
    ldy #$00 : jsr ShiftVariablesMainDir
    lda $a0 : and.b #$F0 : lsr #3 : sta $0603 : inc : sta $0607


    lda $aa : asl : tax ; current quad as 0/4
    lda $04 : and #$40 : bne +
        lda $603 : sta $00 : stz $01 : bra ++
    +   lda $607 : sta $00 : lda #$02 : sta $01
    ++ ; $01 now contains 0 or 2
    lda $00 : sta $21 : sta $0601 : sta $0605
    lda $01 : sta $aa : lsr : sta $01 : stz $00
    lda $0a : sta $20

    stz $0e
    rep #$30
    lda $e8 : and #$01ff : sta $02
    lda $0a : and #$00ff : !add $00 : sta $00

    cmp #$006c : !bge +
        lda #$0077 : bra ++
    + cmp #$017c : !blt +
        lda #$0187 : bra ++
    + !add #$000b
    ++ sta $0618 : inc #2 : sta $061a

    lda $00 : cmp #$0078 : !bge +
        lda #$0000 : bra ++
    + cmp #$0178 : !blt +
        lda #$0100 : bra ++
    + !sub #$0078
    ++ sta $00

    ; figures out scroll amt
    cmp $02 : bne +
        lda #$0000 : bra .done
    + !blt +
        !sub $02 : inc $0e : bra .done
    + lda $02 : !sub $00

    .done sta $ab : sep #$30
    lda $0e : asl : ora $ac : sta $ac
    lda $0603, x : sta $e9

    lda $04 : and #$80 : lsr #4 : sta $ee ; layer stuff
    rts

LoadEdgeRoomVert:
    lda $03 : sta $a0
    sty $09
    and.b #$f0 : lsr #3 : !sub $21 : !add $09 : sta $02
    ldy #$01 : jsr ShiftVariablesMainDir
    lda $a0 : and.b #$0f : asl : sta $060b : inc : sta $060f

    lda $a9 : asl #2 : tax ; current quad as 0/4
    lda $04 : and #$20 : bne +
        lda $60b : sta $00 : stz $01 : bra ++
    +   lda $60f : sta $00 : lda #$01 : sta $01
    ++ ; $01 now contains 0 or 1
    lda $00 : sta $23 : sta $0609 : sta $060d
    lda $01 : sta $a9 : stz $00 ; setup for 16 bit ops
    lda $0a : sta $22

    stz $0e ; pos/neg indicator
    rep #$30
    lda $e2 : and #$01ff : sta $02
    lda $0a : and #$00ff : !add $00 : sta $00

    cmp #$0078 : !bge +
        lda #$007f : bra ++
    + cmp #$0178 : !blt +
        lda #$017f : bra ++
    + !add #$0007
    ++ sta $061c : inc #2 : sta $061e

    lda $00 : cmp #$0078 : !bge +
        lda #$0000 : bra ++
    + cmp #$0178 : !blt +
        lda #$0100 : bra ++
    + !sub #$0078
    ++ sta $00

    ; figures out scroll amt
    cmp $02 : bne +
        lda #$0000 : bra .done
    + !blt +
        !sub $02 : inc $0e : bra .done
    + lda $02 : !sub $00

    .done sta $ab : sep #$30
    lda $0e : asl : ora $ac : sta $ac
    lda $060b, x : sta $e3

    lda $04 : and #$10 : lsr #4 : sta $ee ; layer stuff
    rts


LoadNorthData:
    lda NorthEdgeInfo, x : sta $06 ; not needed I think
    lda NorthOpenEdge, x : sta $03 : inx
    lda NorthEdgeInfo, x : sta $07 ;probably needed for maths - unsure
    lda NorthOpenEdge, x : sta $04 : inx
    lda NorthEdgeInfo, x : sta $08 ; needed for maths
    lda NorthOpenEdge, x : sta $05
    lda $04 : and #$0f : sta $00 : asl : !add $00 : tax
    lda SouthEdgeInfo, x : sta $0a : inx ; needed now, and for nrml transition
    lda SouthEdgeInfo, x : sta $0b : inx ; probably not needed - unsure
    lda SouthEdgeInfo, x : sta $0c ; needed for maths
    rts

LoadSouthData:
    lda SouthEdgeInfo, x : sta $06
    lda SouthOpenEdge, x : sta $03 : inx
    lda SouthEdgeInfo, x : sta $07
    lda SouthOpenEdge, x : sta $04 : inx
    lda SouthEdgeInfo, x : sta $08
    lda SouthOpenEdge, x : sta $05
    lda $04 : and #$0f : sta $00 : asl : !add $00 : tax
    lda NorthEdgeInfo, x : sta $0a : inx
    lda NorthEdgeInfo, x : sta $0b : inx
    lda NorthEdgeInfo, x : sta $0c
    rts

LoadWestData:
    lda WestEdgeInfo, x : sta $06
    lda WestOpenEdge, x : sta $03 : inx
    lda WestEdgeInfo, x : sta $07
    lda WestOpenEdge, x : sta $04 : inx
    lda WestEdgeInfo, x : sta $08
    lda WestOpenEdge, x : sta $05
    lda $04 : and #$0f : sta $00 : asl : !add $00 : tax
    lda EastEdgeInfo, x : sta $0a : inx
    lda EastEdgeInfo, x : sta $0b : inx
    lda EastEdgeInfo, x : sta $0c
    rts

LoadEastData:
    lda EastEdgeInfo, x : sta $06
    lda EastOpenEdge, x : sta $03 : inx
    lda EastEdgeInfo, x : sta $07
    lda EastOpenEdge, x : sta $04 : inx
    lda EastEdgeInfo, x : sta $08
    lda EastOpenEdge, x : sta $05
    lda $04 : and #$0f : sta $00 : asl : !add $00 : tax
    lda WestEdgeInfo, x : sta $0a : inx
    lda WestEdgeInfo, x : sta $0b : inx
    lda WestEdgeInfo, x : sta $0c
    rts


DetectNorthEdge:
    ldx #$ff
    lda $a2
    cmp #$82 : bne +
        lda $22 : cmp #$50 : bcs ++
            ldx #$01 : bra .end
        ++ ldx #$00 : bra .end
    + cmp #$83 : bne +
        ldx #$02 : bra .end
    + cmp #$84 : bne +
        lda $a9 : beq ++
            lda $22 : cmp #$78 : bcs +++
                ldx #$04 : bra .end
            +++ ldx #$05 : bra .end
        ++ lda $22 : cmp #$78 : bcs ++
            ldx #$03 : bra .end
        ++ ldx #$04 : bra .end
    + cmp #$85 : bne +
        ldx #$06 : bra .end
    + cmp #$db : bne +
        lda $a9 : beq ++
            lda $22 : beq ++
                ldx #$08 : bra .end
        ++ ldx #$07 : bra .end
    + cmp #$dc : bne .end
        lda $a9 : bne ++
            lda $22 : cmp #$b0 : bcs ++
                ldx #$09 : bra .end
        ++ ldx #$0a
    .end txa : rts

DetectSouthEdge:
    ldx #$ff
    lda $a2
    cmp #$72 : bne +
        lda $22 : cmp #$50 : bcs ++
            ldx #$01 : bra .end
        ++ ldx #$00 : bra .end
    + cmp #$73 : bne +
        ldx #$02 : bra .end
    + cmp #$74 : bne +
        lda $a9 : beq ++
            lda $22 : cmp #$78 : bcs +++
                ldx #$04 : bra .end
            +++ ldx #$05 : bra .end
        ++ lda $22 : cmp #$78 : bcs ++
            ldx #$03 : bra .end
        ++ ldx #$04 : bra .end
    + cmp #$75 : bne +
        ldx #$06 : bra .end
    + cmp #$cb : bne +
        lda $a9 : beq ++
            lda $22 : beq ++
                ldx #$08 : bra .end
        ++ ldx #$07 : bra .end
    + cmp #$cc : bne .end
        lda $a9 : bne ++
            lda $22 : cmp #$b0 : bcs ++
                ldx #$09 : bra .end
        ++ ldx #$0a
    .end txa : rts

DetectWestEdge:
    ldx #$ff
    lda $a2
    cmp #$65 : bne +
        ldx #$00 : bra .end
    + cmp #$74 : bne +
        ldx #$01 : bra .end
    + cmp #$75 : bne +
        ldx #$02 : bra .end
    + cmp #$82 : bne +
        lda $aa : beq ++
           ldx #$03 : bra .end
        ++ ldx #$04 : bra .end
    + cmp #$85 : bne +
            ldx #$05 : bra .end
    + cmp #$cc : bne +
        lda $aa : beq ++
            ldx #$07 : bra .end
        ++ ldx #$06 : bra .end
    + cmp #$dc : bne .end
        ldx #$08
    .end txa : rts

DetectEastEdge:
    ldx #$ff
    lda $a2
    cmp #$64 : bne +
        ldx #$00 : bra .end
    + cmp #$73 : bne +
        ldx #$01 : bra .end
    + cmp #$74 : bne +
        ldx #$02 : bra .end
    + cmp #$81 : bne +
        lda $aa : beq ++
           ldx #$04 : bra .end
        ++ ldx #$03 : bra .end
    + cmp #$84 : bne +
        ldx #$05 : bra .end
    + cmp #$cb : bne +
        lda $aa : beq ++
            ldx #$07 : bra .end
        ++ ldx #$06 : bra .end
    + cmp #$db : bne .end
        ldx #$08
    .end txa : rts



