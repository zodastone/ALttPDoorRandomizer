HorzEdge:
    cpy #$ff : beq +
        jsr DetectWestEdge : ldy #$02 : bra ++
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
    sty $06
    and.b #$0f : asl a : !sub $23 : !add $06 : sta $02
    ldy #$00 : jsr ShiftVariablesMainDir

    lda $04 : and #$80 : bne .edge
    lda $04 : sta $01 ; load up flags in $01
    jsr PrepScrollToNormal
    bra .scroll

    .edge
    lda $04 : and #$10 : beq +
       lda #$01
    + sta $ee ; layer stuff

    jsr MathHorz

    .scroll
    jsr ScrollY
    rts

LoadEdgeRoomVert:
    lda $03 : sta $a0
    sty $06
    and.b #$f0 : lsr #3 : !sub $21 : !add $06 : sta $02
    ldy #$01 : jsr ShiftVariablesMainDir

    lda $04 : and #$80 : bne .edge
    lda $04 : sta $01 ; load up flags in $01
    jsr PrepScrollToNormal
    bra .scroll

    .edge
    lda $04 : and #$10 : beq +
       lda #$01
    + sta $ee ; layer stuff

    jsr MathVert
    lda $03

    .scroll
    jsr ScrollX
    rts


MathHorz:
    jsr MathStart : lda $20
    jsr MathMid : and #$0040
    jsr MathEnd
    rts

MathVert:
    jsr MathStart : lda $22
    jsr MathMid : and #$0020
    jsr MathEnd
    rts

MathStart:
    rep #$30
    lda $08 : and #$00ff : sta $00
    rts

MathMid:
    and #$01ff : !sub $00 : and #$00ff : sta $00
    ; nothing should be bigger than $a0 at this point

    lda $05 : and #$00f0 : lsr #4 : tax
    lda MultDivInfo, x : and #$00ff : tay
    lda $00 : jsr MultiplyByY : sta $02

    lda $07 : and #$00ff : jsr MultiplyByY : tax

    lda $05 : and #$000f : tay
    lda MultDivInfo, y : and #$00ff : tay
    lda $02 : jsr DivideByY : sta $00
    lda $0c : and #$00ff : sta $02
    lda $04
    rts

MathEnd:
     beq +
        lda #$0100
    + !add $02 : !add $00
    sta $04
    sep #$30
    rts


; expects target quad in $05 (either 0 or 1) and target pixel in $04, target room should be in $a0
; $06 is either $ff or $01/02
; uses $00-$03 and $0e for calculation
; also set up $ac
ScrollY: ;change the Y offset variables
    lda $a0 : and.b #$f0 : lsr #3 : sta $0603 : inc : sta $0607

    lda $05 : bne +
        lda $603 : sta $00 : stz $01 : bra ++
    +   lda $607 : sta $00 : lda #$02 : sta $01
    ++ ; $01 now contains 0 or 2 and $00 contains the correct lat

    stz $0e
    rep #$30
    lda $00 : pha

    lda $e8 : and #$01ff : sta $02
    lda $04 : jsr LimitYCamera : sta $00
    jsr CheckRoomLayoutY : bcc +
        lda $00 : cmp #$0080 : !bge ++
            cmp #$0010 : !blt .cmpSrll
                lda #$0010 : bra .cmpSrll
        ++ cmp #$0100 : !bge .cmpSrll
            lda #$0100
    .cmpSrll sta $00

    ; figures out scroll amt
    + lda $00 : cmp $02 : bne +
        lda #$0000 : bra .next
    + !blt +
        !sub $02 : inc $0e : bra .next
    + lda $02 : !sub $00

    .next
    sta $ab
    jsr AdjustCameraBoundsY

    pla : sta $00
    sep #$30
    lda $04 : sta $20
    lda $00 : sta $21 : sta $0601 : sta $0605
    lda $01 : sta $aa
    lda $0e : asl : ora $ac : sta $ac
    lda $e9 : and #$01 : asl #2 : tax : lda $0603, x : sta $e9
    rts

LimitYCamera:
    cmp #$006c : !bge +
        lda #$0000 : bra .end
    + cmp #$017d : !blt +
        lda #$0110 : bra .end
    + !sub #$006c
    .end rts

CheckRoomLayoutY:
    jsr LoadRoomLayout ;switches to 8-bit
    cmp #$00 : beq .lock
    cmp #$07 : beq .free
    cmp #$01 : beq .free
    cmp #$04 : !bge .lock
    cmp #$02 : bne +
        lda $06 : cmp #$ff : beq .lock
    + cmp #$03 : bne .free
        lda $06 : cmp #$ff : bne .lock
    .free rep #$30 : clc : rts
    .lock rep #$30 : sec : rts

LoadRoomLayout:
    lda $a0 : asl : !add $a0 : tax
    lda $1f8001, x : sta $b8
    lda $1f8000, x : sta $b7
    sep #$30
    ldy #$01 : lda [$b7], y : and #$1c : lsr #2
    rts

