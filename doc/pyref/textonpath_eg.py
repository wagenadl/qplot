import pyqplot as qp
import numpy as np

qp.figure('textonpath', 3, 3)

xx = np.linspace(0,10,1000)
yy = np.cos(xx)
qp.pen(width=1)
qp.plot(xx, yy)
qp.ylim(-10, 10)
qp.font('Helvetica', 14)

qp.align('center', 'base')
qp.textonpath(xx, yy, 'This text follows the curve', dy=-3)


