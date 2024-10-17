import qplot as qp
import numpy as np

qp.figure('image', 3, 3)

xx = np.repeat(np.reshape(np.arange(10), (1,10,1)), 10, 0)
yy = np.transpose(xx, (1,0,2))
img = np.concatenate((xx/10,yy/10,.5+0*xx), 2)

qp.image(img, [0, 0, 1, 1])

