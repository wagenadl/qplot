import pyqplot.all as qp

qp.figure('gline', 3, 3)

xx=[-1.5*pi:1.5*pi]
yy=cos(xx)
qp.marker o solid
qp.mark(xx, yy)

N=length(xx)-1
for n=1:N:
    qp.gline({'absdata',xx(n),yy(n), 'retract', 10}, ...
            {'absdata',xx(n+1),yy(n+1), 'retract', 10})
