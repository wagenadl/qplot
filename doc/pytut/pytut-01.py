import sys
sys.path.append('../../..')
import numpy as np
import qplot as qp

x = np.arange(-10, 10, 0.1)
qp.plot(x, np.sin(x));

qp.shrink
qp.save('pytut-02-01.png', 96);

qp.xaxis(ticks=np.arange(-10, 10, 5), y=-1.1)
qp.xaxis('Time', lim=[-10, 10], y=-1.4)
qp.xaxis('Angle', ticks=[-2*np.pi, 0, 2*np.pi], labels=['-2π', '0', '2π'], lim=[-10, 10], y=-1.7)


qp.shrink()
qp.save('pytut-02-02.png', 96)

qp.font('Times', 15, bold=True)
qp.axshift(5)
qp.ticklen(10)
qp.textdist(5)
qp.yaxis('Height', ticks=[-1,0,1], x=-10)

qp.shrink()
qp.save('pytut-02-03.png', 96)
