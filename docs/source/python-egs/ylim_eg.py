import qplot as qp
import numpy as np

qp.figure('ylim', 3, 3)

qp.pen('777')
qp.panel('A', (30, 20, 3*72-40, 1.5*72-40))
qp.pen('k')
xx = np.linspace(0, 2*np.pi, 50)
qp.plot(xx, np.sin(xx))
qp.yaxis()

qp.ylim(-2, 1.5)

qp.pen('777')
qp.panel('B', (30, 20+1.5*72, 3*72-40, 1.5*72-40))
qp.pen('k')
qp.plot(xx, np.sin(xx))
qp.yaxis()

qp.ylim(-.8, .8)

qp.panel('-')
