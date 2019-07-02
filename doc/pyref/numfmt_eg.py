import pyqplot as qp
import numpy as np

qp.figure('numfmt', 3, 3)

qp.xaxis(0, [0:.5:2])

qp.numfmt('#.1f')
qp.yaxis(0, [0:.5:2])

qp.numfmt('#.3f')
qp.yaxis(.75,[0.5:.125:1])

qp.numfmt('')
qp.yaxis(1.5,[0.5:.125:1]
