import qplot as qp
import numpy as np

qp.figure('zaxis', 3, 3)

qp.xaxis('X', np.arange(6))
qp.yaxis('Y', np.arange(6))
qp.zaxis('Z', np.arange(6), [-.4,-.6])
