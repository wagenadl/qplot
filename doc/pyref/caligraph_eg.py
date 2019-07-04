import pyqplot as qp
import numpy as np

qp.figure('caligraph', 3, 3)

qp.plot([0, 1], [0, 0])
qp.plot([0, 0], [0, 1])
qp.plot([0, -1/3], [0, -2/3])

phi = np.linspace(-.9*np.pi, .9*np.pi, 100)
xx = np.sin(phi)
yy = -np.cos(phi)
ww = 1.5*(1-yy)
xx = xx/10
yy = 1 + yy/30

qp.caligraph(xx, yy, ww)

qp.at(xx[-1], yy[-1], along=(xx[-1]-xx[-2], yy[-1]-yy[-2]))
qp.brush('k')
qp.arrow(6, 4, -2, 1.5)

qp.shrink(1,1)
