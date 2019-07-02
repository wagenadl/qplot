import pyqplot as qp
import numpy as np

qp.figure('xaxis', 3, 3)

qp.xaxis(0, [0:5])

qp.xaxis(1, [0:5], {'zero', 'one', 'two', 'three', 'four', 'five'})

qp.xaxis(2, [0:5], 'x-axis')

qp.xaxis(3, [0 5], [1:4])

qp.xaxis(4, [0:5], {})

qp.xaxis('t', 5, [0:5], 'top orientation')

qp.shrink
