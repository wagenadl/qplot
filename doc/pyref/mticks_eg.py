import pyqplot.all as qp

qp.figure('mticks', 3, 3)

qp.plot(0:.1:2*pi, sin(0:.1:2*pi))
qp.axshift 10
qp.ticklen 5
qp.xaxis(-1, [0 pi 2*pi], {'0', 'π', '2π'})
qp.ticklen 3

qp.mticks([0:pi/4:2*pi])

qp.shrink
