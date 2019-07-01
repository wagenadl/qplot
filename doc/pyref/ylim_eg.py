import pyqplot.all as qp

qp.figure('ylim', 3, 3)

qp.pen 777
qp.panel('A', 20,20,3*72-30,1.5*72-40)
qp.pen k
qp.plot(0:.1:2*pi, sin(0:.1:2*pi))
qp.yaxis(0, [-1:1])

qp.ylim -2 1.5

qp.pen 777
qp.panel('B', 20,20+1.5*72,3*72-30,1.5*72-40)
qp.pen k
qp.plot(0:.1:2*pi, sin(0:.1:2*pi))
qp.yaxis(0, [-1:1])

qp.ylim -.8 .8

qp.panel -
