import qplot as qp
import numpy as np

qp.figure('garea2', 3, 3)

xx = np.linspace(-np.pi, np.pi, 50)
qp.plot(xx, np.sin(xx))

qp.pen('none')
qp.brush('r', .5)

xxx = np.stack((xx, np.flip(xx, 0)))
yyy = np.stack((0*xx+36, 0*xx+72))

qp.garea2([qp.AbsData(xxx, np.sin(xxx)),
           qp.RelPaper(0*xxx, yyy)])


