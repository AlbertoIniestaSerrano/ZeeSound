<CsoundSynthesizer>
<CsOptions>
-f -i adc -o dac

</CsOptions>
<CsInstruments>
sr     = 44100
ksmps  = 16
nchnls = 2
0dbfs  = 1



instr 1
k1 	chnget	"pl_pitch"

k1=k1/100

ain  diskin2  "elcubismo.wav", k1, 0, 1
outs ain, ain
endin


</CsInstruments>
<CsScore>

i 1 0 1000
e
</CsScore>
</CsoundSynthesizer>