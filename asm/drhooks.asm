
org $01b714 ; PC: b714
OpenableDoors:
jsl CheckIfDoorsOpen
bcs .normal
rts
.normal
