
import qplot as qp
import numpy as np

qp.figure('hatch', 3, 3)

qp.subplot(2, 1, 0)
for x in range(6):
    qp.brush('c')
    qp.pen('none')
    qp.fill([x, x+.8, x+.8, x], [0, 0, 1, 1])
    qp.pen('b', 3)
    
    qp.hatch([x, x+.8, x+.8, x], [0, 0, 1, 1], angle=x/6*np.pi)
    
qp.shrink()

typ = '-|\\/+x*:'
qp.subplot(2, 1, 1)
for x in range(len(typ)):
    qp.brush('c')
    qp.pen('none')
    qp.fill([x, x+.8, x+.8, x], [0, 0, 1, 1])
    qp.pen('b', 0)
    qp.marker('o', 2)
    
    qp.hatch([x, x+.8, x+.8, x], [0, 0, 1, 1], typ[x], offset=0)

qp.shrink()

