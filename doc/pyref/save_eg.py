import pyqplot as qp
import numpy as np

qp.figure('save', 3, 3)
xx = np.linspace(0,2*np.pi,50)
qp.plot(xx, np.sin(xx))

qp.save('save.pdf')
qp.save('save.png')
qp.save('save.jpg')
qp.save('save.svg')
