import qplot as qp
import numpy as np

qp.figure('zyimage', 3, 3)

xx = np.repeat(np.reshape(np.arange(10), (1,10,1)), 10, 0)
yy = np.transpose(xx, (1,0,2))
img = np.concatenate((xx/10,yy/10,.5+0*xx), 2)

qp.zyimage(img, [0, 0, 10, 10], [-.4, -.6])
qp.xaxis('X', np.arange(0,11,2), flip=False)
qp.yaxis('Y', np.arange(0,11,2), flip=True)
qp.zaxis('Z', np.arange(0,11,2), [-.4,-.6], below=True)

qp.shrink()
