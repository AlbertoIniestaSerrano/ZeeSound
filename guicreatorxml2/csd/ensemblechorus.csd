<CsoundSynthesizer>
<CsOptions>
-f -o dac -i adc

</CsOptions>
<CsInstruments>
sr     = 44100
ksmps  = 16
nchnls = 2
0dbfs  = 1

	opcode ensembleChorus, aa, akkkkiip
ain, kdelay, kdpth, kmin, kmax, inumvoice, iwave, icount xin
incr = 1/(inumvoice)

if (icount == inumvoice) goto out
ainl, ainr ensembleChorus ain, kdelay, kdpth, kmin, kmax, inumvoice, iwave, icount + 1

out:

max:
imax = i(kmax)
if (kmax != imax) then 
reinit max
endif

iratemax unirand imax
rireturn
alfo oscil kdpth, iratemax + kmin, iwave
adel vdelay3 ain/(inumvoice * .5), (kdelay + alfo) * 1000, 1000
al = ainl + adel * incr * icount
ar = ainr + adel * (1 - incr * icount)
xout al, ar
	endop

instr 1
k1 	chnget	"ec_delay"
k2	chnget	"ec_depth"

k1=k1/100000
k2=k2/10000;para poner milisg y hacerlos segundos

;ain  diskin2  "C:\loop.wav", 1, 0, 1
al,ar ins
ain=(al+ar)*.5
al, ar ensembleChorus ain, k1, k2, .75, 1, 12, 10
outs al, ar
endin

</CsInstruments>
<CsScore>
f1 0 65536 10 1
f10 0 65536 10 1 0 0 0 0 0 0 0 0 .05

i 1 0 60
e
</CsScore>
</CsoundSynthesizer>