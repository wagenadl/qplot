import pyqplot as qp
import numpy as np

qp.figure('arange', 3, 3)

xx = np.arange(100)
yy = np.cos(xx/10)
qp.plot(xx, yy)
qp.axshift(5)

qp.xaxis(ticks=qp.arange(0,100,20), y=-1)
qp.yaxis(ticks=qp.arange(-1,1))
