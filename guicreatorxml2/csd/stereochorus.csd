<CsoundSynthesizer>
<CsOptions>
-d -n
</CsOptions>
<CsInstruments>
sr = 44100
ksmps = 32
nchnls = 2
0dbfs = 1

;Author: Iain McCurdy (2012)
;http://iainmccurdy.org/csound.html

opcode StChorus,aa,aakkk
ainL,ainR,krate,kdepth,kwidth xin     ;READ IN INPUT ARGUMENTS
ilfoshape ftgentmp 0, 0, 131072, 19, 1, 0.5, 0,  0.5 ;POSITIVE DOMAIN ONLY SINE WAVE
kporttime linseg 0,0.001,0.02     ;RAMPING UP PORTAMENTO VARIABLE
kChoDepth portk kdepth*0.01, kporttime    ;SMOOTH VARIABLE CHANGES WITH PORTK
aChoDepth interp kChoDepth     ;INTERPOLATE TO CREATE A-RATE VERSION OF K-RATE VARIABLE
amodL   osciliktp  krate, ilfoshape, 0   ;LEFT CHANNEL LFO
amodR   osciliktp  krate, ilfoshape, kwidth*0.5  ;THE PHASE OF THE RIGHT CHANNEL LFO IS ADJUSTABLE
amodL  =  (amodL*aChoDepth)+.01   ;RESCALE AND OFFSET LFO (LEFT CHANNEL)
amodR  =  (amodR*aChoDepth)+.01   ;RESCALE AND OFFSET LFO (RIGHT CHANNEL)
aChoL  vdelay ainL, amodL*1000, 1.2*1000   ;CREATE VARYING DELAYED / CHORUSED SIGNAL (LEFT CHANNEL) 
aChoR  vdelay ainR, amodR*1000, 1.2*1000   ;CREATE VARYING DELAYED / CHORUSED SIGNAL (RIGHT CHANNEL)
aoutL  sum  aChoL*0.6, ainL*0.6                   ;MIX DRY AND WET SIGNAL (LEFT CHANNEL)
aoutR  sum  aChoR*0.6, ainR*0.6    ;MIX DRY AND WET SIGNAL (RIGHT CHANNEL)
xout aoutL,aoutR     ;SEND AUDIO BACK TO CALLER INSTRUMENT
endop

instr 1                                                         
krate chnget "rate"
krate=krate/1000
kdepth chnget "depth"
kdepth=kdepth/100
kwidth chnget "width"
kwidth=kwidth/100
klevel chnget "level"
klevel=klevel/100
a1,a2 ins
a1,a2 StChorus a1,a2,krate,kdepth,kwidth
a1 = a1 * klevel
a2 = a2 * klevel
outs a1,a2
endin

</CsInstruments>

<CsScore>                                              
i 1 0 [60*60*24*7]
</CsScore>

</CsoundSynthesizer>