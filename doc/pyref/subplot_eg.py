import qplot as qp
import numpy as np

qp.figure('subplot', 3, 3)

qp.subplot(2,1,1)
xx=np.linspace(0, 2*np.pi, 50)
qp.plot(xx, np.cos(xx))
qp.shrink(10)

qp.subplot(2,1,2)

qp.plot(xx, np.sin(xx))
qp.shrink(10)
