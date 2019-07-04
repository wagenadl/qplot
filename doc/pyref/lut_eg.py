import pyqplot as qp
import numpy as np
import matplotlib.pyplot as plt
import cv2

qp.figure('lut', 3, 3)

xx = np.linspace(0, 2*np.pi, 101)
xx = np.tile(xx, (len(xx), 1))
yy = np.transpose(xx)
zz = np.cos(xx)+np.sin(yy)

qp.imsc(zz, [0, 0, 1, 1])
qp.cbar()

c = plt.cm.get_cmap('rainbow')
qp.lut(c(range(c.N)))
qp.imsc(zz, [0, 1.1, 1, 1])
qp.cbar()

c = plt.cm.get_cmap('seismic')
qp.lut(c(range(c.N)))
qp.imsc(zz, [1.5, 0, 1, 1])
qp.cbar()

c = plt.cm.get_cmap('YlOrRd')
qp.lut(c(range(c.N)))
qp.imsc(zz, [1.5, 1.1, 1, 1])
qp.cbar()


