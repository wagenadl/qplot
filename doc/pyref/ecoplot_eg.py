import pyqplot as qp
import numpy as np

qp.figure('ecoplot', 3, 3)

N = 1000000
tt = np.arange(N)
yy = (np.mod(tt, 100000)==30000).astype(float) \
     - (np.mod(tt, 130000)==45000).astype(float) \
     + np.random.randn(N)/15

qp.pen('k', 0)
qp.brush('k')

# Plot at 300 dpi but don't lose any spikes

qp.ecoplot(tt[0], tt[1]-tt[0], yy, 3*300)
