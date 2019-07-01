import pyqplot.all as qp

qp.figure('overline', 3, 3)

xx = [1 2]
yy = [3 4]
dy = [.5 .75]
qp.bars(xx, yy, .5)
qp.errorbar(xx, yy, dy)

qp.overline(xx, max(yy+dy), '*')

xx = [3.5 4.5]
qp.bars(xx, yy, .5)
qp.errorbar(xx, yy, dy)

qp.overline(xx, yy+dy, '+')

qp.shrink
