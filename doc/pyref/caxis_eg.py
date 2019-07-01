import pyqplot.all as qp

qp.figure('caxis', 3, 3)

xx = repmat([1:10], 10, 1)
yy = xx'
zz = cos(xx).*sin(yy)
qp.imsc([0 0 1 1], zz, -1, 1)
qp.at 1 0
qp.cbar(10, [], 10, 0, 1)

qp.caxis([-1:1:1], {'negv', '0', 'posv'})
qp.caxis('l', [-1:.2:1],{})

qp.at 0 0
qp.cbarh([], 10, 0, 10, 1)
qp.caxis([-1:1:1])
qp.caxis('t', [-1:.5:1],{})


qp.shrink
