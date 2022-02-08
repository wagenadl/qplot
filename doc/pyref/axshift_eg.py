import qplot as qp
import numpy as np

qp.figure('axshift', 3, 3)
xx = np.linspace(-np.pi, np.pi, 50)
qp.plot(xx, np.sin(xx))

qp.axshift(10)

qp.xaxis('', [-np.pi, 0, np.pi], ['π', '0', 'π'], y=-1)
qp.yaxis('', [-1,0,1], x=-np.pi)
qp.shrink()
