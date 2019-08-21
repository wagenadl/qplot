import pyqplot as qp
import numpy as np

qp.figure('ctext_eg', 3, 3)

xx = np.array([1,2])
yy = np.array([2,1])

qp.marker('o')
qp.mark(xx, yy)
qp.at(1, 2)
qp.text('One', dy=20)
qp.ctext('Two', dx=5)
qp.ctext('Three', dx=10)
qp.ctext('Four', dy=5)

