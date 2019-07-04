import pyqplot as qp
import numpy as np

qp.figure('garea', 3, 3)

xx = np.linspace(-np.pi, np.pi, 50)
qp.plot(xx, np.sin(xx))

qp.pen('none')
qp.brush('r', .5)

qp.garea([[qp.AbsData(0, 0)],
          [qp.AbsData(0, 0), qp.RelPaper(0, 36)],
          [qp.AbsData(1, np.sin(1)), qp.RelPaper(0, 36)],
          [qp.AbsData(1, np.sin(1))]])


