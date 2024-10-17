import qplot as qp
import numpy as np

qp.figure('memo', 3, 3)
xx = np.arange(0, 2*np.pi, .01)
qp.subplot(1,2,0)
qp.plot(xx, np.cos(xx))
qp.xaxis(' ', [0, np.pi, 2*np.pi], ['0', 'π', '2π'], y=-1, axshift=5)

qp.memo('A', 'center', 'bottom')

qp.shrink()

qp.subplot(1,2,1)
qp.plot(xx, np.sin(xx))
qp.xaxis(' ', [0, np.pi, 2*np.pi], ['0', 'π', '2π'], y=-1, axshift=5)

qp.memo('B', 'center', 'bottom')

qp.shrink()

qp.panel()
qp.recall(['A', 'B'])
qp.align('center', 'bottom')
qp.text('Phase (radians)')
