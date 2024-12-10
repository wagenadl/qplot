import qplot as qp
import numpy as np

qp.figure('imsc', 3, 3)

xx, yy = np.meshgrid(range(11), range(11))
zz = np.cos(xx) + np.sin(yy)
qp.luts.set("jet", 100)
qp.imsc(zz, xx=xx, yy=yy, c0=-2, c1=2)
qp.xaxis('X', [0, 5, 10], y=-0.5, lim=[-0.5, 10.5])
qp.yaxis('Y', [0, 5, 10], x=-0.5, lim=[-0.5, 10.5])
qp.cbar(width=10)
qp.caxis()
