import pyqplot as qp
import numpy as np

qp.figure('plot', 3, 3)

xx = np.arange(0, 2*np.pi, .1)

qp.plot(xx, np.sin(xx))

qp.clf()

qp.plot(xx, np.cos(xx))
