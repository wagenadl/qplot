import pyqplot.all as qp

qp.figure('area', 3, 3)

qp.area([1 2 2 1]*72, [1 1 2 2]*72)
qp.area([2.5 2.5 2]*72, [2 2.5 2.5]*72)
