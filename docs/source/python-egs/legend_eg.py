import qplot as qp
import numpy as np

qp.figure('legend', 3, 3)

qp.legopt(x0=2*np.pi, y0=1, dx=10)

xx = np.arange(0, 2*np.pi, .1)

qp.pen('b')
qp.plot(xx, np.cos(xx))

qp.legend('Cosine')

qp.pen('r')
qp.plot(xx, np.sin(xx))

qp.legend('Sine')

qp.shrink()
