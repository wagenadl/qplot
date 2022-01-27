import qplot as qp
import numpy as np

qp.figure('sharelim', 3, 3)

qp.relpanel('A', (0, 0, 1, .5))
xx = np.arange(100)
qp.plot(xx, np.sqrt(xx))
qp.xaxis(ticks=[0,50,100])
qp.yaxis(ticks=[0,2,4,6,8,10])
qp.shrink()

qp.relpanel('B', (0, .5, 1, .5))
xx = np.arange(50,150)
qp.plot(xx, 20+2*np.cos(xx/10))
qp.axshift(5)
qp.xaxis(ticks=[50,100,150], y=18)
qp.yaxis(ticks=[18,20,22],x=50)
qp.shrink()

qp.sharelim(ids='A')
