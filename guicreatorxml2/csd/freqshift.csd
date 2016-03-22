<CsoundSynthesizer>
<CsOptions>
-f -odac -iadc
</CsOptions>
<CsInstruments>
sr = 44100 ;set sample rate to 44100 Hz
ksmps = 32 ;number of samples per control cycle
nchnls = 2 ;use two audio channels
0dbfs = 1 ;set maximum level as 1

opcode freqShift, a, ak
  
	ain, kfreq	xin
	
	; Phase quadrature output derived from input signal.
	areal, aimag hilbert ain
	 
	; Sine table for quadrature oscillator.
	iSineTable ftgen	0, 0, 16384, 10, 1

	; Quadrature oscillator.
	asin oscili 1, kfreq, iSineTable
	acos oscili 1, kfreq, iSineTable, .25
	 
	; Use a trigonometric identity. 
	; See the references for further details.
	amod1 = areal * acos
	amod2 = aimag * asin
	
	; Both sum and difference frequencies can be 
	; output at once.
	; aupshift corresponds to the sum frequencies.
	aupshift = (amod1 + amod2) * 0.7
	; adownshift corresponds to the difference frequencies. 
	adownshift = (amod1 - amod2) * 0.7
	
	; Notice that the adding of the two together is
	; identical to the output of ring modulation.
	
	xout aupshift
endop


instr 1
	k1 chnget "fs_pitch" ;-200,200

	ail,air ins
	asig=(ail+air)+.5
	aout freqShift asig, k1
	outs aout,aout

endin
</CsInstruments>
<CsScore>
i1	0	100

e
</CsScore>

</CsoundSynthesizer>