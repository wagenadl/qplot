import qplot as qp
import numpy as np

qp.figure('caxis', 3, 3)

xx = np.tile(np.arange(11), (11,1))
yy = np.transpose(xx)
zz = np.cos(xx) * np.sin(yy)
qp.imsc(zz, [0, 0, 1, 1], c0=-1, c1=1)
qp.cbar()

qp.caxis('', np.arange(-1,1.1,1), ['negv', '0', 'posv'])
qp.caxis('', np.arange(-1,1.1,.2), [], flip=True)

qp.hcbar()
qp.caxis('', [-1, 0, 1])
qp.caxis('', [-.5, .5], [], flip=True)

