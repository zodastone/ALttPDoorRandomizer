;================================================================================
; Lamp Mantle & Light Cone Fix
;--------------------------------------------------------------------------------
; Output: 0 for darkness, 1 for lamp cone
;--------------------------------------------------------------------------------
LampCheckOverride:
	LDA $7F50C4 : CMP.b #$01 : BNE + : RTL : +
				  CMP.b #$FF : BNE + : INC : RTL : +

	LDA $7EF34A : BNE .done ; skip if we already have lantern

	LDA $7EF3CA : BNE +
		.lightWorld
		LDA $040C : CMP.b #$02 : BNE ++ ; check if we're in HC
			LDA LampConeSewers : BRA .done
		++
			LDA LampConeLightWorld : BRA .done
	+
		.darkWorld
		LDA LampConeDarkWorld
	.done
	;BNE + : STZ $1D : + ; remember to turn cone off after a torch
RTL

GtBossHeartCheckOverride:
    lda $a0 : cmp #$1c : beq ++
    cmp #$6c : beq ++
    cmp #$4d : bne +
    ++ lda DRFlags : and #$01 : bne ++ ;skip if flag on
        lda $403 : ora #$80 : sta $403
    ++ clc
rtl
    + sec
rtl

OnFileLoadOverride:
    jsl OnFileLoad ; what I wrote over
    lda DRFlags : and #$80 : beq +  ;flag is off
        lda $7ef086 : ora #$80 : sta $7ef086
    + lda DRFlags : and #$02 : beq +
        lda $7ef353 : bne +
            lda #$01 : sta $7ef353
+ rtl

MirrorCheckOverride:
    lda DRFlags : and #$02 : beq ++
        lda $7ef353 : cmp #$01 : beq +
    ++ lda $8A : and #$40 ; what I wrote over
    rtl
    + lda DRScroll : rtl

MirrorCheckOverride2:
    lda $7ef353 : and #$02 : rtl