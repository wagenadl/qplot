import pyqplot.all as qp

qp.figure('axshift', 3, 3)
qp.plot([-pi:.1:pi], sin([-pi:.1:pi]))

qp.axshift 10

qp.xaxis(-1, [-pi 0 pi], {'π', '0', 'π'})
qp.yaxis(-pi,[-1:1])
qp.shrink
