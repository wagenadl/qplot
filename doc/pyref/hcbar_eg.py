import pyqplot.all as qp

qp.figure('hcbar', 3, 3)

xx = repmat([1:10], 10, 1)
yy = xx'
zz = cos(xx).*sin(yy)
qp.imsc([0 0 1 1], zz, -1, 1)
qp.axshift 5
qp.hcbar(0, 0, 1)
qp.axshift 0
qp.caxis([-1:1:1], {'negative', '0', 'positive'})

qp.shrink(1, 1)