; expects target quad in $05 (either 0 or 1) and target pixel in $04, target room should be in $a0
; uses $00-$03 and $0e for calculation
; also set up $ac
ScrollX: ;change the X offset variables
    lda $a0 : and.b #$0f : asl : sta $060b : inc : sta $060f

    lda $05 : bne +
        lda $60b : sta $00 : stz $01 : bra ++
    +   lda $60f : sta $00 : lda #$01 : sta $01
    ++ ; $01 now contains 0 or 1 and $00 contains the correct long

    stz $0e ; pos/neg indicator
    rep #$30
    lda $00 : pha

    lda $e2 : and #$01ff : sta $02
    lda $04 : jsr LimitXCamera : sta $00
    jsr CheckRoomLayoutX : bcc +
        lda $00 : cmp #$0080 : !bge ++
            lda #$0000 : bra .cmpSrll
        ++ lda #$0100
    .cmpSrll sta $00

    ;figures out scroll amt
    + lda $00 : cmp $02 : bne +
        lda #$0000 : bra .next
    + !blt +
        !sub $02 : inc $0e : bra .next
    + lda $02 : !sub $00

    .next
    sta $ab : lda $04

    cmp #$0078 : !bge +
        lda #$007f : bra ++
    + cmp #$0178 : !blt +
        lda #$017f : bra ++
    + !add #$0007
    ++ sta $061c : inc #2 : sta $061e

    pla : sta $00
    sep #$30
    lda $04 : sta $22
    lda $00 : sta $23 : sta $0609 : sta $060d
    lda $01 : sta $a9
    lda $0e : asl : ora $ac : sta $ac
    lda $e3 : and #$01 : asl #2 : tax : lda $060b, x : sta $e3

    rts

LimitXCamera:
    cmp #$0080 : !bge +
        lda #$0000 : bra .end
    + cmp #$0181 : !blt +
        lda #$0180
    + !sub #$0080
    .end rts

CheckRoomLayoutX:
    jsr LoadRoomLayout ;switches to 8-bit
    cmp #$04 : !blt .lock
    cmp #$05 : bne +
        lda $06 : cmp #$ff : beq .lock
    + cmp #$06 : bne .free
        lda $06 : cmp #$ff : bne .lock
    .free rep #$30 : clc : rts
    .lock rep #$30 : sec : rts

AdjustCameraBoundsY:
    jsr CheckRoomLayoutY : bcc .free

    ; layouts that are camera locked (quads only)
    lda $04 : and #$00ff : cmp #$007d : !blt +
        lda #$0088 : bra ++
    + cmp #$006d : !bge +
        lda #$0078 : bra ++
    + !add #$000b

    ; I think we no longer need the $02 variable
    ++ sta $02 : lda $04 : and #$0100 : !add $02 : bra .setBounds

    ; layouts where the camera is free
    .free lda $04 : cmp #$006c : !bge +
        lda #$0077 : bra .setBounds
    + cmp #$017c : !blt +
        lda #$0187 : bra .setBounds
    + !add #$000b
    .setBounds sta $0618 : inc #2 : sta $061a
    rts


; don't need midpoint of edge Link is leaving (formerly in $06 - used by dir indicator)
; don't need width of edge Link is going to (currently in $0b)
LoadNorthData:
    lda NorthOpenEdge, x : sta $03 : inx ; target room
    lda NorthEdgeInfo, x : sta $07 ; needed for maths - (divide by 2 anyway)
    lda NorthOpenEdge, x : sta $04 : inx ; bit field
    lda NorthEdgeInfo, x : sta $08 ; needed for maths
    lda NorthOpenEdge, x : sta $05 ; ratio
    lda $04 : jsr LoadSouthMidpoint : inx ; needed now, and for nrml transition
    lda SouthEdgeInfo, x : sta $0b : inx ; probably not needed todo: remove
    lda SouthEdgeInfo, x : sta $0c ; needed for maths
    rts

LoadSouthMidpoint:
    and #$0f : sta $00 : asl : !add $00 : tax
    lda SouthEdgeInfo, x : sta $0a ; needed now, and for nrml transition
    rts

LoadSouthData:
    lda SouthOpenEdge, x : sta $03 : inx
    lda SouthEdgeInfo, x : sta $07
    lda SouthOpenEdge, x : sta $04 : inx
    lda SouthEdgeInfo, x : sta $08
    lda SouthOpenEdge, x : sta $05
    lda $04 : jsr LoadNorthMidpoint : inx
    lda NorthEdgeInfo, x : sta $0b : inx
    lda NorthEdgeInfo, x : sta $0c
    rts

LoadNorthMidpoint:
    and #$0f : sta $00 : asl : !add $00 : tax
    lda NorthEdgeInfo, x : sta $0a ; needed now, and for nrml transition
    rts

LoadWestData:
    lda WestOpenEdge, x : sta $03 : inx
    lda WestEdgeInfo, x : sta $07
    lda WestOpenEdge, x : sta $04 : inx
    lda WestEdgeInfo, x : sta $08
    lda WestOpenEdge, x : sta $05
    lda $04 : jsr LoadEastMidpoint : inx
    lda EastEdgeInfo, x : sta $0b : inx
    lda EastEdgeInfo, x : sta $0c
    rts

LoadEastMidpoint:
    and #$0f : sta $00 : asl : !add $00 : tax
    lda EastEdgeInfo, x : sta $0a ; needed now, and for nrml transition
    rts

LoadEastData:
    lda EastOpenEdge, x : sta $03 : inx
    lda EastEdgeInfo, x : sta $07
    lda EastOpenEdge, x : sta $04 : inx
    lda EastEdgeInfo, x : sta $08
    lda EastOpenEdge, x : sta $05
    lda $04 : jsr LoadWestMidpoint : inx
    lda WestEdgeInfo, x : sta $0b : inx
    lda WestEdgeInfo, x : sta $0c


LoadWestMidpoint:
    and #$0f : sta $00 : asl : !add $00 : tax
    lda WestEdgeInfo, x : sta $0a ; needed now, and for nrml transition
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
            ldx #$06 : bra .end
        ++ ldx #$07 : bra .end
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
            ldx #$06 : bra .end
        ++ ldx #$07 : bra .end
    + cmp #$db : bne .end
        ldx #$08
    .end txa : rts



