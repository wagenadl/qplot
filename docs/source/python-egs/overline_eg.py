import qplot as qp
import numpy as np

qp.figure('overline', 3, 3)

xx = [1, 2]
yy = np.array([3, 4])
dy = np.array([.5, .75])
qp.bars(xx, yy, .5)
qp.errorbars(xx, yy, dy)

qp.overline(xx, np.max(yy+dy), '*')

xx = [3.5, 4.5]
qp.bars(xx, yy, .5)
qp.errorbars(xx, yy, dy)

qp.overline(xx, yy+dy, '+')
