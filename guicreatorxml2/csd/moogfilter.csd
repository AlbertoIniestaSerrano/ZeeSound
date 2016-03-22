<CsoundSynthesizer>
<CsOptions>
-f -odac -iadc
</CsOptions>
<CsInstruments>
sr = 44100 ;set sample rate to 44100 Hz
ksmps = 32 ;number of samples per control cycle
nchnls = 2 ;use two audio channels
0dbfs = 1 ;set maximum level as 1




instr 1
k1 chnget "mf_freq"
k2 chnget "mf_reso"
k2=k2/100
ail,air ins
asig=(ail+air)+.5
aout moogladder asig, k1,k2
outs aout, aout

endin
</CsInstruments>
<CsScore>
i1	0	100

e
</CsScore>

</CsoundSynthesizer>