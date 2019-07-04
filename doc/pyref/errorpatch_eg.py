import pyqplot as qp
import numpy as np

qp.figure('errorpatch', 3, 3)

tt = np.linspace(-np.pi, np.pi, 50)

qp.brush('555')
qp.pen('none')

qp.errorpatch(tt, np.sin(tt), .2*np.cos(tt)+.3)

qp.pen('k', 1, cap='round')
qp.plot(tt, np.sin(tt))
