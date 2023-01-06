#!/usr/bin/python3

import numpy as np
import qplot as qp

qp.figure('eg_gline', 1.8, 2.)
xx = qp.arange(-1.5*np.pi, 1.5*np.pi, 1)
yy = np.cos(xx)
qp.marker('o', 3, 'solid')
qp.mark(xx, yy)

qp.pen('777')
for n in range(len(xx)-1):
    qp.gline([[qp.AbsData(xx[n],yy[n]), qp.Retract(5)],
              [qp.AbsData(xx[n+1],yy[n+1]), qp.Retract(5)]])

qp.shrink()
qp.save('pdf')
