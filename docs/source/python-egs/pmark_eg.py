import qplot as qp
import numpy as np

qp.figure('pmark', 3, 3)

xx = [1, 2, 3]
yy = [3, .5, 1.5]
qp.brush('555')
qp.bars(xx, yy, .5)

mrks='+-x'
for k in range(3):
    qp.at(xx[k], yy[k])
    qp.marker(mrks[k])
    qp.pmark(0,-10)
