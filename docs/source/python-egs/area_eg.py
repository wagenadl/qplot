import qplot as qp
import numpy as np

qp.figure('area', 3, 3)

qp.marker('o', 3)
qp.mark([1, 3], [2, 1])
qp.at(1, 2)

qp.area([10, 20, 20, 10], [10, 10, 20, 20])

qp.at(3, 1)
qp.area([10, 20, 30, 20], [-10, 0, -10, -20])

qp.shrink()
