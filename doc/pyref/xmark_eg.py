import pyqplot as qp
import numpy as np

qp.figure('xmark', 3, 3)

qp.marker('o', fill='solid')
for x in range(3):
    yy = np.random.randn(30) + x
    qp.xmark(x + np.zeros_like(yy), yy, rx=6)
