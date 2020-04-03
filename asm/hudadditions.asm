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
    .next lda DRMode : and #$0002 : beq .restore
            lda DungeonReminderTable, x : sta $7ec702
            lda $7ef368 : and.l $0098c0, x : beq .restore
                txa : lsr : tax
                lda $7ef4b0, x : jsr ConvertToDisplay : sta $7ec7a2
                lda #$2830 : sta $7ec7a4
                lda TotalKeys, x : jsr ConvertToDisplay : sta $7ec7a6

                lda $7ef4e0, x : jsr ConvertToDisplay : sta $7ec7e2
                lda #$2830 : sta $7ec7e4
                lda ChestKeys, x : jsr ConvertToDisplay : sta $7ec7e6
    .restore
    plb : rts
}

ConvertToDisplay:
    and #$00ff : cmp #$000a : !blt +
        !add #$2553 : rts
    + !add #$2490 : rts

; and $18c0, x
;207f is blank

CountChestKeys:
    jsl ItemDowngradeFix
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
    .end rtl

CountAbsorbedKeys:
    jsl IncrementSmallKeysNoPrimary : phx
    lda $040c : cmp #$ff : beq +
        lsr : tax
        lda $7ef4b0, x : inc : sta $7ef4b0, x
    + plx : rtl