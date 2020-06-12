DrHudOverride:
{
	jsl.l NewDrawHud
	jsr HudAdditions
	rtl
}

HudAdditions:
{
    lda.l DRFlags : and #$0008 : beq ++
        lda $7EF423 : and #$00ff
        jsr HudHexToDec4DigitCopy
        LDX.b $05 : TXA : ORA.w #$2400 : STA !GOAL_DRAW_ADDRESS+10 ; draw 100's digit
        LDX.b $06 : TXA : ORA.w #$2400 : STA !GOAL_DRAW_ADDRESS+12 ; draw 10's digit
        LDX.b $07 : TXA : ORA.w #$2400 : STA !GOAL_DRAW_ADDRESS+14 ; draw 1's digit

        lda $7ef29b : and #$0020 : beq +
            lda #$207f : bra .drawthing
        + lda #$345e
        .drawthing STA !GOAL_DRAW_ADDRESS+16 ; castle gate indicator
    ++

    ldx $040c : cpx #$ff : bne + : rts : +
    lda.l DRMode : bne + : rts : +
        phb : phk : plb
        lda $7ef364 : and.l $0098c0, x : beq +
            lda.w CompassBossIndicator, x : and #$00ff : cmp $a0 : bne +
                lda $1a : and #$0010 : beq +
                    lda #$345e : sta $7ec790 : bra .next
        + lda #$207f : sta $7ec790
    .next lda.w DRMode : and #$0002 : bne + : plb : rts : +
            lda $7ef36d : and #$00ff : beq +
                lda.w DungeonReminderTable, x : bra .reminder
            + lda #$207f
            .reminder sta $7ec702
            + lda.w DRFlags : and #$0004 : beq .restore
            lda $7ef368 : and.l $0098c0, x : beq .restore

                lda #$2811 : sta $7ec740
                lda $7ef366 : and.l $0098c0, x : bne .check
                    lda.w BigKeyStatus, x : bne + ; change this, if bk status changes to one byte
                        lda #$2574 : bra ++
                    + cmp #$0002 : bne +
                        lda #$2420 : bra ++
                    + lda #$207f : bra ++
                .check lda #$2826
                ++ sta $7ec742
                txa : lsr : tax

                lda $7ef4e0, x : jsr ConvertToDisplay : sta $7ec7a2
                lda #$2830 : sta $7ec7a4
                lda.w ChestKeys, x : jsr ConvertToDisplay : sta $7ec7a6

                lda #$2871 : sta $7ec780
                lda.w TotalKeys, x
                sep #$20 : !sub $7ef4b0, x : rep #$20
                jsr ConvertToDisplay : sta $7ec782

    .restore
    plb : rts
}

ConvertToDisplay:
    and #$00ff : cmp #$000a : !blt +
        !add #$2553 : rts
    + !add #$2490 : rts


CountChestKeys:
    jsl ItemDowngradeFix
    jsr CountChest
    rtl

CountChest:
    lda !MULTIWORLD_ITEM_PLAYER_ID : bne .end
    cpy #$24 : beq +
    cpy #$a0 : !blt .end
    cpy #$ae : !bge .end
        pha : phx
        tya : and #$0f : bne ++
            inc a
        ++ tax : bra .count
    + pha : phx
    lda $040c : lsr : tax
    .count
    lda $7ef4b0, x : inc : sta $7ef4b0, x
    lda $7ef4e0, x : inc : sta $7ef4e0, x
    .restore plx : pla
    .end rts

CountAbsorbedKeys:
    jsl IncrementSmallKeysNoPrimary : phx
    lda $040c : cmp #$ff : beq +
        lsr : tax
        lda $7ef4b0, x : inc : sta $7ef4b0, x
    + plx : rtl

CountBonkItem:
    jsl GiveBonkItem
    lda $a0 ; check room ID - only bonk keys in 2 rooms so we're just checking the lower byte
    cmp #115 : bne + ; Desert Bonk Key
        lda.l BonkKey_Desert
        bra ++
    + : cmp #140 : bne + ; GTower Bonk Key
        lda.l BonkKey_GTower
        bra ++
    + lda.b #$24 ; default to small key
    ++
    phy : tay : jsr CountChest : ply
    rtl

;================================================================================
; 16-bit A, 8-bit X
; in:	A(b) - Byte to Convert
; out:	$04 - $07 (high - low)
;================================================================================
HudHexToDec4DigitCopy:
    LDY.b #$90
    -
        CMP.w #1000 : !BLT +
        INY
        SBC.w #1000 : BRA -
    +
    STY $04 : LDY #$90 ; Store 1000s digit & reset Y
    -
        CMP.w #100 : !BLT +
        INY
        SBC.w #100 : BRA -
    +
    STY $05 : LDY #$90 ; Store 100s digit & reset Y
    -
        CMP.w #10 : !BLT +
        INY
        SBC.w #10 : BRA -
    +
    STY $06 : LDY #$90 ; Store 10s digit & reset Y
    CMP.w #1 : !BLT +
    -
        INY
        DEC : BNE -
    +
    STY $07 ; Store 1s digit
RTS