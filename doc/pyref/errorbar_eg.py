import pyqplot.all as qp

qp.figure('errorbar', 3, 3)

tt = [-pi:.5:pi]'

qp.marker o solid
qp.mark(tt, sin(tt))

qp.errorbar(tt, sin(tt), .2*cos(tt)+.3, 5)

qp.marker o solid
qp.mark(tt, 2+sin(tt-1))

qp.errorbar(tt, 2+sin(tt-1), [.3+zeros(size(tt)), .2*cos(tt)+.3])
