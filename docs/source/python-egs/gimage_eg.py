import qplot as qp
import numpy as np

qp.figure('gimage', 3, 3)

xx = np.tile(np.arange(10), (10,1))
yy = np.transpose(xx)
r = xx/10
g = yy/10
b = .5+0*xx
img = np.dstack((r,g,b))
qp.gimage(img, [np.nan, np.nan, 0, 0], np.array([.5, .5, 2, 2])*72)

