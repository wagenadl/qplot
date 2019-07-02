import pyqplot as qp
import numpy as np

qp.figure('area', 3, 3)

qp.area([1 2 2 1]*72, [1 1 2 2]*72)
qp.area([2.5 2.5 2]*72, [2 2.5 2.5]*72)
