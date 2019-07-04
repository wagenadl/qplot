import pyqplot as qp
import numpy as np

qp.figure('title', 3, 3)

xx = np.linspace(0, 2*np.pi, 50)
qp.plot(xx, np.sin(xx))

qp.title('Sine wave')

