import qplot as qp
import numpy as np
import matplotlib.pyplot as plt

qp.figure('lut', 3, 3)

xx = np.linspace(0, 2*np.pi, 101)
xx = np.tile(xx, (len(xx), 1))
yy = np.transpose(xx)
zz = np.cos(xx)+np.sin(yy)

qp.subplot(2,2,0)
qp.imsc(zz)
qp.cbar()
qp.shrink(5)

qp.subplot(2,2,1)
qp.lut(qp.luts.get('qphsv'))
qp.imsc(zz)
qp.cbar()
qp.shrink(5)

qp.subplot(2,2,2)
qp.lut(qp.luts.get('qpcoldhot'))
qp.imsc(zz)
qp.cbar()
qp.shrink(5)

qp.subplot(2,2,3)
qp.lut(plt.cm.get_cmap('rainbow', 256))
qp.imsc(zz)
qp.cbar()
qp.shrink(5)

