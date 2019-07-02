import pyqplot as qp
import numpy as np

qp.figure('ytitlerot', 3, 3)

qp.ytitlerot(1)
qp.yaxis(0, np.arange(6), title='Normal')

qp.ytitlerot(0)
qp.yaxis(1, np.arange(6), title='Upright')

qp.ytitlerot(-1)
qp.yaxis(2, np.arange(6), title='Reverse')

qp.yaxis(3, np.arange(6))
qp.at('left', 5)
qp.align('right', 'middle')
qp.reftext('5')
qp.text('Manual', -5, 0)

qp.shrink()
