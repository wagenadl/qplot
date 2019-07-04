import pyqplot as qp
import numpy as np

qp.figure('numformat', 3, 3)

qp.xaxis('', [0, .5, 1, 1.5, 2])

qp.numformat('%.1f')
qp.yaxis('', [0, .5, 1, 1.5, 2])

qp.numformat('%.3f')
qp.yaxis('', np.arange(.5, 1.01, .125), x=.75)

qp.numformat('')
qp.yaxis('', np.arange(.5, 1.01, .125), x=1.5)
