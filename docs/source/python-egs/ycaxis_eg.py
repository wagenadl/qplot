import qplot as qp
import numpy as np

qp.figure('ycaxis_eg', 3, 3)

yy = np.array([1,2,3])
xx = np.array([1,3,2])
qp.pen('none')
qp.brush('777')
qp.hbars(yy, xx, 0.8)

qp.pen('k', .5)
qp.textdist(2, 7)
qp.ycaxis('/Categories/', yy, ['One', 'Two', 'Three'])
