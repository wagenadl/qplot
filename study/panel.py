#!/usr/bin/python3

import numpy as np
import qplot as qp

qp.figure('s1', 5, 2)
qp.subplot(1, 2, 0)
xx = np.arange(0, 4*np.pi, .001)
qp.pen('b', 1)
qp.plot(xx, np.cos(xx))
qp.pen()
qp.xaxis('Phase')
qp.yaxis('Cosine')
qp.shrink()

qp.subplot(1, 2, 1)
xx = np.arange(0, 4*np.pi, .001)
qp.pen('r', 1)
qp.plot(xx, np.sin(xx))
qp.pen()
qp.xaxis('Phase')
qp.yaxis('Sine')
qp.shrink()
