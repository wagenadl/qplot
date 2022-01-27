import qplot as qp
import numpy as np

qp.figure('bars', 3, 3)
qp.brush('777')

xx = np.arange(0,4*np.pi,1)
qp.bars(xx, np.sin(xx), 0.5)
