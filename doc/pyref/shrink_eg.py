import pyqplot as qp
import numpy as np

qp.figure('shrink', 3, 3)

qp.brush 888
qp.pen none
qp.panel('A', [.25 .25 2.5 1]*72)
qp.pen k solid
qp.plot(0:.1:2*pi,sin(0:.1:2*pi))
qp.xaxis(-1,[0 pi 2*pi],{'0','π','2π'})
qp.yaxis(0,-1:1)

qp.brush 888
qp.pen none
qp.panel('B', [.25 1.75 2.5 1]*72)
qp.pen k solid
qp.plot(0:.1:2*pi,sin(0:.1:2*pi))
qp.xaxis(-1,[0 pi 2*pi],{'0','π','2π'})
qp.yaxis(0,-1:1)

qp.shrink
