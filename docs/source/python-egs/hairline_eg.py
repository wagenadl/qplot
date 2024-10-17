import qplot as qp
import numpy as np

qp.figure('hairline', 3, 3)
qp.hairline(1)
qp.plot(np.arange(6), np.mod(np.arange(6), 2))
