import qplot as qp
import numpy as np

qp.figure('xaxis', 3, 3)

qp.xaxis('x-axis', np.arange(6))

qp.xaxis('', np.arange(6), ['zero', 'one', 'two', 'three', 'four', 'five'], y=1)

qp.xaxis('', np.arange(6), lambda x: '%g%%' % (10*x), y=2)

qp.xaxis('', np.arange(1,5), lim=[0, 5], y=3)

qp.xaxis('', np.arange(6), [], y=4)

qp.xaxis('top orientation', np.arange(6), y=5, flip=True)

qp.shrink()
