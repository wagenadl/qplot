import qplot as qp
import numpy as np

qp.figure('ytransform', 3, 3)

yy = np.exp(np.random.randn(100))
xx = np.random.randn(100)

qp.ytransform(lambda x: np.log10(x))

qp.marker('o', 2)
qp.mark(xx, yy)
qp.yaxis(ticks=[.1, 1, 10], x=-3)
qp.minorticks(np.arange(.2,1,.1))
qp.minorticks(np.arange(2,10,1))
qp.xaxis(ticks=qp.arange(-2,2,1), y=np.exp(-3))
