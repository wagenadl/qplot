import qplot as qp
import numpy as np

qp.figure('mlegend', 3, 3)

qp.legopt(x0=5, y0=5, dx=10, width=5)

qp.pen('b')
qp.marker('x')
qp.mark(np.random.randn(50), np.random.randn(50))

qp.mlegend('1 x 1')

qp.pen('r')
qp.marker('+')
qp.mark(np.random.randn(50)/2, np.random.randn(50)*2)

qp.mlegend('0.5 x 2')

qp.pen('080')
qp.brush('none')
qp.marker('o', fill='brush')
qp.mark(np.random.randn(50)*2, np.random.randn(50)/2)

qp.mlegend('2 x 0.5')

qp.shrink(1, 1)
