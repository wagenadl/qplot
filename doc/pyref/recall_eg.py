import qplot as qp
import numpy as np

qp.figure('memo', 3, 3)
xx = np.arange(0, 2*np.pi, .01)
qp.subplot(2,1,0)
qp.plot(xx, np.cos(xx))
qp.yaxis(' ', [-1, 0, 1], x=0, axshift=5)
qp.memo('A', 'left', 'middle')
qp.shrink()

qp.subplot(2,1,1)
qp.plot(xx, np.sin(xx))
qp.yaxis(' ', [-1, 0, 1], x=0, axshift=5)
qp.memo('B', 'left', 'middle')
qp.shrink()
 
qp.panel()

qp.recall(['A', 'B'], deg=90)

qp.align('center', 'top')
qp.text('Amplitude (normalized)')
