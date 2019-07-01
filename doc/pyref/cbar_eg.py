import pyqplot.all as qp

qp.figure('cbar', 3, 3)

xx = repmat([1:10], 10, 1)
yy = xx'
zz = cos(xx).*sin(yy)
qp.imsc([0 0 1 1], zz, -1, 1)
qp.at 1 1
qp.cbar(10, 2.5*72, 10, 10)

qp.caxis([-1:1:1], {'negv', '0', 'posv'})

qp.shrink
