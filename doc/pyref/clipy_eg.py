import qplot as qp
import numpy as np

qp.figure('clipy', 3, 3)

xx = np.linspace(0, 4*np.pi, 100)
yy = np.sin(xx)
xx1, yy1 = qp.clipy(xx, yy, -.8, .8)

qp.plot(xx1, yy1)
