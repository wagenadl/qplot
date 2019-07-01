import pyqplot.all as qp

qp.figure('pen', 3, 3)

qp.pen A r 2
qp.plot([0 1],[0 0])

qp.pen('b', 'dash', [ 10 6 1 6])
qp.plot([0 1],[1 1])

qp.pen 930 dot 6
qp.plot([0 1], [2 2])

qp.pen([1 0 1], 'solid')
qp.plot([0 1], [3 3])

qp.pen k miterjoin roundcap 10
qp.plot([.3 .5 .7],[.2 .8 .2])

qp.pen k roundjoin sqp.uarecap 10
qp.plot([.3 .5 .7],[.2 .8 .2]+1)

qp.pen k beveljoin flatcap 10
qp.plot([.3 .5 .7],[.2 .8 .2]+2)

qp.pen A
qp.plot([.4 .6], [.2 .2])
