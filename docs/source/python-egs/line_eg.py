import qplot as qp
import numpy as np

qp.figure('line', 3, 3)

xx = np.linspace(-np.pi, np.pi, 50)
yy = np.sin(xx)

qp.plot(xx, yy)

dx = np.diff(xx)
dy = np.diff(yy)

for n in range(2, len(xx)-1, 5):
    qp.at(xx[n], yy[n], along=(dx[n], dy[n]))
    qp.line([0, 0],[-5, 5])
