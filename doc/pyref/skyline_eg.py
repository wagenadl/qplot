import qplot as qp
import numpy as np

qp.figure('skyline', 3, 3)
xx = np.linspace(0, 1, 20)**2 * 2*np.pi
yy = np.sin(xx)
qp.brush('666')

qp.skyline(xx, yy)
