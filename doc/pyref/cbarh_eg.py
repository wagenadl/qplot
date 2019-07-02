import pyqplot as qp
import numpy as np

qp.figure('cbarh', 3, 3)

xx = repmat([1:10], 10, 1)
yy = xx'
zz = cos(xx).*sin(yy)
qp.imsc([0 0 1 1], zz, -1, 1)
qp.at 0 0
qp.cbarh(2.5*72, 10, 5, 5)

qp.caxis([-1:1:1], {'negv', '0', 'posv'})

qp.shrink
