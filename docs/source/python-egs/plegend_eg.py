import qplot as qp
import numpy as np

qp.figure('plegend', 3, 3)

qp.legopt(x0=5, y0=5, dx=10, width=5)

xx = np.linspace(0, 2*np.pi, 50)

qp.pen('none')
qp.brush('b', .5)
qp.bars(xx, np.cos(xx), .1)

qp.plegend('Cosine')

qp.brush('r', .5)
qp.bars(xx, np.sin(xx), .1)

qp.plegend('Sine')
