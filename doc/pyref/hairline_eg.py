import pyqplot.all as qp

qp.figure('hairline', 3, 3)

qp.hairline 1
qp.plot([0:5], mod([0:5],2))
