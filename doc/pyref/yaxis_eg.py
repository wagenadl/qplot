import qplot as qp
import numpy as np

qp.figure('yaxis', 3, 3)

qp.yaxis('', np.arange(6))

qp.yaxis('', np.arange(6), ['zero', 'one', 'two', 'three', 'four', 'five'], x=1)

qp.yaxis('', np.arange(6), [], x=2)

qp.yaxis('right orientation', np.arange(6), flip=True, x=3)

qp.yaxis('flipped title', np.arange(1,5), lim=[0,5], flip=2, x=4)

