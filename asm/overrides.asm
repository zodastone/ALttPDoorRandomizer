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
		LDA $040C : CMP.b #$04 : !BGE ++ ; check if we're in HC
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
    ++ lda.l DRFlags : and #$01 : bne ++ ;skip if flag on
        lda $403 : ora #$80 : sta $403
    ++ clc
rtl
    + sec
rtl

OnFileLoadOverride:
    jsl OnFileLoad ; what I wrote over
    lda.l DRFlags : and #$80 : beq +  ;flag is off
        lda $7ef086 : ora #$80 : sta $7ef086
    + lda.l DRFlags : and #$02 : beq +
        lda $7ef353 : bne +
            lda #$01 : sta $7ef353
+ rtl

MirrorCheckOverride:
    lda.l DRFlags : and #$02 : beq ++
        lda $7ef353 : cmp #$01 : beq +
    ++ lda $8A : and #$40 ; what I wrote over
    rtl
    + lda.l DRScroll : rtl

BlockEraseFix:
    lda $7ef353 : and #$02 : beq +
        stz $05fc : stz $05fd
    + rtl

FixShopCode:
    cpx #$300 : !bge +
        sta $7ef000, x
    + rtl

VitreousKeyReset:
    lda.l DRMode : beq +
        stz $0cba, x
    + jsl $0db818 ;restore old code
    rtl

GuruguruFix:
    lda $a0 : cmp #$df : !bge +
        and #$0f : cmp #$0e : !blt +
            iny #2
    + rtl

BlindAtticFix:
    lda.l DRMode : beq +
        lda #$01 : rtl
    + lda $7EF3CC : cmp.b #$06
    rtl

SuctionOverworldFix:
    stz $50 : stz $5e
    lda.l DRMode : beq +
        stz $49
    + rtl

; TT Alcove, Mire bridges, pod falling, SW torch room, TR Pipe room, Bob's Room, Ice Many Pots, Mire Hub
; swamp waterfall, Gauntlet 3, Eastern Push block
CutoffRooms:
db $bc, $a2, $1a, $49, $14, $8c, $9f, $c2
db $66, $5d, $a8
; Don't forget CutoffRoomCount!!!

CutoffEntranceRug:
    pha : phx
    lda.l DRMode : beq .norm
        lda $04 : cmp #$000A : beq +
        cmp #$000C : bne .norm
          + lda $a0 : sep #$20 : ldx #$0000
          	- cmp.l CutoffRooms, x : beq .check
          	inx : cpx #$000B : !blt - ; CutoffRoomCount is here!
        rep #$20
    .norm plx : pla : lda $9B52, y : sta $7E2000, x ; what we wrote over
rtl
     .check
		  rep #$20
		  lda $0c : cmp #$0006 : !bge .skip
		  lda $0e : cmp #$0008 : !bge .skip
		  cmp #$0004 : !blt .skip
      bra  .norm
.skip plx : pla : rtl


StoreTempBunnyState:
	LDA $5D : CMP #$1C : BNE +
		STA $5F
	+ LDA #$15 : STA $5D ; what we wrote over
RTL

RetrieveBunnyState:
	STY $5D : STZ $02D8 ; what we wrote over
	LDA $5F : BEQ +
		STA $5D
+ RTL
