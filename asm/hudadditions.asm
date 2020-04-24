DrHudOverride:
{
	jsl.l NewDrawHud
	jsr HudAdditions
	rtl
}

HudAdditions:
{
    ldx $040c : cpx #$ff : bne + : rts : +
    lda DRMode : bne + : rts : +
        phb : phk : plb
        lda $7ef364 : and.l $0098c0, x : beq +
            lda CompassBossIndicator, x : and #$00ff : cmp $a0 : bne +
                lda $1a : and #$0010 : beq +
                    lda #$345e : sta $7ec790 : bra .next
        + lda #$207f : sta $7ec790
    .next lda DRMode : and #$0002 : bne + : plb : rts : +
            lda $7ef36d : and #$00ff : beq +
                lda DungeonReminderTable, x : bra .reminder
            + lda #$207f
            .reminder sta $7ec702
            + lda DRFlags : and #$0004 : beq .restore
            lda $7ef368 : and.l $0098c0, x : beq .restore

                lda #$2811 : sta $7ec740
                lda $7ef366 : and.l $0098c0, x : bne .check
                    lda BigKeyStatus, x : bne + ; change this, if bk status changes to one byte
                        lda #$2574 : bra ++
                    + cmp #$0002 : bne +
                        lda #$2420 : bra ++
                    + lda #$207f : bra ++
                .check lda #$2826
                ++ sta $7ec742
                txa : lsr : tax

                lda $7ef4e0, x : jsr ConvertToDisplay : sta $7ec7a2
                lda #$2830 : sta $7ec7a4
                lda ChestKeys, x : jsr ConvertToDisplay : sta $7ec7a6

                lda #$2871 : sta $7ec780
                lda TotalKeys, x
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