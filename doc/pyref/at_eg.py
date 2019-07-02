import pyqplot as qp
import numpy as np

qp.figure('at', 3, 3)
qp.plot([0 1 2 3 4], [0 1 4 2 5])
qp.align top left

qp.at(1, 1)
qp.text(3, 3, 'one')

qp.at(2, 4, -pi/4)
qp.text(3, 3, 'two')
qp.at right bottom A

qp.at(3, 2, (4-3), (5-2))
qp.text(3, 3, 'three')

qp.at A
qp.text(3, 3, 'four')
