import pyqplot.all as qp

qp.figure('bars', 3, 3)
qp.brush 777

qp.bars([0:4*pi], sin([0:4*pi]), 0.5)
