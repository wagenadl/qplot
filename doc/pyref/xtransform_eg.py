import qplot as qp
import numpy as np

qp.figure('xtransform', 3, 3)

xx = np.exp(np.random.randn(100))
yy = np.random.randn(100)

qp.xtransform(lambda x: np.log10(x))

qp.marker('o', 2)
qp.mark(xx, yy)
qp.xaxis(ticks=[.1, 1, 10], y=-3)
qp.minorticks(np.arange(.2,1,.1))
qp.minorticks(np.arange(2,10,1))
qp.yaxis(ticks=qp.arange(-2,2,1), x=np.exp(-3))
