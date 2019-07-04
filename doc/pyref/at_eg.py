import pyqplot as qp
import numpy as np

qp.figure('at', 3, 3)
qp.plot([0, 1, 2, 3, 4], [0, 1, 4, 2, 5])
qp.align('top', 'left')

qp.at(1, 1)
qp.text('one', dx=3, dy=3)

qp.at(2, 4, -np.pi/4)
qp.text('two', dx=3, dy=3)
qp.at('right', 'bottom', id='A')

qp.at(3, 2, (4-3), (5-2))
qp.text('three', dx=3, dy=3)

qp.at(id='A')
qp.text('four', dx=3, dy=3)
