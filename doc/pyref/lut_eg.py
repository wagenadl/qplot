import pyqplot as qp
import numpy as np
import matplotlib.pyplot as plt

qp.figure('lut', 3, 3)

xx = np.linspace(0, 2*np.pi, 101)
xx = np.tile(xx, (len(xx), 1))
yy = np.transpose(xx)
zz = -xx #np.cos(xx)+np.sin(yy)

qp.imsc(zz, [0, 0, 1, 1])
qp.cbar()
qp.shrink()
'''
qp.lut(plt.cm.spectral(np.arange(plt.cm.spectral.N)))

qp.imsc(zz, [0, 1.1, 1, 1])
qp.cbar()

qp.lut(plt.cm.datad['bwr'])

qp.imsc(zz, [1.5, 0, 1, 1])
qp.cbar()

qp.lut(plt.cm.datad['hot'])
qp.imsc(zz, [1.5, 1.1, 1, 1])
qp.cbar()

'''
