import qplot as qp
import numpy as np

qp.figure('textdist', 3, 3)

qp.textdist(10)
qp.xaxis('Title A', np.arange(6), y=3)

qp.textdist(3)
qp.xaxis('Title B', np.arange(6), y=2)

qp.textdist(-3, 3)
qp.xaxis('Title C', np.arange(6), y=1)

qp.textdist(3, -10)
qp.xaxis('Title D', np.arange(6), y=0)

qp.shrink()
