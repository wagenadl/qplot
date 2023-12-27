import qplot as qp
import numpy as np

qp.figure('current', 3, 3)
qp.plot(np.arange(0, 10, .1), np.cos(np.arange(0, 10, .1)))

fn = qp.current()

print(fn)

