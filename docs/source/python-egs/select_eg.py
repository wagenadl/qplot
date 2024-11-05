import qplot as qp
import numpy as np

qp.figure('select_one', 3, 3)
xx = np.linspace(0,2*np.pi,50)
qp.plot(xx, np.sin(xx))

qp.figure('select_two', 4, 2)
qp.plot(xx, np.cos(xx))

qp.select('select_one')
qp.plot(xx, -np.sin(xx))
