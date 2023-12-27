import qplot as qp
import numpy as np
import time

qp.figure('', 3, 3)
qp.plot(np.arange(0, 10, .1), np.cos(np.arange(0, 10, .1)))
time.sleep(1)

qp.close()
