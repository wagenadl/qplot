import qplot as qp
import numpy as np

qp.figure('overlinemin', 3, 3)

xx = np.array([1, 2])
yy = np.array([3, 4])
dy = np.array([.5, .75])

qp.bars(xx, yy, .5)
qp.errorbars(xx, yy, dy)

qp.overline(xx, yy+dy, '*')

xx = xx + 2.5 
qp.bars(xx, yy, .5)
qp.errorbars(xx, yy, dy)
qp.overlinemin(15)
qp.overline(xx, yy+dy, '*')
