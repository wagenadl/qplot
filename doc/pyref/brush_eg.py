import pyqplot.all as qp

qp.figure('brush', 3, 3)

qp.brush 777
qp.patch([0 1 1 0], [0 0 1 1])

qp.brush A r .25
qp.patch([.5 1.5 1.5 .5], [.5 .5 1.5 1.5])

qp.brush none
qp.patch([.2 .7 .7 .2], [.8 .8 1.3 1.3])

qp.brush b
qp.patch([.2 .4 .4 .2], [.2 .2 .4 .4])

qp.brush A .75
qp.patch([1.2 1.4 1.4 1.2], [.3 .3 .8 .8])
