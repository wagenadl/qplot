import qplot as qp
import numpy as np

qp.figure('mark', 3, 3)

qp.marker('o', fill='solid')

qp.mark(np.arange(1,6), np.cos(np.arange(1,6)))
