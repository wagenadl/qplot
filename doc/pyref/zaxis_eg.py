import pyqplot as qp
import numpy as np

qp.figure('zaxis', 3, 3)

qp.xaxis(0, np.arange(6), title='X')
qp.yaxis(0, np.arange(6), title='Y')
qp.zaxis((0, 0), [-.4,-.6], np.arange(6), title='Z')

qp.shrink()
