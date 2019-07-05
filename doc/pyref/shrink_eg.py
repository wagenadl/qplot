import pyqplot as qp
import numpy as np

qp.figure('shrink', 3, 3)

qp.brush('888')
qp.pen('none')
qp.panel('A', np.array([.25, .25, 2.5, 1])*72)
qp.pen('k', pattern='solid')
xx = np.linspace(0, 2*np.pi, 50)
qp.plot(xx, np.sin(xx))
qp.xaxis('', [0, np.pi, 2*np.pi], ['0','π','2π'], y=-1)
qp.yaxis('', [-1, 0, 1], x=0)

qp.brush('888')
qp.pen('none')
qp.panel('B', np.array([.25, 1.75, 2.5, 1])*72)
qp.pen('k', pattern='solid')
qp.plot(xx, np.sin(xx))
qp.xaxis('', [0, np.pi, 2*np.pi], ['0','π','2π'], y=-1)
qp.yaxis('', [-1, 0, 1], x=0)
qp.shrink()
