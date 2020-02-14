HorzEdge:
    cpy #$ff : beq +
        jsr DetectWestEdge : bra ++
    + jsr DetectEastEdge
    ++ cmp #$ff : beq +
        sta $00 : asl : !add $00: tax
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
        ; todo: work to do
        sec : rts
    + clc : rts

; todo: LoadVert
; todo: FixAdjustTrans
; todo: Fix ab fe swap in normal

LoadEdgeRoomHorz:
    lda $03 : sta $a0
    sty $09
    and.b #$0f : asl a : !sub $23 : !add $09 : sta $02
    ldy #$00 : jsr ShiftVariablesMainDir
    lda $a0 : and.b #$F0 : lsr #3 : sta $0603 : inc : sta $0607


    lda $04 : and #$40 : bne +
        lda $603 : sta $00 : stz $01 : bra ++
    +   lda $607 : sta $00 : lda #$02 : sta $01
    ++
    lda $00 : sta $21 : sta $0601 : sta $0605
    lda $01 : sta $aa : lsr : sta $01 : stz $00

    stz $0e
    rep #$30
    lda $e8 : sta $02
    lda $06 : and #$00ff : !add $00 : sta $00

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
        !sub $02 : bra .done
    + lda $02 : !sub $00 : inc $0e

    .done sta $ab : sep #$30
    lda $0e : asl : ora $ac : sta $ac
    lda $0601 : sta $e9

    lda $04 : and #$80 : lsr #4 : sta $ee ; layer stuff
    rts


LoadNorthData:
    lda NorthEdgeInfo x, sta $06
    lda NorthEdgeInfo x+1, sta $07
    lda NorthEdgeInfo x+2, sta $08
    lda NorthOpenEdge x, sta $03
    lda NorthOpenEdge x+1, sta $04
    lda NorthOpenEdge x+2, sta $05
    rts

LoadSouthData:
    lda SouthEdgeInfo x, sta $06
    lda SouthEdgeInfo x+1, sta $07
    lda SouthEdgeInfo x+2, sta $08
    lda SouthOpenEdge x, sta $03
    lda SouthOpenEdge x+1, sta $04
    lda SouthOpenEdge x+2, sta $05
    rts

LoadWestData:
    lda WestEdgeInfo x, sta $06
    lda WestEdgeInfo x+1, sta $07
    lda WestEdgeInfo x+2, sta $08
    lda WestOpenEdge x, sta $03
    lda WestOpenEdge x+1, sta $04
    lda WestOpenEdge x+2, sta $05
    rts

LoadEastData:
    lda EastEdgeInfo x, sta $06
    lda EastEdgeInfo x+1, sta $07
    lda EastEdgeInfo x+2, sta $08
    lda EastOpenEdge x, sta $03
    lda EastOpenEdge x+1, sta $04
    lda EastOpenEdge x+2, sta $05
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
            lda $22 : bcs #$b0 : bcs ++
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
            lda $22 : bcs #$b0 : bcs ++
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



