import qplot as qp
import numpy as np

qp.figure('minorticks', 3, 3)

xx = np.linspace(0, 2*np.pi, 50)
qp.plot(xx, np.sin(xx))
qp.axshift(10)
qp.ticklen(5)
qp.xaxis('', [0, np.pi, 2*np.pi], ['0', 'π', '2π'], y=-1)

qp.minorticks(np.arange(0, 2*np.pi, np.pi/4), ticklen=3)

qp.shrink()
