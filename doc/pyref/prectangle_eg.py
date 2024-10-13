import qplot as qp
import numpy as np

qp.figure('prectangle', 3, 3)
qp.brush('049')
qp.pen('none')

qp.prectangle(3, 3, 72, 18)

qp.brush('940')

qp.prectangle(3*72 - 18 - 3, 3*72 - 72 - 3, 18, 72)

qp.pen('k', 2)
xx = np.arange(0, 4*np.pi, np.pi/100)
qp.plot(xx, np.cos(xx))
qp.pen()
qp.xaxis('Phase')
qp.yaxis('Cosine')

