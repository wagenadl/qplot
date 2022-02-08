import qplot as qp
import numpy as np

qp.figure('align', 3, 3)

qp.pen('777')
qp.plot([-1, 1], [0, 0])
qp.plot([-1, 1], [.5, .5])
qp.plot([-1, 1], [-.5, -.5])

qp.plot([0, 0], [-1, 1])
qp.plot([.5, .5], [-1, 1])
qp.plot([-.5, -.5], [-1, 1])

qp.pen('k')

qp.at(0, 0)
qp.align('center', 'middle')
qp.text('Center/Middle')

qp.at(0.5, 0)
qp.align('left', 'base')
qp.text('Left/Base')

qp.at(-.5, 0)
qp.align('right')
qp.text('Right/Base')

qp.at(0, .5)
qp.align('bottom', 'center')
qp.text('Bottom')

qp.at(0, -.5)
qp.align('top', 'center')
qp.text('Top')
