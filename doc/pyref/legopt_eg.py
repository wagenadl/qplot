import qplot as qp
import numpy as np

qp.figure('legopt', 3, 3)

qp.legopt(x0=2*np.pi, y0=1, dx=10, height=16, skip=20, drop=5)
qp.font('Helvetica', 16)

xx = np.arange(0, 2*np.pi, .1)

qp.pen('none')
qp.brush('b', .5)
qp.bars(xx, np.cos(xx), .1)

qp.legopt(color='b')

qp.plegend('Cosine')

qp.brush('r', .5)
qp.bars(xx, np.sin(xx), .1)

qp.legopt(color='r')

qp.plegend('Sine')

qp.shrink()
