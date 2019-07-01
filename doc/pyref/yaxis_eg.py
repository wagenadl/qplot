import pyqplot.all as qp

qp.figure('yaxis', 3, 3)

qp.yaxis(0, [0:5])

qp.yaxis(1, [0:5], {'zero', 'one', 'two', 'three', 'four', 'five'})

qp.yaxis(2, [0:5], [])

qp.yaxis('r', 3, [0:5], 'right orientation')

qp.yaxis('R', 4, [0 5], [1:4], 'flipped title')

qp.shrink
