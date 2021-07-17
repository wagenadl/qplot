import pyqplot as qp
import numpy as np

qp.figure('ticklen', 3, 3)

qp.ticklen(3)
qp.xaxis('Positive', np.arange(6), y=0)

qp.ticklen(-3)
qp.xaxis('Negative', np.arange(6), y=1)

qp.ticklen(10)
qp.xaxis('Big', np.arange(6), y=2)

qp.shrink()
