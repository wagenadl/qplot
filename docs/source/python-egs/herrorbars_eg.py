import qplot as qp
import numpy as np

qp.figure('herrorbars', 3, 3)

tt = np.linspace(-np.pi, np.pi, 10)

qp.marker('o', fill='solid')
qp.mark(np.sin(tt), tt)

qp.herrorbars(tt, np.sin(tt), .2*np.cos(tt)+.3, 5)

qp.pen([0, .4, 1])
qp.marker('o', fill='solid')
qp.mark(2+np.sin(tt-1), tt)

qp.herrorbars(tt, 2+np.sin(tt-1), (.3+0*tt, .2*np.cos(tt)+.3))
