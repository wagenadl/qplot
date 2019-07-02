import pyqplot as qp
import numpy as np

qp.figure('caligraph', 3, 3)

qp.plot([0 1], [0 0])
qp.plot([0 0], [0 1])
qp.plot([0 -1/3], [0 -2/3])

phi = [-.9*pi:.1:.9*pi]
xx = sin(phi)
yy = -cos(phi)
ww = 1.5*(1-yy)
xx=xx/10
yy=1+yy/30

qp.caligraph(xx, yy, ww)

qp.at(xx(end), yy(end), xx(end)-xx(end-1), yy(end)-yy(end-1))
qp.brush k
qp.arrow(6,4,-2,1.5)

qp.shrink(1,1)
