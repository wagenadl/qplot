import qplot as qp
import numpy as np

qp.figure('errorbars', 3, 3)

tt = np.linspace(-np.pi, np.pi, 10)

qp.marker('o', fill='solid')
qp.mark(tt, np.sin(tt))

qp.errorbars(tt, np.sin(tt), .2*np.cos(tt)+.3, 5)

qp.pen([0, .4, 1])
qp.marker('o', fill='solid')
qp.mark(tt, 2+np.sin(tt-1))

qp.errorbars(tt, 2+np.sin(tt-1), (.3+0*tt, .2*np.cos(tt)+.3))
