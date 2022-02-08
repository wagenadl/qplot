import qplot as qp
import numpy as np

qp.figure('gline', 3, 3)

xx = np.arange(-1.5*np.pi, 1.5*np.pi)
yy = np.cos(xx)
qp.marker('o', fill='solid')
qp.mark(xx, yy)

N=len(xx)
for n in range(N-1):
    qp.gline([[qp.AbsData(xx[n], yy[n]), qp.Retract(10)],
              [qp.AbsData(xx[n+1],yy[n+1]), qp.Retract(10)]])
