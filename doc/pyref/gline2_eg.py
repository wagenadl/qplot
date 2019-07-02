import pyqplot as qp
import numpy as np

qp.figure('gline2', 3, 3)

xx = np.arange(-1.5*np.pi, 1.5*np.pi)
yy = np.cos(xx)
qp.marker('o', fill='solid')
qp.mark(xx, yy)

N=len(xx)
qp.gline2([qp.AbsData(xx, yy), qp.Retract(10)])
