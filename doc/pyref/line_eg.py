import pyqplot.all as qp

qp.figure('line', 3, 3)

xx=[-pi:.1:pi]
yy=sin(xx)

qp.plot(xx, yy)

for n=4:5:length(xx)-1:
    qp.at(xx(n), yy(n), xx(n+1)-xx(n), yy(n+1)-yy(n))
    qp.line([0 0],[-5 5])
