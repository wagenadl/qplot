#!/usr/bin/python

import vscope
import ppersist
import numpy as np

srcdir = "/home/wagenaar/xps/publications/manuscripts/qplot/figs/data"

xml = vscope.loadxml(f"{srcdir}/003.xml")
ana = vscope.loadanalog(f"{srcdir}/003.xml", xml.analog)

I_nA = ana["ME2_I"]
V_mV = ana["ME2_Vm"]
V_mV[I_nA>.5] = V_mV[I_nA>.5] - 50; # Apply bridge balance
fs_Hz = xml.analog.rate.value("Hz")

N = len(I_nA)
tt = np.arange(N) / fs_Hz
use = (tt >= 3.3) & (tt <= 3.8)
V_mV = V_mV[use]
I_nA = I_nA[use]

ppersist.save("data/ephys.pkl", I_nA, V_mV, fs_Hz)

