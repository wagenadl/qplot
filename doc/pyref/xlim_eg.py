import pyqplot.all as qp

qp.figure('xlim', 3, 3)

qp.pen 777
qp.panel('A', 20,20,3*72-40,1.5*72-40)
qp.pen k
qp.plot(0:.1:2*pi, sin(0:.1:2*pi))
qp.xaxis(-1, [0 pi 2*pi], {'0','π','2π'})

qp.xlim -5 10

qp.pen 777
qp.panel('B', 20,20+1.5*72,3*72-40,1.5*72-40)
qp.pen k
qp.plot(0:.1:2*pi, sin(0:.1:2*pi))
qp.xaxis(-1, [0 pi 2*pi], {'0','π','2π'})
qp.xlim 1 6

qp.panel -
