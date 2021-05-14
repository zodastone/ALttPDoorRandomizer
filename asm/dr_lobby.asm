CheckDarkWorldSanc:
	STA $A0 : STA $048E ; what we wrote over
	LDA.l InvertedMode : AND #$00FF : BNE +
	LDA.l SancDarkWorldFlag : AND #$00FF : BEQ +
		SEP #$30
		LDA $A0 : CMP #$12 : BNE ++
		LDA.l $7EF357 : BNE ++ ; moon pearl?
			LDA #$17 : STA $5D : INC $02E0 : LDA.b #$40 : STA !DARK_WORLD
		++ REP #$30
+ RTL
