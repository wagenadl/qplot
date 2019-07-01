import pyqplot.all as qp

qp.figure('legopt', 3, 3)

qp.legopt('x', 2*pi, 'y', 1, 'dx', 10, 'height', 16, 'skip', 20, 'drop', 5)
qp.font Helvetica 16

xx=[0:.1:2*pi]

qp.pen none
qp.brush b .5
qp.bars(xx, cos(xx), .1)

qp.legopt('color', 'b')

qp.plegend('Cosine')

qp.brush r .5
qp.bars(xx, sin(xx), .1)

qp.legopt('color', 'r')

qp.plegend('Sine')

qp.shrink
