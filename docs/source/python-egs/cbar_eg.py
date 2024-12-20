import qplot as qp
import numpy as np

qp.figure('cbar', 3, 3)

xx = np.tile(np.linspace(0,3*np.pi,101), (101,1))
yy = np.transpose(xx)
zz = np.cos(xx) * np.sin(yy)
qp.imsc(zz, [0, 0, 1, 1], c0=-1, c1=1)

qp.cbar()

qp.caxis('', [-1, 0, 1], ['negative', '0', 'positive'], axshift=2, ticklen=4)
qp.minorticks(np.arange(-.75, 1, .25))
