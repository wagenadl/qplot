#!/usr/bin/python3

import numpy as np
import qplot as qp

qp.figure('eg_imsc', 2.7, 2.)

xx = qp.arange(0, 20, .1)
xx = xx.reshape(1, len(xx))
yy = xx.T

zz = np.cos(xx/2) + np.sin(yy/2)

cc = qp.luts.get('qpjet', 100)

qp.lut(cc)

qp.imsc(zz, xx=xx, yy=yy, c0=-2, c1=2)

qp.cbar(20, 0, 20)
qp.ticklen(5)
qp.caxis('Density', qp.arange(-2,2,2))
qp.ticklen(-2)
qp.minorticks(qp.arange(-1.5, 1.5, .5))

qp.shrink(1, 1)

qp.save('pdf')

