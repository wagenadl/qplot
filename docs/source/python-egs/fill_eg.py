import qplot as qp
import numpy as np

qp.figure('fill', 3, 3)
qp.brush('g')

xx = np.linspace(0, 2*np.pi, 7)
qp.fill(np.cos(xx), np.sin(xx))

qp.brush('r', .5)

qp.fill(np.sin(xx), np.cos(xx))

