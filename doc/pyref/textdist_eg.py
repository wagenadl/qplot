import pyqplot as qp
import numpy as np

qp.figure('textdist', 3, 3)

qp.textdist 10
qp.xaxis(0, [0:5], 'Title')

qp.textdist 3
qp.xaxis(1, [0:5], 'Title')

qp.textdist -3 3
qp.xaxis(2, [0:5], 'Title')

qp.textdist 3 -10
qp.xaxis(3, [0:5], 'Title')

qp.shrink
