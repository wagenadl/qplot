import pyqplot as qp
import numpy as np

qp.figure('cbard', 3, 3)

xx = repmat([1:10], 10, 1)
yy = xx'
zz = cos(xx).*sin(yy)
qp.imsc([0 0 1 1], zz, -1, 1)
qp.cbard([1.1 0 .1 1])
qp.caxis([-1:1:1], {'negv', '0', 'posv'})

qp.cbard([0 1.1 1 .1],'h')
qp.caxis([-1:1:1], {'negv', '0', 'posv'})

qp.shrink
