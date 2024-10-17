import qplot as qp
import numpy as np

qp.figure('panel', 3, 3)
xx = np.linspace(0, 3*np.pi, 1000)

qp.plot(xx, np.sin(xx))
qp.shrink(1)

qp.pen(pattern='dash')
qp.brush('777')

qp.relpanel('B', [.6, .7, .35, .25])

qp.pen(pattern='solid')
qp.plot(xx, np.cos(xx))
qp.shrink(5)
