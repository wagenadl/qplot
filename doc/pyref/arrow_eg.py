import pyqplot as qp
import numpy as np

qp.figure('arrow', 3, 3)
qp.plot([0, 1, 2, 3],[0, 3, 1, 4])

qp.brush('k')
qp.at(1, 3, along=(0, -1))
qp.arrow()

qp.at(2, 1, along=(1, 1))
qp.arrow(20, 15, 5, 5)

