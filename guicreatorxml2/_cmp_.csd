<CsoundSynthesizer>
<CsOptions>
;contenedor de opciones, dependeran del programa
 -b 4096 -B 16384 -i adc -o dac
</CsOptions>
<CsInstruments>
;opciones de instrumento
sr=48000
ksmps=32
nchnls=2
0dbfs=1
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
k1 	chnget	"pl_pitch"

k1=k1/100

ain  diskin2  "elcubismo.wav", k1, 0, 1
ga1l = ain
ga1r =  ain
endin
instr 2
k1 chnget "mf_freq"
k2 chnget "mf_reso"
k2=k2/100
ail = ga1l
air = ga1r
asig=(ail+air)+.5
aout moogladder asig, k1,k2
ga2l = aout
ga2r =  aout

endin
instr 3
k1 	chnget	"ec_delay"
k2	chnget	"ec_depth"

k1=k1/100000
k2=k2/10000;para poner milisg y hacerlos segundos

;ain  diskin2  "C:\loop.wav", 1, 0, 1
al = ga2l
ar = ga2r
ain=(al+ar)*.5
al, ar ensembleChorus ain, k1, k2, .75, 1, 12, 10
ga3l = al
ga3r =  ar
endin
instr 4
k1 	chnget	"pl_pitch"

k1=k1/100

ain  diskin2  "elcubismo.wav", k1, 0, 1
ga4l = ain
ga4r =  ain
endin
instr 5
k1 chnget "mf_freq"
k2 chnget "mf_reso"
k2=k2/100
ail = ga4l
air = ga4r
asig=(ail+air)+.5
aout moogladder asig, k1,k2
ga5l = aout
ga5r =  aout

endin
instr 6
k1 	chnget	"ec_delay"
k2	chnget	"ec_depth"

k1=k1/100000
k2=k2/10000;para poner milisg y hacerlos segundos

;ain  diskin2  "C:\loop.wav", 1, 0, 1
al = ga5l
ar = ga5r
ain=(al+ar)*.5
al, ar ensembleChorus ain, k1, k2, .75, 1, 12, 10
outs al, ar
endin
</CsInstruments>
<CsScore>
f1 0 65536 10 1
f10 0 65536 10 1 0 0 0 0 0 0 0 0 .05
f1 0 65536 10 1
f10 0 65536 10 1 0 0 0 0 0 0 0 0 .05
i1 0 36000
i2 0 36000
i3 0 36000
i4 0 36000
i5 0 36000
i6 0 36000
</CsScore>
</CsoundSynthesizer>
