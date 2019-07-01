import pyqplot.all as qp

qp.figure('mlegend', 3, 3)

qp.legopt('x', 5, 'y', 5, 'dx', 10, 'width', 5)

qp.pen b
qp.marker x
qp.mark(randn(50,1), randn(50,1))

qp.mlegend('1 x 1')

qp.pen r
qp.marker +
qp.mark(randn(50,1)/2, randn(50,1)*2)

qp.mlegend('0.5 x 2')

qp.pen 080
qp.brush none
qp.marker o brush
qp.mark(randn(50,1)*2, randn(50,1)/2)

qp.mlegend('2 x 0.5')

qp.shrink(1, 1)
