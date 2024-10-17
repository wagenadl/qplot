import qplot as qp
import numpy as np

qp.figure('ymark', 3, 3)

qp.marker('o', fill='solid')
for y in range(3):
    xx = np.random.randn(30) + y
    qp.ymark(xx, y + np.zeros_like(xx), rx=6)
