import pyqplot as qp
import numpy as np

qp.figure('save', 3, 3)

qp.plot(0:.1:2*pi,sin(0:.1:2*pi))

qp.save('save.pdf')
qp.save('save.png')
qp.save('save.jpg')
qp.save('save.svg')
