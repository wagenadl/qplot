import qplot as qp
import numpy as np

qp.figure('commonscale', 3, 3)

idA = qp.subplot(2,1,0)
xx = np.arange(75)
qp.plot(xx, np.sqrt(xx))
qp.xaxis(ticks=[0,25,50,75])
qp.yaxis(ticks=[0,2,4,6,8,10])
qp.shrink()

idB = qp.subplot(2,1,1)
xx = np.arange(25,125)
qp.plot(xx, 20+2*np.cos(xx/10))
qp.axshift(5)
qp.xaxis(ticks=[25,50,75,100,125], y=18)
qp.yaxis('Sinusoid', ticks=[18,20,22],x=25)
qp.shrink()

qp.commonscale('xy', [idA, idB])
