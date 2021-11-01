GfxFixer:
{
    lda.l DRMode : bne +
        jsl LoadRoomHook ;this is the code we overwrote
        jsl Dungeon_InitStarTileCh
        jsl LoadTransAuxGfx_Alt
        inc $b0
        rtl
    + lda $b1 : bne .stage2
    jsl LoadRoomHook ; this is the rando version - let's only call this guy once - may fix star tiles and slower loads
    jsl Dungeon_InitStarTileCh
    jsl LoadTransAuxGfx
    jsl Dungeon_LoadCustomTileAttr
    jsl PrepTransAuxGfx
    lda.l DRMode : cmp #$02 : bne + ; only do this in crossed mode
        ldx $a0 : lda.l TilesetTable, x
        cmp $0aa1 : beq + ; already eq no need to decomp
            sta $0aa1
            tax : lda $02802e, x : tay
            jsl DecompDungAnimatedTiles
    +
    lda #$09 : sta $17 : sta $0710
    jsl Palette_SpriteAux3
    jsl Palette_SpriteAux2
    jsl Palette_SpriteAux1
    jsl Palette_DungBgMain
    jsr CgramAuxToMain
    inc $b1
    rtl
    .stage2
    lda #$0a : sta $17 : sta $0710
    stz $b1 : inc $b0
    rtl
}

FixAnimatedTiles:
	LDA.L DRMode : CMP #$02 : BNE +
	LDA $040C : CMP.b #$FF : BEQ +
		PHX
			LDX $A0 : LDA.l TilesetTable, x
			CMP $0AA1 : beq ++
				TAX : PLA : BRA +
			++
		PLX
	+ LDA $02802E, X ; what we wrote over
	RTL

FixCloseDungeonMap:
    LDA.l DRMode : CMP #$02 : BNE .vanilla
	LDA $040C : BMI .vanilla
        LSR : TAX
        LDA.l DungeonTilesets,x
        RTL
    .vanilla
    LDA $7EC20E
    RTL

FixWallmasterLamp:
ORA $0458
STY $1C : STA $1D : RTL ; what we wrote over


CgramAuxToMain: ; ripped this from bank02 because it ended with rts
{
    rep #$20
    ldx.b #$00

    .loop
    lda $7EC300, X : sta $7EC500, x
    lda $7EC340, x : sta $7EC540, x
    lda $7EC380, x : sta $7EC580, x
    lda $7EC3C0, x : sta $7EC5C0, x
    lda $7EC400, x : sta $7EC600, x
    lda $7EC440, x : sta $7EC640, x
    lda $7EC480, x : sta $7EC680, x
    lda $7EC4C0, x : sta $7EC6C0, x

    inx #2 : cpx.b #$40 : bne .loop
    sep #$20

    ; tell NMI to upload new CGRAM data
    inc $15
    rts
}

OverridePaletteHeader:
	lda.l DRMode : cmp #$02 : bne +
	lda.l DRFlags : and #$20 : bne +
	cpx #$01c2 : !bge +
		rep #$20
		txa : lsr : tax
		lda.l PaletteTable, x
		iny : rtl
	+ rep #$20 : iny : lda [$0D], Y ; what we wrote over
rtl