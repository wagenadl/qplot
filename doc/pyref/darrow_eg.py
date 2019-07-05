import pyqplot as qp
import numpy as np

qp.figure('darrow', 3, 3)

tt = np.linspace(0, 4*np.pi, 100)
xx = np.sin(tt/2)
yy = np.sin(tt)
qp.pen('666')
qp.plot(xx, yy)

qp.brush('k')
qp.pen('k')

for n in range(5, len(xx), 10):
    qp.darrow(xx[n], yy[n], along=[xx[n]-xx[n-1], yy[n]-yy[n-1]])
