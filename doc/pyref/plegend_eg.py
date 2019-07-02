import pyqplot as qp
import numpy as np

qp.figure('plegend', 3, 3)

qp.legopt('x', 2*pi, 'y', 1, 'dx', 10)

xx=[0:.1:2*pi]

qp.pen none
qp.brush b .5
qp.bars(xx, cos(xx), .1)

qp.plegend('Cosine')

qp.brush r .5
qp.bars(xx, sin(xx), .1)

qp.plegend('Sine')

qp.shrink
