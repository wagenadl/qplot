import pyqplot as qp
import numpy as np

qp.figure('ytitlerot', 3, 3)

qp.ytitlerot 1
qp.yaxis(0, [0:5], 'Normal')

qp.ytitlerot 0
qp.yaxis(1, [0:5], 'Upright')

qp.ytitlerot -1
qp.yaxis(2, [0:5], 'Reverse')

qp.yaxis(3, [0:5])
qp.at left 5
qp.align right middle
qp.reftext '5'
qp.text(-5, 0, 'Manual')

qp.shrink
