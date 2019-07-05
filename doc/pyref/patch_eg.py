import pyqplot as qp
import numpy as np

qp.figure('patch', 3, 3)
qp.brush('g')

xx = np.linspace(0, 2*np.pi, 7)
qp.patch(np.cos(xx), np.sin(xx))

qp.brush('r', .5)

qp.patch(np.sin(xx), np.cos(xx))

