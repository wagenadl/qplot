import qplot as qp
import numpy as np

qp.figure('mm_eg', 3, 3)

phi = np.linspace(0, 2*np.pi, 100)
qp.plot(np.cos(phi), np.sin(phi))
cx = 72*1.5
cy = 72*1.5
dx = qp.mm(10*np.array([-1,1,1,-1,-1]))
dy = qp.mm(10*np.array([-1,-1,1,1,-1]))
qp.line(cx + dx, cy + dy)
