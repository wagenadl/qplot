import pyqplot as qp
import numpy as np

qp.figure('legend', 3, 3)

qp.legopt('x', 2*pi, 'y', 1, 'dx', 10)

xx=[0:.1:2*pi]

qp.pen b
qp.plot(xx, cos(xx))

qp.legend('Cosine')

qp.pen r
qp.plot(xx, sin(xx))

qp.legend('Sine')

qp.shrink
