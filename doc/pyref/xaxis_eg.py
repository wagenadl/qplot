import pyqplot as qp
import numpy as np

qp.figure('xaxis', 3, 3)

qp.xaxis(0, np.arange(6))

qp.xaxis(1, np.arange(6), ['zero', 'one', 'two', 'three', 'four', 'five'])

qp.xaxis(2, np.arange(6), title='x-axis')

qp.xaxis(3, np.arange(1,5), lim=[0, 5])

qp.xaxis(4, np.arange(6), [])

qp.xaxis(5, np.arange(6), title='top orientation', flip=True)

qp.shrink()
