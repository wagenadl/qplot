import qplot as qp
import numpy as np

qp.figure('plot', 3, 3)

xx = np.arange(0, 2*np.pi, .1)

qp.plot(xx, np.sin(xx))

yy = np.cos(xx)
yy[np.abs(yy)<.1] = np.nan

qp.plot(xx, yy)
