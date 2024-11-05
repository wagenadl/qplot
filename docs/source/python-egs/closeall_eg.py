import qplot as qp
import numpy as np
import time

qp.figure('f1', 3, 3)
qp.figure('f2', 3, 3)
qp.figure('f3', 3, 3)
qp.figure('f4', 3, 3)
qp.mark([0,1], [0,1])
time.sleep(1)

qp.closeall()
