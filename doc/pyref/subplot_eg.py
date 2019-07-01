import pyqplot.all as qp

qp.figure('subplot', 3, 3)

qp.subplot(0, 0, 1, .5)

qp.plot(0:.1:2*pi, cos(0:.1:2*pi))
qp.shrink 10

qp.subplot(0, .5, 1, .5)

qp.plot(0:.1:2*pi, sin(0:.1:2*pi))
qp.shrink 10
