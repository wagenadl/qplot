import qplot as qp
import numpy as np

qp.figure('ytitlerot', 3, 3)

qp.ytitlerot(1)
qp.yaxis('Normal', np.arange(6))

qp.ytitlerot(0)
qp.yaxis('Upright', np.arange(6), x=1)

qp.ytitlerot(-1)
qp.yaxis('Reverse', np.arange(6), x=2)

qp.yaxis('', np.arange(6), x=3)
qp.at('left', 5)
qp.align('right', 'middle')
qp.reftext('5')
qp.text('Manual', -5, 0)

qp.shrink()
