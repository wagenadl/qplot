import qplot as qp
import numpy as np

qp.figure('pen', 3, 3)

qp.pen('r', 2, id='A')
qp.plot([0, 1],[0, 0])

qp.pen('b', pattern=('dash', [10, 6, 1, 6]))
qp.plot([0, 1],[1, 1])

qp.pen('930', pattern=('dot', 6))
qp.plot([0, 1], [2, 2])

qp.pen([1, 0, 1], pattern='solid')
qp.plot([0, 1], [3, 3])

qp.pen('k', 10, join='miter', cap='round')
qp.plot([.3, .5, .7],[.2, .8, .2])

qp.pen('k', 10, join='round', cap='square')
qp.plot([.3, .5, .7], np.array([.2, .8, .2])+1)

qp.pen('k', join='bevel', cap='flat', width=10)
qp.plot([.3, .5, .7], np.array([.2, .8, .2])+2)

qp.pen(id='A')
qp.plot([.4, .6], [.2, .2])
