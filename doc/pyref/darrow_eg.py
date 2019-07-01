import pyqplot.all as qp

qp.figure('darrow', 3, 3)

tt = [0:.1:4*pi]
xx = sin(tt/2)
yy = sin(tt)
qp.pen 666
qp.plot(xx, yy)

qp.brush k
qp.pen k

for n=5:10:length(xx):
    qp.darrow(xx(n), yy(n), [xx(n)-xx(n-1), yy(n)-yy(n-1)])
