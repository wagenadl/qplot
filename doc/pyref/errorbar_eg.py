import pyqplot as qp
import numpy as np

qp.figure('errorbar', 3, 3)

tt = np.linspace(-np.pi, np.pi, 10)

qp.marker('o', fill='solid')
qp.mark(tt, np.sin(tt))

qp.errorbar(tt, np.sin(tt), .2*np.cos(tt)+.3, 5)

qp.marker('o', fill='solid')
qp.mark(tt, 2+np.sin(tt-1))

qp.errorbar(tt, 2+np.sin(tt-1), (.3+0*tt, .2*np.cos(tt)+.3))
