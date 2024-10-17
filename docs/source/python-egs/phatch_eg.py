
import qplot as qp
import numpy as np

qp.figure('phatch', 3, 3)

qp.marker('o', 3)
qp.mark([1, 3], [2, 1])

qp.at(1, 2)
qp.pen('none')
qp.brush('b')
qp.marker('d', 5, 'brush')

qp.phatch([10, 30, 30, 10], [10, 10, 30, 30], pattern=':', spacing=7)

qp.at(3, 1)
qp.pen('r', .5)

qp.phatch([10, 20, 30, 20], [-10, 0, -10, -20], pattern='x', spacing=5)

qp.shrink()
