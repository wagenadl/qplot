import pyqplot as qp
import numpy as np

qp.figure('shiftedline', 3, 3)

xx = np.array([1,2])
yy = np.array([2,1])

qp.marker('o')
qp.mark(xx, yy)
qp.shiftedline(xx, yy, np.array([-5, 5]), -15)

