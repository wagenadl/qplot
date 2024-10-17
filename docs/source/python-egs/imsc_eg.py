import qplot as qp
import numpy as np

qp.figure('imsc', 3, 3)

xx = np.tile(np.arange(11), (11,1))
yy = np.transpose(xx)
zz = np.cos(xx) + np.sin(yy)
qp.luts.set("jet", 100)
qp.imsc(zz, xx=xx, yy=yy, c0=-2, c1=2)
qp.xaxis('X', [0,5,10], y=-.5, lim=[-.5, 10.5])
qp.yaxis('Y', [0,5,10], x=-.5, lim=[-.5, 10.5])
qp.cbar(width=10)
qp.caxis()
