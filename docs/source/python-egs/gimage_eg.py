import qplot as qp
import numpy as np

qp.figure('gimage', 3, 3)

xx1 = np.array([0, 10])
qp.plot(xx1, xx1)
qp.plot(xx1, 10 - xx1)
xx, yy = np.meshgrid(range(10), range(10))
r = xx/10
g = yy/10
b = .5+0*xx
img = np.dstack((r,g,b))

qp.gimage(img, [2, 2, 0, 0], np.array([0, -2, 2, 2])*72)

