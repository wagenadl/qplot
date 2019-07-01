import pyqplot.all as qp

qp.figure('align', 3, 3)

qp.pen 777
qp.plot([-1 1], [0 0])
qp.plot([-1 1], [.5 .5])
qp.plot([-1 1], [-.5 -.5])

qp.plot([0 0], [-1 1])
qp.plot([.5 .5], [-1 1])
qp.plot([-.5 -.5], [-1 1])

qp.pen k

qp.at 0 0
qp.align center middle
qp.text 0 0 Center/Middle

qp.at 0.5 0
qp.align left base
qp.text 0 0 Left/Base

qp.at -.5 0
qp.align right
qp.text 0 0 Right/Base

qp.at 0 .5
qp.align bottom center
qp.text 0 0 Bottom

qp.at 0 -.5
qp.align top center
qp.text 0 0 Top
