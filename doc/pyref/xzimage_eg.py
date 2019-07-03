import pyqplot as qp
import numpy as np

qp.figure('xzimage', 3, 3)

xx = np.repeat(np.reshape(np.arange(10), (1,10,1)), 10, 0)
yy = np.transpose(xx, (1,0,2))
img = np.concatenate((xx/10,yy/10,.5+0*xx), 2)

qp.xzimage(img, [0, 0, 10, 10], [-.4, -.6])
qp.xaxis(0, np.arange(0,11,2), title='X', flip=True)
qp.yaxis(0, np.arange(0,11,2), title='Y')
qp.zaxis((0, 0), [-.4,-.6], np.arange(0,11,2), title='Z')

qp.shrink()
