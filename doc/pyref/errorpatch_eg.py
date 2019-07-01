import pyqplot.all as qp

qp.figure('errorpatch', 3, 3)

tt = [-pi:.1:pi]'

qp.brush 555
qp.pen none

qp.errorpatch(tt, sin(tt), .2*cos(tt)+.3, 5)

qp.pen k 1
qp.plot(tt, sin(tt))
