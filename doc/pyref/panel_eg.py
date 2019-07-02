import pyqplot as qp
import numpy as np

qp.figure('panel', 3, 3)
xx=[0:.01:3*pi]

qp.plot(xx, sin(xx))
qp.shrink 1

qp.pen dash
qp.brush 777

qp.panel('B', [2.1 2.3 .9 .7]*72)

qp.pen solid
qp.plot(xx, cos(xx))
qp.shrink 5
