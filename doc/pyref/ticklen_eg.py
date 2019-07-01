import pyqplot.all as qp

qp.figure('ticklen', 3, 3)

qp.ticklen 3
qp.xaxis(0, [0:5], 'Title')

qp.ticklen -3
qp.xaxis(1, [0:5], 'Title')

qp.ticklen 10
qp.xaxis(2, [0:5], 'Title')

qp.ticklen -10
qp.xaxis(3, [0:5], 'Title')

qp.shrink
