#!/usr/bin/python3

import numpy as np
import qplot as qp

qp.figure('s1', 3, 2)
xx = np.arange(0, 4*np.pi, .001)
qp.pen('b', 1)
qp.plot(xx, np.cos(xx))
qp.pen()
qp.xaxis('Phase')
qp.yaxis('Cosine')
qp.shrink()
