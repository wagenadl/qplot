import pyqplot.all as qp

qp.figure('textonpath', 3, 3)

xx = [0:.01:10]
yy = cos(xx)
qp.pen 1
qp.plot(xx, yy)
qp.ylim -10 10
qp.font Helvetica 14

qp.align center base
qp.textonpath(xx, yy, -3, 'This text follows the curve')

qp.shrink
